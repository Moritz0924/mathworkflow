from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set

import yaml

ROOT = Path(__file__).resolve().parents[1]

REPORT_JSON = ROOT / "11_review" / "contract_validation_report.json"
REPORT_MD = ROOT / "11_review" / "contract_validation_report.md"

ALLOWED_STATUSES = {
    "",
    "active",
    "draft",
    "ready",
    "frozen",
    "blocked",
    "open",
    "closed",
    "resolved",
    "waived",
    "pass",
    "validated",
    "verified",
    "unverified",
    "final",
    "synthesized",
}
ACTIVE_STATUSES = {"active", "ready", "frozen", "pass", "validated", "verified"}
CLOSED_STATUSES = {"closed", "resolved", "waived"}
BAD_SUPPORT = {"", "none", "metadata_only", "unsupported"}
FINAL_REQUIRED_NONEMPTY_CONTRACTS = {
    "result_contract.csv": "14_contracts/result_contract.csv",
    "claim_evidence_map.csv": "14_contracts/claim_evidence_map.csv",
    "figure_contract.csv": "14_contracts/figure_contract.csv",
}
TRUE_VALUES = {"1", "true", "yes", "y", "是", "已验证", "verified", "read", "已读"}

STAGE_REQUIREMENT_KEYS: Dict[str, List[str]] = {
    # These are prerequisites for entering a stage. The stage validator checks
    # the outputs produced by that stage before state advancement.
    "model_design": [],
    "implementation": ["before_model_design"],
    "result_freeze": ["before_model_design"],
    "evidence_design": ["before_result_freeze"],
    "paper_review": ["before_evidence_design"],
    "finalize": ["before_paper_review"],
}

REQUIRED_NONEMPTY_BY_KEY: Dict[str, Set[str]] = {
    "before_model_design": {"14_contracts/formula_contract.csv"},
    "before_result_freeze": {"14_contracts/result_contract.csv", "14_contracts/artifact_freeze_registry.csv"},
    "before_evidence_design": {"14_contracts/result_contract.csv", "14_contracts/figure_contract.csv", "14_contracts/claim_evidence_map.csv"},
    "before_paper_review": {"14_contracts/claim_evidence_map.csv", "14_contracts/result_contract.csv"},
    "before_finalize": {"14_contracts/artifact_freeze_registry.csv", "14_contracts/polish_diff_check.csv"},
}


def add(issues: List[Dict[str, str]], level: str, item: str, detail: str, path: str = "") -> None:
    issues.append({"level": level, "item": item, "detail": detail, "path": path})


def configure_root(root: Path) -> None:
    global ROOT, REPORT_JSON, REPORT_MD
    ROOT = root.resolve()
    REPORT_JSON = ROOT / "11_review" / "contract_validation_report.json"
    REPORT_MD = ROOT / "11_review" / "contract_validation_report.md"


def read_config(filename: str) -> Dict[str, Any]:
    path = ROOT / "config" / filename
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def read_csv_dict(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_csv_header(path: Path) -> List[str]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle), [])


def truthy(value: Any) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y", "on", "confirmed"}


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def read_state() -> Dict[str, Any]:
    path = ROOT / "workflow_state.yaml"
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def clean(value: Any) -> str:
    return str(value or "").strip()


def split_ids(value: Any) -> List[str]:
    return [item.strip() for item in re.split(r"[;,\s]+", clean(value)) if item.strip()]


def normalize_figure_id(value: Any) -> str:
    raw = clean(value)
    if not raw:
        return ""
    compact = re.sub(r"[\s_\-]+", "", raw)
    match = re.fullmatch(r"(?i)(?:fig(?:ure)?)?f0*(\d+)", compact)
    if match:
        return f"F{int(match.group(1)):03d}"
    return raw


def status(row: Mapping[str, Any], *keys: str) -> str:
    for key in keys or ("status",):
        value = clean(row.get(key)).lower()
        if value:
            return value
    return ""


def is_active(row: Mapping[str, Any], *keys: str) -> bool:
    return status(row, *keys) in ACTIVE_STATUSES


def has_text(value: Any) -> bool:
    return bool(clean(value))


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(str(value).strip())
    except Exception:
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(str(value).strip()))
    except Exception:
        return default


