# 阶段提示词：`prior_retrieval` - 先验经验卡片检索

> 中文注释：使用阶段为 `prior_retrieval`；使用场景是在模型路由前，从先验材料中提取经验卡片和评分风险提示，但不复制历史论文文本。

## 1. 阶段身份

```yaml
stage_id: prior_retrieval
stage_name: 先验经验卡片检索
stage_order: 4
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P2
```

## 2. 目标

从先验材料中抽取可复用建模经验卡片，不复制历史论文文本。

## 3. 必需输入

```text
- config/prior_db_policy.yaml
- 01_task_analysis/problem_model_profile.csv
```

## 4. 可选输入

```text
- 13_prior_db/
- 13_sample_prior/
- 01_task_analysis/task_decomposition.md
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 01_task_analysis/
- 13_prior_db/
- 13_sample_prior/
```

## 6. 允许写入路径

```text
- 13_prior_db/
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 不得复制历史论文摘要、正文、表格、图注或结论。
- 不得把历史论文当作当前题目的事实答案。
- 不得输出可直接粘贴到论文的段落。
- 不得绕过 prior_db_policy.yaml。
```

## 8. 必需输出

```text
- 13_prior_db/pre_solve_cards.md 或等价经验卡片
- copy-risk 或风险说明
- 阶段总结
```

## 9. 合同更新

```text
可更新：无
只读：14_contracts/*.csv
```

## 10. 允许技能

```text
- nature-reader（如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 prior_retrieval 阶段。
只能抽取题型经验、常见模型族、常见图型、评分风险和预处理模式。
不得复制历史论文表达或直接生成当前题目答案。
输出必须保持 advisory_only。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage prior_retrieval
```

```bash
python scripts/check_prior_copy_risk.py --warn-only
```

## 13. 人工确认问题

```text
这些先验卡片是否只作为提示使用，且没有复制历史表述或结构？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 先验库不存在 | 创建空经验卡片占位，并说明没有可用先验。 |
| 拷贝风险过高 | 丢弃相关文本，只保留抽象经验标签。 |
| 问题画像缺失 | 返回 task_analysis 补齐画像。 |
| 技能不可用 | 记录未运行，使用本地保守模板。 |

## 15. 完成条件

```text
- 输出只包含经验卡片和风险提示。
- 没有历史论文可复制文本。
- 下游模型路由能读取卡片 ID 或提示。
```
