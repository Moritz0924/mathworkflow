from __future__ import annotations

import argparse
import json
import re
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
TRAINING_REQUIRED_AREAS = {"system", "prompt", "gate"}


def add(issues: List[Dict[str, str]], level: str, item: str, detail: str, path: Path | str = "") -> None:
    issues.append({"level": level, "item": item, "detail": detail, "path": str(path)})


def read_text(path: Path, max_chars: int = 500000) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")[:max_chars]


def row_count(path: Path) -> int:
    return len(read_csv_dict(path)) if path.exists() else 0


def split_ids(value: str) -> List[str]:
    return [item.strip() for item in re.split(r"[;,]", str(value or "")) if item.strip()]


def id_set(path: Path, field: str) -> set[str]:
    return {str(row.get(field) or "").strip() for row in read_csv_dict(path) if str(row.get(field) or "").strip()}


def blocking_queue_rows(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    blockers: List[Dict[str, str]] = []
    for row in rows:
        status = str(row.get("status") or "").strip().lower()
        severity = str(row.get("severity") or "").strip().lower()
        if status == "open" and severity in {"fail", "major"}:
            blockers.append(row)
    return blockers


def validate_training_outputs(run_dir: Path, issues: List[Dict[str, str]]) -> None:
    route_csv = run_dir / "reports" / "prompt_route_manifest.csv"
    route_rows = read_csv_dict(route_csv)
    if len(route_rows) < 16:
        add(issues, "fail", "prompt_route_manifest_incomplete", f"expected at least 16 stage prompt rows, got {len(route_rows)}", route_csv)
    missing_prompt_rows = [row for row in route_rows if str(row.get("included_in_training") or "") != "yes"]
    if missing_prompt_rows:
        add(issues, "fail", "prompt_route_manifest_missing_stage_prompt", f"{len(missing_prompt_rows)} stage prompts were not included", route_csv)
    bundle = run_dir / "reports" / "stage_prompt_bundle.md"
    bundle_text = read_text(bundle)
    if not bundle_text.strip():
        add(issues, "fail", "missing_stage_prompt_bundle", "formal stage prompt bundle is missing or empty", bundle)
    elif "prompts/stage_prompt_contract.md" not in bundle_text or "Stage 15: final_export" not in bundle_text:
        add(issues, "fail", "stage_prompt_bundle_incomplete", "bundle must include global contract and final_export stage prompt", bundle)

    enhancement_csv = run_dir / "reports" / "training_enhancement_points.csv"
    enhancement_md = run_dir / "reports" / "training_enhancement_points.md"
    enhancement_rows = read_csv_dict(enhancement_csv)
    if not enhancement_rows:
        add(issues, "fail", "missing_training_enhancement_points", "training must output system/prompt/gate enhancement candidates", enhancement_csv)
    else:
        areas = {str(row.get("target_area") or "").strip().lower() for row in enhancement_rows}
        missing = sorted(TRAINING_REQUIRED_AREAS - areas)
        if missing:
            add(issues, "fail", "training_enhancement_area_missing", "missing target_area: " + ",".join(missing), enhancement_csv)
    if not read_text(enhancement_md).strip():
        add(issues, "fail", "missing_training_enhancement_markdown", "training_enhancement_points.md is missing or empty", enhancement_md)

    workspace = run_dir / "workspace"
    full_draft = workspace / "09_paper" / "full_draft.md"
    final_paper = workspace / "12_submission" / "final_submit_paper.md"
    submit_package = workspace / "12_submission" / "final_submit_package.md"
    for path in (full_draft, final_paper, submit_package):
        if not read_text(path).strip():
            add(issues, "fail", "missing_submit_ready_training_artifact", f"{path.name} is missing or empty", path)

    paper_text = read_text(final_paper)
    if paper_text:
        section_count = len(re.findall(r"(^|\n)##\s+", paper_text))
        if len(paper_text) < 2500 or section_count < 7:
            add(issues, "fail", "training_final_paper_too_thin", f"chars={len(paper_text)}, sections={section_count}", final_paper)
        if re.search(r"TODO|待补|占位|禁止直接提交", paper_text):
            add(issues, "fail", "training_final_paper_placeholder", "submit-ready paper still contains placeholder markers", final_paper)
        for required in ("摘要", "问题分析", "模型", "结果", "结论"):
            if required not in paper_text:
                add(issues, "fail", "training_final_paper_missing_section_signal", required, final_paper)

    required_contracts = {
        "result_contract.csv": run_dir / "workspace" / "14_contracts" / "result_contract.csv",
        "claim_evidence_map.csv": run_dir / "workspace" / "14_contracts" / "claim_evidence_map.csv",
        "figure_contract.csv": run_dir / "workspace" / "14_contracts" / "figure_contract.csv",
    }
    for name, path in required_contracts.items():
        if row_count(path) == 0:
            add(issues, "fail", "training_contract_empty", f"{name} has no rows", path)

    result_path = required_contracts["result_contract.csv"]
    claim_path = required_contracts["claim_evidence_map.csv"]
    figure_path = required_contracts["figure_contract.csv"]
    formula_path = workspace / "14_contracts" / "formula_contract.csv"
    result_ids = id_set(result_path, "result_id")
    figure_ids = id_set(figure_path, "figure_id")
    formula_ids = id_set(formula_path, "formula_id")

    for row in read_csv_dict(figure_path):
        figure_id = str(row.get("figure_id") or "").strip()
        outputs = [str(row.get(field) or "").strip() for field in ("output_svg", "output_png", "output_pdf")]
        outputs = [item for item in outputs if item]
        existing_outputs = [item for item in outputs if (workspace / item).exists()]
        if not outputs:
            add(issues, "fail", "training_figure_contract_missing_output", figure_id or str(row), figure_path)
        elif not existing_outputs:
            add(issues, "fail", "training_figure_contract_file_missing", f"{figure_id}: " + ";".join(outputs), figure_path)

    for row in read_csv_dict(claim_path):
        claim_id = str(row.get("claim_id") or "").strip()
        for result_id in split_ids(str(row.get("result_id") or "")):
            if result_id not in result_ids:
                add(issues, "fail", "training_claim_missing_result_link", f"{claim_id}: {result_id}", claim_path)
        for figure_id in split_ids(str(row.get("figure_id") or "")):
            if figure_id not in figure_ids:
                add(issues, "fail", "training_claim_missing_figure_link", f"{claim_id}: {figure_id}", claim_path)
        for formula_id in split_ids(str(row.get("formula_id") or "")):
            if formula_id and formula_id not in formula_ids:
                add(issues, "fail", "training_claim_missing_formula_link", f"{claim_id}: {formula_id}", claim_path)

    paper_combined = read_text(workspace / "09_paper" / "full_draft.md") + "\n" + read_text(workspace / "12_submission" / "final_submit_paper.md")
    for figure_ref in sorted(set(re.findall(r"\bF\d+\b", paper_combined))):
        if figure_ref not in figure_ids:
            add(issues, "fail", "training_paper_unregistered_figure_reference", figure_ref, figure_path)

    queue_path = run_dir / "reports" / "agent_revision_queue.csv"
    blockers = blocking_queue_rows(read_csv_dict(queue_path))
    for row in blockers:
        add(
            issues,
            "fail",
            "open_blocking_revision_queue",
            f"{row.get('severity')} {row.get('task_id')}: {row.get('proposed_action') or row.get('issue_summary')}",
            queue_path,
        )

    gate_log = run_dir / "workspace" / "11_review" / "simulated_human_gate_log.csv"
    gate_rows = read_csv_dict(gate_log)
    if len(gate_rows) < 4:
        add(issues, "fail", "training_simulated_gate_log_incomplete", f"expected simulated logs for major gates, got {len(gate_rows)}", gate_log)
    for row in gate_rows:
        if str(row.get("formal_effect") or "").strip().lower() not in {"none", "no"}:
            add(issues, "fail", "training_simulated_gate_has_formal_effect", str(row), gate_log)


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
        if not incomplete_status:
            validate_training_outputs(run_dir, issues)

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
