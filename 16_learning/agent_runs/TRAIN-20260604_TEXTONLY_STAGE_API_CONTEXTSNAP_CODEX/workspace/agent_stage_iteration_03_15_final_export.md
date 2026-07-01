# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX\workspace`
Run dir: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX`
Call id: `iteration_03_15_final_export`
Iteration: 3
Max iterations: 5
Current simulated stage: `final_export`
Stage order: 15
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX/reports/prompt_route_manifest.md`
Training sandbox stage prompt bundle: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX/reports/stage_prompt_bundle.md`

Revision queue: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX\reports\agent_revision_queue.csv`

Open fail/major queue items:
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-001: Expand 12_submission/final_submit_paper.md from the latest full_draft with substantive problem analysis, model, results, validation, and conclusion sections. | acceptance: final_submit_paper.md has at least 2500 characters and at least seven sections. | notes: validation_item=training_final_paper_too_thin
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-002: Update figure_contract.csv so every result_id exists in result_contract.csv. | acceptance: Every figure result_id is present in result_contract.csv. | notes: contract_item=figure_unknown_result
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-003: Update figure_contract.csv so every result_id exists in result_contract.csv. | acceptance: Every figure result_id is present in result_contract.csv. | notes: contract_item=figure_unknown_result
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-004: Update figure_contract.csv so every result_id exists in result_contract.csv. | acceptance: Every figure result_id is present in result_contract.csv. | notes: contract_item=figure_unknown_result
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-005: Update figure_contract.csv so every result_id exists in result_contract.csv. | acceptance: Every figure result_id is present in result_contract.csv. | notes: contract_item=figure_unknown_result
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-006: Update figure_contract.csv so every result_id exists in result_contract.csv. | acceptance: Every figure result_id is present in result_contract.csv. | notes: contract_item=figure_unknown_result
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-007: Update figure_contract.csv so every result_id exists in result_contract.csv. | acceptance: Every figure result_id is present in result_contract.csv. | notes: contract_item=figure_unknown_result
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-008: Bind each active claim to an existing result_id, figure_id, formula_id, citation_id, or evidence_ref. | acceptance: validate_contracts.py no longer reports unsupported_claim for claim_evidence_map.csv. | notes: contract_item=unsupported_claim
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-009: Resolve contract validation failure polish_changed_protected_atom: POL-000 protected_atom_delta_count=0, decision=blocked | acceptance: validate_contracts.py no longer reports polish_changed_protected_atom. | notes: contract_item=polish_changed_protected_atom

Rules:
- Follow only deep_sequential behavior for this stage.
- Do not edit `00_problem/problem_statement.md` or `00_problem/inbox/`; write intake analysis to `01_task_analysis/`.
- A formal human gate becomes a simulated sandbox gate. Record it in `11_review/simulated_human_gate_log.csv`.
- Update contracts before writing paper claims, result analysis, figures, or submission text.
- Use the Workspace Context Snapshot below as the current file context; do not request read_file/list_files pseudo-tools.
- Reply only through runner file actions. The external runner will reject prose-only or pseudo-tool responses.

Stage output target:
- Create or update the artifacts normally owned by `final_export`.
- If this stage cannot close a blocker, update review/revision artifacts with a concrete blocker note.
- Keep `reports/training_enhancement_points.csv` current once a full draft or review finding exists.

Stage-specific required outputs:
- Write `12_submission/final_submit_paper.md` as the submit-ready paper text copied or assembled from `09_paper/full_draft.md` after contracts exist.
- The final submit paper must preserve the latest full_draft topic markers, especially T01/T02/T03, RGB, and concentration; do not replace it with a generic paper.
- If `09_paper/full_draft.md` changed in the same iteration, final_export must refresh `12_submission/final_submit_paper.md` from that latest draft.
- Write `12_submission/final_submit_package.md` with included artifacts and residual risks.
- Write `reports/training_enhancement_points.csv` and `.md`; CSV must include at least one target_area each of system, prompt, and gate.
- Ensure simulated gate log has at least four rows and formal_effect is `none` for every row.

# Workspace Context Snapshot

This bounded snapshot is the API agent's read context for the current stage. Use it instead of pseudo-tools or file-read requests.

## Workspace File Listing

- 07_results/.gitkeep (0 bytes)
- 07_results/cv_results.csv (23 bytes)
- 07_results/logs/.gitkeep (0 bytes)
- 07_results/logs/generate_latex_template.log (152 bytes)
- 07_results/logs/q1_run.log (421 bytes)
- 07_results/metrics/.gitkeep (0 bytes)
- 07_results/metrics_summary.csv (92 bytes)
- 07_results/q1_coefficients.csv (77 bytes)
- 07_results/q1_metrics.csv (49 bytes)
- 07_results/q1_results.csv (74 bytes)
- 07_results/q1_stats.csv (142 bytes)
- 07_results/q2_comparison.csv (136 bytes)
- 07_results/q2_results.csv (74 bytes)
- 07_results/q3_predictions.csv (101 bytes)
- 07_results/q3_results.csv (74 bytes)
- 07_results/result_freeze_report.md (3917 bytes)
- 07_results/result_source_map.csv (201 bytes)
- 07_results/tables/.gitkeep (0 bytes)
- 08_figures/appendix_figures/.gitkeep (0 bytes)
- 08_figures/chart_blueprint.csv (962 bytes)
- 08_figures/chart_type_library.md (1653 bytes)
- 08_figures/eda_figures/.gitkeep (0 bytes)
- 08_figures/export/pdf_vector/.gitkeep (0 bytes)
- 08_figures/export/png_300dpi/.gitkeep (0 bytes)
- 08_figures/export/svg_vector/.gitkeep (0 bytes)
- 08_figures/figure_caption_bank.md (2285 bytes)
- 08_figures/figure_design_review.csv (834 bytes)
- 08_figures/figure_status.csv (356 bytes)
- 08_figures/figure_template_registry.csv (2006 bytes)
- 08_figures/figure_text_balance_rules.md (1829 bytes)
- 08_figures/figure_version_compare.md (131 bytes)
- 08_figures/graphviz/.gitkeep (0 bytes)
- 08_figures/graphviz/model_mechanism.dot (183 bytes)
- 08_figures/main_figures/.gitkeep (0 bytes)
- 08_figures/main_figures/F001_coefficient_bar.svg (1763 bytes)
- 08_figures/main_figures/F002_pred_vs_actual.svg (1607 bytes)
- 08_figures/main_figures/F003_resid_fitted.svg (1378 bytes)
- 08_figures/main_figures/F004_qq_resid.svg (1279 bytes)
- 08_figures/main_figures/F005_channel_scatter.svg (2269 bytes)
- 08_figures/main_figures/F006_correlation_heatmap.svg (2910 bytes)
- 08_figures/main_figures/F007_model_comparison.svg (1442 bytes)
- 08_figures/main_figures/F008_prediction_intervals.svg (2128 bytes)
- 08_figures/mermaid/.gitkeep (0 bytes)
- 08_figures/mermaid/workflow_map.mmd (284 bytes)
- 08_figures/model_chart_priority_matrix.csv (1558 bytes)
- 08_figures/output/.gitkeep (0 bytes)
- 08_figures/palette_library.yaml (1500 bytes)
- 08_figures/scripts/generate_figures.py (2986 bytes)
- 08_figures/templates/.gitkeep (0 bytes)
- 08_figures/templates/geopandas_map_template.py (962 bytes)
- 08_figures/templates/graphviz_mechanism_template.dot (267 bytes)
- 08_figures/templates/matplotlib_publication.py (2328 bytes)
- 08_figures/templates/mermaid_flow_template.mmd (183 bytes)
- 08_figures/templates/networkx_template.py (1718 bytes)
- 08_figures/templates/plotly_interactive.py (994 bytes)
- 08_figures/templates/publication_advanced.py (6039 bytes)
- 08_figures/templates/seaborn_publication.py (1148 bytes)
- 08_figures/visual_style_guide.md (2261 bytes)
- 08_figures/visual_weight_profiles.csv (841 bytes)
- 09_paper/.gitkeep (0 bytes)
- 09_paper/ai_style_risk_check.md (337 bytes)
- 09_paper/ai_superscript_insert_list.csv (93 bytes)
- 09_paper/anchor_consistency_check.md (440 bytes)
- 09_paper/citation_insert_list.csv (97 bytes)
- 09_paper/consistency_risk_report.md (3977 bytes)
- 09_paper/draft_sec_q1_model.md (4218 bytes)
- 09_paper/draft_v1.md (120 bytes)
- 09_paper/draft_v1_with_anchors.md (145 bytes)
- 09_paper/draft_v2.md (123 bytes)
- 09_paper/draft_v2_polished.md (132 bytes)
- 09_paper/dynamic_outline_router.md (1711 bytes)
- 09_paper/figure_insert_list.csv (83 bytes)
- 09_paper/final_paper.md (117 bytes)
- 09_paper/formatting_checklist.md (260 bytes)
- 09_paper/frozen_text_blocks.md (170 bytes)
- 09_paper/full_draft.md (11949 bytes)
- 09_paper/human_rewrite_log.md (139 bytes)
- 09_paper/missing_evidence_report.md (1455 bytes)
- 09_paper/outline.md (728 bytes)
- 09_paper/paper_block_map.csv (245 bytes)
- 09_paper/paper_draft_stage_summary.md (1032 bytes)
- 09_paper/paper_full_stage_summary.md (4631 bytes)
- 09_paper/polish_diff_log.md (144 bytes)
- 09_paper/polish_plan.md (237 bytes)
- 09_paper/polish_tasks.csv (232 bytes)
- 09_paper/section_weight_profiles.csv (2354 bytes)
- 09_paper/unresolved_review_issues.md (855 bytes)
- 11_review/.gitkeep (0 bytes)
- 11_review/auto_review_stage_summary.md (793 bytes)
- 11_review/code_reviewer_comments.md (591 bytes)
- 11_review/compile_stage_summary.md (528 bytes)
- 11_review/contract_validation_report.json (4091 bytes)
- 11_review/contract_validation_report.md (2245 bytes)
- 11_review/figure_reviewer_comments.md (691 bytes)
- 11_review/figures_stage_summary.md (1724 bytes)
- 11_review/final_export_blocker_note.md (744 bytes)
- 11_review/final_submission_checklist.md (206 bytes)
- 11_review/gate_report.json (111 bytes)
- 11_review/judge_reviewer_comments.md (533 bytes)
- 11_review/latex_template_stage_summary.md (331 bytes)
- 11_review/model_reviewer_comments.md (717 bytes)
- 11_review/paper_full_stage_summary.md (1302 bytes)
- 11_review/paper_reviewer_comments.md (662 bytes)
- 11_review/polish_blocker_note.md (952 bytes)
- 11_review/prior_copy_risk_report.md (196 bytes)
- 11_review/prior_retrieval_stage_summary.md (969 bytes)
- 11_review/problem_reviewer_comments.md (520 bytes)
- 11_review/review_scorecard.csv (896 bytes)
- 11_review/revision_stage_summary.md (1620 bytes)
- 11_review/revision_tasks.csv (5450 bytes)
- 11_review/simulated_human_gate_log.csv (1047 bytes)
- 11_review/skill_router_report.json (5728 bytes)
- 11_review/skill_router_report.md (356 bytes)
- 11_review/unresolved_review_issues.md (1854 bytes)
- 12_submission/ai_usage_detail.pdf (2757 bytes)
- 12_submission/code_package/.gitkeep (0 bytes)
- 12_submission/data_package/.gitkeep (0 bytes)
- 12_submission/figure_package/.gitkeep (0 bytes)
- 12_submission/final_submit_package.md (2102 bytes)
- 12_submission/final_submit_paper.md (11947 bytes)
- [truncated after 120 files]

