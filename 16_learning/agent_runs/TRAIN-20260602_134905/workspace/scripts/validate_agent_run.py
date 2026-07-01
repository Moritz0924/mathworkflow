from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from agent_mode_utils import (
    AGENT_RUNS_ROOT,
    compare_protected_snapshot,
    read_agent_policy,
    safe_rel,
    write_csv_rows,
)
from workflow_utils import load_yaml, read_csv_dict

ISSUE_FIELDS = ["level", "item", "detail", "path"]


def add(issues: List[Dict[str, str]], level: str, item: str, detail: str, path: Path | str = "") -> None:
    issues.append({"level": level, "item": item, "detail": detail, "path": str(path)})


def validate_run(run_id: str) -> Dict[str, Any]:
    policy = read_agent_policy()
    run_dir = AGENT_RUNS_ROOT / run_id
    issues: List[Dict[str, str]] = []
    if not run_dir.exists():
        add(issues, "fail", "missing_run_dir", run_id, run_dir)
        return write_validation(run_dir, run_id, issues)

    manifest_path = run_dir / "run_manifest.yaml"
    manifest = load_yaml(manifest_path)
    if not manifest:
        add(issues, "fail", "missing_manifest", "run_manifest.yaml is missing or empty", manifest_path)

    workspace = run_dir / "workspace"
    if not workspace.exists():
        add(issues, "fail", "missing_workspace", "workspace directory is missing", workspace)

    report_paths = [
        run_dir / "reports" / "full_gap_report.md",
        run_dir / "reports" / "gap_report.csv",
        run_dir / "reports" / "agent_revision_queue.csv",
    ]
    for path in report_paths:
        if not path.exists():
            add(issues, "fail", "missing_agent_report", path.name, path)

    mode = str(manifest.get("mode") or "")
    status = str(manifest.get("status") or "")
    incomplete_status = status in {"dry_run", "needs_agent_executor", "prompt_bundle_ready"}
    copy_required = bool(((policy.get("training_sandbox") or {}).get("copy_risk_required")))
    copy_risk = run_dir / "reports" / "copy_risk_report.csv"
    if mode == "training_sandbox" and copy_required and not incomplete_status:
        if not copy_risk.exists():
            add(issues, "fail", "missing_copy_risk_report", "copy risk report is required for completed training runs", copy_risk)
        else:
            for row in read_csv_dict(copy_risk):
                if str(row.get("decision") or "").lower() == "fail":
                    add(issues, "fail", "copy_risk_failed", str(row), copy_risk)
    elif mode == "training_sandbox" and not copy_risk.exists():
        add(issues, "warn", "copy_risk_not_run", "copy risk skipped because run is incomplete or dry-run", copy_risk)

    if mode == "training_sandbox":
        snapshot = run_dir / "formal_protected_snapshot.csv"
        if not snapshot.exists():
            add(issues, "fail", "missing_protected_snapshot", "formal protected snapshot is missing", snapshot)
        else:
            for issue in compare_protected_snapshot(snapshot, policy):
                add(issues, issue.get("level", "fail"), issue.get("item", "protected_change"), issue.get("detail", ""), "formal project root")

    gap_report = run_dir / "reports" / "gap_report.csv"
    if gap_report.exists() and not read_csv_dict(gap_report):
        add(issues, "warn", "empty_gap_report", "gap_report.csv has no findings", gap_report)

    return write_validation(run_dir, run_id, issues)


def write_validation(run_dir: Path, run_id: str, issues: List[Dict[str, str]]) -> Dict[str, Any]:
    report_dir = run_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    fail_count = sum(1 for issue in issues if issue.get("level") == "fail")
    warn_count = sum(1 for issue in issues if issue.get("level") == "warn")
    payload = {
        "run_id": run_id,
        "status": "fail" if fail_count else "pass",
        "fail_count": fail_count,
        "warn_count": warn_count,
        "issue_count": len(issues),
        "issues": issues,
    }
    json_path = report_dir / "agent_run_validation.json"
    md_path = report_dir / "agent_run_validation.md"
    csv_path = report_dir / "agent_run_validation.csv"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv_rows(csv_path, issues, ISSUE_FIELDS)
    lines = [
        "# Agent Run Validation",
        "",
        f"- run_id: {run_id}",
        f"- status: {payload['status']}",
        f"- fail_count: {fail_count}",
        f"- warn_count: {warn_count}",
        "",
    ]
    if issues:
        for issue in issues:
            lines.append(f"- [{issue.get('level')}] {issue.get('item')}: {issue.get('detail')} ({issue.get('path')})")
    else:
        lines.append("No agent-run validation issues found.")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    payload["report"] = safe_rel(md_path)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an agent-mode run directory.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--warn-only", action="store_true")
    args = parser.parse_args()
    result = validate_run(args.run_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result.get("fail_count") and not args.warn_only:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
