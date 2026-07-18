from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import yaml

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from mmwf.config import read_policy  # noqa: E402
from mmwf.errors import WorkflowError  # noqa: E402
from mmwf.legacy import verify_legacy_prompts  # noqa: E402
from mmwf.state import STAGE_STATUSES, validate_state  # noqa: E402
from mmwf.validators import validate_stage  # noqa: E402


def add(issues: List[Dict[str, str]], level: str, item: str, detail: str, path: str = "") -> None:
    issues.append({"level": level, "item": item, "detail": detail, "path": path})


def load_state_unchecked(root: Path) -> Dict[str, Any]:
    path = root / "workflow_state.yaml"
    if not path.exists():
        raise WorkflowError("workflow_state.yaml is missing")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def validate_state_invariants(root: Path, policy: Dict[str, Any], state: Dict[str, Any], issues: List[Dict[str, str]]) -> None:
    try:
        validate_state(state, policy)
    except WorkflowError as exc:
        add(issues, "fail", "invalid_workflow_state", str(exc), "workflow_state.yaml")

    stages = policy["stages"]
    completed = list(state.get("completed_stages") or [])
    if len(completed) != len(set(completed)):
        add(issues, "fail", "duplicate_completed_stage", str(completed), "workflow_state.yaml")
    unknown = [stage for stage in completed if stage not in stages]
    if unknown:
        add(issues, "fail", "unknown_completed_stage", str(unknown), "workflow_state.yaml")
    ordered = [stage for stage in stages if stage in completed]
    if completed != ordered:
        add(issues, "fail", "completed_stage_order", f"expected {ordered}, got {completed}", "workflow_state.yaml")

    current = str(state.get("current_stage") or "")
    pending = str(state.get("pending_gate") or "")
    expected_gate = str((policy.get("gates") or {}).get(current) or "")
    if state.get("status") == "pending_human" and pending != expected_gate:
        add(issues, "fail", "pending_gate_mismatch", f"expected {expected_gate or 'none'}, got {pending or 'none'}", "workflow_state.yaml")
    if state.get("status") != "pending_human" and pending:
        add(issues, "fail", "unexpected_pending_gate", pending, "workflow_state.yaml")

    active = str(state.get("active_handoff_id") or "")
    if state.get("status") == "pending_codex":
        if not active:
            add(issues, "fail", "missing_active_handoff", "pending_codex requires active_handoff_id", "workflow_state.yaml")
        elif not (root / "10_ai_logs" / "handoffs" / active / "chatgpt_response.md").exists():
            add(issues, "fail", "missing_imported_response", active, f"10_ai_logs/handoffs/{active}")
    if state.get("status") in {"pending_human", "completed"} and active:
        add(issues, "fail", "stale_active_handoff", active, "workflow_state.yaml")
    if state.get("status") not in STAGE_STATUSES:
        add(issues, "fail", "invalid_status", str(state.get("status")), "workflow_state.yaml")


def validate_completed_artifacts(root: Path, state: Dict[str, Any], issues: List[Dict[str, str]]) -> None:
    due = list(state.get("completed_stages") or [])
    if state.get("status") == "pending_human":
        due.append(str(state.get("current_stage") or ""))
    for stage in due:
        try:
            validate_stage(root, stage)
        except WorkflowError as exc:
            add(issues, "fail", "stage_acceptance_failed", f"{stage}: {exc}", "config/formal_workflow.yaml")


def validate_revision_closure(root: Path, state: Dict[str, Any], issues: List[Dict[str, str]]) -> None:
    stages = ["paper_review", "finalize"]
    if state.get("current_stage") not in stages and not any(stage in (state.get("completed_stages") or []) for stage in stages):
        return
    path = root / "14_contracts" / "revision_tasks.csv"
    if not path.exists():
        add(issues, "fail", "missing_revision_tasks", "revision task contract is missing", "14_contracts/revision_tasks.csv")
        return
    closed = {"closed", "resolved", "waived"}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row_number, row in enumerate(csv.DictReader(handle), start=2):
            severity = str(row.get("severity") or "").strip().lower()
            status = str(row.get("status") or "").strip().lower()
            if severity in {"fail", "major"} and status not in closed:
                add(issues, "fail", "revision_task_unresolved", f"row {row_number}: severity={severity}, status={status}", "14_contracts/revision_tasks.csv")


def write_reports(root: Path, payload: Dict[str, Any]) -> None:
    review = root / "11_review"
    review.mkdir(parents=True, exist_ok=True)
    (review / "gate_report.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Gate report v4",
        "",
        f"- fail_count: {payload['fail_count']}",
        f"- warn_count: {payload['warn_count']}",
        "",
    ]
    for issue in payload["issues"]:
        lines.append(f"- [{issue['level']}] {issue['item']}: {issue['detail']} ({issue['path']})")
    if not payload["issues"]:
        lines.append("No gate invariant issues found. Human confirmation is still required at pending gates.")
    (review / "gate_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(root: Path, write: bool = True) -> Dict[str, Any]:
    issues: List[Dict[str, str]] = []
    try:
        policy = read_policy(root)
        state = load_state_unchecked(root)
        validate_state_invariants(root, policy, state, issues)
        validate_completed_artifacts(root, state, issues)
        validate_revision_closure(root, state, issues)
        if (root / "config" / "legacy_prompt_hashes.yaml").exists():
            try:
                verify_legacy_prompts(root)
            except WorkflowError as exc:
                add(issues, "fail", "legacy_prompt_changed", str(exc), "config/legacy_prompt_hashes.yaml")
    except (WorkflowError, OSError, yaml.YAMLError) as exc:
        add(issues, "fail", "gate_check_error", str(exc))
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fail_count": sum(1 for issue in issues if issue["level"] == "fail"),
        "warn_count": sum(1 for issue in issues if issue["level"] == "warn"),
        "issues": issues,
    }
    if write:
        write_reports(root, payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Check v4 workflow state, artifacts, contracts and human-gate invariants")
    parser.add_argument("--root", default=str(SCRIPT_ROOT))
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    payload = run(Path(args.root).resolve(), write=not args.no_write)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(f"[{'PASS' if payload['fail_count'] == 0 else 'FAIL'}] fail={payload['fail_count']} warn={payload['warn_count']}")
    raise SystemExit(1 if payload["fail_count"] else 0)


if __name__ == "__main__":
    main()
