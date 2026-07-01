# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX\workspace`
Run dir: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX`
Call id: `initial_11_auto_review`
Iteration: 1
Max iterations: 5
Current simulated stage: `auto_review`
Stage order: 11
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX/reports/prompt_route_manifest.md`
Training sandbox stage prompt bundle: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX/reports/stage_prompt_bundle.md`

Rules:
- Follow only deep_sequential behavior for this stage.
- Do not edit `00_problem/problem_statement.md` or `00_problem/inbox/`; write intake analysis to `01_task_analysis/`.
- A formal human gate becomes a simulated sandbox gate. Record it in `11_review/simulated_human_gate_log.csv`.
- Update contracts before writing paper claims, result analysis, figures, or submission text.
- Use the Workspace Context Snapshot below as the current file context; do not request read_file/list_files pseudo-tools.
- Reply only through runner file actions. The external runner will reject prose-only or pseudo-tool responses.

Stage output target:
- Create or update the artifacts normally owned by `auto_review`.
- If this stage cannot close a blocker, update review/revision artifacts with a concrete blocker note.
- Keep `reports/training_enhancement_points.csv` current once a full draft or review finding exists.

Stage-specific required outputs:
- Write current `11_review/review_scorecard.csv` and `14_contracts/revision_tasks.csv`; do not leave stale fail rows from earlier missing artifacts.
- Review scorecard rows should use score/max_score and must be at least 85% after the sandbox artifacts are fixed; on a 10-point scale use 9 or 10 for pass, otherwise keep the item as an open blocker.
- Write `11_review/simulated_human_gate_log.csv` with columns stage_id, gate_id, agent_decision, evidence, residual_risk, formal_effect.
- Every simulated gate row must set formal_effect to `none`; never use confirmed/approved as a formal workflow effect.

# Workspace Context Snapshot

This bounded snapshot is the API agent's read context for the current stage. Use it instead of pseudo-tools or file-read requests.

## Workspace File Listing

- 07_results/.gitkeep (0 bytes)
- 07_results/logs/.gitkeep (0 bytes)
- 07_results/logs/generate_latex_template.log (152 bytes)
- 07_results/logs/q1_run.log (421 bytes)
- 07_results/metrics/.gitkeep (0 bytes)
- 07_results/metrics_summary.csv (92 bytes)
- 07_results/q1_coefficients.csv (77 bytes)
- 07_results/q1_metrics.csv (49 bytes)
- 07_results/q1_results.csv (74 bytes)
- 07_results/q2_results.csv (74 bytes)
- 07_results/q3_results.csv (74 bytes)
- 07_results/result_freeze_report.md (2523 bytes)
- 07_results/result_source_map.csv (201 bytes)
- 07_results/tables/.gitkeep (0 bytes)
- 08_figures/appendix_figures/.gitkeep (0 bytes)
- 08_figures/chart_blueprint.csv (605 bytes)
- 08_figures/chart_type_library.md (1653 bytes)
- 08_figures/eda_figures/.gitkeep (0 bytes)
- 08_figures/export/pdf_vector/.gitkeep (0 bytes)
- 08_figures/export/png_300dpi/.gitkeep (0 bytes)
- 08_figures/export/svg_vector/.gitkeep (0 bytes)
- 08_figures/figure_caption_bank.md (225 bytes)
- 08_figures/figure_design_review.csv (300 bytes)
- 08_figures/figure_status.csv (247 bytes)
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
- 08_figures/mermaid/.gitkeep (0 bytes)
- 08_figures/mermaid/workflow_map.mmd (284 bytes)
- 08_figures/model_chart_priority_matrix.csv (1558 bytes)
- 08_figures/output/.gitkeep (0 bytes)
- 08_figures/palette_library.yaml (1500 bytes)
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
- 09_paper/consistency_risk_report.md (2722 bytes)
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
- 09_paper/full_draft.md (8423 bytes)
- 09_paper/human_rewrite_log.md (139 bytes)
- 09_paper/missing_evidence_report.md (1455 bytes)
- 09_paper/outline.md (728 bytes)
- 09_paper/paper_block_map.csv (245 bytes)
- 09_paper/paper_draft_stage_summary.md (1032 bytes)
- 09_paper/polish_diff_log.md (144 bytes)
- 09_paper/polish_plan.md (237 bytes)
- 09_paper/polish_tasks.csv (232 bytes)
- 09_paper/section_weight_profiles.csv (2354 bytes)
- 09_paper/unresolved_review_issues.md (1199 bytes)
- 11_review/.gitkeep (0 bytes)
- 11_review/code_reviewer_comments.md (230 bytes)
- 11_review/contract_validation_report.json (145 bytes)
- 11_review/contract_validation_report.md (148 bytes)
- 11_review/figure_reviewer_comments.md (244 bytes)
- 11_review/figures_stage_summary.md (2049 bytes)
- 11_review/final_submission_checklist.md (206 bytes)
- 11_review/gate_report.json (123 bytes)
- 11_review/judge_reviewer_comments.md (219 bytes)
- 11_review/latex_template_stage_summary.md (331 bytes)
- 11_review/model_reviewer_comments.md (225 bytes)
- 11_review/paper_full_stage_summary.md (1302 bytes)
- 11_review/paper_reviewer_comments.md (225 bytes)
- 11_review/prior_copy_risk_report.md (196 bytes)
- 11_review/prior_retrieval_stage_summary.md (969 bytes)
- 11_review/problem_reviewer_comments.md (224 bytes)
- 11_review/review_scorecard.csv (110 bytes)
- 11_review/revision_tasks.csv (228 bytes)
- 11_review/simulated_human_gate_log.csv (2245 bytes)
- 11_review/skill_router_report.json (5728 bytes)
- 11_review/skill_router_report.md (356 bytes)
- 12_submission/ai_usage_detail.pdf (2757 bytes)
- 12_submission/code_package/.gitkeep (0 bytes)
- 12_submission/data_package/.gitkeep (0 bytes)
- 12_submission/figure_package/.gitkeep (0 bytes)
- 12_submission/final_submit_package.md (313 bytes)
- 12_submission/submission_checklist.md (477 bytes)

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

## 14_contracts/result_contract.csv

```text
result_id,question_id,model_id,metric_name,metric_value,unit,source_file,source_row_or_cell,code_file,run_id,random_seed,assumption_ids,used_by_figure_ids,used_by_claim_ids,freeze_status,freeze_time,owner,notes
R01,Q1,linear_OLS,coefficient_Intercept,1.067247,dimensionless,07_results/q1_coefficients.csv,row 1,06_code/q1_linear_model.py,run_001,deterministic,F01,,,frozen,2026-06-04T12:00:00Z,system,validated source value 1.067247 from q1_coefficients.csv row 1; OLS intercept coefficient
R02,Q1,linear_OLS,coefficient_R,-1.821404,dimensionless,07_results/q1_coefficients.csv,row 2,06_code/q1_linear_model.py,run_001,deterministic,F01,,,frozen,2026-06-04T12:00:00Z,system,validated source value -1.821404 from q1_coefficients.csv row 2; R channel coefficient
R03,Q1,linear_OLS,coefficient_G,0.995618,dimensionless,07_results/q1_coefficients.csv,row 3,06_code/q1_linear_model.py,run_001,deterministic,F01,,,frozen,2026-06-04T12:00:00Z,system,validated source value 0.995618 from q1_coefficients.csv row 3; G channel coefficient
R04,Q1,linear_OLS,coefficient_B,5.630987,dimensionless,07_results/q1_coefficients.csv,row 4,06_code/q1_linear_model.py,run_001,deterministic,F01,,,frozen,2026-06-04T12:00:00Z,system,validated source value 5.630987 from q1_coefficients.csv row 4; B channel coefficient
R05,Q1,linear_OLS,R_squared,0.997747,dimensionless,07_results/q1_metrics.csv,row 1,06_code/q1_linear_model.py,run_001,deterministic,F01,,,frozen,2026-06-04T12:00:00Z,system,validated source value 0.997747 from q1_metrics.csv row 1; OLS R-squared
R06,Q1,linear_OLS,RMSE,0.067418,mg/L,07_results/q1_metrics.csv,row 2,06_code/q1_linear_model.py,run_001,deterministic,F01,,,frozen,2026-06-04T12:00:00Z,system,validated source value 0.067418 from q1_metrics.csv row 2; OLS RMSE
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
figure_id,question_id,core_claim,evidence_source,result_id,panel_plan,chart_type,backend,script_path,output_svg,output_png,output_pdf,dpi,used_in_section,latex_label,caption_source,quality_score,review_risk,status,owner,last_checked
F001,Q1,OLS系数估计值与方向,07_results/q1_coefficients.csv,R01;R02;R03;R04,单图,bar,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F001_coefficient_bar.svg,,,300,sec_model,fig:coef,figure_caption_bank.md,4.5,font_risk,active,system,
F002,Q1,模型预测值与真实值对比,基于冻结系数和标准样本数据,R05;R06,单图,scatter,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F002_pred_vs_actual.svg,,,300,sec_results,fig:pred_actual,figure_caption_bank.md,4.5,font_risk,active,system,
F003,Q1,残差同方差性检验,残差计算,R05;R06,单图,scatter,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F003_resid_fitted.svg,,,300,sec_diagnostics,fig:resid_fitted,figure_caption_bank.md,4.5,font_risk,active,system,
F004,Q1,残差正态性检验,残差计算,R05;R06,单图,qq,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F004_qq_resid.svg,,,300,sec_diagnostics,fig:qq,figure_caption_bank.md,4.5,font_risk,active,system,
F005,Q1,浓度与各通道线性关系,标准样本数据表,,一组散点图,scatter_matrix,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F005_channel_scatter.svg,,,300,sec_model,fig:scatter_matrix,figure_caption_bank.md,4.2,font_risk,active,system,
F006,Q1,变量相关性热力图,标准样本数据表,,单图,heatmap,matplotlib,08_figures/scripts/generate_figures.py,08_figures/main_figures/F006_correlation_heatmap.svg,,,300,sec_model,fig:corr_heat,figure_caption_bank.md,4.2,font_risk,active,system,
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
```

## 11_review/revision_tasks.csv

```text
task_id,round_id,reviewer,source_comment_id,severity,scope,target_artifact,target_location,issue_summary,required_action,acceptance_check,linked_contract_ids,status,assignee,created_time,closed_time,closure_note,human_waiver_by
```

## 14_contracts/revision_tasks.csv

```text
task_id,round_id,reviewer,source_comment_id,severity,scope,target_artifact,target_location,issue_summary,required_action,acceptance_check,linked_contract_ids,status,assignee,created_time,closed_time,closure_note,human_waiver_by
```

## 09_paper/full_draft.md

```text
# 颜色通道与物质浓度的辨识模型研究

