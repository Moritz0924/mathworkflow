from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Dict, List

import yaml

from .errors import WorkflowError


def verify_legacy_prompts(root: Path) -> Dict[str, Any]:
    manifest_path = root / "config" / "legacy_prompt_hashes.yaml"
    if not manifest_path.exists():
        raise WorkflowError("legacy prompt hash manifest is missing")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    files = manifest.get("files") or {}
    missing: List[str] = []
    changed: List[str] = []
    for relative, expected in files.items():
        path = root / relative
        if not path.exists():
            missing.append(relative)
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != str(expected):
            changed.append(relative)
    if missing or changed:
        raise WorkflowError(f"legacy prompt protection failed: missing={missing}; changed={changed}")
    return {"verified_files": len(files), "missing": missing, "changed": changed}
