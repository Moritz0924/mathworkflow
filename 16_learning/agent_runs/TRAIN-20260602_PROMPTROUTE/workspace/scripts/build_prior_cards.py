from __future__ import annotations

import argparse
from collections import defaultdict
from typing import Any, Dict, List

from learning_utils import (
    ROOT,
    compact_list,
    family_model_hints,
    family_problem_type,
    family_scoring_risks,
    load_family_figure_hints,
    policy_path,
    read_csv_rows,
    read_learning_policy,
    stable_id,
    utc_now,
    write_csv_rows,
    write_jsonl,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build abstract prior cards from the extracted corpus manifest.")
    parser.parse_args()

    policy = read_learning_policy()
    paths = policy.get("paths") or {}
    manifest_path = policy_path(paths.get("manifest", ""), "13_prior_db/screening/pdf_manifest.csv")
    cards_path = policy_path(paths.get("prior_cards", ""), "13_prior_db/cards/prior_cards.jsonl")
    feature_path = policy_path(paths.get("training_data", ""), "16_learning/training_data") / "prior_card_features.csv"
    report_path = policy_path(paths.get("reports", ""), "16_learning/reports") / "prior_cards_report.md"
    rows = read_csv_rows(manifest_path)
    if not rows:
        raise SystemExit(f"[FAIL] missing or empty manifest: {manifest_path.relative_to(ROOT)}")

    figure_hints = load_family_figure_hints()
    grouped: Dict[tuple[str, str], List[Dict[str, str]]] = defaultdict(list)
    for row in rows:
        category = row.get("category") or "unknown"
        family = row.get("family") or "综合集成"
        grouped[(category, family)].append(row)

    created_at = utc_now()
    cards: List[Dict[str, Any]] = []
    feature_rows: List[Dict[str, Any]] = []
    for (category, family), group in sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0][1], item[0][0])):
        card_id = stable_id("CARD", f"{category}|{family}")
        source_ids = [row.get("source_id", "") for row in group if row.get("source_id")]
        source_hashes = [row.get("text_hash", "") for row in group if row.get("text_hash")]
        hints = family_model_hints(category, family)
        figures = figure_hints.get(family) or figure_hints.get("综合集成") or []
        risks = family_scoring_risks(family)
        status_values = {row.get("extract_status", "") for row in group}
        extraction_note = "has_partial_or_failed_sources" if any(str(s).startswith("failed") or s == "partial" for s in status_values) else "source_text_extracted"
        card = {
            "card_id": card_id,
            "source_ids": source_ids,
            "category": category,
            "family": family,
            "problem_type": family_problem_type(family),
            "model_hints": hints,
            "figure_hints": figures,
            "scoring_risks": risks,
            "copy_risk_status": "abstracted_pass",
            "source_hashes": compact_list(source_hashes, max_items=12),
            "source_count": len(source_ids),
            "created_at": created_at,
            "notes": extraction_note,
        }
        cards.append(card)
        feature_rows.append(
            {
                "card_id": card_id,
                "category": category,
                "family": family,
                "problem_type": family_problem_type(family),
                "source_count": len(source_ids),
                "figure_hint_count": len(figures),
                "risk_hint_count": len(risks),
                "copy_risk_status": "abstracted_pass",
            }
        )

    write_jsonl(cards_path, cards)
    write_csv_rows(
        feature_path,
        feature_rows,
        ["card_id", "category", "family", "problem_type", "source_count", "figure_hint_count", "risk_hint_count", "copy_risk_status"],
    )

    lines = [
        "# Prior Cards Report",
        "",
        f"- generated_at: {created_at}",
        f"- source_manifest_rows: {len(rows)}",
        f"- prior_card_count: {len(cards)}",
        f"- output: {cards_path.relative_to(ROOT).as_posix()}",
        "",
        "## Largest Cards",
        "",
    ]
    for card in sorted(cards, key=lambda item: int(item.get("source_count") or 0), reverse=True)[:12]:
        lines.append(f"- {card['card_id']} | {card['category']} | {card['family']} | sources={card['source_count']}")
    lines += [
        "",
        "## Copy Policy",
        "",
        "- Cards contain abstract model, figure, and risk hints only.",
        "- No source paragraphs, abstracts, captions, tables, or conclusions are copied into card text.",
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] wrote {cards_path.relative_to(ROOT)}")
    print(f"[OK] wrote {feature_path.relative_to(ROOT)}")
    print(f"[OK] wrote {report_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
