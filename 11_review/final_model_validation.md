# 终稿模型与冻结结果复核

- 结论：**PASS**
- 冻结包：`RF-20260722T114756Z`
- 边界：冻结方案复核；不声明全局最优，不改变模型假设。

## 核心指标

| 指标 | 冻结值 / s |
|---|---:|
| Q1/primary_duration_M1 | 1.362201500 |
| Q2/primary_duration_M1 | 2.238164377 |
| Q5/objective_total_duration | 6.097008562 |
| Q5/objective_minimum_duration | 1.876800871 |

## 复核项

| 检查 | 状态 | 说明 |
|---|---|---|
| frozen_metric_status | pass | 冻结汇总含 9 项指标，状态集合为 ['frozen']。 |
| result_contract_alignment | pass | 冻结 CSV 与结果合同逐项对齐；最大绝对差 0.000e+00 s。 |
| row_interval_duration | pass | 复算 23 条方案记录的区间长度；最大绝对差 0.000e+00 s。 |
| question_aggregate_metrics | pass | 按区间并集复算 Q1--Q5 汇总指标；最大绝对差 0.000e+00 s。 |
| physical_and_timing_constraints | pass | 速度、时序、起爆高度和同机投放间隔均满足冻结实现约束。 |
| q5_assignment | pass | Q5 使用 FY1→M1、FY2→M2、FY5→M3，每枚导弹均获得正遮蔽。 |
| seed_stability | pass | 三个登记随机种子逐指标一致；最大跨度 0.000e+00 s。 |
| grid_tolerance_convergence | pass | 较上一档加密配置，最终严格复算的主指标最大变化 2.039e-04 s，低于登记稳定性阈值 0.05 s。 |
| a03_sensitivity | pass | 取消干扰弹水平速度继承后，登记指标均降为 0 s，结论对 A03 高敏感。 |
| a07_sensitivity | pass | 本组方案的烟幕未在有效区间触地，A07 变体最大变化 0.000e+00 s。 |
| a08_sensitivity | pass | 将全点遮蔽放宽到 80% 覆盖后指标不下降，且 M2 出现显著增量，说明结论受 A08 口径影响。 |

## 结论边界

本报告证明冻结 CSV、合同、区间并集、约束和登记稳定性情景相互一致。它不扩大搜索预算，也不把当前可复现冻结方案解释为全局最优解。
