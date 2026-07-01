from __future__ import annotations

import argparse
import csv
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple

from workflow_utils import (
    ROOT,
    assert_stage_allowed,
    complete_stage,
    read_csv_dict,
    read_state,
    rel,
    resolve_stage_for_current,
    write_csv_dicts,
)

SECTIONS_DIR = ROOT / "02_latex_template" / "sections"
PAPER_DIR = ROOT / "09_paper"
CONTRACT_DIR = ROOT / "14_contracts"
PLAN_PATH = PAPER_DIR / "section_generation_plan.csv"
SECTION_CLAIMS_PATH = PAPER_DIR / "section_claims.csv"
MISSING_EVIDENCE_PATH = PAPER_DIR / "missing_evidence_report.md"

SECTION_ORDER = [
    "01_background",
    "02_problem_analysis",
    "05_data_analysis",
    "03_assumptions",
    "04_symbols",
    "06_model_q1",
    "07_model_q2",
    "08_model_q3",
    "09_sensitivity",
    "10_model_evaluation",
    "11_conclusion",
    "00_abstract",
]

SECTION_TITLES = {
    "00_abstract": "摘要",
    "01_background": "问题背景与问题重述",
    "02_problem_analysis": "问题分析",
    "03_assumptions": "模型假设",
    "04_symbols": "符号说明",
    "05_data_analysis": "数据预处理与数据分析",
    "06_model_q1": "问题一模型建立与求解",
    "07_model_q2": "问题二模型建立与求解",
    "08_model_q3": "问题三模型建立与求解",
    "09_sensitivity": "灵敏度分析与误差分析",
    "10_model_evaluation": "模型评价",
    "11_conclusion": "结论",
}

SECTION_QUESTION = {
    "06_model_q1": "Q1",
    "07_model_q2": "Q2",
    "08_model_q3": "Q3",
}

PLAN_FIELDS = [
    "section_id",
    "section_file",
    "depends_on",
    "required_contracts",
    "required_sources",
    "status",
    "human_confirmed",
    "generated_at",
    "claim_count",
    "missing_evidence_count",
    "notes",
]

SECTION_CLAIM_FIELDS = [
    "section_id",
    "claim_id",
    "question_id",
    "claim_text",
    "evidence_type",
    "evidence_id",
    "result_id",
    "figure_id",
    "formula_id",
    "citation_id",
    "support_grade",
    "status",
    "written_to_file",
    "risk_note",
]

BAD_SUPPORT = {"", "none", "unsupported", "weak", "unverified", "todo", "missing", "待补", "未验证"}
ACTIVE_STATUSES = {"active", "approved", "frozen", "used", "ready", "completed", "confirmed", "已确认", "通过"}
INACTIVE_STATUSES = {"", "draft", "pending", "todo", "archived", "deprecated", "rejected", "disabled", "草稿", "待定"}


def clean(value: Any) -> str:
    return str(value or "").strip()


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def latex_escape(text: Any) -> str:
    s = clean(text)
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in s)


def split_ids(value: Any) -> List[str]:
    raw = clean(value)
    if not raw:
        return []
    return [x.strip() for x in re.split(r"[;,，、\s]+", raw) if x.strip()]


def id_set(rows: Sequence[Mapping[str, Any]], key: str) -> set[str]:
    return {clean(row.get(key)) for row in rows if clean(row.get(key))}


def by_id(rows: Sequence[Mapping[str, str]], key: str) -> Dict[str, Mapping[str, str]]:
    return {clean(row.get(key)): row for row in rows if clean(row.get(key))}


def status(row: Mapping[str, Any], key: str = "status") -> str:
    return clean(row.get(key)).lower()


def is_active(row: Mapping[str, Any], key: str = "status") -> bool:
    value = status(row, key)
    if value in ACTIVE_STATUSES:
        return True
    if value in INACTIVE_STATUSES:
        return False
    return bool(value)


def default_plan_row(section: str) -> Dict[str, str]:
    return {
        "section_id": section,
        "section_file": f"{section}.tex",
        "depends_on": "confirmed_previous_results",
        "required_contracts": "claim_evidence_map;result_contract;figure_contract;formula_contract;citation_contract",
        "required_sources": "07_results;08_figures;14_contracts",
        "status": "pending",
        "human_confirmed": "否",
        "generated_at": "",
        "claim_count": "0",
        "missing_evidence_count": "0",
        "notes": "v3.2-MVP contract-driven generation",
    }


