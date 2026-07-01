# Training Sandbox Prompt Backup: results_freeze

Formal source prompt: `prompts/stages/07_results_freeze.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

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

将已核验代码输出晋升为冻结结果行，使 `result_contract.csv` 成为论文数字的最高结构化来源。算力集中在来源追踪、指标口径、数值一致性、复现证据、人工确认和下游图表/论断可用性上。

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
- 不得把探索性 EDA 数字晋升为模型结果。
- 不得冻结缺少 source_file、metric_name 或 metric_value 的论文可用结果。
```

## 8. 必需输出

```text
- 07_results/result_freeze_report.md
- 14_contracts/result_contract.csv 中冻结或待冻结行
- 14_contracts/artifact_freeze_registry.csv 中相关条目
- 每个结果的 source_file、source_row_or_cell、code_file、run_id、random_seed 和 freeze_status 说明
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

输入核验：
1. 检查 07_results/ 中真实输出、06_code/ 运行日志和 result_contract.csv 表头。
2. 确认每个候选结果都有可定位的源文件、代码文件和运行记录。
3. 确认当前阶段为 hard gate，未获人工确认前不得进入 figures 或 paper_draft。

阶段目标：
逐项核对代码输出、来源文件、指标名称、指标值和可复现性；只有真实运行且可追溯的结果才能写入 result_contract 并标记冻结。

深度分析：
1. 为每个候选结果建立冻结审查表：result_id、question_id、model_id、metric_name、metric_value、unit、source_file、source_row_or_cell、code_file、run_id、random_seed。
2. 对照运行日志和输出文件确认数值没有被手工改写。
3. 检查指标口径：单位、方向、是否越大越好、是否与模型路线一致、是否可被图表或论断使用。
4. 将不确定结果标记 blocked 或 draft，不得冻结。
5. 对可论文使用的结果登记 artifact_freeze_registry，并说明 protected_atoms。

证据绑定：
每个 frozen 结果必须绑定真实文件和代码运行记录；下游图表和论断只能引用 frozen 或 ready 且可复核的结果。

风险清单：
记录结果不可复现、指标含义不明、随机性不稳定、源文件缺失、单位不明、异常值和人工未确认风险。

自检清单：
1. 没有改变结果数值。
2. 没有冻结未运行结果。
3. 每个论文可用结果都有 source_file、metric_name、metric_value。
4. 下游引用字段已预留或说明。
5. 校验命令已运行或记录 not_run。

人工确认输出：
请人类批准将这些数值结果冻结为论文唯一可用结果来源。
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
| 数值与日志不一致 | 停止冻结，重新运行或人工复核。 |
| 人工未确认 | 停在 `results_freeze_gate`。 |

## 15. 完成条件

```text
- 每个论文可用结果都有来源文件、代码文件、指标名称和指标值。
- 冻结状态与人工复核一致。
- 下游图表和论文只能读取冻结结果。
- 不确定结果已标记 blocked 或 draft。
- 未触发本阶段禁止动作。
```

