from __future__ import annotations

import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Set

from workflow_utils import ROOT, gate_after_stage, is_stage_at_or_after, ordered_stages, read_config, read_csv_dict, read_policy, read_state, rel, truthy
from validate_contracts import run_validation

OUT_JSON = ROOT / "11_review" / "gate_report.json"
OUT_MD = ROOT / "11_review" / "final_submission_checklist.md"


def add(issues: List[Dict[str, str]], level: str, item: str, detail: str, path: str = "") -> None:
    issues.append({"level": level, "item": item, "detail": detail, "path": path})


def clean(value: Any) -> str:
    return str(value or "").strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def current_stage_context() -> tuple[str, str]:
    state = read_state()
    return clean(state.get("current_stage")), clean(state.get("pending_gate"))


def should_check_latex_placeholders(stage: str, pending_gate: str) -> bool:
    return pending_gate == "final_submission_gate" or is_stage_at_or_after(stage, "paper_full")


def should_check_result_summary(stage: str, pending_gate: str) -> bool:
    return pending_gate == "final_submission_gate" or is_stage_at_or_after(stage, "paper_draft")


def validate_execution_policy(issues: List[Dict[str, str]]) -> None:
    state = read_state()
    policy = read_policy()
    if state.get("execution_mode") != "deep_sequential":
        add(issues, "fail", "execution_mode", f"workflow_state execution_mode={state.get('execution_mode')}", "workflow_state.yaml")
    if truthy(state.get("allow_parallel")):
        add(issues, "fail", "allow_parallel", "workflow_state allow_parallel is true", "workflow_state.yaml")
    parallel = policy.get("parallel_execution") or {}
    for key in ("enabled", "allow_multi_stage", "allow_multi_question_codegen", "allow_full_paper_one_shot"):
        if truthy(parallel.get(key)):
            add(issues, "fail", "policy.parallel_execution", f"{key}=true", "config/execution_policy.yaml")
    if (policy.get("mode") or "deep_sequential") != "deep_sequential":
        add(issues, "fail", "policy.mode", f"mode={policy.get('mode')}", "config/execution_policy.yaml")


def validate_latex(issues: List[Dict[str, str]], check_placeholders: bool = True) -> None:
    tex_dir = ROOT / "02_latex_template" / "sections"
    labels: List[str] = []
    refs: List[str] = []
    todos: List[str] = []
    if not tex_dir.exists():
        add(issues, "warn", "latex_sections_missing", "02_latex_template/sections does not exist", "02_latex_template/sections")
        return

    for path in sorted(tex_dir.glob("*.tex")):
        text = read_text(path)
        labels += re.findall(r"\\label\{([^}]+)\}", text)
        refs += re.findall(r"\\(?:ref|eqref|figref|tabref|eqnref)\{([^}]+)\}", text)
        if check_placeholders and re.search(r"TODO|待补|占位|禁止直接提交", text):
            todos.append(rel(path))

    label_set = set(labels)
    for label in sorted({x for x in labels if labels.count(x) > 1}):
        add(issues, "fail", "duplicate_label", label, "02_latex_template/sections")
    for ref in refs:
        if ref not in label_set:
            add(issues, "warn", "missing_ref_target", ref, "02_latex_template/sections")
    for path in todos:
        add(issues, "warn", "todo_exists", "TODO/placeholder text remains", path)

    registered_fig_labels = figure_labels_from_contracts()
    for ref in refs:
        if ref.startswith("fig:") and registered_fig_labels and ref not in registered_fig_labels:
            add(issues, "fail", "latex_ref_to_unregistered_figure", ref, "02_latex_template/sections")


def figure_labels_from_contracts() -> Set[str]:
    labels: Set[str] = set()
    for row in read_csv_dict(ROOT / "14_contracts" / "figure_contract.csv"):
        label = clean(row.get("latex_label"))
        if label:
            labels.add(label)
    for row in read_csv_dict(ROOT / "08_figures" / "figure_registry.csv"):
        label = clean(row.get("latex_label") or row.get("label"))
        if label:
            labels.add(label)
    return labels


