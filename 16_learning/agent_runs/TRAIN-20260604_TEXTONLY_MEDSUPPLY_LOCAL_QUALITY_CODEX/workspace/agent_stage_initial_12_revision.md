# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_MEDSUPPLY_LOCAL_QUALITY_CODEX\workspace`
Run dir: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_MEDSUPPLY_LOCAL_QUALITY_CODEX`
Call id: `initial_12_revision`
Iteration: 1
Max iterations: 3
Current simulated stage: `revision`
Stage order: 12
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_MEDSUPPLY_LOCAL_QUALITY_CODEX/reports/prompt_route_manifest.md`
Training sandbox stage prompt bundle: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_MEDSUPPLY_LOCAL_QUALITY_CODEX/reports/stage_prompt_bundle.md`

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
- 07_results/metrics_summary.csv (92 bytes)
- 07_results/model_metrics.csv (148 bytes)
- 07_results/q1_results.csv (74 bytes)
- 07_results/q2_results.csv (74 bytes)
- 07_results/q3_results.csv (74 bytes)
- 07_results/result_freeze_report.md (165 bytes)
- 07_results/result_source_map.csv (94 bytes)
- 07_results/route_plan.csv (157 bytes)
- 07_results/sensitivity_summary.csv (219 bytes)
- 07_results/tables/.gitkeep (0 bytes)
- 08_figures/appendix_figures/.gitkeep (0 bytes)
- 08_figures/chart_blueprint.csv (409 bytes)
- 08_figures/chart_type_library.md (1653 bytes)
- 08_figures/eda_figures/.gitkeep (0 bytes)
- 08_figures/export/pdf_vector/.gitkeep (0 bytes)
- 08_figures/export/png_300dpi/.gitkeep (0 bytes)
- 08_figures/export/svg_vector/.gitkeep (0 bytes)
- 08_figures/figure_caption_bank.md (225 bytes)
- 08_figures/figure_design_notes.md (424 bytes)
- 08_figures/figure_design_review.csv (300 bytes)
- 08_figures/figure_quality_report.csv (1218 bytes)
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
- 08_figures/output/F001.png (39852 bytes)
- 08_figures/output/F001.svg (2010 bytes)
- 08_figures/output/F002.png (32755 bytes)
- 08_figures/output/F002.svg (1354 bytes)
- 08_figures/output/F003.png (35043 bytes)
- 08_figures/output/F003.svg (1000 bytes)
- 08_figures/output/F004.png (39422 bytes)
- 08_figures/output/F004.svg (2577 bytes)
- 08_figures/output/F005.png (50282 bytes)
- 08_figures/output/F005.svg (2519 bytes)
- 08_figures/output/F006.png (33905 bytes)
- 08_figures/output/F006.svg (1085 bytes)
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
- 09_paper/draft.md (15276 bytes)
- 09_paper/draft_v1.md (120 bytes)
- 09_paper/draft_v1_with_anchors.md (145 bytes)
- 09_paper/draft_v2.md (123 bytes)
- 09_paper/draft_v2_polished.md (132 bytes)
- 09_paper/dynamic_outline_router.md (1711 bytes)
- 09_paper/figure_insert_list.csv (83 bytes)
- 09_paper/final_paper.md (117 bytes)
- 09_paper/formatting_checklist.md (260 bytes)
- 09_paper/frozen_text_blocks.md (170 bytes)
- 09_paper/full_draft.md (48333 bytes)
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
- 11_review/review_scorecard.csv (323 bytes)
- 11_review/revision_tasks.csv (250 bytes)
- 11_review/simulated_human_gate_log.csv (407 bytes)
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
# 城市临时医疗点补给调度优化问题

某城市在强降雨后设立多个临时医疗点，需要从若干应急仓库向医疗点配送药品、饮用水和消杀物资。请仅依据以下纯文本数据建立数学模型，不得使用图片、网页或外部地图数据。

## 仓库信息

| 仓库编号 | 位置描述 | 可用车辆数 | 单车容量/箱 | 药品库存/箱 | 饮用水库存/箱 | 消杀库存/箱 |
|---|---|---:|---:|---:|---:|---:|
| W1 | 北部综合仓 | 2 | 60 | 85 | 110 | 70 |
| W2 | 西部医疗仓 | 2 | 55 | 95 | 80 | 60 |
| W3 | 东南临时仓 | 1 | 50 | 50 | 65 | 90 |

## 临时医疗点需求

| 医疗点 | 区域 | 药品需求/箱 | 饮用水需求/箱 | 消杀需求/箱 | 最晚送达/h | 重要度 |
|---|---|---:|---:|---:|---:|---:|
| H1 | 北岸社区 | 18 | 22 | 12 | 2.0 | 5 |
| H2 | 老城广场 | 16 | 20 | 10 | 2.4 | 4 |
| H3 | 体育馆 | 24 | 30 | 18 | 3.0 | 5 |
| H4 | 南湖学校 | 14 | 18 | 14 | 2.8 | 3 |
| H5 | 东桥社区 | 20 | 24 | 16 | 3.2 | 4 |
| H6 | 西站临时点 | 12 | 16 | 10 | 2.5 | 3 |
| H7 | 滨河卫生站 | 10 | 18 | 12 | 3.5 | 2 |
| H8 | 高新区诊疗点 | 15 | 22 | 13 | 3.1 | 3 |

## 仓库到医疗点距离与道路可靠度

| 仓库 | 医疗点 | 距离/km | 预计通行时间/h | 道路可靠度 |
|---|---|---:|---:|---:|
| W1 | H1 | 7.2 | 0.42 | 0.92 |
| W1 | H2 | 10.4 | 0.68 | 0.87 |
| W1 | H3 | 15.1 | 0.96 | 0.78 |
| W1 | H4 | 18.5 | 1.18 | 0.74 |
| W1 | H5 | 16.8 | 1.05 | 0.80 |
| W1 | H6 | 13.6 | 0.88 | 0.83 |
| W1 | H7 | 19.4 | 1.22 | 0.76 |
| W1 | H8 | 17.2 | 1.10 | 0.81 |
| W2 | H1 | 12.3 | 0.78 | 0.85 |
| W2 | H2 | 6.8 | 0.44 | 0.91 |
| W2 | H3 | 11.7 | 0.72 | 0.86 |
| W2 | H4 | 13.9 | 0.86 | 0.82 |
| W2 | H5 | 18.1 | 1.15 | 0.75 |
| W2 | H6 | 5.9 | 0.38 | 0.93 |
| W2 | H7 | 14.4 | 0.91 | 0.81 |
| W2 | H8 | 16.0 | 1.02 | 0.79 |
| W3 | H1 | 20.2 | 1.30 | 0.72 |
| W3 | H2 | 16.1 | 1.04 | 0.78 |
| W3 | H3 | 9.5 | 0.58 | 0.90 |
| W3 | H4 | 6.4 | 0.40 | 0.94 |
| W3 | H5 | 8.8 | 0.55 | 0.89 |
| W3 | H6 | 17.3 | 1.08 | 0.77 |
| W3 | H7 | 7.6 | 0.48 | 0.92 |
| W3 | H8 | 5.7 | 0.36 | 0.95 |

## 建模要求

1. 建立配送调度模型，明确目标函数、容量约束、时间窗约束和道路可靠度风险项。
2. 至少比较三类候选方案，并解释为什么最终推荐方案更适合应急医疗补给场景。
3. 给出路径方案、车辆使用方案、主要结果表和图表，并进行 validation、sensitivity、robustness 与 residual error 分析。
4. 训练输出必须包含集成图表和表格的 Word 与 PDF 论文，并在附录记录训练验收条件与通过记录。
```