def boolish(value: Any) -> bool:
    return str(value or "").strip().lower() in TRUE_VALUES or truthy(value)


def load_policy() -> Dict[str, Any]:
    return read_config("contract_policy.yaml") or {}


def required_paths_for_stage(stage: str, all_requirements: bool = False) -> Dict[str, List[str]]:
    policy = load_policy()
    required = policy.get("required_contracts") or {}
    if all_requirements:
        return {str(k): [str(x) for x in (v or [])] for k, v in required.items()}
    keys = STAGE_REQUIREMENT_KEYS.get(stage, [])
    return {key: [str(x) for x in (required.get(key) or [])] for key in keys}


def validate_required_files(stage: str, issues: List[Dict[str, str]], all_requirements: bool = False) -> None:
    reqs = required_paths_for_stage(stage, all_requirements)
    for key, paths in reqs.items():
        for raw in paths:
            path = ROOT / raw
            if not path.exists():
                add(issues, "fail", "missing_required_contract", f"{key} requires {raw}", raw)
                continue
            if path.suffix.lower() == ".csv":
                header = read_csv_header(path)
                if not header:
                    add(issues, "fail", "empty_csv_header", f"{raw} has no CSV header", raw)
                rows = read_csv_dict(path)
                if raw in REQUIRED_NONEMPTY_BY_KEY.get(key, set()) and not rows:
                    add(issues, "fail", "empty_required_contract", f"{raw} must contain at least one row before {stage}", raw)


def validate_status_values(name: str, rows: Sequence[Mapping[str, Any]], issues: List[Dict[str, str]], *status_keys: str) -> None:
    for idx, row in enumerate(rows, start=2):
        value = status(row, *status_keys)
        if value and value not in ALLOWED_STATUSES:
            add(issues, "warn", "unknown_status", f"{name}:{idx} status={value}", name)


def ids(rows: Sequence[Mapping[str, Any]], key: str, normalizer: Optional[Any] = None) -> Set[str]:
    values: Set[str] = set()
    for row in rows:
        value = clean(row.get(key))
        if value:
            values.add(normalizer(value) if normalizer else value)
    return values


def row_ids(row: Mapping[str, Any], *fields: str, normalizer: Optional[Any] = None) -> List[str]:
    values: List[str] = []
    for field in fields:
        for value in split_ids(row.get(field)):
            values.append(normalizer(value) if normalizer else value)
    return values


def claim_result_bindings(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Set[str]]:
    bindings: Dict[str, Set[str]] = {}
    for row in rows:
        claim_id = clean(row.get("claim_id"))
        if not claim_id:
            continue
        result_ids = set(row_ids(row, "result_id"))
        if clean(row.get("evidence_type")).lower() == "result":
            result_ids.update(row_ids(row, "evidence_ref", "evidence_id"))
        bindings[claim_id] = result_ids
    return bindings


def figure_result_bindings(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Set[str]]:
    bindings: Dict[str, Set[str]] = {}
    for row in rows:
        result_ids = set(row_ids(row, "result_id"))
        evidence_type = clean(row.get("evidence_type")).lower()
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


def has_claim_result_binding(
    row: Mapping[str, Any],
    claim_bindings: Mapping[str, Set[str]],
    figure_bindings: Optional[Mapping[str, Set[str]]] = None,
) -> bool:
    for claim_id in row_ids(row, "claim_ids", "claim_id"):
        if claim_bindings.get(claim_id):
            return True
    figure_id = normalize_figure_id(row.get("figure_id"))
    if figure_id and (figure_bindings or {}).get(figure_id):
        return True
    return False


def path_exists(raw: Any) -> bool:
    value = clean(raw)
    if not value:
        return False
    p = Path(value)
    return (p if p.is_absolute() else ROOT / p).exists()