## 00_problem/problem_statement.md

```text
# 颜色与物质浓度的辨识问题

> 沙盒训练题面。题目方向取自本地题库文件名：
> `论文数据集/1/多元回归/颜色与物质浓度的辨识问题 .PDF`。
> 本文件不复制历史论文正文、摘要、图注、表格或结论。

某检测设备对不同浓度溶液进行拍摄和预处理后，输出三个归一化颜色通道 `R`、`G`、`B`。现在给出若干标准样本的真实浓度和颜色读数，以及若干待测样本的颜色读数。请建立数学模型识别待测样本的物质浓度。

## 已知标准样本

| sample_id | concentration_mg_L | R | G | B |
|---|---:|---:|---:|---:|
| S01 | 0.5 | 0.91 | 0.23 | 0.18 |
| S02 | 1.0 | 0.85 | 0.29 | 0.21 |
| S03 | 1.5 | 0.79 | 0.35 | 0.26 |
| S04 | 2.0 | 0.72 | 0.42 | 0.31 |
| S05 | 2.5 | 0.66 | 0.49 | 0.37 |
| S06 | 3.0 | 0.60 | 0.55 | 0.43 |
| S07 | 3.5 | 0.54 | 0.61 | 0.50 |
| S08 | 4.0 | 0.49 | 0.67 | 0.57 |
| S09 | 4.5 | 0.43 | 0.72 | 0.63 |
| S10 | 5.0 | 0.39 | 0.76 | 0.69 |

## 待测样本

| sample_id | R | G | B |
|---|---:|---:|---:|
| T01 | 0.77 | 0.37 | 0.28 |
| T02 | 0.58 | 0.57 | 0.46 |
| T03 | 0.45 | 0.70 | 0.61 |

## 问题一

分析颜色通道与物质浓度之间的关系，建立一个可解释的浓度预测模型，并说明各颜色通道对浓度识别的作用方向。

## 问题二

比较至少三类候选模型的预测误差，例如线性回归、多项式回归、集成回归或其他合理模型。请给出模型选择依据，并说明如何控制小样本过拟合风险。

## 问题三

预测待测样本 `T01`、`T02`、`T03` 的浓度，给出不确定性说明，并提出可复用的检测流程建议。

## 硬性要求

- 本题不使用图片输入。
- 所有数值结果必须能追溯到结果合同。
- 图表引用必须先登记到图表合同。
- 不得复制题库中历史论文文本。
```

## reports/agent_revision_queue.csv

```text
﻿task_id,run_id,iteration,severity,target_artifact,issue_summary,proposed_action,acceptance_check,status,human_decision,notes
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-001,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,validation,fail,E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX\workspace\12_submission\final_submit_paper.md,"chars=5803, sections=6","Expand 12_submission/final_submit_paper.md from the latest full_draft with substantive problem analysis, model, results, validation, and conclusion sections.",final_submit_paper.md has at least 2500 characters and at least seven sections.,open,,validation_item=training_final_paper_too_thin
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-002,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,contract_validation,fail,14_contracts/figure_contract.csv,F001 references missing result_id=R01;R02;R03;R04,Update figure_contract.csv so every result_id exists in result_contract.csv.,Every figure result_id is present in result_contract.csv.,open,,contract_item=figure_unknown_result
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-003,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,contract_validation,fail,14_contracts/figure_contract.csv,F002 references missing result_id=R05;R06,Update figure_contract.csv so every result_id exists in result_contract.csv.,Every figure result_id is present in result_contract.csv.,open,,contract_item=figure_unknown_result
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-004,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,contract_validation,fail,14_contracts/figure_contract.csv,F003 references missing result_id=R05;R06,Update figure_contract.csv so every result_id exists in result_contract.csv.,Every figure result_id is present in result_contract.csv.,open,,contract_item=figure_unknown_result
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-005,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,contract_validation,fail,14_contracts/figure_contract.csv,F004 references missing result_id=R05;R06,Update figure_contract.csv so every result_id exists in result_contract.csv.,Every figure result_id is present in result_contract.csv.,open,,contract_item=figure_unknown_result
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-006,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,contract_validation,fail,14_contracts/figure_contract.csv,F007 references missing result_id=R07;R08;R09,Update figure_contract.csv so every result_id exists in result_contract.csv.,Every figure result_id is present in result_contract.csv.,open,,contract_item=figure_unknown_result
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-007,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,contract_validation,fail,14_contracts/figure_contract.csv,F008 references missing result_id=R10;R11;R12;R13;R14;R15;R16;R17;R18,Update figure_contract.csv so every result_id exists in result_contract.csv.,Every figure result_id is present in result_contract.csv.,open,,contract_item=figure_unknown_result
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-008,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,contract_validation,fail,14_contracts/claim_evidence_map.csv,C06 references missing citation_id=moderate,"Bind each active claim to an existing result_id, figure_id, formula_id, citation_id, or evidence_ref.",validate_contracts.py no longer reports unsupported_claim for claim_evidence_map.csv.,open,,contract_item=unsupported_claim
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-009,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,contract_validation,fail,14_contracts/polish_diff_check.csv,"POL-000 protected_atom_delta_count=0, decision=blocked","Resolve contract validation failure polish_changed_protected_atom: POL-000 protected_atom_delta_count=0, decision=blocked",validate_contracts.py no longer reports polish_changed_protected_atom.,open,,contract_item=polish_changed_protected_atom
```

## reports/gap_report.csv

```text
﻿gap_id,dimension,severity,benchmark_source_id,evidence_summary,our_artifact,recommended_change,acceptance_check,status,human_decision
```

## reports/full_gap_report.md

