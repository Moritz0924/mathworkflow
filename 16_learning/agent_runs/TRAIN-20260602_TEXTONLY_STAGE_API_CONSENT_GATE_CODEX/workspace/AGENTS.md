# 数学建模工作流 v3.2-MVP 代理规则

本仓库使用受控的深度顺序数学建模工作流。工作流控制器拥有状态；Codex 负责执行任务；`nature-skills` 是阶段内专家工具；先验数据库只提供经验提示，不提供答案；审稿器只生成审稿与修订工件。

## 权威顺序

1. 人类最终闸门
2. 工作流控制器与阶段状态
3. 合同总线与校验脚本
4. Codex 执行器
5. `nature-skills` 专家指导
6. Prior DB 检索说明

规则冲突时，服从更高层级的权威。

## 硬性约束

- 只能使用 `deep_sequential` 模式。
- 不得并行运行多个阶段。
- 不得跳过人工闸门。
- 在结果合同存在前，不得生成完整论文。
- 没有模型输出和 `result_contract.csv` 条目时，不得写结果分析。
- 图未登记到 `figure_contract.csv` 且文件不存在时，不得在论文中引用。
- 润色不得改变数字、公式、标签、引用、文献、模型名或结果含义。
- 不得复制历史论文文本，包括摘要、正文段落、图注、表格和结论。
- 不得允许审稿代理直接修改正式交付物。
- 不得把 `nature-skills` 当作工作流控制器。

## 阶段到技能路由

| 阶段 | 允许技能 | 角色 | 使用前必需合同 |
|---|---|---|---|
| `literature` | `nature-academic-search`, `nature-citation` | 文献检索与引用核验 | `citation_contract.csv` 脚手架 |
| `data` | `nature-data` | 数据来源与可复现性说明 | 如存在则使用 `data_contract.yaml` |
| `prior_retrieval` | `nature-reader` | 只抽取经验卡片 | `prior_db_policy.yaml` |
| `figures` | `nature-figure` | 图表论证设计与导出质量 | `result_contract.csv`, `figure_contract.csv` |
| `paper_draft` | `nature-writing` | 分章节论证草拟 | `claim_evidence_map.csv`, `result_contract.csv`, `figure_contract.csv` |
| `paper_full` | `nature-writing` | 跨章节一致性 | 同 `paper_draft` |
| `auto_review` | `nature-response` 风格逻辑 | 评论归并与可追踪修订 | 草稿论文与合同 |
| `polish` | `nature-polishing` | 不改事实的语言润色 | `artifact_freeze_registry.csv` |
| `final_export` | `nature-paper2ppt` | 终稿确认后的展示材料 | 人工确认的终稿 |

## 合同总线规则

所有正式论断必须记录在 `14_contracts/claim_evidence_map.csv`。
论文使用的所有数值结果必须记录在 `14_contracts/result_contract.csv`。
论文使用的所有图表必须记录在 `14_contracts/figure_contract.csv`。
所有重要公式必须记录在 `14_contracts/formula_contract.csv`。
所有引用必须记录在 `14_contracts/citation_contract.csv`。
所有冻结产物必须记录在 `14_contracts/artifact_freeze_registry.csv`。
所有润色变更必须通过 `14_contracts/polish_diff_check.csv`。
所有审稿问题必须记录在 `14_contracts/revision_tasks.csv`。

## 审稿器权限

审稿器可以写入：

- `11_review/*_reviewer_comments.md`
- `11_review/review_scorecard.csv`
- `11_review/revision_tasks.csv`
- `14_contracts/revision_tasks.csv`

审稿器不得修改：

- `02_latex_template/`
- `05_model/`
- `06_code/`
- `07_results/`
- `08_figures/`
- `09_paper/`
- `12_submission/`

## Prior DB 规则

求解前，Prior DB 检索只能输出：

- 题型经验
- 常见模型族
- 常见图表类型
- 常见评分风险

第一版完整草稿形成后，Prior DB 检索才可以额外输出：

- 结构对比
- 论证缺口对比
- 图表密度对比
- 评分风险对比

禁止行为：

- 复制历史论文文本
- 复用历史图注
- 复用历史摘要或结论
- 直接复制历史表格
- 把历史论文当作当前题目的事实答案

## `nature-skills` 集成规则

- 复制整个 `skills/nature-*` 目录，而不是只复制 `SKILL.md`。
- 项目内 vendored 技能放在 `vendor/nature-skills/skills/`。
- 只有本地运行 Codex 时才同步到 `~/.codex/skills/`。
- 条件允许时，在 `vendor/nature-skills/VERSION.txt` 固定 `nature-skills` 提交版本。
- 技能只作为阶段内专家；其输出仍必须通过合同校验。

## 最终闸门

只有同时满足以下条件，才允许形成最终交付：

- `scripts/check_gates.py` 通过。
- `scripts/validate_contracts.py` 通过。
- `11_review/review_scorecard.csv` 中没有 fail 级未关闭问题。
- 所有必需修订任务已经关闭，或由人类明确豁免。
- 人类最终闸门已确认。
