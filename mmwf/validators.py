from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Dict, List

from .config import read_policy
from .errors import WorkflowError


def validate_stage(root: Path, stage: str) -> List[Dict[str, str]]:
    policy = read_policy(root)
    contract = (policy.get("stage_contracts") or {}).get(stage) or {}
    checks: List[Dict[str, str]] = []
    failures: List[str] = []
    for relative in contract.get("required_artifacts") or []:
        path = root / relative
        passed = path.exists() and path.is_file() and path.stat().st_size > 0
        checks.append({"id": f"artifact:{relative}", "status": "pass" if passed else "fail", "evidence": relative})
        if not passed:
            failures.append(f"missing or empty required artifact: {relative}")
    for relative, minimum in (contract.get("required_contract_rows") or {}).items():
        path = root / relative
        count = 0
        if path.exists():
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                count = sum(1 for row in csv.DictReader(handle) if any(str(value or "").strip() for value in row.values()))
        passed = count >= int(minimum)
        checks.append({"id": f"contract:{relative}", "status": "pass" if passed else "fail", "evidence": f"{relative} rows={count}"})
        if not passed:
            failures.append(f"contract {relative} requires at least {minimum} data rows, found {count}")
    if failures:
        raise WorkflowError("; ".join(failures))
    return checks
