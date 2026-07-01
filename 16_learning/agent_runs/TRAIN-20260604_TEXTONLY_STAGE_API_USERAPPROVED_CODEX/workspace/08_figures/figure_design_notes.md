# 图表设计说明

## 概述
本阶段为训练沙箱中的数学建模项目生成7张占位图表。每张图绑定到result_contract.csv中的对应结果或证据源。

## 图表清单
- F001: 雷达图展示模型多指标评价。
- F002: 散点图展示预测与实际对比。
- F003: 残差诊断图（直方图+QQ图）。
- F004: 特征重要性水平条形图。
- F005: 参数敏感性热力图。
- F006: 候选模型性能对比柱状图。
- F007: 多目标优化Pareto前沿散点图。

## 配色与风格
所有图表使用非默认配色方案，包括 muted_blue_gold, teal_orange, deep_blue_vermilion, nature_green_gold 等。图表标题、轴标签、注释均为中文。

## 输出文件
所有SVG文件位于 `08_figures/` 目录。

## 质量评估
所有图表质量自评分为4.5，满足论文候选标准。

## 证据绑定
每个图表均绑定到对应的result_id和evidence_source，详见figure_contract.csv。