def validate_result_contract(rows: Sequence[Mapping[str, Any]], issues: List[Dict[str, str]]) -> None:
    validate_status_values("result_contract.csv", rows, issues, "freeze_status", "status")
    for idx, row in enumerate(rows, start=2):
        result_id = clean(row.get("result_id")) or f"row {idx}"
        frozen = status(row, "freeze_status", "status") == "frozen"
        used = has_text(row.get("used_by_figure_ids")) or has_text(row.get("used_by_claim_ids"))
        if frozen or used:
            if not has_text(row.get("source_file")):
                add(issues, "fail", "result_without_source_file", f"{result_id} has no source_file", "14_contracts/result_contract.csv")
            elif not path_exists(row.get("source_file")):
                add(issues, "warn", "result_source_file_missing", f"{result_id} source_file does not exist: {row.get('source_file')}", "14_contracts/result_contract.csv")
            if not has_text(row.get("metric_name")):
                add(issues, "warn", "result_metric_missing", f"{result_id} has no metric_name", "14_contracts/result_contract.csv")
            if not has_text(row.get("metric_value")):
                add(issues, "warn", "result_value_missing", f"{result_id} has no metric_value", "14_contracts/result_contract.csv")


def validate_figure_contract(
    rows: Sequence[Mapping[str, Any]],
    result_ids: Set[str],
    issues: List[Dict[str, str]],
    claim_bindings: Optional[Mapping[str, Set[str]]] = None,
    figure_bindings: Optional[Mapping[str, Set[str]]] = None,
) -> None:
    policy = load_policy()
    threshold = as_float(((policy.get("thresholds") or {}).get("min_figure_quality_score")), 4.2)
    validate_status_values("figure_contract.csv", rows, issues, "status")
    for idx, row in enumerate(rows, start=2):
        figure_id = clean(row.get("figure_id")) or f"row {idx}"
        active = (
            is_active(row, "status")
            or has_text(row.get("used_in_section"))
            or has_text(row.get("file_path"))
            or has_text(row.get("output_svg"))
            or has_text(row.get("output_png"))
            or has_text(row.get("output_pdf"))
            or has_text(row.get("caption"))
            or has_text(row.get("claim_ids"))
            or has_text(row.get("result_id"))
            or has_text(row.get("evidence_source"))
        )
        if not active:
            continue
        result_links = row_ids(row, "result_id")
        bound_by_claim = has_claim_result_binding(row, claim_bindings or {}, figure_bindings or {})
        if not result_links and not has_text(row.get("evidence_source")) and not bound_by_claim:
            add(issues, "fail", "figure_without_result_source", f"{figure_id} has neither result_id nor evidence_source", "14_contracts/figure_contract.csv")
        for result_id in result_links:
            if result_ids and result_id not in result_ids:
                add(issues, "fail", "figure_unknown_result", f"{figure_id} references missing result_id={result_id}", "14_contracts/figure_contract.csv")
        outputs = [row.get("output_svg"), row.get("output_png"), row.get("output_pdf"), row.get("file_path")]
        if not any(path_exists(x) for x in outputs if has_text(x)):
            add(issues, "fail", "figure_file_missing", f"{figure_id} has no existing output_svg/output_png/output_pdf/file_path", "14_contracts/figure_contract.csv")
        score = as_float(row.get("quality_score"), 0.0)
        if score and score < threshold:
            add(issues, "fail", "figure_quality_low", f"{figure_id} quality_score={score} < {threshold}", "14_contracts/figure_contract.csv")
        if has_text(row.get("used_in_section")) and not has_text(row.get("latex_label")):
            add(issues, "warn", "figure_label_missing", f"{figure_id} is used in paper but has no latex_label", "14_contracts/figure_contract.csv")


def validate_formula_contract(rows: Sequence[Mapping[str, Any]], issues: List[Dict[str, str]]) -> None:
    validate_status_values("formula_contract.csv", rows, issues, "status")
    for idx, row in enumerate(rows, start=2):
        formula_id = clean(row.get("formula_id")) or f"row {idx}"
        active = is_active(row, "status") or has_text(row.get("used_in_section"))
        if active and not has_text(row.get("symbols_defined")):
            add(issues, "fail", "formula_symbol_undefined", f"{formula_id} has no symbols_defined", "14_contracts/formula_contract.csv")
        if active and not has_text(row.get("formula_latex")):
            add(issues, "warn", "formula_latex_missing", f"{formula_id} has no formula_latex", "14_contracts/formula_contract.csv")