```text
# Agent Training Gap Report

- run_id: TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX
- draft: 16_learning/agent_runs/TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX/workspace/09_paper/full_draft.md
- draft_status: existing
- benchmark_source: local prior DB

## Benchmark Sources

- SRCad03b2fb65cc | 预测回归 | 多元回归 | card=CARD60dd60d8f596 | score=0.321341
- SRCfb178d4139ba | 预测回归 | 多元回归 | card=CARD60dd60d8f596 | score=0.321341
- SRC4225edb1178d | 预测回归 | 多元回归 | card=CARD60dd60d8f596 | score=0.321341

## Feature Comparison

| metric | sandbox | benchmark_average |
|---|---:|---:|
| chars | 5804 | 30069.67 |
| sections | 17 | 0.00 |
| figure_mentions | 13 | 4.33 |
| table_mentions | 8 | 13.67 |
| formula_mentions | 3 | 1.67 |
| validation_mentions | 36 | 44.67 |
| citation_mentions | 9 | 11.00 |

## Gap Findings

- No major structural gap found by the lightweight benchmark checks.

## Safety

- This report compares counts, structure signals, and risk patterns only.
- It intentionally does not copy prior-paper text, abstracts, captions, tables, or conclusions.
- Any promotion into the formal workflow must go through contracts, review tasks, and human gates.
```

## 14_contracts/result_contract.csv

```text
result_id,question_id,model_id,metric_name,metric_value,unit,source_file,source_row_or_cell,code_file,run_id,random_seed,assumption_ids,used_by_figure_ids,used_by_claim_ids,freeze_status,freeze_time,owner,notes
R01,Q1,linear_OLS,coefficient_Intercept,1.067247,dimensionless,07_results/q1_coefficients.csv,row 1,06_code/q1_linear_model.py,run_001,deterministic,F01,,,frozen,2026-06-04T12:00:00Z,system,validated source value 1.067247 from q1_coefficients.csv row 1; OLS intercept coefficient
R02,Q1,linear_OLS,coefficient_R,-1.821404,dimensionless,07_results/q1_coefficients.csv,row 2,06_code/q1_linear_model.py,run_001,deterministic,F01,,,frozen,2026-06-04T12:00:00Z,system,validated source value -1.821404 from q1_coefficients.csv row 2; R channel coefficient
R03,Q1,linear_OLS,coefficient_G,0.995618,dimensionless,07_results/q1_coefficients.csv,row 3,06_code/q1_linear_model.py,run_001,deterministic,F01,,,frozen,2026-06-04T12:00:00Z,system,validated source value 0.995618 from q1_coefficients.csv row 3; G channel coefficient
R04,Q1,linear_OLS,coefficient_B,5.630987,dimensionless,07_results/q1_coefficients.csv,row 4,06_code/q1_linear_model.py,run_001,deterministic,F01,,,frozen,2026-06-04T12:00:00Z,system,validated source value 5.630987 from q1_coefficients.csv row 4; B channel coefficient
R05,Q1,linear_OLS,R_squared,0.997747,dimensionless,07_results/q1_metrics.csv,row 1,06_code/q1_linear_model.py,run_001,deterministic,F01,,,frozen,2026-06-04T12:00:00Z,system,validated source value 0.997747 from q1_metrics.csv row 1; OLS R-squared
R06,Q1,linear_OLS,RMSE,0.067418,mg/L,07_results/q1_metrics.csv,row 2,06_code/q1_linear_model.py,run_001,deterministic,F01,,,frozen,2026-06-04T12:00:00Z,system,validated source value 0.067418 from q1_metrics.csv row 2; OLS RMSE
R07,Q2,linear_OLS,CV_RMSE_LOOCV,0.0748,mg/L,07_results/q2_comparison.csv,row 1,06_code/q2_model_comparison.py,run_002,deterministic,,,,frozen,2026-06-04T14:00:00Z,system,LOOCV cross-validated RMSE for linear OLS
R08,Q2,polynomial_degree2,CV_RMSE_LOOCV,0.347,mg/L,07_results/q2_comparison.csv,row 2,06_code/q2_model_comparison.py,run_002,deterministic,,,,frozen,2026-06-04T14:00:00Z,system,Polynomial degree-2 interaction model LOOCV RMSE; overfitting evident
R09,Q2,ridge,CV_RMSE_LOOCV,0.098,mg/L,07_results/q2_comparison.csv,row 3,06_code/q2_model_comparison.py,run_002,deterministic,,,,frozen,2026-06-04T14:00:00Z,system,Ridge regression (alpha=0.1) LOOCV RMSE
R10,Q3,linear_OLS,prediction_T01,1.61,mg/L,07_results/q3_predictions.csv,row 1,06_code/q3_uncertainty.py,run_002,deterministic,,,,frozen,2026-06-04T14:00:00Z,system,Point prediction for T01
R11,Q3,linear_OLS,lower_95PI_T01,1.35,mg/L,07_results/q3_predictions.csv,row 1,06_code/q3_uncertainty.py,run_002,deterministic,,,,frozen,2026-06-04T14:00:00Z,system,Lower bound of 95% prediction interval for T01
R12,Q3,linear_OLS,upper_95PI_T01,1.87,mg/L,07_results/q3_predictions.csv,row 1,06_code/q3_uncertainty.py,run_002,deterministic,,,,frozen,2026-06-04T14:00:00Z,system,Upper bound of 95% PI for T01
R13,Q3,linear_OLS,prediction_T02,3.17,mg/L,07_results/q3_predictions.csv,row 2,06_code/q3_uncertainty.py,run_002,deterministic,,,,frozen,2026-06-04T14:00:00Z,system,Point prediction for T02
R14,Q3,linear_OLS,lower_95PI_T02,2.90,mg/L,07_results/q3_predictions.csv,row 2,06_code/q3_uncertainty.py,run_002,deterministic,,,,frozen,2026-06-04T14:00:00Z,system,Lower bound of 95% PI for T02
R15,Q3,linear_OLS,upper_95PI_T02,3.44,mg/L,07_results/q3_predictions.csv,row 2,06_code/q3_uncertainty.py,run_002,deterministic,,,,frozen,2026-06-04T14:00:00Z,system,Upper bound of 95% PI for T02
R16,Q3,linear_OLS,prediction_T03,4.38,mg/L,07_results/q3_predictions.csv,row 3,06_code/q3_uncertainty.py,run_002,deterministic,,,,frozen,2026-06-04T14:00:00Z,system,Point prediction for T03
R17,Q3,linear_OLS,lower_95PI_T03,4.10,mg/L,07_results/q3_predictions.csv,row 3,06_code/q3_uncertainty.py,run_002,deterministic,,,,frozen,2026-06-04T14:00:00Z,system,Lower bound of 95% PI for T03
R18,Q3,linear_OLS,upper_95PI_T03,4.66,mg/L,07_results/q3_predictions.csv,row 3,06_code/q3_uncertainty.py,run_002,deterministic,,,,frozen,2026-06-04T14:00:00Z,system,Upper bound of 95% PI for T03
R19,Q1,linear_OLS,SE_Intercept,0.05,dimensionless,07_results/q1_stats.csv,row 1,06_code/q3_uncertainty.py,run_002,deterministic,,,,frozen,2026-06-04T14:00:00Z,system,Standard error of intercept
R20,Q1,linear_OLS,SE_R,0.08,dimensionless,07_results/q1_stats.csv,row 2,06_code/q3_uncertainty.py,run_002,deterministic,,,,frozen,2026-06-04T14:00:00Z,system,Standard error of R coefficient
R21,Q1,linear_OLS,SE_G,0.15,dimensionless,07_results/q1_stats.csv,row 3,06_code/q3_uncertainty.py,run_002,deterministic,,,,frozen,2026-06-04T14:00:00Z,system,Standard error of G coefficient
R22,Q1,linear_OLS,SE_B,0.20,dimensionless,07_results/q1_stats.csv,row 4,06_code/q3_uncertainty.py,run_002,deterministic,,,,frozen,2026-06-04T14:00:00Z,system,Standard error of B coefficient
```

## 14_contracts/claim_evidence_map.csv

```text
claim_id,question_id,section_id,claim_text,claim_type,evidence_type,evidence_id,result_id,figure_id,formula_id,citation_id,support_grade,boundary_condition,risk_note,status,owner,last_checked
C01,Q1,sec_model,线性回归模型能够以极高拟合优度（R²=0.9977）描述浓度与RGB通道的关系,result,result,R05;R06,R05;R06,F002,F01,,strong,对于标准样本范围(0.5—5.0 mg/L)成立；外推需谨慎,,draft,system,
C02,Q1,sec_model,R通道与浓度呈现负相关（系数-1.8214），表明红色分量增加导致预测浓度降低,result,result,R02,R02,F001;F005,,,strong,,,draft,system,
C03,Q1,sec_model,G通道与浓度呈现弱正相关（系数0.9956），其影响幅度小于B通道,result,result,R03,R03,F001;F005,,,moderate,G通道系数置信区间需进一步考察,,draft,system,
C04,Q1,sec_model,B通道是浓度预测的主导正向因子（系数5.6310），显示蓝色分量对浓度变化的响应最强烈,result,result,R04,R04,F001;F005,,,strong,,,draft,system,
C05,Q1,sec_diagnostics,残差图未显示系统模式，残差近似满足正态性和同方差性，支持OLS假设,figure,figure,F003;F004,,F003;F004,,,moderate,样本量仅10个，诊断统计效力有限,,draft,system,
C06,Q1,sec_diagnostics,模型RMSE为0.0674 mg/L，表明预测误差在可接受范围,result,result,R06,R06,,,moderate,相对误差需结合浓度范围评估,,draft,system,
```

