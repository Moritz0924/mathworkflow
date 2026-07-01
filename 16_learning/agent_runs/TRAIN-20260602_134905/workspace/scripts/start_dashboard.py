from __future__ import annotations

import argparse
import csv
import json
import mimetypes
import os
import subprocess
import sys
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple
from urllib.parse import parse_qs, unquote, urlparse

from workflow_utils import ROOT, load_yaml, ordered_stages, read_csv_dict, read_state

from agent_mode_utils import AGENT_RUNS_ROOT, INDEX_PATH

DASHBOARD_ROOT = ROOT / "11_dashboard"
WEB_ROOT = DASHBOARD_ROOT / "web" / "dist"
RUN_LOG_DIR = DASHBOARD_ROOT / "run_logs"
ACTION_LOG = ROOT / "10_ai_logs" / "dashboard_action_log.csv"

ALLOWED_FILE_SUFFIXES = {".md", ".csv", ".json", ".yaml", ".yml", ".txt", ".tex", ".log", ".mmd"}
ALLOWED_FILE_ROOTS = [
    "00_problem",
    "01_task_analysis",
    "02_latex_template",
    "02_literature",
    "03_data",
    "04_eda",
    "05_model",
    "07_results",
    "08_figures",
    "09_paper",
    "10_ai_logs",
    "11_dashboard",
    "11_review",
    "12_submission",
    "13_prior_db",
    "14_contracts",
    "15_iteration_memory",
    "16_learning",
    "config",
    "prompts",
]

CHECK_ACTIONS: Dict[str, List[str]] = {
    "check-gates": ["scripts/check_gates.py"],
    "validate-contracts": ["scripts/validate_contracts.py", "--stage", "current", "--warn-only"],
    "check-skill-router": ["scripts/check_skill_router.py", "--validate-policy"],
    "validate-export": ["scripts/validate_v32_export.py"],
}

ACTION_LOG_FIELDS = [
    "action_id",
    "timestamp",
    "action",
    "command",
    "job_id",
    "status",
    "exit_code",
    "confirmation",
    "notes",
]


def utc_like_now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except Exception:
        return path.as_posix()


def read_json_file(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"read_error": str(exc)}


def read_text_tail(path: Path, limit: int = 16000) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    return text[-limit:]


# --- Sandbox helpers ---

def load_run_index() -> List[Dict[str, str]]:
    if not INDEX_PATH.exists():
        return []
    runs = read_csv_dict(INDEX_PATH)
    runs.sort(key=lambda r: r.get("created_at", ""), reverse=True)
    return runs


def load_run_manifest(run_id: str) -> Dict[str, Any]:
    manifest_path = AGENT_RUNS_ROOT / run_id / "run_manifest.yaml"
    return load_yaml(manifest_path)


def run_report_summaries(run_dir: Path) -> Dict[str, Any]:
    reports: Dict[str, Any] = {}
    val_path = run_dir / "reports" / "agent_run_validation.json"
    if val_path.exists():
        reports["validation"] = read_json_file(val_path)
    else:
        reports["validation"] = {"exists": False}

    gap_path = run_dir / "reports" / "gap_report.csv"
    if gap_path.exists():
        gaps = read_csv_dict(gap_path)
        reports["gap"] = {
            "exists": True,
            "path": rel(gap_path),
            "count": len(gaps),
            "fail_count": sum(1 for g in gaps if g.get("severity") == "fail"),
            "warn_count": sum(1 for g in gaps if g.get("severity") in ("major", "minor")),
        }
    else:
        reports["gap"] = {"exists": False}

    copy_path = run_dir / "reports" / "copy_risk_report.csv"
    if copy_path.exists():
        copy_rows = read_csv_dict(copy_path)
        reports["copy_risk"] = {
            "exists": True,
            "path": rel(copy_path),
            "decision": copy_rows[0].get("decision") if copy_rows else None,
        }
    else:
        reports["copy_risk"] = {"exists": False}

    full_gap = run_dir / "reports" / "full_gap_report.md"
    reports["full_gap"] = {
        "exists": full_gap.exists(),
        "path": rel(full_gap) if full_gap.exists() else None,
    }

    queue_path = run_dir / "reports" / "agent_revision_queue.csv"
    if queue_path.exists():
        queue = read_csv_dict(queue_path)
        reports["revision_queue"] = {
            "exists": True,
            "path": rel(queue_path),
            "count": len(queue),
        }
    else:
        reports["revision_queue"] = {"exists": False}

    return reports


