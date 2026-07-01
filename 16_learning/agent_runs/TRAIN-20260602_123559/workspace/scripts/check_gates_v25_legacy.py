from pathlib import Path
import csv
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "00_problem/problem_statement.md",
    "01_task_analysis/task_decomposition.md",
    "01_task_analysis/problem_model_profile.csv",
    "05_model/model_family_weight_config.csv",
    "08_figures/model_chart_priority_matrix.csv",
    "08_figures/visual_weight_profiles.csv",
    "08_figures/chart_blueprint.csv",
    "08_figures/visual_style_guide.md",
    "08_figures/figure_template_registry.csv",
    "08_figures/palette_library.yaml",
    "02_literature/evidence_table.csv",
    "02_literature/citation_anchor_map.csv",
    "10_ai_logs/ai_usage_log.csv",
    "10_ai_logs/ai_anchor_map.csv",
    "09_paper/paper_block_map.csv",
]


def exists_and_nonempty(rel):
    p = ROOT / rel
    return p.exists() and p.stat().st_size > 0


def csv_has_nonempty_rows(rel):
    p = ROOT / rel
    if not p.exists():
        return False, "missing"
    with p.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    nonempty = [r for r in rows if any(str(v).strip() for v in r.values())]
    return bool(nonempty), f"nonempty rows: {len(nonempty)}"


def check_weight_routing():
    profile = ROOT / "01_task_analysis/problem_model_profile.csv"
    if not profile.exists():
        return False, "problem_model_profile.csv missing"
    rows = list(csv.DictReader(profile.open("r", encoding="utf-8-sig", newline="")))
    routed = [r for r in rows if str(r.get("question", "")).strip() and str(r.get("problem_type", "")).strip() and str(r.get("model_family", "")).strip()]
    if not routed:
        return False, "problem_model_profile.csv has no filled problem_type + model_family rows"
    active = ROOT / "09_paper/active_weight_config.csv"
    if not active.exists():
        return False, "active_weight_config.csv missing; run scripts/route_weight_config.py after filling profile"
    return True, f"active weight config exists for {len(routed)} question(s)"


def check_figure_quality():
    p = ROOT / "08_figures/figure_design_review.csv"
    if not p.exists():
        return False, "figure_design_review.csv missing"
    df = pd.read_csv(p)
    if df.empty:
        return False, "no figure review rows yet"
    required = {"approved_for_main_text", "overall_score_1_5", "chinese_font_score", "non_default_palette_score", "model_fit_score", "figure_type"}
    if not required.issubset(df.columns):
        return False, f"required columns missing: {required - set(df.columns)}"
    main = df[df["approved_for_main_text"].astype(str).str.lower().isin(["true", "1", "yes", "是"])]
    low = main[pd.to_numeric(main["overall_score_1_5"], errors="coerce") < 4.2]
    bad_font = main[pd.to_numeric(main["chinese_font_score"], errors="coerce") < 4]
    bad_palette = main[pd.to_numeric(main["non_default_palette_score"], errors="coerce") < 4]
    bad_fit = main[pd.to_numeric(main["model_fit_score"], errors="coerce") < 4]
    diversity_msg = ""
    if not main.empty:
        share = main["figure_type"].value_counts(normalize=True).max()
        if share > 0.35 and len(main) >= 4:
            return False, f"figure type monopoly: max share {share:.0%} > 35%"
        diversity_msg = f", max type share {share:.0%}"
    ok = low.empty and bad_font.empty and bad_palette.empty and bad_fit.empty
    msg = f"low score: {len(low)}, font issues: {len(bad_font)}, default palette issues: {len(bad_palette)}, model-fit issues: {len(bad_fit)}{diversity_msg}"
    return ok, msg


def main():
    print("=== Gate Check ===")
    for rel in REQUIRED_FILES:
        print(f"{'OK' if exists_and_nonempty(rel) else 'MISS'}  {rel}")
    ok, msg = check_weight_routing()
    print(f"{'OK' if ok else 'WARN'}  weight routing gate: {msg}")
    ok, msg = check_figure_quality()
    print(f"{'OK' if ok else 'WARN'}  visual quality gate: {msg}")


if __name__ == "__main__":
    main()
