from __future__ import annotations

import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Mapping, Optional


ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff", ".gif"}
DEFAULT_MAX_BYTES = 10 * 1024 * 1024


def json_response(request_id: Any, result: Optional[Mapping[str, Any]] = None, error: Optional[Mapping[str, Any]] = None) -> None:
    payload: Dict[str, Any] = {"jsonrpc": "2.0", "id": request_id}
    if error:
        payload["error"] = dict(error)
    else:
        payload["result"] = dict(result or {})
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def resolve_workspace_path(workspace: str, image_path: str) -> Path:
    workspace_root = Path(workspace or os.getcwd()).resolve()
    candidate = Path(image_path)
    if not candidate.is_absolute():
        candidate = workspace_root / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(workspace_root)
    except Exception as exc:
        raise ValueError("image_path must stay inside workspace") from exc
    return resolved


def validate_image_path(workspace: str, image_path: str, max_bytes: int) -> Path:
    path = resolve_workspace_path(workspace, image_path)
    if not path.exists() or not path.is_file():
        raise ValueError("image_path does not exist")
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(f"unsupported image extension: {path.suffix}")
    size = path.stat().st_size
    if size > max_bytes:
        raise ValueError(f"image exceeds max bytes: {size} > {max_bytes}")
    return path


def image_to_data_url(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(str(path))
    mime_type = mime_type or "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{data}"


def offline_result(path: Path, prompt: str, risk: str = "") -> Dict[str, Any]:
    return {
        "summary": f"Offline image metadata only: {path.name}, {path.stat().st_size} bytes.",
        "ocr_text": "",
        "objects": [],
        "table_or_chart_clues": [],
        "confidence": "metadata_only",
        "risks": [risk or "VISION_OFFLINE or missing VISION_API_KEY; no visual semantics were inferred."],
        "source": "offline_metadata",
        "prompt": prompt,
        "image_path": str(path),
    }


def call_openai_compatible_vision(path: Path, prompt: str, timeout_seconds: int = 120) -> Dict[str, Any]:
    api_key = os.environ.get("VISION_API_KEY", "").strip()
    base_url = os.environ.get("VISION_BASE_URL", "").strip().rstrip("/")
    model = os.environ.get("VISION_MODEL", "").strip()
    if os.environ.get("VISION_OFFLINE", "").strip().lower() in {"1", "true", "yes"}:
        return offline_result(path, prompt)
    if not api_key or not base_url or not model:
        return offline_result(path, prompt, "Vision backend env is incomplete.")

    endpoint = base_url + "/chat/completions"
    instruction = (
        "Return compact JSON with keys: summary, ocr_text, objects, "
        "table_or_chart_clues, confidence, risks. Treat the image as evidence "
        "for a math modeling workflow, not as a final paper conclusion."
    )
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": instruction + "\n\nUser prompt: " + (prompt or "Analyze this image.")},
                    {"type": "image_url", "image_url": {"url": image_to_data_url(path)}},
                ],
            }
        ],
        "temperature": 0.0,
    }
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[-1000:]
        raise RuntimeError(f"vision backend HTTP {exc.code}: {body}") from exc

    content = (((data.get("choices") or [{}])[0].get("message") or {}).get("content") or "").strip()
    try:
        parsed = json.loads(content)
        if isinstance(parsed, dict):
            parsed.setdefault("source", "vision_api")
            parsed.setdefault("image_path", str(path))
            return parsed
    except Exception:
        pass
    return {
        "summary": content,
        "ocr_text": "",
        "objects": [],
        "table_or_chart_clues": [],
        "confidence": "backend_text",
        "risks": ["Vision backend did not return structured JSON."],
        "source": "vision_api",
        "image_path": str(path),
    }


def tool_schema() -> Dict[str, Any]:
    return {
        "name": "image_recognize",
        "description": "Analyze one image inside the workspace and return structured observation JSON.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "workspace": {"type": "string"},
                "image_path": {"type": "string"},
                "prompt": {"type": "string"},
                "max_bytes": {"type": "integer"},
            },
            "required": ["workspace", "image_path"],
        },
    }


def handle_tools_call(arguments: Mapping[str, Any]) -> Dict[str, Any]:
    workspace = str(arguments.get("workspace") or os.getcwd())
    image_path = str(arguments.get("image_path") or "")
    prompt = str(arguments.get("prompt") or "")
    max_bytes = int(arguments.get("max_bytes") or os.environ.get("VISION_MAX_IMAGE_BYTES") or DEFAULT_MAX_BYTES)
    path = validate_image_path(workspace, image_path, max_bytes)
    result = call_openai_compatible_vision(path, prompt)
    return {
        "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}],
        "structuredContent": result,
        "isError": False,
    }


def handle_request(request: Mapping[str, Any]) -> Dict[str, Any]:
    method = str(request.get("method") or "")
    params = dict(request.get("params") or {})
    if method == "initialize":
        return {
            "protocolVersion": params.get("protocolVersion") or "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "math-workflow-vision", "version": "v1"},
        }
    if method == "tools/list":
        return {"tools": [tool_schema()]}
    if method == "tools/call":
        name = str(params.get("name") or "")
        if name != "image_recognize":
            return {"content": [{"type": "text", "text": f"unknown tool: {name}"}], "isError": True}
        try:
            return handle_tools_call(dict(params.get("arguments") or {}))
        except Exception as exc:
            return {"content": [{"type": "text", "text": str(exc)}], "isError": True}
    return {"content": [{"type": "text", "text": f"unknown method: {method}"}], "isError": True}


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            result = handle_request(request)
            json_response(request.get("id"), result=result)
        except Exception as exc:
            json_response(None, error={"code": -32603, "message": str(exc)})


if __name__ == "__main__":
    main()