def validate_legacy_figure_registry(issues: List[Dict[str, str]]) -> None:
    reg = ROOT / "08_figures" / "figure_registry.csv"
    if not reg.exists():
        return
    with reg.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            figure_id = clean(row.get("figure_id")) or "<unknown>"
            path_value = clean(row.get("path"))
            path = ROOT / path_value if path_value else None
            used = clean(row.get("used_in_paper")) in {"是", "yes", "true", "1"}
            if used and (not path or not path.exists()):
                add(issues, "fail", "registered_figure_missing", figure_id, "08_figures/figure_registry.csv")
            try:
                score = float(clean(row.get("quality_score")) or 0)
            except Exception:
                score = 0.0
            if used and score < 4.2:
                add(issues, "fail", "figure_quality_low", f"{figure_id} score={score}", "08_figures/figure_registry.csv")


def validate_stage_summaries(issues: List[Dict[str, str]]) -> None:
    policy = read_policy()
    if not truthy((policy.get("quality_policy") or {}).get("require_stage_summary")):
        return
    completed = read_state().get("completed_stages") or []
    for stage in completed:
        summary = ROOT / "11_review" / f"{stage}_stage_summary.md"
        if not summary.exists():
            add(issues, "warn", "missing_stage_summary", f"missing summary for completed stage {stage}", rel(summary))


def validate_result_summary(issues: List[Dict[str, str]]) -> None:
    if not (ROOT / "07_results" / "result_summary.tex").exists():
        add(issues, "warn", "result_summary", "07_results/result_summary.tex is missing; paper must not contain final result analysis yet", "07_results/result_summary.tex")


def validate_human_gate_state(issues: List[Dict[str, str]]) -> None:
    state = read_state()
    pending = clean(state.get("pending_gate"))
    current = clean(state.get("current_stage"))
    gates = gate_after_stage()
    if pending:
        expected = gates.get(current)
        if expected and expected != pending:
            add(issues, "fail", "pending_gate_mismatch", f"current_stage={current}, pending_gate={pending}, expected={expected}", "workflow_state.yaml")
        else:
            add(issues, "warn", "pending_human_gate", f"pending gate: {pending}", "workflow_state.yaml")


def validate_required_config_files(issues: List[Dict[str, str]]) -> None:
    required = [
        "config/execution_policy.yaml",
        "config/skill_enhancement.yaml",
        "config/contract_policy.yaml",
        "config/iteration_policy.yaml",
        "config/prior_db_policy.yaml",
        "AGENTS.md",
    ]
    for raw in required:
        if not (ROOT / raw).exists():
            add(issues, "fail", "missing_v32_config", raw, raw)


def validate_skill_router_policy_gate(issues: List[Dict[str, str]]) -> None:
    policy_path = ROOT / "config" / "skill_router_policy.yaml"
    usage_log_path = ROOT / "10_ai_logs" / "skill_usage_log.csv"
    templates_path = ROOT / "10_ai_logs" / "skill_outputs" / "templates"
    report_path = ROOT / "11_review" / "skill_router_report.json"

    if not policy_path.exists():
        add(issues, "fail", "skill_router_policy_gate", "config/skill_router_policy.yaml is missing", "config/skill_router_policy.yaml")
        return

    policy = read_config("skill_router_policy")
    expected_header = [str(x) for x in (((policy.get("usage_log") or {}).get("columns")) or [])]
    if not expected_header:
        add(issues, "fail", "skill_router_policy_gate", "usage_log.columns is missing in router policy", "config/skill_router_policy.yaml")

    if not usage_log_path.exists():
        add(issues, "fail", "skill_router_policy_gate", "10_ai_logs/skill_usage_log.csv is missing", "10_ai_logs/skill_usage_log.csv")
    else:
        with usage_log_path.open("r", encoding="utf-8-sig", newline="") as f:
            actual_header = next(csv.reader(f), [])
        if expected_header and actual_header != expected_header:
            add(issues, "fail", "skill_router_policy_gate", "skill usage log header does not match router policy", "10_ai_logs/skill_usage_log.csv")

    if not templates_path.exists():
        add(issues, "fail", "skill_router_policy_gate", "skill output templates directory is missing", "10_ai_logs/skill_outputs/templates")

    if not report_path.exists():
        add(issues, "fail", "skill_router_policy_gate", "run python scripts/check_skill_router.py --validate-policy before final gates", "11_review/skill_router_report.json")
        return

    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except Exception as exc:
        add(issues, "fail", "skill_router_policy_gate", f"skill router report JSON cannot be parsed: {exc}", "11_review/skill_router_report.json")
        return

    status = clean(report.get("status"))
    if status == "fail":
        add(issues, "fail", "skill_router_policy_gate", "skill router report status is fail", "11_review/skill_router_report.json")
    elif status == "warning":
        add(issues, "warn", "skill_router_policy_gate", "skill router report status is warning", "11_review/skill_router_report.json")


