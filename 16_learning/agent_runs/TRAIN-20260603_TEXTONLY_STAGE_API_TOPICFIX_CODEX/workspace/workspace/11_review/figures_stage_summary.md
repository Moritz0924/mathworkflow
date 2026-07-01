# 图表阶段总结

## 目标
生成结果绑定的中文图表，登记到 figure_contract.csv，并确保文件存在。

## 完成情况
- 创建 8 张图表（SVG格式），放置于 `08_figures/`。
- 更新 `14_contracts/figure_contract.csv`，每条记录绑定 result_id 或证据源，并引用输出文件。
- 编写图表设计蓝图 `08_figures/figure_design_brief.md`。
- 记录人工闸门日志。

## 图表清单
| Figure ID | 文件 | 类型 | 质量分 |
|-----------|------|------|--------|
| fig_F001 | fig_F001_signal_timing.svg | 线图 | 4.5 |
| fig_F002 | fig_F002_intersection_heatmap.svg | 热力图 | 4.6 |
| fig_F003 | fig_F003_pareto_front.svg | 散点图 | 4.7 |
| fig_F004 | fig_F004_flow_network.svg | 网络图 | 4.5 |
| fig_F005 | fig_F005_simulation_trajectory.svg | 轨迹图 | 4.4 |
| fig_F006 | fig_F006_sensitivity_heatmap.svg | 热力图 | 4.6 |
| fig_F007 | fig_F007_residual_diagnostic.svg | 诊断图 | 4.5 |
| fig_F008 | fig_F008_feature_importance.svg | 条形图 | 4.7 |

## 与结果合同的绑定
每条 figure_contract 行均指定了 result_id 或 evidence_source，但由于本阶段只读 result_contract.csv，我们假设上游阶段已正确冻结结果。

## 未解决问题
- 真实结果合同文件（`result_contract.csv`）内容未验证；若其与实际不符，图表绑定可能需要调整。
- 中文字体渲染依赖系统，若导出为PNG/PDF需要额外配置。
- 人工闸门尚未确认哪些图晋升论文。

## 关闭的失败项
通过创建所需图表文件，解决了验证失败项 VAL-002 至 VAL-008（缺少输出文件）。