def ensure_plan() -> None:
    PAPER_DIR.mkdir(parents=True, exist_ok=True)
    rows = read_csv_dict(PLAN_PATH) if PLAN_PATH.exists() else []
    if not rows:
        write_csv_dicts(PLAN_PATH, [default_plan_row(s) for s in SECTION_ORDER], PLAN_FIELDS)
        return

    changed = False
    for row in rows:
        for field in PLAN_FIELDS:
            if field not in row:
                row[field] = ""
                changed = True
    known = {clean(row.get("section_id")) for row in rows}
    for section in SECTION_ORDER:
        if section not in known:
            rows.append(default_plan_row(section))
            changed = True
    if changed:
        write_csv_dicts(PLAN_PATH, rows, PLAN_FIELDS)


def choose_current_section() -> str:
    ensure_plan()
    rows = read_csv_dict(PLAN_PATH)
    for row in rows:
        if clean(row.get("status")).lower() not in {"completed", "done", "已完成"}:
            return clean(row.get("section_id")) or SECTION_ORDER[0]
    return "00_abstract"


def load_contracts() -> Dict[str, List[Dict[str, str]]]:
    return {
        "claims": read_csv_dict(CONTRACT_DIR / "claim_evidence_map.csv"),
        "results": read_csv_dict(CONTRACT_DIR / "result_contract.csv"),
        "figures": read_csv_dict(CONTRACT_DIR / "figure_contract.csv"),
        "formulas": read_csv_dict(CONTRACT_DIR / "formula_contract.csv"),
        "citations": read_csv_dict(CONTRACT_DIR / "citation_contract.csv"),
    }


