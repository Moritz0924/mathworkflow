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

只在图表能支撑已登记结果、证据或论断时，设计并生成图表。

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
```

## 8. 必需输出

```text
- 图表文件
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
每张图都必须绑定结果、证据或论断，并有真实输出路径。
优先生成能解释模型结果的图，避免装饰性图表。
最终图表必须面向中文论文：标题、坐标轴、图例、注释、节点文字和图中说明均使用中文；图片生成提示词也必须写明“图片中的文字为中文”。必要的英文缩写、变量名和指标名可以保留。
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

## 15. 完成条件

```text
- 论文候选图都有真实文件和合同记录。
- 图表与冻结结果或论断绑定。
- 下游论文可安全引用已登记图。
- 图中文字已检查为中文。
```
