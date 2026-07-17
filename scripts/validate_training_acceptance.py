from __future__ import annotations

import argparse
import csv
import json
import math
import re
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

from agent_mode_utils import AGENT_RUNS_ROOT, safe_rel
from benchmark_agent_run import source_features, select_benchmark_sources, text_features
from workflow_utils import read_csv_dict


ISSUE_FIELDS = ["level", "item", "detail", "path"]
CLOSED_STATUSES = {"closed", "resolved", "waived", "pass", "passed"}
NO_FORMAL_EFFECT_VALUES = {"none", "no", "false", "0", "无", "没有", "不影响"}
QUALITY_TERMS = re.compile(r"validation|sensitivity|robust|robustness|residual|误差|残差|灵敏|敏感|检验|验证|稳健|鲁棒", re.I)
TABLE_RE = re.compile(r"(^|\n)\s*(表\s*[0-9一二三四五六七八九十]+|table\s*\d+|\\begin\{tabular\}|\|.+\|)", re.I)
QUALITY_TIER_ORDER = {
    "needs_revision": 0,
    "rejected": 0,
    "training_draft": 1,
    "submission_candidate": 2,
    "excellent_training_sample": 3,
}


def add(issues: List[Dict[str, str]], level: str, item: str, detail: str, path: Path | str = "") -> None:
    issues.append({"level": level, "item": item, "detail": detail, "path": str(path)})


def read_text(path: Path, max_chars: int = 800000) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")[:max_chars]


def read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(read_text(path))
    except Exception:
        return {}