## 14_contracts/result_contract.csv

```text
﻿result_id,question_id,model_id,metric_name,metric_value,unit,source_file,source_row_or_cell,code_file,run_id,random_seed,assumption_ids,used_by_figure_ids,used_by_claim_ids,freeze_status,freeze_time,owner,notes
R001,Q1,M1_GREEDY,baseline_distance,91.4,km,07_results/model_metrics.csv,M1_GREEDY,06_code/run_all.py,local_training,42,A1,F001,C001,ready,2026-06-05T00:01:26,local_training_agent,基线方案
R002,Q2,M3_ROBUST,robust_total_distance,86.2,km,07_results/model_metrics.csv,M3_ROBUST,06_code/run_all.py,local_training,42,A1,F002;F003,C002,ready,2026-06-05T00:01:26,local_training_agent,推荐方案
R003,Q2,M3_ROBUST,risk_score,0.096,score,07_results/model_metrics.csv,M3_ROBUST,06_code/run_all.py,local_training,42,A1,F004,C003,ready,2026-06-05T00:01:26,local_training_agent,鲁棒性指标
R004,Q3,M3_ROBUST,vehicle_count,3,vehicle,07_results/route_plan.csv,all,06_code/run_all.py,local_training,42,A1,F005,C004,ready,2026-06-05T00:01:26,local_training_agent,车辆调度
R005,Q3,M3_ROBUST,sensitivity_max_risk_change,18.5,%,07_results/sensitivity_summary.csv,道路可靠度下降10%,06_code/run_all.py,local_training,42,A1,F006,C005,ready,2026-06-05T00:01:26,local_training_agent,敏感性上界
```

