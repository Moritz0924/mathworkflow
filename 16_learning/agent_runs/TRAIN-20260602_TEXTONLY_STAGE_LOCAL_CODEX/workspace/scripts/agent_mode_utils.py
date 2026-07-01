from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import shlex
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from workflow_utils import ROOT, dump_yaml, load_yaml, read_csv_dict, rel

POLICY_PATH = ROOT / "config" / "agent_mode_policy.yaml"
AGENT_RUNS_ROOT = ROOT / "16_learning" / "agent_runs"
INDEX_PATH = AGENT_RUNS_ROOT / "index.csv"

RUN_INDEX_FIELDS = [
    "run_id",
    "created_at",
    "mode",
    "status",
    "workspace",
    "manifest",
    "report",
    "notes",
]

SNAPSHOT_FIELDS = ["path", "sha256", "size", "mtime_ns"]
PROBLEM_LOCK_FIELDS = ["source_path", "source_sha256", "source_title", "statement_sha256", "statement_title", "status", "detail"]

DEFAULT_PROTECTED_PATHS = [
    "workflow_state.yaml",
    "02_latex_template/",
    "05_model/",
    "06_code/",
    "07_results/",
    "08_figures/",
    "09_paper/",
    "12_submission/",
    "14_contracts/",
]

SKIP_DIR_NAMES = {
    ".git",
    "__pycache__",
    "node_modules",
    "dist",
    ".cache",
    "agent_runs",
}


def now_local() -> str:
    return datetime.now().isoformat(timespec="seconds")


def read_agent_policy() -> Dict[str, Any]:
    policy = load_yaml(POLICY_PATH)
    return policy or {
        "version": "v1-default",
        "enabled": True,
        "default_mode": "training_sandbox",
        "agent_executor": {"command_template": [], "timeout_seconds": 1800, "fallback": "prompt_bundle"},
        "training_sandbox": {"max_iterations": 3, "copy_risk_required": True},
        "benchmark": {"source": "prior_db", "top_k_fulltext": 3},
    }


def ensure_run_root() -> None:
    AGENT_RUNS_ROOT.mkdir(parents=True, exist_ok=True)