def claim_supported(claim: Mapping[str, str], contracts: Mapping[str, Sequence[Mapping[str, str]]]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    grade = clean(claim.get("support_grade")).lower()
    if grade in BAD_SUPPORT:
        issues.append(f"support_grade={grade or '<empty>'}")
    if not any(clean(claim.get(k)) for k in ["evidence_id", "result_id", "figure_id", "formula_id", "citation_id"]):
        issues.append("no evidence id")

    result_ids = id_set(contracts["results"], "result_id")
    figure_ids = id_set(contracts["figures"], "figure_id")
    formula_ids = id_set(contracts["formulas"], "formula_id")
    citation_ids = id_set(contracts["citations"], "citation_id")

    for rid in split_ids(claim.get("result_id")):
        if rid not in result_ids:
            issues.append(f"missing result_id={rid}")
    for fid in split_ids(claim.get("figure_id")):
        if fid not in figure_ids:
            issues.append(f"missing figure_id={fid}")
    for fid in split_ids(claim.get("formula_id")):
        if fid not in formula_ids:
            issues.append(f"missing formula_id={fid}")
    for cid in split_ids(claim.get("citation_id")):
        if cid not in citation_ids:
            issues.append(f"missing citation_id={cid}")
    return (not issues, issues)


def rows_for_section(section: str, contracts: Mapping[str, Sequence[Mapping[str, str]]], name: str) -> List[Dict[str, str]]:
    qid = SECTION_QUESTION.get(section)
    rows: List[Dict[str, str]] = []
    if name == "claims":
        for raw in contracts["claims"]:
            row = dict(raw)
            claim_section = clean(row.get("section_id"))
            claim_q = clean(row.get("question_id")).upper()
            if claim_section == section or (qid and claim_q == qid.upper()):
                rows.append(row)
            elif section in {"00_abstract", "11_conclusion"} and is_active(row):
                rows.append(row)
        return rows

    if name == "figures":
        for raw in contracts["figures"]:
            row = dict(raw)
            if clean(row.get("used_in_section")) == section or (qid and clean(row.get("question_id")).upper() == qid.upper()):
                rows.append(row)
        return rows

    if name == "formulas":
        for raw in contracts["formulas"]:
            row = dict(raw)
            if clean(row.get("section_id")) == section or clean(row.get("used_in_section")) == section:
                rows.append(row)
            elif qid and clean(row.get("question_id")).upper() == qid.upper():
                rows.append(row)
        return rows

    if name == "results":
        claim_result_ids = set()
        for claim in rows_for_section(section, contracts, "claims"):
            claim_result_ids.update(split_ids(claim.get("result_id")))
        for raw in contracts["results"]:
            row = dict(raw)
            rid = clean(row.get("result_id"))
            if rid in claim_result_ids or (qid and clean(row.get("question_id")).upper() == qid.upper()):
                rows.append(row)
        return rows

    return rows


def citation_markup(citation_ids: str, citations: Mapping[str, Mapping[str, str]], warnings: List[str]) -> str:
    keys: List[str] = []
    for cid in split_ids(citation_ids):
        row = citations.get(cid)
        if not row:
            warnings.append(f"citation {cid} missing from citation_contract.csv")
            continue
        key = clean(row.get("bibtex_key"))
        verified = clean(row.get("metadata_verified")).lower() in {"true", "yes", "1", "是", "已确认"}
        if key and verified:
            keys.append(key)
        elif key:
            warnings.append(f"citation {cid} has bibtex_key but metadata_verified is not true")
        else:
            warnings.append(f"citation {cid} has no bibtex_key")
    return f"~\\cite{{{','.join(keys)}}}" if keys else ""


def render_results(results: Sequence[Mapping[str, str]]) -> List[str]:
    if not results:
        return []
    lines = ["\\paragraph{已冻结结果摘要}", "\\begin{itemize}"]
    for row in results:
        rid = latex_escape(row.get("result_id"))
        metric = latex_escape(row.get("metric_name"))
        value = latex_escape(row.get("metric_value"))
        unit = latex_escape(row.get("unit"))
        src = latex_escape(row.get("source_file"))
        text = f"\\textbf{{{rid}}}"
        if metric:
            text += f"：{metric}"
        if value:
            text += f" = {value}{(' ' + unit) if unit else ''}"
        if src:
            text += f"；来源：\\texttt{{{src}}}"
        lines.append(f"  \\item {text}。")
    lines.append("\\end{itemize}")
    return lines


def render_formulas(formulas: Sequence[Mapping[str, str]]) -> List[str]:
    lines: List[str] = []
    for row in formulas:
        formula = clean(row.get("formula_latex"))
        if not formula:
            continue
        lines.append("\\begin{equation}")
        lines.append(formula)
        label = clean(row.get("latex_label"))
        if label:
            lines.append(f"\\label{{{label}}}")
        lines.append("\\end{equation}")
        symbols = latex_escape(row.get("symbols_defined"))
        if symbols:
            lines.append(f"其中，{symbols}。")
    return lines


def render_figures(figures: Sequence[Mapping[str, str]]) -> List[str]:
    lines: List[str] = []
    for row in figures:
        fig_id = latex_escape(row.get("figure_id"))
        claim = latex_escape(row.get("core_claim"))
        label = clean(row.get("latex_label"))
        if label and claim:
            lines.append(f"图~\\ref{{{label}}} 对应图表契约 {fig_id}，核心论证为：{claim}。")
        elif claim:
            lines.append(f"图表契约 {fig_id} 的核心论证为：{claim}。该图尚未登记 LaTeX label，正式稿不得直接引用。")
    return lines


def render_claims(section: str, claims: Sequence[Mapping[str, str]], contracts: Mapping[str, Sequence[Mapping[str, str]]]) -> Tuple[List[str], List[Dict[str, str]], List[str]]:
    citations = by_id(contracts["citations"], "citation_id")
    lines: List[str] = []
    used: List[Dict[str, str]] = []
    warnings: List[str] = []

    if not claims:
        return ["本节暂未发现可写入的已登记论断。请先在 \\texttt{14\\_contracts/claim\\_evidence\\_map.csv} 中补充 claim 与 evidence 关系。"], used, warnings

    for claim in claims:
        supported, issues = claim_supported(claim, contracts)
        cid = clean(claim.get("claim_id"))
        if not supported:
            warnings.append(f"{cid or '<empty claim_id>'}: " + "; ".join(issues))
            continue
        text = latex_escape(claim.get("claim_text"))
        if not text:
            warnings.append(f"{cid or '<empty claim_id>'}: empty claim_text")
            continue
        cite = citation_markup(clean(claim.get("citation_id")), citations, warnings)
        boundary = latex_escape(claim.get("boundary_condition"))
        if boundary:
            lines.append(f"{text}{cite}。该结论成立的边界条件为：{boundary}。")
        else:
            lines.append(f"{text}{cite}。")
        used.append({
            "section_id": section,
            "claim_id": cid,
            "question_id": clean(claim.get("question_id")),
            "claim_text": clean(claim.get("claim_text")),
            "evidence_type": clean(claim.get("evidence_type")),
            "evidence_id": clean(claim.get("evidence_id")),
            "result_id": clean(claim.get("result_id")),
            "figure_id": clean(claim.get("figure_id")),
            "formula_id": clean(claim.get("formula_id")),
            "citation_id": clean(claim.get("citation_id")),
            "support_grade": clean(claim.get("support_grade")),
            "status": clean(claim.get("status")),
            "written_to_file": "是",
            "risk_note": clean(claim.get("risk_note")),
        })

    if not lines:
        lines.append("本节存在候选论断，但均未通过证据契约检查，因此暂不写入实质性结论。")
    return lines, used, warnings


def read_optional(path: Path, max_chars: int = 1200) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore").strip()[:max_chars]


def paragraph_from_file(title: str, path: Path) -> List[str]:
    text = read_optional(path)
    if not text:
        return [f"\\paragraph{{{title}}} 尚未找到 \\texttt{{{latex_escape(rel(path))}}}，本节保留占位。"]
    compact = re.sub(r"\s+", " ", text)
    return [f"\\paragraph{{{title}}} 以下内容来自项目已登记材料摘要，正式稿需人工改写与核验：", latex_escape(compact)]


def render_symbols(formulas: Sequence[Mapping[str, str]]) -> List[str]:
    rows = [r for r in formulas if clean(r.get("symbols_defined"))]
    if not rows:
        return ["符号说明尚未从 \\texttt{14\\_contracts/formula\\_contract.csv} 中登记。请先补充公式、符号含义与单位。"]
    lines = [
        "\\begin{table}[htbp]",
        "\\centering",
        "\\caption{主要符号说明}",
        "\\begin{tabular}{p{0.22\\linewidth}p{0.68\\linewidth}}",
        "\\toprule",
        "符号来源 & 含义说明 \\\\",
        "\\midrule",
    ]
    for row in rows:
        source = latex_escape(row.get("formula_id") or row.get("latex_label"))
        symbols = latex_escape(row.get("symbols_defined"))
        lines.append(f"{source} & {symbols} \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}"])
    return lines


