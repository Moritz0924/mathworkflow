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
    canonical_line_endings = manifest.get("canonical_line_endings")
    missing: List[str] = []
    changed: List[str] = []
    for relative, expected in files.items():
        path = root / relative
        if not path.exists():
            missing.append(relative)
            continue
        content = path.read_bytes()
        if canonical_line_endings == "crlf":
            content = content.replace(b"\r\n", b"\n").replace(b"\r", b"\n").replace(b"\n", b"\r\n")
        actual = hashlib.sha256(content).hexdigest()
        if actual != str(expected):
            changed.append(relative)
    if missing or changed:
        raise WorkflowError(f"legacy prompt protection failed: missing={missing}; changed={changed}")
    return {"verified_files": len(files), "missing": missing, "changed": changed}
