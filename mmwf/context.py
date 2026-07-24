from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from .errors import WorkflowError


BLOCKED_SUFFIXES = {".key", ".pem", ".secret", ".p12", ".pfx"}
TEXT_SUFFIXES = {".md", ".txt", ".csv", ".tsv", ".json", ".yaml", ".yml", ".tex", ".py", ".bib"}
SECRET_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{16,}|(?i:(?:api[_-]?key|access[_-]?token|secret)\s*[:=]\s*[\"']?[A-Za-z0-9._-]{20,})"
)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise WorkflowError(f"context path escapes workspace: {path}") from exc


def _blocked_reason(relative: str, path: Path, max_file_bytes: int) -> str:
    parts = Path(relative).parts
    if any(part.startswith(".") for part in parts):
        return "hidden_or_environment_file"
    if path.name.lower() == ".env" or path.suffix.lower() in BLOCKED_SUFFIXES:
        return "secret_file_type"
    if path.stat().st_size > max_file_bytes:
        return "file_too_large"
    if path.suffix.lower() in TEXT_SUFFIXES:
        try:
            sample = path.read_text(encoding="utf-8", errors="ignore")[:200000]
        except OSError:
            return "unreadable"
        if SECRET_PATTERN.search(sample):
            return "sensitive_content"
    return ""


def _candidate_files(root: Path, sources: Iterable[str]) -> Tuple[List[Path], List[Dict[str, str]]]:
    files: List[Path] = []
    excluded: List[Dict[str, str]] = []
    for source in sources:
        path = (root / source).resolve()
        relative = _safe_relative(root, path)
        if not path.exists():
            excluded.append({"path": relative, "reason": "missing"})
        elif path.is_file():
            files.append(path)
        else:
            files.extend(item for item in path.rglob("*") if item.is_file())
    return sorted(set(files), key=lambda item: _safe_relative(root, item)), excluded


def build_context_manifest(root: Path, sources: Iterable[str], max_file_bytes: int = 2_000_000) -> Dict[str, Any]:
    included: List[Dict[str, Any]] = []
    files, excluded = _candidate_files(root, sources)
    for path in files:
        relative = _safe_relative(root, path)
        reason = _blocked_reason(relative, path, max_file_bytes)
        if reason:
            excluded.append({"path": relative, "reason": reason})
            continue
        included.append({"path": relative, "size": path.stat().st_size, "sha256": file_sha256(path)})
    canonical = json.dumps(included, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {
        "context_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "files": included,
        "excluded": sorted(excluded, key=lambda item: item["path"]),
    }


def render_context_snapshot(root: Path, manifest: Dict[str, Any], max_chars: int = 60000) -> str:
    chunks: List[str] = []
    used = 0
    for item in manifest.get("files") or []:
        path = root / item["path"]
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        block = f"\n## `{item['path']}`\n\n{text}\n"
        if used + len(block) > max_chars:
            break
        chunks.append(block)
        used += len(block)
    return "".join(chunks)
