from __future__ import annotations

import argparse
import csv
import json
import os
import re
import socket
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # type: ignore

from mcp_client import MCPClient, MCPError


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "config" / "llm_router_policy.yaml"
SKILL_ROUTER_POLICY_PATH = ROOT / "config" / "skill_router_policy.yaml"
DEFAULT_DEEPSEEK_MODEL = "deepseek-v4-pro"
DEFAULT_FORBIDDEN_MODELS = {"deepseek-v4-flash", "deepseek-chat", "deepseek-reasoner"}
PSEUDO_TOOL_PATTERN = re.compile(r"</?\s*(read_file|list_files|write_file|edit_file|tool|function)\b", re.IGNORECASE)


class AgentRunnerError(RuntimeError):
    pass


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and (key not in os.environ or not os.environ.get(key, "").strip()):
            os.environ[key] = value


def load_yaml(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
    if not text.strip():
        return {}
    if yaml is not None:
        data = yaml.safe_load(text)
        return data or {}
    try:
        return json.loads(text)
    except Exception:
        from simple_yaml import loads as simple_yaml_load

        data = simple_yaml_load(text)
        return data or {}


def dump_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2), encoding="utf-8")


def read_text(path: Path, max_chars: int = 60000) -> str:
    if not path.exists() or not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="ignore")
    return text[:max_chars]


def safe_rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except Exception:
        return path.as_posix()


def is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except Exception:
        return False


def stage_from_state(workspace: Path) -> str:
    state = load_yaml(workspace / "workflow_state.yaml")
    return str(os.environ.get("MMWF_CURRENT_STAGE") or state.get("current_stage") or "current")


def pending_gate_from_state(workspace: Path) -> str:
    state = load_yaml(workspace / "workflow_state.yaml")
    return str(state.get("pending_gate") or "")


def sandbox_stage_prompt_path(stage: str, workspace: Path) -> Optional[Path]:
    base = workspace / "prompts" / "training_sandbox" / "stages"
    if not base.exists():
        return None
    direct = base / f"{stage}.md"
    if direct.exists():
        return direct
    matches = sorted(base.glob(f"*_{stage}.md"))
    return matches[0] if matches else None


def stage_prompt_path(stage: str, workspace: Path, mode: str = "") -> Optional[Path]:
    if mode == "training_sandbox":
        sandbox = sandbox_stage_prompt_path(stage, workspace)
        if sandbox:
            return sandbox
    policy = load_yaml(workspace / "config" / "skill_router_policy.yaml")
    mapping = (((policy.get("stage_identity_policy") or {}).get("stage_prompt_files")) or {})
    raw = mapping.get(stage)
    if raw:
        return workspace / str(raw)
    direct = workspace / "prompts" / "stages" / f"{stage}.md"
    if direct.exists():
        return direct
    matches = sorted((workspace / "prompts" / "stages").glob(f"*_{stage}.md")) if (workspace / "prompts" / "stages").exists() else []
    return matches[0] if matches else None


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def contains_any(text: str, needles: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(str(item).lower() in lowered for item in needles)


def first_matching_keyword(text: str, needles: Iterable[str]) -> str:
    lowered = text.lower()
    for item in needles:
        value = str(item)
        if value.lower() in lowered:
            return value
    return ""


def read_csv_dict(path: Path) -> List[Dict[str, str]]:
    if not path.exists() or not path.is_file():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(row) for row in csv.DictReader(f)]


def blocking_queue_rows(rows: Sequence[Mapping[str, str]]) -> List[Mapping[str, str]]:
    blockers: List[Mapping[str, str]] = []
    for row in rows:
        status = str(row.get("status") or "").strip().lower()
        severity = str(row.get("severity") or "").strip().lower()
        if status == "open" and severity in {"fail", "major"}:
            blockers.append(row)
    return blockers


def extract_prompt_paths(prompt_text: str, workspace: Path) -> List[Path]:
    candidates: List[Path] = []
    pattern = re.compile(r"([A-Za-z]:[^\s`]+|[^\s`]+(?:agent_revision_queue|gap_report)\.csv)", re.IGNORECASE)
    for raw in pattern.findall(prompt_text):
        cleaned = raw.strip().strip("`\"'")
        path = Path(cleaned)
        if not path.is_absolute():
            path = workspace / cleaned
        candidates.append(path)
    return candidates


def queue_paths_from_context(prompt_text: str, workspace: Path, run_dir: Optional[Path]) -> List[Path]:
    paths = extract_prompt_paths(prompt_text, workspace)
    if run_dir:
        paths.append(run_dir / "reports" / "agent_revision_queue.csv")
    paths.append(workspace / "reports" / "agent_revision_queue.csv")
    unique: List[Path] = []
    seen: set[str] = set()
    for path in paths:
        key = str(path)
        if key not in seen:
            unique.append(path)
            seen.add(key)
    return unique


def gap_dimension_for_task(run_dir: Optional[Path], task: Mapping[str, str]) -> str:
    if not run_dir:
        return ""
    note = str(task.get("notes") or "")
    match = re.search(r"from\s+(\S+)", note)
    gap_id = match.group(1) if match else ""
    for row in read_csv_dict(run_dir / "reports" / "gap_report.csv"):
        if gap_id and str(row.get("gap_id") or "") != gap_id:
            continue
        dimension = str(row.get("dimension") or "")
        if dimension:
            return dimension
    return ""


def training_depth_escalation_reason(prompt_text: str, workspace: Path, run_dir: Optional[Path]) -> str:
    for path in queue_paths_from_context(prompt_text, workspace, run_dir):
        blockers = blocking_queue_rows(read_csv_dict(path))
        if blockers:
            dimension = gap_dimension_for_task(run_dir, blockers[0])
            severity = str(blockers[0].get("severity") or "major").lower()
            return f"open_{severity}_gap:{dimension or blockers[0].get('task_id') or path.name}"
    prompt_keyword = first_matching_keyword(
        prompt_text,
        [
            "agent_revision_queue",
            "gap_report",
            "figure_density",
            "open major",
            "open fail",
            "差异报告",
            "图表密度",
            "未关闭修订",
            "合同冲突",
        ],
    )
    if prompt_keyword:
        return f"training_deep_keyword:{prompt_keyword}"
    return ""


