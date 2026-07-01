# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX\workspace`
Run dir: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX`
Call id: `iteration_05_07_results_freeze`
Iteration: 5
Max iterations: 5
Current simulated stage: `results_freeze`
Stage order: 7
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX/reports/prompt_route_manifest.md`
Training sandbox stage prompt bundle: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX/reports/stage_prompt_bundle.md`

Revision queue: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX\reports\agent_revision_queue.csv`

Open fail/major queue items:
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-001: Expand 12_submission/final_submit_paper.md from the latest full_draft with substantive problem analysis, model, results, validation, and conclusion sections. | acceptance: final_submit_paper.md has at least 2500 characters and at least seven sections. | notes: validation_item=training_final_paper_too_thin
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-002: Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied. | acceptance: All major/fail revision_tasks.csv rows have status closed/resolved/waived. | notes: validation_item=training_revision_task_unresolved
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-003: Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied. | acceptance: All major/fail revision_tasks.csv rows have status closed/resolved/waived. | notes: validation_item=training_revision_task_unresolved
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-004: Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied. | acceptance: All major/fail revision_tasks.csv rows have status closed/resolved/waived. | notes: validation_item=training_revision_task_unresolved
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-005: Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied. | acceptance: All major/fail revision_tasks.csv rows have status closed/resolved/waived. | notes: validation_item=training_revision_task_unresolved
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-006: Resolve or close fail-level review scorecard items after applying the corresponding sandbox fixes. | acceptance: No review_scorecard row has severity/fail_level=fail unless status is closed/resolved/waived. | notes: validation_item=training_review_fail_unclosed
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-007: Fix the underlying low-score artifacts first: result sources, figure files/contracts, paper sections, evidence bindings, and revision tasks; then rerun auto_review so scores rise above threshold. | acceptance: Every review_scorecard row is at least 85% of max_score, with supporting artifact fixes present. | notes: validation_item=training_review_score_below_threshold
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-008: Resolve or close fail-level review scorecard items after applying the corresponding sandbox fixes. | acceptance: No review_scorecard row has severity/fail_level=fail unless status is closed/resolved/waived. | notes: validation_item=training_review_fail_unclosed
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-009: Fix the underlying low-score artifacts first: result sources, figure files/contracts, paper sections, evidence bindings, and revision tasks; then rerun auto_review so scores rise above threshold. | acceptance: Every review_scorecard row is at least 85% of max_score, with supporting artifact fixes present. | notes: validation_item=training_review_score_below_threshold
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-010: Close or resolve fail/major revision tasks after applying the corresponding sandbox fix. | acceptance: All fail/major revision tasks are closed/resolved/waived. | notes: contract_item=revision_task_unresolved
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-011: Close or resolve fail/major revision tasks after applying the corresponding sandbox fix. | acceptance: All fail/major revision tasks are closed/resolved/waived. | notes: contract_item=revision_task_unresolved
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-012: Close or resolve fail/major revision tasks after applying the corresponding sandbox fix. | acceptance: All fail/major revision tasks are closed/resolved/waived. | notes: contract_item=revision_task_unresolved

Rules:
- Follow only deep_sequential behavior for this stage.
- Do not edit `00_problem/problem_statement.md` or `00_problem/inbox/`; write intake analysis to `01_task_analysis/`.
- A formal human gate becomes a simulated sandbox gate. Record it in `11_review/simulated_human_gate_log.csv`.
- Update contracts before writing paper claims, result analysis, figures, or submission text.
- Use the Workspace Context Snapshot below as the current file context; do not request read_file/list_files pseudo-tools.
- Reply only through runner file actions. The external runner will reject prose-only or pseudo-tool responses.

Stage output target:
- Create or update the artifacts normally owned by `results_freeze`.
- If this stage cannot close a blocker, update review/revision artifacts with a concrete blocker note.
- Keep `reports/training_enhancement_points.csv` current once a full draft or review finding exists.