## 摘要

基于某检测设备输出的归一化颜色通道（R、G、B）与标准溶液浓度数据，本研究建立了一阶线性回归模型用于浓度辨识。模型在标准样本（0.5−5.0 mg/L）上取得决定系数 R² = 0.9977，均方根误差 RMSE = 0.0674 mg/L，表明颜色通道能够高精度地解释浓度变异。系数分析揭示：R 通道与浓度呈显著负相关（系数 −1.8214），B 通道是浓度预测的主导正向因子（系数 5.6310），G 通道影响相对温和（系数 0.9956）。利用该模型对待测样本 T01、T02、T03 的点预测浓度分别为 1.61、3.17 和 4.38 mg/L。受限于当前执行进度，问题二要求的多模型比较和问题三要求的不确定性量化尚未完成，相应缺口已单独标记，供后续审稿与补证。全文图表、公式和关键论断均与合同系统绑定，确保可追溯与可复现。

**关键词**：颜色通道；浓度辨识；线性回归；模型诊断；缺失证据

## 1 问题分析

某检测设备对不同浓度溶液成像后，输出三个归一化颜色通道 R、G、B。现给出 10 个标准样本的真实浓度及颜色读数，以及 3 个待测样本的颜色读数。需要解决三个递进问题：

- **问题一**：分析颜色通道与浓度的关系，建立可解释的浓度预测模型，并说明各通道的作用方向；
- **问题二**：比较至少三类候选模型（如线性回归、多项式回归、集成回归等）的预测误差，给出模型选择依据，并说明小样本过拟合风险控制策略；
- **问题三**：预测 T01、T02、T03 的浓度，提供不确定性说明，并提出可复用的检测流程建议。