## 14_contracts/figure_contract.csv

```text
figure_id,question_id,core_claim,evidence_source,result_id,panel_plan,chart_type,backend,script_path,output_svg,output_png,output_pdf,dpi,used_in_section,latex_label,caption_source,quality_score,review_risk,status,owner,last_checked,title_cn,caption_cn,notes
F001,Q1,OLS系数估计值与方向,07_results/q1_coefficients.csv,R01;R02;R03;R04,单图,bar,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F001_coefficient_bar.svg,,,300,sec_model,fig:coef,figure_caption_bank.md,4.5,font_risk,active,system,,OLS系数估计值与方向,"多元线性回归模型各变量系数估计值，反映各颜色通道对浓度的作用方向和大小。",所有result_id均存在于result_contract.csv; 使用非默认配色; 文字为中文
F002,Q1,模型预测值与真实值对比,基于冻结系数和标准样本数据,R05;R06,单图,scatter,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F002_pred_vs_actual.svg,,,300,sec_results,fig:pred_actual,figure_caption_bank.md,4.5,font_risk,active,system,,预测浓度与真实浓度对比,"模型预测值与标准样本真实浓度的散点图，显示模型拟合精度。",所有result_id均存在于result_contract.csv
F003,Q1,残差同方差性检验,残差计算,R05;R06,单图,scatter,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F003_resid_fitted.svg,,,300,sec_diagnostics,fig:resid_fitted,figure_caption_bank.md,4.5,font_risk,active,system,,残差-拟合值图,"残差对拟合值的散点图，用于检验同方差性假设。",所有result_id均存在于result_contract.csv
F004,Q1,残差正态性检验,残差计算,R05;R06,单图,qq,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F004_qq_resid.svg,,,300,sec_diagnostics,fig:qq,figure_caption_bank.md,4.5,font_risk,active,system,,残差Q-Q图,"残差分位数-理论分位数图，检验残差正态性。",所有result_id均存在于result_contract.csv
F005,Q1,浓度与各通道线性关系,标准样本数据表,,一组散点图,scatter_matrix,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F005_channel_scatter.svg,,,300,sec_model,fig:scatter_matrix,figure_caption_bank.md,4.2,font_risk,active,system,,浓度与各颜色通道散点矩阵,"浓度与R、G、B通道的散点图矩阵，展示线性关系。",使用non-default配色
F006,Q1,变量相关性热力图,标准样本数据表,,单图,heatmap,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F006_correlation_heatmap.svg,,,300,sec_model,fig:corr_heat,figure_caption_bank.md,4.2,font_risk,active,system,,变量相关性热力图,"浓度及RGB通道之间的Pearson相关系数热力图。",
F007,Q2,模型对比交叉验证RMSE,07_results/q2_comparison.csv,R07;R08;R09,单图,bar,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F007_model_comparison.svg,,,300,sec_model_comparison,fig:model_cmp,figure_caption_bank.md,4.5,font_risk,active,system,,三种模型留一交叉验证RMSE对比,"线性回归、多项式回归、岭回归三种模型的留一交叉验证RMSE对比图。",所有result_id均存在于result_contract.csv; 新增图表
F008,Q3,预测区间可视化,07_results/q3_predictions.csv,R10;R11;R12;R13;R14;R15;R16;R17;R18,单图,errorbar,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F008_prediction_intervals.svg,,,300,sec_predictions,fig:pred_intervals,figure_caption_bank.md,4.5,font_risk,active,system,,待测样本预测浓度及95%预测区间,"T01、T02、T03的点预测值和95%预测区间，显示不确定性范围。",所有result_id均存在于result_contract.csv; 新增图表
```

## 14_contracts/formula_contract.csv

```text
formula_id,question_id,section_id,formula_latex,symbols_defined,assumption_ids,derivation_source,used_in_section,latex_label,depends_on_formula_ids,validation_note,status,owner,last_checked
F01,Q1,sec_model,"C = \beta_0 + \beta_1 R + \beta_2 G + \beta_3 B + \varepsilon","C: concentration; R,G,B: color channels; \beta_i: regression coefficients; \varepsilon: error term","linearity, independence, homoscedasticity, normality of errors",derived from OLS theory,main model section,eq:linear_model,,to be estimated via statsmodels OLS,draft,system,
F02,Q2,sec_comparison,"C = \beta_0 + \sum_{i=1}^3 \beta_i X_i + \sum_{i=1}^3 \beta_{ii} X_i^2 + \sum_{i<j} \beta_{ij} X_i X_j + \varepsilon","X_1=R, X_2=G, X_3=B; \beta: coefficients; \varepsilon: error term","polynomial of degree 2, includes interactions",standard polynomial regression,model comparison section,eq:poly2,,will implement with PolynomialFeatures from sklearn,draft,system,
F03,Q2,sec_comparison,"RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^n (C_i - \hat{C}_i)^2}","C_i: true concentration; \hat{C}_i: predicted concentration; n: sample size",,"standard metric",model evaluation,eq:rmse,,used for cross-validation,draft,system,
```

## 11_review/review_scorecard.csv

```text
round_id,reviewer,dimension,score,max_score,severity,issue_count,top_risk,required_action,status,last_checked
2,problem_reviewer,Problem Coverage,10,10,none,0,None,None,closed,2026-06-04T16:00:00Z
2,model_reviewer,Model Rigor,10,10,none,0,None,None,closed,2026-06-04T16:00:00Z
2,code_reviewer,Code Reproducibility,9,10,minor,1,Insufficient code documentation,Add docstrings and inline comments to Python scripts,open,2026-06-04T16:00:00Z
2,figure_reviewer,Figure Quality,9,10,minor,1,Chinese font rendering unverified,Verify font rendering in generated SVGs; regenerate if needed,open,2026-06-04T16:00:00Z
2,paper_reviewer,Writing & Argumentation,9,10,minor,1,Minor language polish,Perform final language polish pass,open,2026-06-04T16:00:00Z
2,judge_reviewer,Overall Judgment,9,10,minor,3,Minor tasks remain,Address the three minor tasks before final submission,open,2026-06-04T16:00:00Z
```

## 11_review/revision_tasks.csv

```text
task_id,round_id,reviewer,source_comment_id,severity,scope,target_artifact,target_location,issue_summary,required_action,acceptance_check,linked_contract_ids,status,assignee,created_time,closed_time,closure_note,human_waiver_by
RV-001,1,problem_reviewer,PRC-4;PRC-5;MRC-6;MRC-7;MRC-8;CRC-4,fail,code; results; paper,06_code/q2_model_comparison.py; 07_results/q2_comparison.csv; 09_paper/full_draft.md,Section 2.2; Section 4,Problem 2 requires comparison of at least three model types (linear polynomial regularized) with predictive error metrics and overfitting control discussion. Currently no code results or quantitative comparison exists.,Implement code to fit and compare: (1) OLS linear regression (2) 2nd-order polynomial regression with interactions (3) ridge or LASSO regression. Use LOOCV to compute RMSE for each. Report comparison table with RMSE AIC BIC. Discuss overfitting risk and justify chosen model.,1) 07_results/q2_comparison.csv exists and contains RMSE for all three models; 2) Paper Section 2.2 includes actual numerical comparison and model selection rationale; 3) New results registered in result_contract.csv; 4) Paper discusses overfitting control strategy.,F02;F03,open,system,2026-06-04T12:30:00Z,,,
RV-002,1,problem_reviewer,PRC-7;MRC-4;CRC-5;JRC-1,fail,code; results; paper,06_code/q3_uncertainty.py; 09_paper/full_draft.md,Section 2.3; Section 3.3; Section 5,Problem 3 requires uncertainty quantification for predictions (e.g. prediction intervals) and a reusable measurement protocol. Currently only point predictions are provided without intervals or protocol.,1) Extract coefficient standard errors and residual standard deviation from OLS; construct 95% prediction intervals for T01-T03. 2) Optionally apply bootstrap to validate intervals. 3) Write a measurement protocol section describing sample preparation imaging channel normalization model calibration and prediction steps.,1) Paper includes prediction intervals (e.g. 95% PI) for T01-T03; 2) New result entries in result_contract.csv for intervals; 3) Paper contains a clear Reusable Measurement Protocol subsection.,F01,open,system,2026-06-04T12:30:00Z,,,
RV-003,1,problem_reviewer,PRC-8,major,contracts,14_contracts/result_contract.csv,new rows for predictions and intervals,Predicted concentrations for T01-T03 and future uncertainty statistics are not registered in result_contract.csv violating contract traceability.,Add result rows for: predicted values of T01 T02 T03; prediction interval lower/upper bounds; any new metrics (e.g. LOOCV RMSE).,result_contract.csv contains at least 5 new rows (3 predictions plus lower/upper bounds or other).,,open,system,2026-06-04T12:30:00Z,,,
RV-004,1,model_reviewer,MRC-4;MRC-5,major,results; paper,07_results/q1_metrics.csv (or new); 09_paper/full_draft.md,Table 1; Section 2.1,Coefficient standard errors t-values and p-values are not reported making it impossible to judge statistical significance.,Extract standard errors t-stats p-values from the OLS summary (statsmodels). Record them and update Table 1.,Table 1 includes columns for Std. Error; t; p-value. The text discusses significance of each coefficient.,F01,open,system,2026-06-04T12:30:00Z,,,
RV-005,1,model_reviewer,MRC-9;PRC-5,major,code; results; paper,06_code/cross_validation.py; 07_results/cv_results.csv; 09_paper/full_draft.md,Section 4,No cross-validation or sensitivity analysis has been performed; current high R² may be due to overfitting.,Implement LOOCV or 5-fold CV for the linear model; report CV RMSE. Optionally perform bootstrap for coefficient distributions. Update Section 4.,Paper Section 4 includes cross-validation RMSE and coefficient bootstrap confidence intervals; results are registered.,F01,open,system,2026-06-04T12:30:00Z,,,
RV-006,1,paper_reviewer,PaRC-7;PaRC-8,major,paper; contracts,14_contracts/citation_contract.csv; 09_paper/full_draft.md,References section; appropriate locations,No references are cited in the paper and citation_contract.csv is not established.,Identify and cite at least 3-5 relevant works; add cite commands and reference list; populate citation_contract.csv.,citation_contract.csv contains at least 3 valid entries; paper includes in-text citations and a reference list.,,open,system,2026-06-04T12:30:00Z,,,
RV-007,1,figure_reviewer,FRC-3;FRC-6,minor,figures,08_figures/main_figures/*.svg; 08_figures/scripts/generate_figures.py,all figure SVGs,Figures are marked with font_risk; Chinese characters may not render correctly. Figure captions lack details.,Configure matplotlib for Chinese font; regenerate SVGs; verify rendering; write comprehensive figure captions.,Figures display Chinese labels correctly; each has descriptive caption.,,open,system,2026-06-04T12:30:00Z,,,
RV-008,1,paper_reviewer,PaRC-5;PaRC-6,minor,paper,09_paper/full_draft.md,Section 5 Conclusions,Conclusions use overly definitive language despite small sample size and incomplete validation.,Reword conclusions to add hedging phrases.,Conclusion paragraphs inclu
[truncated to 5000 chars]
```

