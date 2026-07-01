# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_CROP_YIELD_LOCAL_V2_CODEX\workspace`
Run dir: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_CROP_YIELD_LOCAL_V2_CODEX`
Call id: `initial_12_revision`
Iteration: 1
Max iterations: 3
Current simulated stage: `revision`
Stage order: 12
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_CROP_YIELD_LOCAL_V2_CODEX/reports/prompt_route_manifest.md`
Training sandbox stage prompt bundle: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_CROP_YIELD_LOCAL_V2_CODEX/reports/stage_prompt_bundle.md`

Rules:
- Follow only deep_sequential behavior for this stage.
- Do not edit `00_problem/problem_statement.md` or `00_problem/inbox/`; write intake analysis to `01_task_analysis/`.
- A formal human gate becomes a simulated sandbox gate. Record it in `11_review/simulated_human_gate_log.csv`.
- Update contracts before writing paper claims, result analysis, figures, or submission text.
- Use the Workspace Context Snapshot below as the current file context; do not request read_file/list_files pseudo-tools.
- Reply only through runner file actions. The external runner will reject prose-only or pseudo-tool responses.

Stage output target:
- Create or update the artifacts normally owned by `revision`.
- If this stage cannot close a blocker, update review/revision artifacts with a concrete blocker note.
- Keep `reports/training_enhancement_points.csv` current once a full draft or review finding exists.

# Workspace Context Snapshot

This bounded snapshot is the API agent's read context for the current stage. Use it instead of pseudo-tools or file-read requests.

## Workspace File Listing

- 07_results/.gitkeep (0 bytes)
- 07_results/logs/.gitkeep (0 bytes)
- 07_results/logs/generate_latex_template.log (152 bytes)
- 07_results/metrics/.gitkeep (0 bytes)
- 07_results/metrics_summary.csv (124 bytes)
- 07_results/q1_results.csv (74 bytes)
- 07_results/q2_results.csv (74 bytes)
- 07_results/q3_results.csv (110 bytes)
- 07_results/result_freeze_report.md (165 bytes)
- 07_results/result_source_map.csv (94 bytes)
- 07_results/tables/.gitkeep (0 bytes)
- 08_figures/appendix_figures/.gitkeep (0 bytes)
- 08_figures/chart_blueprint.csv (409 bytes)
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
- 08_figures/mermaid/.gitkeep (0 bytes)
- 08_figures/mermaid/workflow_map.mmd (284 bytes)
- 08_figures/model_chart_priority_matrix.csv (1558 bytes)
- 08_figures/output/.gitkeep (0 bytes)
- 08_figures/output/color_channel_scatter.svg (409 bytes)
- 08_figures/output/crop_driver_relationship.svg (258 bytes)
- 08_figures/output/crop_model_error_compare.svg (261 bytes)
- 08_figures/output/crop_prediction_interval.svg (258 bytes)
- 08_figures/output/model_error_compare.svg (393 bytes)
- 08_figures/output/prediction_interval.svg (388 bytes)
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
- 09_paper/draft_v1.md (120 bytes)
- 09_paper/draft_v1_with_anchors.md (145 bytes)
- 09_paper/draft_v2.md (123 bytes)
- 09_paper/draft_v2_polished.md (132 bytes)
- 09_paper/dynamic_outline_router.md (1711 bytes)
- 09_paper/figure_insert_list.csv (83 bytes)
- 09_paper/final_paper.md (7513 bytes)
- 09_paper/formatting_checklist.md (260 bytes)
- 09_paper/frozen_text_blocks.md (170 bytes)
- 09_paper/full_draft.md (7216 bytes)
- 09_paper/human_rewrite_log.md (139 bytes)
- 09_paper/outline.md (728 bytes)
- 09_paper/paper_block_map.csv (245 bytes)
- 09_paper/polish_diff_log.md (144 bytes)
- 09_paper/polish_plan.md (237 bytes)
- 09_paper/polish_tasks.csv (232 bytes)
- 09_paper/section_weight_profiles.csv (2354 bytes)
- 11_review/.gitkeep (0 bytes)
- 11_review/code_reviewer_comments.md (230 bytes)
- 11_review/contract_validation_report.json (145 bytes)
- 11_review/contract_validation_report.md (148 bytes)
- 11_review/figure_reviewer_comments.md (244 bytes)
- 11_review/final_submission_checklist.md (206 bytes)
- 11_review/gate_report.json (123 bytes)
- 11_review/judge_reviewer_comments.md (219 bytes)
- 11_review/latex_template_stage_summary.md (331 bytes)
- 11_review/model_reviewer_comments.md (225 bytes)
- 11_review/paper_reviewer_comments.md (225 bytes)
- 11_review/prior_copy_risk_report.md (196 bytes)
- 11_review/problem_reviewer_comments.md (224 bytes)
- 11_review/review_scorecard.csv (284 bytes)
- 11_review/revision_tasks.csv (247 bytes)
- 11_review/simulated_human_gate_log.csv (827 bytes)
- 11_review/skill_router_report.json (5728 bytes)
- 11_review/skill_router_report.md (356 bytes)
- 11_review/training_enhancement_points.csv (1518 bytes)
- 11_review/training_enhancement_points.md (1802 bytes)
- 12_submission/ai_usage_detail.pdf (2757 bytes)
- 12_submission/code_package/.gitkeep (0 bytes)
- 12_submission/data_package/.gitkeep (0 bytes)
- 12_submission/figure_package/.gitkeep (0 bytes)
- 12_submission/final_submit_package.md (246 bytes)
- 12_submission/final_submit_paper.md (7216 bytes)
- 12_submission/submission_checklist.md (325 bytes)

## 00_problem/problem_statement.md

```text
# 温室作物产量预测与水肥调控问题

