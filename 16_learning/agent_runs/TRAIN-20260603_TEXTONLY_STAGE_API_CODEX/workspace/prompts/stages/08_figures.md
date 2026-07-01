# 阶段提示词：`figures` - 结果绑定图表

> 中文注释：使用阶段为 `figures`；使用场景是在结果冻结后，设计和生成只服务于已登记结果、证据或论断的正式图表。

## 1. 阶段身份

```yaml
stage_id: figures
stage_name: 结果绑定图表
stage_order: 8
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P6
```

## 2. 目标

只在图表能支撑已登记结果、证据或论断时，设计并生成图表。算力集中在图表蓝图、图表类型选择、证据绑定、配色、中文标注、图表去冲突、导出质量和 `figure_contract.csv` 登记上。

## 3. 必需输入

```text
- 14_contracts/result_contract.csv
- 14_contracts/figure_contract.csv
- 07_results/ 中冻结结果来源
```

## 4. 可选输入

```text
- 08_figures/visual_style_guide.md
- 08_figures/chart_type_library.md
- 人工图表偏好
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 07_results/
- 08_figures/
- 14_contracts/
```

## 6. 允许写入路径

```text
- 08_figures/
- 14_contracts/figure_contract.csv
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 不得引用未冻结结果。
- 不得生成无论断支撑的装饰图。
- 不得在图文件不存在时登记为论文可用。
- 不得伪造图表质量分或标签。
- 不得生成英文标题、英文坐标轴、英文图例或英文注释的正式图表；必要的指标缩写和变量名除外。
- 不得使用默认配色或低辨识度配色作为正式图表风格。
- 不得为了凑数量生成重复、冲突或不服务论证的图。
```

## 8. 必需输出

```text
- 图表文件
- 图表蓝图或图表设计说明
- 14_contracts/figure_contract.csv 更新
- 图表质量或风险说明
- 阶段总结
- 所有正式图表中的标题、坐标轴、图例、注释、节点文字和说明文字必须为中文；图片生成提示词也必须明确要求图中文字为中文。
```

## 9. 合同更新

```text
可更新：figure_contract.csv
只读：result_contract.csv, claim_evidence_map.csv, formula_contract.csv, citation_contract.csv
```

## 10. 允许技能

```text
- nature-figure（如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 figures 阶段。

输入核验：
1. 检查 result_contract.csv、figure_contract.csv 和 07_results/ 中冻结结果来源。
2. 读取 08_figures/figure_template_registry.csv（若存在），优先使用 TPL_001 到 TPL_008 的高级模板。
3. 若需要参考 13_prior_db/cards/prior_cards.jsonl、16_learning/training_data/corpus_features.csv 或 16_learning/reports/training_report.md，只能使用上游阶段已经写入允许路径的摘要；本阶段不得直接读取未授权路径。

阶段目标：
每张图都必须绑定结果、证据或论断，并有真实输出路径。优先生成能解释模型结果、机制、误差、权衡和敏感性的图，避免装饰性图表。

深度分析：
1. 建立图表蓝图矩阵：figure_id、question_id、core_claim、result_id/evidence_source、chart_type、panel_plan、used_in_section、latex_label、review_risk。
2. 按模型族和数据特征选择图表：
   - 统计评价：指标体系层级图、权重热力图、综合得分矩阵图、排序坡度图。
   - 优化决策：目标约束结构图、Pareto 前沿图、路径/网络图、调度甘特图、敏感性热力图。
   - 预测回归：变量关系热力图、预测区间图、残差诊断组图、误差分布或 QQ 图。
   - 机理仿真：机制示意图、状态转移图、仿真轨迹图、参数敏感性图、情景对比图。
   - 机器学习：特征重要性图、混淆矩阵、误差诊断图、嵌入/聚类可视化、消融对比图。
3. 与语料规律对齐但不机械套数：优秀样本图表密度较高，整体图/表/公式提及中位数约 12/8/2；本阶段应保证正式图足以支撑核心论断，但不得凑重复图。
4. 图表去冲突：同一结果不重复画同质图；同一章节图表类型不堆叠；图、表、公式职责清晰。
5. 配色和风格：优先使用 figure_template_registry 的 muted_blue_gold、teal_orange_diverging、deep_blue_vermilion、nature_green_gold 等非默认配色；不得使用 matplotlib 默认蓝橙序列作为最终风格。
6. 导出要求：优先导出 svg/png/pdf 中至少一种真实存在文件，正式图建议保留矢量格式；质量分低于 4.2 的图不得进入正文。
7. 图中文字必须为中文，必要英文缩写、变量名和指标名可保留；图注必须来自合同绑定证据，不得复用历史图注。

证据绑定：
每张正式图必须写入 figure_contract.csv，并至少绑定 result_id 或 evidence_source；进入正文的图必须有 used_in_section 和 latex_label。

风险清单：
记录数据字段不足、图表类型不匹配、配色风险、中文字体风险、导出失败、质量分不足、合同绑定缺失和图表密度不足风险。

自检清单：
1. 图文件真实存在。
2. figure_contract.csv 字段可被 validate_contracts.py 校验。
3. 每张图有结果或证据绑定。
4. 图中文字为中文。
5. 非默认配色。
6. quality_score >= 4.2，或降级为探索性材料。
7. 校验命令已运行或记录 not_run。

人工确认输出：
请人类确认哪些图晋升进入论文，哪些只保留为探索性材料。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage figures
```

```bash
python scripts/check_figure_quality.py
```

## 13. 人工确认问题

```text
哪些图应晋升进入论文，哪些只保留为探索性材料？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 缺少冻结结果 | 返回 results_freeze。 |
| 图文件缺失 | 重新生成或将状态标为 blocked。 |
| 图表质量低 | 改进导出质量或降级为附录/探索图。 |
| 合同绑定缺失 | 补 `figure_contract.csv`，不先引用。 |
| 图表类型与数据不匹配 | 重新选择模板；若无合适图，记录不生成原因。 |
| 中文字体或配色失败 | 修复字体/配色后重导出，或降级为不可用。 |

## 15. 完成条件

```text
- 论文候选图都有真实文件和合同记录。
- 图表与冻结结果或论断绑定。
- 图表类型、数量和章节分布服务论证且不冲突。
- 下游论文可安全引用已登记图。
- 图中文字已检查为中文。
- 未触发本阶段禁止动作。
```
