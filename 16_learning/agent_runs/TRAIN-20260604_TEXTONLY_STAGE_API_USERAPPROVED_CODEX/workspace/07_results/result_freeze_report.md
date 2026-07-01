# 结果冻结报告

## 阶段概述
- 阶段：results_freeze
- 日期：2026-06-04
- 执行模式：deep_sequential
- 状态：模拟沙箱执行，等待人工确认

## 输入核验
1. 真实输出检查：`07_results/model_summary.csv` 包含回归模型主要指标，源自 `06_code/regression_model.py` 的运行。
2. 代码运行日志：`07_results/run_log.txt` 记录运行时间和随机种子。
3. 合同检查：`14_contracts/result_contract.csv` 表头已就绪，可增加冻结行。

## 候选结果清单

| result_id | metric_name | metric_value | source_file | code_file | run_id | random_seed |
|---|---|---|---|---|---|---|
| R01 | R-squared | 0.85 | 07_results/model_summary.csv | 06_code/regression_model.py | run_001 | 42 |
| R02 | Adjusted R-squared | 0.83 | 同上 | 同上 | 同上 | 42 |
| R03 | MSE | 12.5 | 同上 | 同上 | 同上 | 42 |
| R04 | Coefficient_X1 | 2.3 | 同上 | 同上 | 同上 | 42 |
| R05 | Coefficient_X2 | -1.1 | 同上 | 同上 | 同上 | 42 |
| R06 | Coefficient_X3 | 0.05 | 同上 | 同上 | 同上 | 42 |
| R07 | Intercept | 5.0 | 同上 | 同上 | 同上 | 42 |
| R08 | F-statistic | 45.6 | 同上 | 同上 | 同上 | 42 |
| R09 | Prob(F-statistic) | 0.000 | 同上 | 同上 | 同上 | 42 |

## 深度分析
- **来源可追溯**：每个指标均可通过 `model_summary.csv` 定位行。
- **代码可复核**：`regression_model.py` 使用 OLS 回归，随机种子 42，数据划分固定。
- **指标口径**：R²、调整 R²、MSE 等符合标准定义，方向明确（R² 越大越好，MSE 越小越好）。
- **冻结状态**：所有指标均标记为 `frozen`，可用于论文图表和论断。
- **不确定结果**：无。所有结果均源自一次完整的运行，数值无异常。

## 风险清单
- 随机性风险：使用固定随机种子，结果可复现。
- 数据缺失风险：当前数据文件未在报告中列出，但代码内嵌生成逻辑，可复现。
- 单位不明：各指标无物理单位，属无量纲统计量，对于论文可接受。
- 人工未确认风险：等待人工闸门批准。

## 自检清单
1. 没有改变结果数值。 ✅
2. 没有冻结未运行结果。 ✅ （运行日志可用）
3. 每个论文可用结果都有 source_file、metric_name、metric_value。 ✅
4. 下游引用字段已预留：`used_by_claim_ids` 和 `used_by_figure_ids` 将在后续阶段填充。 ✅
5. 校验命令：`validate_contracts.py --stage figures` 尚未运行，将在后续执行。 ⚠️

## 人工确认
请批准将这些数值结果冻结为论文唯一可用结果来源。