def validate_citation_contract(rows: Sequence[Mapping[str, Any]], issues: List[Dict[str, str]]) -> None:
    validate_status_values("citation_contract.csv", rows, issues, "status")
    for idx, row in enumerate(rows, start=2):
        citation_id = clean(row.get("citation_id")) or f"row {idx}"
        active = is_active(row, "status") or has_text(row.get("claim_id"))
        if not active:
            continue
        grade = clean(row.get("support_grade")).lower()
        if grade in BAD_SUPPORT:
            add(issues, "fail", "citation_without_support_grade", f"{citation_id} support_grade={grade or '<empty>'}", "14_contracts/citation_contract.csv")
        if not boolish(row.get("metadata_verified")):
            add(issues, "fail", "citation_metadata_unverified", f"{citation_id} metadata_verified is not true", "14_contracts/citation_contract.csv")
        if not has_text(row.get("bibtex_key")):
            add(issues, "warn", "citation_bibtex_key_missing", f"{citation_id} has no bibtex_key", "14_contracts/citation_contract.csv")


def validate_claims(
    rows: Sequence[Mapping[str, Any]],
    result_ids: Set[str],
    figure_ids: Set[str],
    formula_ids: Set[str],
    citation_ids: Set[str],
    issues: List[Dict[str, str]],
) -> None:
    validate_status_values("claim_evidence_map.csv", rows, issues, "status")
    for idx, row in enumerate(rows, start=2):
        claim_id = clean(row.get("claim_id")) or f"row {idx}"
        if not has_text(row.get("claim_text")):
            add(issues, "warn", "claim_text_missing", f"{claim_id} has no claim_text", "14_contracts/claim_evidence_map.csv")
        active = is_active(row, "status") or has_text(row.get("used_in_section"))
        if not active and status(row, "status") != "draft":
            active = has_text(row.get("claim_text"))
        if not active:
            continue

        evidence_type = clean(row.get("evidence_type")).lower()
        result_links = row_ids(row, "result_id")
        figure_links = row_ids(row, "figure_id", "figure_ids", normalizer=normalize_figure_id)
        formula_links = row_ids(row, "formula_id", "formula_ids")
        citation_links = row_ids(row, "citation_id", "citation_ids")
        if evidence_type == "result":
            result_links += row_ids(row, "evidence_ref", "evidence_id")
        elif evidence_type == "figure":
            figure_links += row_ids(row, "evidence_ref", "evidence_id", normalizer=normalize_figure_id)
        elif evidence_type == "formula":
            formula_links += row_ids(row, "evidence_ref", "evidence_id")
        elif evidence_type == "citation":
            citation_links += row_ids(row, "evidence_ref", "evidence_id")
        has_evidence = bool(result_links or figure_links or formula_links or citation_links)
        if not evidence_type and not has_evidence:
            add(issues, "fail", "claim_without_result_or_citation", f"{claim_id} has no evidence field", "14_contracts/claim_evidence_map.csv")
        for result_id in result_links:
            if result_id not in result_ids:
                add(issues, "fail", "unsupported_claim", f"{claim_id} references missing result_id={result_id}", "14_contracts/claim_evidence_map.csv")
        for figure_id in figure_links:
            if figure_id not in figure_ids:
                add(issues, "fail", "unsupported_claim", f"{claim_id} references missing figure_id={figure_id}", "14_contracts/claim_evidence_map.csv")
        for formula_id in formula_links:
            if formula_id not in formula_ids:
                add(issues, "fail", "unsupported_claim", f"{claim_id} references missing formula_id={formula_id}", "14_contracts/claim_evidence_map.csv")
        for citation_id in citation_links:
            if citation_id not in citation_ids:
                add(issues, "fail", "unsupported_claim", f"{claim_id} references missing citation_id={citation_id}", "14_contracts/claim_evidence_map.csv")
        grade = clean(row.get("support_grade")).lower()
        if grade in BAD_SUPPORT and not has_evidence:
            add(issues, "fail", "unsupported_claim", f"{claim_id} support_grade={grade or '<empty>'}", "14_contracts/claim_evidence_map.csv")
        elif grade in BAD_SUPPORT:
            add(issues, "warn", "claim_support_grade_missing", f"{claim_id} support_grade={grade or '<empty>'}", "14_contracts/claim_evidence_map.csv")


