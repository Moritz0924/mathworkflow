from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence, TextIO

from .errors import WorkflowError
from .handoff import import_chatgpt_response, prepare_handoff, record_codex_verification
from .migration import migrate_v32
from .state import confirm_gate, default_state, read_state, write_state


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ChatGPT + Codex formal mathematical-modeling workflow")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Initialize one competition workspace")
    init.add_argument("--project-id", required=True)

    sub.add_parser("status", help="Show current workflow state")

    prepare = sub.add_parser("prepare", help="Prepare a ChatGPT prompt or Codex verification task")
    prepare.add_argument("--target", required=True, choices=["chatgpt", "codex"])
    prepare.add_argument("--handoff-id", default="")

    importing = sub.add_parser("import", help="Import one immutable ChatGPT response")
    importing.add_argument("--handoff-id", required=True)
    importing.add_argument("--response", required=True)

    verify = sub.add_parser("verify", help="Validate and record one Codex verification report")
    verify.add_argument("--handoff-id", required=True)
    verify.add_argument("--report", required=True)

    confirm = sub.add_parser("confirm", help="Confirm the exact pending human gate")
    confirm.add_argument("--gate", required=True)

    migrate = sub.add_parser("migrate", help="Migrate the active v3.2 workspace without moving formal assets")
    migrate.add_argument("--from", dest="source_version", required=True, choices=["v3.2"])
    migrate.add_argument("--project-id", default="math-workflow-current")
    return parser


def _emit(output: TextIO, payload: Any) -> None:
    output.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def main(argv: Sequence[str] | None = None, *, root: Path | None = None, output: TextIO | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    workspace = (root or Path.cwd()).resolve()
    stream = output or sys.stdout
    try:
        if args.command == "init":
            if (workspace / "workflow_state.yaml").exists():
                raise WorkflowError("workflow_state.yaml already exists; use migrate for a v3.2 workspace")
            state = default_state(args.project_id)
            write_state(workspace, state)
            _emit(stream, state)
        elif args.command == "status":
            _emit(stream, read_state(workspace))
        elif args.command == "prepare":
            _emit(stream, prepare_handoff(workspace, args.target, handoff_id=args.handoff_id or None))
        elif args.command == "import":
            _emit(stream, import_chatgpt_response(workspace, args.handoff_id, Path(args.response).resolve()))
        elif args.command == "verify":
            report_path = Path(args.report).resolve()
            report = json.loads(report_path.read_text(encoding="utf-8"))
            _emit(stream, record_codex_verification(workspace, args.handoff_id, report))
        elif args.command == "confirm":
            _emit(stream, confirm_gate(workspace, args.gate))
        elif args.command == "migrate":
            _emit(stream, migrate_v32(workspace, project_id=args.project_id))
        else:
            raise WorkflowError(f"unknown command: {args.command}")
        return 0
    except (WorkflowError, OSError, ValueError, json.JSONDecodeError) as exc:
        _emit(stream, {"status": "error", "error": str(exc), "command": args.command})
        return 3
