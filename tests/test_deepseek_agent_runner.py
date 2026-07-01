from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from deepseek_agent_runner import (  # noqa: E402
    apply_file_actions,
    build_chat_payload,
    choose_profile,
    extract_strict_json_object,
    extract_file_actions,
    is_write_allowed,
    load_yaml,
    protocol_issues_for_response,
    parse_stream_payload,
    sanitized_call_id,
    stream_timeout_reason,
)


POLICY = load_yaml(ROOT / "config" / "llm_router_policy.yaml")


def test_stage_defaults_route_to_expected_profiles() -> None:
    assert choose_profile(POLICY, "latex_template", "generate template", "training_sandbox")["profile_id"] == "light"
    assert choose_profile(POLICY, "paper_draft", "draft section", "training_sandbox")["profile_id"] == "standard"
    assert choose_profile(POLICY, "codegen", "fix high risk contract failure", "training_sandbox")["profile_id"] == "deep"


def test_payload_uses_configured_model_and_thinking_controls() -> None:
    light = choose_profile(POLICY, "latex_template", "simple", "training_sandbox")
    light_payload = build_chat_payload(POLICY, light, [{"role": "user", "content": "hello"}])
    assert light_payload["model"] == "deepseek-v4-pro"
    assert light_payload["thinking"] == {"type": "enabled"}
    assert light_payload["reasoning_effort"] == "high"
    assert light_payload["stream"] is True

    deep = choose_profile(POLICY, "revision", "high risk failure in contract", "training_sandbox")
    deep_payload = build_chat_payload(POLICY, deep, [{"role": "user", "content": "hello"}])
    assert deep_payload["model"] == "deepseek-v4-pro"
    assert deep_payload["thinking"] == {"type": "enabled"}
    assert deep_payload["reasoning_effort"] == "max"


def test_training_revision_queue_forces_deep_profile(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    reports = run_dir / "reports"
    reports.mkdir(parents=True)
    (reports / "agent_revision_queue.csv").write_text(
        "task_id,severity,target_artifact,issue_summary,proposed_action,acceptance_check,status,notes\n"
        "T1,major,09_paper/full_draft.md,our_count=1,Add result-bound figures.,Figure mentions are backed.,open,from GAP-002\n",
        encoding="utf-8",
    )
    (reports / "gap_report.csv").write_text("gap_id,dimension\nGAP-002,figure_density\n", encoding="utf-8")
    route = choose_profile(
        POLICY,
        "paper_draft",
        "Use agent_revision_queue.csv and fix open major gaps.",
        "training_sandbox",
        workspace=tmp_path,
        run_dir=run_dir,
    )
    assert route["profile_id"] == "deep"
    assert route["reasoning_effort"] == "max"
    assert route["depth_escalation_reason"] == "open_major_gap:figure_density"


def test_stream_parser_and_timeout_events() -> None:
    reasoning = parse_stream_payload('{"choices":[{"delta":{"reasoning_content":"thinking"},"finish_reason":null}]}')
    assert reasoning["content"] == ""
    assert reasoning["reasoning_content_chars"] == len("thinking")

    content = parse_stream_payload('{"choices":[{"delta":{"content":"done"},"finish_reason":"stop"}],"usage":{"total_tokens":5}}')
    assert content["content"] == "done"
    assert content["finish_reason"] == "stop"
    assert content["usage"]["total_tokens"] == 5
    assert parse_stream_payload("[DONE]")["done"] is True

    cfg = {"hard_timeout_seconds": 1800, "first_chunk_timeout_seconds": 600, "idle_timeout_seconds": 360}
    assert stream_timeout_reason(0, 0, False, 601, cfg) == "first_chunk_timeout"
    assert stream_timeout_reason(0, 10, True, 371, cfg) == "stream_idle_timeout"
    assert stream_timeout_reason(0, 1700, True, 1801, cfg) == "stream_hard_timeout"


def test_payload_never_contains_api_key_value(monkeypatch) -> None:
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-secret")
    route = choose_profile(POLICY, "paper_full", "draft", "training_sandbox")
    payload = build_chat_payload(POLICY, route, [{"role": "user", "content": "hello"}])
    assert "sk-test-secret" not in json.dumps(payload)


def test_formal_assist_cannot_write_protected_or_any_workspace_file(tmp_path: Path) -> None:
    target = tmp_path / "09_paper" / "draft.md"
    allowed, reason = is_write_allowed(target, tmp_path, "formal_assist", "paper_draft", POLICY)
    assert not allowed
    assert "disabled" in reason

    state_target = tmp_path / "workflow_state.yaml"
    allowed, reason = is_write_allowed(state_target, tmp_path, "training_sandbox", "paper_draft", POLICY)
    assert not allowed
    assert "forbidden" in reason

    problem_target = tmp_path / "00_problem" / "problem_statement.md"
    allowed, reason = is_write_allowed(problem_target, tmp_path, "training_sandbox", "intake", POLICY)
    assert not allowed
    assert "input source" in reason


def test_training_sandbox_applies_safe_file_actions(tmp_path: Path) -> None:
    response = json.dumps({"files": [{"path": "11_review/note.md", "content": "ok", "operation": "write"}]})
    actions = extract_file_actions(response)
    results = apply_file_actions(actions, tmp_path, "training_sandbox", "auto_review", POLICY)
    assert results[0]["applied"] is True
    assert (tmp_path / "11_review" / "note.md").read_text(encoding="utf-8") == "ok"


def test_training_sandbox_denies_workspace_escape(tmp_path: Path) -> None:
    actions = [{"path": "../escape.txt", "content": "bad", "operation": "write"}]
    results = apply_file_actions(actions, tmp_path, "training_sandbox", "auto_review", POLICY)
    assert results[0]["applied"] is False
    assert "escapes" in results[0]["reason"]


def test_strict_training_protocol_rejects_pseudo_tools_and_empty_actions() -> None:
    obj, issues = extract_strict_json_object('{"status":"ok","files":[{"path":"11_review/a.md","content":"ok"}]}')
    assert obj
    assert issues == []

    obj, issues = extract_strict_json_object('```json\n{"files":[]}\n```')
    assert obj is None
    assert "markdown_fence" in issues

    obj, issues = extract_strict_json_object('<read_file path="x"/>')
    assert obj is None
    assert "pseudo_tool_tag" in issues

    actions, issues = protocol_issues_for_response('{"status":"ok","files":[]}', "training_sandbox", "paper_full")
    assert actions == []
    assert "empty_file_actions" in issues

    assert sanitized_call_id("iteration 02/paper_full", "fallback") == "iteration_02_paper_full"
