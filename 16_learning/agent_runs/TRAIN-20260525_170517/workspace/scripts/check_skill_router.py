from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - fallback is intentionally narrow.
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "config" / "skill_router_policy.yaml"
STATE_PATH = ROOT / "workflow_state.yaml"
REPORT_JSON = ROOT / "11_review" / "skill_router_report.json"
REPORT_MD = ROOT / "11_review" / "skill_router_report.md"
RUNTIME_VERSION = "v3.2-p1-runtime"

USAGE_LOG_HEADER = [
    "call_id",
    "timestamp",
    "stage_id",
    "skill_id",
    "permission_level",
    "router_decision",
    "required_inputs_status",
    "archive_path",
    "output_type",
    "promotion_target",
    "validation_status",
    "failure_code",
    "human_confirmation_required",
    "notes",
]

ALLOWED_ROUTER_DECISIONS = {
    "allow",
    "deny",
    "skip",
    "block",
    "archive_only",
    "promotion_validated",
    "promotion_blocked",
}
ALLOWED_INPUT_STATUS = {
    "exists",
    "missing_optional",
    "missing_required",
    "stale",
    "frozen",
    "invalid_contract",
}
ALLOWED_VALIDATION_STATUS = {"not_run", "passed", "warning", "failed", "blocked"}


class RouterError(Exception):
    def __init__(self, message: str, exit_code: int = 2) -> None:
        super().__init__(message)
        self.exit_code = exit_code


class CheckRecorder:
    def __init__(self) -> None:
        self.checks: List[Dict[str, Any]] = []

    def add(
        self,
        check_id: str,
        name: str,
        status: str,
        message: str,
        related_path: str = "config/skill_router_policy.yaml",
        severity: Optional[str] = None,
    ) -> None:
        if severity is None:
            severity = {"pass": "info", "warning": "warning", "fail": "fail"}.get(status, "info")
        self.checks.append(
            {
                "check_id": check_id,
                "name": name,
                "status": status,
                "severity": severity,
                "message": message,
                "related_path": related_path,
            }
        )

    @property
    def error_count(self) -> int:
        return sum(1 for item in self.checks if item.get("status") == "fail")

    @property
    def warning_count(self) -> int:
        return sum(1 for item in self.checks if item.get("status") == "warning")

    @property
    def status(self) -> str:
        if self.error_count:
            return "fail"
        if self.warning_count:
            return "warning"
        return "pass"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def safe_load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise RouterError(f"missing YAML file: {rel(path)}", 2)
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return {}
    if yaml is None:
        try:
            return json.loads(text)
        except Exception as exc:
            raise RouterError(f"PyYAML unavailable and JSON fallback failed for {rel(path)}: {exc}", 2) from exc
    try:
        data = yaml.safe_load(text)
        return data or {}
    except Exception as exc:
        raise RouterError(f"YAML parse failed for {rel(path)}: {exc}", 2) from exc


def safe_dump_yaml(data: Mapping[str, Any]) -> str:
    if yaml is not None:
        return yaml.safe_dump(dict(data), allow_unicode=True, sort_keys=False)
    return json.dumps(data, ensure_ascii=False, indent=2)


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except Exception:
        return path.as_posix()


def load_policy(recorder: Optional[CheckRecorder] = None) -> Dict[str, Any]:
    try:
        policy = safe_load_yaml(POLICY_PATH)
        if recorder:
            recorder.add("SR-POLICY-001", "policy_yaml_parse", "pass", "policy YAML parses")
        return policy
    except RouterError as exc:
        if recorder:
            recorder.add("SR-POLICY-001", "policy_yaml_parse", "fail", str(exc))
        raise


def load_state() -> Dict[str, Any]:
    if not STATE_PATH.exists():
        return {}
    try:
        return safe_load_yaml(STATE_PATH)
    except RouterError:
        return {}


def ordered_stages(policy: Mapping[str, Any]) -> List[str]:
    return [str(item) for item in (((policy.get("stage_identity_policy") or {}).get("ordered_stages")) or [])]


def stage_prompt_files(policy: Mapping[str, Any]) -> Dict[str, str]:
    return {str(k): str(v) for k, v in (((policy.get("stage_identity_policy") or {}).get("stage_prompt_files")) or {}).items()}


def legacy_stages(policy: Mapping[str, Any]) -> set[str]:
    return set(str(k) for k in (((policy.get("stage_identity_policy") or {}).get("legacy_stage_names")) or {}).keys())


