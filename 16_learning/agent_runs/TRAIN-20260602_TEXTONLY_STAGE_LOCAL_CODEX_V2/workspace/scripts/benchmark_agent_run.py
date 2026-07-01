from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple

from agent_mode_utils import AGENT_RUNS_ROOT, read_agent_policy, safe_rel, validate_problem_source_lock, write_csv_rows
from learning_utils import ROOT, cosine_sparse, tfidf_vector

GAP_FIELDS = [
    "gap_id",
    "dimension",
    "severity",
    "benchmark_source_id",
    "evidence_summary",
    "our_artifact",
    "recommended_change",
    "acceptance_check",
    "status",
    "human_decision",
]

QUEUE_FIELDS = [
    "task_id",
    "run_id",
    "iteration",
    "severity",
    "target_artifact",
    "issue_summary",
    "proposed_action",
    "acceptance_check",
    "status",
    "human_decision",
    "notes",
]


def read_text(path: Path, max_chars: int = 300000) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")[:max_chars]


def find_or_build_draft(workspace: Path) -> Tuple[Path, str]:
    normalized = workspace / "09_paper" / "full_draft.md"
    candidates = [
        workspace / "09_paper" / "full_draft.tex",
        workspace / "09_paper" / "final_paper.md",
        workspace / "09_paper" / "draft_v2.md",
        workspace / "09_paper" / "draft_v1.md",
    ]
    if normalized.exists() and read_text(normalized).strip():
        return normalized, "existing"
    for path in candidates:
        text = read_text(path)
        if path.exists() and text.strip():
            normalized.parent.mkdir(parents=True, exist_ok=True)
            normalized.write_text(
                f"# Sandbox full draft normalized from {path.name}\n\n{text}\n",
                encoding="utf-8",
            )
            return normalized, f"normalized_from_{path.name}"
    section_dir = workspace / "02_latex_template" / "sections"
    sections = sorted(section_dir.glob("*.tex")) if section_dir.exists() else []
    chunks = [read_text(path) for path in sections if read_text(path).strip()]
    if chunks:
        normalized.parent.mkdir(parents=True, exist_ok=True)
        normalized.write_text(
            "# Sandbox full draft assembled from LaTeX sections\n\n" + "\n\n".join(chunks) + "\n",
            encoding="utf-8",
        )
        return normalized, "assembled_from_sections"
    return normalized, "missing"


def count_csv_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return sum(1 for _ in csv.DictReader(f))


def text_features(text: str) -> Dict[str, int]:
    return {
        "chars": len(text),
        "sections": len(re.findall(r"(^|\n)\s*(#{1,3}\s+|\\section\{|\\subsection\{)", text)),
        "figure_mentions": len(re.findall(r"figure|fig\.|\\includegraphics|图\s*[Ff]?\s*\d+|图\s*[一二三四五六七八九十]+|Fig", text, flags=re.I)),
        "table_mentions": len(re.findall(r"table|表\s*\d+|表\s*[一二三四五六七八九十]+|\\begin\{tabular\}", text, flags=re.I)),
        "formula_mentions": len(re.findall(r"\\begin\{equation\}|\\\[|公式|equation", text, flags=re.I)),
        "validation_mentions": len(re.findall(r"validation|sensitivity|robust|误差|残差|灵敏|敏感|检验|验证|稳健|鲁棒", text, flags=re.I)),
        "citation_mentions": len(re.findall(r"\\cite\{|参考文献|\[[0-9, ]+\]", text)),
    }


