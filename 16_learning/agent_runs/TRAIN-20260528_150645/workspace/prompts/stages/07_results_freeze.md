# 阶段提示词：`results_freeze` - 结果冻结

> 中文注释：使用阶段为 `results_freeze`；使用场景是在代码真实运行后，将可复核结果登记并冻结为论文可用结果来源。

## 1. 阶段身份

```yaml
stage_id: results_freeze
stage_name: 结果冻结
stage_order: 7
gate_type: hard
execution_mode: deep_sequential
roadmap_item: P4
```

## 2. 目标

将已核验代码输出晋升为冻结结果行，使 `result_contract.csv` 成为论文数字的最高结构化来源。

## 3. 必需输入

```text
- 07_results/ 中真实模型输出
- 06_code/ 运行日志
- 14_contracts/result_contract.csv
```

## 4. 可选输入

```text
- 05_model/model_route.md
- 14_contracts/formula_contract.csv
- 人工结果复核说明
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 05_model/
- 06_code/
- 07_results/
- 14_contracts/
```

## 6. 允许写入路径

```text
- 07_results/
- 14_contracts/result_contract.csv
- 14_contracts/artifact_freeze_registry.csv
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 不得冻结未运行或不可复核的结果。
- 不得改变模型输出数值。
- 不得为通过校验而删除结果风险。
- 不得在人工闸门前进入图表或论文阶段。
```

## 8. 必需输出

```text
- 07_results/result_freeze_report.md
- 14_contracts/result_contract.csv 中冻结或待冻结行
- 14_contracts/artifact_freeze_registry.csv 中相关条目
- 阶段总结和人工闸门说明
```

## 9. 合同更新

```text
可更新：result_contract.csv, artifact_freeze_registry.csv
只读：其他合同
```

## 10. 允许技能

```text
- 无
```

## 11. 代理提示词模板

```text
你正在执行 results_freeze 阶段。
逐项核对代码输出、来源文件、指标名称、指标值和可复现性。
只有真实运行且可追溯的结果才能写入 result_contract 并标记冻结。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage figures
```

## 13. 人工确认问题

```text
是否批准将这些数值结果冻结为论文唯一可用结果来源？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 来源文件缺失 | 不冻结该结果，返回 codegen。 |
| 指标含义不明 | 标记为 blocked，等待人工解释。 |
| 结果不可复现 | 保留候选结果但不进入论文。 |
| 人工未确认 | 停在 `results_freeze_gate`。 |

## 15. 完成条件

```text
- 每个论文可用结果都有来源文件和指标说明。
- 冻结状态与人工复核一致。
- 下游图表和论文只能读取冻结结果。
```
