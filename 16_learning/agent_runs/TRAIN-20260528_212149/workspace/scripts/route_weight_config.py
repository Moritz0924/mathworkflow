from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "01_task_analysis/problem_model_profile.csv"
MODEL_CFG = ROOT / "05_model/model_family_weight_config.csv"
VISUAL_CFG = ROOT / "08_figures/visual_weight_profiles.csv"
CHART_MATRIX = ROOT / "08_figures/model_chart_priority_matrix.csv"
PRIOR_RESULTS = ROOT / "13_prior_db/screening/retrieval_results.csv"
OUT_WEIGHT = ROOT / "09_paper/active_weight_config.csv"
OUT_FIG = ROOT / "08_figures/active_figure_plan.csv"
OUT_MD = ROOT / "08_figures/active_visual_profile.md"


def read_csv_dict(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def index_by(rows, key):
    return {r[key]: r for r in rows if r.get(key)}


def first_nonempty(*values, default=""):
    for v in values:
        if v is not None and str(v).strip():
            return str(v).strip()
    return default


def load_prior_results():
    if not PRIOR_RESULTS.exists():
        return {}
    rows = read_csv_dict(PRIOR_RESULTS)
    allowed_status = {"abstracted_pass", "pass", "checked_pass"}
    grouped = {}
    for row in rows:
        status = (row.get("copy_risk_status") or "").strip()
        if status not in allowed_status:
            continue
        question = (row.get("question") or "").strip()
        if not question:
            continue
        try:
            score = float(row.get("score") or 0)
        except Exception:
            score = 0.0
        row["_score_float"] = score
        grouped.setdefault(question, []).append(row)
    for question in grouped:
        grouped[question].sort(key=lambda item: item.get("_score_float", 0), reverse=True)
    return grouped


def prior_summary(prior_rows):
    if not prior_rows:
        return "", "", ""
    top = prior_rows[0]
    card_ids = ";".join([r.get("card_id", "") for r in prior_rows[:3] if r.get("card_id")])
    source_ids = ";".join([r.get("source_ids", "") for r in prior_rows[:2] if r.get("source_ids")])
    confidence = top.get("score", "")
    return card_ids, source_ids, confidence


def main():
    profiles = read_csv_dict(PROFILE)
    model_cfg = index_by(read_csv_dict(MODEL_CFG), "model_family")
    visual_cfg = index_by(read_csv_dict(VISUAL_CFG), "problem_type")
    chart_cfg = index_by(read_csv_dict(CHART_MATRIX), "model_family")
    prior_by_question = load_prior_results()

    weight_rows = []
    fig_rows = []
    md = ["# 当前图文权重配置", ""]

    skipped = []
    for p in profiles:
        q = p.get("question", "").strip()
        if not q:
            continue
        family = p.get("model_family", "").strip()
        problem_type = p.get("problem_type", "").strip()
        if not family or not problem_type:
            skipped.append(q)
            continue
        mcfg = model_cfg.get(family, model_cfg.get("综合集成", {}))
        vcfg = visual_cfg.get(problem_type, visual_cfg.get("综合开放型", {}))
        ccfg = chart_cfg.get(family, chart_cfg.get("综合集成", {}))
        prior_rows = prior_by_question.get(q, [])
        prior_card_ids, prior_source_ids, prior_confidence = prior_summary(prior_rows)

        weight_rows.append({
            "question": q,
            "problem_type": problem_type,
            "model_family": family,
            "main_model": p.get("main_model", ""),
            "baseline_model": p.get("baseline_model", ""),
            "abstract_pct": mcfg.get("abstract_pct", ""),
            "problem_restatement_pct": mcfg.get("problem_restatement_pct", ""),
            "analysis_pct": mcfg.get("analysis_pct", ""),
            "assumption_symbol_pct": mcfg.get("assumption_symbol_pct", ""),
            "data_processing_pct": mcfg.get("data_processing_pct", ""),
            "model_building_pct": mcfg.get("model_building_pct", ""),
            "solution_pct": mcfg.get("solution_pct", ""),
            "result_analysis_pct": mcfg.get("result_analysis_pct", ""),
            "validation_pct": mcfg.get("validation_pct", ""),
            "evaluation_extension_pct": mcfg.get("evaluation_extension_pct", ""),
            "main_figures_target": mcfg.get("main_figures_target", ""),
            "main_tables_target": mcfg.get("main_tables_target", ""),
            "figure_text_ratio": mcfg.get("figure_text_ratio", ""),
            "text_weight": vcfg.get("text_weight", ""),
            "figure_weight": vcfg.get("figure_weight", ""),
            "table_weight": vcfg.get("table_weight", ""),
            "formula_weight": vcfg.get("formula_weight", ""),
            "validation_weight": vcfg.get("validation_weight", ""),
            "writing_emphasis": mcfg.get("writing_emphasis", ""),
            "prior_card_ids": prior_card_ids,
            "prior_source_ids": prior_source_ids,
            "prior_confidence": prior_confidence,
        })
        priorities = [ccfg.get(f"priority_{i}", "") for i in range(1, 6)]
        for i, ft in enumerate([x for x in priorities if x], start=1):
            fig_rows.append({
                "question": q,
                "problem_type": problem_type,
                "model_family": family,
                "priority_rank": i,
                "recommended_figure_type": ft,
                "paper_position": ["问题分析后", "模型建立处", "结果分析开头", "检验段", "总结前"][min(i-1, 4)],
                "required": "是" if i <= 3 else "建议",
                "quality_gate": ccfg.get("mandatory_check", ""),
                "prior_card_ids": prior_card_ids,
                "prior_confidence": prior_confidence,
            })
        md.append(f"## {q}")
        md.append("")
        md.append(f"- 题型：{problem_type}")
        md.append(f"- 模型族：{family}")
        md.append(f"- 主模型：{p.get('main_model', '')}")
        md.append(f"- 图文比例：{mcfg.get('figure_text_ratio', '')}")
        md.append(f"- 正文主图目标：{mcfg.get('main_figures_target', '')}")
        md.append(f"- 正文主表目标：{mcfg.get('main_tables_target', '')}")
        md.append(f"- 图表插入密度：{vcfg.get('recommended_insert_density', '')}")
        md.append(f"- 必备图类：{'；'.join([x for x in priorities[:3] if x])}")
        md.append(f"- 写作重点：{mcfg.get('writing_emphasis', '')}")
        if prior_card_ids:
            md.append(f"- Prior DB 建议卡：{prior_card_ids}")
            md.append(f"- Prior DB 置信度：{prior_confidence}")
            md.append("- Prior DB 状态：仅作 advisory 路由提示，模型选择仍需人工 gate 确认")
        md.append("")

    if not weight_rows:
        raise SystemExit("[WARN] problem_model_profile.csv 尚未填写 problem_type 和 model_family，未生成 active 配置。")
    if skipped:
        print(f"[WARN] skipped questions without routing fields: {', '.join(skipped)}")
    with OUT_WEIGHT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(weight_rows[0].keys()))
        w.writeheader(); w.writerows(weight_rows)
    if fig_rows:
        with OUT_FIG.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(fig_rows[0].keys()))
            w.writeheader(); w.writerows(fig_rows)
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"[OK] wrote {OUT_WEIGHT.relative_to(ROOT)}")
    print(f"[OK] wrote {OUT_FIG.relative_to(ROOT)}")
    print(f"[OK] wrote {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
    try:
        from workflow_utils import complete_stage, read_state
        if read_state().get("current_stage") == "model_route":
            complete_stage("model_route", "已生成模型路由后的正文权重和图表规划。请完成 Gate 2 后再进入代码生成。")
    except Exception as exc:
        print(f"[WARN] workflow_state 未更新: {exc}")
