from __future__ import annotations

import argparse
import json
import os
import re
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
        if key and key not in os.environ:
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


def stage_prompt_path(stage: str, workspace: Path) -> Optional[Path]:
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


def choose_profile(policy: Mapping[str, Any], stage: str, prompt_text: str, mode: str) -> Dict[str, Any]:
    routing = policy.get("routing") or {}
    stage_defaults = routing.get("stage_defaults") or {}
    profile_id = str(stage_defaults.get(stage) or routing.get("default_profile") or "standard")
    deep_candidates = set(str(item) for item in (routing.get("deep_stage_candidates") or []))
    deep_keywords = [str(item) for item in (routing.get("deep_keywords") or [])]
    high_risk = contains_any(prompt_text, deep_keywords)
    if stage in deep_candidates and high_risk:
        profile_id = "deep"
    profiles = policy.get("profiles") or {}
    models = policy.get("models") or {}
    if profile_id not in profiles:
        raise AgentRunnerError(f"unknown profile in policy: {profile_id}")
    profile = dict(profiles[profile_id] or {})
    model_alias = str(profile.get("model") or "")
    model_name = str(models.get(model_alias) or model_alias)
    if not model_name:
        raise AgentRunnerError(f"profile {profile_id} has no model")
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
    }


def build_chat_payload(policy: Mapping[str, Any], route: Mapping[str, Any], messages: Sequence[Mapping[str, str]]) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "model": route["model"],
        "messages": [dict(item) for item in messages],
        "temperature": route.get("temperature", 0.2),
    }
    payload["thinking"] = {"type": "enabled" if route.get("thinking") else "disabled"}
    if route.get("reasoning_effort"):
        payload["reasoning_effort"] = route.get("reasoning_effort")
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


def build_system_prompt(mode: str, stage: str, pending_gate: str) -> str:
    formal_extra = ""
    if mode == "formal_assist":
        formal_extra = (
            "\nFormal assist constraints: do not confirm human gates, do not run --stage all, "
            "do not bypass contract validation, and do not directly edit protected deliverables."
        )
    return (
        "You are a controlled external agent for Math Modeling Workflow v3.2-MVP.\n"
        "Follow deep_sequential mode only. The workflow controller owns state; contracts and validation scripts "
        "are higher authority than model output. Treat MCP vision results as observations, not final paper facts.\n"
        f"Current stage: {stage}. Pending gate: {pending_gate or 'none'}.{formal_extra}\n"
        "If you propose file writes, place them in a JSON object with a top-level 'files' list of "
        "{path, content, operation}. Do not include secrets."
    )


def build_user_prompt(workspace: Path, prompt_path: Path, stage: str, observations: Sequence[Mapping[str, Any]]) -> Tuple[str, Dict[str, int]]:
    agents = read_text(workspace / "AGENTS.md", 20000)
    state = read_text(workspace / "workflow_state.yaml", 12000)
    stage_prompt = read_text(stage_prompt_path(stage, workspace) or Path(), 30000)
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


def call_deepseek(policy: Mapping[str, Any], payload: Mapping[str, Any]) -> Dict[str, Any]:
    provider = policy.get("provider") or {}
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
    stage = stage_from_state(workspace)
    pending_gate = pending_gate_from_state(workspace)
    task_text = read_text(prompt_path, 60000)
    route = choose_profile(policy, stage, task_text, args.mode)
    images = discover_image_candidates(task_text, workspace, policy)
    observations = call_vision_observations(policy, workspace, images, task_text)
    user_prompt, prompt_lengths = build_user_prompt(workspace, prompt_path, stage, observations)
    messages = [
        {"role": "system", "content": build_system_prompt(args.mode, stage, pending_gate)},
        {"role": "user", "content": user_prompt},
    ]
    payload = build_chat_payload(policy, route, messages)

    request_manifest = {
        "provider": (policy.get("provider") or {}).get("name", "deepseek"),
        "model": route["model"],
        "profile_id": route["profile_id"],
        "stage": stage,
        "mode": args.mode,
        "max_iterations": args.max_iterations,
        "prompt_path": str(prompt_path),
        "workspace": str(workspace),
        "run_dir": str(run_dir),
        "prompt_lengths": prompt_lengths,
        "thinking": payload.get("thinking"),
        "reasoning_effort": payload.get("reasoning_effort"),
        "image_candidates": [safe_rel(path, workspace) for path in images],
        "vision_observation_count": len(observations),
        "api_key_logged": False,
    }
    logging_cfg = policy.get("logging") or {}
    dump_json(run_dir / str(logging_cfg.get("route_manifest") or "deepseek_route.json"), route)
    dump_json(run_dir / str(logging_cfg.get("request_manifest") or "deepseek_request_manifest.json"), request_manifest)

    api_result = call_deepseek(policy, payload)
    content, meta = response_content(api_result)
    response_path = run_dir / str(logging_cfg.get("response_markdown") or "deepseek_response.md")
    response_path.parent.mkdir(parents=True, exist_ok=True)
    response_path.write_text(content + "\n", encoding="utf-8")
    actions = extract_file_actions(content)
    action_results = apply_file_actions(actions, workspace, args.mode, stage, policy)
    dump_json(
        run_dir / str(logging_cfg.get("file_actions_manifest") or "deepseek_file_actions.json"),
        {"action_count": len(actions), "results": action_results, "response_meta": meta},
    )
    print(
        json.dumps(
            {
                "status": "completed",
                "stage": stage,
                "profile_id": route["profile_id"],
                "model": route["model"],
                "response": str(response_path),
                "file_actions": action_results,
                "usage": meta.get("usage") or {},
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
        if expected == "light":
            assert payload["thinking"]["type"] == "disabled"
        if expected == "deep":
            assert payload["reasoning_effort"] == "max"
        results["cases"].append({"stage": stage, "expected": expected, "model": route["model"]})

    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        (workspace / "09_paper").mkdir()
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