def render_section(section: str, contracts: Mapping[str, Sequence[Mapping[str, str]]]) -> Tuple[str, List[Dict[str, str]], List[str]]:
    title = SECTION_TITLES.get(section, section)
    claims = rows_for_section(section, contracts, "claims")
    results = rows_for_section(section, contracts, "results")
    figures = rows_for_section(section, contracts, "figures")
    formulas = rows_for_section(section, contracts, "formulas")
    claim_lines, used_claims, warnings = render_claims(section, claims, contracts)

    lines: List[str] = [
        "% Auto-generated by v3.2-MVP contract-driven generate_paper_sections.py",
        f"% generated_at: {now()}",
        "% Do not treat placeholders as final submission text.",
        "",
    ]

    if section == "00_abstract":
        lines.append("\\begin{abstract}")
        if used_claims:
            lines.append("本文基于已登记的结果契约与论断证据映射，对赛题问题进行了建模求解。核心结论均来自 \\texttt{14\\_contracts} 中已登记的 claim、result、figure 与 citation。")
            for line in claim_lines[:4]:
                lines.append(line)
        else:
            lines.append("摘要必须在模型结果、图表和结论全部冻结并经人工确认后生成；当前文本仅为占位骨架，禁止直接提交。")
        lines.append("\\end{abstract}")
        lines.append("")
        lines.append("\\noindent\\textbf{关键词：} 数学建模；合同驱动；数据分析；模型求解")
        return "\n".join(lines) + "\n", used_claims, warnings

    lines.append(f"\\section{{{title}}}")
    lines.append("")

    if section == "01_background":
        lines.extend(paragraph_from_file("赛题背景材料", ROOT / "00_problem" / "problem_statement.md"))
        lines.append("")
    elif section == "02_problem_analysis":
        lines.extend(paragraph_from_file("任务分解", ROOT / "01_task_analysis" / "task_decomposition.md"))
        lines.append("")
    elif section == "03_assumptions":
        lines.extend(paragraph_from_file("模型假设", ROOT / "05_model" / "assumptions.md"))
        lines.append("")
    elif section == "04_symbols":
        lines.extend(render_symbols(contracts["formulas"]))
        lines.append("")
    elif section == "05_data_analysis":
        lines.extend(paragraph_from_file("数据质量与预处理", ROOT / "03_data" / "data_quality_report.md"))
        lines.append("")

    lines.extend(render_formulas(formulas))
    if formulas:
        lines.append("")

    lines.extend(render_results(results))
    if results:
        lines.append("")

    lines.extend(claim_lines)
    lines.append("")

    fig_lines = render_figures(figures)
    if fig_lines:
        lines.append("\\paragraph{图表论证}")
        lines.extend(fig_lines)
        lines.append("")

    lines.append("\\paragraph{人工复核要求}")
    lines.append("本节所有实质性结论必须能追溯到 \\texttt{14\\_contracts}，不得写入未冻结结果、未登记图表或未核验引用。")
    return "\n".join(lines) + "\n", used_claims, warnings