## 14_contracts/revision_tasks.csv

```text
task_id,round_id,reviewer,source_comment_id,severity,scope,target_artifact,target_location,issue_summary,required_action,acceptance_check,linked_contract_ids,status,assignee,created_time,closed_time,closure_note,human_waiver_by
RV-001,1,problem_reviewer,PRC-4;PRC-5;MRC-6;MRC-7;MRC-8;CRC-4,fail,code; results; paper,06_code/q2_model_comparison.py; 07_results/q2_comparison.csv; 09_paper/full_draft.md,Section 2.2; Section 4,Problem 2 required model comparison and overfitting discussion. Now implemented with three models and LOOCV.,Already completed,1) q2_comparison.csv exists with RMSE for all three models; 2) Paper includes comparison and rationale; 3) Results R07-R09 registered; 4) Overfitting discussion present.,F02;F03,closed,system,2026-06-04T12:30:00Z,2026-06-04T16:00:00Z,Code and results present; paper updated with comparison and overfitting strategy.,
RV-002,1,problem_reviewer,PRC-7;MRC-4;CRC-5;JRC-1,fail,code; results; paper,06_code/q3_uncertainty.py; 09_paper/full_draft.md,Section 2.3; Section 3.3; Section 5,Problem 3 required uncertainty quantification and reusable protocol. Now implemented with 95% PI and protocol section.,Already completed,1) Paper includes 95% PI for T01-T03; 2) Results R10-R18 registered; 3) Reusable protocol subsection present.,F01,closed,system,2026-06-04T12:30:00Z,2026-06-04T16:00:00Z,Code and predictions generated; protocol written and results registered.,
RV-003,1,problem_reviewer,PRC-8,major,contracts,14_contracts/result_contract.csv,new rows for predictions and intervals,Result contract lacked prediction rows. Now contains R07-R22 covering predictions intervals and metrics.,Add missing result rows,result_contract.csv contains new rows for predictions intervals CV RMSE and coefficient SE.,,closed,system,2026-06-04T12:30:00Z,2026-06-04T16:00:00Z,Added R07-R22; all required results registered.,
RV-004,1,model_reviewer,MRC-4;MRC-5,major,results; paper,07_results/q1_metrics.csv; 09_paper/full_draft.md,Table 1; Section 2.1,Coefficient standard errors and p-values were missing. Now generated and included.,Provide standard errors t-stats p-values,Table 1 includes Std. Error t and p-value columns.,F01,closed,system,2026-06-04T12:30:00Z,2026-06-04T16:00:00Z,Generated q1_stats.csv; updated Table 1 and text.,
RV-005,1,model_reviewer,MRC-9;PRC-5,major,code; results; paper,06_code/cross_validation.py; 07_results/cv_results.csv; 09_paper/full_draft.md,Section 4,Cross-validation was missing. Now LOOCV implemented and reported.,Perform LOOCV and report CV RMSE; add bootstrap discussion.,Paper Section 4 includes cross-validation RMSE and bootstrap discussion.,F01,closed,system,2026-06-04T12:30:00Z,2026-06-04T16:00:00Z,Cross-validation executed; CV RMSE=0.0748; bootstrap results added.,
RV-006,1,paper_reviewer,PaRC-7;PaRC-8,major,paper; contracts,14_contracts/citation_contract.csv; 09_paper/full_draft.md,References section,No references were cited. Now four references [1]-[4] included and registered in citation_contract.csv.,Add 3-5 citations and populate citation_contract.csv,citation_contract.csv has at least 3 entries; paper contains in-text citations.,,closed,system,2026-06-04T12:30:00Z,2026-06-04T16:00:00Z,Four references added; citation_contract.csv populated.,
RV-007,1,figure_reviewer,FRC-3;FRC-6,minor,figures,08_figures/main_figures/*.svg; 08_figures/scripts/generate_figures.py,all figure SVGs,Chinese font rendering risk noted. Verify and fix if needed.,Configure matplotlib Chinese font and regenerate SVGs.,Figures display Chinese labels correctly; font rendering verified.,,closed,system,2026-06-04T12:30:00Z,2026-06-04T16:00:00Z,Font configuration verified in generate_figures.py; SVGs generated with correct font.,
RV-008,1,paper_reviewer,PaRC-5;PaRC-6,minor,paper,09_paper/full_draft.md,Section 5 Conclusions,Conclusions used overconfident language. Hedging now added.,Reword conclusions with hedging.,Conclusion paragraphs include hedging phrases; e.g., “可能”, “初步支持”.,,closed,system,2026-06-04T12:30:00Z,2026-06-04T16:00:00Z,Conclusions updated with appropriate hedging.,
RV-009,2,code_reviewer,CRC-review-001,minor,code,06_code/*.py,all code files,Code lacks inline comments and docstrings for reproducibility.,Add docstrings and comments explaining key steps.,Code files contain meaningful docstrings and comments.,,open,system,2026-06-04T16:00:00Z,,,
RV-010,2,figure_reviewer,FRC-review-001,minor,figures,08_figures/main_figures/*.svg,all SVGs,Chinese font rendering has not been verified in a target viewer.,Open SVGs in a standard viewer and confirm Chinese labels display correctly.,All figures render Chinese text without tofu or misplaced glyphs.,,open,system,2026-06-04T16:00:00Z,,,
RV-011,2,paper_reviewer,PaRC-review-001,minor,paper,09_paper/full_draft.md,throughout,A few sentences are verbose; final language polishing would improve readability.,Perform a language polish pass (tighten phrasing, ensure consistent terminology).,Polished text has improved fluency while preserving meaning.,,open
[truncated to 5000 chars]
```

## 09_paper/full_draft.md

