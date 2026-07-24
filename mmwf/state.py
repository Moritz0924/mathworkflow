from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from .config import read_policy
from .errors import WorkflowError


STAGE_STATUSES = {"pending_chatgpt", "pending_codex", "blocked", "pending_human", "completed"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def default_state(project_id: str) -> Dict[str, Any]:
    project_id = str(project_id or "").strip()
    if not project_id:
        raise WorkflowError("project_id is required")
    return {
        "version": "v4",
        "project_id": project_id,
        "current_stage": "intake",
        "status": "pending_chatgpt",
        "active_handoff_id": None,
        "context_sha256": None,
        "pending_gate": None,
        "completed_stages": [],
        "history": [],
    }


def state_path(root: Path) -> Path:
    return root / "workflow_state.yaml"


def validate_state(state: Dict[str, Any], policy: Optional[Dict[str, Any]] = None) -> None:
    if state.get("version") != "v4":
        raise WorkflowError("workflow state version must be v4")
    if not str(state.get("project_id") or "").strip():
        raise WorkflowError("workflow state project_id is required")
    status = state.get("status")
    if status not in STAGE_STATUSES:
        raise WorkflowError(f"invalid workflow status: {status}")
    if policy and state.get("current_stage") not in policy["stages"]:
        raise WorkflowError(f"unknown current stage: {state.get('current_stage')}")
    if policy:
        stages = policy["stages"]
        current = state.get("current_stage")
        expected_completed = stages if status == "completed" else stages[: stages.index(current)]
        if list(state.get("completed_stages") or []) != expected_completed:
            raise WorkflowError(
                f"completed_stages must be the exact ordered prefix before {current}: {expected_completed}"
            )
        if status == "completed" and current != stages[-1]:
            raise WorkflowError("completed workflow must remain at the finalize stage")
    if status == "pending_human" and not state.get("pending_gate"):
        raise WorkflowError("pending_human state requires pending_gate")
    if status != "pending_human" and state.get("pending_gate"):
        raise WorkflowError("pending_gate is only allowed in pending_human state")


def read_state(root: Path) -> Dict[str, Any]:
    path = state_path(root)
    if not path.exists():
        raise WorkflowError(f"workflow state is missing: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    policy = read_policy(root) if data.get("version") == "v4" else None
    validate_state(data, policy)
    return data


def write_state(root: Path, state: Dict[str, Any]) -> None:
    policy = read_policy(root) if (root / "config" / "formal_workflow.yaml").exists() else None
    validate_state(state, policy)
    path = state_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".yaml.tmp")
    temporary.write_text(yaml.safe_dump(state, allow_unicode=True, sort_keys=False), encoding="utf-8")
    temporary.replace(path)


def add_history(state: Dict[str, Any], event: str, **details: Any) -> None:
    history = list(state.get("history") or [])
    history.append({"at": now_iso(), "event": event, **details})
    state["history"] = history


def confirm_gate(root: Path, gate: str) -> Dict[str, Any]:
    policy = read_policy(root)
    state = read_state(root)
    pending = state.get("pending_gate")
    if state.get("status") != "pending_human" or not pending:
        raise WorkflowError("no pending human gate")
    if gate != pending:
        raise WorkflowError(f"pending gate is {pending}, not {gate}")
    stage = state["current_stage"]
    expected = (policy.get("gates") or {}).get(stage)
    if expected != gate:
        raise WorkflowError(f"gate {gate} does not belong to current stage {stage}")

    completed = list(state.get("completed_stages") or [])
    if stage not in completed:
        completed.append(stage)
    state["completed_stages"] = completed
    state["pending_gate"] = None
    state["active_handoff_id"] = None
    state["context_sha256"] = None
    stages = policy["stages"]
    index = stages.index(stage)
    if index == len(stages) - 1:
        state["status"] = "completed"
    else:
        state["current_stage"] = stages[index + 1]
        state["status"] = "pending_chatgpt"
    add_history(state, "human_gate_confirmed", stage=stage, gate=gate)
    write_state(root, state)
    return state