def validate_model_name(policy: Mapping[str, Any], model_name: str) -> None:
    normalized = str(model_name or "").strip()
    lowered = normalized.lower()
    model_policy = policy.get("model_policy") or {}
    allowed = {str(item).strip().lower() for item in (model_policy.get("allow_models") or []) if str(item).strip()}
    forbidden = {str(item).strip().lower() for item in (model_policy.get("forbidden_models") or []) if str(item).strip()}
    if not forbidden:
        forbidden = set(DEFAULT_FORBIDDEN_MODELS)
    if lowered in forbidden:
        raise AgentRunnerError(
            f"forbidden DeepSeek model selected: {normalized}. "
            f"This workflow requires {model_policy.get('default_model') or DEFAULT_DEEPSEEK_MODEL}."
        )
    if allowed and lowered not in allowed:
        raise AgentRunnerError(f"model {normalized} is not in llm_router_policy.model_policy.allow_models")


def choose_profile(
    policy: Mapping[str, Any],
    stage: str,
    prompt_text: str,
    mode: str,
    workspace: Optional[Path] = None,
    run_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    routing = policy.get("routing") or {}
    stage_defaults = routing.get("stage_defaults") or {}
    profile_id = str(stage_defaults.get(stage) or routing.get("default_profile") or "standard")
    deep_candidates = set(str(item) for item in (routing.get("deep_stage_candidates") or []))
    deep_keywords = [str(item) for item in (routing.get("deep_keywords") or [])]
    matched_keyword = first_matching_keyword(prompt_text, deep_keywords)
    high_risk = bool(matched_keyword)
    depth_reason = ""
    if mode == "training_sandbox" and workspace is not None:
        depth_reason = training_depth_escalation_reason(prompt_text, workspace, run_dir)
    if depth_reason:
        profile_id = "deep"
    elif stage in deep_candidates and high_risk:
        profile_id = "deep"
        depth_reason = f"stage_keyword:{matched_keyword}"
    profiles = policy.get("profiles") or {}
    models = policy.get("models") or {}
    if profile_id not in profiles:
        raise AgentRunnerError(f"unknown profile in policy: {profile_id}")
    profile = dict(profiles[profile_id] or {})
    model_alias = str(profile.get("model") or "")
    model_name = str(models.get(model_alias) or model_alias)
    if not model_name:
        raise AgentRunnerError(f"profile {profile_id} has no model")
    validate_model_name(policy, model_name)
    return {
        "stage": stage,
        "mode": mode,
        "profile_id": profile_id,
        "model_alias": model_alias,
        "model": model_name,
        "thinking": bool(profile.get("thinking")),
        "reasoning_effort": profile.get("reasoning_effort"),
        "temperature": profile.get("temperature", 0.2),
        "high_risk_detected": high_risk,
        "matched_keyword": matched_keyword,
        "depth_escalation_reason": depth_reason,
    }


def build_chat_payload(policy: Mapping[str, Any], route: Mapping[str, Any], messages: Sequence[Mapping[str, str]]) -> Dict[str, Any]:
    validate_model_name(policy, str(route.get("model") or ""))
    provider = policy.get("provider") or {}
    payload: Dict[str, Any] = {
        "model": route["model"],
        "messages": [dict(item) for item in messages],
        "temperature": route.get("temperature", 0.2),
    }
    payload["thinking"] = {"type": "enabled" if route.get("thinking") else "disabled"}
    if route.get("reasoning_effort"):
        payload["reasoning_effort"] = route.get("reasoning_effort")
    if bool(provider.get("stream")):
        payload["stream"] = True
    return payload


def discover_image_candidates(prompt_text: str, workspace: Path, policy: Mapping[str, Any]) -> List[Path]:
    routing = policy.get("routing") or {}
    extensions = {str(item).lower() for item in (routing.get("image_extensions") or [])}
    image_keywords = [str(item) for item in (routing.get("image_keywords") or [])]
    max_candidates = int(routing.get("max_image_candidates") or 4)
    candidates: List[Path] = []

    pattern = re.compile(r"([^\s\"'<>]+\.(?:png|jpg|jpeg|webp|bmp|tif|tiff|gif))", re.IGNORECASE)
    for match in pattern.findall(prompt_text):
        path = Path(match)
        if not path.is_absolute():
            path = workspace / path
        if path.exists() and path.suffix.lower() in extensions and is_under(path, workspace):
            candidates.append(path.resolve())

    should_scan = contains_any(prompt_text, image_keywords)
    search_dirs = [workspace / str(raw) for raw in (routing.get("image_search_dirs") or [])]
    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        for path in sorted(search_dir.rglob("*")):
            if len(candidates) >= max_candidates:
                break
            if path.is_file() and path.suffix.lower() in extensions:
                if should_scan or "00_problem" in path.parts or "03_data" in path.parts:
                    candidates.append(path.resolve())

    unique: List[Path] = []
    seen: set[str] = set()
    for path in candidates:
        key = str(path)
        if key not in seen:
            unique.append(path)
            seen.add(key)
        if len(unique) >= max_candidates:
            break
    return unique


def call_vision_observations(policy: Mapping[str, Any], workspace: Path, images: Sequence[Path], prompt_text: str) -> List[Dict[str, Any]]:
    vision_cfg = policy.get("vision_mcp") or {}
    if not vision_cfg.get("enabled", True) or not images:
        return []
    command = [str(part) for part in (vision_cfg.get("command") or [])]
    if not command:
        return [{"image_path": str(path), "error": "vision_mcp.command is empty"} for path in images]
    tool_name = str(vision_cfg.get("tool_name") or "image_recognize")
    timeout = float(vision_cfg.get("timeout_seconds") or 60)
    observations: List[Dict[str, Any]] = []
    try:
        with MCPClient(command, cwd=workspace, timeout_seconds=timeout) as client:
            client.initialize()
            tool_names = {str(tool.get("name")) for tool in client.list_tools()}
            if tool_name not in tool_names:
                return [{"error": f"MCP tool not found: {tool_name}", "available_tools": sorted(tool_names)}]
            for path in images:
                result = client.call_tool(
                    tool_name,
                    {
                        "workspace": str(workspace),
                        "image_path": str(path),
                        "prompt": prompt_text[:2000],
                    },
                )
                observations.append(
                    {
                        "image_path": safe_rel(path, workspace),
                        "is_error": bool(result.get("isError")),
                        "structured": result.get("structuredContent") or {},
                        "content": result.get("content") or [],
                    }
                )
    except MCPError as exc:
        observations.append({"error": str(exc), "image_count": len(images)})
    return observations


def build_system_prompt(mode: str, stage: str, pending_gate: str, retry_note: str = "") -> str:
    formal_extra = ""
    if mode == "formal_assist":
        formal_extra = (
            "\nFormal assist constraints: do not confirm human gates, do not run --stage all, "
            "do not bypass contract validation, and do not directly edit protected deliverables."
        )
    training_extra = ""
    if mode == "training_sandbox":
        training_extra = (
            "\nTraining sandbox response protocol: output exactly one top-level JSON object and no prose, markdown fence, "
            "or pseudo-tool tag. Schema: {\"status\":\"ok|blocked\", \"summary\":\"short\", "
            "\"files\":[{\"path\":\"relative/path\", \"operation\":\"write|append\", \"content\":\"...\"}], "
            "\"unresolved\":[{\"issue\":\"...\", \"blocker\":\"...\"}]}. "
            "Do not use <read_file>, <list_files>, or any other tool-like XML tag. "
            "Do not write 00_problem/problem_statement.md or 00_problem/inbox/; put intake analysis in 01_task_analysis/."
        )
    if retry_note:
        training_extra += f"\nProtocol retry instruction: {retry_note}"
    return (
        "You are a controlled external agent for Math Modeling Workflow v3.2-MVP.\n"
        "Follow deep_sequential mode only. The workflow controller owns state; contracts and validation scripts "
        "are higher authority than model output. Treat MCP vision results as observations, not final paper facts.\n"
        f"Current stage: {stage}. Pending gate: {pending_gate or 'none'}.{formal_extra}{training_extra}\n"
        "If you propose file writes, place them in a JSON object with a top-level 'files' list of "
        "{path, content, operation}. Do not include secrets."
    )


def build_user_prompt(workspace: Path, prompt_path: Path, stage: str, observations: Sequence[Mapping[str, Any]], mode: str = "") -> Tuple[str, Dict[str, Any]]:
    agents = read_text(workspace / "AGENTS.md", 20000)
    state = read_text(workspace / "workflow_state.yaml", 12000)
    prompt_source = stage_prompt_path(stage, workspace, mode)
    stage_prompt = read_text(prompt_source or Path(), 30000)
    task_prompt = read_text(prompt_path, 60000)
    observation_text = json.dumps(list(observations), ensure_ascii=False, indent=2) if observations else "[]"
    parts = [
        "# Repository Rules",
        agents,
        "# Workflow State",
        state,
        "# Stage Prompt",
        stage_prompt,
        "# MCP Vision Observations",
        observation_text,
        "# User/Controller Task",
        task_prompt,
    ]
    combined = "\n\n".join(parts)
    lengths = {
        "agents_chars": len(agents),
        "state_chars": len(state),
        "stage_prompt_chars": len(stage_prompt),
        "stage_prompt_source": str(prompt_source or ""),
        "task_prompt_chars": len(task_prompt),
        "vision_observation_chars": len(observation_text),
        "total_estimated_tokens": estimate_tokens(combined),
    }
    return combined, lengths


def api_endpoint(policy: Mapping[str, Any]) -> str:
    provider = policy.get("provider") or {}
    load_env_file(ROOT / ".env")
    base_url = os.environ.get(str(provider.get("base_url_env") or "DEEPSEEK_BASE_URL"), "").strip()
    base_url = (base_url or str(provider.get("default_base_url") or "https://api.deepseek.com")).rstrip("/")
    path = str(provider.get("chat_path") or "/chat/completions")
    if not path.startswith("/"):
        path = "/" + path
    return base_url + path


def provider_timeout_config(policy: Mapping[str, Any]) -> Dict[str, int]:
    provider = policy.get("provider") or {}
    hard = int(provider.get("stream_hard_timeout_seconds") or provider.get("timeout_seconds") or 1800)
    return {
        "soft_timeout_seconds": int(provider.get("stream_soft_timeout_seconds") or 1200),
        "hard_timeout_seconds": hard,
        "first_chunk_timeout_seconds": int(provider.get("stream_first_chunk_timeout_seconds") or 600),
        "idle_timeout_seconds": int(provider.get("stream_idle_timeout_seconds") or 360),
        "heartbeat_seconds": max(1, int(provider.get("stream_heartbeat_seconds") or 30)),
        "request_timeout_seconds": int(provider.get("timeout_seconds") or hard),
    }


def provider_network_retry_config(policy: Mapping[str, Any]) -> Dict[str, float]:
    provider = policy.get("provider") or {}
    return {
        "count": max(0, int(provider.get("network_retry_count") or 0)),
        "backoff_seconds": max(0.0, float(provider.get("network_retry_backoff_seconds") or 0)),
    }


def is_retryable_deepseek_error(exc: BaseException) -> bool:
    message = str(exc).lower()
    if "deepseek http" in message:
        return False
    if "missing api key" in message:
        return False
    retry_markers = [
        "deepseek request failed",
        "winerror 10054",
        "connection reset",
        "remote host closed",
        "forcibly closed",
        "timed out",
        "timeout",
        "ssl",
        "eof occurred",
    ]
    return any(marker in message for marker in retry_markers)


def short_error(exc: BaseException, max_len: int = 300) -> str:
    text = str(exc).replace("\n", " ").strip()
    return text[:max_len]


def stream_timeout_reason(started: float, last_chunk: float, first_chunk_seen: bool, now: float, cfg: Mapping[str, int]) -> str:
    if now - started >= int(cfg.get("hard_timeout_seconds") or 1800):
        return "stream_hard_timeout"
    if not first_chunk_seen and now - started >= int(cfg.get("first_chunk_timeout_seconds") or 600):
        return "first_chunk_timeout"
    if first_chunk_seen and now - last_chunk >= int(cfg.get("idle_timeout_seconds") or 360):
        return "stream_idle_timeout"
    return ""


def parse_stream_payload(data: str) -> Dict[str, Any]:
    if data.strip() == "[DONE]":
        return {"done": True, "content": "", "reasoning_content_chars": 0, "finish_reason": "done", "usage": {}}
    obj = json.loads(data)
    choice = (obj.get("choices") or [{}])[0]
    delta = choice.get("delta") or choice.get("message") or {}
    reasoning = str(delta.get("reasoning_content") or "")
    return {
        "done": False,
        "content": str(delta.get("content") or ""),
        "reasoning_content_chars": len(reasoning),
        "finish_reason": choice.get("finish_reason"),
        "usage": obj.get("usage") or {},
    }


def append_stream_status(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    row = dict(payload)
    row["logged_at"] = datetime.now().isoformat(timespec="seconds")
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def stream_status_payload(
    event: str,
    started: float,
    last_chunk: float,
    chunk_count: int,
    content_chars: int,
    reasoning_content_chars: int,
    finish_reason: Any = None,
) -> Dict[str, Any]:
    now = time.monotonic()
    return {
        "event": event,
        "elapsed_seconds": round(now - started, 3),
        "chunk_count": chunk_count,
        "content_chars": content_chars,
        "reasoning_content_chars": reasoning_content_chars,
        "idle_seconds": round(now - last_chunk, 3),
        "finish_reason": finish_reason,
    }


def call_deepseek_stream(policy: Mapping[str, Any], payload: Mapping[str, Any], status_path: Path) -> Dict[str, Any]:
    provider = policy.get("provider") or {}
    api_key_env = str(provider.get("api_key_env") or "DEEPSEEK_API_KEY")
    api_key = os.environ.get(api_key_env, "").strip()
    if not api_key:
        raise AgentRunnerError(f"missing API key env: {api_key_env}")
    cfg = provider_timeout_config(policy)
    stream_payload = dict(payload)
    stream_payload["stream"] = True
    req = urllib.request.Request(
        api_endpoint(policy),
        data=json.dumps(stream_payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    started = time.monotonic()
    last_chunk = started
    next_heartbeat = started + int(cfg["heartbeat_seconds"])
    soft_warning_sent = False
    first_chunk_seen = False
    content_parts: List[str] = []
    reasoning_content_chars = 0
    chunk_count = 0
    finish_reason: Any = None
    usage: Dict[str, Any] = {}

    def heartbeat(event: str) -> None:
        append_stream_status(
            status_path,
            stream_status_payload(event, started, last_chunk, chunk_count, len("".join(content_parts)), reasoning_content_chars, finish_reason),
        )

    try:
        heartbeat("stream_start")
        with urllib.request.urlopen(req, timeout=int(cfg["first_chunk_timeout_seconds"])) as resp:
            try:
                resp.fp.raw._sock.settimeout(int(cfg["heartbeat_seconds"]))  # type: ignore[attr-defined]
            except Exception:
                pass
            while True:
                now = time.monotonic()
                reason = stream_timeout_reason(started, last_chunk, first_chunk_seen, now, cfg)
                if reason:
                    heartbeat(reason)
                    raise AgentRunnerError(reason)
                if not soft_warning_sent and now - started >= int(cfg["soft_timeout_seconds"]):
                    soft_warning_sent = True
                    heartbeat("long_thinking_warning")
                if now >= next_heartbeat:
                    heartbeat("stream_progress")
                    print(
                        json.dumps(
                            stream_status_payload("stream_progress", started, last_chunk, chunk_count, len("".join(content_parts)), reasoning_content_chars, finish_reason),
                            ensure_ascii=False,
                        ),
                        flush=True,
                    )
                    next_heartbeat = now + int(cfg["heartbeat_seconds"])

                try:
                    raw = resp.readline()
                except (socket.timeout, TimeoutError):
                    continue
                if not raw:
                    finish_reason = finish_reason or "stream_eof"
                    heartbeat("stream_eof")
                    break
                line = raw.decode("utf-8", errors="replace").strip()
                if not line or not line.startswith("data:"):
                    continue
                first_chunk_seen = True
                last_chunk = time.monotonic()
                data = line[len("data:") :].strip()
                try:
                    parsed = parse_stream_payload(data)
                except json.JSONDecodeError as exc:
                    heartbeat("stream_bad_json")
                    raise AgentRunnerError(f"stream_bad_json: {exc}") from exc
                chunk_count += 1
                if parsed.get("done"):
                    finish_reason = finish_reason or parsed.get("finish_reason") or "done"
                    heartbeat("stream_done")
                    break
                content = str(parsed.get("content") or "")
                if content:
                    content_parts.append(content)
                reasoning_content_chars += int(parsed.get("reasoning_content_chars") or 0)
                if parsed.get("finish_reason"):
                    finish_reason = parsed.get("finish_reason")
                if parsed.get("usage"):
                    usage = dict(parsed.get("usage") or {})
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[-1500:]
        raise AgentRunnerError(f"DeepSeek HTTP {exc.code}: {body}") from exc
    except Exception as exc:
        if isinstance(exc, AgentRunnerError):
            raise
        raise AgentRunnerError(f"DeepSeek request failed: {exc}") from exc
    content = "".join(content_parts)
    return {
        "choices": [{"message": {"content": content}, "finish_reason": finish_reason}],
        "usage": usage,
        "stream_meta": {
            "stream": True,
            "chunk_count": chunk_count,
            "content_chars": len(content),
            "reasoning_content_chars": reasoning_content_chars,
            "finish_reason": finish_reason,
            "status_log": str(status_path),
        },
    }


def call_deepseek(policy: Mapping[str, Any], payload: Mapping[str, Any], stream_status_path: Optional[Path] = None) -> Dict[str, Any]:
    provider = policy.get("provider") or {}
    if payload.get("stream") or bool(provider.get("stream")):
        if stream_status_path is None:
            raise AgentRunnerError("stream_status_path is required when streaming is enabled")
        return call_deepseek_stream(policy, payload, stream_status_path)
    api_key_env = str(provider.get("api_key_env") or "DEEPSEEK_API_KEY")
    api_key = os.environ.get(api_key_env, "").strip()
    if not api_key:
        raise AgentRunnerError(f"missing API key env: {api_key_env}")
    timeout = int(provider.get("timeout_seconds") or 120)
    req = urllib.request.Request(
        api_endpoint(policy),
        data=json.dumps(dict(payload), ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[-1500:]
        raise AgentRunnerError(f"DeepSeek HTTP {exc.code}: {body}") from exc
    except Exception as exc:
        raise AgentRunnerError(f"DeepSeek request failed: {exc}") from exc


def response_content(api_result: Mapping[str, Any]) -> Tuple[str, Dict[str, Any]]:
    choice = (api_result.get("choices") or [{}])[0]
    message = choice.get("message") or {}
    content = str(message.get("content") or "")
    usage = dict(api_result.get("usage") or {})
    meta = {
        "finish_reason": choice.get("finish_reason"),
        "usage": usage,
        "reasoning_content_chars": len(str(message.get("reasoning_content") or "")),
    }
    meta.update(dict(api_result.get("stream_meta") or {}))
    return content, meta


def extract_json_object(text: str) -> Optional[Dict[str, Any]]:
    stripped = text.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        try:
            value = json.loads(stripped)
            return value if isinstance(value, dict) else None
        except Exception:
            pass
    fenced = re.search(r"```json\s*(\{.*?\})\s*```", text, re.IGNORECASE | re.DOTALL)
    if fenced:
        try:
            value = json.loads(fenced.group(1))
            return value if isinstance(value, dict) else None
        except Exception:
            return None
    return None


def extract_strict_json_object(text: str) -> Tuple[Optional[Dict[str, Any]], List[str]]:
    stripped = text.strip()
    issues: List[str] = []
    if not stripped:
        return None, ["empty_response"]
    if PSEUDO_TOOL_PATTERN.search(stripped):
        issues.append("pseudo_tool_tag")
    if stripped.startswith("```"):
        issues.append("markdown_fence")
    if not (stripped.startswith("{") and stripped.endswith("}")):
        issues.append("not_top_level_json_object")
        return None, issues
    try:
        value = json.loads(stripped)
    except Exception as exc:
        issues.append(f"json_parse_error:{exc}")
        return None, issues
    if not isinstance(value, dict):
        issues.append("json_root_not_object")
        return None, issues
    return value, issues


def extract_file_actions(text: str) -> List[Dict[str, str]]:
    obj = extract_json_object(text)
    if not obj:
        return []
    raw_files = obj.get("files") or obj.get("file_writes") or []
    actions: List[Dict[str, str]] = []
    if not isinstance(raw_files, list):
        return actions
    for item in raw_files:
        if not isinstance(item, dict):
            continue
        path = str(item.get("path") or "").strip()
        content = str(item.get("content") or "")
        operation = str(item.get("operation") or "write").strip().lower()
        if path and operation in {"write", "append"}:
            actions.append({"path": path, "content": content, "operation": operation})
    return actions


def extract_file_actions_from_object(obj: Mapping[str, Any]) -> List[Dict[str, str]]:
    raw_files = obj.get("files") or obj.get("file_writes") or []
    actions: List[Dict[str, str]] = []
    if not isinstance(raw_files, list):
        return actions
    for item in raw_files:
        if not isinstance(item, dict):
            continue
        path = str(item.get("path") or "").strip()
        content = str(item.get("content") or "")
        operation = str(item.get("operation") or "write").strip().lower()
        if path and operation in {"write", "append"}:
            actions.append({"path": path, "content": content, "operation": operation})
    return actions


def stage_requires_file_actions(mode: str, stage: str) -> bool:
    if mode != "training_sandbox":
        return False
    return stage not in {"prior_retrieval"}


def protocol_issues_for_response(text: str, mode: str, stage: str) -> Tuple[List[Dict[str, str]], List[str]]:
    if mode != "training_sandbox":
        return extract_file_actions(text), []
    obj, issues = extract_strict_json_object(text)
    actions = extract_file_actions_from_object(obj or {})
    if obj is not None and "files" not in obj and "file_writes" not in obj:
        issues.append("missing_files_field")
    if stage_requires_file_actions(mode, stage) and not actions:
        issues.append("empty_file_actions")
    return actions, issues


def sanitized_call_id(value: str, fallback: str) -> str:
    raw = value.strip() or fallback
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", raw).strip("._")
    return cleaned or fallback


def force_deep_route(policy: Mapping[str, Any], route: Mapping[str, Any], reason: str) -> Dict[str, Any]:
    profiles = policy.get("profiles") or {}
    models = policy.get("models") or {}
    deep = dict(profiles.get("deep") or {})
    model_alias = str(deep.get("model") or route.get("model_alias") or "")
    model_name = str(models.get(model_alias) or model_alias or route.get("model") or "")
    validate_model_name(policy, model_name)
    updated = dict(route)
    updated.update(
        {
            "profile_id": "deep",
            "model_alias": model_alias,
            "model": model_name,
            "thinking": bool(deep.get("thinking", True)),
            "reasoning_effort": deep.get("reasoning_effort") or "max",
            "temperature": deep.get("temperature", 0.15),
            "depth_escalation_reason": reason,
        }
    )
    return updated


def path_matches_any(relative_path: str, patterns: Sequence[str]) -> bool:
    normalized = relative_path.replace("\\", "/").lstrip("/")
    for raw in patterns:
        pattern = str(raw).replace("\\", "/").lstrip("/")
        if pattern.endswith("/"):
            if normalized.startswith(pattern):
                return True
        elif normalized == pattern:
            return True
    return False


def is_write_allowed(target: Path, workspace: Path, mode: str, stage: str, policy: Mapping[str, Any]) -> Tuple[bool, str]:
    resolved = target.resolve()
    if not is_under(resolved, workspace):
        return False, "path escapes workspace"
    rel_path = safe_rel(resolved, workspace)
    permissions = policy.get("permissions") or {}
    always_forbidden = [str(item) for item in (permissions.get("always_forbidden_paths") or [])]
    if path_matches_any(rel_path, always_forbidden):
        return False, "path is always forbidden"
    mode_policy = permissions.get(mode) or {}
    if not bool(mode_policy.get("allow_workspace_writes")):
        return False, f"workspace writes disabled for mode {mode}"
    protected_inputs = [str(item) for item in (mode_policy.get("protected_input_paths") or [])]
    if protected_inputs and path_matches_any(rel_path, protected_inputs):
        return False, "training sandbox input source is protected"
    if mode == "formal_assist":
        protected = [str(item) for item in (permissions.get("protected_formal_paths") or [])]
        if path_matches_any(rel_path, protected):
            return False, "formal assist cannot write protected path"
    return True, "allowed"


def apply_file_actions(
    actions: Sequence[Mapping[str, str]],
    workspace: Path,
    mode: str,
    stage: str,
    policy: Mapping[str, Any],
) -> List[Dict[str, Any]]:
    permissions = policy.get("permissions") or {}
    mode_policy = permissions.get(mode) or {}
    if not bool(mode_policy.get("apply_file_actions")):
        return [
            {"path": action.get("path"), "operation": action.get("operation"), "applied": False, "reason": "apply_file_actions disabled"}
            for action in actions
        ]
    results: List[Dict[str, Any]] = []
    for action in actions:
        rel_path = str(action.get("path") or "")
        target = (workspace / rel_path).resolve()
        allowed, reason = is_write_allowed(target, workspace, mode, stage, policy)
        record: Dict[str, Any] = {"path": rel_path, "operation": action.get("operation"), "applied": False, "reason": reason}
        if allowed:
            target.parent.mkdir(parents=True, exist_ok=True)
            if action.get("operation") == "append" and target.exists():
                existing = target.read_text(encoding="utf-8", errors="ignore")
                target.write_text(existing + str(action.get("content") or ""), encoding="utf-8")
            else:
                target.write_text(str(action.get("content") or ""), encoding="utf-8")
            record.update({"applied": True, "resolved_path": safe_rel(target, workspace)})
        results.append(record)
    return results


def run_live(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    run_dir = Path(args.run_dir).resolve() if args.run_dir else workspace / "10_ai_logs" / f"deepseek_agent_{int(time.time())}"
    prompt_path = Path(args.prompt).resolve()
    if not prompt_path.exists():
        raise AgentRunnerError(f"prompt file does not exist: {prompt_path}")

    load_env_file(ROOT / ".env")
    load_env_file(workspace / ".env")
    policy = load_yaml(POLICY_PATH)
    stage = str(args.stage or "").strip() or stage_from_state(workspace)
    pending_gate = pending_gate_from_state(workspace)
    call_id = sanitized_call_id(str(args.call_id or ""), f"{stage}_{int(time.time())}")
    call_dir = run_dir / "deepseek_calls" / call_id
    call_dir.mkdir(parents=True, exist_ok=True)
    task_text = read_text(prompt_path, 60000)
    route = choose_profile(policy, stage, task_text, args.mode, workspace=workspace, run_dir=run_dir)
    images = discover_image_candidates(task_text, workspace, policy)
    observations = call_vision_observations(policy, workspace, images, task_text)
    logging_cfg = policy.get("logging") or {}
    mode_policy = (policy.get("permissions") or {}).get(args.mode) or {}
    retry_count = int(mode_policy.get("protocol_retry_count") or 0) if args.mode == "training_sandbox" else 0
    protocol_history: List[Dict[str, Any]] = []
    final_content = ""
    final_meta: Dict[str, Any] = {}
    final_actions: List[Dict[str, str]] = []
    final_action_results: List[Dict[str, Any]] = []
    final_route = route
    final_payload: Dict[str, Any] = {}
    final_request_manifest: Dict[str, Any] = {}
    final_protocol_issues: List[str] = []
    final_network_history: List[Dict[str, Any]] = []
    stream_status_path = call_dir / "deepseek_stream_status.jsonl"
    network_retry_cfg = provider_network_retry_config(policy)
    network_retry_count = int(network_retry_cfg["count"])
    network_retry_backoff = float(network_retry_cfg["backoff_seconds"])

    for attempt in range(1, retry_count + 2):
        attempt_route = route if attempt == 1 else force_deep_route(policy, route, f"protocol_retry:{','.join(final_protocol_issues)}")
        retry_note = ""
        if attempt > 1:
            retry_note = "Previous response violated protocol: " + ", ".join(final_protocol_issues) + ". Return bare JSON only with non-empty files."
        user_prompt, prompt_lengths = build_user_prompt(workspace, prompt_path, stage, observations, mode=args.mode)
        messages = [
            {"role": "system", "content": build_system_prompt(args.mode, stage, pending_gate, retry_note=retry_note)},
            {"role": "user", "content": user_prompt},
        ]
        network_history: List[Dict[str, Any]] = []
        last_network_error = ""
        payload: Dict[str, Any] = {}
        request_manifest: Dict[str, Any] = {}
        network_route = attempt_route
        api_result: Dict[str, Any] = {}
        for network_attempt in range(1, network_retry_count + 2):
            network_route = (
                attempt_route
                if network_attempt == 1
                else force_deep_route(policy, attempt_route, f"network_retry:{last_network_error or 'transient_error'}")
            )
            payload = build_chat_payload(policy, network_route, messages)
            request_manifest = {
                "provider": (policy.get("provider") or {}).get("name", "deepseek"),
                "model": network_route["model"],
                "profile_id": network_route["profile_id"],
                "depth_escalation_reason": network_route.get("depth_escalation_reason"),
                "stage": stage,
                "stage_override": bool(args.stage),
                "call_id": call_id,
                "attempt": attempt,
                "network_attempt": network_attempt,
                "network_retry_count": network_retry_count,
                "network_retry_backoff_seconds": network_retry_backoff,
                "network_history": network_history,
                "mode": args.mode,
                "max_iterations": args.max_iterations,
                "prompt_path": str(prompt_path),
                "workspace": str(workspace),
                "run_dir": str(run_dir),
                "call_dir": str(call_dir),
                "prompt_lengths": prompt_lengths,
                "thinking": payload.get("thinking"),
                "reasoning_effort": payload.get("reasoning_effort"),
                "stream": bool(payload.get("stream")),
                "stream_status_log": str(stream_status_path) if payload.get("stream") else "",
                "stream_timeout_config": provider_timeout_config(policy) if payload.get("stream") else {},
                "image_candidates": [safe_rel(path, workspace) for path in images],
                "vision_observation_count": len(observations),
                "api_key_logged": False,
            }
            dump_json(call_dir / f"attempt_{attempt:02d}_network_{network_attempt:02d}_route.json", network_route)
            dump_json(call_dir / f"attempt_{attempt:02d}_network_{network_attempt:02d}_request_manifest.json", request_manifest)
            dump_json(call_dir / f"attempt_{attempt:02d}_route.json", network_route)
            dump_json(call_dir / f"attempt_{attempt:02d}_request_manifest.json", request_manifest)
            try:
                api_result = call_deepseek(policy, payload, stream_status_path=stream_status_path if payload.get("stream") else None)
                break
            except AgentRunnerError as exc:
                retryable = is_retryable_deepseek_error(exc)
                error_record = {
                    "attempt": attempt,
                    "network_attempt": network_attempt,
                    "stage": stage,
                    "call_id": call_id,
                    "retryable": retryable,
                    "error": short_error(exc),
                    "profile_id": network_route.get("profile_id"),
                    "reasoning_effort": network_route.get("reasoning_effort"),
                }
                dump_json(call_dir / f"attempt_{attempt:02d}_network_{network_attempt:02d}_error.json", error_record)
                append_stream_status(stream_status_path, {"event": "network_error", **error_record})
                if not retryable or network_attempt > network_retry_count:
                    raise
                network_history.append(error_record)
                last_network_error = error_record["error"]
                append_stream_status(stream_status_path, {"event": "network_retry", "next_network_attempt": network_attempt + 1, **error_record})
                if network_retry_backoff:
                    time.sleep(network_retry_backoff)
        content, meta = response_content(api_result)
        (call_dir / f"attempt_{attempt:02d}_response.md").write_text(content + "\n", encoding="utf-8")
        actions, protocol_issues = protocol_issues_for_response(content, args.mode, stage)
        action_results: List[Dict[str, Any]] = []
        if not protocol_issues:
            action_results = apply_file_actions(actions, workspace, args.mode, stage, policy)
        attempt_record = {
            "action_count": len(actions),
            "results": action_results,
            "protocol_issues": protocol_issues,
            "network_history": network_history,
            "response_meta": meta,
        }
        dump_json(call_dir / f"attempt_{attempt:02d}_file_actions.json", attempt_record)
        final_content = content
        final_meta = meta
        final_actions = actions
        final_action_results = action_results
        final_route = network_route
        final_payload = payload
        final_request_manifest = request_manifest
        final_protocol_issues = protocol_issues
        final_network_history = network_history
        if not protocol_issues:
            break
        protocol_history.append({"attempt": attempt, "issues": protocol_issues})

    response_path = call_dir / str(logging_cfg.get("response_markdown") or "deepseek_response.md")
    response_path.write_text(final_content + "\n", encoding="utf-8")
    dump_json(call_dir / str(logging_cfg.get("route_manifest") or "deepseek_route.json"), final_route)
    dump_json(call_dir / str(logging_cfg.get("request_manifest") or "deepseek_request_manifest.json"), final_request_manifest)
    final_file_actions_payload = {
        "action_count": len(final_actions),
        "results": final_action_results,
        "protocol_issues": final_protocol_issues,
        "protocol_history": protocol_history,
        "network_history": final_network_history,
        "response_meta": final_meta,
    }
    dump_json(call_dir / str(logging_cfg.get("file_actions_manifest") or "deepseek_file_actions.json"), final_file_actions_payload)

    dump_json(run_dir / str(logging_cfg.get("route_manifest") or "deepseek_route.json"), final_route)
    dump_json(run_dir / str(logging_cfg.get("request_manifest") or "deepseek_request_manifest.json"), final_request_manifest)
    latest_response = run_dir / str(logging_cfg.get("response_markdown") or "deepseek_response.md")
    latest_response.write_text(final_content + "\n", encoding="utf-8")
    dump_json(run_dir / str(logging_cfg.get("file_actions_manifest") or "deepseek_file_actions.json"), final_file_actions_payload)
    if stream_status_path.exists():
        (run_dir / "deepseek_stream_status.jsonl").write_text(stream_status_path.read_text(encoding="utf-8", errors="ignore"), encoding="utf-8")

    if final_protocol_issues:
        dump_json(call_dir / "protocol_violation.json", {"call_id": call_id, "stage": stage, "issues": final_protocol_issues, "history": protocol_history})
        raise AgentRunnerError("response_protocol_violation: " + ",".join(final_protocol_issues))

    print(
        json.dumps(
            {
                "status": "completed",
                "stage": stage,
                "call_id": call_id,
                "profile_id": final_route["profile_id"],
                "model": final_route["model"],
                "response": str(response_path),
                "file_actions": final_action_results,
                "usage": final_meta.get("usage") or {},
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def run_self_test(offline: bool = True) -> int:
    policy = load_yaml(POLICY_PATH)
    cases = [
        ("latex_template", "generate the template", "light"),
        ("paper_draft", "draft section from contracts", "standard"),
        ("codegen", "fix high risk contract failure in model code", "deep"),
    ]
    results: Dict[str, Any] = {"cases": []}
    for stage, prompt, expected in cases:
        route = choose_profile(policy, stage, prompt, "training_sandbox")
        assert route["profile_id"] == expected, (stage, route)
        payload = build_chat_payload(policy, route, [{"role": "user", "content": prompt}])
        assert "DEEPSEEK_API_KEY" not in json.dumps(payload)
        assert payload["model"] == DEFAULT_DEEPSEEK_MODEL
        assert route["model"] == DEFAULT_DEEPSEEK_MODEL
        assert payload["thinking"]["type"] == "enabled"
        if expected in {"light", "standard"}:
            assert payload["reasoning_effort"] == "high"
        if expected == "deep":
            assert payload["reasoning_effort"] == "max"
        results["cases"].append({"stage": stage, "expected": expected, "model": route["model"]})

    for forbidden_model in sorted(DEFAULT_FORBIDDEN_MODELS):
        try:
            build_chat_payload(policy, {"model": forbidden_model}, [{"role": "user", "content": "test"}])
        except AgentRunnerError:
            results.setdefault("forbidden_models_rejected", []).append(forbidden_model)
        else:
            raise AssertionError(f"forbidden model was accepted: {forbidden_model}")

    parsed = parse_stream_payload('{"choices":[{"delta":{"reasoning_content":"thinking"},"finish_reason":null}]}')
    assert parsed["content"] == ""
    assert parsed["reasoning_content_chars"] == len("thinking")
    parsed = parse_stream_payload('{"choices":[{"delta":{"content":"answer"},"finish_reason":"stop"}],"usage":{"total_tokens":3}}')
    assert parsed["content"] == "answer"
    assert parsed["finish_reason"] == "stop"
    assert parsed["usage"]["total_tokens"] == 3
    assert parse_stream_payload("[DONE]")["done"] is True

    timeout_cfg = {
        "hard_timeout_seconds": 1800,
        "first_chunk_timeout_seconds": 600,
        "idle_timeout_seconds": 360,
    }
    assert stream_timeout_reason(0, 0, False, 601, timeout_cfg) == "first_chunk_timeout"
    assert stream_timeout_reason(0, 10, True, 371, timeout_cfg) == "stream_idle_timeout"
    assert stream_timeout_reason(0, 1700, True, 1801, timeout_cfg) == "stream_hard_timeout"
    results["stream_parser"] = "pass"

    strict_obj, strict_issues = extract_strict_json_object('{"status":"ok","files":[{"path":"11_review/x.md","content":"ok"}]}')
    assert strict_obj and not strict_issues
    _, strict_issues = extract_strict_json_object('```json\n{"files":[]}\n```')
    assert "markdown_fence" in strict_issues
    _, strict_issues = extract_strict_json_object('<read_file path="x"/>')
    assert "pseudo_tool_tag" in strict_issues and "not_top_level_json_object" in strict_issues
    actions, protocol_issues = protocol_issues_for_response('{"status":"ok","files":[]}', "training_sandbox", "paper_full")
    assert actions == [] and "empty_file_actions" in protocol_issues
    assert sanitized_call_id("initial 01/intake", "fallback") == "initial_01_intake"
    assert provider_network_retry_config({"provider": {"network_retry_count": 1, "network_retry_backoff_seconds": 2}})["count"] == 1
    assert is_retryable_deepseek_error(AgentRunnerError("DeepSeek request failed: [WinError 10054] remote host closed"))
    assert is_retryable_deepseek_error(AgentRunnerError("DeepSeek request failed: timed out"))
    assert not is_retryable_deepseek_error(AgentRunnerError("DeepSeek HTTP 402: insufficient balance"))
    results["strict_protocol"] = "pass"

    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        (workspace / "09_paper").mkdir()
        run_dir = workspace / "run"
        (run_dir / "reports").mkdir(parents=True)
        with (run_dir / "reports" / "agent_revision_queue.csv").open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["task_id", "severity", "target_artifact", "issue_summary", "proposed_action", "acceptance_check", "status", "notes"],
            )
            writer.writeheader()
            writer.writerow(
                {
                    "task_id": "T1",
                    "severity": "major",
                    "target_artifact": "09_paper/full_draft.md",
                    "issue_summary": "our_count=1",
                    "proposed_action": "Add result-bound figures.",
                    "acceptance_check": "Figure mentions are backed.",
                    "status": "open",
                    "notes": "from GAP-002",
                }
            )
        with (run_dir / "reports" / "gap_report.csv").open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["gap_id", "dimension"])
            writer.writeheader()
            writer.writerow({"gap_id": "GAP-002", "dimension": "figure_density"})
        deep_route = choose_profile(
            policy,
            "paper_draft",
            "Use agent_revision_queue.csv to address open major items.",
            "training_sandbox",
            workspace=workspace,
            run_dir=run_dir,
        )
        assert deep_route["profile_id"] == "deep", deep_route
        assert deep_route["reasoning_effort"] == "max", deep_route
        assert deep_route["depth_escalation_reason"] == "open_major_gap:figure_density", deep_route
        results["training_queue_deep_escalation"] = "pass"

        allowed, _ = is_write_allowed(workspace / "09_paper" / "draft.md", workspace, "training_sandbox", "paper_draft", policy)
        assert allowed
        denied, reason = is_write_allowed(workspace / "workflow_state.yaml", workspace, "training_sandbox", "paper_draft", policy)
        assert not denied and "forbidden" in reason
        denied, reason = is_write_allowed(workspace / "09_paper" / "draft.md", workspace, "formal_assist", "paper_draft", policy)
        assert not denied and "disabled" in reason

        image = workspace / "input.png"
        image.write_bytes(b"\x89PNG\r\n\x1a\n")
        env = os.environ.copy()
        env["VISION_OFFLINE"] = "1"
        with MCPClient(["python", str(ROOT / "mcp_servers" / "vision_server.py")], cwd=workspace, env=env, timeout_seconds=10) as client:
            client.initialize()
            tools = client.list_tools()
            assert any(tool.get("name") == "image_recognize" for tool in tools)
            call = client.call_tool("image_recognize", {"workspace": str(workspace), "image_path": str(image)})
            assert not call.get("isError")
            assert (call.get("structuredContent") or {}).get("source") == "offline_metadata"
    results["mcp_offline"] = "pass"
    print(json.dumps({"status": "pass", "offline": offline, **results}, ensure_ascii=False, indent=2))
    return 0


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Controlled DeepSeek V4 external agent runner.")
    parser.add_argument("--prompt", default="")
    parser.add_argument("--workspace", default=str(ROOT))
    parser.add_argument("--run-dir", default="")
    parser.add_argument("--mode", default="training_sandbox", choices=["training_sandbox", "formal_assist"])
    parser.add_argument("--max-iterations", type=int, default=1)
    parser.add_argument("--stage", default="")
    parser.add_argument("--call-id", default="")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--offline", action="store_true")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = parse_args(argv)
    try:
        if args.self_test:
            raise SystemExit(run_self_test(offline=args.offline))
        if not args.prompt:
            raise AgentRunnerError("--prompt is required unless --self-test is used")
        raise SystemExit(run_live(args))
    except AgentRunnerError as exc:
        print(json.dumps({"status": "failed", "failure_code": "DEEPSEEK_AGENT_ERROR", "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
