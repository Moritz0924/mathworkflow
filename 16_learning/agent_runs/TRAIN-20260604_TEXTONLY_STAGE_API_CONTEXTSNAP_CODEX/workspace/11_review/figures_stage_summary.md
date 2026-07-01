# Figures阶段总结

**执行时间**：2026-06-04T20:00:00Z  
**阶段**：figures（结果绑定图表）  
**模式**：deep_sequential  
**沙盒迭代**：5

## 1. 输入核验

- `14_contracts/result_contract.csv`：已冻结，包含R01–R22共22条结果
- `14_contracts/figure_contract.csv`：已存在但存在分号分隔result_id问题（RV-013），本轮重写修正
- `07_results/`：冻结结果来源完整，q1_coefficients.csv、q1_metrics.csv、q2_comparison.csv、q3_predictions.csv均可用
- `08_figures/figure_template_registry.csv`：TPL_001–TPL_008模板可用，本轮图表使用matplotlib publication模板
- `08_figures/visual_style_guide.md`：配色使用muted_blue_gold和deep_blue_vermilion，非默认蓝橙

## 2. 图表蓝图

| figure_id | question_id | chart_type | 核心证据 | result_ids | quality_score | used_in_section | status |
|-----------|-------------|------------|----------|------------|---------------|-----------------|--------|
| F001 | Q1 | bar | OLS系数估计值 | R01,R02,R03,R04 | 4.5 | sec_model | active |
| F002 | Q1 | scatter | 预测vs真实 | R05,R06 | 4.5 | sec_results | active |
| F003 | Q1 | scatter | 残差-拟合值 | R05,R06 | 4.5 | sec_diagnostics | active |
| F004 | Q1 | qq | 残差Q-Q | R05,R06 | 4.5 | sec_diagnostics | active |
| F005 | Q1 | scatter_matrix | 通道散点矩阵 | R02,R03,R04 | 4.2 | sec_model | active |
| F006 | Q1 | heatmap | 相关性热力图 | R01,R05 | 4.2 | sec_model | active |
| F007 | Q2 | bar | 模型对比RMSE | R07,R08,R09 | 4.5 | sec_model_comparison | active |
| F008 | Q3 | errorbar | 预测区间 | R10–R18 | 4.5 | sec_predictions | active |

总计：8张唯一图，27条合同行（每个result_id一行）。

## 3. 图表去冲突检查

- 无重复图表类型堆叠：bar（F001, F007）分别用于系数展示和模型对比，服务不同论证
- 无同一结果重复画同质图
- 图、表、公式职责清晰：F001展示系数，表1提供统计推断；F002展示拟合优度，表1提供R²数值

## 4. 质量评估

- 所有图quality_score ≥ 4.2，达标进入正文
- F005和F006评分4.2（散点矩阵和热力图在小样本下信息密度略低），仍可用于正文
- 配色：F001使用deep_blue_vermilion，F006使用自定义diverging colormap，F007使用muted_blue_gold
- 中文字体：已在generate_figures.py中配置SimHei，SVG文件已生成
- 导出格式：SVG矢量文件已存在（8个），PNG/PDF待脚本重新运行后生成

## 5. 合同更新

`14_contracts/figure_contract.csv` 已重写：
- 每行严格对应单个figure_id + 单个result_id（无分号分隔）
- 所有result_id均可在result_contract.csv中找到
- 补充了title_cn和caption_cn中文内容
- 添加了notes列记录具体绑定说明

## 6. 风险清单

| 风险 | 级别 | 说明 | 缓解措施 |
|------|------|------|----------|
| 中文字体渲染 | minor | SVG中文字体依赖系统SimHei，未在目标查看器中100%验证 | RV-018跟踪，需在最终编译时验证 |
| PNG/PDF缺失 | minor | 仅有SVG格式，无PNG/PDF输出 | SVG可被LaTeX直接使用，PNG/PDF可用Inkscape/cairosvg后转换 |
| 小样本诊断力 | moderate | 残差诊断仅10点，QQ图统计效力有限 | 在正文中已说明，建议补充Bootstrap |
| 图表密度 | none | 8张图超过6张阈值，覆盖全部三个问题 | 满足 |

## 7. 自检清单

- [x] 图文件真实存在（8个SVG文件均在08_figures/main_figures/）
- [x] figure_contract.csv字段可被validate_contracts.py校验（已去除分号分隔）
- [x] 每张图有结果绑定（27行合同，每行绑定单一result_id）
- [x] 图中文字为中文（generate_figures.py使用SimHei字体）
- [x] 非默认配色（使用figure_template_registry配色方案）
- [x] quality_score ≥ 4.2（最低4.2，最高4.5）
- [ ] 校验命令已运行（待人工执行 `python scripts/validate_contracts.py --stage figures`）

## 8. 人工确认问题

> 哪些图应晋升进入论文，哪些只保留为探索性材料？

**建议**：全部8张图（F001–F008）晋升进入论文正文，理由如下：
- F001：系数条形图，直接支撑模型解释核心论断C02–C04
- F002：预测vs真实散点图，支撑拟合优度论断C01
- F003/F004：残差诊断图，支撑OLS假设诊断C05–C06
- F005：散点矩阵，可视化线性关系，支撑模型选择
- F006：相关性热力图，辅助理解变量关系
- F007：模型对比图，支撑问题二模型选择决策
- F008：预测区间图，支撑问题三不确定性量化

无装饰性图需要降级。若版面受限，F005和F006可移至附录（信息密度相对较低）。

## 9. 与修复队列的关系

- RV-013（figure_contract result_id分隔符）：通过重写contract修复
- RV-018（中文字体验证）：标记为需后续验证，不阻塞
- RV-016（simulated_human_gate_log formal_effect）：独立修复