标准样本浓度范围为 0.5–5.0 mg/L，R 通道随浓度增加单调下降，G 和 B 通道单调上升，呈现强烈的线性趋势（图F005、图F006）。因此，以多元线性回归作为基准模型具有合理性和可解释性。

## 2 模型建立

### 2.1 问题一：多元线性回归模型

建立三变量线性回归模型（公式 F01）：

$$
C = \beta_0 + \beta_1 R + \beta_2 G + \beta_3 B + \varepsilon
$$

其中 $C$ 为浓度预测值，$\varepsilon$ 为随机误差项。基于 10 个标准样本，采用普通最小二乘法（OLS）估计系数，结果列于表1。

**表1 线性回归系数估计值**
| 变量 | 系数 | 含义             |
|------|-------|------------------|
| 截距 | 1.0672 | 基准浓度         |
| R    | -1.8214 | 红色通道影响，负向 |
| G    | 0.9956  | 绿色通道影响，正向 |
| B    | 5.6310  | 蓝色通道影响，正向 |

该模型对应的决定系数 R² = 0.9977，表明颜色通道联合解释了 99.77% 的浓度变异；RMSE = 0.0674 mg/L，在 0.5–5.0 mg/L 的浓度范围内相对误差较低。系数方向明确：R 通道升高（溶液颜色偏红）会降低预测浓度，而 G、B 通道升高则提高预测浓度，且 B 通道的边际效应最强。该结果与直觉一致——高浓度物质使溶液颜色变蓝（R 降低、B 升高）。图F001 以条形图展示了各系数大小和方向，图F005 展示了浓度与各通道的散点关系，图F006 给出了变量间的相关性热力图。

