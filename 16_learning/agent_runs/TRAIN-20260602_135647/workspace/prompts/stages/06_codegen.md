# 阶段提示词：`codegen` - 分问题代码生成

> 中文注释：使用阶段为 `codegen`；使用场景是在模型路线经人工确认后，按问题逐个生成、运行和记录可复现求解代码。

## 1. 阶段身份

```yaml
stage_id: codegen
stage_name: 分问题代码生成
stage_order: 6
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P4
```

## 2. 目标

一次只为一个问题生成并运行可复现求解代码，产出候选结果文件。

## 3. 必需输入

```text
- 05_model/model_route.md
- 05_model/fallback_plan.md
- 03_data/ 或已确认数据源
```

## 4. 可选输入

```text
- 14_contracts/formula_contract.csv
- 04_eda/
- 人工实现约束
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
- 05_model/
- templates/code/
```

## 6. 允许写入路径

```text
- 06_code/
- 07_results/
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 不得同时生成多个问题的代码。
- 不得绕过已批准模型路线。
- 不得将未运行代码的输出写成结果。
- 不得写论文结果分析。
```

## 8. 必需输出

```text
- 对应问题的代码文件
- 运行日志
- 候选结果文件
- 失败或复现风险说明
```

## 9. 合同更新

```text
可更新：建议只生成 result_contract 候选说明，正式冻结在 results_freeze 阶段
只读：formula_contract.csv
```

## 10. 允许技能

```text
- 无
```

## 11. 代理提示词模板

```text
你正在执行 codegen 阶段。
只处理当前指定问题，按已批准模型路线生成可复现代码。
运行代码并记录真实输出；失败时记录失败原因，不伪造结果。
```

## 12. 校验命令

```bash
python scripts/run_current_stage.py --question Q1
```

```bash
python scripts/validate_contracts.py --stage current --warn-only
```

## 13. 人工确认问题

```text
生成的代码是否实现了已批准模型，而不是为了方便采用了捷径？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 代码运行失败 | 修复最小代码路径并重跑，保留日志。 |
| 模型路线不可实现 | 返回 model_route 记录备选模型。 |
| 数据读取失败 | 返回 eda 或数据准备阶段。 |
| 结果异常 | 标记为候选结果，不进入冻结。 |

## 15. 完成条件

```text
- 指定问题代码存在并可解释。
- 运行日志和真实候选结果已保存。
- 没有把候选结果直接写成论文结论。
```
