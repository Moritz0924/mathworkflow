from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple

from workflow_utils import (
    ROOT,
    assert_stage_allowed,
    complete_stage,
    read_csv_dict,
    rel,
    write_csv_dicts,
)

CONTRACT_DIR = ROOT / "14_contracts"
FIGURE_CONTRACT = CONTRACT_DIR / "figure_contract.csv"
RESULT_CONTRACT = CONTRACT_DIR / "result_contract.csv"
OLD_REGISTRY = ROOT / "08_figures" / "figure_registry.csv"
OUT_PATH = ROOT / "08_figures" / "figure_quality_check.csv"
REVIEW_PATH = ROOT / "11_review" / "figure_reviewer_comments.md"

FIGURE_FIELDS = [
    "figure_id",
    "question_id",
    "core_claim",
    "evidence_source",
    "result_id",
    "panel_plan",
    "chart_type",
    "backend",
    "script_path",
    "output_svg",
    "output_png",
    "output_pdf",
    "dpi",
    "used_in_section",
    "latex_label",
    "caption_source",
    "quality_score",
    "review_risk",
    "status",
    "owner",
    "last_checked",
]

CHECK_FIELDS = [
    "figure_id",
    "question_id",
    "used_in_section",
    "latex_label",
    "chart_type",
    "backend",
    "result_id",
    "has_core_claim",
    "has_evidence",
    "result_exists",
    "has_output_file",
    "svg_exists",
    "png_exists",
    "pdf_exists",
    "script_exists",
    "dpi_ok",
    "label_ok",
    "computed_quality_score",
    "contract_quality_score",
    "gate_result",
    "severity",
    "issues",
    "recommendation",
]

ACTIVE_STATUSES = {"active", "approved", "ready", "used", "frozen", "completed", "confirmed", "已确认", "通过"}
INACTIVE_STATUSES = {"", "draft", "pending", "todo", "archived", "deprecated", "rejected", "disabled", "草稿", "待定"}


def clean(value: Any) -> str:
    return str(value or "").strip()


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(clean(value))
    except Exception:
        return default


def as_int(value: Any, default: int = 0) -> int:
    raw = clean(value)
    if not raw:
        return default
    m = re.search(r"\d+", raw)
    if not m:
        return default
    try:
        return int(m.group(0))
    except Exception:
        return default


def exists_path(value: Any) -> bool:
    raw = clean(value)
    if not raw:
        return False
    p = Path(raw)
    if not p.is_absolute():
        p = ROOT / p
    return p.exists()


def normalize_path(value: Any) -> str:
    raw = clean(value)
    if not raw:
        return ""
    p = Path(raw)
    if p.is_absolute():
        try:
            return str(p.relative_to(ROOT))
        except ValueError:
            return str(p)
    return raw


def is_active(row: Mapping[str, Any]) -> bool:
    value = clean(row.get("status")).lower()
    if value in ACTIVE_STATUSES:
        return True
    if value in INACTIVE_STATUSES:
        return bool(clean(row.get("used_in_section")))
    return bool(value or clean(row.get("used_in_section")))


def result_ids() -> set[str]:
    return {clean(row.get("result_id")) for row in read_csv_dict(RESULT_CONTRACT) if clean(row.get("result_id"))}


def read_figures() -> Tuple[List[Dict[str, str]], str]:
    rows = read_csv_dict(FIGURE_CONTRACT)
    if rows:
        return rows, "figure_contract"

    # v3.0 compatibility fallback. This does not mutate figure_contract unless --sync-contract is used.
    old = read_csv_dict(OLD_REGISTRY)
    converted: List[Dict[str, str]] = []
    for row in old:
        converted.append({
            "figure_id": clean(row.get("figure_id")),
            "question_id": clean(row.get("question_id")),
            "core_claim": clean(row.get("main_message") or row.get("title")),
            "evidence_source": clean(row.get("data_source")),
            "result_id": clean(row.get("result_id")),
            "panel_plan": "",
            "chart_type": clean(row.get("chart_type")),
            "backend": clean(row.get("backend")),
            "script_path": clean(row.get("script_path")),
            "output_svg": clean(row.get("output_svg")),
            "output_png": clean(row.get("path") or row.get("output_png")),
            "output_pdf": clean(row.get("output_pdf")),
            "dpi": clean(row.get("dpi")),
            "used_in_section": clean(row.get("section")),
            "latex_label": clean(row.get("latex_label")),
            "caption_source": clean(row.get("caption_source")),
            "quality_score": clean(row.get("quality_score")),
            "review_risk": "",
            "status": "used" if clean(row.get("used_in_paper")) in {"是", "yes", "true", "1"} else clean(row.get("status")),
            "owner": clean(row.get("owner")),
            "last_checked": "",
        })
    return converted, "figure_registry_fallback"