### 2.2 问题二：多模型比较计划

为满足问题二，拟比较以下三类模型：

1. **多元线性回归**（已有，基准模型）；
2. **二阶多项式回归**（含交互项，公式 F02）；
3. **岭回归或 LASSO** 等正则化方法，以考察小样本下的稳定性。

理想情况下，应使用留一交叉验证（LOOCV）或 K 折交叉验证比较各模型的 RMSE（公式 F03），并结合 AIC/BIC 等准则避免过拟合。然而，截至本文撰写，上述实验代码尚未执行或结果未冻结，因此**问题二的数值比较结论暂时缺失**。该缺口将纳入审稿前待办清单，待补充后重新评估模型优选。

### 2.3 问题三：待测样本预测方法

利用 2.1 节建立的线性模型，可以直接计算待测样本的点预测值：

$$
\hat{C}_{T} = 1.0672 - 1.8214 \cdot R_T + 0.9956 \cdot G_T + 5.6310 \cdot B_T
$$

不确定性量化通常需要回归系数的标准误差、残差标准差等统计量，进而构建置信区间或预测区间。由于这些统计量尚未从模型拟合输出中完整提取并冻结，**当前仅给出点预测，不确定性说明暂缺**。

## 3 结果分析

### 3.1 模型拟合与系数解释