def load_prior_index() -> Dict[str, Any]:
    path = ROOT / "13_prior_db" / "fulltext_index" / "prior_card_tfidf.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def select_benchmark_sources(query: str, top_k: int) -> List[Dict[str, str]]:
    index = load_prior_index()
    if not index:
        return []
    qvec = tfidf_vector(query, index.get("idf") or {})
    hits: List[Dict[str, Any]] = []
    for doc in index.get("docs") or []:
        score = cosine_sparse(qvec, doc.get("vector") or {})
        if score <= 0:
            continue
        out = dict(doc)
        out["_score"] = score
        hits.append(out)
    hits.sort(key=lambda item: float(item.get("_score") or 0.0), reverse=True)

    manifest_by_id: Dict[str, Dict[str, str]] = {}
    manifest = ROOT / "13_prior_db" / "screening" / "pdf_manifest.csv"
    if manifest.exists():
        with manifest.open("r", encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                manifest_by_id[str(row.get("source_id") or "")] = dict(row)

    selected: List[Dict[str, str]] = []
    seen: set[str] = set()
    for hit in hits:
        source_ids = hit.get("source_ids") or []
        if isinstance(source_ids, str):
            source_ids = [source_ids]
        for source_id in source_ids:
            source_id = str(source_id)
            if not source_id or source_id in seen:
                continue
            meta = manifest_by_id.get(source_id, {})
            selected.append(
                {
                    "source_id": source_id,
                    "path": str(meta.get("path") or ""),
                    "category": str(meta.get("category") or hit.get("category") or ""),
                    "family": str(meta.get("family") or hit.get("family") or ""),
                    "card_id": str(hit.get("card_id") or ""),
                    "score": f"{float(hit.get('_score') or 0.0):.6f}",
                }
            )
            seen.add(source_id)
            if len(selected) >= top_k:
                return selected
    if selected:
        return selected

    # Conservative fallback: keep benchmarking local and non-generative even when
    # the prompt has too little overlap with prior-card vocabulary.
    fallback: List[Dict[str, str]] = []
    for source_id, meta in sorted(manifest_by_id.items()):
        if not source_id:
            continue
        if str(meta.get("extract_status") or "").startswith("failed"):
            continue
        fallback.append(
            {
                "source_id": source_id,
                "path": str(meta.get("path") or ""),
                "category": str(meta.get("category") or ""),
                "family": str(meta.get("family") or ""),
                "card_id": "fallback_manifest",
                "score": "0.000000",
            }
        )
        if len(fallback) >= top_k:
            break
    return fallback


def source_features(sources: Sequence[Mapping[str, str]]) -> Dict[str, float]:
    if not sources:
        return {key: 0.0 for key in ["chars", "sections", "figure_mentions", "table_mentions", "formula_mentions", "validation_mentions", "citation_mentions"]}
    totals: Dict[str, float] = {}
    count = 0
    for source in sources:
        text_path = ROOT / "13_prior_db" / "fulltext_index" / "source_texts" / f"{source.get('source_id')}.txt"
        text = read_text(text_path, 120000)
        if not text:
            continue
        feats = text_features(text)
        for key, value in feats.items():
            totals[key] = totals.get(key, 0.0) + value
        count += 1
    if count == 0:
        return {key: 0.0 for key in ["chars", "sections", "figure_mentions", "table_mentions", "formula_mentions", "validation_mentions", "citation_mentions"]}
    return {key: totals.get(key, 0.0) / count for key in totals}


def make_gap_rows(
    run_id: str,
    draft_path: Path,
    draft_status: str,
    our: Mapping[str, int],
    bench: Mapping[str, float],
    sources: Sequence[Mapping[str, str]],
    workspace: Path,
) -> List[Dict[str, str]]:
    source_ids = ";".join(str(s.get("source_id") or "") for s in sources)
    rel_draft = safe_rel(draft_path)
    rows: List[Dict[str, str]] = []
    if draft_status == "missing":
        return [
            {
                "gap_id": f"{run_id}-GAP-001",
                "dimension": "draft_availability",
                "severity": "fail",
                "benchmark_source_id": source_ids,
                "evidence_summary": "No sandbox full draft or section content was found.",
                "our_artifact": rel_draft,
                "recommended_change": "Run the agent to produce a contract-bound draft before benchmarking.",
                "acceptance_check": "workspace/09_paper/full_draft.md exists and contains substantive content.",
                "status": "open",
                "human_decision": "",
            }
        ]

    checks = [
        (
            "structure_depth",
            our.get("sections", 0),
            max(4.0, bench.get("sections", 0) * 0.65),
            "major",
            "Expand the paper structure so problem analysis, model building, results, validation, and conclusion are all visible.",
            "Draft contains at least five clear sections or subsections.",
        ),
        (
            "figure_density",
            our.get("figure_mentions", 0),
            max(2.0, bench.get("figure_mentions", 0) * 0.25),
            "major",
            "Add result-bound figures and register them in the sandbox figure contract before citing them.",
            "Figure mentions are backed by existing figure files and figure_contract rows.",
        ),
        (
            "validation_completeness",
            our.get("validation_mentions", 0),
            max(2.0, bench.get("validation_mentions", 0) * 0.3),
            "major",
            "Add validation, sensitivity, robustness, or error analysis tied to model outputs.",
            "Validation section cites frozen result rows or reproducible code outputs.",
        ),
        (
            "formula_and_model_detail",
            our.get("formula_mentions", 0),
            max(1.0, bench.get("formula_mentions", 0) * 0.2),
            "minor",
            "Make the core model equations and variable definitions explicit.",
            "Important formulas have formula_contract rows and symbol definitions.",
        ),
    ]
    for idx, (dimension, actual, threshold, severity, change, acceptance) in enumerate(checks, start=1):
        if actual >= threshold:
            continue
        rows.append(
            {
                "gap_id": f"{run_id}-GAP-{idx:03d}",
                "dimension": dimension,
                "severity": severity,
                "benchmark_source_id": source_ids,
                "evidence_summary": f"our_count={actual}; benchmark_average={bench.get(dimension, threshold):.2f}; threshold={threshold:.2f}",
                "our_artifact": rel_draft,
                "recommended_change": change,
                "acceptance_check": acceptance,
                "status": "open",
                "human_decision": "",
            }
        )

    claim_rows = count_csv_rows(workspace / "14_contracts" / "claim_evidence_map.csv")
    result_rows = count_csv_rows(workspace / "14_contracts" / "result_contract.csv")
    if claim_rows == 0 or result_rows == 0:
        rows.append(
            {
                "gap_id": f"{run_id}-GAP-900",
                "dimension": "contract_binding",
                "severity": "fail",
                "benchmark_source_id": source_ids,
                "evidence_summary": f"claim_rows={claim_rows}; result_rows={result_rows}",
                "our_artifact": "workspace/14_contracts",
                "recommended_change": "Populate sandbox result_contract and claim_evidence_map before treating draft claims as paper-ready.",
                "acceptance_check": "Both contract files contain rows supporting major claims and numerical results.",
                "status": "open",
                "human_decision": "",
            }
        )
    return rows


def queue_from_gaps(run_id: str, gap_rows: Sequence[Mapping[str, str]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for idx, gap in enumerate(gap_rows, start=1):
        rows.append(
            {
                "task_id": f"{run_id}-TASK-{idx:03d}",
                "run_id": run_id,
                "iteration": "1",
                "severity": gap.get("severity", ""),
                "target_artifact": gap.get("our_artifact", ""),
                "issue_summary": gap.get("evidence_summary", ""),
                "proposed_action": gap.get("recommended_change", ""),
                "acceptance_check": gap.get("acceptance_check", ""),
                "status": "open",
                "human_decision": "",
                "notes": f"from {gap.get('gap_id', '')}",
            }
        )
    return rows


def write_full_report(
    run_id: str,
    run_dir: Path,
    draft_path: Path,
    draft_status: str,
    our: Mapping[str, int],
    bench: Mapping[str, float],
    sources: Sequence[Mapping[str, str]],
    gaps: Sequence[Mapping[str, str]],
) -> Path:
    report = run_dir / "reports" / "full_gap_report.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Agent Training Gap Report",
        "",
        f"- run_id: {run_id}",
        f"- draft: {safe_rel(draft_path)}",
        f"- draft_status: {draft_status}",
        f"- benchmark_source: local prior DB",
        "",
        "## Benchmark Sources",
        "",
    ]
    if sources:
        for source in sources:
            lines.append(
                f"- {source.get('source_id')} | {source.get('family')} | {source.get('category')} | card={source.get('card_id')} | score={source.get('score')}"
            )
    else:
        lines.append("- No prior DB benchmark source was selected.")
    lines += [
        "",
        "## Feature Comparison",
        "",
        "| metric | sandbox | benchmark_average |",
        "|---|---:|---:|",
    ]
    for key in ["chars", "sections", "figure_mentions", "table_mentions", "formula_mentions", "validation_mentions", "citation_mentions"]:
        lines.append(f"| {key} | {our.get(key, 0)} | {float(bench.get(key, 0.0)):.2f} |")
    lines += ["", "## Gap Findings", ""]
    if gaps:
        for gap in gaps:
            lines.append(f"- [{gap.get('severity')}] {gap.get('dimension')}: {gap.get('recommended_change')}")
    else:
        lines.append("- No major structural gap found by the lightweight benchmark checks.")
    lines += [
        "",
        "## Safety",
        "",
        "- This report compares counts, structure signals, and risk patterns only.",
        "- It intentionally does not copy prior-paper text, abstracts, captions, tables, or conclusions.",
        "- Any promotion into the formal workflow must go through contracts, review tasks, and human gates.",
    ]
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def benchmark_run(run_id: str) -> Dict[str, Any]:
    policy = read_agent_policy()
    run_dir = AGENT_RUNS_ROOT / run_id
    workspace = run_dir / "workspace"
    if not workspace.exists():
        raise SystemExit(f"[FAIL] missing workspace for run_id={run_id}")
    top_k = int(((policy.get("benchmark") or {}).get("top_k_fulltext")) or 3)
    draft_path, draft_status = find_or_build_draft(workspace)
    drift_issues = validate_problem_source_lock(run_dir, workspace)
    if drift_issues:
        detail = "; ".join(str(issue.get("detail") or "") for issue in drift_issues)
        gaps = [
            {
                "gap_id": f"{run_id}-GAP-DRIFT",
                "dimension": "problem_source_drift",
                "severity": "fail",
                "benchmark_source_id": "",
                "evidence_summary": detail or "problem statement no longer matches problem_source_lock.json",
                "our_artifact": safe_rel(workspace / "00_problem" / "problem_statement.md"),
                "recommended_change": "Restore the locked sandbox problem statement before benchmarking or revising paper artifacts.",
                "acceptance_check": "problem_statement.md sha256 matches reports/problem_source_lock.json source.sha256.",
                "status": "open",
                "human_decision": "",
            }
        ]
        queue = queue_from_gaps(run_id, gaps)
        write_csv_rows(run_dir / "reports" / "gap_report.csv", gaps, GAP_FIELDS)
        write_csv_rows(run_dir / "reports" / "agent_revision_queue.csv", queue, QUEUE_FIELDS)
        our = text_features(read_text(draft_path, 60000) if draft_path.exists() else "")
        bench = source_features([])
        report = write_full_report(run_id, run_dir, draft_path, draft_status, our, bench, [], gaps)
        return {
            "run_id": run_id,
            "draft_path": safe_rel(draft_path),
            "draft_status": draft_status,
            "gap_count": len(gaps),
            "queue_count": len(queue),
            "report": safe_rel(report),
            "problem_source_drift": True,
        }
    problem_text = read_text(workspace / "00_problem" / "problem_statement.md", 20000)
    draft_text = read_text(draft_path, 60000) if draft_path.exists() else ""
    query = problem_text + "\n\n" + draft_text[:12000]
    sources = select_benchmark_sources(query, top_k=top_k)
    our = text_features(draft_text)
    bench = source_features(sources)
    gaps = make_gap_rows(run_id, draft_path, draft_status, our, bench, sources, workspace)
    queue = queue_from_gaps(run_id, gaps)
    write_csv_rows(run_dir / "reports" / "gap_report.csv", gaps, GAP_FIELDS)
    write_csv_rows(run_dir / "reports" / "agent_revision_queue.csv", queue, QUEUE_FIELDS)
    report = write_full_report(run_id, run_dir, draft_path, draft_status, our, bench, sources, gaps)
    return {
        "run_id": run_id,
        "draft_path": safe_rel(draft_path),
        "draft_status": draft_status,
        "gap_count": len(gaps),
        "queue_count": len(queue),
        "report": safe_rel(report),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark an agent training run against the local prior DB.")
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    result = benchmark_run(args.run_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
