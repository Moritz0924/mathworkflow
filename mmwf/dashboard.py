from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

import yaml

from .errors import WorkflowError


class DashboardService:
    def __init__(self, workspace: Path, cli_script: Path) -> None:
        self.workspace = workspace.resolve()
        self.cli_script = cli_script.resolve()

    def run_cli(self, args: Sequence[str]) -> Dict[str, Any]:
        env = os.environ.copy()
        env["MMWF_WORKSPACE_ROOT"] = str(self.workspace)
        process = subprocess.run(
            [sys.executable, str(self.cli_script), *list(args)],
            cwd=str(self.cli_script.parents[1]),
            env=env,
            text=True,
            capture_output=True,
            timeout=120,
            check=False,
        )
        try:
            payload = json.loads(process.stdout)
        except json.JSONDecodeError as exc:
            raise WorkflowError(f"workflow CLI returned invalid JSON: {process.stdout[-500:] or process.stderr[-500:]}") from exc
        if process.returncode != 0:
            raise WorkflowError(str(payload.get("error") or process.stderr or "workflow CLI failed"))
        return payload

    def run_check(self, name: str) -> Dict[str, Any]:
        scripts = self.cli_script.parent
        if name == "gates":
            command = [sys.executable, str(scripts / "check_gates.py"), "--root", str(self.workspace), "--json"]
            report_path = self.workspace / "11_review" / "gate_report.json"
        elif name == "contracts":
            command = [sys.executable, str(scripts / "validate_contracts.py"), "--root", str(self.workspace), "--stage", "current"]
            report_path = self.workspace / "11_review" / "contract_validation_report.json"
        else:
            raise WorkflowError(f"unsupported check: {name}")
        process = subprocess.run(command, cwd=str(self.cli_script.parents[1]), text=True, capture_output=True, timeout=120, check=False)
        if name == "gates":
            try:
                return json.loads(process.stdout)
            except json.JSONDecodeError as exc:
                raise WorkflowError(f"gate check returned invalid JSON: {process.stderr[-500:]}") from exc
        if not report_path.exists():
            raise WorkflowError(f"contract check did not produce {report_path}")
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        payload["return_code"] = process.returncode
        return payload

    def state(self) -> Dict[str, Any]:
        return self.run_cli(["status"])

    def prepare(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        target = str(payload.get("target") or "")
        args = ["prepare", "--target", target]
        handoff_id = str(payload.get("handoff_id") or "").strip()
        if handoff_id:
            args.extend(["--handoff-id", handoff_id])
        return self.run_cli(args)

    def import_response(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        handoff_id = str(payload.get("handoff_id") or "").strip()
        response_text = str(payload.get("response_text") or "")
        if not handoff_id or not response_text:
            raise WorkflowError("handoff_id and response_text are required")
        with tempfile.TemporaryDirectory(prefix="mmwf-import-") as raw:
            path = Path(raw) / "chatgpt_response.md"
            path.write_text(response_text, encoding="utf-8")
            return self.run_cli(["import", "--handoff-id", handoff_id, "--response", str(path)])

    def verify(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        handoff_id = str(payload.get("handoff_id") or "").strip()
        report = payload.get("report")
        if not handoff_id or not isinstance(report, Mapping):
            raise WorkflowError("handoff_id and report object are required")
        with tempfile.TemporaryDirectory(prefix="mmwf-verify-") as raw:
            path = Path(raw) / "codex_report.json"
            path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            return self.run_cli(["verify", "--handoff-id", handoff_id, "--report", str(path)])

    def confirm(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        gate = str(payload.get("gate") or "").strip()
        confirmation = str(payload.get("confirmation") or "").strip()
        if not gate or confirmation != gate:
            raise WorkflowError("confirmation must exactly match the pending gate")
        return self.run_cli(["confirm", "--gate", gate])

    def list_handoffs(self) -> List[Dict[str, Any]]:
        base = self.workspace / "10_ai_logs" / "handoffs"
        if not base.exists():
            return []
        rows: List[Dict[str, Any]] = []
        for path in base.glob("*/manifest.yaml"):
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            rows.append(
                {
                    "handoff_id": data.get("handoff_id"),
                    "stage": data.get("stage"),
                    "revision": data.get("revision"),
                    "status": data.get("status"),
                    "created_at": data.get("created_at"),
                }
            )
        return sorted(rows, key=lambda row: str(row.get("created_at") or ""), reverse=True)

    def handoff_detail(self, handoff_id: str) -> Dict[str, Any]:
        directory = (self.workspace / "10_ai_logs" / "handoffs" / handoff_id).resolve()
        try:
            directory.relative_to((self.workspace / "10_ai_logs" / "handoffs").resolve())
        except ValueError as exc:
            raise WorkflowError("handoff path escapes workspace") from exc
        manifest = directory / "manifest.yaml"
        if not manifest.exists():
            raise WorkflowError(f"unknown handoff_id: {handoff_id}")
        payload: Dict[str, Any] = {"manifest": yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}}
        for name in ["chatgpt_prompt.md", "chatgpt_response.md", "codex_task.md", "codex_receipt.json"]:
            path = directory / name
            payload[name] = path.read_text(encoding="utf-8") if path.exists() else ""
        return payload

    def dispatch(self, action: str, payload: Mapping[str, Any]) -> Dict[str, Any]:
        routes = {
            "prepare": self.prepare,
            "import": self.import_response,
            "verify": self.verify,
            "confirm": self.confirm,
            "check_gates": lambda _: self.run_check("gates"),
            "check_contracts": lambda _: self.run_check("contracts"),
        }
        handler = routes.get(action)
        if not handler:
            raise WorkflowError(f"unsupported dashboard action: {action}")
        return handler(payload)