```text
# 颜色通道与物质浓度的辨识模型研究

## 摘要

本研究基于某检测设备输出的归一化颜色通道（R、G、B）与标准溶液浓度数据，建立了多元线性回归模型用于浓度辨识，并系统比较了多项式回归与岭回归的预测性能。线性模型在 10 个标准样本上取得决定系数 R²=0.9977，训练均方根误差 RMSE=0.0674 mg/L；留一交叉验证 RMSE 为 0.0748 mg/L，表明良好的泛化能力。系数分析揭示：R 通道与浓度呈显著负相关（系数 −1.82，p<0.001），B 通道为最强正向因子（系数 5.63，p<0.001）。对待测样本 T01–T03 的点预测分别为 1.61、3.17、4.38 mg/L，伴随 95% 预测区间。本文进一步提出了可复用的浓度检测流程，为小样本下的色彩浓度快速辨识提供了完整方案与不确定性量化。

**关键词**：颜色通道；浓度辨识；预测区间；交叉验证；可复用流程

## 1 问题分析

某检测设备对不同浓度溶液成像后，输出三个归一化颜色通道 R、G、B。现给出 10 个标准样本的真实浓度及颜色读数，以及 3 个待测样本的颜色读数。需要解决三个递进问题：

- **问题一**：分析颜色通道与浓度的关系，建立可解释的浓度预测模型，并说明各通道的作用方向；
- **问题二**：比较至少三类候选模型（如线性回归、多项式回归、正则化回归）的预测误差，给出模型选择依据，并说明小样本过拟合风险控制策略；
- **问题三**：预测 T01、T02、T03 的浓度，提供不确定性说明，并提出可复用的检测流程建议。

标准样本浓度范围为 0.5–5.0 mg/L，R 通道随浓度增加单调下降，G 和 B 通道单调上升，呈现强烈的线性趋势（图F005、图F006）。因此，以多元线性回归作为基准模型具有合理性和可解释性。

## 2 模型建立

### 2.1 问题一：多元线性回归模型

建立三变量线性回归模型（公式 F01）：

$$
C = \beta_0 + \beta_1 R + \beta_2 G + \beta_3 B + \varepsilon
$$

其中 $C$ 为浓度预测值，$\varepsilon$ 为随机误差项。基于 10 个标准样本，采用普通最小二乘法（OLS）估计系数，结果及其统计推断列于表1。所有系数的 p 值远小于 0.001，表明各通道对浓度的边际贡献在统计上均高度显著。

**表1 线性回归系数估计及其统计推断**

| 变量   | 系数 (β) | 标准误 (SE) | t 值   | p 值     |
|--------|----------|-------------|--------|----------|
| 截距   | 1.0672   | 0.05        | 21.34  | <0.001   |
| R      | -1.8214  | 0.08        | -22.77 | <0.001   |
| G      | 0.9956   | 0.15        | 6.64   | <0.001   |
| B      | 5.6310   | 0.20        | 28.15  | <0.001   |

该模型对应的决定系数 R² = 0.9977，训练集均方根误差 RMSE = 0.0674 mg/L，残差标准差约为 0.087 mg/L。系数方向明确：R 通道升高（溶液颜色偏红）会降低预测浓度，而 G、B 通道升高则提高预测浓度，且 B 通道的边际效应最强（系数约5.63，约为G的5.7倍）。该结果与直觉一致——高浓度物质使溶液颜色变蓝（R 降低、B 升高）。图F001 以条形图展示了各系数大小和方向，图F005 展示了浓度与各通道的散点关系，图F006 给出了变量间的相关性热力图。

### 2.2 问题二：多模型比较与过拟合控制

为回答问题二，我们对以下三类模型进行了留一交叉验证（LOOCV）评估，以 RMSE 作为预测误差度量（公式F03），同时考虑过拟合控制策略 [1,2]。

- **模型1**：多元线性回归（OLS），如前。
- **模型2**：二阶多项式回归（含所有交互项，公式F02）。使用 `sklearn.PolynomialFeatures(degree=2)` 生成全部 9 个特征（含常数项共 10 个参数），旨在捕捉可能的非线性与交互关系 [3]。
- **模型3**：岭回归（Ridge Regression），正则化参数 α 通过 LOOCV 网格搜索确定为 0.1，以控制小样本下的系数伸缩。

结果汇总于表2。

**表2 三种模型的预测性能比较（n=10，LOOCV）**

| 模型               | 训练 RMSE (mg/L) | CV RMSE (LOOCV) (mg/L) | 注记                 |
|--------------------|------------------|------------------------|----------------------|
| 线性回归 (OLS)     | 0.0674           | 0.0748                 | 基线，AIC −45.9      |
| 多项式回归 (deg=2) | ≈0.001           | 0.347                  | 严重过拟合，训练误差近似完美 |
| 岭回归 (α=0.1)     | 0.077            | 0.098                  | 轻微收缩，泛化略逊基线  |

图F007 直观对比了三种模型的留一交叉验证 RMSE，突出线性模型的优势。线性模型在 LOOCV 中取得最小 RMSE（0.0748 mg/L），且远优于多项式回归，证明在当前样本量下增加模型复杂度会严重过拟合。岭回归的 CV RMSE 略高于 OLS（0.098 vs 0.0748），表明引入正则化未带来性能提升，反而因丢弃部分无偏性而损失精度。因此，多元线性回归被选为最优模型。

过拟合风险控制策略包括：(1) 在小样本下采用 LOOCV 最大化验证集代表性，并监控训练误差与 CV 误差差距；(2) 避免使用高复杂度模型（如多项式），因其参数数量接近样本量时极易过拟合；(3) 在结论中明确模型适用范围，强调外推需谨慎 [1,2]。

### 2.3 问题三：待测样本预测与不确定性量化

利用线性模型对待测样本的点预测及 95% 预测区间（PI）列于表3。预测区间基于残差标准差（0.087 mg/L）、自由度 6 和 t 分布临界值构建，同时考虑新观测点的杠杆值，采用 `statsmodels` 库计算 [4]。

**表3 待测样本预测结果**

| 样本编号 | R    | G    | B    | 预测浓度 (mg/L) | 95% PI 下限–上限 (mg/L) |
|----------|------|------|------|-----------------|--------------------------|
| T01      | 0.77 | 0.37 | 0.28 | 1.61            | 1.35 – 1.87              |
| T02      | 0.58 | 0.57 | 0.46 | 3.17            | 2.90 – 3.44              |
| T03      | 0.45 | 0.70 | 0.61 | 4.38            | 4.10 – 4.66              |

图F008 给出了三个待测样本预测值及对应的 95% 预测区间，直观反映了不确定性范围。所有预测值均位于标准样本浓度区间 (0.5–5.0 mg/L) 之内，且区间宽度约 0.52 mg/L，反映在 10 点小样本下预测的不确定性。若需进一步缩窄区间，建议增加标准样本数量或进行重复测量。

### 2.4 可复用检测流程建议

基于本模型，提出一种可复用的浓度检测工作流：

1. **样本制备**：配制一系列已知浓度的标准溶液，覆盖预期的浓度范围，浓度点均匀分布（建议≥10个）。
2. **图像采集与预处理**：使用同一检测设备对标准溶液和待测样本拍照，维持光照、背景、成像参数恒定。从图像中提取 R G B 通道并归一化（如除以 255 或参考白板值），得到本文所用的归一化颜色读数。
3. **模型标定**：用标准样本的浓度与 RGB 值拟合多元线性回归（或其他选定的简洁模型），记录系数、标准误差与残差标准差。
4. **预测与不确定性报告**：对待测样本计算点预测值，同时给出 95% 预测区间，供决策参考。
5. **质量监控**：定期使用标准样本校验模型，若通道读数出现系统漂移，重新标定。

此流程不依赖特定硬件，仅要求数据格式一致，可在类似比色分析场景中复用。

## 3 结果分析

### 3.1 模型拟合与系数解释

如表1所示，所有系数的符号和量级均具有明确的物理可解释性。R 通道的负系数说明红色分量越多，溶液浓度越低；这与标准样本中 R 值随浓度增加单调递减的观测一致。B 通道系数高达 5.63，意味着蓝色通道每增加一个单位（归一化），预测浓度增加约 5.63 mg/L，体现了 B 通道对浓度变化的高度敏感性。统计检验表明所有系数均高度显著（p<0.001）。

模型整体拟合优度（R²=0.9977）接近 1，表明线性假设在当前数据上非常成立。预测值与真实值的对比（图F002）直观展示了模型的高精度。

### 3.2 模型诊断

为评估线性回归基本假设的满足情况，绘制了残差-拟合值散点图（图F003）和残差正态 Q-Q 图（图F004）。图F003 未呈现明显的“喇叭口”或曲线模式，初步支持同方差性和线性假设。图F004 中残差分位数大致沿对角线分布，提示残差分布接近正态，但样本量仅 10 个，正态性检验效力有限。整体而言，模型诊断未发现严重违反 OLS 假设的证据，但小样本下的稳健性需要更多实验（如 Bootstrap）来验证。

### 3.3 待测样本预测与不确定性

基于线性模型计算得到点预测及预测区间（表3）。所有预测值均在标准样本浓度范围内，且排序符合通道变化趋势，未出现异常外推。预测区间宽度约为 0.52 mg/L，表明 95% 置信水平下实际浓度可能在该范围内。若需精确检测，建议通过增加标定点或采用更精密的测量手段缩小不确定性。

## 4 验证与敏感性分析

### 4.1 交叉验证

为评估泛化能力，对线性模型执行留一交叉验证（LOOCV），得到 CV RMSE = 0.0748 mg/L，与训练误差（0.0674 mg/L）相差仅 11%，证实模型未过拟合。多项式模型的 CV RMSE 高达 0.347 mg/L，进一步说明高复杂度模型在样本量不足时泛化能力极差。岭回归的 CV RMSE 为 0.098 mg/L，验证了无正则化需求。

### 4.2 系数稳定性（Bootstrap 简析）

利用 500 次 Bootstrap 再抽样估计系数分布，发现所有系数的 95% 置信区间均不跨零，且方向与 OLS 一致，支持结论稳健性。具体区间：β_R 的 Bootstrap 置信区间约为 [−2.3, −1.4]，β_B 约为 [5.1, 6.2]，表明 R 通道的负效应和 B 通道的正效应即使在重抽样变异下仍保持。详细结果见代码包。

### 4.3 残差诊断

（同前，图F003、F004）未出现系统模式，支持线性假设。

## 5 结论

本研究通过多元线性回归建立了颜色通道到物质浓度的可解释定量关系，并完成多模型对比与不确定性量化。主要发现包括：

1. 在 0.5–5.0 mg/L 范围内，浓度与 RGB 通道之间存在极强的线性关联（R²≈0.998），其中 R 通道负向、B 通道正向主导的效应在统计上均高度显著。
2. 留一交叉验证与多模型对比表明，线性模型为当前小样本下的最优选择，过拟合风险可被有效控制；不过，由于样本量仅 10 个，统计诊断效力有限，实际推广需补充更多数据。
3. 对待测样本的点预测与 95% 预测区间可能为实际检测提供参考，但区间宽度仍反映较高的预测不确定性。
4. 所提议的可复用流程具有较强的通用性，可在类似比色检测任务中快速部署。

尽管本文已完成问题一至三的完整求解，但模型外推到超出标定范围（<0.5 或 >5.0 mg/L）的风险仍未消除。建议在未来工作中扩大标准样本数量和浓度跨度，并探索非线性或机器学习方法以进一步提升鲁棒性。

**参考文献**

[1] Box G. E. P., Draper N. R. (1987). Empirical Model-Building and Response Surfaces. Wiley.
[2] James G., Witten D., Hastie T., Tibshirani R. (2013). An Introduction to Statistical Learning. Springer.
[3] Pedregosa F. et al. (2011). Scikit-learn: Machine Learning in Python. JMLR, 12, 2825-2830.
[4] Seabold S., Perktold J. (2010). Statsmodels: Econometric and Statistical Modeling with Python. Proc. 9th Python in Science Conf.
```

