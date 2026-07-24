from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List

import yaml

from .context import file_sha256
from .errors import WorkflowError
from .state import add_history, default_state, write_state
from .validators import validate_stage


FORMAL_ASSET_DIRS = [
    "00_problem",
    "01_task_analysis",
    "02_latex_template",
    "02_literature",
    "03_data",
    "04_eda",
    "04_eda_code",
    "05_model",
    "06_code",
    "07_results",
    "08_figures",
    "09_paper",
    "11_review",
    "12_submission",
    "14_contracts",
]


def _asset_manifest(root: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for directory in FORMAL_ASSET_DIRS:
        base = root / directory
        if not base.exists():
            continue
        for path in sorted((item for item in base.rglob("*") if item.is_file()), key=lambda item: item.as_posix()):
            rows.append({"path": path.relative_to(root).as_posix(), "size": path.stat().st_size, "sha256": file_sha256(path)})
    return rows


def migrate_v32(root: Path, project_id: str = "math-workflow-current") -> Dict[str, Any]:
    state_path = root / "workflow_state.yaml"
    if not state_path.exists():
        raise WorkflowError("v3.2 workflow_state.yaml is missing")
    old = yaml.safe_load(state_path.read_text(encoding="utf-8")) or {}
    if not str(old.get("version") or "").startswith("v3.2"):
        raise WorkflowError("migrate --from v3.2 requires a v3.2 state file")
    backup = root / "workflow_state.v3.2.yaml"
    if backup.exists():
        raise WorkflowError("workflow_state.v3.2.yaml already exists")
    shutil.copy2(state_path, backup)

    state = default_state(project_id)
    try:
        validate_stage(root, "intake")
        state["completed_stages"].append("intake")
        state["current_stage"] = "data_analysis"
    except WorkflowError:
        pass
    if state["current_stage"] == "data_analysis":
        try:
            validate_stage(root, "data_analysis")
            state["completed_stages"].append("data_analysis")
            state["current_stage"] = "model_design"
        except WorkflowError:
            pass
    add_history(state, "migrated_from_v3.2", old_stage=old.get("current_stage"), validated_stages=list(state["completed_stages"]))
    write_state(root, state)

    log_dir = root / "10_ai_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"source_version": old.get("version"), "source_stage": old.get("current_stage"), "assets": _asset_manifest(root)}
    (log_dir / "migration_v32_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return state