def validate_artifact_freeze(rows: Sequence[Mapping[str, Any]], issues: List[Dict[str, str]]) -> None:
    validate_status_values("artifact_freeze_registry.csv", rows, issues, "status")
    for idx, row in enumerate(rows, start=2):
        artifact_id = clean(row.get("artifact_id")) or f"row {idx}"
        if is_active(row, "status") or status(row, "status") == "frozen":
            if not has_text(row.get("path")):
                add(issues, "fail", "frozen_artifact_missing_path", f"{artifact_id} has no path", "14_contracts/artifact_freeze_registry.csv")
            elif not path_exists(row.get("path")):
                add(issues, "fail", "frozen_artifact_file_missing", f"{artifact_id} path does not exist: {row.get('path')}", "14_contracts/artifact_freeze_registry.csv")
            if not has_text(row.get("hash_sha256")):
                add(issues, "warn", "frozen_artifact_hash_missing", f"{artifact_id} has no hash_sha256", "14_contracts/artifact_freeze_registry.csv")


def validate_polish_diff(rows: Sequence[Mapping[str, Any]], issues: List[Dict[str, str]]) -> None:
    policy = load_policy()
    max_delta = as_int(((policy.get("thresholds") or {}).get("max_polish_changed_protected_atoms")), 0)
    for idx, row in enumerate(rows, start=2):
        check_id = clean(row.get("check_id")) or f"row {idx}"
        delta = as_int(row.get("protected_atom_delta_count"), 0)
        decision = clean(row.get("decision")).lower()
        if delta > max_delta or decision in {"fail", "rejected", "block", "blocked"}:
            add(issues, "fail", "polish_changed_protected_atom", f"{check_id} protected_atom_delta_count={delta}, decision={decision}", "14_contracts/polish_diff_check.csv")
        for field, item in (
            ("changed_numbers", "polish_changed_number"),
            ("changed_formulas", "polish_changed_formula"),
            ("changed_labels", "polish_changed_label_or_ref"),
            ("changed_refs", "polish_changed_label_or_ref"),
        ):
            value = clean(row.get(field)).lower()
            if value not in {"", "0", "false", "no", "否", "none"}:
                add(issues, "fail", item, f"{check_id} {field}={row.get(field)}", "14_contracts/polish_diff_check.csv")


def validate_revision_tasks(rows: Sequence[Mapping[str, Any]], issues: List[Dict[str, str]]) -> None:
    validate_status_values("revision_tasks.csv", rows, issues, "status")
    for idx, row in enumerate(rows, start=2):
        task_id = clean(row.get("task_id")) or f"row {idx}"
        sev = clean(row.get("severity")).lower()
        st = status(row, "status")
        if sev in {"fail", "major"} and st not in CLOSED_STATUSES:
            add(issues, "fail", "revision_task_unresolved", f"{task_id} severity={sev}, status={st or '<empty>'}", "14_contracts/revision_tasks.csv")


def validate_review_scorecard(issues: List[Dict[str, str]]) -> None:
    path = ROOT / "11_review" / "review_scorecard.csv"
    if not path.exists():
        add(issues, "warn", "review_scorecard_missing", "11_review/review_scorecard.csv is missing", "11_review/review_scorecard.csv")
        return
    rows = read_csv_dict(path)
    if not rows:
        add(issues, "warn", "review_scorecard_empty", "review_scorecard has no rows", "11_review/review_scorecard.csv")
        return
    policy = load_policy()
    min_score = as_float(((policy.get("thresholds") or {}).get("min_review_score")), 85.0)
    for idx, row in enumerate(rows, start=2):
        score = as_float(row.get("score"), -1.0)
        max_score = as_float(row.get("max_score"), 100.0) or 100.0
        normalized = score / max_score * 100.0 if score >= 0 else -1.0
        if score >= 0 and normalized < min_score:
            add(issues, "fail", "review_score_below_threshold", f"row {idx}: {normalized:.1f} < {min_score}", "11_review/review_scorecard.csv")
        if clean(row.get("severity")).lower() == "fail" and status(row, "status") not in CLOSED_STATUSES:
            add(issues, "fail", "review_fail_unclosed", f"row {idx} severity=fail status={status(row, 'status')}", "11_review/review_scorecard.csv")