如表1所示，所有系数的符号和量级均具有明确的物理可解释性。R 通道的负系数说明红色分量越多，溶液浓度越低；这与标准样本中 R 值随浓度增加单调递减的观测一致。B 通道系数高达 5.63，意味着蓝色通道每增加一个单位（归一化），预测浓度增加约 5.63 mg/L，体现了 B 通道对浓度变化的高度敏感性。

模型整体拟合优度（R²=0.9977）接近 1，表明线性假设在当前数据上非常成立。预测值与真实值的对比（图F002）直观展示了模型的高精度，几乎所有点都紧贴对角线。RMSE 仅为 0.0674 mg/L，对于 mg/L 级别的浓度测量，该误差水平在可接受范围。

### 3.2 模型诊断

为评估线性回归基本假设的满足情况，绘制了残差-拟合值散点图（图F003）和残差正态 Q-Q 图（图F004）。图F003 未呈现明显的“喇叭口”或曲线模式，初步支持同方差性和线性假设。图F004 中残差分位数大致沿对角线分布，提示残差分布接近正态，但样本量仅 10 个，正态性检验效力有限。整体而言，模型诊断未发现严重违反 OLS 假设的证据，但小样本下的稳健性需要更多实验（如 Bootstrap）来验证。

### 3.3 待测样本预测

基于线性模型计算得到以下点预测结果：

**表2 待测样本浓度预测**
| 样本编号 | R    | G    | B    | 预测浓度 (mg/L) |
|----------|------|------|------|-----------------|
| T01      | 0.77 | 0.37 | 0.28 | 1.61            |
| T02      | 0.58 | 0.57 | 0.46 | 3.17            |
| T03      | 0.45 | 0.70 | 0.61 | 4.38            |

预测值均在标准样本浓度范围（0.5–5.0 mg/L）之内，且排序符合通道变化趋势，未出现异常外推。但在没有预测区间的情况下，这些点值不应被视为精确的真值，实际应用时应进行多次重复实验或扩展标准点以标定不确定性。

## 4 验证与敏感性分析

受限于当前只完成了线性模型的基础拟合，本章节内容存在大量缺口：

- **交叉验证**：未执行任何重抽样验证，无法评估模型的外推泛化误差。
- **敏感性分析**：未对系数进行扰动分析或 Bootstrap 置信区间计算，难以判断各通道贡献的统计显著性。
- **模型比较**：如 2.2 节所述，多模型评估实验未完成。

这些缺口可能导致模型评价过于乐观（过拟合风险未被定量评估），也使得问题二和问题三的要求无法完全满足。建议在后续工作中优先执行留一交叉验证、提取标准误差并绘制预测区间。

## 5 结论

本研究使用多元线性回归模型成功建立了颜色通道（R、G、B）到物质浓度的定量关系。主要结论包括：

1. 颜色通道与浓度之间存在极强的线性关联（R² ≈ 0.998），且各通道的作用方向明确：R 通道负向，G、B 通道正向，其中 B 通道的边际效应最大。
2. 模型诊断（残差图、Q-Q 图）未发现明显违反回归假设的迹象，但样本量较小，诊断效力有限。
3. 利用该模型对待测样本 T01–T03 的点预测浓度分别为 1.61、3.17、4.38 mg/L，可作为后续实验的参考基准。
4. 由于多模型比较、不确定性量化和验证实验尚未完成，当前结果的完整性和鲁棒性有待进一步补证。

综上所述，线性回归为颜色浓度辨识提供了一个简单高效且可解释的基准方案，但完整的问题求解仍需补充缺失的证据链。本文所记录的结构化缺口将直接作为审稿阶段的重点待办事项，以确保最终成果满足竞赛或期刊的严谨性要求。

**附录**：标准样本数据及生成的图表已归档至对应合同，详见 `14_contracts/` 下的绑定记录。
```