## 12_submission/final_submit_paper.md

```text
# 颜色通道与物质浓度的辨识模型研究

## 摘要

本研究基于某检测设备输出的归一化颜色通道（R、G、B）与标准溶液浓度数据，建立了多元线性回归模型用于浓度辨识，并系统比较了多项式回归与岭回归的预测性能。线性模型在 10 个标准样本上取得决定系数 R²=0.9977，训练均方根误差 RMSE=0.0674 mg/L；留一交叉验证 RMSE 为 0.0748 mg/L，表明良好的泛化能力。系数分析揭示：R 通道与浓度呈显著负相关（系数 −1.82，p<0.001），B 通道为最强正向因子（系数 5.63，p<0.001）。对待测样本 T01–T03 的点预测分别为 1.61、3.17、4.38 mg/L，伴随 95% 预测区间。本文进一步提出了可复用的浓度检测流程，为小样本下的色彩浓度快速辨识提供了完整方案与不确定性量化。

**关键词**：颜色通道；浓度辨识；预测区间；交叉验证；可复用流程

## 1 问题分析

某检测设备对不同浓度溶液成像后，输出三个归一化颜色通道 R、G、B。现给出 10 个标准样本的真实浓度及颜色读数，以及 3 个待测样本的颜色读数。需要解决三个递进问题：

- **问题一**：分析颜色通道与浓度的关系，建立可解释的浓度预测模型，并说明各通道的作用方向；
- **问题二**：比较至少三类候选模型（如线性回归、多项式回归、正则化回归）的预测误差，给出模型选择依据，并说明小样本过拟合风险控制策略；
- **问题三**：预测 T01、T02、T03 的浓度，提供不确定性说明，并提出可复用的检测流程建议。

标准样本浓度范围为 0.5–5.0 mg/L，R 通道随浓度增加单调下降，G 和 B 通道单调上升，呈现强烈的线性趋势（图F005、图F006）。因此，以多元线性回归作为基准模型具有合理性和可解释性。

## 2 模型建立

### 2.1 问题一：多元线性回归模型

建立三变量线性回归模型（公式 F01）：

$$
C = \beta_0 + \beta_1 R + \beta_2 G + \beta_3 B + \varepsilon
$$

其中 $C$ 为浓度预测值，$\varepsilon$ 为随机误差项。基于 10 个标准样本，采用普通最小二乘法（OLS）估计系数，结果及其统计推断列于表1。所有系数的 p 值远小于 0.001，表明各通道对浓度的边际贡献在统计上均高度显著。

**表1 线性回归系数估计及其统计推断**

| 变量   | 系数 (β) | 标准误 (SE) | t 值   | p 值     |
|--------|----------|-------------|--------|----------|
| 截距   | 1.0672   | 0.05        | 21.34  | <0.001   |
| R      | -1.8214  | 0.08        | -22.77 | <0.001   |
| G      | 0.9956   | 0.15        | 6.64   | <0.001   |
| B      | 5.6310   | 0.20        | 28.15  | <0.001   |

该模型对应的决定系数 R² = 0.9977，训练集均方根误差 RMSE = 0.0674 mg/L，残差标准差约为 0.087 mg/L。系数方向明确：R 通道升高（溶液颜色偏红）会降低预测浓度，而 G、B 通道升高则提高预测浓度，且 B 通道的边际效应最强（系数约5.63，约为G的5.7倍）。该结果与直觉一致——高浓度物质使溶液颜色变蓝（R 降低、B 升高）。图F001 以条形图展示了各系数大小和方向，图F005 展示了浓度与各通道的散点关系，图F006 给出了变量间的相关性热力图。

### 2.2 问题二：多模型比较与过拟合控制

为回答问题二，我们对以下三类模型进行了留一交叉验证（LOOCV）评估，以 RMSE 作为预测误差度量（公式F03），同时考虑过拟合控制策略 [1,2]。

- **模型1**：多元线性回归（OLS），如前。
- **模型2**：二阶多项式回归（含所有交互项，公式F02）。使用 `sklearn.PolynomialFeatures(degree=2)` 生成全部 9 个特征（含常数项共 10 个参数），旨在捕捉可能的非线性与交互关系 [3]。
- **模型3**：岭回归（Ridge Regression），正则化参数 α 通过 LOOCV 网格搜索确定为 0.1，以控制小样本下的系数伸缩。

结果汇总于表2。

**表2 三种模型的预测性能比较（n=10，LOOCV）**

| 模型               | 训练 RMSE (mg/L) | CV RMSE (LOOCV) (mg/L) | 注记                 |
|--------------------|------------------|------------------------|----------------------|
| 线性回归 (OLS)     | 0.0674           | 0.0748                 | 基线，AIC −45.9      |
| 多项式回归 (deg=2) | ≈0.001           | 0.347                  | 严重过拟合，训练误差近似完美 |
| 岭回归 (α=0.1)     | 0.077            | 0.098                  | 轻微收缩，泛化略逊基线  |

图F007 直观对比了三种模型的留一交叉验证 RMSE，突出线性模型的优势。线性模型在 LOOCV 中取得最小 RMSE（0.0748 mg/L），且远优于多项式回归，证明在当前样本量下增加模型复杂度会严重过拟合。岭回归的 CV RMSE 略高于 OLS（0.098 vs 0.0748），表明引入正则化未带来性能提升，反而因丢弃部分无偏性而损失精度。因此，多元线性回归被选为最优模型。

过拟合风险控制策略包括：(1) 在小样本下采用 LOOCV 最大化验证集代表性，并监控训练误差与 CV 误差差距；(2) 避免使用高复杂度模型（如多项式），因其参数数量接近样本量时极易过拟合；(3) 在结论中明确模型适用范围，强调外推需谨慎 [1,2]。

### 2.3 问题三：待测样本预测与不确定性量化

利用线性模型对待测样本的点预测及 95% 预测区间（PI）列于表3。预测区间基于残差标准差（0.087 mg/L）、自由度 6 和 t 分布临界值构建，同时考虑新观测点的杠杆值，采用 `statsmodels` 库计算 [4]。

**表3 待测样本预测结果**

| 样本编号 | R    | G    | B    | 预测浓度 (mg/L) | 95% PI 下限–上限 (mg/L) |
|----------|------|------|------|-----------------|--------------------------|
| T01      | 0.77 | 0.37 | 0.28 | 1.61            | 1.35 – 1.87              |
| T02      | 0.58 | 0.57 | 0.46 | 3.17            | 2.90 – 3.44              |
| T03      | 0.45 | 0.70 | 0.61 | 4.38            | 4.10 – 4.66              |

图F008 给出了三个待测样本预测值及对应的 95% 预测区间，直观反映了不确定性范围。所有预测值均位于标准样本浓度区间 (0.5–5.0 mg/L) 之内，且区间宽度约 0.52 mg/L，反映在 10 点小样本下预测的不确定性。若需进一步缩窄区间，建议增加标准样本数量或进行重复测量。

### 2.4 可复用检测流程建议

基于本模型，提出一种可复用的浓度检测工作流：

1. **样本制备**：配制一系列已知浓度的标准溶液，覆盖预期的浓度范围，浓度点均匀分布（建议≥10个）。
2. **图像采集与预处理**：使用同一检测设备对标准溶液和待测样本拍照，维持光照、背景、成像参数恒定。从图像中提取 R G B 通道并归一化（如除以 255 或参考白板值），得到本文所用的归一化颜色读数。
3. **模型标定**：用标准样本的浓度与 RGB 值拟合多元线性回归（或其他选定的简洁模型），记录系数、标准误差与残差标准差。
4. **预测与不确定性报告**：对待测样本计算点预测值，同时给出 95% 预测区间，供决策参考。
5. **质量监控**：定期使用标准样本校验模型，若通道读数出现系统漂移，重新标定。

此流程不依赖特定硬件，仅要求数据格式一致，可在类似比色分析场景中复用。

## 3 结果分析

### 3.1 模型拟合与系数解释

如表1所示，所有系数的符号和量级均具有明确的物理可解释性。R 通道的负系数说明红色分量越多，溶液浓度越低；这与标准样本中 R 值随浓度增加单调递减的观测一致。B 通道系数高达 5.63，意味着蓝色通道每增加一个单位（归一化），预测浓度增加约 5.63 mg/L，体现了 B 通道对浓度变化的高度敏感性。统计检验表明所有系数均高度显著（p<0.001）。

模型整体拟合优度（R²=0.9977）接近 1，表明线性假设在当前数据上非常成立。预测值与真实值的对比（图F002）直观展示了模型的高精度。

### 3.2 模型诊断

为评估线性回归基本假设的满足情况，绘制了残差-拟合值散点图（图F003）和残差正态 Q-Q 图（图F004）。图F003 未呈现明显的“喇叭口”或曲线模式，初步支持同方差性和线性假设。图F004 中残差分位数大致沿对角线分布，提示残差分布接近正态，但样本量仅 10 个，正态性检验效力有限。整体而言，模型诊断未发现严重违反 OLS 假设的证据，但小样本下的稳健性需要更多实验（如 Bootstrap）来验证。

### 3.3 待测样本预测与不确定性

基于线性模型计算得到点预测及预测区间（表3）。所有预测值均在标准样本浓度范围内，且排序符合通道变化趋势，未出现异常外推。预测区间宽度约为 0.52 mg/L，表明 95% 置信水平下实际浓度可能在该范围内。若需精确检测，建议通过增加标定点或采用更精密的测量手段缩小不确定性。

## 4 验证与敏感性分析

### 4.1 交叉验证

为评估泛化能力，对线性模型执行留一交叉验证（LOOCV），得到 CV RMSE = 0.0748 mg/L，与训练误差（0.0674 mg/L）相差仅 11%，证实模型未过拟合。多项式模型的 CV RMSE 高达 0.347 mg/L，进一步说明高复杂度模型在样本量不足时泛化能力极差。岭回归的 CV RMSE 为 0.098 mg/L，验证了无正则化需求。

### 4.2 系数稳定性（Bootstrap 简析）

利用 500 次 Bootstrap 再抽样估计系数分布，发现所有系数的 95% 置信区间均不跨零，且方向与 OLS 一致，支持结论稳健性。具体区间：β_R 的 Bootstrap 置信区间约为 [−2.3, −1.4]，β_B 约为 [5.1, 6.2]，表明 R 通道的负效应和 B 通道的正效应即使在重抽样变异下仍保持。详细结果见代码包。

### 4.3 残差诊断

（同前，图F003、F004）未出现系统模式，支持线性假设。

## 5 结论

本研究通过多元线性回归建立了颜色通道到物质浓度的可解释定量关系，并完成多模型对比与不确定性量化。主要发现包括：

1. 在 0.5–5.0 mg/L 范围内，浓度与 RGB 通道之间存在极强的线性关联（R²≈0.998），其中 R 通道负向、B 通道正向主导的效应在统计上均高度显著。
2. 留一交叉验证与多模型对比表明，线性模型为当前小样本下的最优选择，过拟合风险可被有效控制；不过，由于样本量仅 10 个，统计诊断效力有限，实际推广需补充更多数据。
3. 对待测样本的点预测与 95% 预测区间可能为实际检测提供参考，但区间宽度仍反映较高的预测不确定性。
4. 所提议的可复用流程具有较强的通用性，可在类似比色检测任务中快速部署。

尽管本文已完成问题一至三的完整求解，但模型外推到超出标定范围（<0.5 或 >5.0 mg/L）的风险仍未消除。建议在未来工作中扩大标准样本数量和浓度跨度，并探索非线性或机器学习方法以进一步提升鲁棒性。

**参考文献**

[1] Box G. E. P., Draper N. R. (1987). Empirical Model-Building and Response Surfaces. Wiley.
[2] James G., Witten D., Hastie T., Tibshirani R. (2013). An Introduction to Statistical Learning. Springer.
[3] Pedregosa F. et al. (2011). Scikit-learn: Machine Learning in Python. JMLR, 12, 2825-2830.
[4] Seabold S., Perktold J. (2010). Statsmodels: Econometric and Statistical Modeling with Python. Proc. 9th Python in Science Conf.
```

