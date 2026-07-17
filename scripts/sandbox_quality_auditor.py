from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

from agent_mode_utils import AGENT_RUNS_ROOT, safe_rel


RUBRIC_VERSION = "sandbox-quality-v1.0"
DIMENSION_MAX = {
    "length_information_density": 10,
    "section_argument_closure": 18,
    "model_derivation_reasonableness": 18,
    "experiment_validation_credibility": 18,
    "figure_traceability_reproducibility": 16,
    "figure_density_narrative_coverage": 10,
    "format_delivery_quality": 10,
}
TIER_THRESHOLDS = {
    "training_draft": {
        "min_score": 75,
        "min_chars": 10000,
        "min_sections": 7,
        "min_figures": 5,
        "min_tables": 3,
        "min_formulas": 2,
        "min_quality_terms": 18,
    },
    "submission_candidate": {
        "min_score": 85,
        "min_chars": 16000,
        "min_sections": 9,
        "min_figures": 8,
        "min_tables": 5,
        "min_formulas": 4,
        "min_quality_terms": 30,
    },
    "excellent_training_sample": {
        "min_score": 90,
        "min_chars": 20000,
        "min_sections": 10,
        "min_figures": 10,
        "min_tables": 6,
        "min_formulas": 6,
        "min_quality_terms": 42,
    },
}
TIER_ORDER = {
    "needs_revision": 0,
    "training_draft": 1,
    "submission_candidate": 2,
    "excellent_training_sample": 3,
}
QUALITY_FINDING_FIELDS = [
    "finding_id",
    "severity",
    "dimension",
    "score_impact",
    "target_artifact",
    "target_location",
    "evidence_refs",
    "finding",
    "required_action",
    "acceptance_check",
    "recheck_mode",
]
QUALITY_SCORECARD_FIELDS = [
    "dimension",
    "score",
    "max_score",
    "machine_score",
    "auditor_score",
    "status",
    "evidence",
]
QUALITY_TASK_FIELDS = [
    "task_id",
    "source",
    "severity",
    "target_artifact",
    "issue",
    "action",
    "acceptance_check",
    "status",
    "owner",
    "finding_id",
    "recheck_mode",
    "notes",
]
PLACEHOLDER_RE = re.compile(r"TODO|TBD|placeholder|sandbox figure|占位|待补|待完善|示例图", re.I)
QUALITY_TERMS_RE = re.compile(
    r"validation|sensitivity|robust|robustness|residual|baseline|cross[- ]?validation|"
    r"误差|残差|灵敏|敏感|检验|验证|稳健|鲁棒|基线|交叉验证|对比|扰动|置信",
    re.I,
)
TABLE_RE = re.compile(r"(^|\n)\s*(表\s*[0-9一二三四五六七八九十]+|table\s*\d+|\\begin\{tabular\}|\|.+\|)", re.I)


def read_text(path: Path, max_chars: int = 1_000_000) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")[:max_chars]


def read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(read_text(path))
    except Exception:
        return {}


def read_csv_dict(path: Path) -> List[Dict[str, str]]:
    if not path.exists() or not path.is_file():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(row) for row in csv.DictReader(f)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(fields), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2), encoding="utf-8")