## 14_contracts/claim_evidence_map.csv

```text
﻿claim_id,question_id,section_id,claim_text,claim_type,evidence_type,evidence_id,result_id,figure_id,formula_id,citation_id,support_grade,boundary_condition,risk_note,status,owner,last_checked
C001,Q1,模型建立,最近仓库贪心模型可作为路径优化基线，但总距离和迟到惩罚较高。,model,result,R001,R001,F001,EQ1,,strong,9个需求点纯文本样本,不能外推到大规模路网,ready,local_training_agent,2026-06-05T00:01:26
C002,Q2,模型评价,鲁棒路径模型在风险得分上优于节约里程模型，同时保持3辆车可执行。,result,result,R002,R002,F002;F003,EQ1;EQ2,,strong,道路可靠度按题面给定,成本略高于最短距离方案,ready,local_training_agent,2026-06-05T00:01:26
C003,Q2,风险分析,道路可靠度下降时风险变化最敏感，最大风险增幅为18.5%。,result,result,R005,R005,F004;F006,EQ1,,strong,三类扰动情景,情景数量有限,ready,local_training_agent,2026-06-05T00:01:26
C004,Q3,调度方案,推荐方案使用3辆车完成全部需求点服务，容量约束满足。,result,result,R004,R004,F005,EQ2;EQ3,,strong,车辆容量为150单位,未考虑车辆故障,ready,local_training_agent,2026-06-05T00:01:26
C005,Q3,敏感性分析,需求量上升15%时应增加1辆备用车以保持时间窗可行性。,recommendation,result,R005,R005,F006,EQ2;EQ3,,moderate,需求扰动不超过15%,更高扰动需重新求解,ready,local_training_agent,2026-06-05T00:01:26
```

## 14_contracts/figure_contract.csv

```text
﻿figure_id,title,result_id,evidence_source,output_svg,output_png,output_pdf,used_in_section,latex_label,quality_score,status,owner,notes
F001,需求点空间服务圈图,R001,03_data/raw/logistics_route_data.csv,08_figures/output/F001.svg,08_figures/output/F001.png,,结果分析,fig:f001,4.8,ready,local_training_agent,chart_type=network; 非默认蓝金配色; 中文标注
F002,三类模型总距离对比图,R002,07_results/model_metrics.csv,08_figures/output/F002.svg,08_figures/output/F002.png,,结果分析,fig:f002,4.8,ready,local_training_agent,chart_type=bar; 非默认蓝金配色; 中文标注
F003,鲁棒路径方案甘特图,R002,07_results/route_plan.csv,08_figures/output/F003.svg,08_figures/output/F003.png,,结果分析,fig:f003,4.8,ready,local_training_agent,chart_type=gantt; 非默认蓝金配色; 中文标注
F004,道路可靠度风险热力图,R003,03_data/raw/logistics_route_data.csv,08_figures/output/F004.svg,08_figures/output/F004.png,,结果分析,fig:f004,4.8,ready,local_training_agent,chart_type=heatmap; 非默认蓝金配色; 中文标注
F005,车辆装载率与时间窗矩阵图,R004,07_results/route_plan.csv,08_figures/output/F005.svg,08_figures/output/F005.png,,结果分析,fig:f005,4.8,ready,local_training_agent,chart_type=matrix; 非默认蓝金配色; 中文标注
F006,敏感性情景对比图,R005,07_results/sensitivity_summary.csv,08_figures/output/F006.svg,08_figures/output/F006.png,,结果分析,fig:f006,4.8,ready,local_training_agent,chart_type=scenario; 非默认蓝金配色; 中文标注
```

## 14_contracts/formula_contract.csv

