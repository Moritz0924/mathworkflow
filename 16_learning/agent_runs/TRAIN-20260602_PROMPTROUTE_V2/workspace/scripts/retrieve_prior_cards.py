from __future__ import annotations

import argparse
from typing import Any, Dict, List

from learning_utils import (
    ROOT,
    cosine_sparse,
    policy_path,
    read_csv_rows,
    read_json,
    read_learning_policy,
    split_semicolon,
    tfidf_vector,
    utc_now,
    write_csv_rows,
)


RESULT_FIELDS = [
    "question",
    "card_id",
    "category",
    "family",
    "problem_type",
    "score",
    "source_ids",
    "copy_risk_status",
]


def row_query(row: Dict[str, str]) -> str:
    return "\n".join(
        [
            row.get("question") or row.get("question_id") or "",
            row.get("problem_type") or "",
            row.get("model_family") or "",
            row.get("main_model") or "",
            row.get("baseline_model") or "",
            row.get("data_shape") or "",
            row.get("output_type") or "",
            row.get("risk_focus") or "",
            row.get("notes") or "",
        ]
    )


def has_profile_signal(row: Dict[str, str]) -> bool:
    signal_keys = [
        "problem_type",
        "model_family",
        "main_model",
        "baseline_model",
        "data_shape",
        "output_type",
        "risk_focus",
        "notes",
    ]
    return any(str(row.get(key) or "").strip() for key in signal_keys)


def search(index: Dict[str, Any], query: str, top_k: int, min_score: float) -> List[Dict[str, Any]]:
    qvec = tfidf_vector(query, index.get("idf") or {})
    results: List[Dict[str, Any]] = []
    for doc in index.get("docs") or []:
        if str(doc.get("copy_risk_status") or "") not in {"abstracted_pass", "pass", "checked_pass"}:
            continue
        score = cosine_sparse(qvec, doc.get("vector") or {})
        if score >= min_score:
            out = dict(doc)
            out["score"] = score
            results.append(out)
    results.sort(key=lambda item: float(item.get("score") or 0.0), reverse=True)
    return results[:top_k]


def format_card_block(question: str, doc: Dict[str, Any], rank: int) -> List[str]:
    source_ids = doc.get("source_ids") or []
    if isinstance(source_ids, str):
        source_ids = split_semicolon(source_ids)
    source_preview = ";".join(str(x) for x in source_ids[:8])
    text = str(doc.get("search_text") or "")
    lines = [
        f"### {question} card {rank}: {doc.get('category')} / {doc.get('family')}",
        "",
        f"- card_id: {doc.get('card_id')}",
        f"- confidence: {float(doc.get('score') or 0.0):.4f}",
        f"- problem_type_experience: {doc.get('problem_type')}",
        f"- source_ids: {source_preview}",
        "",
    ]
    for label, heading in [
        ("model_hints", "common_model_families"),
        ("figure_hints", "common_figure_types"),
        ("scoring_risks", "common_scoring_risks"),
    ]:
        marker = heading
        values: List[str] = []
        if label == "model_hints":
            values = [part.strip() for part in text.splitlines() if part.strip()][:5]
        elif label == "figure_hints":
            values = [part.strip() for part in text.splitlines() if "图" in part or "matrix" in part.lower() or "heat" in part.lower()][:5]
        else:
            values = [part.strip() for part in text.splitlines() if "missing" in part.lower() or "unclear" in part.lower() or "weak" in part.lower()][:5]
        lines.append(f"- {marker}: {'; '.join(values) if values else 'see prior card JSONL'}")
    lines.append("")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Retrieve advisory prior cards for problem-model profiles.")
    parser.add_argument("--query", default="", help="Ad hoc query text for smoke tests.")
    parser.add_argument("--top-k", type=int, default=0)
    args = parser.parse_args()

    policy = read_learning_policy()
    paths = policy.get("paths") or {}
    retrieval = policy.get("retrieval") or {}
    index_path = policy_path(paths.get("prior_index", ""), "13_prior_db/fulltext_index/prior_card_tfidf.json")
    profile_path = ROOT / "01_task_analysis" / "problem_model_profile.csv"
    out_md = ROOT / "13_prior_db" / "pre_solve_cards.md"
    out_csv = policy_path(paths.get("retrieval_results", ""), "13_prior_db/screening/retrieval_results.csv")
    top_k = args.top_k or int(retrieval.get("top_k_cards") or 5)
    min_score = float(retrieval.get("min_score_to_report") or 0.01)

    index = read_json(index_path)
    if not index:
        raise SystemExit(f"[FAIL] missing prior index: {index_path.relative_to(ROOT)}")

    queries: List[Dict[str, str]] = []
    if args.query.strip():
        queries.append({"question": "ad_hoc", "query_text": args.query.strip()})
    else:
        for row in read_csv_rows(profile_path):
            q = row.get("question") or row.get("question_id") or ""
            text = row_query(row)
            if q and has_profile_signal(row) and text.strip():
                queries.append({"question": q, "query_text": text})

    now = utc_now()
    result_rows: List[Dict[str, str]] = []
    lines = [
        "# Prior DB pre-solve cards",
        "",
        f"- generated_at: {now}",
        "- status: advisory_only",
        "- allowed_use: problem type experience, common model families, common figure types, scoring risks, preprocessing patterns",
        "- forbidden_use: source text copying, historical conclusions as current answers, unverified result claims",
        "",
    ]
    if not queries:
        lines += [
            "No usable problem profile rows were found. Fill `01_task_analysis/problem_model_profile.csv` before using prior retrieval for routing.",
            "",
        ]

    for item in queries:
        question = item["question"]
        hits = search(index, item["query_text"], top_k=top_k, min_score=min_score)
        lines += [f"## {question}", ""]
        if not hits:
            lines += ["- no prior cards above threshold", ""]
            continue
        for rank, hit in enumerate(hits, start=1):
            source_ids = hit.get("source_ids") or []
            source_text = ";".join(str(x) for x in source_ids)
            result_rows.append(
                {
                    "question": question,
                    "card_id": str(hit.get("card_id") or ""),
                    "category": str(hit.get("category") or ""),
                    "family": str(hit.get("family") or ""),
                    "problem_type": str(hit.get("problem_type") or ""),
                    "score": f"{float(hit.get('score') or 0.0):.6f}",
                    "source_ids": source_text,
                    "copy_risk_status": str(hit.get("copy_risk_status") or ""),
                }
            )
            lines.extend(format_card_block(question, hit, rank))

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_csv_rows(out_csv, result_rows, RESULT_FIELDS)
    print(f"[OK] wrote {out_md.relative_to(ROOT)}")
    print(f"[OK] wrote {out_csv.relative_to(ROOT)}")

    try:
        from workflow_utils import complete_stage, read_state

        if read_state().get("current_stage") == "prior_retrieval":
            complete_stage("prior_retrieval", "Retrieved advisory prior cards from the local RAG index. Model choices remain human-gated.")
    except Exception as exc:
        print(f"[WARN] workflow_state not updated: {exc}")


if __name__ == "__main__":
    main()
