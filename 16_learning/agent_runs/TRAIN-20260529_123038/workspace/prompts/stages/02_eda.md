# 阶段提示词：`eda` - 探索性数据分析

> 中文注释：使用阶段为 `eda`；使用场景是在正式建模前检查数据质量、字段含义、分布特征和描述性风险。

## 1. 阶段身份

```yaml
stage_id: eda
stage_name: 探索性数据分析
stage_order: 2
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. 目标

刻画可用数据，产出谨慎的描述性发现，为模型路由提供依据，但不得形成冻结结果。

## 3. 必需输入

```text
- workflow_state.yaml
- config/execution_policy.yaml
- 03_data/raw/ 或已登记数据说明
```

## 4. 可选输入

```text
- 00_problem/problem_statement.md
- 00_problem/attachments_overview.md
- 人工字段解释
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 00_problem/
- 03_data/
- 04_eda_code/
```

## 6. 允许写入路径

```text
- 03_data/
- 04_eda/
- 04_eda_code/
- 08_figures/eda_figures/
- 10_ai_logs/
```

## 7. 禁止动作

```text
- 不得把 EDA 输出当作冻结结果。
- 不得写最终结果分析。
- 不得生成正式论文图表引用。
- 不得伪造缺失字段或单位。
```

## 8. 必需输出

```text
- 数据字典或字段说明
- 数据质量报告
- EDA 摘要
- 风险报告和阶段总结
```

## 9. 合同更新

```text
可更新：data_contract.yaml 草稿（如适用）
只读：其他 14_contracts/*.csv
```

## 10. 允许技能

```text
- nature-data（如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 eda 阶段。
目标是描述数据、发现质量风险、为模型路线提供依据。
不得把描述性发现写成最终结论。
记录缺失值、异常值、单位、口径、样本量和可复现性风险。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage current --warn-only
```

## 13. 人工确认问题

```text
EDA 警告是否需要在模型路由前先修正数据？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 数据文件缺失 | 回到 intake 或请求人工补充。 |
| 字段含义不明 | 标记为风险，不自行猜测。 |
| EDA 代码失败 | 记录失败命令和报错，先修复数据读取。 |
| 图表无法生成 | 保留表格摘要，不晋升为正式图。 |

## 15. 完成条件

```text
- 数据质量和字段含义风险已记录。
- EDA 产物没有被当作冻结结果。
- 下游模型路由可以读取本阶段摘要。
```