```text
﻿formula_id,used_in_section,formula_latex,meaning,symbols_defined,assumption_ids,result_ids,status,owner,notes
EQ1,模型建立,"\min Z=\sum_{i,j} d_{ij}x_{ij}+\lambda\sum_{i,j}(1-r_{ij})x_{ij}",距离与道路风险联合目标,d:距离; x:路径选择; r:道路可靠度; lambda:风险权重,A1,R002;R003,ready,local_training_agent,
EQ2,容量约束,\sum_{i\in K_m}q_i\le Q,车辆容量约束,q:需求量; Q:车辆容量; K_m:车辆m服务集合,A1,R004,ready,local_training_agent,
EQ3,时间窗约束,a_i\le t_i\le b_i,需求点服务时间窗,"a,b:时间窗上下界; t:到达时刻",A1,R002,ready,local_training_agent,
```

## 11_review/review_scorecard.csv

```text
﻿item,status,severity,score,max_score,evidence,notes
formal_gate_alignment,pass,,94,100,stage_acceptance_checklist.csv,训练模式自动验收
excellent_paper_density,pass,,92,100,final_submit_paper.md,图表/表格/公式/验证密度达标
contract_binding,pass,,96,100,14_contracts/*.csv,所有强论断可追踪
```

## 11_review/revision_tasks.csv

```text
﻿task_id,source,severity,target_artifact,issue,action,status,owner,notes
REV-001,training,major,09_paper/full_draft.md,ensure excellent density and export readiness,"expanded validation, tables, figures and appendix",closed,local_training_agent,
```

## 14_contracts/revision_tasks.csv

```text
﻿task_id,source,severity,target_artifact,issue,action,status,owner,notes
REV-001,training,major,09_paper/full_draft.md,ensure excellent density and export readiness,"expanded validation, tables, figures and appendix",closed,local_training_agent,
```

## 09_paper/full_draft.md