def sync_contract(rows: Sequence[Mapping[str, Any]]) -> None:
    existing = read_csv_dict(FIGURE_CONTRACT) if FIGURE_CONTRACT.exists() else []
    by_id = {clean(row.get("figure_id")): dict(row) for row in existing if clean(row.get("figure_id"))}
    for row in rows:
        fid = clean(row.get("figure_id"))
        if not fid:
            continue
        merged = {field: "" for field in FIGURE_FIELDS}
        merged.update(by_id.get(fid, {}))
        for field in FIGURE_FIELDS:
            value = clean(row.get(field))
            if value and not clean(merged.get(field)):
                merged[field] = value
        by_id[fid] = merged
    write_csv_dicts(FIGURE_CONTRACT, list(by_id.values()), FIGURE_FIELDS)


def grade_row(row: Mapping[str, Any], known_results: set[str]) -> Dict[str, str]:
    issues: List[str] = []
    recommendations: List[str] = []
    score = 5.0

    figure_id = clean(row.get("figure_id"))
    if not figure_id:
        issues.append("缺少 figure_id")
        score -= 1.0

    has_core_claim = bool(clean(row.get("core_claim")))
    if not has_core_claim:
        issues.append("缺少 core_claim")
        recommendations.append("补充该图支撑的唯一核心论断")
        score -= 0.8

    result_id = clean(row.get("result_id"))
    has_evidence = bool(result_id or clean(row.get("evidence_source")))
    if not has_evidence:
        issues.append("缺少 result_id 或 evidence_source")
        recommendations.append("绑定 result_contract 或说明证据来源")
        score -= 1.0

    result_exists = True
    if result_id:
        result_exists = result_id in known_results
        if not result_exists:
            issues.append(f"result_id 不存在：{result_id}")
            score -= 1.2

    svg_exists = exists_path(row.get("output_svg"))
    png_exists = exists_path(row.get("output_png"))
    pdf_exists = exists_path(row.get("output_pdf"))
    has_output_file = svg_exists or png_exists or pdf_exists
    if not has_output_file:
        issues.append("缺少实际输出文件 output_svg/output_png/output_pdf")
        recommendations.append("生成可复现图表文件并登记路径")
        score -= 1.2

    script_path = clean(row.get("script_path"))
    script_exists = (not script_path) or exists_path(script_path)
    if script_path and not script_exists:
        issues.append(f"script_path 不存在：{script_path}")
        score -= 0.5
    elif not script_path:
        recommendations.append("建议登记图表生成脚本，方便复现")
        score -= 0.2

    dpi = as_int(row.get("dpi"), 0)
    dpi_ok = True
    if png_exists or pdf_exists:
        dpi_ok = dpi >= 300
        if not dpi_ok:
            issues.append(f"dpi 低于 300：{dpi or '未登记'}")
            score -= 0.4

    used = clean(row.get("used_in_section"))
    latex_label = clean(row.get("latex_label"))
    label_ok = True
    if used and not latex_label:
        label_ok = False
        issues.append("正文使用但缺少 latex_label")
        recommendations.append("补充 latex_label 并确保正文使用 \\ref")
        score -= 0.5

    if not clean(row.get("chart_type")):
        issues.append("缺少 chart_type")
        score -= 0.3
    if not clean(row.get("backend")):
        recommendations.append("建议登记 backend，如 matplotlib/R/graphviz")
        score -= 0.1

    score = max(0.0, min(5.0, round(score, 2)))
    contract_score = clean(row.get("quality_score"))
    active = is_active(row)

    hard_fail = active and any(
        phrase in "；".join(issues)
        for phrase in ["缺少 result_id", "result_id 不存在", "缺少实际输出文件", "缺少 core_claim", "正文使用但缺少 latex_label"]
    )
    gate_result = "fail" if hard_fail or score < 4.2 and active else "pass"
    severity = "fail" if gate_result == "fail" else ("warn" if issues or recommendations else "pass")

    return {
        "figure_id": figure_id,
        "question_id": clean(row.get("question_id")),
        "used_in_section": used,
        "latex_label": latex_label,
        "chart_type": clean(row.get("chart_type")),
        "backend": clean(row.get("backend")),
        "result_id": result_id,
        "has_core_claim": "是" if has_core_claim else "否",
        "has_evidence": "是" if has_evidence else "否",
        "result_exists": "是" if result_exists else "否",
        "has_output_file": "是" if has_output_file else "否",
        "svg_exists": "是" if svg_exists else "否",
        "png_exists": "是" if png_exists else "否",
        "pdf_exists": "是" if pdf_exists else "否",
        "script_exists": "是" if script_exists else "否",
        "dpi_ok": "是" if dpi_ok else "否",
        "label_ok": "是" if label_ok else "否",
        "computed_quality_score": str(score),
        "contract_quality_score": contract_score,
        "gate_result": gate_result,
        "severity": severity,
        "issues": "；".join(issues),
        "recommendation": "；".join(recommendations),
    }