def update_plan(section: str, used_count: int, warning_count: int) -> None:
    ensure_plan()
    rows = read_csv_dict(PLAN_PATH)
    for row in rows:
        if clean(row.get("section_id")) == section:
            row["status"] = "completed"
            row["generated_at"] = now()
            row["claim_count"] = str(used_count)
            row["missing_evidence_count"] = str(warning_count)
            row["notes"] = "generated from contract bus; check missing_evidence_report.md"
    write_csv_dicts(PLAN_PATH, rows, PLAN_FIELDS)


def append_section_claims(rows: Sequence[Mapping[str, str]]) -> None:
    existing = read_csv_dict(SECTION_CLAIMS_PATH) if SECTION_CLAIMS_PATH.exists() else []
    existing = [r for r in existing if clean(r.get("section_id")) != (clean(rows[0].get("section_id")) if rows else "")]
    all_rows = existing + [dict(r) for r in rows]
    write_csv_dicts(SECTION_CLAIMS_PATH, all_rows, SECTION_CLAIM_FIELDS)


def write_missing_report(section: str, warnings: Sequence[str]) -> None:
    old = MISSING_EVIDENCE_PATH.read_text(encoding="utf-8") if MISSING_EVIDENCE_PATH.exists() else "# Missing evidence report\n\n"
    block = [f"## {section} - {now()}", ""]
    if warnings:
        block.extend([f"- {w}" for w in warnings])
    else:
        block.append("- No missing evidence detected for written claims.")
    block.append("")
    MISSING_EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    MISSING_EVIDENCE_PATH.write_text(old.rstrip() + "\n\n" + "\n".join(block), encoding="utf-8")


def write_section(section: str, force: bool = False) -> Tuple[Path, int, int]:
    contracts = load_contracts()
    text, used_claims, warnings = render_section(section, contracts)
    SECTIONS_DIR.mkdir(parents=True, exist_ok=True)
    path = SECTIONS_DIR / f"{section}.tex"
    if path.exists() and not force:
        backup = path.with_suffix(path.suffix + f".bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        backup.write_text(path.read_text(encoding="utf-8", errors="ignore"), encoding="utf-8")
    path.write_text(text, encoding="utf-8")
    update_plan(section, len(used_claims), len(warnings))
    if used_claims:
        append_section_claims(used_claims)
    write_missing_report(section, warnings)
    return path, len(used_claims), len(warnings)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate one LaTeX section from v3.2-MVP contracts.")
    parser.add_argument("--section", default="current", help="Section id, current, or all. all requires --dev-debug.")
    parser.add_argument("--mode", default="deep")
    parser.add_argument("--force", action="store_true", help="Overwrite without backup.")
    parser.add_argument("--dev-debug", action="store_true")
    args = parser.parse_args()

    assert_stage_allowed("paper_draft", args.dev_debug)
    actual_stage = resolve_stage_for_current("paper_draft", read_state())

    if args.section == "all" and not args.dev_debug:
        raise SystemExit("[FAIL] 单环节深度模式禁止一次性生成全文。请逐节生成，或仅在开发调试时使用 --dev-debug。")

    if args.section == "current":
        section = choose_current_section()
        path, used_count, warning_count = write_section(section, args.force)
        complete_stage("paper_draft", f"Generated {section} into {rel(path)} from contract bus; claims={used_count}, warnings={warning_count}.")
        print(f"[OK] wrote {rel(path)}")
        print(f"[OK] updated {rel(PLAN_PATH)} and {rel(MISSING_EVIDENCE_PATH)}")
        return

    sections = SECTION_ORDER if args.section == "all" else [args.section]
    outputs: List[str] = []
    total_claims = 0
    total_warnings = 0
    for section in sections:
        path, used_count, warning_count = write_section(section, args.force)
        outputs.append(rel(path))
        total_claims += used_count
        total_warnings += warning_count

    complete_stage("paper_draft", f"Generated {len(outputs)} section(s) from contract bus during {actual_stage}; claims={total_claims}, warnings={total_warnings}.")
    print("[OK] wrote:")
    for item in outputs:
        print(f"  - {item}")


if __name__ == "__main__":
    main()