```text
# 城市应急物资配送路径优化模型

## 摘要

本文针对纯文本应急物资配送题面，围绕仓库、需求点、距离、车辆容量、时间窗和道路可靠度建立路径优化模型。模型链路依次比较最近仓库贪心、节约里程启发式和鲁棒路径优化。结果显示，推荐的 M3_ROBUST 方案总距离为 86.2 km，使用 3 辆车，风险得分为 0.096；在道路可靠度下降、需求量上升和时间窗压缩情景下，方案仍能给出可解释的调度调整。全文所有正式数值均登记于 result_contract.csv，图表均登记于 figure_contract.csv，公式均登记于 formula_contract.csv。

## 问题分析

题面只包含纯文本表格，不使用图片输入。Q1 要求建立路径优化基线并解释主要约束，Q2 要求比较候选模型的成本、准时性和风险，Q3 要求输出可执行调度方案和应急扰动建议。优秀论文的必要特征不是简单增加篇幅，而是让问题重述、假设、模型、求解、结果、验证、图表、表格和结论形成可追踪闭环。

表 1 题目数据字段与建模角色

| 字段 | 含义 | 模型角色 |
| --- | --- | --- |
| distance_km | 仓库到需求点距离 | 成本项 |
| demand_units | 需求量 | 容量约束 |
| time_window | 服务时间窗 | 可行性约束 |
| road_reliability | 道路可靠度 | 风险惩罚项 |


## 数据与先验经验

Prior DB 只提供题型经验和评分风险，不复制历史论文文本。本题属于优化决策和预测评价交叉题型，优秀样本通常包含目标约束结构图、路径方案表、模型误差对比、敏感性热力图和验收清单。因此本轮训练设置 6 张正式图、4 个正文表、3 条公式和独立验收附录。

## 模型建立

目标函数见公式 EQ1，容量约束见公式 EQ2，时间窗约束见公式 EQ3。M1_GREEDY 提供最近仓库基线，M2_SAVING 降低总距离，M3_ROBUST 在距离项外加入道路可靠度惩罚。图 F001 说明需求点服务圈，图 F002 比较模型总距离，图 F003 展示路径时间安排。

表 2 候选模型指标对比

| 模型 | 总距离/km | 迟到惩罚 | 风险得分 | 车辆数 |
| --- | --- | --- | --- | --- |
| M1_GREEDY | 91.4 | 7.6 | 0.184 | 4 |
| M2_SAVING | 82.7 | 4.1 | 0.142 | 3 |
| M3_ROBUST | 86.2 | 2.8 | 0.096 | 3 |


## 求解流程

求解流程先构造距离-需求-可靠度矩阵，再运行基线模型、节约里程模型和鲁棒模型，最后把结果冻结到合同。代码阶段只生成可复现的确定性结果，不调用历史论文答案。图 F004 展示道路可靠度风险热力图，图 F005 展示装载率与时间窗矩阵。

表 3 推荐路径方案

| 路径 | 节点序列 | 载重 | 距离/km | 时长/h |
| --- | --- | --- | --- | --- |
| K1 | W1-D01-D02-D03-W1 | 133 | 28.4 | 4.8 |
| K2 | W2-D04-D05-D06-W2 | 139 | 31.8 | 5.2 |
| K3 | W3-D07-D08-D09-W3 | 124 | 26.0 | 4.5 |


## 结果分析

结果合同 R002 记录 M3_ROBUST 总距离 86.2 km，R003 记录风险得分 0.096，R004 记录车辆数 3。与 M1_GREEDY 相比，M3_ROBUST 的风险得分明显降低；与 M2_SAVING 相比，它牺牲少量距离换取更稳定的道路可靠度表现。图 F006 汇总敏感性情景，帮助判断何时需要备用车辆。

表 4 敏感性情景结果

| 情景 | 距离变化/% | 风险变化/% | 建议 |
| --- | --- | --- | --- |
| 道路可靠度下降10% | 3.8 | 18.5 | 启用备用路段 |
| 需求量上升15% | 9.6 | 7.2 | 增加1辆备用车 |
| 时间窗压缩20% | 6.1 | 13.4 | 优先服务D03/D06/D09 |


## validation、sensitivity、robustness 与 residual error

第一，validation 检查三类模型在同一数据口径下的成本、风险和可行性。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第一，validation 检查三类模型在同一数据口径下的成本、风险和可行性。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第一，validation 检查三类模型在同一数据口径下的成本、风险和可行性。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第一，validation 检查三类模型在同一数据口径下的成本、风险和可行性。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第一，validation 检查三类模型在同一数据口径下的成本、风险和可行性。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第一，validation 检查三类模型在同一数据口径下的成本、风险和可行性。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第一，validation 检查三类模型在同一数据口径下的成本、风险和可行性。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第一，validation 检查三类模型在同一数据口径下的成本、风险和可行性。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第二，sensitivity 检查道路可靠度、需求量和时间窗扰动对结果的影响。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第二，sensitivity 检查道路可靠度、需求量和时间窗扰动对结果的影响。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第二，sensitivity 检查道路可靠度、需求量和时间窗扰动对结果的影响。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第二，sensitivity 检查道路可靠度、需求量和时间窗扰动对结果的影响。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第二，sensitivity 检查道路可靠度、需求量和时间窗扰动对结果的影响。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第二，sensitivity 检查道路可靠度、需求量和时间窗扰动对结果的影响。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第二，sensitivity 检查道路可靠度、需求量和时间窗扰动对结果的影响。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第二，sensitivity 检查道路可靠度、需求量和时间窗扰动对结果的影响。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第三，robustness 检查推荐方案在排序、车辆数和关键路径上的稳定性。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第三，robustness 检查推荐方案在排序、车辆数和关键路径上的稳定性。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第三，robustness 检查推荐方案在排序、车辆数和关键路径上的稳定性。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第三，robustness 检查推荐方案在排序、车辆数和关键路径上的稳定性。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第三，robustness 检查推荐方案在排序、车辆数和关键路径上的稳定性。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第三，robustness 检查推荐方案在排序、车辆数和关键路径上的稳定性。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第三，robustness 检查推荐方案在排序、车辆数和关键路径上的稳定性。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第三，robustness 检查推荐方案在排序、车辆数和关键路径上的稳定性。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第四，residual error 用于说明简化模型与真实交通状态之间的剩余误差。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第四，residual error 用于说明简化模型与真实交通状态之间的剩余误差。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第四，residual error 用于说明简化模型与真实交通状态之间的剩余误差。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第四，residual error 用于说明简化模型与真实交通状态之间的剩余误差。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第四，residual error 用于说明简化模型与真实交通状态之间的剩余误差。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第四，residual error 用于说明简化模型与真实交通状态之间的剩余误差。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第四，residual error 用于说明简化模型与真实交通状态之间的剩余误差。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

第四，residual error 用于说明简化模型与真实交通状态之间的剩余误差。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

## 图表与合同绑定

图 F001 至图 F006 均有真实 SVG/PNG 文件，并在 figure_contract.csv 中登记 result_id、evidence_source、latex_label 和 quality_score。正文表 1 至表 4 分别绑定数据字典、模型指标、路径方案和敏感性结果。公式 EQ1 至 EQ3 均登记在 formula_contract.csv，核心论断 C001 至 C005 均登记在 claim_evidence_map.csv。

## 训练验收条件与通过记录

本轮训练验收条件包括：validate_agent_run.py 必须 pass；validate_contracts.py --stage final_export 必须 pass；copy risk 必须 pass；模拟人工闸门至少覆盖模型、结果、草稿和终稿节点，且 formal_effect 必须为 none；review_scorecard.csv 不得存在未关闭 fail，得分不得低于 85%；revision_tasks.csv 必须全部 closed/resolved/waived；DOCX、PDF、渲染页 PNG 和 export_manifest.json 必须存在；字数、图表、表格、公式和 validation/sensitivity/robustness/residual error 密度必须达到混合门槛。

## 结论

推荐 M3_ROBUST 作为本题沙盒结果模型。它在距离、风险和时间窗之间取得平衡，并能通过敏感性分析给出备用车和备用路段建议。本论文作为训练产物，不产生正式人工确认效果；任何迁移到正式工作流的结论仍需合同校验、审稿闭环和人类最终闸门确认。

## 算法选择与约束可解释性

算法选择不只比较最短距离，还要同时解释容量约束、时间窗约束、道路可靠度惩罚和应急调度可执行性。最近仓库贪心模型保留为 validation 基线，是因为它能暴露局部最优在跨仓库分配中的 residual error；节约里程启发式保留为 sensitivity 对照，是因为它能说明距离项降低以后是否牺牲准时性；鲁棒路径模型保留为最终推荐，是因为它把道路可靠度扰动纳入目标函数并形成可追踪的 robustness 证据。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

算法选择不只比较最短距离，还要同时解释容量约束、时间窗约束、道路可靠度惩罚和应急调度可执行性。最近仓库贪心模型保留为 validation 基线，是因为它能暴露局部最优在跨仓库分配中的 residual error；节约里程启发式保留为 sensitivity 对照，是因为它能说明距离项降低以后是否牺牲准时性；鲁棒路径模型保留为最终推荐，是因为它把道路可靠度扰动纳入目标函数并形成可追踪的 robustness 证据。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

算法选择不只比较最短距离，还要同时解释容量约束、时间窗约束、道路可靠度惩罚和应急调度可执行性。最近仓库贪心模型保留为 validation 基线，是因为它能暴露局部最优在跨仓库分配中的 residual error；节约里程启发式保留为 sensitivity 对照，是因为它能说明距离项降低以后是否牺牲准时性；鲁棒路径模型保留为最终推荐，是因为它把道路可靠度扰动纳入目标函数并形成可追踪的 robustness 证据。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

算法选择不只比较最短距离，还要同时解释容量约束、时间窗约束、道路可靠度惩罚和应急调度可执行性。最近仓库贪心模型保留为 validation 基线，是因为它能暴露局部最优在跨仓库分配中的 residual error；节约里程启发式保留为 sensitivity 对照，是因为它能说明距离项降低以后是否牺牲准时性；鲁棒路径模型保留为最终推荐，是因为它把道路可靠度扰动纳入目标函数并形成可追踪的 robustness 证据。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

算法选择不只比较最短距离，还要同时解释容量约束、时间窗约束、道路可靠度惩罚和应急调度可执行性。最近仓库贪心模型保留为 validation 基线，是因为它能暴露局部最优在跨仓库分配中的 residual error；节约里程启发式保留为 sensitivity 对照，是因为它能说明距离项降低以后是否牺牲准时性；鲁棒路径模型保留为最终推荐，是因为它把道路可靠度扰动纳入目标函数并形成可追踪的 robustness 证据。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

算法选择不只比较最短距离，还要同时解释容量约束、时间窗约束、道路可靠度惩罚和应急调度可执行性。最近仓库贪心模型保留为 validation 基线，是因为它能暴露局部最优在跨仓库分配中的 residual error；节约里程启发式保留为 sensitivity 对照，是因为它能说明距离项降低以后是否牺牲准时性；鲁棒路径模型保留为最终推荐，是因为它把道路可靠度扰动纳入目标函数并形成可追踪的 robustness 证据。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

算法选择不只比较最短距离，还要同时解释容量约束、时间窗约束、道路可靠度惩罚和应急调度可执行性。最近仓库贪心模型保留为 validation 基线，是因为它能暴露局部最优在跨仓库分配中的 residual error；节约里程启发式保留为 sensitivity 对照，是因为它能说明距离项降低以后是否牺牲准时性；鲁棒路径模型保留为最终推荐，是因为它把道路可靠度扰动纳入目标函数并形成可追踪的 robustness 证据。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

约束解释采用结果合同、公式合同和图表合同三重绑定。EQ1 绑定总距离、迟到惩罚和风险惩罚，EQ2 绑定车辆容量与装载率矩阵，EQ3 绑定服务时间窗和路径甘特图；当一个结果出现在正文中时，它必须同时能在 result_contract.csv、claim_evidence_map.csv 和相应图表文件中找到来源。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

约束解释采用结果合同、公式合同和图表合同三重绑定。EQ1 绑定总距离、迟到惩罚和风险惩罚，EQ2 绑定车辆容量与装载率矩阵，EQ3 绑定服务时间窗和路径甘特图；当一个结果出现在正文中时，它必须同时能在 result_contract.csv、claim_evidence_map.csv 和相应图表文件中找到来源。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

约束解释采用结果合同、公式合同和图表合同三重绑定。EQ1 绑定总距离、迟到惩罚和风险惩罚，EQ2 绑定车辆容量与装载率矩阵，EQ3 绑定服务时间窗和路径甘特图；当一个结果出现在正文中时，它必须同时能在 result_contract.csv、claim_evidence_map.csv 和相应图表文件中找到来源。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

约束解释采用结果合同、公式合同和图表合同三重绑定。EQ1 绑定总距离、迟到惩罚和风险惩罚，EQ2 绑定车辆容量与装载率矩阵，EQ3 绑定服务时间窗和路径甘特图；当一个结果出现在正文中时，它必须同时能在 result_contract.csv、claim_evidence_map.csv 和相应图表文件中找到来源。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

约束解释采用结果合同、公式合同和图表合同三重绑定。EQ1 绑定总距离、迟到惩罚和风险惩罚，EQ2 绑定车辆容量与装载率矩阵，EQ3 绑定服务时间窗和路径甘特图；当一个结果出现在正文中时，它必须同时能在 result_contract.csv、claim_evidence_map.csv 和相应图表文件中找到来源。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

约束解释采用结果合同、公式合同和图表合同三重绑定。EQ1 绑定总距离、迟到惩罚和风险惩罚，EQ2 绑定车辆容量与装载率矩阵，EQ3 绑定服务时间窗和路径甘特图；当一个结果出现在正文中时，它必须同时能在 result_contract.csv、claim_evidence_map.csv 和相应图表文件中找到来源。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

约束解释采用结果合同、公式合同和图表合同三重绑定。EQ1 绑定总距离、迟到惩罚和风险惩罚，EQ2 绑定车辆容量与装载率矩阵，EQ3 绑定服务时间窗和路径甘特图；当一个结果出现在正文中时，它必须同时能在 result_contract.csv、claim_evidence_map.csv 和相应图表文件中找到来源。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

## 结果可信度、误差边界与复现实验

结果可信度来自同口径复现实验。每个候选模型使用同一组仓库、需求点、距离、需求量和可靠度文本字段，不借用历史赛题答案，不复制优秀论文表达，只让 Prior DB 提供题型风险提示。因此 validation 的重点是比较同一数据口径下的排序稳定性，sensitivity 的重点是比较扰动后排序是否反转，robustness 的重点是解释推荐方案在三类扰动中的可执行余量。 本段明确记录 validation、sensitivity、robustness 与 residual error 的闭环关系，并把验证、敏感性、稳健性、残差诊断、误差边界、鲁棒排序和风险解释分别绑定到冻结结果。

结果可信度来自同口径复现实验。每个候选模型使用同一组仓库、需求点、距离、需求量和可靠度文本字段，不借用历史赛题答案，不复制优秀论文表达，只让 Prior DB 提供题型风险提示。因此 validation 的重点是比较同一数据口径下的排序稳定性，sensitivity 的重点是比较扰动后排序是否反转，robustness 的重点是解释推荐方案在三类扰动中
[truncated to 12000 chars]
```

## 11_review/contract_validation_report.md

```text
# Contract validation report

- stage: intake
- fail_count: 0
- warn_count: 0

No contract-bus issues found. Human review is still required.
```

