from __future__ import annotations

import argparse
from collections import Counter
from typing import Dict, List

from learning_utils import (
    ROOT,
    family_scoring_risks,
    load_family_figure_hints,
    policy_path,
    read_csv_rows,
    read_json,
    read_jsonl,
    read_learning_policy,
    utc_now,
    write_csv_rows,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate suggestion-only workflow optimization notes from learning outputs.")
    parser.parse_args()

    policy = read_learning_policy()
    paths = policy.get("paths") or {}
    manifest_path = policy_path(paths.get("manifest", ""), "13_prior_db/screening/pdf_manifest.csv")
    cards_path = policy_path(paths.get("prior_cards", ""), "13_prior_db/cards/prior_cards.jsonl")
    model_path = policy_path(paths.get("models", ""), "16_learning/models") / "workflow_scorers.json"
    report_path = policy_path(paths.get("reports", ""), "16_learning/reports") / "workflow_optimization_report.md"
    suggestions_path = policy_path(paths.get("reports", ""), "16_learning/reports") / "workflow_policy_suggestions.csv"
    rows = read_csv_rows(manifest_path)
    cards = read_jsonl(cards_path)
    scorer = read_json(model_path)
    if not rows:
        raise SystemExit(f"[FAIL] missing or empty manifest: {manifest_path.relative_to(ROOT)}")

    family_counts = Counter(row.get("family") or "综合集成" for row in rows)
    figure_hints = load_family_figure_hints()
    suggestion_rows: List[Dict[str, str]] = []
    now = utc_now()
    for family, count in family_counts.most_common():
        confidence = "high" if count >= 10 else "medium" if count >= 4 else "low"
        suggestion_rows.append(
            {
                "suggestion_id": f"SUG-{family}",
                "target_file": "05_model/model_family_weight_config.csv",
                "target_area": family,
                "suggestion_type": "review_weight",
                "suggestion": f"Review section weights for {family}; local corpus has {count} samples.",
                "confidence": confidence,
                "auto_apply": "false",
            }
        )
        if family in figure_hints:
            suggestion_rows.append(
                {
                    "suggestion_id": f"SUG-FIG-{family}",
                    "target_file": "08_figures/model_chart_priority_matrix.csv",
                    "target_area": family,
                    "suggestion_type": "figure_priority_review",
                    "suggestion": "Keep or review priority figures: " + "; ".join(figure_hints[family]),
                    "confidence": confidence,
                    "auto_apply": "false",
                }
            )
        suggestion_rows.append(
            {
                "suggestion_id": f"SUG-RISK-{family}",
                "target_file": "prompts/stages/11_auto_review.md",
                "target_area": family,
                "suggestion_type": "review_risk_prompt",
                "suggestion": "Reviewer should check: " + "; ".join(family_scoring_risks(family)),
                "confidence": confidence,
                "auto_apply": "false",
            }
        )

    write_csv_rows(
        suggestions_path,
        suggestion_rows,
        ["suggestion_id", "target_file", "target_area", "suggestion_type", "suggestion", "confidence", "auto_apply"],
    )

    lines = [
        "# Workflow Optimization Report",
        "",
        f"- generated_at: {now}",
        "- status: suggestion_only",
        "- auto_apply: false",
        f"- corpus_samples: {len(rows)}",
        f"- prior_cards: {len(cards)}",
        f"- scorer_available: {bool(scorer)}",
        "",
        "## Suggested Config Reviews",
        "",
    ]
    for row in suggestion_rows[:60]:
        lines.append(
            f"- [{row['confidence']}] {row['target_file']} / {row['target_area']}: {row['suggestion']}"
        )
    lines += [
        "",
        "## Guardrails",
        "",
        "- Do not apply these suggestions automatically.",
        "- Any model-route change still requires the model_route human gate.",
        "- Prior cards and scorers are advisory and cannot support paper claims directly.",
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] wrote {report_path.relative_to(ROOT)}")
    print(f"[OK] wrote {suggestions_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
