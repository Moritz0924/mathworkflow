from __future__ import annotations

import json
import re
import shutil
import uuid
import csv
from pathlib import Path
from typing import Any, Dict, Mapping

import yaml

from .config import read_policy
from .context import build_context_manifest, file_sha256, render_context_snapshot
from .errors import WorkflowError
from .state import add_history, now_iso, read_state, write_state
from .validators import validate_stage


def handoff_root(root: Path) -> Path:
    return root / "10_ai_logs" / "handoffs"


def _validate_handoff_id(handoff_id: str) -> str:
    value = str(handoff_id or "")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", value):
        raise WorkflowError("invalid handoff_id; use 1-64 letters, digits, dots, underscores, or hyphens")
    return value


def read_manifest(root: Path, handoff_id: str) -> Dict[str, Any]:
    handoff_id = _validate_handoff_id(handoff_id)
    path = handoff_root(root) / handoff_id / "manifest.yaml"
    if not path.exists():
        raise WorkflowError(f"unknown handoff_id: {handoff_id}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def write_manifest(root: Path, handoff_id: str, manifest: Dict[str, Any]) -> None:
    handoff_id = _validate_handoff_id(handoff_id)
    path = handoff_root(root) / handoff_id / "manifest.yaml"
    path.write_text(yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False), encoding="utf-8")


def _new_handoff_id() -> str:
    return f"H-{uuid.uuid4().hex[:12].upper()}"


def _response_header(manifest: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            f"protocol: {manifest['protocol']}",
            f"project_id: {manifest['project_id']}",
            f"stage: {manifest['stage']}",
            f"handoff_id: {manifest['handoff_id']}",
            f"context_sha256: {manifest['context_sha256']}",
            "---",
        ]
    )


def prepare_handoff(root: Path, target: str, handoff_id: str | None = None) -> Dict[str, Any]:
    policy = read_policy(root)
    state = read_state(root)
    stage = state["current_stage"]
    contract = (policy.get("stage_contracts") or {}).get(stage) or {}
    if target == "chatgpt":
        retrying_blocked = state["status"] == "blocked"
        if state["status"] not in {"pending_chatgpt", "blocked"} or state.get("pending_gate"):
            raise WorkflowError(f"cannot prepare ChatGPT handoff while status is {state['status']}")
        if retrying_blocked:
            state["status"] = "pending_chatgpt"
            state["active_handoff_id"] = None
            state["context_sha256"] = None
            add_history(state, "blocked_stage_retry_started", stage=stage)
        handoff_id = _validate_handoff_id(handoff_id or _new_handoff_id())
        directory = handoff_root(root) / handoff_id
        if directory.exists():
            raise WorkflowError(f"handoff already exists: {handoff_id}")
        directory.mkdir(parents=True)
        context = build_context_manifest(root, contract.get("context_paths") or [])
        manifest = {
            "schema_version": "v1",
            "protocol": policy.get("protocol") or "mmwf-handoff/v1",
            "project_id": state["project_id"],
            "stage": stage,
            "handoff_id": handoff_id,
            "revision": 1 + sum(1 for row in state.get("history") or [] if row.get("event") == "chatgpt_handoff_prepared" and row.get("stage") == stage),
            "context_sha256": context["context_sha256"],
            "context_files": context["files"],
            "excluded_files": context["excluded"],
            "created_at": now_iso(),
            "status": "awaiting_chatgpt",
        }
        write_manifest(root, handoff_id, manifest)
        template = root / "prompts" / "formal_v4" / stage / "chatgpt.md"
        if not template.exists():
            raise WorkflowError(f"ChatGPT prompt template is missing: {template}")
        sections = [template.read_text(encoding="utf-8").strip()]
        if manifest.get("revision", 1) > 1:
            revision_block = _build_revision_block(root, stage)
            if revision_block:
                sections.append(revision_block)
        sections.append(
            "## Response metadata\n\nBegin the response with this exact metadata block:\n\n" + _response_header(manifest)
        )
        sections.append("## Verified context\n" + render_context_snapshot(root, context))
        prompt = "\n\n".join(
            [
                template.read_text(encoding="utf-8").strip(),
                *sections[1:],
            ]
        )
        (directory / "chatgpt_prompt.md").write_text(prompt.rstrip() + "\n", encoding="utf-8")
        state["active_handoff_id"] = handoff_id
        state["context_sha256"] = context["context_sha256"]
        add_history(state, "chatgpt_handoff_prepared", stage=stage, handoff_id=handoff_id)
        write_state(root, state)
        return manifest

    if target == "codex":
        handoff_id = _validate_handoff_id(str(handoff_id or state.get("active_handoff_id") or ""))
        if state["status"] != "pending_codex" or handoff_id != state.get("active_handoff_id"):
            raise WorkflowError("Codex handoff requires the active imported ChatGPT response")
        directory = handoff_root(root) / str(handoff_id)
        response = directory / "chatgpt_response.md"
        if not response.exists():
            raise WorkflowError("ChatGPT response has not been imported")
        template = root / "prompts" / "formal_v4" / stage / "codex.md"
        if not template.exists():
            raise WorkflowError(f"Codex prompt template is missing: {template}")
        task = "\n\n".join(
            [
                template.read_text(encoding="utf-8").strip(),
                f"## Handoff\n\n- handoff_id: `{handoff_id}`\n- response: `{response.relative_to(root).as_posix()}`",
                "## Required receipt\n\nReturn pass, needs_revision, or blocked with checks, artifacts, contract_rows, conflicts, and next_action.",
            ]
        )
        (directory / "codex_task.md").write_text(task.rstrip() + "\n", encoding="utf-8")
        manifest = read_manifest(root, str(handoff_id))
        manifest["status"] = "awaiting_codex"
        write_manifest(root, str(handoff_id), manifest)
        return manifest
    raise WorkflowError("target must be chatgpt or codex")