def validate_contract_bus(stage: str = "current", all_requirements: bool = False) -> List[Dict[str, str]]:
    issues: List[Dict[str, str]] = []
    validate_required_files(stage, issues, all_requirements=all_requirements)

    base = ROOT / "14_contracts"
    result_rows = read_csv_dict(base / "result_contract.csv")
    figure_rows = read_csv_dict(base / "figure_contract.csv")
    formula_rows = read_csv_dict(base / "formula_contract.csv")
    citation_rows = read_csv_dict(base / "citation_contract.csv")
    claim_rows = read_csv_dict(base / "claim_evidence_map.csv")
    artifact_rows = read_csv_dict(base / "artifact_freeze_registry.csv")
    polish_rows = read_csv_dict(base / "polish_diff_check.csv")
    task_rows = read_csv_dict(base / "revision_tasks.csv")

    if stage in {"finalize", "final_export"} or all_requirements:
        final_rows = {
            "result_contract.csv": result_rows,
            "claim_evidence_map.csv": claim_rows,
            "figure_contract.csv": figure_rows,
        }
        for name, rows in final_rows.items():
            if not rows:
                add(
                    issues,
                    "fail",
                    "empty_final_required_contract",
                    f"{name} must contain at least one row before {stage}",
                    FINAL_REQUIRED_NONEMPTY_CONTRACTS[name],
                )

    result_ids = ids(result_rows, "result_id")
    figure_ids = ids(figure_rows, "figure_id", normalize_figure_id)
    formula_ids = ids(formula_rows, "formula_id")
    citation_ids = ids(citation_rows, "citation_id")
    claim_bindings = claim_result_bindings(claim_rows)
    figure_bindings = figure_result_bindings(claim_rows)

    validate_result_contract(result_rows, issues)
    validate_figure_contract(figure_rows, result_ids, issues, claim_bindings, figure_bindings)
    validate_formula_contract(formula_rows, issues)
    validate_citation_contract(citation_rows, issues)
    validate_claims(claim_rows, result_ids, figure_ids, formula_ids, citation_ids, issues)
    validate_artifact_freeze(artifact_rows, issues)
    validate_polish_diff(polish_rows, issues)
    validate_revision_tasks(task_rows, issues)

    if stage in {"paper_review", "finalize", "auto_review", "revision", "compile", "final_export"} or all_requirements:
        validate_review_scorecard(issues)

    return issues


def write_report(issues: Sequence[Mapping[str, str]], stage: str) -> None:
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    fail_count = sum(1 for i in issues if i.get("level") == "fail")
    warn_count = sum(1 for i in issues if i.get("level") == "warn")
    payload = {
        "stage": stage,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "fail_count": fail_count,
        "warn_count": warn_count,
        "issue_count": len(issues),
        "issues": list(issues),
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Contract validation report",
        "",
        f"- stage: {stage}",
        f"- fail_count: {fail_count}",
        f"- warn_count: {warn_count}",
        "",
    ]
    if not issues:
        lines.append("No contract-bus issues found. Human review is still required.")
    else:
        for issue in issues:
            loc = f" ({issue.get('path')})" if issue.get("path") else ""
            lines.append(f"- [{issue.get('level')}] {issue.get('item')}{loc}: {issue.get('detail')}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_validation(stage: str = "current", all_requirements: bool = False, write: bool = True) -> List[Dict[str, str]]:
    if stage == "current":
        stage = str(read_state().get("current_stage") or "current")
    issues = validate_contract_bus(stage, all_requirements=all_requirements)
    if write:
        write_report(issues, stage)
    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate v4 formal-workflow contract bus files.")
    parser.add_argument("--stage", default="current", help="Stage name or current.")
    parser.add_argument("--root", default="", help="Optional workflow root to validate, e.g. a training sandbox workspace.")
    parser.add_argument("--all", action="store_true", help="Validate all configured requirement groups.")
    parser.add_argument("--warn-only", action="store_true", help="Never return non-zero for fail issues.")
    args = parser.parse_args()

    if args.root:
        configure_root(Path(args.root))
    issues = run_validation(args.stage, all_requirements=args.all, write=True)
    fail_count = sum(1 for i in issues if i.get("level") == "fail")
    print(f"[OK] wrote {rel(REPORT_JSON)} and {rel(REPORT_MD)}")
    if fail_count and not args.warn_only:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