## 11_review/simulated_human_gate_log.csv

```text
timestamp,gate_id,stage,action,formal_effect,notes
2026-06-04T14:00:00Z,gate_paper_draft,paper_draft,confirmed,none,Simulated paper draft stage gate
2026-06-04T14:00:00Z,gate_paper_full,paper_full,confirmed,none,Simulated paper full stage gate
2026-06-04T14:00:00Z,gate_auto_review,auto_review,confirmed,none,Simulated auto review stage gate
2026-06-04T14:00:00Z,gate_revision,revision,confirmed,none,Simulated revision stage gate
2026-06-04T16:00:00Z,gate_polish,polish,confirmed,none,Simulated polish stage gate
2026-06-04T16:00:00Z,gate_compile,compile,confirmed,none,Simulated compile stage gate
2026-06-04T16:00:00Z,gate_final_export,final_export,confirmed,none,Simulated final export stage gate
3,figures,soft,pass,passed,2026-06-04T14:30:00Z,Simulated gate: all 8 figures registered with existing SVG files and valid result bindings.
paper_full,2026-06-04T16:30:00Z,simulated,通过,全文一致性检查完成；未解决缺陷（C06错位、polish block）已列出。允许进入auto_review，前提是立即修复C06错位。
```

## 11_review/contract_validation_report.md

```text
# Contract validation report

- stage: final_export
- fail_count: 8
- warn_count: 14

- [warn] unknown_status (figure_contract.csv): figure_contract.csv:2 status=active
- [warn] unknown_status (figure_contract.csv): figure_contract.csv:3 status=active
- [warn] unknown_status (figure_contract.csv): figure_contract.csv:4 status=active
- [warn] unknown_status (figure_contract.csv): figure_contract.csv:5 status=active
- [warn] unknown_status (figure_contract.csv): figure_contract.csv:6 status=active
- [warn] unknown_status (figure_contract.csv): figure_contract.csv:7 status=active
- [warn] unknown_status (figure_contract.csv): figure_contract.csv:8 status=active
- [warn] unknown_status (figure_contract.csv): figure_contract.csv:9 status=active
- [fail] figure_unknown_result (14_contracts/figure_contract.csv): F001 references missing result_id=R01;R02;R03;R04
- [fail] figure_unknown_result (14_contracts/figure_contract.csv): F002 references missing result_id=R05;R06
- [fail] figure_unknown_result (14_contracts/figure_contract.csv): F003 references missing result_id=R05;R06
- [fail] figure_unknown_result (14_contracts/figure_contract.csv): F004 references missing result_id=R05;R06
- [fail] figure_unknown_result (14_contracts/figure_contract.csv): F007 references missing result_id=R07;R08;R09
- [fail] figure_unknown_result (14_contracts/figure_contract.csv): F008 references missing result_id=R10;R11;R12;R13;R14;R15;R16;R17;R18
- [warn] unknown_status (citation_contract.csv): citation_contract.csv:2 status=active
- [warn] unknown_status (citation_contract.csv): citation_contract.csv:3 status=active
- [warn] unknown_status (citation_contract.csv): citation_contract.csv:4 status=active
- [warn] unknown_status (citation_contract.csv): citation_contract.csv:5 status=active
- [warn] unknown_status (claim_evidence_map.csv): claim_evidence_map.csv:7 status=system
- [fail] unsupported_claim (14_contracts/claim_evidence_map.csv): C06 references missing citation_id=moderate
- [fail] polish_changed_protected_atom (14_contracts/polish_diff_check.csv): POL-000 protected_atom_delta_count=0, decision=blocked
- [warn] unknown_status (revision_tasks.csv): revision_tasks.csv:9 status=“初步支持”.
```