def make_run_id(mode: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = "TRAIN" if mode == "training_sandbox" else "FORMAL"
    return f"{prefix}-{stamp}"


def write_csv_rows(path: Path, rows: Sequence[Mapping[str, Any]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(fieldnames))
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def append_csv_row(path: Path, row: Mapping[str, Any], fieldnames: Sequence[str]) -> None:
    rows = read_csv_dict(path) if path.exists() else []
    rows.append({field: row.get(field, "") for field in fieldnames})
    write_csv_rows(path, rows, fieldnames)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def read_text(path: Path, max_chars: int = 200000) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")[:max_chars]


def title_from_text(text: str) -> str:
    for raw in text.splitlines():
        line = raw.strip().strip("#").strip()
        if line and not line.startswith(">"):
            return line[:120]
    return ""


def problem_fingerprint(text: str) -> Dict[str, Any]:
    compact = "".join(ch for ch in text if ch.isalnum() or "\u4e00" <= ch <= "\u9fff")
    markers = []
    for marker in ["R", "G", "B", "浓度", "颜色", "concentration", "sample_id"]:
        if marker.lower() in text.lower():
            markers.append(marker)
    return {
        "title": title_from_text(text),
        "sha256": sha256_text(text),
        "length": len(text),
        "markers": markers,
        "compact_prefix_sha256": sha256_text(compact[:1000]),
    }


def safe_rel(path: Path, root: Path = ROOT) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except Exception:
        return path.as_posix()


def iter_files_for_snapshot(paths: Sequence[str], root: Path = ROOT) -> Iterable[Path]:
    for raw in paths:
        target = (root / raw.rstrip("/\\")).resolve()
        if not target.exists():
            continue
        if target.is_file():
            yield target
            continue
        for path in sorted(target.rglob("*")):
            if not path.is_file():
                continue
            if any(part in SKIP_DIR_NAMES for part in path.parts):
                continue
            yield path


def collect_protected_snapshot(paths: Sequence[str], root: Path = ROOT) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for path in iter_files_for_snapshot(paths, root=root):
        stat = path.stat()
        rows.append(
            {
                "path": safe_rel(path, root),
                "sha256": sha256_file(path),
                "size": stat.st_size,
                "mtime_ns": getattr(stat, "st_mtime_ns", int(stat.st_mtime * 1_000_000_000)),
            }
        )
    rows.sort(key=lambda row: str(row.get("path") or ""))
    return rows


def protected_paths_from_policy(policy: Mapping[str, Any]) -> List[str]:
    sandbox = policy.get("training_sandbox") or {}
    paths = sandbox.get("protected_formal_paths") or DEFAULT_PROTECTED_PATHS
    return [str(item) for item in paths]


def write_protected_snapshot(run_dir: Path, policy: Mapping[str, Any]) -> Path:
    snapshot_path = run_dir / "formal_protected_snapshot.csv"
    rows = collect_protected_snapshot(protected_paths_from_policy(policy))
    write_csv_rows(snapshot_path, rows, SNAPSHOT_FIELDS)
    return snapshot_path


def compare_protected_snapshot(snapshot_path: Path, policy: Mapping[str, Any]) -> List[Dict[str, str]]:
    issues: List[Dict[str, str]] = []
    before = {row.get("path", ""): row for row in read_csv_dict(snapshot_path)}
    current_rows = collect_protected_snapshot(protected_paths_from_policy(policy))
    current = {row.get("path", ""): row for row in current_rows}
    for path, row in before.items():
        if path not in current:
            issues.append({"level": "fail", "item": "protected_file_missing", "detail": path})
            continue
        if str(row.get("sha256")) != str(current[path].get("sha256")):
            issues.append({"level": "fail", "item": "protected_file_changed", "detail": path})
    for path in sorted(set(current) - set(before)):
        issues.append({"level": "fail", "item": "protected_file_created", "detail": path})
    return issues


def copy_file_if_exists(src: Path, dst: Path) -> None:
    if not src.exists() or not src.is_file():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def ignore_copy_names(_: str, names: List[str]) -> set[str]:
    return {name for name in names if name in SKIP_DIR_NAMES}


def copy_tree_if_exists(src: Path, dst: Path) -> None:
    if not src.exists() or not src.is_dir():
        return
    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=ignore_copy_names)


def prepare_sandbox_workspace(run_dir: Path, problem: Optional[Path], policy: Mapping[str, Any]) -> Path:
    workspace = run_dir / "workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    copy_cfg = ((policy.get("training_sandbox") or {}).get("workspace_copy") or {})
    for raw in copy_cfg.get("directories") or []:
        copy_tree_if_exists(ROOT / str(raw), workspace / str(raw))
    for raw in copy_cfg.get("files") or []:
        copy_file_if_exists(ROOT / str(raw), workspace / str(raw))
    for raw in copy_cfg.get("prior_db_partial") or []:
        src = ROOT / str(raw)
        dst = workspace / str(raw)
        if src.is_dir():
            copy_tree_if_exists(src, dst)
        else:
            copy_file_if_exists(src, dst)

    if problem:
        problem = (problem if problem.is_absolute() else ROOT / problem).resolve()
        inbox = workspace / "00_problem" / "inbox"
        inbox.mkdir(parents=True, exist_ok=True)
        if problem.exists() and problem.is_file():
            copy_file_if_exists(problem, inbox / problem.name)
            if problem.suffix.lower() in {".md", ".txt"}:
                text = problem.read_text(encoding="utf-8", errors="ignore")
                (workspace / "00_problem" / "problem_statement.md").write_text(text, encoding="utf-8")
                write_problem_source_lock(run_dir, workspace, problem, text)
        elif problem.exists() and problem.is_dir():
            copy_tree_if_exists(problem, inbox / problem.name)
    return workspace


def write_problem_source_lock(run_dir: Path, workspace: Path, source_path: Path, source_text: str) -> Path:
    statement = workspace / "00_problem" / "problem_statement.md"
    statement_text = read_text(statement)
    lock = {
        "created_at": now_local(),
        "source_path": safe_rel(source_path),
        "workspace_statement": safe_rel(statement, workspace),
        "source": problem_fingerprint(source_text),
        "statement": problem_fingerprint(statement_text),
    }
    path = run_dir / "reports" / "problem_source_lock.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(lock, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def validate_problem_source_lock(run_dir: Path, workspace: Path) -> List[Dict[str, str]]:
    path = run_dir / "reports" / "problem_source_lock.json"
    if not path.exists():
        return []
    try:
        lock = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception as exc:
        return [{"level": "fail", "item": "problem_source_lock_invalid", "detail": str(exc), "path": safe_rel(path)}]
    statement_path = workspace / "00_problem" / "problem_statement.md"
    current = problem_fingerprint(read_text(statement_path))
    expected = lock.get("source") or {}
    issues: List[Dict[str, str]] = []
    if str(current.get("sha256") or "") != str(expected.get("sha256") or ""):
        issues.append(
            {
                "level": "fail",
                "item": "problem_source_drift",
                "detail": f"expected_title={expected.get('title')}; current_title={current.get('title')}",
                "path": safe_rel(statement_path),
            }
        )
    return issues


def write_environment_diagnostics(run_dir: Path) -> Path:
    payload = {
        "generated_at": now_local(),
        "python_executable": sys.executable,
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "preferred_encoding": sys.getdefaultencoding(),
        "filesystem_encoding": sys.getfilesystemencoding(),
        "PYTHONUTF8": os.environ.get("PYTHONUTF8", ""),
        "PYTHONIOENCODING": os.environ.get("PYTHONIOENCODING", ""),
        "note": "Repository-only diagnostics. Local shell profile is not modified.",
    }
    path = run_dir / "reports" / "environment_diagnostics.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def write_manifest(run_dir: Path, payload: Mapping[str, Any]) -> Path:
    path = run_dir / "run_manifest.yaml"
    existing = load_yaml(path) if path.exists() else {}
    merged = dict(existing)
    merged.update(dict(payload))
    dump_yaml(merged, path)
    return path


def append_run_index(run_id: str, mode: str, status: str, workspace: Path, manifest: Path, report: Path, notes: str = "") -> None:
    append_csv_row(
        INDEX_PATH,
        {
            "run_id": run_id,
            "created_at": now_local(),
            "mode": mode,
            "status": status,
            "workspace": safe_rel(workspace),
            "manifest": safe_rel(manifest),
            "report": safe_rel(report) if report else "",
            "notes": notes,
        },
        RUN_INDEX_FIELDS,
    )


def resolve_agent_command(
    policy: Mapping[str, Any],
    prompt_path: Path,
    workspace: Path,
    run_dir: Path,
    mode: str,
    max_iterations: int,
    stage: str = "",
    call_id: str = "",
) -> List[str]:
    raw_env = os.environ.get("MMWF_AGENT_CMD_JSON", "").strip()
    if raw_env:
        value = json.loads(raw_env)
    else:
        executor = policy.get("agent_executor") or {}
        value = executor.get("command_template") or []
    if not value:
        return []
    if isinstance(value, str):
        parts = shlex.split(value)
    else:
        parts = [str(item) for item in value]
    mapping = {
        "prompt_path": str(prompt_path.resolve()),
        "workspace": str(workspace.resolve()),
        "run_dir": str(run_dir.resolve()),
        "mode": mode,
        "max_iterations": str(max_iterations),
        "stage": stage,
        "call_id": call_id,
    }
    return [part.format(**mapping) for part in parts]


def run_agent_command(cmd: Sequence[str], cwd: Path, log_path: Path, timeout_seconds: int) -> Tuple[int, str]:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", encoding="utf-8", errors="replace") as f:
        f.write("$ " + " ".join(cmd) + "\n")
        f.write(f"cwd: {cwd}\n\n")
        f.flush()
        try:
            env = os.environ.copy()
            env.setdefault("PYTHONUTF8", "1")
            env.setdefault("PYTHONIOENCODING", "utf-8")
            proc = subprocess.run(
                list(cmd),
                cwd=str(cwd),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=timeout_seconds,
                env=env,
            )
            output = proc.stdout or ""
            f.write(output)
            return proc.returncode, output[-4000:]
        except subprocess.TimeoutExpired as exc:
            output = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
            f.write(output)
            f.write(f"\n[TIMEOUT] command exceeded {timeout_seconds} seconds\n")
            return 124, output[-4000:]
        except Exception as exc:
            f.write(f"\n[AGENT_COMMAND_ERROR] {exc}\n")
            return 127, str(exc)


def default_timeout(policy: Mapping[str, Any]) -> int:
    executor = policy.get("agent_executor") or {}
    try:
        return int(executor.get("timeout_seconds") or 1800)
    except Exception:
        return 1800


def ngrams(text: str, n: int) -> set[str]:
    compact = "".join(ch.lower() for ch in text if ch.isalnum() or "\u4e00" <= ch <= "\u9fff")
    if len(compact) < n:
        return set()
    return {compact[i : i + n] for i in range(len(compact) - n + 1)}


def write_run_copy_risk(run_dir: Path, target: Path, policy: Mapping[str, Any]) -> Tuple[Path, Path, List[Dict[str, Any]]]:
    benchmark = policy.get("benchmark") or {}
    n = int(benchmark.get("ngram_size") or 8)
    threshold = float(benchmark.get("max_prior_overlap_ratio") or 0.08)
    max_source_chars = int(benchmark.get("max_source_chars_per_doc") or 120000)
    manifest = ROOT / "13_prior_db" / "screening" / "pdf_manifest.csv"
    text_dir = ROOT / "13_prior_db" / "fulltext_index" / "source_texts"
    target_text = target.read_text(encoding="utf-8", errors="ignore") if target.exists() else ""
    target_ngrams = ngrams(target_text, n)
    rows: List[Dict[str, Any]] = []
    best_ratio = 0.0
    best_id = ""
    best_path = ""
    for row in read_csv_dict(manifest):
        source_id = str(row.get("source_id") or "")
        if not source_id:
            continue
        source_path = text_dir / f"{source_id}.txt"
        if not source_path.exists():
            continue
        source_text = source_path.read_text(encoding="utf-8", errors="ignore")[:max_source_chars]
        source_ngrams = ngrams(source_text, n)
        if not source_ngrams or not target_ngrams:
            continue
        ratio = len(target_ngrams & source_ngrams) / max(1, len(target_ngrams))
        if ratio > best_ratio:
            best_ratio = ratio
            best_id = source_id
            best_path = str(row.get("path") or "")
    decision = "fail" if best_ratio > threshold else "pass"
    rows.append(
        {
            "target_path": safe_rel(target),
            "target_type": "agent_training_sandbox_draft",
            "max_overlap_ratio": f"{best_ratio:.6f}",
            "matched_source_id": best_id,
            "matched_source_path": best_path,
            "ngram_size": str(n),
            "threshold": f"{threshold:.6f}",
            "decision": decision if target.exists() else "missing_target",
            "checked_at": now_local(),
        }
    )
    csv_path = run_dir / "reports" / "copy_risk_report.csv"
    md_path = run_dir / "reports" / "copy_risk_report.md"
    write_csv_rows(
        csv_path,
        rows,
        [
            "target_path",
            "target_type",
            "max_overlap_ratio",
            "matched_source_id",
            "matched_source_path",
            "ngram_size",
            "threshold",
            "decision",
            "checked_at",
        ],
    )
    lines = [
        "# Agent Run Copy Risk Report",
        "",
        f"- target: {safe_rel(target)}",
        f"- decision: {rows[0]['decision']}",
        f"- max_overlap_ratio: {rows[0]['max_overlap_ratio']}",
        f"- threshold: {rows[0]['threshold']}",
        f"- matched_source_id: {best_id}",
        "",
        "This report uses n-gram overlap against the local prior DB text cache. It does not copy prior-paper text.",
    ]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return csv_path, md_path, rows
