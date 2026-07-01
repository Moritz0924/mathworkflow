from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Mapping

from agent_mode_utils import (
    AGENT_RUNS_ROOT,
    compare_protected_snapshot,
    read_agent_policy,
    safe_rel,
    validate_problem_source_lock,
    write_csv_rows,
)
from workflow_utils import ROOT, load_yaml, read_csv_dict

ISSUE_FIELDS = ["level", "item", "detail", "path"]
TRAINING_REQUIRED_AREAS = {"system", "prompt", "gate"}
NO_FORMAL_EFFECT_VALUES = {"none", "no", "无", "無", "无影响", "無影響", "没有", "沒有", "不影响", "不影響"}


def add(issues: List[Dict[str, str]], level: str, item: str, detail: str, path: Path | str = "") -> None:
    issues.append({"level": level, "item": item, "detail": detail, "path": str(path)})


def read_text(path: Path, max_chars: int = 500000) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")[:max_chars]


def row_count(path: Path) -> int:
    return len(read_csv_dict(path)) if path.exists() else 0


def split_ids(value: str) -> List[str]:
    return [item.strip() for item in re.split(r"[;,\s]+", str(value or "")) if item.strip()]


def normalize_figure_id(value: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    compact = re.sub(r"[\s_\-]+", "", raw)
    match = re.fullmatch(r"(?i)(?:fig(?:ure)?)?f0*(\d+)", compact)
    if match:
        return f"F{int(match.group(1)):03d}"
    return raw


def id_set(path: Path, field: str, normalizer: Any = None) -> set[str]:
    values = set()
    for row in read_csv_dict(path):
        value = str(row.get(field) or "").strip()
        if value:
            values.add(normalizer(value) if normalizer else value)
    return values


def figure_output_paths(row: Mapping[str, Any]) -> List[str]:
    outputs = [str(row.get(field) or "").strip() for field in ("output_svg", "output_png", "output_pdf", "file_path")]
    return [item for item in outputs if item]


def row_ids(row: Mapping[str, Any], *fields: str, normalizer: Any = None) -> List[str]:
    values: List[str] = []
    for field in fields:
        for item in split_ids(str(row.get(field) or "")):
            values.append(normalizer(item) if normalizer else item)
    return values


def claim_result_bindings(claim_rows: List[Dict[str, str]]) -> Dict[str, set[str]]:
    bindings: Dict[str, set[str]] = {}
    for row in claim_rows:
        claim_id = str(row.get("claim_id") or "").strip()
        if not claim_id:
            continue
        result_ids = set(row_ids(row, "result_id"))
        evidence_type = str(row.get("evidence_type") or "").strip().lower()
        if evidence_type == "result":
            result_ids.update(row_ids(row, "evidence_ref", "evidence_id"))
        bindings[claim_id] = result_ids
    return bindings


def figure_result_bindings(claim_rows: List[Dict[str, str]]) -> Dict[str, set[str]]:
    bindings: Dict[str, set[str]] = {}
    for row in claim_rows:
        result_ids = set(row_ids(row, "result_id"))
        evidence_type = str(row.get("evidence_type") or "").strip().lower()
        if evidence_type == "result":
            result_ids.update(row_ids(row, "evidence_ref", "evidence_id"))
        if not result_ids:
            continue
        figure_ids = row_ids(row, "figure_id", "figure_ids", normalizer=normalize_figure_id)
        if evidence_type == "figure":
            figure_ids += row_ids(row, "evidence_ref", "evidence_id", normalizer=normalize_figure_id)
        for figure_id in figure_ids:
            bindings.setdefault(figure_id, set()).update(result_ids)
    return bindings


def figure_has_evidence_binding(
    row: Mapping[str, Any],
    claim_bindings: Mapping[str, set[str]],
    figure_bindings: Mapping[str, set[str]],
) -> bool:
    if str(row.get("result_id") or "").strip() or str(row.get("evidence_source") or "").strip():
        return True
    for claim_id in row_ids(row, "claim_ids", "claim_id"):
        if claim_bindings.get(claim_id):
            return True
    figure_id = normalize_figure_id(str(row.get("figure_id") or ""))
    if figure_id and figure_bindings.get(figure_id):
        return True
    return False


def blocking_queue_rows(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    blockers: List[Dict[str, str]] = []
    for row in rows:
        status = str(row.get("status") or "").strip().lower()
        severity = str(row.get("severity") or "").strip().lower()
        if status == "open" and severity in {"fail", "major"}:
            blockers.append(row)
    return blockers


def problem_source_text(run_dir: Path) -> str:
    lock_path = run_dir / "reports" / "problem_source_lock.json"
    try:
        lock = json.loads(read_text(lock_path))
    except Exception:
        return ""
    source_path = str(lock.get("source_path") or "")
    if source_path:
        text = read_text(ROOT / source_path, 200000)
        if text:
            return text
    source = lock.get("source") or {}
    markers = " ".join(str(item) for item in (source.get("markers") or []))
    return " ".join([str(source.get("title") or ""), markers])


def group_present(text: str, terms: List[str]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def no_formal_effect(value: str) -> bool:
    normalized = str(value or "").strip().lower()
    if normalized.startswith("formal_effect="):
        normalized = normalized.split("=", 1)[1].strip()
    if normalized.startswith("formal_effect:"):
        normalized = normalized.split(":", 1)[1].strip()
    return normalized in NO_FORMAL_EFFECT_VALUES


def topic_alignment_issue(source_text: str, paper_text: str) -> str:
    if not source_text.strip() or not paper_text.strip():
        return ""
    source_lower = source_text.lower()
    color_problem = (
        ("concentration_mg_l" in source_lower or "concentration" in source_lower or "浓度" in source_text)
        and ("sample_id" in source_lower or "t01" in source_lower or "待测" in source_text)
        and ("颜色" in source_text or "rgb" in source_lower or "`r`" in source_lower)
    )
    if not color_problem:
        return ""
    required_groups = [
        ["颜色", "color", "RGB", "`R`", "`G`", "`B`", "颜色通道"],
        ["浓度", "concentration", "mg/L", "mg_L", "物质浓度"],
        ["T01", "T02", "T03", "待测样本"],
    ]
    present_count = sum(1 for terms in required_groups if group_present(paper_text, terms))
    unrelated_terms = ["AQI", "空气质量", "PM2.5", "PM10", "葡萄酒", "wine quality", "wine"]
    unrelated = [term for term in unrelated_terms if term.lower() in paper_text.lower()]
    target_ids = [target for target in ("T01", "T02", "T03") if target.lower() in source_lower]
    missing_targets = [target for target in target_ids if target.lower() not in paper_text.lower()]
    if present_count < 2 or unrelated or missing_targets:
        detail = f"present_marker_groups={present_count}/3"
        if unrelated:
            detail += "; unrelated_terms=" + ",".join(unrelated[:5])
        if missing_targets:
            detail += "; missing_targets=" + ",".join(missing_targets)
        return detail
    return ""


def paper_figure_references(text: str) -> List[str]:
    refs: set[str] = set()
    for match in re.finditer(r"(?:图|figure\s*)\s*(F\d{3,})(?![A-Za-z0-9])", text, flags=re.IGNORECASE):
        refs.add(match.group(1))
    return sorted(refs)


def paper_structure_counts(text: str) -> Dict[str, int]:
    h2_count = len(re.findall(r"(^|\n)##\s+", text))
    heading_count = len(re.findall(r"(^|\n)#{2,4}\s+", text))
    return {"h2": h2_count, "headings": heading_count}


def final_paper_is_structurally_thin(text: str) -> bool:
    counts = paper_structure_counts(text)
    return len(text) < 2500 or (counts["h2"] < 7 and not (counts["h2"] >= 5 and counts["headings"] >= 9))


def validate_training_outputs(run_dir: Path, issues: List[Dict[str, str]]) -> None:
    workspace = run_dir / "workspace"
    for drift in validate_problem_source_lock(run_dir, workspace):
        add(issues, drift.get("level", "fail"), drift.get("item", "problem_source_drift"), drift.get("detail", ""), drift.get("path", ""))

    route_csv = run_dir / "reports" / "prompt_route_manifest.csv"
    route_rows = read_csv_dict(route_csv)
    if len(route_rows) < 16:
        add(issues, "fail", "prompt_route_manifest_incomplete", f"expected at least 16 stage prompt rows, got {len(route_rows)}", route_csv)
    missing_prompt_rows = [row for row in route_rows if str(row.get("included_in_training") or "") != "yes"]
    if missing_prompt_rows:
        add(issues, "fail", "prompt_route_manifest_missing_stage_prompt", f"{len(missing_prompt_rows)} stage prompts were not included", route_csv)
    missing_sandbox_prompts = [
        row
        for row in route_rows
        if not str(row.get("formal_prompt_file") or "").strip()
        or not str(row.get("sandbox_prompt_file") or "").strip()
        or not (run_dir / "workspace" / str(row.get("sandbox_prompt_file") or "")).exists()
    ]
    if missing_sandbox_prompts:
        add(issues, "fail", "training_sandbox_prompt_set_incomplete", f"{len(missing_sandbox_prompts)} stage rows lack formal/sandbox prompt pair", route_csv)
    bundle = run_dir / "reports" / "stage_prompt_bundle.md"
    bundle_text = read_text(bundle)
    if not bundle_text.strip():
        add(issues, "fail", "missing_stage_prompt_bundle", "formal stage prompt bundle is missing or empty", bundle)
    elif "prompts/stage_prompt_contract.md" not in bundle_text or "Stage 15: final_export" not in bundle_text:
        add(issues, "fail", "stage_prompt_bundle_incomplete", "bundle must include global contract and final_export stage prompt", bundle)

    stage_exec = run_dir / "reports" / "stage_execution_manifest.csv"
    stage_exec_rows = read_csv_dict(stage_exec)
    if stage_exec.exists():
        initial_stages = {str(row.get("stage_id") or "") for row in stage_exec_rows if str(row.get("iteration") or "") == "1" and str(row.get("status") or "") == "pass"}
        if len(initial_stages) < 16:
            add(issues, "fail", "stage_execution_incomplete", f"expected 16 initial stage calls, got {len(initial_stages)}", stage_exec)
        if initial_stages == {"intake"}:
            add(issues, "fail", "stage_execution_stuck_at_intake", "only intake was executed", stage_exec)
    else:
        add(issues, "fail", "missing_stage_execution_manifest", "training sandbox must record per-stage agent calls", stage_exec)

    for violation in sorted((run_dir / "deepseek_calls").glob("*/protocol_violation.json")) if (run_dir / "deepseek_calls").exists() else []:
        add(issues, "fail", "deepseek_protocol_violation", read_text(violation, 2000).strip(), violation)

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

    full_draft = workspace / "09_paper" / "full_draft.md"
    final_paper = workspace / "12_submission" / "final_submit_paper.md"
    submit_package = workspace / "12_submission" / "final_submit_package.md"
    for path in (full_draft, final_paper, submit_package):
        if not read_text(path).strip():
            add(issues, "fail", "missing_submit_ready_training_artifact", f"{path.name} is missing or empty", path)

    paper_text = read_text(final_paper)
    if paper_text:
        alignment_detail = topic_alignment_issue(problem_source_text(run_dir), paper_text)
        if alignment_detail:
            add(issues, "fail", "training_topic_alignment_drift", alignment_detail, final_paper)
        section_counts = paper_structure_counts(paper_text)
        if final_paper_is_structurally_thin(paper_text):
            add(
                issues,
                "fail",
                "training_final_paper_too_thin",
                f"chars={len(paper_text)}, h2={section_counts['h2']}, headings={section_counts['headings']}",
                final_paper,
            )
        if re.search(r"TODO|待补|占位|禁止直接提交", paper_text):
            add(issues, "fail", "training_final_paper_placeholder", "submit-ready paper still contains placeholder markers", final_paper)
        required_signals = {
            "摘要": ["摘要"],
            "问题分析": ["问题分析", "问题描述", "问题定义", "题目分析"],
            "模型": ["模型", "方法"],
            "结果": ["结果", "实验"],
            "结论": ["结论"],
        }
        for required, alternatives in required_signals.items():
            if not any(item in paper_text for item in alternatives):
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
    figure_ids = id_set(figure_path, "figure_id", normalize_figure_id)
    formula_ids = id_set(formula_path, "formula_id")
    claim_rows = read_csv_dict(claim_path)
    claim_bindings = claim_result_bindings(claim_rows)
    figure_bindings = figure_result_bindings(claim_rows)

    for row in read_csv_dict(figure_path):
        figure_id = str(row.get("figure_id") or "").strip()
        if not figure_has_evidence_binding(row, claim_bindings, figure_bindings):
            add(issues, "fail", "training_figure_contract_missing_evidence_source", figure_id or str(row), figure_path)
        outputs = figure_output_paths(row)
        existing_outputs = [item for item in outputs if (workspace / item).exists()]
        if not outputs:
            add(issues, "fail", "training_figure_contract_missing_output", figure_id or str(row), figure_path)
        elif not existing_outputs:
            add(issues, "fail", "training_figure_contract_file_missing", f"{figure_id}: " + ";".join(outputs), figure_path)

    for row in claim_rows:
        claim_id = str(row.get("claim_id") or "").strip()
        result_links = row_ids(row, "result_id")
        if str(row.get("evidence_type") or "").strip().lower() == "result":
            result_links += row_ids(row, "evidence_ref", "evidence_id")
        for result_id in result_links:
            if result_id not in result_ids:
                add(issues, "fail", "training_claim_missing_result_link", f"{claim_id}: {result_id}", claim_path)
        figure_links = row_ids(row, "figure_id", "figure_ids", normalizer=normalize_figure_id)
        if str(row.get("evidence_type") or "").strip().lower() == "figure":
            figure_links += row_ids(row, "evidence_ref", "evidence_id", normalizer=normalize_figure_id)
        for figure_id in figure_links:
            if figure_id not in figure_ids:
                add(issues, "fail", "training_claim_missing_figure_link", f"{claim_id}: {figure_id}", claim_path)
        formula_links = row_ids(row, "formula_id", "formula_ids")
        if str(row.get("evidence_type") or "").strip().lower() == "formula":
            formula_links += row_ids(row, "evidence_ref", "evidence_id")
        for formula_id in formula_links:
            if formula_id and formula_id not in formula_ids:
                add(issues, "fail", "training_claim_missing_formula_link", f"{claim_id}: {formula_id}", claim_path)

    paper_combined = read_text(workspace / "09_paper" / "full_draft.md") + "\n" + read_text(workspace / "12_submission" / "final_submit_paper.md")
    for figure_ref in paper_figure_references(paper_combined):
        if normalize_figure_id(figure_ref) not in figure_ids:
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
        if not no_formal_effect(str(row.get("formal_effect") or "")):
            add(issues, "fail", "training_simulated_gate_has_formal_effect", str(row), gate_log)

    revision_tasks = run_dir / "workspace" / "14_contracts" / "revision_tasks.csv"
    for index, row in enumerate(read_csv_dict(revision_tasks), start=2):
        severity = str(row.get("severity") or "").strip().lower()
        status = str(row.get("status") or "").strip().lower()
        task_id = str(row.get("task_id") or f"row {index}")
        if severity in {"fail", "major"} and status not in {"closed", "resolved", "waived"}:
            add(issues, "fail", "training_revision_task_unresolved", f"{task_id} severity={severity}, status={status or '<empty>'}", revision_tasks)

    scorecard = run_dir / "workspace" / "11_review" / "review_scorecard.csv"
    score_rows = read_csv_dict(scorecard)
    if not score_rows:
        add(issues, "fail", "training_review_scorecard_missing", "review_scorecard.csv is missing or empty", scorecard)
    for index, row in enumerate(score_rows, start=2):
        severity = str(row.get("severity") or row.get("fail_level") or "").strip().lower()
        status = str(row.get("status") or "").strip().lower()
        score_raw = str(row.get("score") or "").strip()
        max_raw = str(row.get("max_score") or "100").strip()
        try:
            score = float(score_raw) if score_raw else None
            max_score = float(max_raw) if max_raw else 100.0
        except ValueError:
            score = None
            max_score = 100.0
        if severity == "fail" and status not in {"closed", "resolved", "waived"}:
            add(issues, "fail", "training_review_fail_unclosed", f"row {index}: {row}", scorecard)
        if score is not None and max_score and (score / max_score * 100.0) < 85.0:
            add(issues, "fail", "training_review_score_below_threshold", f"row {index}: {score}/{max_score}", scorecard)


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
