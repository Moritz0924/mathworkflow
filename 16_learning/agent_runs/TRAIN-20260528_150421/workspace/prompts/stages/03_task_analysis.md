# 阶段提示词：`task_analysis` - 任务拆解

> 中文注释：使用阶段为 `task_analysis`；使用场景是在题面和数据初查后，将赛题拆成可建模子问题、交付物和依赖关系。

## 1. 阶段身份

```yaml
stage_id: task_analysis
stage_name: 任务拆解
stage_order: 3
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. 目标

将赛题拆解为子问题、交付物、假设、依赖关系和建模要求。

## 3. 必需输入

```text
- 00_problem/problem_statement.md
- 00_problem/attachments_overview.md
- 03_data/data_quality_report.md（如已有数据）
```

## 4. 可选输入

```text
- 04_eda/eda_summary_for_paper.md
- 人工任务理解说明
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 00_problem/
- 01_task_analysis/
- 03_data/
- 04_eda/
```

## 6. 允许写入路径

```text
- 01_task_analysis/
- 10_ai_logs/
```

## 7. 禁止动作

```text
- 不得选择最终模型。
- 不得写模型结果。
- 不得忽略题目显式交付要求。
- 不得把先验论文内容写入题目拆解。
```

## 8. 必需输出

```text
- 01_task_analysis/task_decomposition.md
- 01_task_analysis/problem_model_profile.csv
- 01_task_analysis/question_dependency_map.md 或同等说明
- 阶段总结和风险说明
```

## 9. 合同更新

```text
可更新：无
只读：14_contracts/*.csv
```

## 10. 允许技能

```text
- 无
```

## 11. 代理提示词模板

```text
你正在执行 task_analysis 阶段。
根据题面和数据状态拆解子问题、输入输出、依赖和风险。
不得直接给出最终模型或结果。
输出必须能支持后续 prior_retrieval 与 model_route。
```

## 12. 校验命令

```bash
python scripts/check_gates.py --dev-debug
```

## 13. 人工确认问题

```text
拆解结果是否与官方题目交付要求一致？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 题面不完整 | 回到 intake 补齐题面。 |
| 子问题边界不清 | 记录多种解释，交给人工确认。 |
| 数据与题目不匹配 | 写入风险报告，不强行建模。 |
| 依赖关系不明确 | 保守标记依赖，等待模型路由复核。 |

## 15. 完成条件

```text
- 每个子问题都有输入、输出和风险描述。
- 后续阶段能读取问题画像。
- 未产生越权模型结论。
```