def file_nonempty(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def no_formal_effect(value: str) -> bool:
    return str(value or "").strip().lower() in NO_FORMAL_EFFECT_VALUES


def count_tables(text: str) -> int:
    markdown_tables = len(re.findall(r"(^|\n)\s*\|[^\n]+\|\s*\n\s*\|[\s:\-|]+\|", text))
    mentions = len(TABLE_RE.findall(text))
    return max(markdown_tables, mentions)


def count_quality_terms(text: str) -> int:
    return len(QUALITY_TERMS.findall(text))


def row_count(path: Path) -> int:
    return len(read_csv_dict(path)) if path.exists() else 0


def derive_thresholds(workspace: Path, profile: str = "excellent") -> Dict[str, int]:
    draft_text = read_text(workspace / "12_submission" / "final_submit_paper.md") or read_text(workspace / "09_paper" / "full_draft.md")
    sources = select_benchmark_sources(draft_text, top_k=3)
    bench = source_features(sources)
    if profile != "excellent":
        return {
            "min_chars": 2500,
            "min_figures": 3,
            "min_tables": 1,
            "min_formulas": 1,
            "min_quality_terms": 8,
        }
    return {
        "min_chars": max(12000, min(18000, math.ceil(float(bench.get("chars") or 0.0) * 0.55))),
        "min_figures": max(6, math.ceil(float(bench.get("figure_mentions") or 0.0) * 0.5)),
        "min_tables": max(4, math.ceil(float(bench.get("table_mentions") or 0.0) * 0.4)),
        "min_formulas": max(3, math.ceil(float(bench.get("formula_mentions") or 0.0) * 0.5)),
        "min_quality_terms": max(30, math.ceil(float(bench.get("validation_mentions") or 0.0) * 0.7)),
    }


def figure_rows_ready(workspace: Path) -> int:
    ready = 0
    for row in read_csv_dict(workspace / "14_contracts" / "figure_contract.csv"):
        score_raw = str(row.get("quality_score") or "0").strip()
        try:
            score = float(score_raw)
        except ValueError:
            score = 0.0
        outputs = [str(row.get(field) or "").strip() for field in ("output_svg", "output_png", "output_pdf", "file_path")]
        existing = [output for output in outputs if output and (workspace / output).exists()]
        if score >= 4.2 and existing and str(row.get("result_id") or row.get("evidence_source") or "").strip():
            text = " ".join(read_text(workspace / output, 10000) for output in existing)
            if not re.search(r"sandbox figure|placeholder", text, flags=re.I):
                ready += 1
    return ready


def formula_rows_ready(workspace: Path) -> int:
    return row_count(workspace / "14_contracts" / "formula_contract.csv")


def validate_report_status(path: Path, issues: List[Dict[str, str]], item: str) -> None:
    payload = read_json(path)
    if not payload:
        add(issues, "fail", f"missing_{item}", f"{path.name} missing or invalid", path)
        return
    if int(payload.get("fail_count") or 0) > 0 or str(payload.get("status") or "").lower() == "fail":
        add(issues, "fail", f"{item}_failed", json.dumps(payload.get("issues") or [], ensure_ascii=False)[:1000], path)


def validate_exports(workspace: Path, issues: List[Dict[str, str]]) -> Dict[str, Any]:
    submission = workspace / "12_submission"
    manifest_path = submission / "export_manifest.json"
    manifest = read_json(manifest_path)
    docx = submission / "final_submit_paper.docx"
    pdf = submission / "final_submit_paper.pdf"
    if not file_nonempty(docx):
        add(issues, "fail", "missing_docx_export", "final_submit_paper.docx missing or empty", docx)
    if not file_nonempty(pdf):
        add(issues, "fail", "missing_pdf_export", "final_submit_paper.pdf missing or empty", pdf)
    if not manifest:
        add(issues, "fail", "missing_export_manifest", "export_manifest.json missing or invalid", manifest_path)
        return {}
    visual = manifest.get("visual_qa") or {}
    rendered = [str(item) for item in (manifest.get("rendered_pages") or [])]
    if str(visual.get("status") or "").lower() != "pass":
        add(issues, "fail", "docx_visual_qa_not_pass", str(visual), manifest_path)
    if not rendered or not all((workspace / item).exists() for item in rendered):
        add(issues, "fail", "missing_rendered_docx_pages", ";".join(rendered), manifest_path)
    if int(visual.get("page_count") or 0) != int(visual.get("pdf_page_count") or 0):
        add(issues, "fail", "pdf_docx_page_count_mismatch", str(visual), manifest_path)
    return manifest


def validate_quality_verdict(run_dir: Path, workspace: Path, issues: List[Dict[str, str]], target_tier: str = "training_draft") -> Dict[str, Any]:
    verdict_path = workspace / "11_review" / "quality_verdict.json"
    verdict = read_json(verdict_path)
    if not verdict:
        add(issues, "fail", "missing_quality_verdict", "quality_verdict.json missing or invalid", verdict_path)
        return {}
    snapshot_id = str(verdict.get("snapshot_id") or "").strip()
    snapshot_manifest = run_dir / "audit_snapshot" / "snapshot_manifest.json"
    if not snapshot_id:
        add(issues, "fail", "quality_verdict_missing_snapshot_id", "quality verdict must bind to a snapshot_id", verdict_path)
    if not snapshot_manifest.exists():
        add(issues, "fail", "missing_quality_audit_snapshot", "audit_snapshot/snapshot_manifest.json missing", snapshot_manifest)
    total_score = float(verdict.get("total_score") or 0.0)
    if total_score < 75.0:
        add(issues, "fail", "quality_score_below_passline", f"total_score={total_score} < 75", verdict_path)
    if not bool(verdict.get("hard_gate_passed")):
        add(issues, "fail", "quality_hard_gate_not_passed", "quality verdict hard_gate_passed is false", verdict_path)
    recommended = str(verdict.get("recommended_decision") or verdict.get("quality_tier") or "needs_revision")
    if QUALITY_TIER_ORDER.get(recommended, 0) < QUALITY_TIER_ORDER.get(target_tier, 1):
        add(issues, "fail", "quality_verdict_below_target_tier", f"{recommended} < {target_tier}", verdict_path)
    if int(verdict.get("redline_count") or 0) > 0 or int(verdict.get("open_fail_count") or 0) > 0:
        add(issues, "fail", "quality_redline_or_fail_open", f"redline={verdict.get('redline_count')} fail={verdict.get('open_fail_count')}", verdict_path)
    return verdict


def evaluate_training_acceptance(run_dir: Path | str, profile: str = "excellent") -> Dict[str, Any]:
    run_dir = Path(run_dir)
    workspace = run_dir / "workspace"
    issues: List[Dict[str, str]] = []

    validate_report_status(run_dir / "reports" / "agent_run_validation.json", issues, "agent_run_validation")
    validate_report_status(workspace / "11_review" / "contract_validation_report.json", issues, "contract_validation")

    checklist = read_csv_dict(run_dir / "reports" / "stage_acceptance_checklist.csv")
    if len(checklist) < 16:
        add(issues, "fail", "stage_acceptance_checklist_incomplete", f"rows={len(checklist)} < 16", run_dir / "reports" / "stage_acceptance_checklist.csv")
    for idx, row in enumerate(checklist, start=2):
        if str(row.get("status") or "").strip().lower() not in {"pass", "passed"}:
            add(issues, "fail", "stage_acceptance_check_failed", f"row {idx}: {row}", run_dir / "reports" / "stage_acceptance_checklist.csv")

    copy_rows = read_csv_dict(run_dir / "reports" / "copy_risk_report.csv")
    if not copy_rows:
        add(issues, "fail", "missing_copy_risk_report", "copy_risk_report.csv missing or empty", run_dir / "reports" / "copy_risk_report.csv")
    elif any(str(row.get("decision") or "").lower() == "fail" for row in copy_rows):
        add(issues, "fail", "copy_risk_failed", str(copy_rows[:3]), run_dir / "reports" / "copy_risk_report.csv")

    gate_rows = read_csv_dict(workspace / "11_review" / "simulated_human_gate_log.csv")
    if len(gate_rows) < 4:
        add(issues, "fail", "simulated_gate_log_incomplete", f"rows={len(gate_rows)}", workspace / "11_review" / "simulated_human_gate_log.csv")
    for idx, row in enumerate(gate_rows, start=2):
        if not no_formal_effect(str(row.get("formal_effect") or "")):
            add(issues, "fail", "simulated_gate_has_formal_effect", f"row {idx}: {row}", workspace / "11_review" / "simulated_human_gate_log.csv")

    score_rows = read_csv_dict(workspace / "11_review" / "review_scorecard.csv")
    if not score_rows:
        add(issues, "fail", "review_scorecard_missing", "review_scorecard.csv missing or empty", workspace / "11_review" / "review_scorecard.csv")
    for idx, row in enumerate(score_rows, start=2):
        status = str(row.get("status") or "").strip().lower()
        severity = str(row.get("severity") or row.get("fail_level") or "").strip().lower()
        if severity == "fail" and status not in CLOSED_STATUSES:
            add(issues, "fail", "review_fail_unclosed", f"row {idx}: {row}", workspace / "11_review" / "review_scorecard.csv")
        score_raw = str(row.get("score") or "").strip()
        if score_raw:
            try:
                score = float(score_raw)
                max_score = float(str(row.get("max_score") or "100"))
            except ValueError:
                score = 0.0
                max_score = 100.0
            if max_score and score / max_score * 100.0 < 85.0:
                add(issues, "fail", "review_score_below_threshold", f"row {idx}: {score}/{max_score}", workspace / "11_review" / "review_scorecard.csv")

    for task_path in (workspace / "14_contracts" / "revision_tasks.csv", workspace / "11_review" / "revision_tasks.csv"):
        for idx, row in enumerate(read_csv_dict(task_path), start=2):
            if str(row.get("status") or "").strip().lower() not in CLOSED_STATUSES:
                add(issues, "fail", "revision_task_unresolved", f"row {idx}: {row}", task_path)

    paper_path = workspace / "12_submission" / "final_submit_paper.md"
    paper_text = read_text(paper_path)
    thresholds = derive_thresholds(workspace, profile=profile)
    if "训练验收条件与通过记录" not in paper_text:
        add(issues, "fail", "missing_acceptance_appendix", "paper must include training acceptance appendix", paper_path)
    if len(paper_text) < thresholds["min_chars"]:
        add(issues, "fail", "excellent_paper_too_short", f"chars={len(paper_text)} < {thresholds['min_chars']}", paper_path)
    table_count = count_tables(paper_text)
    if table_count < thresholds["min_tables"]:
        add(issues, "fail", "excellent_table_density_low", f"tables={table_count} < {thresholds['min_tables']}", paper_path)
    quality_terms = count_quality_terms(paper_text)
    if quality_terms < thresholds["min_quality_terms"]:
        add(issues, "fail", "excellent_validation_density_low", f"quality_terms={quality_terms} < {thresholds['min_quality_terms']}", paper_path)

    ready_figures = figure_rows_ready(workspace)
    if ready_figures < thresholds["min_figures"]:
        add(issues, "fail", "excellent_figure_density_low", f"ready_figures={ready_figures} < {thresholds['min_figures']}", workspace / "14_contracts" / "figure_contract.csv")
    ready_formulas = formula_rows_ready(workspace)
    if ready_formulas < thresholds["min_formulas"]:
        add(issues, "fail", "excellent_formula_density_low", f"formulas={ready_formulas} < {thresholds['min_formulas']}", workspace / "14_contracts" / "formula_contract.csv")

    export_manifest = validate_exports(workspace, issues)
    quality_verdict = validate_quality_verdict(run_dir, workspace, issues, target_tier="training_draft")

    fail_count = sum(1 for issue in issues if issue.get("level") == "fail")
    payload = {
        "run_id": run_dir.name,
        "status": "fail" if fail_count else "pass",
        "profile": profile,
        "fail_count": fail_count,
        "warn_count": sum(1 for issue in issues if issue.get("level") == "warn"),
        "issue_count": len(issues),
        "thresholds": thresholds,
        "observed": {
            "chars": len(paper_text),
            "ready_figures": ready_figures,
            "tables": table_count,
            "formulas": ready_formulas,
            "quality_terms": quality_terms,
            "export_manifest": bool(export_manifest),
            "quality_verdict": bool(quality_verdict),
        },
        "issues": issues,
    }
    return payload


def write_reports(run_dir: Path, payload: Mapping[str, Any]) -> None:
    reports = run_dir / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    json_path = reports / "training_acceptance.json"
    csv_path = reports / "training_acceptance.csv"
    md_path = reports / "training_acceptance.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ISSUE_FIELDS)
        writer.writeheader()
        for issue in payload.get("issues") or []:
            writer.writerow({field: issue.get(field, "") for field in ISSUE_FIELDS})
    lines = [
        "# Training Acceptance",
        "",
        f"- run_id: {payload.get('run_id')}",
        f"- status: {payload.get('status')}",
        f"- profile: {payload.get('profile')}",
        f"- thresholds: `{json.dumps(payload.get('thresholds') or {}, ensure_ascii=False)}`",
        f"- observed: `{json.dumps(payload.get('observed') or {}, ensure_ascii=False)}`",
        "",
    ]
    issues = list(payload.get("issues") or [])
    if issues:
        lines.append("## Issues")
        lines.append("")
        for issue in issues:
            lines.append(f"- [{issue.get('level')}] {issue.get('item')}: {issue.get('detail')} ({issue.get('path')})")
    else:
        lines.append("No training acceptance issues found.")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate training sandbox acceptance against formal gates and excellent-paper quality thresholds.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--profile", default="excellent")
    args = parser.parse_args()
    run_dir = AGENT_RUNS_ROOT / args.run_id
    payload = evaluate_training_acceptance(run_dir, profile=args.profile)
    write_reports(run_dir, payload)
    print(json.dumps({**payload, "report": safe_rel(run_dir / "reports" / "training_acceptance.md")}, ensure_ascii=False, indent=2))
    return 0 if payload.get("status") == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