def _parse_frontmatter(text: str) -> Dict[str, Any]:
    if not text.startswith("---\n"):
        raise WorkflowError("ChatGPT response must start with YAML frontmatter")
    marker = text.find("\n---", 4)
    if marker < 0:
        raise WorkflowError("ChatGPT response frontmatter is not closed")
    return yaml.safe_load(text[4:marker]) or {}


def import_chatgpt_response(root: Path, handoff_id: str, response_path: Path) -> Dict[str, Any]:
    handoff_id = _validate_handoff_id(handoff_id)
    directory = handoff_root(root) / handoff_id
    target = directory / "chatgpt_response.md"
    if target.exists():
        raise WorkflowError("ChatGPT response already imported; create a new revision")
    state = read_state(root)
    if state["status"] != "pending_chatgpt" or state.get("active_handoff_id") != handoff_id:
        raise WorkflowError("response does not belong to the active ChatGPT handoff")
    manifest = read_manifest(root, handoff_id)
    text = response_path.read_text(encoding="utf-8")
    metadata = _parse_frontmatter(text)
    for key in ["protocol", "project_id", "stage", "handoff_id", "context_sha256"]:
        if str(metadata.get(key) or "") != str(manifest.get(key) or ""):
            raise WorkflowError(f"ChatGPT response {key} does not match handoff manifest")
    policy = read_policy(root)
    contract = (policy.get("stage_contracts") or {}).get(state["current_stage"]) or {}
    current = build_context_manifest(root, contract.get("context_paths") or [])
    if current["context_sha256"] != manifest["context_sha256"]:
        raise WorkflowError("context_sha256 changed after prompt preparation; create a new handoff")
    target.write_text(text, encoding="utf-8")
    manifest["response_sha256"] = file_sha256(target)
    manifest["imported_at"] = now_iso()
    manifest["status"] = "response_imported"
    write_manifest(root, handoff_id, manifest)
    state["status"] = "pending_codex"
    add_history(state, "chatgpt_response_imported", stage=state["current_stage"], handoff_id=handoff_id)
    write_state(root, state)
    return manifest


def _validate_report(report: Mapping[str, Any]) -> None:
    required = {"verdict", "checks", "artifacts", "contract_rows", "conflicts", "next_action"}
    missing = sorted(required - set(report))
    if missing:
        raise WorkflowError(f"Codex report missing fields: {', '.join(missing)}")
    if report.get("verdict") not in {"pass", "needs_revision", "blocked"}:
        raise WorkflowError("Codex verdict must be pass, needs_revision, or blocked")
    for key in ["checks", "artifacts", "contract_rows", "conflicts"]:
        if not isinstance(report.get(key), list):
            raise WorkflowError(f"Codex report {key} must be a list")
    if report.get("verdict") == "pass":
        if report.get("conflicts"):
            raise WorkflowError("pass verdict cannot contain unresolved conflicts")
        failed = [
            str(check.get("id") or "unnamed") if isinstance(check, Mapping) else "malformed"
            for check in report.get("checks") or []
            if not isinstance(check, Mapping) or str(check.get("status") or "").lower() != "pass"
        ]
        if failed:
            raise WorkflowError(f"pass verdict cannot contain non-pass checks: {', '.join(failed)}")