def update_contract_scores(rows: Sequence[Mapping[str, Any]], checks: Sequence[Mapping[str, str]]) -> None:
    if not FIGURE_CONTRACT.exists():
        return
    check_by_id = {clean(row.get("figure_id")): row for row in checks if clean(row.get("figure_id"))}
    out: List[Dict[str, str]] = []
    for raw in rows:
        row = {field: clean(raw.get(field)) for field in FIGURE_FIELDS}
        check = check_by_id.get(clean(row.get("figure_id")))
        if check:
            row["quality_score"] = clean(check.get("computed_quality_score"))
            risk = clean(check.get("issues")) or clean(check.get("recommendation"))
            row["review_risk"] = risk
            row["last_checked"] = now()
            if clean(check.get("gate_result")) == "fail" and is_active(row):
                row["status"] = "blocked"
            elif clean(check.get("gate_result")) == "pass" and is_active(row):
                row["status"] = row["status"] or "ready"
        out.append(row)
    write_csv_dicts(FIGURE_CONTRACT, out, FIGURE_FIELDS)


def write_review(checks: Sequence[Mapping[str, str]], source_name: str) -> None:
    fails = [r for r in checks if clean(r.get("gate_result")) == "fail"]
    warns = [r for r in checks if clean(r.get("severity")) == "warn"]
    lines = [
        "# Figure reviewer comments",
        "",
        f"- generated_at: {now()}",
        f"- source: {source_name}",
        f"- checked_figures: {len(checks)}",
        f"- failed_figures: {len(fails)}",
        f"- warning_figures: {len(warns)}",
        "",
    ]
    if fails:
        lines.append("## Failures")
        for row in fails:
            lines.append(f"- **{clean(row.get('figure_id')) or '<empty>'}**: {clean(row.get('issues'))}")
        lines.append("")
    if warns:
        lines.append("## Warnings")
        for row in warns:
            lines.append(f"- **{clean(row.get('figure_id')) or '<empty>'}**: {clean(row.get('issues')) or clean(row.get('recommendation'))}")
        lines.append("")
    if not fails and not warns:
        lines.append("No figure quality issues detected by MVP checks.")
    REVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check figure quality against v3.2-MVP figure_contract.csv.")
    parser.add_argument("--sync-contract", action="store_true", help="When only v3.0 figure_registry exists, create/update figure_contract.csv.")
    parser.add_argument("--allow-fail", action="store_true", help="Write reports but exit 0 even when active figures fail.")
    parser.add_argument("--dev-debug", action="store_true")
    args = parser.parse_args()

    assert_stage_allowed("figures", args.dev_debug)
    rows, source_name = read_figures()

    if args.sync_contract and rows:
        sync_contract(rows)
        rows, source_name = read_figures()

    known_results = result_ids()
    checks = [grade_row(row, known_results) for row in rows]
    if not checks:
        checks = [{
            "figure_id": "",
            "question_id": "",
            "used_in_section": "",
            "latex_label": "",
            "chart_type": "",
            "backend": "",
            "result_id": "",
            "has_core_claim": "否",
            "has_evidence": "否",
            "result_exists": "否",
            "has_output_file": "否",
            "svg_exists": "否",
            "png_exists": "否",
            "pdf_exists": "否",
            "script_exists": "否",
            "dpi_ok": "否",
            "label_ok": "否",
            "computed_quality_score": "0",
            "contract_quality_score": "",
            "gate_result": "fail",
            "severity": "fail",
            "issues": "尚无图表登记；请先补充 14_contracts/figure_contract.csv",
            "recommendation": "为每张正文图登记 core_claim、result_id/evidence_source、输出文件和 latex_label",
        }]

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_csv_dicts(OUT_PATH, checks, CHECK_FIELDS)
    update_contract_scores(rows, checks)
    write_review(checks, source_name)

    failed = [row for row in checks if clean(row.get("gate_result")) == "fail"]
    print(f"[OK] wrote {rel(OUT_PATH)}")
    print(f"[OK] wrote {rel(REVIEW_PATH)}")
    print(f"[INFO] figures checked={len(checks)}, failed={len(failed)}")

    if failed and not (args.allow_fail or args.dev_debug):
        raise SystemExit("[FAIL] active figure contract check failed; see figure_quality_check.csv")

    complete_stage("figures", f"Checked {len(checks)} figure contract row(s); failed={len(failed)}.")


if __name__ == "__main__":
    main()