def validate_prior_copy_risk_report(issues: List[Dict[str, str]]) -> None:
    path = ROOT / "13_prior_db" / "screening" / "copy_risk_report.csv"
    if not path.exists():
        return
    for idx, row in enumerate(read_csv_dict(path), start=2):
        if clean(row.get("decision")).lower() == "fail":
            add(
                issues,
                "fail",
                "prior_text_overlap_high",
                f"row {idx}: {row.get('target_path')} overlaps {row.get('matched_source_id')} at {row.get('max_overlap_ratio')}",
                "13_prior_db/screening/copy_risk_report.csv",
            )



def merge_contract_issues(issues: List[Dict[str, str]]) -> None:
    state = read_state()
    stage = clean(state.get("current_stage")) or "current"
    pending_gate = clean(state.get("pending_gate"))

    # During early stages, validate only the requirements that are due now.
    # Full requirement validation starts at compile/final export, or at the final submission gate.
    all_requirements = is_stage_at_or_after(stage, "compile") or pending_gate == "final_submission_gate"
    contract_issues = run_validation(stage=stage, all_requirements=all_requirements, write=True)
    for issue in contract_issues:
        merged = dict(issue)
        merged["item"] = f"contract.{merged.get('item')}"
        issues.append(merged)


def write_reports(issues: Sequence[Mapping[str, str]]) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    fail_count = sum(1 for issue in issues if issue.get("level") == "fail")
    warn_count = sum(1 for issue in issues if issue.get("level") == "warn")
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "fail_count": fail_count,
        "warn_count": warn_count,
        "issue_count": len(issues),
        "issues": list(issues),
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Final submission checklist",
        "",
        f"- fail_count: {fail_count}",
        f"- warn_count: {warn_count}",
        f"- issue_count: {len(issues)}",
        "",
    ]
    if not issues:
        lines.append("No structural gate issues found. Manual verification of data, model validity and contest formatting is still required.")
    else:
        for issue in issues:
            loc = f" ({issue.get('path')})" if issue.get("path") else ""
            lines.append(f"- [{issue.get('level')}] {issue.get('item')}{loc}: {issue.get('detail')}")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    issues: List[Dict[str, str]] = []
    stage, pending_gate = current_stage_context()
    validate_required_config_files(issues)
    validate_execution_policy(issues)
    validate_human_gate_state(issues)
    validate_latex(issues, check_placeholders=should_check_latex_placeholders(stage, pending_gate))
    validate_legacy_figure_registry(issues)
    if should_check_result_summary(stage, pending_gate):
        validate_result_summary(issues)
    validate_stage_summaries(issues)
    validate_skill_router_policy_gate(issues)
    validate_prior_copy_risk_report(issues)
    merge_contract_issues(issues)

    write_reports(issues)
    print(f"[OK] wrote {rel(OUT_JSON)} and {rel(OUT_MD)}")
    if any(issue.get("level") == "fail" for issue in issues):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