def record_codex_verification(root: Path, handoff_id: str, report: Mapping[str, Any]) -> Dict[str, Any]:
    handoff_id = _validate_handoff_id(handoff_id)
    _validate_report(report)
    policy = read_policy(root)
    state = read_state(root)
    if state["status"] != "pending_codex" or state.get("active_handoff_id") != handoff_id:
        raise WorkflowError("verification does not belong to the active Codex handoff")
    directory = handoff_root(root) / handoff_id
    receipt_path = directory / "codex_receipt.json"
    if receipt_path.exists():
        raise WorkflowError("Codex receipt already exists; receipts are immutable")
    stage = state["current_stage"]
    stage_checks = validate_stage(root, stage) if report["verdict"] == "pass" else []
    receipt = {
        "schema_version": "v1",
        "project_id": state["project_id"],
        "stage": stage,
        "handoff_id": handoff_id,
        "created_at": now_iso(),
        **dict(report),
        "checks": list(report["checks"]) + stage_checks,
    }
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest = read_manifest(root, handoff_id)
    manifest["receipt_sha256"] = file_sha256(receipt_path)
    manifest["status"] = f"codex_{report['verdict']}"
    write_manifest(root, handoff_id, manifest)

    verdict = report["verdict"]
    if verdict == "needs_revision":
        state["status"] = "pending_chatgpt"
        state["active_handoff_id"] = None
        state["context_sha256"] = None
    elif verdict == "blocked":
        state["status"] = "blocked"
    else:
        gate = (policy.get("gates") or {}).get(stage)
        state["active_handoff_id"] = None
        state["context_sha256"] = None
        if gate:
            state["status"] = "pending_human"
            state["pending_gate"] = gate
        else:
            completed = list(state.get("completed_stages") or [])
            if stage not in completed:
                completed.append(stage)
            state["completed_stages"] = completed
            index = policy["stages"].index(stage)
            if index == len(policy["stages"]) - 1:
                state["status"] = "completed"
            else:
                state["current_stage"] = policy["stages"][index + 1]
                state["status"] = "pending_chatgpt"
    add_history(state, "codex_verification_recorded", stage=stage, handoff_id=handoff_id, verdict=verdict)
    write_state(root, state)
    return receipt
def _build_revision_block(root: Path, stage: str) -> str | None:
    """Read active (non-closed) revision tasks and format them for prompt injection."""
    task_path = root / "14_contracts" / "revision_tasks.csv"
    if not task_path.exists():
        return None
    with task_path.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    closed = {"closed", "resolved", "waived"}
    active = []
    for row in rows:
        st = (row.get("status") or "").strip().lower()
        sev = (row.get("severity") or "").strip().lower()
        if st in closed or (not st and sev in closed):
            continue
        active.append(row)
    if not active:
        return None
    lines = ["## 未关闭的修订任务（必须逐项完成并做出回应）", ""]
    for row in active:
        tid = (row.get("task_id") or "?").strip()
        sev = (row.get("severity") or "?").strip().upper()
        issue = (row.get("issue_summary") or "").strip()
        action = (row.get("required_action") or "").strip()
        check = (row.get("acceptance_check") or "").strip()
        linked = (row.get("linked_contract_ids") or "").strip()
        target = (row.get("target_location") or "").strip()
        lines.append(f"### {tid} [{sev}]")
        if target:
            lines.append(f"- 位置：{target}")
        if issue:
            lines.append(f"- 问题：{issue}")
        if action:
            lines.append(f"- 要求：{action}")
        if check:
            lines.append(f"- 验收：{check}")
        if linked:
            lines.append(f"- 关联合同：{linked}")
        lines.append("")
    lines.append("请在回复正文中逐一写出你对上述每项任务的完成情况，不能只复制原论文。")
    return "\n".join(lines)
