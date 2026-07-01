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

生成结构化审稿意见、评分表和修订任务，但不得直接编辑正式交付物。

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
```

## 8. 必需输出

```text
- 11_review/*_reviewer_comments.md
- 11_review/review_scorecard.csv
- 14_contracts/revision_tasks.csv
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
从问题、模型、代码、图表、论文和评委视角审阅草稿。
只输出评论、评分和修订任务，不直接修改交付物。
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

## 15. 完成条件

```text
- 审稿意见和评分表已生成。
- 必需修订已进入 revision_tasks。
- 没有直接修改正式产物。
```