def skills(policy: Mapping[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {str(k): dict(v or {}) for k, v in (policy.get("skills") or {}).items()}


def permission_levels(policy: Mapping[str, Any]) -> set[str]:
    return set(str(k) for k in (((policy.get("permission_model") or {}).get("levels")) or {}).keys())


def stage_routes(policy: Mapping[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {str(k): dict(v or {}) for k, v in (policy.get("stage_routes") or {}).items()}


def route_for_skill(policy: Mapping[str, Any], stage_id: str, skill_id: str) -> Optional[Dict[str, Any]]:
    route = stage_routes(policy).get(stage_id) or {}
    for item in route.get("allowed_skills") or []:
        if str((item or {}).get("skill_id")) == skill_id:
            return dict(item or {})
    return None


def all_skill_output_types(policy: Mapping[str, Any]) -> set[str]:
    output_types: set[str] = set()
    for meta in skills(policy).values():
        output_types.update(str(item) for item in (meta.get("allowed_output_types") or []))
    return output_types


def failure_codes(policy: Mapping[str, Any]) -> set[str]:
    return set(str(k) for k in ((((policy.get("failure_policy") or {}).get("failure_codes")) or {}).keys()))


def failure_recovery(policy: Mapping[str, Any], code: str) -> str:
    return str(((((policy.get("failure_policy") or {}).get("failure_codes")) or {}).get(code) or {}).get("recovery") or "")


def checksum(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def path_exists(path_text: str) -> bool:
    return (ROOT / path_text).exists()


def resolve_under_root(path_text: str) -> Path:
    path = (ROOT / path_text).resolve()
    root = ROOT.resolve()
    try:
        path.relative_to(root)
    except Exception as exc:
        raise RouterError(f"path escapes project root: {path_text}", 4) from exc
    return path


def archive_root(policy: Mapping[str, Any]) -> Path:
    root_text = str(((policy.get("output_archiving") or {}).get("root")) or "10_ai_logs/skill_outputs")
    return resolve_under_root(root_text)


def ensure_archive_dir_inside_policy_root(policy: Mapping[str, Any], archive_dir: Path) -> Path:
    root = archive_root(policy).resolve()
    actual = archive_dir.resolve()
    try:
        actual.relative_to(root)
    except Exception as exc:
        raise RouterError("archive path outside allowed root", 4) from exc
    return actual


def usage_log_path(policy: Mapping[str, Any]) -> Path:
    log_text = str(((policy.get("usage_log") or {}).get("path")) or "10_ai_logs/skill_usage_log.csv")
    return resolve_under_root(log_text)


def read_csv_header(path: Path) -> List[str]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        return next(reader, [])


def markdown_key_values(text: str) -> Dict[str, str]:
    values: Dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("-") or line.startswith("```"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in values:
            values[key] = value
    return values


def normalize_placeholder(value: Any) -> str:
    text = str(value or "").strip()
    if not text or (text.startswith("<") and text.endswith(">")):
        return ""
    return text


RAW_OUTPUT_EMPTY_SENTINEL = "RAW_OUTPUT_STATUS: EMPTY_INITIALIZED"
RAW_OUTPUT_FILLED_SENTINELS = {
    "RAW_OUTPUT_STATUS: FILLED",
    "RAW_OUTPUT_STATUS: FILLED_BY_SKILL_OR_HUMAN",
    "RAW_OUTPUT_STATUS: FILLED_BY_EXTERNAL_SKILL",
    "RAW_OUTPUT_STATUS: FILLED_BY_HUMAN",
}


CONTRACT_BINDING_SOURCES: Dict[str, List[Tuple[str, str]]] = {
    "claim_id": [("14_contracts/claim_evidence_map.csv", "claim_id")],
    "section_id": [
        ("14_contracts/claim_evidence_map.csv", "section_id"),
        ("14_contracts/citation_contract.csv", "section_id"),
        ("14_contracts/formula_contract.csv", "section_id"),
        ("14_contracts/polish_diff_check.csv", "section_id"),
    ],
    "evidence_id": [("14_contracts/claim_evidence_map.csv", "evidence_id")],
    "result_id": [
        ("14_contracts/result_contract.csv", "result_id"),
        ("14_contracts/claim_evidence_map.csv", "result_id"),
        ("14_contracts/figure_contract.csv", "result_id"),
    ],
    "figure_id": [
        ("14_contracts/figure_contract.csv", "figure_id"),
        ("14_contracts/claim_evidence_map.csv", "figure_id"),
    ],
    "formula_id": [
        ("14_contracts/formula_contract.csv", "formula_id"),
        ("14_contracts/claim_evidence_map.csv", "formula_id"),
    ],
    "citation_id": [
        ("14_contracts/citation_contract.csv", "citation_id"),
        ("14_contracts/claim_evidence_map.csv", "citation_id"),
    ],
    "reviewer_issue_id": [
        ("11_review/revision_tasks.csv", "source_comment_id"),
        ("14_contracts/revision_tasks.csv", "source_comment_id"),
        ("11_review/revision_tasks.csv", "task_id"),
        ("14_contracts/revision_tasks.csv", "task_id"),
    ],
}

# Empty contract status is intentionally invalid. A promotion must be based on a
# row that has been explicitly accepted/frozen/verified by the contract layer.
CONTRACT_STATUS_ALLOWED: Dict[str, Tuple[str, set[str]]] = {
    "14_contracts/claim_evidence_map.csv": ("status", {"valid", "verified", "accepted", "approved", "frozen"}),
    "14_contracts/result_contract.csv": ("freeze_status", {"frozen", "verified", "accepted", "approved", "valid"}),
    "14_contracts/figure_contract.csv": ("status", {"valid", "verified", "accepted", "approved", "frozen"}),
    "14_contracts/formula_contract.csv": ("status", {"valid", "verified", "accepted", "approved", "frozen"}),
    "14_contracts/citation_contract.csv": ("status", {"valid", "verified", "accepted", "approved", "frozen"}),
    "14_contracts/polish_diff_check.csv": ("decision", {"passed", "accepted", "approved", "waived", "waived_with_reason"}),
    "14_contracts/artifact_freeze_registry.csv": ("status", {"frozen", "valid", "verified", "accepted", "approved"}),
    "11_review/revision_tasks.csv": ("status", {"open", "accepted", "approved", "verified", "closed", "done"}),
    "14_contracts/revision_tasks.csv": ("status", {"open", "accepted", "approved", "verified", "closed", "done"}),
}


def raw_output_effective_lines(raw_text: str) -> List[str]:
    """Return lines that look like real skill/user output rather than scaffold metadata."""
    ignored_prefixes = (
        "WARNING: This file is an archive-only capture area.",
        "To make this eligible for promotion, replace the sentinel with RAW_OUTPUT_STATUS:",
        "call_id:",
        "stage_id:",
        "skill_id:",
        "RAW_OUTPUT_STATUS:",
    )
    ignored_exact = {"# Raw skill output"}
    effective: List[str] = []
    in_fence = False
    for raw_line in raw_text.splitlines():
        line = raw_line.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not line:
            continue
        if not in_fence and line in ignored_exact:
            continue
        if not in_fence and any(line.startswith(prefix) for prefix in ignored_prefixes):
            continue
        effective.append(line)
    return effective


def raw_output_has_real_content(raw_text: str) -> Tuple[bool, str]:
    if not raw_text.strip():
        return False, "raw_output.md is empty"
    if RAW_OUTPUT_EMPTY_SENTINEL in raw_text:
        return False, "raw_output.md still has EMPTY_INITIALIZED sentinel"
    effective = raw_output_effective_lines(raw_text)
    if not effective:
        return False, "raw_output.md contains only scaffold header/metadata"
    if sum(len(line) for line in effective) < 20 and not any(s in raw_text for s in RAW_OUTPUT_FILLED_SENTINELS):
        return False, "raw_output.md has too little non-scaffold content"
    return True, "raw_output.md contains non-scaffold content"


def extract_resolved_bindings(notes_text: str) -> List[Dict[str, str]]:
    """Parse the resolved_bindings YAML-like list from promotion_notes.md.

    The notes file is Markdown, so this deliberately parses only the small
    resolved_bindings shape used by the templates instead of trusting arbitrary
    key/value text elsewhere in the document.
    """
    records: List[Dict[str, str]] = []
    current: Optional[Dict[str, str]] = None
    in_resolved = False

    for raw in notes_text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("```"):
            continue
        if stripped.startswith("resolved_bindings:"):
            in_resolved = True
            if current:
                records.append(current)
                current = None
            continue
        if not in_resolved:
            continue
        if stripped.startswith("required_bindings:") or stripped.startswith("validation_status:") or stripped.startswith("human_confirmation_required:"):
            break
        if stripped.startswith("-"):
            if current:
                records.append(current)
            current = {}
            payload = stripped[1:].strip()
            if payload and ":" in payload:
                key, value = payload.split(":", 1)
                current[key.strip()] = value.strip().strip('"').strip("'")
            continue
        if current is not None and ":" in stripped:
            key, value = stripped.split(":", 1)
            current[key.strip()] = value.strip().strip('"').strip("'")

    if current:
        records.append(current)
    return records


def contract_row_status_ok(contract_path: str, row: Mapping[str, str]) -> Tuple[bool, str]:
    status_column, allowed = CONTRACT_STATUS_ALLOWED.get(contract_path, ("status", {"valid", "verified", "accepted", "approved", "frozen"}))
    raw_status = str(row.get(status_column) or "").strip().lower()
    if not raw_status:
        return False, f"{contract_path}:{status_column} is blank"
    if raw_status not in allowed:
        return False, f"{contract_path}:{status_column}={raw_status} is not one of {sorted(allowed)}"
    return True, f"{contract_path}:{status_column}={raw_status}"


def csv_contract_find_rows(contract_path: str, column: str, binding_id: str) -> Tuple[List[Dict[str, str]], List[str]]:
    messages: List[str] = []
    try:
        path = resolve_under_root(contract_path)
    except RouterError as exc:
        return [], [str(exc)]
    if not path.exists():
        return [], [f"contract file missing: {contract_path}"]
    if path.suffix.lower() != ".csv":
        return [], [f"unsupported contract type for binding lookup: {contract_path}"]
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or column not in reader.fieldnames:
                return [], [f"column {column} not found in {contract_path}"]
            matches: List[Dict[str, str]] = []
            invalid_status_messages: List[str] = []
            for row in reader:
                if str(row.get(column) or "").strip() != binding_id:
                    continue
                ok, status_message = contract_row_status_ok(contract_path, row)
                if ok:
                    matches.append(dict(row))
                else:
                    invalid_status_messages.append(status_message)
            if matches:
                return matches, [f"{binding_id} found as valid {column} in {contract_path}"]
            if invalid_status_messages:
                return [], invalid_status_messages
    except Exception as exc:
        return [], [f"failed to read {contract_path}: {exc}"]
    return [], [f"{binding_id} not found as valid {column} in {contract_path}"]


def csv_contract_contains(contract_path: str, column: str, binding_id: str) -> Tuple[bool, str]:
    rows, messages = csv_contract_find_rows(contract_path, column, binding_id)
    return bool(rows), "; ".join(messages)


def binding_requirement_options(requirement: str) -> List[str]:
    req = requirement.strip()
    if "_or_" in req:
        return [part.strip() for part in req.split("_or_") if part.strip()]
    return [req]


def resolved_record_matches_token(record: Mapping[str, str], token: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    binding_id = normalize_placeholder(record.get("id"))
    source_contract = normalize_placeholder(record.get("source_contract"))
    status = normalize_placeholder(record.get("status")).lower()
    if not binding_id:
        return False, None, "binding id is blank"
    if status != "valid":
        return False, None, f"binding {binding_id} status is not valid"

    allowed_sources = CONTRACT_BINDING_SOURCES.get(token, [])
    if not allowed_sources:
        return False, None, f"unknown binding token: {token}"

    candidate_sources = allowed_sources
    if source_contract:
        source_matches = [item for item in allowed_sources if item[0] == source_contract]
        if not source_matches:
            return False, None, f"{source_contract} cannot satisfy {token}"
        candidate_sources = source_matches

    messages: List[str] = []
    for contract_path, column in candidate_sources:
        rows, row_messages = csv_contract_find_rows(contract_path, column, binding_id)
        if rows:
            return True, {
                "token": token,
                "id": binding_id,
                "source_contract": source_contract or contract_path,
                "contract_path": contract_path,
                "column": column,
                "rows": rows,
            }, row_messages[0]
        messages.extend(row_messages)
    return False, None, "; ".join(messages)


def resolved_record_is_valid_for_token(record: Mapping[str, str], token: str) -> Tuple[bool, str]:
    ok, _match, message = resolved_record_matches_token(record, token)
    return ok, message


def row_has_values(row: Mapping[str, str], expected: Mapping[str, str]) -> bool:
    for column, expected_value in expected.items():
        if expected_value and str(row.get(column) or "").strip() != expected_value:
            return False
    return True


def find_valid_contract_row(contract_path: str, expected: Mapping[str, str]) -> Tuple[bool, str]:
    try:
        path = resolve_under_root(contract_path)
    except RouterError as exc:
        return False, str(exc)
    if not path.exists():
        return False, f"contract file missing: {contract_path}"
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            fieldnames = set(reader.fieldnames or [])
            missing_columns = [column for column in expected if column not in fieldnames]
            if missing_columns:
                return False, f"columns {missing_columns} not found in {contract_path}"
            status_failures: List[str] = []
            for row in reader:
                if not row_has_values(row, expected):
                    continue
                ok, status_message = contract_row_status_ok(contract_path, row)
                if ok:
                    pairs = ", ".join(f"{k}={v}" for k, v in expected.items() if v)
                    return True, f"{contract_path} has valid row with {pairs}"
                status_failures.append(status_message)
            if status_failures:
                return False, "; ".join(status_failures)
    except Exception as exc:
        return False, f"failed to read {contract_path}: {exc}"
    pairs = ", ".join(f"{k}={v}" for k, v in expected.items() if v)
    return False, f"no valid row in {contract_path} with {pairs}"


def split_contract_cell(value: str) -> set[str]:
    parts = re.split(r"[;,|\s]+", str(value or "").strip())
    return {part for part in parts if part}


def result_figure_relation_ok(result_id: str, figure_id: str) -> Tuple[bool, str]:
    ok, message = find_valid_contract_row("14_contracts/figure_contract.csv", {"figure_id": figure_id, "result_id": result_id})
    if ok:
        return True, message
    result_rows, result_messages = csv_contract_find_rows("14_contracts/result_contract.csv", "result_id", result_id)
    if result_rows:
        for row in result_rows:
            if figure_id in split_contract_cell(str(row.get("used_by_figure_ids") or "")):
                return True, f"14_contracts/result_contract.csv links result_id={result_id} to figure_id={figure_id}"
    return False, message + "; " + "; ".join(result_messages)


def claim_secondary_relation_ok(claim_id: str, secondary_token: str, secondary_id: str) -> Tuple[bool, str]:
    column = {
        "evidence_id": "evidence_id",
        "result_id": "result_id",
        "figure_id": "figure_id",
        "formula_id": "formula_id",
        "citation_id": "citation_id",
    }.get(secondary_token)
    if not column:
        return True, f"no relation check needed for claim_id + {secondary_token}"
    ok, message = find_valid_contract_row("14_contracts/claim_evidence_map.csv", {"claim_id": claim_id, column: secondary_id})
    if ok:
        return True, message
    if secondary_token == "result_id":
        result_rows, result_messages = csv_contract_find_rows("14_contracts/result_contract.csv", "result_id", secondary_id)
        if result_rows:
            for row in result_rows:
                if claim_id in split_contract_cell(str(row.get("used_by_claim_ids") or "")):
                    return True, f"14_contracts/result_contract.csv links result_id={secondary_id} to claim_id={claim_id}"
        message += "; " + "; ".join(result_messages)
    return False, message


def section_citation_relation_ok(section_id: str, citation_id: str) -> Tuple[bool, str]:
    return find_valid_contract_row("14_contracts/citation_contract.csv", {"section_id": section_id, "citation_id": citation_id})


def relation_consistency_checks(output_type: str, matched: Mapping[str, Dict[str, Any]]) -> List[str]:
    problems: List[str] = []

    if output_type in {"section_draft", "claim_rewrite"}:
        claim = matched.get("claim_id")
        secondary = next((matched.get(token) for token in ["evidence_id", "result_id", "figure_id", "formula_id", "citation_id"] if matched.get(token)), None)
        if claim and secondary:
            ok, message = claim_secondary_relation_ok(str(claim.get("id") or ""), str(secondary.get("token") or ""), str(secondary.get("id") or ""))
            if not ok:
                problems.append(f"claim binding mismatch: {message}")

    if output_type == "figure_blueprint":
        result = matched.get("result_id")
        figure = matched.get("figure_id")
        if result and figure:
            ok, message = result_figure_relation_ok(str(result.get("id") or ""), str(figure.get("id") or ""))
            if not ok:
                problems.append(f"figure/result binding mismatch: {message}")

    if output_type == "caption_candidate":
        figure = matched.get("figure_id")
        result = matched.get("result_id")
        claim = matched.get("claim_id")
        if figure and result:
            ok, message = result_figure_relation_ok(str(result.get("id") or ""), str(figure.get("id") or ""))
            if not ok:
                problems.append(f"caption figure/result mismatch: {message}")
        if figure and claim:
            ok, message = claim_secondary_relation_ok(str(claim.get("id") or ""), "figure_id", str(figure.get("id") or ""))
            if not ok:
                problems.append(f"caption claim/figure mismatch: {message}")

    if output_type == "citation_candidate":
        citation = matched.get("citation_id")
        claim = matched.get("claim_id")
        section = matched.get("section_id")
        if citation and claim:
            ok, message = find_valid_contract_row("14_contracts/citation_contract.csv", {"citation_id": str(citation.get("id") or ""), "claim_id": str(claim.get("id") or "")})
            if not ok:
                problems.append(f"citation/claim mismatch: {message}")
        if citation and section:
            ok, message = section_citation_relation_ok(str(section.get("id") or ""), str(citation.get("id") or ""))
            if not ok:
                problems.append(f"citation/section mismatch: {message}")

    return problems


def validate_contract_bindings(required_bindings: Sequence[str], notes_text: str, output_type: str = "") -> Tuple[bool, List[str], List[str]]:
    resolved = extract_resolved_bindings(notes_text)
    if not resolved:
        return False, [], ["no resolved_bindings records found"]

    satisfied: List[str] = []
    problems: List[str] = []
    matched_by_token: Dict[str, Dict[str, Any]] = {}
    for requirement in required_bindings:
        tokens = binding_requirement_options(str(requirement))
        matched = False
        token_problems: List[str] = []
        for token in tokens:
            for record in resolved:
                ok, match, message = resolved_record_matches_token(record, token)
                if ok and match:
                    satisfied.append(f"{requirement} via {message}")
                    matched_by_token[token] = match
                    matched = True
                    break
                token_problems.append(message)
            if matched:
                break
        if not matched:
            unique = []
            for item in token_problems:
                if item and item not in unique:
                    unique.append(item)
            problems.append(f"{requirement}: " + ("; ".join(unique) if unique else "no valid matching binding"))

    if not problems:
        relation_problems = relation_consistency_checks(output_type, matched_by_token)
        problems.extend(relation_problems)

    return not problems, satisfied, problems


def write_reports(
    recorder: CheckRecorder,
    policy: Optional[Mapping[str, Any]],
    decision: Optional[Mapping[str, Any]] = None,
    recommended_action: Optional[str] = None,
) -> None:
    policy = policy or {}
    ordered = ordered_stages(policy)
    registered = skills(policy)
    routes = stage_routes(policy)
    payload = {
        "version": RUNTIME_VERSION,
        "timestamp": utc_now(),
        "policy_path": "config/skill_router_policy.yaml",
        "status": recorder.status,
        "summary": {
            "stages_checked": len(ordered),
            "skills_registered": len(registered),
            "stage_routes_checked": len(routes),
            "errors": recorder.error_count,
            "warnings": recorder.warning_count,
        },
        "checks": recorder.checks,
        "skill_call_decision": {
            "stage_id": None,
            "skill_id": None,
            "router_decision": None,
            "permission_level": None,
            "required_inputs_status": None,
            "failure_code": None,
            "human_confirmation_required": False,
        },
    }
    if decision:
        payload["skill_call_decision"].update(dict(decision))

    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Skill Router Report",
        "",
        f"- overall_status: {payload['status']}",
        "- policy_file_checked: config/skill_router_policy.yaml",
        f"- stage_route_coverage: {len(routes)}/{len(ordered)}",
        f"- skill_registry_coverage: {len(registered)} registered skills",
        f"- usage_log_compatibility: {'checked' if any(c['name'] == 'usage_log_header' for c in recorder.checks) else 'not_checked'}",
        f"- errors: {recorder.error_count}",
        f"- warnings: {recorder.warning_count}",
        "",
        "## Errors",
        "",
    ]
    errors = [c for c in recorder.checks if c.get("status") == "fail"]
    if errors:
        lines.extend(f"- {c['check_id']} {c['name']}: {c['message']} ({c.get('related_path','')})" for c in errors)
    else:
        lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    warnings = [c for c in recorder.checks if c.get("status") == "warning"]
    if warnings:
        lines.extend(f"- {c['check_id']} {c['name']}: {c['message']} ({c.get('related_path','')})" for c in warnings)
    else:
        lines.append("- none")
    if decision:
        lines.extend(["", "## Skill call decision", ""])
        for key, value in decision.items():
            lines.append(f"- {key}: {value}")
    lines.extend(["", "## Recommended next action", ""])
    lines.append(f"- {recommended_action or ('fix failed checks' if recorder.error_count else 'router validation passed')}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_policy() -> Tuple[CheckRecorder, Dict[str, Any]]:
    recorder = CheckRecorder()
    try:
        policy = load_policy(recorder)
    except RouterError:
        write_reports(recorder, {}, recommended_action="fix policy YAML before running router checks")
        return recorder, {}

    required_top = [
        "version",
        "stage_identity_policy",
        "router_mode",
        "permission_model",
        "skills",
        "stage_routes",
        "required_inputs",
        "output_archiving",
        "usage_log",
        "promotion_rules",
        "failure_policy",
    ]
    missing = [key for key in required_top if key not in policy]
    recorder.add(
        "SR-POLICY-002",
        "required_top_level_keys",
        "fail" if missing else "pass",
        f"missing keys: {', '.join(missing)}" if missing else "all required top-level keys exist",
    )

    stages = ordered_stages(policy)
    prompts = stage_prompt_files(policy)
    if not stages:
        recorder.add("SR-STAGE-001", "ordered_stages_known", "fail", "no ordered_stages configured")
    else:
        recorder.add("SR-STAGE-001", "ordered_stages_known", "pass", f"{len(stages)} stages configured")

    prompt_missing_keys = [stage for stage in stages if stage not in prompts]
    prompt_missing_files = [path for path in prompts.values() if not (ROOT / path).exists()]
    prompt_status = "fail" if prompt_missing_keys or prompt_missing_files else "pass"
    prompt_message = "stage prompt mapping and files exist"
    if prompt_missing_keys or prompt_missing_files:
        prompt_message = f"missing prompt keys={prompt_missing_keys}; missing files={prompt_missing_files}"
    recorder.add("SR-STAGE-002", "stage_prompt_files", prompt_status, prompt_message, "prompts/stages")

    routes = stage_routes(policy)
    route_keys = set(routes.keys())
    stage_set = set(stages)
    legacy = legacy_stages(policy)
    bad_routes = sorted(route_keys - stage_set)
    legacy_routes = sorted(route_keys & legacy)
    recorder.add(
        "SR-STAGE-003",
        "stage_routes_real_stages",
        "fail" if bad_routes else "pass",
        f"unknown stage routes: {bad_routes}" if bad_routes else "all stage route keys are real ordered stages",
    )
    recorder.add(
        "SR-STAGE-004",
        "legacy_stage_names_rejected",
        "fail" if legacy_routes else "pass",
        f"legacy stage routes present: {legacy_routes}" if legacy_routes else "no legacy stage routes are present",
    )

    registered_skills = skills(policy)
    levels = permission_levels(policy)
    unregistered_route_skills: List[str] = []
    invalid_route_permissions: List[str] = []
    for stage_id, route in routes.items():
        for item in route.get("allowed_skills") or []:
            sid = str((item or {}).get("skill_id") or "")
            if sid not in registered_skills:
                unregistered_route_skills.append(f"{stage_id}:{sid}")
            perm = str((item or {}).get("permission") or "")
            if perm not in levels:
                invalid_route_permissions.append(f"{stage_id}:{sid}:{perm}")
    recorder.add(
        "SR-SKILL-001",
        "route_skills_registered",
        "fail" if unregistered_route_skills else "pass",
        f"unregistered route skills: {unregistered_route_skills}" if unregistered_route_skills else "all route skills are registered",
    )

    incomplete_skills = []
    for sid, meta in registered_skills.items():
        required = ["category", "status", "source", "mode", "default_permission"]
        missing_meta = [key for key in required if key not in meta]
        if missing_meta:
            incomplete_skills.append(f"{sid}:{missing_meta}")
        if str(meta.get("default_permission")) not in levels:
            invalid_route_permissions.append(f"{sid}:default_permission:{meta.get('default_permission')}")
    recorder.add(
        "SR-SKILL-002",
        "skill_registry_metadata",
        "fail" if incomplete_skills else "pass",
        f"skills missing metadata: {incomplete_skills}" if incomplete_skills else "registered skills contain required metadata",
    )
    recorder.add(
        "SR-SKILL-003",
        "permission_levels_defined",
        "fail" if invalid_route_permissions else "pass",
        f"invalid permissions: {invalid_route_permissions}" if invalid_route_permissions else "all referenced permissions are defined",
    )

    input_rules = policy.get("required_inputs") or {}
    unknown_input_rules = sorted(str(sid) for sid in input_rules if str(sid) not in registered_skills)
    recorder.add(
        "SR-IN-001",
        "required_input_rules_registered",
        "fail" if unknown_input_rules else "pass",
        f"required input rules for unknown skills: {unknown_input_rules}" if unknown_input_rules else "all required input rules reference registered skills",
    )

    log_path = usage_log_path(policy)
    expected_header = [str(item) for item in (((policy.get("usage_log") or {}).get("columns")) or USAGE_LOG_HEADER)]
    actual_header = read_csv_header(log_path)
    if not actual_header and (policy.get("usage_log") or {}).get("create_if_missing"):
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerow(expected_header)
        actual_header = expected_header
    recorder.add(
        "SR-LOG-001",
        "usage_log_header",
        "fail" if actual_header != expected_header else "pass",
        f"actual header does not match policy: {actual_header}" if actual_header != expected_header else "usage log header matches policy",
        rel(log_path),
    )

    known_outputs = all_skill_output_types(policy)
    promo_targets = (((policy.get("promotion_rules") or {}).get("allowed_targets")) or {})
    unknown_promo_outputs = sorted(str(key) for key in promo_targets.keys() if str(key) not in known_outputs)
    unpromoted_outputs = sorted(known_outputs - set(str(key) for key in promo_targets.keys()))
    recorder.add(
        "SR-PROMO-001",
        "promotion_targets_registered_output_types",
        "fail" if unknown_promo_outputs else "pass",
        f"promotion rules use unknown output types: {unknown_promo_outputs}" if unknown_promo_outputs else "promotion rule output types are registered",
    )
    recorder.add(
        "SR-PROMO-006",
        "archive_only_output_types",
        "pass",
        f"registered output types without promotion targets remain archive_only: {unpromoted_outputs}" if unpromoted_outputs else "all registered output types have explicit promotion targets",
    )

    global_forbidden = (((policy.get("permission_model") or {}).get("global_forbidden_actions")) or [])
    forbidden_required = {
        "modify_workflow_state_yaml": "SR-PERM-001",
        "modify_AGENTS_md": "SR-PERM-002",
        "modify_scripts_directory": "SR-PERM-003",
        "directly_edit_final_submission_package": "SR-PERM-005",
    }
    for action, check_id in forbidden_required.items():
        recorder.add(
            check_id,
            action,
            "pass" if action in global_forbidden else "fail",
            f"{action} is globally forbidden" if action in global_forbidden else f"{action} is not globally forbidden",
        )
    router_mode = policy.get("router_mode") or {}
    recorder.add(
        "SR-PERM-004",
        "skills_cannot_write_contracts_directly",
        "pass" if router_mode.get("allow_skill_to_modify_contracts_directly") is False else "fail",
        "direct contract writes are blocked" if router_mode.get("allow_skill_to_modify_contracts_directly") is False else "direct contract writes are not blocked",
    )
    return recorder, policy


def compute_required_input_status(policy: Mapping[str, Any], skill_id: str) -> Tuple[str, List[str], List[str], List[Dict[str, str]]]:
    rule = ((policy.get("required_inputs") or {}).get(skill_id)) or {}
    all_of = [str(item) for item in (rule.get("all_of") or [])]
    any_of = [str(item) for item in (rule.get("any_of") or [])]
    recommended = [str(item) for item in (rule.get("recommended") or [])]
    missing_required: List[str] = []
    missing_optional: List[str] = []
    file_records: List[Dict[str, str]] = []

    for path_text in all_of:
        exists = path_exists(path_text)
        if not exists:
            missing_required.append(path_text)
        p = ROOT / path_text
        file_records.append({"path": path_text, "role": "all_of", "status": "exists" if exists else "missing", "checksum_sha256": checksum(p)})

    if any_of:
        any_exists = False
        for path_text in any_of:
            exists = path_exists(path_text)
            any_exists = any_exists or exists
            p = ROOT / path_text
            file_records.append({"path": path_text, "role": "any_of", "status": "exists" if exists else "missing", "checksum_sha256": checksum(p)})
        if not any_exists:
            missing_required.extend(any_of)

    for path_text in recommended:
        exists = path_exists(path_text)
        if not exists:
            missing_optional.append(path_text)
        p = ROOT / path_text
        file_records.append({"path": path_text, "role": "recommended", "status": "exists" if exists else "missing", "checksum_sha256": checksum(p)})

    if missing_required:
        return "missing_required", missing_required, missing_optional, file_records
    if missing_optional:
        return "missing_optional", [], missing_optional, file_records
    return "exists", [], [], file_records


def preflight(args: argparse.Namespace) -> Tuple[CheckRecorder, Dict[str, Any], Dict[str, Any], int]:
    recorder, policy = validate_policy()
    decision: Dict[str, Any] = {
        "stage_id": args.stage,
        "skill_id": args.skill,
        "router_decision": "deny",
        "permission_level": None,
        "required_inputs_status": None,
        "failure_code": None,
        "human_confirmation_required": False,
    }
    if recorder.error_count:
        return recorder, policy, decision, 2

    stage_id = str(args.stage or "")
    skill_id = str(args.skill or "")
    stages = ordered_stages(policy)
    legacy = legacy_stages(policy)
    registered = skills(policy)
    state = load_state()
    current_stage = str(state.get("current_stage") or "")
    authorized_stage = bool(args.authorized_stage or os.environ.get("SKILL_ROUTER_AUTHORIZE_STAGE") == "1")
    human_confirmed = bool(args.human_confirmed or os.environ.get("SKILL_ROUTER_HUMAN_CONFIRMED") == "1")

    if stage_id in legacy:
        decision.update({"router_decision": "deny", "failure_code": "LEGACY_STAGE_NAME"})
        recorder.add("SR-STAGE-004", "requested_stage_not_legacy", "fail", f"legacy stage requested: {stage_id}")
        return recorder, policy, decision, 1
    if stage_id not in stages:
        decision.update({"router_decision": "deny", "failure_code": "STAGE_NOT_ALLOWED"})
        recorder.add("SR-STAGE-001", "requested_stage_exists", "fail", f"unknown stage: {stage_id}")
        return recorder, policy, decision, 1
    recorder.add("SR-STAGE-001", "requested_stage_exists", "pass", f"stage exists: {stage_id}")

    if current_stage and stage_id != current_stage and not authorized_stage:
        decision.update({"router_decision": "block", "failure_code": "STAGE_NOT_ALLOWED"})
        recorder.add(
            "SR-STAGE-005",
            "current_stage_matches_requested_stage",
            "fail",
            f"current_stage={current_stage}; requested_stage={stage_id}; pass --authorized-stage only for explicit human authorization",
            "workflow_state.yaml",
        )
        return recorder, policy, decision, 1
    recorder.add(
        "SR-STAGE-005",
        "current_stage_matches_requested_stage",
        "pass",
        "requested stage matches current stage or is explicitly authorized",
        "workflow_state.yaml",
    )

    if skill_id not in registered:
        decision.update({"router_decision": "deny", "failure_code": "UNKNOWN_SKILL"})
        recorder.add("SR-SKILL-001", "skill_registered", "fail", f"unknown skill: {skill_id}")
        return recorder, policy, decision, 1
    recorder.add("SR-SKILL-001", "skill_registered", "pass", f"skill registered: {skill_id}")

    route = route_for_skill(policy, stage_id, skill_id)
    if not route:
        decision.update({"router_decision": "deny", "failure_code": "STAGE_NOT_ALLOWED"})
        recorder.add("SR-SKILL-005", "skill_allowed_for_stage", "fail", f"{skill_id} is not allowed in {stage_id}")
        return recorder, policy, decision, 1
    recorder.add("SR-SKILL-005", "skill_allowed_for_stage", "pass", f"{skill_id} is allowed in {stage_id}")

    permission = str(route.get("permission") or registered[skill_id].get("default_permission") or "")
    decision["permission_level"] = permission
    if permission not in permission_levels(policy):
        decision.update({"router_decision": "block", "failure_code": "VALIDATION_FAILED"})
        recorder.add("SR-PERM-003", "permission_level", "fail", f"permission is not defined: {permission}")
        return recorder, policy, decision, 2
    recorder.add("SR-PERM-003", "permission_level", "pass", f"permission is valid: {permission}")

    required_status, missing_required, missing_optional, _ = compute_required_input_status(policy, skill_id)
    decision["required_inputs_status"] = required_status
    if required_status == "missing_required":
        route_required = bool(route.get("required"))
        decision.update({"router_decision": "block" if route_required else "skip", "failure_code": "REQUIRED_INPUT_MISSING"})
        recorder.add("SR-IN-001", "required_inputs_exist", "fail", f"missing required inputs: {missing_required}")
        return recorder, policy, decision, 3
    if required_status == "missing_optional":
        recorder.add("SR-IN-003", "recommended_inputs_exist", "warning", f"missing recommended inputs: {missing_optional}")
    recorder.add("SR-IN-001", "required_inputs_exist", "pass", "required inputs exist")

    human_required = bool(route.get("require_human_final_gate")) or bool((((policy.get("required_inputs") or {}).get(skill_id)) or {}).get("require_human_final_gate"))
    decision["human_confirmation_required"] = human_required
    if permission == "post_final":
        human_required = True
        decision["human_confirmation_required"] = True
    if human_required and not human_confirmed:
        decision.update({"router_decision": "block", "failure_code": "HUMAN_CONFIRMATION_REQUIRED"})
        recorder.add("SR-IN-004", "human_final_gate", "fail", "human final gate is required but not satisfied")
        return recorder, policy, decision, 1
    recorder.add("SR-IN-004", "human_final_gate", "pass", "human gate is satisfied or not required")

    decision.update({"router_decision": "allow", "failure_code": None})
    return recorder, policy, decision, 0


def build_manifest(policy: Mapping[str, Any], stage_id: str, skill_id: str, call_id: str, timestamp: str, archive_dir: Path) -> Dict[str, Any]:
    registered = skills(policy)
    route = route_for_skill(policy, stage_id, skill_id) or {}
    skill_meta = registered.get(skill_id) or {}
    permission = str(route.get("permission") or skill_meta.get("default_permission") or "advisory")
    status, missing_required, missing_optional, file_records = compute_required_input_status(policy, skill_id)
    rule = ((policy.get("required_inputs") or {}).get(skill_id)) or {}
    prompt = stage_prompt_files(policy).get(stage_id, "")
    contracts = []
    for path_text in (skill_meta.get("contract_targets") or []):
        p = ROOT / str(path_text)
        contracts.append(
            {
                "path": str(path_text),
                "status": "exists" if p.exists() else "missing",
                "relevant_ids": [],
                "checksum_sha256": checksum(p),
            }
        )
    output_types = skill_meta.get("allowed_output_types") or []
    first_output_type = str(output_types[0]) if output_types else ""
    promo_target = "archive_only"
    promo_rule = ((((policy.get("promotion_rules") or {}).get("allowed_targets")) or {}).get(first_output_type)) or {}
    if promo_rule:
        target = promo_rule.get("target")
        promo_target = ", ".join(str(x) for x in target) if isinstance(target, list) else str(target)
    return {
        "manifest_version": "v3.2-p1",
        "call": {
            "call_id": call_id,
            "timestamp_utc": timestamp,
            "stage_id": stage_id,
            "skill_id": skill_id,
            "skill_category": str(skill_meta.get("category") or ""),
            "permission_level": permission,
            "router_decision": "allow" if status in {"exists", "missing_optional"} else "skip",
            "task_id": "",
            "operator": "Human or external skill call",
        },
        "policy_context": {
            "router_policy_file": "config/skill_router_policy.yaml",
            "router_policy_version": str(policy.get("version") or "v3.2-p1"),
            "stage_prompt_file": prompt,
            "workflow_state_file": "workflow_state.yaml",
            "authority_order_checked": True,
            "deny_by_default_checked": True,
        },
        "preflight": {
            "current_stage_matches_requested_stage": str(load_state().get("current_stage") or "") == stage_id,
            "skill_registered": skill_id in registered,
            "skill_allowed_for_stage": route_for_skill(policy, stage_id, skill_id) is not None,
            "permission_level_allowed": permission in permission_levels(policy),
            "required_inputs_status": status,
            "required_inputs": {
                "all_of": [str(x) for x in (rule.get("all_of") or [])],
                "any_of": [str(x) for x in (rule.get("any_of") or [])],
                "recommended": [str(x) for x in (rule.get("recommended") or [])],
                "missing": missing_required + missing_optional,
            },
            "required_human_gate": {
                "required": bool(route.get("require_human_final_gate")) or bool(rule.get("require_human_final_gate")) or permission == "post_final",
                "satisfied": False,
                "decision_id": "",
            },
        },
        "input_files": {
            "allowed_read_paths": [item["path"] for item in file_records],
            "files_read": file_records,
        },
        "contract_context": {
            "contracts_read": contracts,
            "frozen_artifacts_checked": skill_id == "nature-polishing",
            "frozen_artifact_violations": [],
        },
        "requested_output": {
            "output_type": first_output_type,
            "archive_path": rel(archive_dir / "raw_output.md"),
            "expected_promotion_target": promo_target,
            "must_bind_to_contracts": (promo_rule.get("requires_contract_binding") or []),
            "must_preserve_protected_atoms": ["numbers", "formulas", "labels", "references", "citations", "model_names", "result_meanings"] if promo_rule.get("protected_atoms_must_match") else [],
        },
        "risk_controls": {
            "no_direct_contract_write": True,
            "no_direct_final_paper_write": True,
            "no_workflow_state_change": True,
            "no_script_change": True,
            "no_fabricated_data": True,
            "no_fabricated_citation": True,
            "no_prior_text_copy": True,
        },
        "notes": "Initialized by scripts/check_skill_router.py --init-archive. Raw skill execution is intentionally out of scope.",
    }


def fill_promotion_notes(template_text: str, stage_id: str, skill_id: str, permission: str, output_type: str, target: str, human_required: bool, call_id: str) -> str:
    text = template_text
    replacements = {
        "SKILL-<stage_id>-<skill_id>-<YYYYMMDDTHHMMSSZ>": call_id,
        "<stage_id>": stage_id,
        "<skill_id>": skill_id,
        "advisory | contract_suggest | draft_assist | post_final": permission,
        "<registered_output_type>": output_type or "archive_only",
        "<target path or archive_only>": target or "archive_only",
        "human_confirmation_required: false": f"human_confirmation_required: {str(human_required).lower()}",
        "promotion_decision: archive_only | promote | promote_with_edits | reject | retry_required": "promotion_decision: archive_only",
        "archive_complete: false": "archive_complete: true",
        "promotion_ready: false": "promotion_ready: false",
        "next_required_action: <one concrete next action>": "next_required_action: fill raw_output.md, then update promotion notes before validation",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def init_archive(args: argparse.Namespace) -> Tuple[CheckRecorder, Dict[str, Any], Dict[str, Any], int, Optional[Path]]:
    # Archive creation is itself a guarded action. It must not become a side door
    # around current-stage checks, required inputs, or human final gates.
    recorder, policy, decision, preflight_exit_code = preflight(args)
    if preflight_exit_code != 0:
        recorder.add(
            "SR-ARCH-000",
            "archive_preflight_required",
            "fail",
            f"archive initialization blocked by preflight: {decision.get('failure_code')}",
        )
        return recorder, policy, decision, preflight_exit_code, None

    stage_id = str(args.stage or "")
    skill_id = str(args.skill or "")
    timestamp = utc_now()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base_call_id = f"SKILL-{stage_id}-{skill_id}-{stamp}"
    call_id = base_call_id
    root = archive_root(policy)
    archive_dir = root / stage_id / skill_id / call_id
    counter = 2
    while archive_dir.exists():
        call_id = f"{base_call_id}-{counter}"
        archive_dir = root / stage_id / skill_id / call_id
        counter += 1
    archive_dir = ensure_archive_dir_inside_policy_root(policy, archive_dir)
    archive_dir.mkdir(parents=True, exist_ok=False)

    meta = skills(policy).get(skill_id) or {}
    route = route_for_skill(policy, stage_id, skill_id) or {}
    permission = str(route.get("permission") or meta.get("default_permission") or "advisory")
    category = str(meta.get("category") or "")
    template_dir = root / "templates" / "by_category" / category
    if (template_dir / "input_manifest.yaml").exists():
        recorder.add("SR-ARCH-002", "archive_template", "pass", f"using category template: {rel(template_dir)}")
    else:
        template_dir = root / "templates"
        recorder.add("SR-ARCH-002", "archive_template", "warning", "category template missing; using generic template")

    manifest = build_manifest(policy, stage_id, skill_id, call_id, timestamp, archive_dir)
    manifest_preflight = manifest.get("preflight") or {}
    manifest_human_gate = manifest_preflight.get("required_human_gate") or {}
    manifest_human_gate["satisfied"] = bool(args.human_confirmed or os.environ.get("SKILL_ROUTER_HUMAN_CONFIRMED") == "1")
    manifest_preflight["required_human_gate"] = manifest_human_gate
    manifest_preflight["current_stage_matches_requested_stage"] = True
    manifest["preflight"] = manifest_preflight
    (archive_dir / "input_manifest.yaml").write_text(safe_dump_yaml(manifest), encoding="utf-8")

    output_type = str((manifest.get("requested_output") or {}).get("output_type") or "")
    target = str((manifest.get("requested_output") or {}).get("expected_promotion_target") or "archive_only")
    human_required = bool(((manifest.get("preflight") or {}).get("required_human_gate") or {}).get("required"))
    promo_template = (template_dir / "promotion_notes.md") if (template_dir / "promotion_notes.md").exists() else (root / "templates" / "generic_promotion_notes.md")
    promo_text = fill_promotion_notes(promo_template.read_text(encoding="utf-8"), stage_id, skill_id, permission, output_type, target, human_required, call_id)
    (archive_dir / "promotion_notes.md").write_text(promo_text, encoding="utf-8")

    raw_header = "\n".join(
        [
            "# Raw skill output",
            "",
            "WARNING: This file is an archive-only capture area. Do not copy content from here into workflow artifacts until promotion validation passes.",
            "",
            RAW_OUTPUT_EMPTY_SENTINEL,
            "To make this eligible for promotion, replace the sentinel with RAW_OUTPUT_STATUS: FILLED_BY_SKILL_OR_HUMAN and add the actual skill output below.",
            "",
            f"call_id: {call_id}",
            f"stage_id: {stage_id}",
            f"skill_id: {skill_id}",
            "",
        ]
    )
    (archive_dir / "raw_output.md").write_text(raw_header, encoding="utf-8")
    (root / ".gitkeep").touch(exist_ok=True)

    status = str(((manifest.get("preflight") or {}).get("required_inputs_status")) or "exists")
    decision.update(
        {
            "router_decision": "archive_only",
            "permission_level": permission,
            "required_inputs_status": status,
            "archive_path": rel(archive_dir),
            "call_id": call_id,
            "human_confirmation_required": human_required,
        }
    )
    recorder.add("SR-ARCH-001", "archive_path", "pass", f"created archive dir {rel(archive_dir)}", rel(archive_dir))
    recorder.add("SR-ARCH-003", "raw_output_exists", "pass", "raw_output.md initialized", rel(archive_dir / "raw_output.md"))
    recorder.add("SR-ARCH-004", "promotion_notes_exists", "pass", "promotion_notes.md initialized", rel(archive_dir / "promotion_notes.md"))
    return recorder, policy, decision, 0, archive_dir


def validate_promotion(args: argparse.Namespace) -> Tuple[CheckRecorder, Dict[str, Any], Dict[str, Any], int]:
    recorder, policy = validate_policy()
    decision: Dict[str, Any] = {
        "stage_id": None,
        "skill_id": None,
        "router_decision": "promotion_blocked",
        "permission_level": None,
        "required_inputs_status": None,
        "failure_code": None,
        "human_confirmation_required": False,
    }
    if recorder.error_count:
        return recorder, policy, decision, 2

    archive_dir = Path(args.validate_promotion)
    if not archive_dir.is_absolute():
        archive_dir = ROOT / archive_dir
    try:
        archive_dir = ensure_archive_dir_inside_policy_root(policy, archive_dir)
        recorder.add("SR-ARCH-001", "archive_path", "pass", "archive path is under allowed root", rel(archive_dir))
    except RouterError as exc:
        recorder.add("SR-ARCH-001", "archive_path", "fail", str(exc), str(archive_dir))
        decision["failure_code"] = "OUTPUT_PATH_VIOLATION"
        return recorder, policy, decision, 4

    manifest_path = archive_dir / "input_manifest.yaml"
    raw_path = archive_dir / "raw_output.md"
    notes_path = archive_dir / "promotion_notes.md"

    manifest: Dict[str, Any] = {}
    if not manifest_path.exists():
        recorder.add("SR-ARCH-002", "input_manifest_exists", "fail", "input_manifest.yaml is missing", rel(manifest_path))
    else:
        try:
            manifest = safe_load_yaml(manifest_path)
            recorder.add("SR-ARCH-002", "input_manifest_exists", "pass", "input_manifest.yaml exists and parses", rel(manifest_path))
        except RouterError as exc:
            recorder.add("SR-ARCH-002", "input_manifest_exists", "fail", str(exc), rel(manifest_path))

    raw_text = raw_path.read_text(encoding="utf-8", errors="ignore") if raw_path.exists() else ""
    if not raw_path.exists():
        recorder.add("SR-ARCH-003", "raw_output_exists", "fail", "raw_output.md is missing", rel(raw_path))
    else:
        has_real_raw_output, raw_message = raw_output_has_real_content(raw_text)
        recorder.add(
            "SR-ARCH-003",
            "raw_output_contains_real_content",
            "pass" if has_real_raw_output else "fail",
            raw_message,
            rel(raw_path),
        )
        if not has_real_raw_output:
            decision["failure_code"] = decision.get("failure_code") or "VALIDATION_FAILED"

    notes_text = notes_path.read_text(encoding="utf-8", errors="ignore") if notes_path.exists() else ""
    notes = markdown_key_values(notes_text)
    if not notes_path.exists() or not notes_text.strip():
        recorder.add("SR-ARCH-004", "promotion_notes_exists", "fail", "promotion_notes.md is missing or empty", rel(notes_path))
    elif "promotion_decision" not in notes and "promotion_ready" not in notes:
        recorder.add("SR-ARCH-004", "promotion_notes_structure", "fail", "promotion_notes.md does not contain required structural keys", rel(notes_path))
    else:
        recorder.add("SR-ARCH-004", "promotion_notes_structure", "pass", "promotion_notes.md has required structural keys", rel(notes_path))

    call = manifest.get("call") or {}
    requested = manifest.get("requested_output") or {}
    stage_id = normalize_placeholder(call.get("stage_id"))
    skill_id = normalize_placeholder(call.get("skill_id"))
    permission = normalize_placeholder(call.get("permission_level"))
    output_type = normalize_placeholder(requested.get("output_type")) or normalize_placeholder(notes.get("output_type"))
    decision.update({"stage_id": stage_id, "skill_id": skill_id, "permission_level": permission})

    if skill_id not in skills(policy):
        recorder.add("SR-SKILL-001", "skill_registered", "fail", f"unknown skill in manifest: {skill_id}")
        decision["failure_code"] = "UNKNOWN_SKILL"
    else:
        recorder.add("SR-SKILL-001", "skill_registered", "pass", f"skill is registered: {skill_id}")

    allowed_for_skill = set(str(item) for item in ((skills(policy).get(skill_id) or {}).get("allowed_output_types") or []))
    if not output_type or output_type not in allowed_for_skill:
        recorder.add("SR-PROMO-001", "output_type_allowed_for_skill", "fail", f"output_type is not allowed for skill: {output_type or '<blank>'}")
        decision["failure_code"] = "UNKNOWN_SKILL_OUTPUT"
    else:
        recorder.add("SR-PROMO-001", "output_type_allowed_for_skill", "pass", f"output_type is allowed: {output_type}")

    promo_rules = (((policy.get("promotion_rules") or {}).get("allowed_targets")) or {})
    promo_rule = promo_rules.get(output_type) or {}
    promotion_target = normalize_placeholder(notes.get("promotion_target")) or normalize_placeholder(requested.get("expected_promotion_target"))
    promotion_decision = normalize_placeholder(notes.get("promotion_decision")) or "archive_only"

    if not promo_rule:
        if output_type:
            recorder.add("SR-PROMO-006", "unknown_output_type_archive_only", "fail", f"no promotion rule for output_type: {output_type}")
            decision["failure_code"] = "UNKNOWN_SKILL_OUTPUT"
    else:
        allowed_target = promo_rule.get("target")
        allowed_targets = [str(x) for x in allowed_target] if isinstance(allowed_target, list) else [str(allowed_target)]
        if promotion_decision == "archive_only":
            recorder.add("SR-PROMO-002", "promotion_target_allowed", "fail", "promotion decision is archive_only; not eligible for promotion yet")
            decision["failure_code"] = decision.get("failure_code") or "VALIDATION_FAILED"
        elif promotion_target in allowed_targets:
            recorder.add("SR-PROMO-002", "promotion_target_allowed", "pass", f"promotion target is allowed: {promotion_target}")
        else:
            recorder.add("SR-PROMO-002", "promotion_target_allowed", "fail", f"promotion target {promotion_target} not in allowed targets {allowed_targets}")
            decision["failure_code"] = decision.get("failure_code") or "VALIDATION_FAILED"

        bindings = [str(x) for x in (promo_rule.get("requires_contract_binding") or [])]
        if bindings:
            bindings_valid, binding_satisfied, binding_problems = validate_contract_bindings(bindings, notes_text, output_type)
            recorder.add(
                "SR-PROMO-003",
                "required_contract_bindings",
                "pass" if bindings_valid else "fail",
                "required contract bindings validated against contracts: " + "; ".join(binding_satisfied)
                if bindings_valid
                else "missing or invalid contract bindings: " + "; ".join(binding_problems),
                rel(notes_path),
            )
            if not bindings_valid:
                problem_text = " ".join(binding_problems).lower()
                decision["failure_code"] = decision.get("failure_code") or (
                    "CONTRACT_INVALID" if "failed to read" in problem_text or "column" in problem_text else "CONTRACT_MISSING"
                )

        validation_status = normalize_placeholder(notes.get("validation_status")) or "not_run"
        if promo_rule.get("requires_validation") and validation_status not in {"passed", "waived"}:
            recorder.add("SR-PROMO-004", "validation_requirement", "fail", f"validation_status={validation_status}; expected passed or waived")
            decision["failure_code"] = decision.get("failure_code") or "VALIDATION_FAILED"
        else:
            recorder.add("SR-PROMO-004", "validation_requirement", "pass", f"validation_status={validation_status}")

        human_required = bool(promo_rule.get("requires_human_confirmation")) or bool(promo_rule.get("requires_human_final_gate"))
        decision["human_confirmation_required"] = human_required
        human_decision = normalize_placeholder(notes.get("human_decision"))
        human_decision_id = normalize_placeholder(notes.get("human_decision_id"))
        if human_required and (not human_decision_id or human_decision in {"", "not_required"}):
            recorder.add("SR-PROMO-005", "human_gate_requirement", "fail", "human confirmation is required but not recorded")
            decision["failure_code"] = decision.get("failure_code") or "HUMAN_CONFIRMATION_REQUIRED"
        else:
            recorder.add("SR-PROMO-005", "human_gate_requirement", "pass", "human confirmation recorded or not required")

        if promo_rule.get("protected_atoms_must_match"):
            protected_fields = [
                "numbers_preserved",
                "formulas_preserved",
                "labels_preserved",
                "references_preserved",
                "citations_preserved",
                "model_names_preserved",
                "result_meanings_preserved",
            ]
            bad = [field for field in protected_fields if normalize_placeholder(notes.get(field)).lower() == "false"]
            recorder.add(
                "SR-PROMO-007",
                "protected_atoms_preserved",
                "fail" if bad else "pass",
                f"protected atom fields failed: {bad}" if bad else "protected atoms are preserved or marked not_applicable",
                rel(notes_path),
            )
            if bad:
                decision["failure_code"] = decision.get("failure_code") or "PROTECTED_ATOM_CHANGED"

        if promo_rule.get("requires_copy_risk_check"):
            has_copy_risk = "copy_risk_status" in notes_text or "copy-risk" in notes_text.lower() or "copy risk" in notes_text.lower()
            recorder.add(
                "SR-PROMO-008",
                "copy_risk_status_recorded",
                "pass" if has_copy_risk else "fail",
                "copy-risk status is recorded" if has_copy_risk else "prior_card output requires copy-risk status",
                rel(notes_path),
            )
            if not has_copy_risk:
                decision["failure_code"] = decision.get("failure_code") or "PRIOR_COPY_RISK"

        if promo_rule.get("must_not_modify_final_paper"):
            modifies_final = "09_paper/final_paper.md" in promotion_target or "paper_modification" in raw_text
            recorder.add(
                "SR-PERM-006",
                "post_final_does_not_modify_final_paper",
                "fail" if modifies_final else "pass",
                "post-final output attempts to modify final paper" if modifies_final else "post-final output target does not modify final paper",
            )
            if modifies_final:
                decision["failure_code"] = decision.get("failure_code") or "VALIDATION_FAILED"

    if recorder.error_count:
        decision["router_decision"] = "promotion_blocked"
        return recorder, policy, decision, 4
    decision.update({"router_decision": "promotion_validated", "failure_code": None})
    return recorder, policy, decision, 0


def log_call(args: argparse.Namespace) -> Tuple[CheckRecorder, Dict[str, Any], Dict[str, Any], int]:
    recorder, policy = validate_policy()
    decision: Dict[str, Any] = {
        "stage_id": None,
        "skill_id": None,
        "router_decision": "archive_only",
        "permission_level": None,
        "required_inputs_status": None,
        "failure_code": None,
        "human_confirmation_required": False,
    }
    if recorder.error_count:
        return recorder, policy, decision, 2

    archive_dir = Path(args.log_call)
    if not archive_dir.is_absolute():
        archive_dir = ROOT / archive_dir
    try:
        archive_dir = ensure_archive_dir_inside_policy_root(policy, archive_dir)
        recorder.add("SR-ARCH-001", "archive_path", "pass", "archive path is under allowed root", rel(archive_dir))
    except RouterError as exc:
        recorder.add("SR-ARCH-001", "archive_path", "fail", str(exc), str(archive_dir))
        decision["failure_code"] = "OUTPUT_PATH_VIOLATION"
        return recorder, policy, decision, 4

    manifest_path = archive_dir / "input_manifest.yaml"
    notes_path = archive_dir / "promotion_notes.md"
    if not manifest_path.exists():
        recorder.add("SR-ARCH-002", "input_manifest_exists", "fail", "input_manifest.yaml missing", rel(manifest_path))
        return recorder, policy, decision, 4
    manifest = safe_load_yaml(manifest_path)
    notes_text = notes_path.read_text(encoding="utf-8", errors="ignore") if notes_path.exists() else ""
    notes = markdown_key_values(notes_text)

    call = manifest.get("call") or {}
    preflight_data = manifest.get("preflight") or {}
    requested = manifest.get("requested_output") or {}
    call_id = normalize_placeholder(call.get("call_id")) or archive_dir.name
    stage_id = normalize_placeholder(call.get("stage_id"))
    skill_id = normalize_placeholder(call.get("skill_id"))
    permission = normalize_placeholder(call.get("permission_level"))
    router_decision = normalize_placeholder(call.get("router_decision")) or normalize_placeholder(notes.get("promotion_decision")) or "archive_only"
    if router_decision == "promote":
        router_decision = "promotion_validated"
    if router_decision not in ALLOWED_ROUTER_DECISIONS:
        router_decision = "archive_only"
    input_status = normalize_placeholder(preflight_data.get("required_inputs_status")) or "exists"
    if input_status not in ALLOWED_INPUT_STATUS:
        input_status = "exists"
    output_type = normalize_placeholder(requested.get("output_type")) or normalize_placeholder(notes.get("output_type"))
    promotion_target = normalize_placeholder(notes.get("promotion_target")) or normalize_placeholder(requested.get("expected_promotion_target")) or "archive_only"
    validation_status = normalize_placeholder(notes.get("validation_status")) or "not_run"
    if validation_status == "waived":
        validation_status = "warning"
    if validation_status not in ALLOWED_VALIDATION_STATUS:
        validation_status = "not_run"
    failure_code = normalize_placeholder(notes.get("failure_code"))
    if failure_code in {"NONE", "none", "null"} or "|" in failure_code:
        failure_code = ""
    if failure_code and failure_code not in failure_codes(policy):
        recorder.add("SR-LOG-002", "failure_code_registered", "fail", f"failure_code is not defined: {failure_code}", rel(notes_path))
        return recorder, policy, decision, 4

    human_required = bool(((preflight_data.get("required_human_gate") or {}).get("required")))
    if normalize_placeholder(notes.get("human_confirmation_required")).lower() == "true":
        human_required = True

    log_path = usage_log_path(policy)
    expected_header = [str(item) for item in (((policy.get("usage_log") or {}).get("columns")) or USAGE_LOG_HEADER)]
    actual_header = read_csv_header(log_path)
    if not actual_header:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerow(expected_header)
        actual_header = expected_header
    if actual_header != expected_header:
        recorder.add("SR-LOG-001", "usage_log_header", "fail", "usage log header mismatch; refusing to append", rel(log_path))
        return recorder, policy, decision, 4

    existing_call_ids = set()
    with log_path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            existing_call_ids.add(str(row.get("call_id") or ""))
    if call_id in existing_call_ids:
        recorder.add("SR-LOG-003", "usage_log_deduplicate", "warning", f"call_id already logged; no duplicate row appended: {call_id}", rel(log_path))
    else:
        row = {
            "call_id": call_id,
            "timestamp": normalize_placeholder(call.get("timestamp_utc")) or utc_now(),
            "stage_id": stage_id,
            "skill_id": skill_id,
            "permission_level": permission,
            "router_decision": router_decision,
            "required_inputs_status": input_status,
            "archive_path": rel(archive_dir),
            "output_type": output_type,
            "promotion_target": promotion_target,
            "validation_status": validation_status,
            "failure_code": failure_code,
            "human_confirmation_required": str(human_required).lower(),
            "notes": failure_recovery(policy, failure_code) if failure_code else "logged by check_skill_router.py",
        }
        with log_path.open("a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=expected_header)
            writer.writerow(row)
        recorder.add("SR-LOG-004", "usage_log_append", "pass", f"appended usage log row for {call_id}", rel(log_path))

    decision.update(
        {
            "stage_id": stage_id,
            "skill_id": skill_id,
            "router_decision": router_decision,
            "permission_level": permission,
            "required_inputs_status": input_status,
            "failure_code": failure_code or None,
            "human_confirmation_required": human_required,
        }
    )
    return recorder, policy, decision, 0


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="P1 Skill Router runtime checker")
    parser.add_argument("--validate-policy", action="store_true", help="validate config/skill_router_policy.yaml and write router reports")
    parser.add_argument("--stage", help="workflow stage id for preflight or archive initialization")
    parser.add_argument("--skill", help="skill id for preflight or archive initialization")
    parser.add_argument("--preflight", action="store_true", help="check whether a skill may be called")
    parser.add_argument("--init-archive", action="store_true", help="create an archive scaffold for a skill call")
    parser.add_argument("--validate-promotion", help="validate an archived skill output directory for promotion")
    parser.add_argument("--log-call", help="append one skill usage log row for an archive directory")
    parser.add_argument("--authorized-stage", action="store_true", help="explicitly authorize a non-current stage preflight")
    parser.add_argument("--human-confirmed", action="store_true", help="mark required human confirmation as satisfied for preflight")
    return parser.parse_args(argv)


def require_stage_skill(args: argparse.Namespace) -> None:
    if not args.stage or not args.skill:
        raise RouterError("--stage and --skill are required for this command", 2)


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = parse_args(argv)
    command_count = sum(
        1
        for flag in [args.validate_policy, args.preflight, args.init_archive, bool(args.validate_promotion), bool(args.log_call)]
        if flag
    )
    if command_count != 1:
        raise SystemExit("[FAIL] choose exactly one command: --validate-policy, --preflight, --init-archive, --validate-promotion, or --log-call")

    try:
        if args.validate_policy:
            recorder, policy = validate_policy()
            write_reports(recorder, policy)
            print(f"[{recorder.status.upper()}] wrote {rel(REPORT_JSON)} and {rel(REPORT_MD)}")
            raise SystemExit(0 if not recorder.error_count else 2)

        if args.preflight:
            require_stage_skill(args)
            recorder, policy, decision, exit_code = preflight(args)
            action = "skill call allowed" if exit_code == 0 else f"skill call blocked: {decision.get('failure_code')}"
            write_reports(recorder, policy, decision=decision, recommended_action=action)
            print(f"[{recorder.status.upper()}] {action}; wrote {rel(REPORT_JSON)}")
            raise SystemExit(exit_code)

        if args.init_archive:
            require_stage_skill(args)
            recorder, policy, decision, exit_code, archive_dir = init_archive(args)
            action = f"archive initialized at {rel(archive_dir)}" if archive_dir else f"archive initialization failed: {decision.get('failure_code')}"
            write_reports(recorder, policy, decision=decision, recommended_action=action)
            print(f"[{recorder.status.upper()}] {action}; wrote {rel(REPORT_JSON)}")
            raise SystemExit(exit_code)

        if args.validate_promotion:
            recorder, policy, decision, exit_code = validate_promotion(args)
            action = "promotion validated" if exit_code == 0 else f"promotion blocked: {decision.get('failure_code')}"
            write_reports(recorder, policy, decision=decision, recommended_action=action)
            print(f"[{recorder.status.upper()}] {action}; wrote {rel(REPORT_JSON)}")
            raise SystemExit(exit_code)

        if args.log_call:
            recorder, policy, decision, exit_code = log_call(args)
            action = "usage log updated" if exit_code == 0 else f"usage log update failed: {decision.get('failure_code')}"
            write_reports(recorder, policy, decision=decision, recommended_action=action)
            print(f"[{recorder.status.upper()}] {action}; wrote {rel(REPORT_JSON)}")
            raise SystemExit(exit_code)
    except RouterError as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        raise SystemExit(exc.exit_code)


if __name__ == "__main__":
    main()