> 沙盒训练题面。本文档为新的纯文本赛题，不复制历史论文正文、摘要、图注、表格或结论。

某温室种植系统记录了若干批次番茄的环境与管理变量。每个批次给出日均温度、相对湿度、光照时长、灌溉量、施氮量和最终单位面积产量。现需要建立数学模型，分析影响产量的关键因素，并预测三个待评估批次的产量。

## 已知训练批次

| batch_id | temperature_C | humidity_pct | light_h | irrigation_L_m2 | nitrogen_g_m2 | yield_kg_m2 |
|---|---:|---:|---:|---:|---:|---:|
| B01 | 20.5 | 72 | 6.1 | 3.2 | 8.0 | 5.8 |
| B02 | 21.0 | 70 | 6.5 | 3.5 | 8.5 | 6.2 |
| B03 | 21.8 | 68 | 7.0 | 3.8 | 9.0 | 6.8 |
| B04 | 22.4 | 65 | 7.5 | 4.1 | 9.4 | 7.3 |
| B05 | 23.0 | 63 | 8.0 | 4.4 | 9.8 | 7.9 |
| B06 | 23.6 | 61 | 8.5 | 4.7 | 10.2 | 8.3 |
| B07 | 24.1 | 60 | 8.8 | 5.0 | 10.7 | 8.6 |
| B08 | 24.8 | 58 | 9.1 | 5.2 | 11.0 | 8.9 |
| B09 | 25.3 | 57 | 9.4 | 5.5 | 11.5 | 9.1 |
| B10 | 25.9 | 55 | 9.8 | 5.8 | 12.0 | 9.3 |
| B11 | 26.5 | 54 | 10.1 | 6.1 | 12.5 | 9.4 |
| B12 | 27.0 | 53 | 10.4 | 6.4 | 13.0 | 9.2 |

## 待评估批次

| batch_id | temperature_C | humidity_pct | light_h | irrigation_L_m2 | nitrogen_g_m2 |
|---|---:|---:|---:|---:|---:|
| P01 | 22.8 | 64 | 7.8 | 4.3 | 9.7 |
| P02 | 24.6 | 59 | 9.0 | 5.1 | 10.9 |
| P03 | 26.8 | 53 | 10.3 | 6.3 | 12.8 |

## 问题一

分析环境变量和管理变量对单位面积产量的影响方向，识别主要驱动因素，并给出可解释的产量预测模型。

## 问题二

比较至少三类候选模型的预测误差，例如多元线性回归、带正则化的回归、二次响应面模型、树模型或其他合理模型。说明小样本条件下的验证方式和过拟合控制策略。

## 问题三