def sha256_file(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def rel_or_empty(path: Path, root: Path) -> str:
    return safe_rel(path, root) if path.exists() else ""


def copy_if_exists(src: Path, dst: Path) -> str:
    if not src.exists() or not src.is_file():
        return ""
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return sha256_file(src)


def copy_tree_files(src_dir: Path, dst_dir: Path, patterns: Sequence[str]) -> Dict[str, str]:
    hashes: Dict[str, str] = {}
    if not src_dir.exists():
        return hashes
    for pattern in patterns:
        for src in sorted(src_dir.rglob(pattern)):
            if not src.is_file():
                continue
            rel = src.relative_to(src_dir)
            dst = dst_dir / rel
            copy_if_exists(src, dst)
            hashes[rel.as_posix()] = sha256_file(src)
    return hashes


def output_paths_for_figure(row: Mapping[str, str]) -> List[str]:
    values = []
    for field in ("output_svg", "output_png", "output_pdf", "file_path"):
        value = str(row.get(field) or "").strip()
        if value:
            values.append(value)
    return values


def first_existing(workspace: Path, rel_paths: Iterable[str]) -> Path | None:
    for rel_path in rel_paths:
        path = workspace / rel_path
        if path.exists() and path.is_file():
            return path
    return None


def script_path_for_figure(row: Mapping[str, str]) -> str:
    for field in ("script_path", "figure_script", "source_script"):
        value = str(row.get(field) or "").strip()
        if value:
            return value
    return ""


def log_path_for_figure(row: Mapping[str, str]) -> str:
    for field in ("execution_log", "generation_log", "run_log", "execution_manifest"):
        value = str(row.get(field) or "").strip()
        if value:
            return value
    return ""


def count_tables(text: str) -> int:
    markdown_tables = len(re.findall(r"(^|\n)\s*\|[^\n]+\|\s*\n\s*\|[\s:\-|]+\|", text))
    mentions = len(TABLE_RE.findall(text))
    return max(markdown_tables, mentions)


def count_sections(text: str) -> int:
    headings = re.findall(r"(?m)^#{1,3}\s+\S+", text)
    return len(headings)


def bounded_score(observed: float, target: float, max_score: int) -> float:
    if target <= 0:
        return float(max_score)
    return round(min(float(max_score), float(max_score) * max(0.0, observed) / target), 2)


def tier_thresholds_met(
    tier: str,
    *,
    total_score: float,
    char_count: int,
    section_count: int,
    figure_count: int,
    table_count: int,
    formula_count: int,
    quality_term_count: int,
) -> bool:
    thresholds = TIER_THRESHOLDS[tier]
    return (
        total_score >= thresholds["min_score"]
        and char_count >= thresholds["min_chars"]
        and section_count >= thresholds["min_sections"]
        and figure_count >= thresholds["min_figures"]
        and table_count >= thresholds["min_tables"]
        and formula_count >= thresholds["min_formulas"]
        and quality_term_count >= thresholds["min_quality_terms"]
    )


def add_finding(
    findings: List[Dict[str, Any]],
    finding_id: str,
    severity: str,
    dimension: str,
    score_impact: float,
    target_artifact: str,
    target_location: str,
    evidence_refs: str,
    finding: str,
    required_action: str,
    acceptance_check: str,
    recheck_mode: str,
) -> None:
    if any(row.get("finding_id") == finding_id for row in findings):
        return
    findings.append(
        {
            "finding_id": finding_id,
            "severity": severity,
            "dimension": dimension,
            "score_impact": str(score_impact),
            "target_artifact": target_artifact,
            "target_location": target_location,
            "evidence_refs": evidence_refs,
            "finding": finding,
            "required_action": required_action,
            "acceptance_check": acceptance_check,
            "recheck_mode": recheck_mode,
        }
    )


def create_audit_snapshot(run_dir: Path | str) -> Tuple[Path, Dict[str, Any]]:
    run_dir = Path(run_dir)
    workspace = run_dir / "workspace"
    snapshot = run_dir / "audit_snapshot"
    paper_hashes: Dict[str, str] = {}
    contract_hashes: Dict[str, str] = {}
    result_hashes: Dict[str, str] = {}
    figure_hashes: Dict[str, str] = {}
    script_hashes: Dict[str, str] = {}
    report_hashes: Dict[str, str] = {}

    for name in ("final_submit_paper.md", "final_submit_paper.docx", "final_submit_paper.pdf"):
        src = workspace / "12_submission" / name
        digest = copy_if_exists(src, snapshot / "paper" / name)
        if digest:
            paper_hashes[name] = digest

    for name in ("result_contract.csv", "figure_contract.csv", "formula_contract.csv", "claim_evidence_map.csv"):
        src = workspace / "14_contracts" / name
        digest = copy_if_exists(src, snapshot / "contracts" / name)
        if digest:
            contract_hashes[name] = digest

    result_hashes.update(copy_tree_files(workspace / "07_results", snapshot / "evidence" / "result_files", ["*.csv", "*.json", "*.md", "*.txt"]))
    figure_hashes.update(copy_tree_files(workspace / "08_figures", snapshot / "evidence" / "figure_outputs", ["*.svg", "*.png", "*.pdf", "*.jpg", "*.jpeg"]))
    script_hashes.update(copy_tree_files(workspace / "08_figures", snapshot / "evidence" / "figure_scripts", ["*.py", "*.m", "*.r", "*.R", "*.ipynb", "*.mmd", "*.dot"]))

    for src in (
        workspace / "11_review" / "contract_validation_report.json",
        run_dir / "reports" / "copy_risk_report.csv",
        workspace / "12_submission" / "export_manifest.json",
    ):
        digest = copy_if_exists(src, snapshot / "reports" / src.name)
        if digest:
            report_hashes[src.name] = digest

    rendered_dir = workspace / "12_submission" / "rendered_pages"
    copy_tree_files(rendered_dir, snapshot / "rendered_pages", ["*.png", "*.jpg", "*.jpeg"])

    snapshot_id = "AUDIT-" + sha256_text(run_dir.name + json.dumps(paper_hashes, sort_keys=True))[:12].upper()
    manifest = {
        "run_id": run_dir.name,
        "snapshot_id": snapshot_id,
        "rubric_version": RUBRIC_VERSION,
        "paper_sha256": paper_hashes.get("final_submit_paper.md", ""),
        "contract_sha256": sha256_text(json.dumps(contract_hashes, sort_keys=True)),
        "result_file_hashes": result_hashes,
        "figure_file_hashes": figure_hashes,
        "figure_script_hashes": script_hashes,
        "export_manifest_hash": report_hashes.get("export_manifest.json", ""),
        "report_hashes": report_hashes,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(snapshot / "snapshot_manifest.json", manifest)
    return snapshot, manifest


def evaluate_quality(run_dir: Path | str, snapshot_manifest: Mapping[str, Any], target_tier: str = "training_draft") -> Dict[str, Any]:
    run_dir = Path(run_dir)
    workspace = run_dir / "workspace"
    tier = target_tier if target_tier in TIER_THRESHOLDS else "training_draft"
    thresholds = TIER_THRESHOLDS[tier]
    findings: List[Dict[str, Any]] = []

    paper_path = workspace / "12_submission" / "final_submit_paper.md"
    paper_text = read_text(paper_path)
    docx = workspace / "12_submission" / "final_submit_paper.docx"
    pdf = workspace / "12_submission" / "final_submit_paper.pdf"
    export_manifest = read_json(workspace / "12_submission" / "export_manifest.json")
    figure_rows = read_csv_dict(workspace / "14_contracts" / "figure_contract.csv")
    result_rows = read_csv_dict(workspace / "14_contracts" / "result_contract.csv")
    formula_rows = read_csv_dict(workspace / "14_contracts" / "formula_contract.csv")
    claim_rows = read_csv_dict(workspace / "14_contracts" / "claim_evidence_map.csv")

    char_count = len(paper_text)
    section_count = count_sections(paper_text)
    table_count = count_tables(paper_text)
    quality_term_count = len(QUALITY_TERMS_RE.findall(paper_text))
    formula_count = len(formula_rows)

    if not paper_text.strip():
        add_finding(findings, "QF-PAPER-MISSING", "fail", "length_information_density", 10, safe_rel(paper_path, workspace), "file", "", "Final submit paper is missing or empty.", "Create a submit-ready paper from full_draft.md.", "final_submit_paper.md exists and is non-empty.", "static")
    elif PLACEHOLDER_RE.search(paper_text):
        add_finding(findings, "QF-PAPER-PLACEHOLDER", "redline", "length_information_density", 10, safe_rel(paper_path, workspace), "text", "", "Paper contains placeholder or TODO text.", "Replace placeholders with evidence-backed content or remove them.", "No TODO/placeholder markers remain in the final paper.", "static")
    if char_count < thresholds["min_chars"]:
        add_finding(findings, "QF-PAPER-TOO-SHORT", "major", "length_information_density", 10, safe_rel(paper_path, workspace), "whole paper", str(char_count), f"Effective paper length is below {tier} threshold.", "Expand problem analysis, model derivation, result interpretation, validation, and limitations.", f"Paper length is at least {thresholds['min_chars']} characters for {tier}.", "semantic")
    if section_count < thresholds["min_sections"]:
        add_finding(findings, "QF-SECTIONS-TOO-SHALLOW", "major", "section_argument_closure", 8, safe_rel(paper_path, workspace), "headings", str(section_count), "Paper does not cover enough required modeling-paper sections.", "Add equivalent sections for analysis, assumptions, models, results, validation, limitations, and conclusion.", f"At least {thresholds['min_sections']} substantive sections exist.", "semantic")
    if not result_rows:
        add_finding(findings, "QF-RESULT-CONTRACT-MISSING", "fail", "model_derivation_reasonableness", 8, "14_contracts/result_contract.csv", "file", "", "No result contract rows are available for claims.", "Populate result_contract.csv with source-bound numerical results.", "result_contract.csv contains at least one frozen result row.", "static")
    if not claim_rows:
        add_finding(findings, "QF-CLAIM-CONTRACT-MISSING", "fail", "model_derivation_reasonableness", 6, "14_contracts/claim_evidence_map.csv", "file", "", "No claim-evidence rows are available.", "Bind major paper claims to result, figure, formula, or citation evidence.", "claim_evidence_map.csv contains supported claim rows.", "static")
    if formula_count < thresholds["min_formulas"]:
        add_finding(findings, "QF-FORMULA-DENSITY-LOW", "major", "model_derivation_reasonableness", 6, "14_contracts/formula_contract.csv", "rows", str(formula_count), "Formula contract density is below the target tier.", "Register core formulas with symbols and result links.", f"At least {thresholds['min_formulas']} formula rows exist.", "static")
    if quality_term_count < thresholds["min_quality_terms"]:
        add_finding(findings, "QF-VALIDATION-DENSITY-LOW", "major", "experiment_validation_credibility", 8, safe_rel(paper_path, workspace), "validation text", str(quality_term_count), "Validation, sensitivity, baseline, or robustness evidence is too thin.", "Add task-matched validation and interpret the result strength.", f"Validation evidence count reaches {thresholds['min_quality_terms']} signals.", "semantic")

    seen_ids: Dict[str, int] = {}
    existing_output_count = 0
    evidence_count = 0
    script_count = 0
    log_count = 0
    placeholder_count = 0
    unique_figure_ids = set()
    for row in figure_rows:
        figure_id = str(row.get("figure_id") or "").strip()
        if figure_id:
            seen_ids[figure_id] = seen_ids.get(figure_id, 0) + 1
            unique_figure_ids.add(figure_id)
        output = first_existing(workspace, output_paths_for_figure(row))
        if output:
            existing_output_count += 1
            if PLACEHOLDER_RE.search(read_text(output, 20000)):
                placeholder_count += 1
        script_path = script_path_for_figure(row)
        if script_path and (workspace / script_path).exists():
            script_count += 1
        log_path = log_path_for_figure(row)
        if log_path and (workspace / log_path).exists():
            log_count += 1
        if str(row.get("result_id") or row.get("evidence_source") or "").strip():
            evidence_count += 1
    duplicates = [figure_id for figure_id, count in seen_ids.items() if figure_id and count > 1]
    if duplicates:
        add_finding(findings, "QF-FIG-DUPLICATE-ID", "major", "figure_traceability_reproducibility", 6, "14_contracts/figure_contract.csv", ",".join(duplicates), ",".join(duplicates), "A figure_id is registered more than once and can inflate figure counts.", "Deduplicate figure_contract.csv so each independent figure has exactly one id.", "Every active figure_id appears once.", "static")
    if figure_rows and evidence_count < len(figure_rows):
        add_finding(findings, "QF-FIG-MISSING-EVIDENCE", "major", "figure_traceability_reproducibility", 6, "14_contracts/figure_contract.csv", "result_id/evidence_source", f"{evidence_count}/{len(figure_rows)}", "One or more figures lack result_id or evidence_source binding.", "Bind every data figure to a result row or explicit evidence source.", "Every active figure row has result_id or evidence_source.", "static")
    if figure_rows and existing_output_count < len(figure_rows):
        add_finding(findings, "QF-FIG-MISSING-OUTPUT", "fail", "figure_traceability_reproducibility", 8, "14_contracts/figure_contract.csv", "output path", f"{existing_output_count}/{len(figure_rows)}", "One or more figure outputs are missing.", "Create missing figure files or update the contract to existing outputs.", "Every active figure output path exists.", "static")
    if figure_rows and script_count / max(1, len(figure_rows)) < 0.6:
        add_finding(findings, "QF-FIG-SCRIPT-EVIDENCE-LOW", "major", "figure_traceability_reproducibility", 4, "14_contracts/figure_contract.csv", "script_path", f"{script_count}/{len(figure_rows)}", "Too few figures have executable script evidence.", "Register script_path for generated data figures and keep scripts in the workspace.", "At least 60% of training-draft figures have existing script paths.", "execution")
    if figure_rows and log_count / max(1, len(figure_rows)) < 0.4:
        add_finding(findings, "QF-FIG-RUN-EVIDENCE-LOW", "major", "figure_traceability_reproducibility", 4, "14_contracts/figure_contract.csv", "execution_log", f"{log_count}/{len(figure_rows)}", "Too few figures have generation or execution logs.", "Record generation logs or execution manifests for figure scripts.", "At least 40% of training-draft figures have execution evidence.", "execution")
    if placeholder_count:
        add_finding(findings, "QF-FIG-PLACEHOLDER", "redline", "figure_traceability_reproducibility", 10, "08_figures", "figure file text", str(placeholder_count), "Placeholder or sandbox figure text appears in active figure outputs.", "Replace placeholder figures with generated data figures or mark them inactive.", "No active data figure contains placeholder markers.", "visual")
    if len(unique_figure_ids) < thresholds["min_figures"]:
        add_finding(findings, "QF-FIG-DENSITY-LOW", "major", "figure_density_narrative_coverage", 8, "14_contracts/figure_contract.csv", "figure_id", str(len(unique_figure_ids)), "Independent figure count is below the target tier.", "Add result-bound figures covering results and validation.", f"At least {thresholds['min_figures']} unique figures exist.", "static")

    if table_count < thresholds["min_tables"]:
        add_finding(findings, "QF-TABLE-DENSITY-LOW", "major", "figure_density_narrative_coverage", 4, safe_rel(paper_path, workspace), "tables", str(table_count), "Table density is below the target tier.", "Add compact result, parameter, validation, or comparison tables.", f"At least {thresholds['min_tables']} tables are present.", "semantic")

    visual = export_manifest.get("visual_qa") or {}
    if not docx.exists() or not pdf.exists():
        add_finding(findings, "QF-EXPORT-MISSING", "fail", "format_delivery_quality", 10, "12_submission", "docx/pdf", "", "DOCX or PDF export is missing.", "Regenerate final DOCX and PDF exports.", "final_submit_paper.docx and final_submit_paper.pdf exist and are non-empty.", "static")
    elif str(visual.get("status") or "").lower() != "pass":
        add_finding(findings, "QF-VISUAL-QA-NOT-PASS", "major", "format_delivery_quality", 5, "12_submission/export_manifest.json", "visual_qa", json.dumps(visual, ensure_ascii=False), "Export manifest does not show passing visual QA.", "Render and verify DOCX/PDF pages, then update export_manifest.json.", "visual_qa.status is pass and rendered pages exist.", "visual")

    dimension_scores: Dict[str, float] = {
        "length_information_density": bounded_score(char_count, thresholds["min_chars"], 10),
        "section_argument_closure": min(18.0, bounded_score(section_count, thresholds["min_sections"], 10) + (4 if claim_rows else 0) + (4 if result_rows else 0)),
        "model_derivation_reasonableness": min(18.0, bounded_score(formula_count, thresholds["min_formulas"], 8) + (5 if result_rows else 0) + (5 if claim_rows else 0)),
        "experiment_validation_credibility": min(18.0, bounded_score(quality_term_count, thresholds["min_quality_terms"], 12) + (3 if result_rows else 0) + (3 if table_count >= thresholds["min_tables"] else 0)),
        "figure_traceability_reproducibility": 0.0,
        "figure_density_narrative_coverage": min(10.0, bounded_score(len(unique_figure_ids), thresholds["min_figures"], 7) + (3 if table_count >= thresholds["min_tables"] else bounded_score(table_count, thresholds["min_tables"], 3))),
        "format_delivery_quality": 10.0 if docx.exists() and pdf.exists() and str(visual.get("status") or "").lower() == "pass" else (5.0 if docx.exists() or pdf.exists() else 0.0),
    }
    if figure_rows:
        output_ratio = existing_output_count / max(1, len(figure_rows))
        evidence_ratio = evidence_count / max(1, len(figure_rows))
        script_ratio = script_count / max(1, len(figure_rows))
        log_ratio = log_count / max(1, len(figure_rows))
        duplicate_penalty = 0.0 if duplicates else 1.0
        placeholder_penalty = 0.0 if placeholder_count else 1.0
        figure_score = 16.0 * (0.30 * output_ratio + 0.25 * evidence_ratio + 0.20 * script_ratio + 0.15 * log_ratio + 0.05 * duplicate_penalty + 0.05 * placeholder_penalty)
        dimension_scores["figure_traceability_reproducibility"] = round(min(16.0, figure_score), 2)

    for finding in findings:
        dimension = str(finding.get("dimension") or "")
        impact = float(finding.get("score_impact") or 0)
        if dimension in dimension_scores:
            dimension_scores[dimension] = round(max(0.0, dimension_scores[dimension] - min(impact, dimension_scores[dimension])), 2)

    scorecard = []
    for dimension, max_score in DIMENSION_MAX.items():
        score = round(dimension_scores.get(dimension, 0.0), 2)
        status = "pass" if score >= max_score * 0.7 else "fail"
        scorecard.append(
            {
                "dimension": dimension,
                "score": f"{score:.2f}",
                "max_score": str(max_score),
                "machine_score": f"{score:.2f}",
                "auditor_score": "0.00",
                "status": status,
                "evidence": json.dumps(
                    {
                        "chars": char_count,
                        "sections": section_count,
                        "tables": table_count,
                        "quality_terms": quality_term_count,
                        "figures": len(unique_figure_ids),
                    },
                    ensure_ascii=False,
                ),
            }
        )

    total_score = round(sum(dimension_scores.values()), 2)
    redline_count = sum(1 for row in findings if row.get("severity") == "redline")
    open_fail_count = sum(1 for row in findings if row.get("severity") == "fail")
    open_major_count = sum(1 for row in findings if row.get("severity") == "major")
    evidence_complete = bool(result_rows and claim_rows and figure_rows and evidence_count == len(figure_rows) and existing_output_count == len(figure_rows))
    hard_gate_passed = redline_count == 0 and open_fail_count == 0 and not duplicates and evidence_complete and docx.exists() and pdf.exists()

    tier_context = {
        "total_score": total_score,
        "char_count": char_count,
        "section_count": section_count,
        "figure_count": len(unique_figure_ids),
        "table_count": table_count,
        "formula_count": formula_count,
        "quality_term_count": quality_term_count,
    }

    if redline_count:
        recommended = "rejected"
        decision = "quality_rejected"
        quality_tier = None
    elif not hard_gate_passed or total_score < 75:
        recommended = "needs_revision"
        decision = "quality_needs_revision"
        quality_tier = None
    elif open_major_count == 0 and evidence_complete and tier_thresholds_met("excellent_training_sample", **tier_context):
        recommended = "excellent_training_sample"
        decision = "quality_excellent_training_asset"
        quality_tier = "excellent_training_sample"
    elif open_major_count == 0 and evidence_complete and tier_thresholds_met("submission_candidate", **tier_context):
        recommended = "submission_candidate"
        decision = "quality_submission_candidate"
        quality_tier = "submission_candidate"
    elif tier_thresholds_met("training_draft", **tier_context):
        recommended = "training_draft"
        decision = "quality_training_draft"
        quality_tier = "training_draft"
    else:
        recommended = "needs_revision"
        decision = "quality_needs_revision"
        quality_tier = None

    tasks = []
    for index, finding in enumerate(findings, start=1):
        if str(finding.get("severity")) not in {"redline", "fail", "major"}:
            continue
        tasks.append(
            {
                "task_id": f"QREV-{index:03d}",
                "source": "sandbox_quality_auditor",
                "severity": finding.get("severity"),
                "target_artifact": finding.get("target_artifact"),
                "issue": finding.get("finding"),
                "action": finding.get("required_action"),
                "acceptance_check": finding.get("acceptance_check"),
                "status": "open",
                "owner": "revision_agent",
                "finding_id": finding.get("finding_id"),
                "recheck_mode": finding.get("recheck_mode"),
                "notes": f"snapshot_id={snapshot_manifest.get('snapshot_id')}",
            }
        )

    payload = {
        "run_id": run_dir.name,
        "snapshot_id": snapshot_manifest.get("snapshot_id", ""),
        "rubric_version": RUBRIC_VERSION,
        "target_tier": tier,
        "status": "pass" if TIER_ORDER.get(recommended, 0) >= TIER_ORDER.get(tier, 1) else "fail",
        "decision": decision,
        "recommended_decision": recommended,
        "quality_tier": quality_tier,
        "total_score": total_score,
        "machine_score": round(total_score * 0.44, 2),
        "auditor_score": round(total_score * 0.56, 2),
        "hard_gate_passed": hard_gate_passed,
        "redline_count": redline_count,
        "open_fail_count": open_fail_count,
        "open_major_count": open_major_count,
        "major_count": open_major_count,
        "recheck_required": recommended in {"needs_revision", "rejected"},
        "evidence_complete": evidence_complete,
        "quality_stalled": False,
        "thresholds": thresholds,
        "observed": {
            "chars": char_count,
            "sections": section_count,
            "tables": table_count,
            "formulas": formula_count,
            "quality_terms": quality_term_count,
            "unique_figures": len(unique_figure_ids),
            "figure_rows": len(figure_rows),
            "figure_outputs": existing_output_count,
            "figure_evidence_rows": evidence_count,
            "figure_script_rows": script_count,
            "figure_log_rows": log_count,
        },
        "dimension_scores": dimension_scores,
        "scorecard": scorecard,
        "findings": findings,
        "revision_tasks": tasks,
    }
    return payload


def write_quality_outputs(run_dir: Path | str, payload: Mapping[str, Any]) -> None:
    run_dir = Path(run_dir)
    workspace = run_dir / "workspace"
    review_dir = workspace / "11_review"
    contracts_dir = workspace / "14_contracts"
    verdict = {key: value for key, value in payload.items() if key not in {"scorecard", "findings", "revision_tasks"}}
    write_json(review_dir / "quality_verdict.json", verdict)
    write_json(review_dir / "quality_audit_report.json", payload)
    write_csv(review_dir / "quality_scorecard.csv", list(payload.get("scorecard") or []), QUALITY_SCORECARD_FIELDS)
    write_csv(review_dir / "quality_findings.csv", list(payload.get("findings") or []), QUALITY_FINDING_FIELDS)
    write_csv(contracts_dir / "quality_revision_tasks.csv", list(payload.get("revision_tasks") or []), QUALITY_TASK_FIELDS)

    lines = [
        "# Sandbox Quality Audit",
        "",
        f"- run_id: {payload.get('run_id')}",
        f"- snapshot_id: {payload.get('snapshot_id')}",
        f"- target_tier: {payload.get('target_tier')}",
        f"- status: {payload.get('status')}",
        f"- recommended_decision: {payload.get('recommended_decision')}",
        f"- total_score: {payload.get('total_score')}",
        f"- hard_gate_passed: {payload.get('hard_gate_passed')}",
        f"- evidence_complete: {payload.get('evidence_complete')}",
        "",
        "## Dimension Scores",
        "",
    ]
    for row in payload.get("scorecard") or []:
        lines.append(f"- {row.get('dimension')}: {row.get('score')}/{row.get('max_score')} ({row.get('status')})")
    findings = list(payload.get("findings") or [])
    lines.extend(["", "## Findings", ""])
    if findings:
        for finding in findings:
            lines.append(f"- [{finding.get('severity')}] {finding.get('finding_id')}: {finding.get('finding')}")
    else:
        lines.append("No quality audit findings.")
    (review_dir / "quality_audit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_quality_audit(run_dir: Path | str, target_tier: str = "training_draft") -> Dict[str, Any]:
    snapshot_dir, manifest = create_audit_snapshot(run_dir)
    payload = evaluate_quality(run_dir, manifest, target_tier=target_tier)
    payload["audit_snapshot"] = safe_rel(snapshot_dir, Path(run_dir))
    write_quality_outputs(run_dir, payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic Sandbox Quality Auditor for a training sandbox run.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--target-tier", default="training_draft", choices=sorted(TIER_THRESHOLDS))
    args = parser.parse_args()
    run_dir = AGENT_RUNS_ROOT / args.run_id
    payload = run_quality_audit(run_dir, target_tier=args.target_tier)
    print(json.dumps({k: v for k, v in payload.items() if k not in {"scorecard", "findings", "revision_tasks"}}, ensure_ascii=False, indent=2))
    return 0 if payload.get("status") == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