def append_action_log(row: Mapping[str, Any]) -> None:
    ACTION_LOG.parent.mkdir(parents=True, exist_ok=True)
    exists = ACTION_LOG.exists()
    with ACTION_LOG.open("a", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ACTION_LOG_FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow({field: row.get(field, "") for field in ACTION_LOG_FIELDS})


def latest_action_rows(limit: int = 20) -> List[Dict[str, str]]:
    if not ACTION_LOG.exists():
        return []
    with ACTION_LOG.open("r", encoding="utf-8-sig", newline="") as f:
        rows = [dict(row) for row in csv.DictReader(f)]
    return rows[-limit:]


def report_summary(path: Path) -> Dict[str, Any]:
    payload = read_json_file(path)
    if not payload:
        return {"exists": False, "path": rel(path)}
    return {
        "exists": True,
        "path": rel(path),
        "fail_count": payload.get("fail_count") or payload.get("summary", {}).get("errors"),
        "warn_count": payload.get("warn_count") or payload.get("summary", {}).get("warnings"),
        "status": payload.get("status"),
        "generated_at": payload.get("generated_at") or payload.get("timestamp"),
        "issue_count": payload.get("issue_count"),
    }


def file_info(path: Path, group: str, label: Optional[str] = None) -> Optional[Dict[str, Any]]:
    if not path.exists() or not path.is_file():
        return None
    try:
        stat = path.stat()
    except OSError:
        return None
    return {
        "group": group,
        "label": label or path.name,
        "path": rel(path),
        "size": stat.st_size,
        "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
        "suffix": path.suffix.lower(),
    }


def artifact_patterns() -> List[Tuple[str, str, str]]:
    return [
        ("Contracts", "14_contracts/*", ""),
        ("Review", "11_review/*", ""),
        ("Figures", "08_figures/*.csv", ""),
        ("Figures", "08_figures/*.md", ""),
        ("Prior DB", "13_prior_db/*.md", ""),
        ("Prior DB", "13_prior_db/cards/*.jsonl", ""),
        ("Prior DB", "13_prior_db/screening/*.csv", ""),
        ("Learning", "16_learning/reports/*", ""),
        ("Learning", "16_learning/training_data/*.csv", ""),
        ("Logs", "11_dashboard/run_logs/*.log", ""),
        ("Logs", "10_ai_logs/*.csv", ""),
        ("Workflow", "workflow_state.yaml", "workflow_state.yaml"),
        ("Workflow", "prompts/stages/*.md", ""),
    ]


def list_artifacts() -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for group, pattern, label in artifact_patterns():
        for path in sorted(ROOT.glob(pattern)):
            if path.suffix.lower() not in ALLOWED_FILE_SUFFIXES:
                continue
            info = file_info(path, group, label or None)
            if info:
                grouped.setdefault(group, []).append(info)
    return grouped


def safe_preview_path(raw_path: str) -> Path:
    if not raw_path:
        raise ValueError("missing path")
    raw_path = unquote(raw_path).replace("\\", "/")
    path = Path(raw_path)
    resolved = (path if path.is_absolute() else ROOT / path).resolve()
    try:
        relative = resolved.relative_to(ROOT.resolve()).as_posix()
    except Exception as exc:
        raise ValueError("path escapes project root") from exc
    if resolved.suffix.lower() not in ALLOWED_FILE_SUFFIXES:
        raise ValueError("file suffix is not previewable")
    if not any(relative == root or relative.startswith(root + "/") for root in ALLOWED_FILE_ROOTS):
        raise ValueError("path is outside preview whitelist")
    if not resolved.exists() or not resolved.is_file():
        raise ValueError("file does not exist")
    return resolved


class JobRunner:
    def __init__(self, write_actions_enabled: bool) -> None:
        self.write_actions_enabled = write_actions_enabled
        self.lock = threading.Lock()
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.active_job_id: Optional[str] = None

    def start_job(self, action: str, args: List[str], confirmation: str = "", notes: str = "") -> Tuple[bool, Dict[str, Any]]:
        if not self.write_actions_enabled:
            return False, {"error": "write actions are disabled unless bound to 127.0.0.1"}
        with self.lock:
            if self.active_job_id and self.jobs.get(self.active_job_id, {}).get("status") == "running":
                return False, {"error": "another dashboard job is already running", "active_job_id": self.active_job_id}
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            job_id = f"JOB-{stamp}-{len(self.jobs) + 1:03d}"
            command = [sys.executable, *args]
            log_path = RUN_LOG_DIR / f"{job_id}_{action}.log"
            job = {
                "job_id": job_id,
                "action": action,
                "status": "running",
                "command": command,
                "command_display": " ".join(command),
                "log_path": rel(log_path),
                "started_at": utc_like_now(),
                "finished_at": "",
                "exit_code": None,
                "confirmation": confirmation,
                "notes": notes,
            }
            self.jobs[job_id] = job
            self.active_job_id = job_id
            append_action_log(
                {
                    "action_id": f"ACT-{stamp}-{len(self.jobs):03d}",
                    "timestamp": job["started_at"],
                    "action": action,
                    "command": job["command_display"],
                    "job_id": job_id,
                    "status": "started",
                    "exit_code": "",
                    "confirmation": confirmation,
                    "notes": notes,
                }
            )
            thread = threading.Thread(target=self._run, args=(job_id, log_path), daemon=True)
            thread.start()
            return True, job

    def _run(self, job_id: str, log_path: Path) -> None:
        RUN_LOG_DIR.mkdir(parents=True, exist_ok=True)
        job = self.jobs[job_id]
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        started = time.time()
        with log_path.open("w", encoding="utf-8", errors="replace") as f:
            f.write(f"$ {job['command_display']}\n")
            f.flush()
            try:
                proc = subprocess.Popen(
                    job["command"],
                    cwd=str(ROOT),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    env=env,
                )
                assert proc.stdout is not None
                for line in proc.stdout:
                    f.write(line)
                    f.flush()
                exit_code = proc.wait()
            except Exception as exc:
                f.write(f"\n[DASHBOARD_ERROR] {exc}\n")
                exit_code = 127
        with self.lock:
            job["status"] = "passed" if exit_code == 0 else "failed"
            job["exit_code"] = exit_code
            job["finished_at"] = utc_like_now()
            job["duration_seconds"] = round(time.time() - started, 2)
            if self.active_job_id == job_id:
                self.active_job_id = None
            append_action_log(
                {
                    "action_id": f"ACT-END-{job_id}",
                    "timestamp": job["finished_at"],
                    "action": job["action"],
                    "command": job["command_display"],
                    "job_id": job_id,
                    "status": job["status"],
                    "exit_code": exit_code,
                    "confirmation": job.get("confirmation", ""),
                    "notes": job.get("notes", ""),
                }
            )

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            job = dict(self.jobs.get(job_id) or {})
        if not job:
            return None
        log_path = ROOT / str(job.get("log_path") or "")
        job["log_tail"] = read_text_tail(log_path)
        return job

    def recent_jobs(self, limit: int = 8) -> List[Dict[str, Any]]:
        with self.lock:
            rows = list(self.jobs.values())[-limit:]
        return [dict(row, log_tail=read_text_tail(ROOT / str(row.get("log_path") or ""), 6000)) for row in rows]


def make_state_payload(runner: JobRunner, host: str) -> Dict[str, Any]:
    state = read_state()
    current = str(state.get("current_stage") or "")
    pending = state.get("pending_gate")
    statuses = state.get("stage_status") or {}
    completed = set(state.get("completed_stages") or [])
    locked = set(state.get("locked_stages") or [])
    stages = []
    for index, stage in enumerate(ordered_stages()):
        stages.append(
            {
                "id": stage,
                "index": index,
                "status": statuses.get(stage) or ("completed" if stage in completed else "locked" if stage in locked else "pending"),
                "is_current": stage == current,
                "is_locked": stage in locked,
                "is_completed": stage in completed,
            }
        )
    return {
        "generated_at": utc_like_now(),
        "server": {
            "host": host,
            "write_actions_enabled": runner.write_actions_enabled,
            "python": sys.executable,
        },
        "workflow": {
            "version": state.get("version"),
            "execution_mode": state.get("execution_mode"),
            "allow_parallel": state.get("allow_parallel"),
            "current_stage": current,
            "pending_gate": pending,
            "last_confirmed_gate": state.get("last_confirmed_gate"),
            "stages": stages,
        },
        "reports": {
            "gates": report_summary(ROOT / "11_review" / "gate_report.json"),
            "contracts": report_summary(ROOT / "11_review" / "contract_validation_report.json"),
            "skill_router": report_summary(ROOT / "11_review" / "skill_router_report.json"),
            "copy_risk": file_info(ROOT / "13_prior_db" / "screening" / "copy_risk_report.csv", "Prior DB"),
            "learning": file_info(ROOT / "16_learning" / "reports" / "workflow_optimization_report.md", "Learning"),
        },
        "jobs": {
            "active_job_id": runner.active_job_id,
            "recent": runner.recent_jobs(),
        },
        "actions": latest_action_rows(),
    }


class DashboardHandler(BaseHTTPRequestHandler):
    runner: JobRunner
    server_host: str

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"[dashboard] {self.address_string()} - {fmt % args}")

    def send_json(self, payload: Mapping[str, Any], status: int = 200) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def read_json_body(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        return json.loads(raw) if raw.strip() else {}

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "http://127.0.0.1")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/api/state":
            self.send_json(make_state_payload(self.runner, self.server_host))
            return
        if path == "/api/artifacts":
            self.send_json({"groups": list_artifacts()})
            return
        if path == "/api/file":
            query = parse_qs(parsed.query)
            try:
                target = safe_preview_path(query.get("path", [""])[0])
                stat = target.stat()
                text = target.read_text(encoding="utf-8", errors="replace")
                truncated = False
                if len(text) > 250000:
                    text = text[:250000] + "\n\n[dashboard truncated preview]"
                    truncated = True
                self.send_json({"path": rel(target), "text": text, "size": stat.st_size, "truncated": truncated})
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
            return
        if path.startswith("/api/jobs/"):
            job_id = path.rsplit("/", 1)[-1]
            job = self.runner.get_job(job_id)
            if not job:
                self.send_json({"error": "job not found"}, status=404)
            else:
                self.send_json({"job": job})
            return

        # --- Sandbox endpoints ---
        if path == "/api/sandbox/runs":
            self.send_json({"runs": load_run_index()})
            return
        if path.startswith("/api/sandbox/runs/"):
            run_id = path.rsplit("/", 1)[-1]
            run_dir = AGENT_RUNS_ROOT / run_id
            if not run_dir.exists():
                self.send_json({"error": f"run {run_id} not found"}, status=404)
                return
            manifest = load_run_manifest(run_id)
            reports = run_report_summaries(run_dir)
            log_dir = run_dir / "logs"
            logs = sorted([rel(p) for p in log_dir.glob("*.log")]) if log_dir.exists() else []
            self.send_json({
                "run_id": run_id,
                "manifest": manifest,
                "reports": reports,
                "logs": logs,
            })
            return

        self.serve_static(path)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        try:
            payload = self.read_json_body()
        except Exception as exc:
            self.send_json({"error": f"invalid json body: {exc}"}, status=400)
            return

        if path == "/api/actions/run-current":
            self.handle_run_current(payload)
            return
        if path == "/api/actions/confirm-gate":
            self.handle_confirm_gate(payload)
            return
        if path.startswith("/api/actions/"):
            action = path.rsplit("/", 1)[-1]
            self.handle_check(action)
            return

        # --- Sandbox POST endpoints ---
        if path == "/api/sandbox/start":
            self.handle_sandbox_start(payload)
            return
        if path.startswith("/api/sandbox/benchmark/"):
            run_id = path.rsplit("/", 1)[-1]
            ok, job = self.runner.start_job(
                f"benchmark-{run_id}",
                ["scripts/benchmark_agent_run.py", "--run-id", run_id],
                notes=f"benchmark run_id={run_id}",
            )
            self.send_json({"job": job}, status=202 if ok else 409)
            return
        if path.startswith("/api/sandbox/validate/"):
            run_id = path.rsplit("/", 1)[-1]
            ok, job = self.runner.start_job(
                f"validate-{run_id}",
                ["scripts/validate_agent_run.py", "--run-id", run_id],
                notes=f"validate run_id={run_id}",
            )
            self.send_json({"job": job}, status=202 if ok else 409)
            return

        self.send_json({"error": "unknown action"}, status=404)

    def handle_run_current(self, payload: Mapping[str, Any]) -> None:
        state = read_state()
        stage = str(state.get("current_stage") or "")
        confirmation = str(payload.get("confirmation") or "").strip()
        if confirmation != stage:
            self.send_json({"error": "confirmation must exactly match current_stage", "current_stage": stage}, status=400)
            return
        args = ["scripts/run_current_stage.py"]
        question = str(payload.get("question") or "").strip()
        section = str(payload.get("section") or "").strip()
        if question:
            args += ["--question", question]
        if section:
            args += ["--section", section]
        ok, job = self.runner.start_job("run-current", args, confirmation=confirmation, notes=f"stage={stage}")
        self.send_json({"job": job}, status=202 if ok else 409)

    def handle_confirm_gate(self, payload: Mapping[str, Any]) -> None:
        state = read_state()
        gate = str(state.get("pending_gate") or "").strip()
        confirmation = str(payload.get("confirmation") or "").strip()
        if not gate:
            self.send_json({"error": "no pending gate to confirm"}, status=400)
            return
        if confirmation != gate:
            self.send_json({"error": "confirmation must exactly match pending_gate", "pending_gate": gate}, status=400)
            return
        ok, job = self.runner.start_job("confirm-gate", ["scripts/confirm_gate.py", gate], confirmation=confirmation, notes=f"gate={gate}")
        self.send_json({"job": job}, status=202 if ok else 409)

    def handle_check(self, action: str) -> None:
        command = CHECK_ACTIONS.get(action)
        if not command:
            self.send_json({"error": "unknown check action"}, status=404)
            return
        ok, job = self.runner.start_job(action, command, notes="dashboard check action")
        self.send_json({"job": job}, status=202 if ok else 409)

    def handle_sandbox_start(self, payload: Mapping[str, Any]) -> None:
        mode = str(payload.get("mode") or "training_sandbox")
        if mode not in {"training_sandbox", "formal_assist"}:
            self.send_json({"error": "mode must be training_sandbox or formal_assist"}, status=400)
            return
        max_iterations = max(1, min(10, int(payload.get("max_iterations") or 3)))
        dry_run = bool(payload.get("dry_run", False))
        problem = str(payload.get("problem") or "00_problem/problem_statement.md")
        feedback_run_id = str(payload.get("feedback_run_id") or "").strip()
        no_training_feedback = bool(payload.get("no_training_feedback", False))

        args = [
            "scripts/run_agent_mode.py",
            "--mode", mode,
            "--max-iterations", str(max_iterations),
            "--problem", problem,
        ]
        if mode == "formal_assist" and feedback_run_id:
            args += ["--feedback-run-id", feedback_run_id]
        if mode == "formal_assist" and no_training_feedback:
            args.append("--no-training-feedback")
        if dry_run:
            args.append("--dry-run")

        ok, job = self.runner.start_job(
            f"sandbox-{mode}",
            args,
            confirmation="",
            notes=f"mode={mode}, max_iterations={max_iterations}, dry_run={dry_run}",
        )
        self.send_json({"job": job}, status=202 if ok else 409)

    def serve_static(self, path: str) -> None:
        if not WEB_ROOT.exists():
            self.send_response(503)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Dashboard frontend is not built. Run npm install and npm run build in 11_dashboard/web.")
            return
        if path in {"", "/"}:
            target = WEB_ROOT / "index.html"
        else:
            target = (WEB_ROOT / path.lstrip("/")).resolve()
            try:
                target.relative_to(WEB_ROOT.resolve())
            except Exception:
                self.send_error(404)
                return
            if not target.exists() and "." not in Path(path).name:
                target = WEB_ROOT / "index.html"
        if not target.exists() or not target.is_file():
            self.send_error(404)
            return
        mime = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        data = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Start the local math-workflow dashboard.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    write_enabled = args.host == "127.0.0.1"
    runner = JobRunner(write_actions_enabled=write_enabled)
    DashboardHandler.runner = runner
    DashboardHandler.server_host = args.host

    server = ThreadingHTTPServer((args.host, args.port), DashboardHandler)
    print(f"[OK] dashboard serving at http://{args.host}:{args.port}")
    if not write_enabled:
        print("[WARN] write actions disabled because host is not 127.0.0.1")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[OK] dashboard stopped")


if __name__ == "__main__":
    main()
