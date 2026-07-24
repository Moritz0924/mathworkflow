from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml

from .errors import WorkflowError


FORMAL_STAGES = [
    "intake",
    "data_analysis",
    "model_design",
    "implementation",
    "result_freeze",
    "evidence_design",
    "paper_review",
    "finalize",
]

FORMAL_GATES = {
    "model_design": "model_freeze_gate",
    "result_freeze": "result_freeze_gate",
    "evidence_design": "evidence_gate",
    "paper_review": "paper_gate",
    "finalize": "final_submission_gate",
}


def read_policy(root: Path) -> Dict[str, Any]:
    path = root / "config" / "formal_workflow.yaml"
    if not path.exists():
        raise WorkflowError(f"formal workflow policy is missing: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if data.get("version") != "v4":
        raise WorkflowError("formal workflow policy version must be v4")
    stages = data.get("stages") or []
    if stages != FORMAL_STAGES:
        raise WorkflowError("formal workflow policy must use the fixed eight-stage order")
    if (data.get("gates") or {}) != FORMAL_GATES:
        raise WorkflowError("formal workflow policy must define the fixed five human gates")
    return data
