# Training Sandbox Prompt Backup: auto_review

Formal source prompt: `prompts/stages/11_auto_review.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`auto_review` - 多审稿器自动审稿

> 中文注释：使用阶段为 `auto_review`；使用场景是在全文草稿形成后，生成审稿意见、评分表和可追踪修订任务。

## 1. 阶段身份

```yaml
stage_id: auto_review
stage_name: 多审稿器自动审稿
stage_order: 11
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P3
```

## 2. 目标

生成结构化审稿意见、评分表和修订任务，但不得直接编辑正式交付物。算力集中在多视角批判、合同校验、图表质量、结果可信度、论文说服力、评分风险和可执行修订任务上。

## 3. 必需输入

```text
- 全文草稿
- 14_contracts/claim_evidence_map.csv
- 14_contracts/result_contract.csv
- 14_contracts/figure_contract.csv
```

## 4. 可选输入

```text
- 11_review/历史审稿意见
- 13_prior_db/对标风险卡片（如已允许）
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 02_latex_template/
- 09_paper/
- 11_review/
- 13_prior_db/
- 14_contracts/
```

## 6. 允许写入路径

```text
- 11_review/
- 14_contracts/revision_tasks.csv
- 10_ai_logs/
```

## 7. 禁止动作

```text
- 审稿器不得直接修改论文、代码、结果或图表。
- 不得关闭任务而不提供证据。
- 不得复制先验论文文本。
- 不得把建议伪装成已修复。
- 不得用主观偏好替代合同失败项。
- 不得忽略 fail/major 风险。
```

## 8. 必需输出

```text
- 11_review/*_reviewer_comments.md
- 11_review/review_scorecard.csv
- 14_contracts/revision_tasks.csv
- 多视角问题清单：题目、模型、数据、代码、结果、图表、写作、评委视角
- 阶段总结
```

## 9. 合同更新

```text
可更新：revision_tasks.csv
只读：其他合同
```

## 10. 允许技能

```text
- nature-response（如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 auto_review 阶段。

输入核验：
1. 检查全文草稿和核心合同文件。
2. 若允许读取 13_prior_db/，可参考先验风险卡片和 copy-risk 报告；不得复制历史论文文本。
3. 确认审稿阶段只写评论、评分和修订任务。

阶段目标：
从问题、模型、代码、图表、论文和评委视角审阅草稿。只输出评论、评分和修订任务，不直接修改交付物。

深度分析：
1. 题目视角：是否覆盖所有官方问题、交付物和约束。
2. 数据视角：数据来源、字段解释、缺失异常、可复现性是否支撑模型。
3. 模型视角：假设、变量、公式、验证、备选方案和局限是否充分。
4. 结果视角：冻结结果是否可追踪，数值是否一致，是否有敏感性或误差说明。
5. 图表视角：图表是否高级、非默认配色、中文标注、绑定合同、质量分不低于 4.2，图表密度是否支撑论证。
6. 写作视角：论断是否绑定证据，章节是否连贯，结论是否过强。
7. 评分视角：将问题分为 fail、major、minor、suggestion，并给出可执行 acceptance_check。

证据绑定：
每条修订任务必须指向 source_comment_id、target_artifact、target_location、linked_contract_ids 或明确说明无法定位原因。

风险清单：
记录合同失败、证据缺口、图表质量、结果可信度、复制风险、人工豁免需求和低分风险。

自检清单：
1. 没有修改正式交付物。
2. 所有 fail/major 问题进入 revision_tasks。
3. 每个任务有 required_action 和 acceptance_check。
4. 没有复制先验文本。
5. 校验命令已运行或记录 not_run。

人工确认输出：
请人类决定哪些审稿问题是必修、可选或人工豁免后再开始修订。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage auto_review
```

## 13. 人工确认问题

```text
哪些审稿问题是必修、可选或人工豁免后再开始修订？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 草稿缺失 | 返回 paper_full。 |
| 合同缺失 | 返回相应合同生产阶段。 |
| 审稿意见不可执行 | 改写为具体修订任务。 |
| 分数低于阈值 | 标记 fail/major，进入 revision。 |
| 任务无法定位目标 | 保留评论并要求人工定位，不直接修改。 |

## 15. 完成条件

```text
- 审稿意见和评分表已生成。
- 必需修订已进入 revision_tasks。
- fail/major 风险没有被静默忽略。
- 没有直接修改正式产物。
- 未触发本阶段禁止动作。
```