Stage-specific required outputs:
- Write non-empty `14_contracts/result_contract.csv` with result_id, metric_name, metric_value, source_file, used_by_claim_ids, freeze_status.
- Every numerical result cited later must have a result_contract row.
- Write or update reproducible result files under `07_results/` before freezing numbers.

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
- 09_paper/paper_full_stage_summary.md (2846 bytes)
- 09_paper/polish_diff_log.md (144 bytes)
- 09_paper/polish_plan.md (237 bytes)
- 09_paper/polish_tasks.csv (232 bytes)
- 09_paper/section_weight_profiles.csv (2354 bytes)
- 09_paper/unresolved_review_issues.md (855 bytes)
- 11_review/.gitkeep (0 bytes)
- 11_review/auto_review_stage_summary.md (736 bytes)
- 11_review/code_reviewer_comments.md (446 bytes)
- 11_review/compile_stage_summary.md (528 bytes)
- 11_review/contract_validation_report.json (7115 bytes)
- 11_review/contract_validation_report.md (3730 bytes)
- 11_review/figure_reviewer_comments.md (557 bytes)
- 11_review/figures_stage_summary.md (1359 bytes)
- 11_review/final_export_blocker_note.md (1955 bytes)
- 11_review/final_submission_checklist.md (1399 bytes)
- 11_review/gate_report.json (111 bytes)
- 11_review/judge_reviewer_comments.md (594 bytes)
- 11_review/latex_template_stage_summary.md (331 bytes)
- 11_review/model_reviewer_comments.md (531 bytes)
- 11_review/paper_full_stage_summary.md (1302 bytes)
- 11_review/paper_reviewer_comments.md (551 bytes)
- 11_review/polish_blocker_note.md (952 bytes)
- 11_review/prior_copy_risk_report.md (196 bytes)
- 11_review/prior_retrieval_stage_summary.md (969 bytes)
- 11_review/problem_reviewer_comments.md (334 bytes)
- 11_review/review_scorecard.csv (1147 bytes)
- 11_review/revision_stage_summary.md (1620 bytes)
- 11_review/revision_tasks.csv (5187 bytes)
- 11_review/simulated_human_gate_log.csv (579 bytes)
- 11_review/skill_router_report.json (5728 bytes)
- 11_review/skill_router_report.md (356 bytes)
- 11_review/unresolved_review_issues.md (1854 bytes)
- 12_submission/ai_usage_detail.pdf (2757 bytes)
- 12_submission/code_package/.gitkeep (0 bytes)
- 12_submission/data_package/.gitkeep (0 bytes)
- 12_submission/figure_package/.gitkeep (0 bytes)
- 12_submission/final_submit_package.md (1543 bytes)
- 12_submission/final_submit_paper.md (11949 bytes)
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
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-001,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,validation,fail,E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX\workspace\12_submission\final_submit_paper.md,"chars=5804, sections=6","Expand 12_submission/final_submit_paper.md from the latest full_draft with substantive problem analysis, model, results, validation, and conclusion sections.",final_submit_paper.md has at least 2500 characters and at least seven sections.,open,,validation_item=training_final_paper_too_thin
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-002,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,validation,fail,E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX\workspace\14_contracts\revision_tasks.csv,"RV-013 severity=fail, status=open",Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied.,All major/fail revision_tasks.csv rows have status closed/resolved/waived.,open,,validation_item=training_revision_task_unresolved
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-003,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,validation,fail,E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX\workspace\14_contracts\revision_tasks.csv,"RV-014 severity=fail, status=open",Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied.,All major/fail revision_tasks.csv rows have status closed/resolved/waived.,open,,validation_item=training_revision_task_unresolved
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-004,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,validation,fail,E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX\workspace\14_contracts\revision_tasks.csv,"RV-015 severity=fail, status=open",Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied.,All major/fail revision_tasks.csv rows have status closed/resolved/waived.,open,,validation_item=training_revision_task_unresolved
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-005,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,validation,fail,E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX\workspace\14_contracts\revision_tasks.csv,"RV-016 severity=fail, status=open",Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied.,All major/fail revision_tasks.csv rows have status closed/resolved/waived.,open,,validation_item=training_revision_task_unresolved
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-006,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,validation,fail,E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX\workspace\11_review\review_scorecard.csv,"row 7: {'round_id': '3', 'reviewer': 'contract_auditor', 'dimension': 'Contract Integrity', 'score': '1', 'max_score': '10', 'severity': 'fail', 'issue_count': '10', 'top_risk': 'Multiple contract validation failures', 'required_action': 'Resolve figure_contract result_id separators, add missing citation CIT02, fix polish_diff block, and correct simulated gate log formal_effect', 'status': 'open', 'last_checked': '2026-06-04T18:00:00Z'}",Resolve or close fail-level review scorecard items after applying the corresponding sandbox fixes.,No review_scorecard row has severity/fail_level=fail unless status is closed/resolved/waived.,open,,validation_item=training_review_fail_unclosed
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-007,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,validation,fail,E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX\workspace\11_review\review_scorecard.csv,row 7: 1.0/10.0,"Fix the underlying low-score artifacts first: result sources, figure files/contracts, paper sections, evidence bindings, and revision tasks; then rerun auto_review so scores rise above threshold.","Every review_scorecard row is at least 85% of max_score, with supporting artifact fixes present.",open,,validation_item=training_review_score_below_threshold
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-008,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,validation,fail,E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX\workspace\11_review\review_scorecard.csv,"row 8: {'round_id': '3', 'reviewer': 'judge_reviewer', 'dimension': 'Overall Judgment', 'score': '0', 'max_score': '10', 'severity': 'fail', 'issue_count': '8', 'top_risk': 'Contract failures block submission', 'required_action': 'Fix all contract issues and re-run validation', 'status': 'open', 'last_checked': '2026-06-04T18:00:00Z'}",Resolve or close fail-level review scorecard items after applying the corresponding sandbox fixes.,No review_scorecard row has severity/fail_level=fail unless status is closed/resolved/waived.,open,,validation_item=training_review_fail_unclosed
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-VAL-009,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,validation,fail,E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX\workspace\11_review\review_scorecard.csv,row 8: 0.0/10.0,"Fix the underlying low-score artifacts first: result sources, figure files/contracts, paper sections, evidence bindings, and revision tasks; then rerun auto_review so scores rise above threshold.","Every review_scorecard row is at least 85% of max_score, with supporting artifact fixes present.",open,,validation_item=training_review_score_below_threshold
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-010,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,contract_validation,fail,14_contracts/revision_tasks.csv,"RV-013 severity=fail, status=open",Close or resolve fail/major revision tasks after applying the corresponding sandbox fix.,All fail/major revision tasks are closed/resolved/waived.,open,,contract_item=revision_task_unresolved
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-011,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,contract_validation,fail,14_contracts/revision_tasks.csv,"RV-014 severity=fail, status=open",Close or resolve fail/major revision tasks after applying the corresponding sandbox fix.,All fail/major revision tasks are closed/resolved/waived.,open,,contract_item=revision_task_unresolved
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-012,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,contract_validation,fail,14_contracts/revision_tasks.csv,"RV-015 severity=fail, status=open",Close or resolve fail/major revision tasks after applying the corresponding sandbox fix.,All fail/major revision tasks are closed/resolved/waived.,open,,contract_item=revision_task_unresolved
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-013,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,contract_validation,fail,14_contracts/revision_tasks.csv,"RV-016 severity=fail, status=open",Close or resolve fail/major revision tasks after applying the corresponding sandbox fix.,All fail/major revision tasks are closed/resolved/waived.,open,,contract_item=revision_task_unresolved
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-014,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,contract_validation,fail,11_review/review_scorecard.csv,row 7: 10.0 < 85.0,"Improve the underlying result sources, figures, paper, and evidence bindings before rerunning auto_review.",review_scorecard.csv scores are at least 85% of max_score and the artifact fixes are present.,open,,contract_item=review_score_below_threshold
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-015,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,contract_validation,fail,11_review/review_scorecard.csv,row 7 severity=fail status=open,Close or resolve fail-level review rows only after the corresponding sandbox fix is applied.,No fail-level review scorecard row remains open.,open,,contract_item=review_fail_unclosed
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-016,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,contract_validation,fail,11_review/review_scorecard.csv,row 8: 0.0 < 85.0,"Improve the underlying result sources, figures, paper, and evidence bindings before rerunning auto_review.",review_scorecard.csv scores are at least 85% of max_score and the artifact fixes are present.,open,,contract_item=review_score_below_threshold
TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX-CONTRACT-017,TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX,contract_validation,fail,11_review/review_scorecard.csv,row 8 severity=fail status=open,Close or resolve fail-level review rows only after the corresponding sandbox fix is applied.,No fail-level review scorecard row remains open.,open,,contract_item=review_fail_unclosed
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
| figure_mentions | 27 | 4.33 |
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
C01,Q1,sec_model,线性回归模型能够以极高拟合优度（R²=0.9977）描述浓度与RGB通道的关系,result,result,R05;R06,R05;R06,F002,F01,,strong,对于标准样本范围(0.5—5.0 mg/L)成立；外推需谨慎,,draft,system,2026-06-04T18:00:00Z
C02,Q1,sec_model,R通道与浓度呈现负相关（系数-1.8214），表明红色分量增加导致预测浓度降低,result,result,R02,R02,F001;F005,,,strong,,,draft,system,2026-06-04T18:00:00Z
C03,Q1,sec_model,G通道与浓度呈现弱正相关（系数0.9956），其影响幅度小于B通道,result,result,R03,R03,F001;F005,,,moderate,G通道系数置信区间需进一步考察,,draft,system,2026-06-04T18:00:00Z
C04,Q1,sec_model,B通道是浓度预测的主导正向因子（系数5.6310），显示蓝色分量对浓度变化的响应最强烈,result,result,R04,R04,F001;F005,,,strong,,,draft,system,2026-06-04T18:00:00Z
C05,Q1,sec_diagnostics,残差图未显示系统模式，残差近似满足正态性和同方差性，支持OLS假设,figure,figure,F003;F004,,F003;F004,,,moderate,样本量仅10个，诊断统计效力有限,,draft,system,2026-06-04T18:00:00Z
C06,Q1,sec_diagnostics,模型RMSE为0.0674 mg/L，表明预测误差在可接受范围,result,result,R06,R06,F003;F004,,CIT01,moderate,,需结合浓度范围评估,draft,system,2026-06-04T18:00:00Z
```

## 14_contracts/figure_contract.csv

```text
figure_id,question_id,core_claim,evidence_source,result_id,panel_plan,chart_type,backend,script_path,output_svg,output_png,output_pdf,dpi,used_in_section,latex_label,caption_source,quality_score,review_risk,status,owner,last_checked,title_cn,caption_cn,notes
F001,Q1,OLS系数估计值与方向,07_results/q1_coefficients.csv,R01,单图,bar,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F001_coefficient_bar.svg,,,300,sec_model,fig:coef,figure_caption_bank.md,4.5,font_risk,active,system,,OLS系数估计值与方向,多元线性回归模型各变量系数估计值，反映各颜色通道对浓度的作用方向和大小。,Shows coefficient R01
F001,Q1,OLS系数估计值与方向,07_results/q1_coefficients.csv,R02,单图,bar,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F001_coefficient_bar.svg,,,300,sec_model,fig:coef,figure_caption_bank.md,4.5,font_risk,active,system,,OLS系数估计值与方向,多元线性回归模型各变量系数估计值，反映各颜色通道对浓度的作用方向和大小。,Shows coefficient R02
F001,Q1,OLS系数估计值与方向,07_results/q1_coefficients.csv,R03,单图,bar,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F001_coefficient_bar.svg,,,300,sec_model,fig:coef,figure_caption_bank.md,4.5,font_risk,active,system,,OLS系数估计值与方向,多元线性回归模型各变量系数估计值，反映各颜色通道对浓度的作用方向和大小。,Shows coefficient R03
F001,Q1,OLS系数估计值与方向,07_results/q1_coefficients.csv,R04,单图,bar,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F001_coefficient_bar.svg,,,300,sec_model,fig:coef,figure_caption_bank.md,4.5,font_risk,active,system,,OLS系数估计值与方向,多元线性回归模型各变量系数估计值，反映各颜色通道对浓度的作用方向和大小。,Shows coefficient R04
F002,Q1,模型预测值与真实值对比,基于冻结系数和标准样本数据,R05,单图,scatter,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F002_pred_vs_actual.svg,,,300,sec_results,fig:pred_actual,figure_caption_bank.md,4.5,font_risk,active,system,,预测浓度与真实浓度对比,模型预测值与标准样本真实浓度的散点图，显示模型拟合精度。,Shows R² R05
F002,Q1,模型预测值与真实值对比,基于冻结系数和标准样本数据,R06,单图,scatter,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F002_pred_vs_actual.svg,,,300,sec_results,fig:pred_actual,figure_caption_bank.md,4.5,font_risk,active,system,,预测浓度与真实浓度对比,模型预测值与标准样本真实浓度的散点图，显示模型拟合精度。,Shows RMSE R06
F003,Q1,残差同方差性检验,残差计算,R05,单图,scatter,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F003_resid_fitted.svg,,,300,sec_diagnostics,fig:resid_fitted,figure_caption_bank.md,4.5,font_risk,active,system,,残差-拟合值图,残差对拟合值的散点图，用于检验同方差性假设。,Residual diagnostic R05
F003,Q1,残差同方差性检验,残差计算,R06,单图,scatter,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F003_resid_fitted.svg,,,300,sec_diagnostics,fig:resid_fitted,figure_caption_bank.md,4.5,font_risk,active,system,,残差-拟合值图,残差对拟合值的散点图，用于检验同方差性假设。,Residual diagnostic R06
F004,Q1,残差正态性检验,残差计算,R05,单图,qq,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F004_qq_resid.svg,,,300,sec_diagnostics,fig:qq,figure_caption_bank.md,4.5,font_risk,active,system,,残差Q-Q图,残差分位数-理论分位数图，检验残差正态性。,QQ plot R05
F004,Q1,残差正态性检验,残差计算,R06,单图,qq,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F004_qq_resid.svg,,,300,sec_diagnostics,fig:qq,figure_caption_bank.md,4.5,font_risk,active,system,,残差Q-Q图,残差分位数-理论分位数图，检验残差正态性。,QQ plot R06
F005,Q1,浓度与各通道线性关系,标准样本数据表,R02,一组散点图,scatter_matrix,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F005_channel_scatter.svg,,,300,sec_model,fig:scatter_matrix,figure_caption_bank.md,4.2,font_risk,active,system,,浓度与各颜色通道散点矩阵,浓度与R、G、B通道的散点图矩阵，展示线性关系。,Scatter matrix R02
F005,Q1,浓度与各通道线性关系,标准样本数据表,R03,一组散点图,scatter_matrix,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F005_channel_scatter.svg,,,300,sec_model,fig:scatter_matrix,figure_caption_bank.md,4.2,font_risk,active,system,,浓度与各颜色通道散点矩阵,浓度与R、G、B通道的散点图矩阵，展示线性关系。,Scatter matrix R03
F005,Q1,浓度与各通道线性关系,标准样本数据表,R04,一组散点图,scatter_matrix,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F005_channel_scatter.svg,,,300,sec_model,fig:scatter_matrix,figure_caption_bank.md,4.2,font_risk,active,system,,浓度与各颜色通道散点矩阵,浓度与R、G、B通道的散点图矩阵，展示线性关系。,Scatter matrix R04
F006,Q1,变量相关性热力图,标准样本数据表,R01,单图,heatmap,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F006_correlation_heatmap.svg,,,300,sec_model,fig:corr_heat,figure_caption_bank.md,4.2,font_risk,active,system,,变量相关性热力图,浓度及RGB通道之间的Pearson相关系数热力图。,Correlation heatmap R01
F006,Q1,变量相关性热力图,标准样本数据表,R05,单图,heatmap,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F006_correlation_heatmap.svg,,,300,sec_model,fig:corr_heat,figure_caption_bank.md,4.2,font_risk,active,system,,变量相关性热力图,浓度及RGB通道之间的Pearson相关系数热力图。,Correlation heatmap R05
F007,Q2,模型对比交叉验证RMSE,07_results/q2_comparison.csv,R07,单图,bar,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F007_model_comparison.svg,,,300,sec_model_comparison,fig:model_cmp,figure_caption_bank.md,4.5,font_risk,active,system,,三种模型留一交叉验证RMSE对比,线性回归、多项式回归、岭回归三种模型的留一交叉验证RMSE对比图。,Compares LOOCV RMSE R07
F007,Q2,模型对比交叉验证RMSE,07_results/q2_comparison.csv,R08,单图,bar,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F007_model_comparison.svg,,,300,sec_model_comparison,fig:model_cmp,figure_caption_bank.md,4.5,font_risk,active,system,,三种模型留一交叉验证RMSE对比,线性回归、多项式回归、岭回归三种模型的留一交叉验证RMSE对比图。,Compares LOOCV RMSE R08
F007,Q2,模型对比交叉验证RMSE,07_results/q2_comparison.csv,R09,单图,bar,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F007_model_comparison.svg,,,300,sec_model_comparison,fig:model_cmp,figure_caption_bank.md,4.5,font_risk,active,system,,三种模型留一交叉验证RMSE对比,线性回归、多项式回归、岭回归三种模型的留一交叉验证RMSE对比图。,Compares LOOCV RMSE R09
F008,Q3,预测区间可视化,07_results/q3_predictions.csv,R10,单图,errorbar,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F008_prediction_intervals.svg,,,300,sec_predictions,fig:pred_intervals,figure_caption_bank.md,4.5,font_risk,active,system,,待测样本预测浓度及95%预测区间,T01、T02、T03的点预测值和95%预测区间，显示不确定性范围。,Shows prediction R10
F008,Q3,预测区间可视化,07_results/q3_predictions.csv,R11,单图,errorbar,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F008_prediction_intervals.svg,,,300,sec_predictions,fig:pred_intervals,figure_caption_bank.md,4.5,font_risk,active,system,,待测样本预测浓度及95%预测区间,T01、T02、T03的点预测值和95%预测区间，显示不确定性范围。,Shows prediction R11
F008,Q3,预测区间可视化,07_results/q3_predictions.csv,R12,单图,errorbar,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F008_prediction_intervals.svg,,,300,sec_predictions,fig:pred_intervals,figure_caption_bank.md,4.5,font_risk,active,system,,待测样本预测浓度及95%预测区间,T01、T02、T03的点预测值和95%预测区间，显示不确定性范围。,Shows prediction R12
F008,Q3,预测区间可视化,07_results/q3_predictions.csv,R13,单图,errorbar,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F008_prediction_intervals.svg,,,300,sec_predictions,fig:pred_intervals,figure_caption_bank.md,4.5,font_risk,active,system,,待测样本预测浓度及95%预测区间,T01、T02、T03的点预测值和95%预测区间，显示不确定性范围。,Shows prediction R13
F008,Q3,预测区间可视化,07_results/q3_predictions.csv,R14,单图,errorbar,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F008_prediction_intervals.svg,,,300,sec_predictions,fig:pred_intervals,figure_caption_bank.md,4.5,font_risk,active,system,,待测样本预测浓度及95%预测区间,T01、T02、T03的点预测值和95%预测区间，显示不确定性范围。,Shows prediction R14
F008,Q3,预测区间可视化,07_results/q3_predictions.csv,R15,单图,errorbar,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F008_prediction_intervals.svg,,,300,sec_predictions,fig:pred_intervals,figure_caption_bank.md,4.5,font_risk,active,system,,待测样本预测浓度及95%预测区间,T01、T02、T03的点预测值和95%预测区间，显示不确定性范围。,Shows prediction R15
F008,Q3,预测区间可视化,07_results/q3_predictions.csv,R16,单图,errorbar,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F008_prediction_intervals.svg,,,300,sec_predictions,fig:pred_intervals,figure_caption_bank.md,4.5,font_risk,active,system,,待测样本预测浓度及95%预测区间,T01、T02、T03的点预测值和95%预测区间，显示不确定性范围。,Shows prediction R16
F008,Q3,预测区间可视化,07_results/q3_predictions.csv,R17,单图,errorbar,matplotlib,08_figures/scripts/generate_figures.py,08_
[truncated to 8000 chars]
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
3,problem_reviewer,Problem Coverage,10,10,none,0,None,None,closed,2026-06-04T18:00:00Z
3,model_reviewer,Model Rigor,10,10,none,0,None,None,closed,2026-06-04T18:00:00Z
3,code_reviewer,Code Reproducibility,9,10,minor,1,Insufficient code documentation,Add docstrings and comments to Python scripts,open,2026-06-04T18:00:00Z
3,figure_reviewer,Figure Quality,9,10,minor,1,Chinese font rendering unverified,Verify font rendering in SVGs and regenerate if needed,open,2026-06-04T18:00:00Z
3,paper_reviewer,Writing & Argumentation,9,10,minor,1,Minor language polish,Perform final language polish pass,open,2026-06-04T18:00:00Z
3,contract_auditor,Contract Integrity,1,10,fail,10,Multiple contract validation failures,"Resolve figure_contract result_id separators, add missing citation CIT02, fix polish_diff block, and correct simulated gate log formal_effect",open,2026-06-04T18:00:00Z
3,judge_reviewer,Overall Judgment,0,10,fail,8,Contract failures block submission,Fix all contract issues and re-run validation,open,2026-06-04T18:00:00Z
```

## 11_review/revision_tasks.csv

```text
task_id,round_id,reviewer,source_comment_id,severity,scope,target_artifact,target_location,issue_summary,required_action,acceptance_check,linked_contract_ids,status,assignee,created_time,closed_time,closure_note,human_waiver_by
RV-001,1,problem_reviewer,PRC-4;PRC-5;MRC-6;MRC-7;MRC-8;CRC-4,fail,code; results; paper,06_code/q2_model_comparison.py; 07_results/q2_comparison.csv; 09_paper/full_draft.md,Section 2.2; Section 4,Problem 2 required model comparison and overfitting discussion. Now implemented.,Already completed,1) q2_comparison.csv exists with RMSE for all three models; 2) Paper includes comparison and rationale; 3) Results R07-R09 registered; 4) Overfitting discussion present.,F02;F03,closed,system,2026-06-04T12:30:00Z,2026-06-04T16:00:00Z,Code and results present; paper updated with comparison and overfitting strategy.,
RV-002,1,problem_reviewer,PRC-7;MRC-4;CRC-5;JRC-1,fail,code; results; paper,06_code/q3_uncertainty.py; 09_paper/full_draft.md,Section 2.3; Section 3.3; Section 5,Problem 3 required uncertainty quantification and reusable protocol. Now implemented.,Already completed,1) Paper includes 95% PI for T01-T03; 2) Results R10-R18 registered; 3) Reusable protocol subsection present.,F01,closed,system,2026-06-04T12:30:00Z,2026-06-04T16:00:00Z,Code and predictions generated; protocol written and results registered.,
RV-003,1,problem_reviewer,PRC-8,major,contracts,14_contracts/result_contract.csv,new rows for predictions and intervals,Result contract lacked prediction rows. Now contains R07-R22.,Add missing result rows,result_contract.csv contains new rows for predictions intervals CV RMSE and coefficient SE.,,closed,system,2026-06-04T12:30:00Z,2026-06-04T16:00:00Z,Added R07-R22; all required results registered.,
RV-004,1,model_reviewer,MRC-4;MRC-5,major,results; paper,07_results/q1_metrics.csv; 09_paper/full_draft.md,Table 1; Section 2.1,Coefficient standard errors and p-values were missing. Now provided.,Provide standard errors t-stats p-values,Table 1 includes Std. Error t and p-value columns.,F01,closed,system,2026-06-04T12:30:00Z,2026-06-04T16:00:00Z,Generated q1_stats.csv; updated Table 1 and text.,
RV-005,1,model_reviewer,MRC-9;PRC-5,major,code; results; paper,06_code/cross_validation.py; 07_results/cv_results.csv; 09_paper/full_draft.md,Section 4,Cross-validation was missing. Now LOOCV implemented.,Perform LOOCV and report CV RMSE; add bootstrap discussion.,Paper Section 4 includes cross-validation RMSE and bootstrap discussion.,F01,closed,system,2026-06-04T12:30:00Z,2026-06-04T16:00:00Z,Cross-validation executed; CV RMSE=0.0748; bootstrap results added.,
RV-006,1,paper_reviewer,PaRC-7;PaRC-8,major,paper; contracts,14_contracts/citation_contract.csv; 09_paper/full_draft.md,References section,No references were cited. Now four references [1]-[4] included.,Add 3-5 citations and populate citation_contract.csv,citation_contract.csv has at least 3 entries; paper contains in-text citations.,,closed,system,2026-06-04T12:30:00Z,2026-06-04T16:00:00Z,Four references added; citation_contract.csv populated.,
RV-007,1,figure_reviewer,FRC-3;FRC-6,minor,figures,08_figures/main_figures/*.svg; 08_figures/scripts/generate_figures.py,all figure SVGs,Chinese font rendering risk noted. Verified and fixed.,Configure matplotlib Chinese font and regenerate SVGs.,Figures display Chinese labels correctly; font rendering verified.,,closed,system,2026-06-04T12:30:00Z,2026-06-04T16:00:00Z,Font configuration verified in generate_figures.py; SVGs generated with correct font.,
RV-008,1,paper_reviewer,PaRC-5;PaRC-6,minor,paper,09_paper/full_draft.md,Section 5 Conclusions,Conclusions used overconfident language. Hedging added.,Reword conclusions with hedging.,Conclusion paragraphs include hedging phrases; e.g., “可能”, “初步支持”.,,closed,system,2026-06-04T12:30:00Z,2026-06-04T16:00:00Z,Conclusions updated with appropriate hedging.,
RV-009,2,code_reviewer,CRC-review-001,minor,code,06_code/*.py,all code files,Code lacks inline comments and docstrings.,Add docstrings and comments.,Code files contain meaningful docstrings and comments.,,open,system,2026-06-04T16:00:00Z,,,Skipped in final_export; not blocking.
RV-010,2,figure_reviewer,FRC-review-001,minor,figures,08_figures/main_figures/*.svg,all SVGs,Chinese font rendering not verified in a target viewer.,Verify font rendering.,All figures render Chinese text correctly.,,open,system,2026-06-04T16:00:00Z,,,Skipped in final_export; not blocking.
RV-011,2,paper_reviewer,PaRC-review-001,minor,paper,09_paper/full_draft.md,throughout,Minor language polish desired.,Perform language polish.,Polished text has improved fluency.,,open,system,2026-06-04T16:00:00Z,,,Skipped in final_export; not blocking.
RV-012,2,system,CONTRACT-002–009,fail,contracts,14_contracts/figure_contract.csv; 14_contracts/claim_evidence_map.csv; 14_contracts/polish_diff_check.csv,contract bus,Contract validation failures blocking final export. Details in blocker note.,Fix figure result_id separators; repair claim C06 
[truncated to 5000 chars]
```

## 14_contracts/revision_tasks.csv

```text
task_id,round_id,reviewer,source_comment_id,severity,scope,target_artifact,target_location,issue_summary,required_action,acceptance_check,linked_contract_ids,status,assignee,created_time,closed_time,closure_note,human_waiver_by
RV-013,3,contract_auditor,CONTRACT-004–009,fail,contracts,14_contracts/figure_contract.csv,result_id column,"Figure contract uses semicolon-separated result_ids (e.g., ""R01;R02;R03;R04"") that fail validation because they are not individual entries.",Split result_id into individual rows or use an array format acceptable to validate_contracts.py,Every figure result_id is present individually in result_contract.csv.,"F001,F002,F003,F004,F007,F008",open,system,2026-06-04T18:00:00Z,,
RV-014,3,contract_auditor,CONTRACT-010,fail,contracts,14_contracts/claim_evidence_map.csv,C06,Claim C06 references citation_id=CIT02 which does not exist in citation_contract.csv.,Add CIT02 to citation_contract.csv or change claim to use existing citation.,validate_contracts.py reports no unsupported_claim for C06.,CIT02,open,system,2026-06-04T18:00:00Z,,
RV-015,3,contract_auditor,CONTRACT-011,fail,contracts,14_contracts/polish_diff_check.csv,POL-000,Polish diff check reports blocked with protected_atom_delta_count=0 possibly due to stale row.,Investigate and resolve the polish_diff_check.csv entry to clear the block.,validate_contracts.py no longer reports polish_changed_protected_atom.,,open,system,2026-06-04T18:00:00Z,,
RV-016,3,contract_auditor,VAL-002;VAL-003,fail,sandbox,11_review/simulated_human_gate_log.csv,"rows with formal_effect ≠ none","Simulated gate log rows have formal_effect='passed' or '确认' instead of 'none'.",Rewrite those rows to set formal_effect exactly 'none'.,Every simulated gate row has formal_effect=none.,,open,system,2026-06-04T18:00:00Z,,
RV-017,3,code_reviewer,CRC-001,minor,code,06_code/*.py,all code files,Code lacks inline comments and docstrings.,Add docstrings and comments.,Code files contain meaningful docstrings and comments.,,open,system,2026-06-04T18:00:00Z,,
RV-018,3,figure_reviewer,FRC-001,minor,figures,08_figures/main_figures/*.svg,all SVGs,Chinese font rendering not verified in target viewer.,Verify and regenerate if needed.,Figures display Chinese labels correctly.,,open,system,2026-06-04T18:00:00Z,,
RV-019,3,paper_reviewer,PaRC-001,minor,paper,09_paper/full_draft.md,throughout,Minor language polish desired.,Perform language polish pass.,Polished text has improved fluency while preserving meaning.,,open,system,2026-06-04T18:00:00Z,,
RV-020,3,contract_auditor,VAL-001,minor,sandbox,12_submission/final_submit_paper.md,entire file,"Validation expects at least 2500 chars and 7 sections; current file likely meets both but queue open.",Re-validate and close if criteria satisfied.,final_submit_paper.md has at least 2500 chars and ≥7 sections.,,open,system,2026-06-04T18:00:00Z,,
```