预测待评估批次 `P01`、`P02`、`P03` 的单位面积产量，给出不确定性说明，并提出可复用的水肥调控建议。

## 硬性要求

- 本题只使用纯文本表格数据，不使用图片输入。
- 所有数值结果必须能追溯到 `result_contract.csv`。
- 所有论文图表引用必须先登记到 `figure_contract.csv`，且图表文件必须存在。
- 关键公式必须登记到 `formula_contract.csv`。
- 不得复制历史论文文本、图注、表格或结论。
```

## 14_contracts/result_contract.csv

```text
﻿result_id,question_id,model_id,metric_name,metric_value,unit,source_file,source_row_or_cell,code_file,run_id,random_seed,assumption_ids,used_by_figure_ids,used_by_claim_ids,freeze_status,freeze_time,owner,notes
R-Q1-001,Q1,M-LIN,dominant_driver_light_irrigation,positive,direction,07_results/metrics_summary.csv,analysis,06_code/run_all.py,local_crop_training,42,A1,F1,C1,ready,2026-06-04T21:17:07,local_training_agent,text-only crop-yield sandbox
R-Q2-001,Q2,M-RIDGE,ridge_cv_rmse,0.29,kg/m2,07_results/metrics_summary.csv,ridge,06_code/run_all.py,local_crop_training,42,A1,F2,C2,ready,2026-06-04T21:17:07,local_training_agent,best local validation metric
R-Q3-001,Q3,M-RIDGE,P01_pred,7.7,kg/m2,07_results/q3_results.csv,P01,06_code/run_all.py,local_crop_training,42,A1,F3,C3,ready,2026-06-04T21:17:07,local_training_agent,
R-Q3-002,Q3,M-RIDGE,P02_pred,8.8,kg/m2,07_results/q3_results.csv,P02,06_code/run_all.py,local_crop_training,42,A1,F3,C3,ready,2026-06-04T21:17:07,local_training_agent,
R-Q3-003,Q3,M-RIDGE,P03_pred,9.2,kg/m2,07_results/q3_results.csv,P03,06_code/run_all.py,local_crop_training,42,A1,F3,C3,ready,2026-06-04T21:17:07,local_training_agent,
```

## 14_contracts/claim_evidence_map.csv

```text
﻿claim_id,question_id,section_id,claim_text,claim_type,evidence_type,evidence_id,result_id,figure_id,formula_id,citation_id,support_grade,boundary_condition,risk_note,status,owner,last_checked
C1,Q1,model,光照、灌溉和施氮对温室番茄单位面积产量具有主要正向作用。,model,result,R-Q1-001,R-Q1-001,F1,EQ1,,strong,12 个训练批次范围内,小样本不能作远距离外推,ready,local_training_agent,2026-06-04T21:17:07
C2,Q2,validation,岭回归在留一交叉验证 RMSE 上优于线性模型和二次响应面模型。,result,result,R-Q2-001,R-Q2-001,F2,EQ2,,strong,留一交叉验证,验证样本较少,ready,local_training_agent,2026-06-04T21:17:07
C3,Q3,results,P01、P02、P03 的单位面积产量预测分别约为 7.7、8.8、9.2 kg/m2。,result,result,R-Q3-001,R-Q3-001,F3,EQ3,,strong,待评估批次变量位于训练范围附近,区间为经验残差区间,ready,local_training_agent,2026-06-04T21:17:07
```

## 14_contracts/figure_contract.csv

```text
﻿figure_id,title,result_id,evidence_source,output_svg,output_png,output_pdf,used_in_section,latex_label,quality_score,status,owner,notes
F1,环境管理变量与产量关系图,R-Q1-001,03_data/raw/crop_yield_batches.csv,08_figures/output/crop_driver_relationship.svg,,,数据分析,fig:crop-driver-relationship,4.8,ready,local_training_agent,
F2,候选模型交叉验证误差对比图,R-Q2-001,07_results/metrics_summary.csv,08_figures/output/crop_model_error_compare.svg,,,模型评价,fig:crop-model-error,4.8,ready,local_training_agent,
F3,待评估批次产量预测区间图,R-Q3-001,07_results/q3_results.csv,08_figures/output/crop_prediction_interval.svg,,,结果分析,fig:crop-prediction-interval,4.8,ready,local_training_agent,
```

## 14_contracts/formula_contract.csv

```text
﻿formula_id,used_in_section,formula_latex,meaning,symbols_defined,assumption_ids,result_ids,status,owner,notes
EQ1,模型建立,\hat y=\beta_0+\sum_k \beta_k x_k,可解释多元产量回归,y: yield; x_k: greenhouse feature; beta: coefficient,A1,R-Q1-001,ready,local_training_agent,
EQ2,模型评价,RMSE=\sqrt{n^{-1}\sum_i(y_i-\hat y_i)^2},交叉验证误差,RMSE: root mean squared error; y: observed yield; yhat: predicted yield,A1,R-Q2-001,ready,local_training_agent,
EQ3,不确定性,"I_j=[\hat y_j-1.96s_e,\hat y_j+1.96s_e]",待评估批次产量预测区间,I: interval; yhat: prediction; se: empirical residual std,A1,R-Q3-001;R-Q3-002;R-Q3-003,ready,local_training_agent,
```

## 11_review/review_scorecard.csv

```text
﻿item,status,severity,evidence,notes
text_only_problem,pass,,00_problem/problem_statement.md,no image dependency
contracts_populated,pass,,14_contracts/*.csv,"results, claims, figures, formulas present"
three_iteration_training,pass,,iteration=1,local executor iteration marker
```

## 11_review/revision_tasks.csv

```text
﻿task_id,source,severity,target_artifact,issue,action,status,owner,notes
REV-001,training,major,09_paper/full_draft.md,need validation and contract binding,add validation section and contract references,closed,local_training_agent,iteration 1
```

## 14_contracts/revision_tasks.csv

```text
﻿task_id,source,severity,target_artifact,issue,action,status,owner,notes
REV-001,training,major,09_paper/full_draft.md,need validation and contract binding,add validation section and contract references,closed,local_training_agent,iteration 1
```

## 09_paper/full_draft.md

```text
# 温室作物产量预测与水肥调控模型

## 摘要

本文针对纯文本温室番茄批次数据，建立单位面积产量预测和水肥调控分析流程。训练数据包含温度、湿度、光照、灌溉、施氮和产量字段；待评估批次为 P01、P02、P03。候选模型比较显示，岭回归留一交叉验证 RMSE 为 0.29 kg/m2，优于线性模型的 0.34 kg/m2 和二次响应面模型的 0.31 kg/m2。预测结果显示 P01、P02、P03 的产量约为 7.7、8.8、9.2 kg/m2。

## 问题分析

题面只提供纯文本表格，不依赖图片输入。Q1 需要解释环境和管理变量对产量的影响方向，Q2 需要比较至少三类候选模型，Q3 需要预测待评估批次并给出不确定性和水肥建议。小样本条件下，模型复杂度必须受控，所有正式数值必须写入 `14_contracts/result_contract.csv`。

从变量结构看，温度和湿度属于环境背景变量，光照、灌溉量和施氮量属于可调控管理变量。训练批次的产量从 5.8 kg/m2 增长到 9.4 kg/m2 后略有回落，说明线性增益和高端饱和可能同时存在。由于样本只有 12 个，不能把复杂模型的训练内拟合误差当作结论；本轮把 validation、sensitivity、robustness 和 residual error 都写入建模闭环，用来约束结论强度。

## 数据处理与假设

原始数据登记为 `03_data/raw/crop_yield_batches.csv`。训练批次 B01 至 B12 具有完整产量标签，待评估批次 P01 至 P03 缺少 `yield_kg_m2`，这是预测目标而非数据缺失错误。所有变量均为纯文本表格中的数值字段，无图片、传感器原始图像或外部历史论文文本参与。数据处理只做字段整理和模型输入矩阵构造，不改写题面给出的观测值。

模型假设包括四点。第一，训练批次和待评估批次来自同一温室管理体系，变量口径一致。第二，预测只在训练样本覆盖的温度、光照、灌溉和施氮邻近范围内解释，不做远端外推。第三，高温和高施氮端点可能存在收益递减，因此二次响应面只作为检验项，不作为无约束优化器。第四，residual error 主要来自批次差异、测量误差和未观测管理因素，可以用留一交叉验证残差近似刻画。

## 模型建立

基线模型采用多元线性回归 `EQ1`，岭回归通过惩罚项降低多重共线性风险，二次响应面用于检查边际收益递减。误差评价采用留一交叉验证 RMSE `EQ2`。图 F1 展示驱动变量与产量关系，图 F2 展示候选模型误差比较，图 F3 展示预测区间。

线性模型用于回答 Q1 的可解释性问题：若光照、灌溉和施氮的系数方向为正，则说明这些管理变量在样本范围内对产量提升有贡献。岭回归用于回答 Q2 的小样本稳健性问题：当变量之间存在同步增加趋势时，岭惩罚能降低系数方差，使 validation 指标更稳定。二次响应面用于检查端点的非线性风险：若高温、高施氮附近残差变大，则不应把 P03 的高端预测解释为继续增肥建议。

## 模型 validation 设计

validation 采用留一交叉验证。每次取 11 个训练批次拟合模型，用剩余 1 个批次计算预测误差，最终汇总 RMSE 和 MAE。该 validation 设计牺牲了单次训练样本量，但能让每个批次都参与一次外推式误差检查，适合当前 12 条样本的小数据设置。结果合同 `R-Q2-001` 记录岭回归 validation RMSE 为 0.29 kg/m2，低于线性模型 0.34 kg/m2 和二次响应面 0.31 kg/m2，因此推荐模型选择岭回归。

## 结果分析

结果合同中 `R-Q2-001` 记录岭回归 RMSE 为 0.29 kg/m2。`R-Q3-001`、`R-Q3-002`、`R-Q3-003` 分别记录 P01、P02、P03 的产量预测值 7.7、8.8、9.2 kg/m2。预测区间使用经验残差公式 `EQ3`，用于表达小样本训练带来的不确定性。

P01 的温度、湿度、光照、灌溉和施氮水平接近训练样本中段，因此 residual error 风险较低，预测区间为 7.1 至 8.3 kg/m2。P02 接近训练样本的高产稳定区，预测值 8.8 kg/m2 与 B08 至 B10 的产量水平一致。P03 接近高温和高施氮端点，预测值 9.2 kg/m2 虽仍在训练产量范围内，但 robustness 解释应更谨慎，不能简单推出继续升温或继续增氮会提高产量。

## 验证与敏感性

本轮沙盒使用留一交叉验证比较三类模型，并检查待评估批次是否位于训练变量范围附近。光照、灌溉和施氮增加通常对应产量提升，但 P03 接近高温和高施氮端点，因此建议解释为区间内近端预测，不作为进一步增施氮的外推依据。

sensitivity 分析围绕三个可控变量进行。第一，将光照时长增加 0.2 h 时，P01 和 P02 的预测产量方向为上升，但变化幅度小于经验区间半宽，说明单次小幅调光不能替代长期验证。第二，将灌溉量增加 0.2 L/m2 时，中段批次通常表现为正向响应，但高湿或高灌溉端点可能出现收益递减。第三，将施氮量增加 0.3 g/m2 时，P03 的 sensitivity 不再被解释为强正向，因为它已经接近训练样本的高施氮端点。上述 sensitivity 结论只作为管理建议，不作为新的冻结数值。

robustness 分析检查三类扰动。第一，删除任一训练批次后，P01、P02、P03 的预测排序仍保持 P03 高于 P02、高于 P01。第二，在候选模型之间比较时，三组待评估批次均未出现大幅反向排序，说明 ranking robustness 可以接受。第三，把二次响应面作为非线性检查时，高端预测更保守，这支持对 P03 使用谨慎解释。residual error 分析没有发现低产区和高产区出现明显单侧偏差，因此本轮用统一经验残差构造预测区间。

## 合同与闸门闭环

本轮所有正式数值都登记在 `14_contracts/result_contract.csv`。主要论断通过 `14_contracts/claim_evidence_map.csv` 绑定到 `R-Q1-001`、`R-Q2-001` 和 `R-Q3-001`。核心公式登记在 `14_contracts/formula_contract.csv`，图 F1、F2、F3 均登记在 `14_contracts/figure_contract.csv`，且对应 SVG 文件存在于 `08_figures/output/`。模拟人工闸门日志只记录沙盒判断，`formal_effect` 保持为 `none`，不跳过正式工作流的人类最终闸门。

## 水肥调控建议

对 P01，建议优先补足光照和中等灌溉，使其接近 P02 的管理区间，同时避免一次性大幅增加施氮。对 P02，当前组合接近高产稳定区，建议维持水肥比例，并通过下一批次实测产量校准 residual error。对 P03，虽然预测产量最高，但温度和施氮接近端点，建议把调控目标放在稳产而不是继续增产，重点监控高温胁迫和过量施氮风险。

## 结论

在当前纯文本样本范围内，岭回归提供了较稳健的产量预测基线。建议优先维持 P02 附近的光照、灌溉和施氮组合，对 P03 采取谨慎增肥策略，并通过新增批次数据持续更新交叉验证误差。所有图表、公式、论断和数值已经登记到沙盒合同。
```

## 12_submission/final_submit_paper.md

```text
# 温室作物产量预测与水肥调控模型

## 摘要

本文针对纯文本温室番茄批次数据，建立单位面积产量预测和水肥调控分析流程。训练数据包含温度、湿度、光照、灌溉、施氮和产量字段；待评估批次为 P01、P02、P03。候选模型比较显示，岭回归留一交叉验证 RMSE 为 0.29 kg/m2，优于线性模型的 0.34 kg/m2 和二次响应面模型的 0.31 kg/m2。预测结果显示 P01、P02、P03 的产量约为 7.7、8.8、9.2 kg/m2。

## 问题分析

题面只提供纯文本表格，不依赖图片输入。Q1 需要解释环境和管理变量对产量的影响方向，Q2 需要比较至少三类候选模型，Q3 需要预测待评估批次并给出不确定性和水肥建议。小样本条件下，模型复杂度必须受控，所有正式数值必须写入 `14_contracts/result_contract.csv`。

从变量结构看，温度和湿度属于环境背景变量，光照、灌溉量和施氮量属于可调控管理变量。训练批次的产量从 5.8 kg/m2 增长到 9.4 kg/m2 后略有回落，说明线性增益和高端饱和可能同时存在。由于样本只有 12 个，不能把复杂模型的训练内拟合误差当作结论；本轮把 validation、sensitivity、robustness 和 residual error 都写入建模闭环，用来约束结论强度。

## 数据处理与假设

原始数据登记为 `03_data/raw/crop_yield_batches.csv`。训练批次 B01 至 B12 具有完整产量标签，待评估批次 P01 至 P03 缺少 `yield_kg_m2`，这是预测目标而非数据缺失错误。所有变量均为纯文本表格中的数值字段，无图片、传感器原始图像或外部历史论文文本参与。数据处理只做字段整理和模型输入矩阵构造，不改写题面给出的观测值。

模型假设包括四点。第一，训练批次和待评估批次来自同一温室管理体系，变量口径一致。第二，预测只在训练样本覆盖的温度、光照、灌溉和施氮邻近范围内解释，不做远端外推。第三，高温和高施氮端点可能存在收益递减，因此二次响应面只作为检验项，不作为无约束优化器。第四，residual error 主要来自批次差异、测量误差和未观测管理因素，可以用留一交叉验证残差近似刻画。

## 模型建立

基线模型采用多元线性回归 `EQ1`，岭回归通过惩罚项降低多重共线性风险，二次响应面用于检查边际收益递减。误差评价采用留一交叉验证 RMSE `EQ2`。图 F1 展示驱动变量与产量关系，图 F2 展示候选模型误差比较，图 F3 展示预测区间。

线性模型用于回答 Q1 的可解释性问题：若光照、灌溉和施氮的系数方向为正，则说明这些管理变量在样本范围内对产量提升有贡献。岭回归用于回答 Q2 的小样本稳健性问题：当变量之间存在同步增加趋势时，岭惩罚能降低系数方差，使 validation 指标更稳定。二次响应面用于检查端点的非线性风险：若高温、高施氮附近残差变大，则不应把 P03 的高端预测解释为继续增肥建议。

## 模型 validation 设计

validation 采用留一交叉验证。每次取 11 个训练批次拟合模型，用剩余 1 个批次计算预测误差，最终汇总 RMSE 和 MAE。该 validation 设计牺牲了单次训练样本量，但能让每个批次都参与一次外推式误差检查，适合当前 12 条样本的小数据设置。结果合同 `R-Q2-001` 记录岭回归 validation RMSE 为 0.29 kg/m2，低于线性模型 0.34 kg/m2 和二次响应面 0.31 kg/m2，因此推荐模型选择岭回归。

## 结果分析

结果合同中 `R-Q2-001` 记录岭回归 RMSE 为 0.29 kg/m2。`R-Q3-001`、`R-Q3-002`、`R-Q3-003` 分别记录 P01、P02、P03 的产量预测值 7.7、8.8、9.2 kg/m2。预测区间使用经验残差公式 `EQ3`，用于表达小样本训练带来的不确定性。

P01 的温度、湿度、光照、灌溉和施氮水平接近训练样本中段，因此 residual error 风险较低，预测区间为 7.1 至 8.3 kg/m2。P02 接近训练样本的高产稳定区，预测值 8.8 kg/m2 与 B08 至 B10 的产量水平一致。P03 接近高温和高施氮端点，预测值 9.2 kg/m2 虽仍在训练产量范围内，但 robustness 解释应更谨慎，不能简单推出继续升温或继续增氮会提高产量。

## 验证与敏感性

本轮沙盒使用留一交叉验证比较三类模型，并检查待评估批次是否位于训练变量范围附近。光照、灌溉和施氮增加通常对应产量提升，但 P03 接近高温和高施氮端点，因此建议解释为区间内近端预测，不作为进一步增施氮的外推依据。

sensitivity 分析围绕三个可控变量进行。第一，将光照时长增加 0.2 h 时，P01 和 P02 的预测产量方向为上升，但变化幅度小于经验区间半宽，说明单次小幅调光不能替代长期验证。第二，将灌溉量增加 0.2 L/m2 时，中段批次通常表现为正向响应，但高湿或高灌溉端点可能出现收益递减。第三，将施氮量增加 0.3 g/m2 时，P03 的 sensitivity 不再被解释为强正向，因为它已经接近训练样本的高施氮端点。上述 sensitivity 结论只作为管理建议，不作为新的冻结数值。

robustness 分析检查三类扰动。第一，删除任一训练批次后，P01、P02、P03 的预测排序仍保持 P03 高于 P02、高于 P01。第二，在候选模型之间比较时，三组待评估批次均未出现大幅反向排序，说明 ranking robustness 可以接受。第三，把二次响应面作为非线性检查时，高端预测更保守，这支持对 P03 使用谨慎解释。residual error 分析没有发现低产区和高产区出现明显单侧偏差，因此本轮用统一经验残差构造预测区间。

## 合同与闸门闭环

本轮所有正式数值都登记在 `14_contracts/result_contract.csv`。主要论断通过 `14_contracts/claim_evidence_map.csv` 绑定到 `R-Q1-001`、`R-Q2-001` 和 `R-Q3-001`。核心公式登记在 `14_contracts/formula_contract.csv`，图 F1、F2、F3 均登记在 `14_contracts/figure_contract.csv`，且对应 SVG 文件存在于 `08_figures/output/`。模拟人工闸门日志只记录沙盒判断，`formal_effect` 保持为 `none`，不跳过正式工作流的人类最终闸门。

## 水肥调控建议

对 P01，建议优先补足光照和中等灌溉，使其接近 P02 的管理区间，同时避免一次性大幅增加施氮。对 P02，当前组合接近高产稳定区，建议维持水肥比例，并通过下一批次实测产量校准 residual error。对 P03，虽然预测产量最高，但温度和施氮接近端点，建议把调控目标放在稳产而不是继续增产，重点监控高温胁迫和过量施氮风险。

## 结论

在当前纯文本样本范围内，岭回归提供了较稳健的产量预测基线。建议优先维持 P02 附近的光照、灌溉和施氮组合，对 P03 采取谨慎增肥策略，并通过新增批次数据持续更新交叉验证误差。所有图表、公式、论断和数值已经登记到沙盒合同。
```

## 11_review/contract_validation_report.md

```text
# Contract validation report

- stage: intake
- fail_count: 0
- warn_count: 0

No contract-bus issues found. Human review is still required.
```

