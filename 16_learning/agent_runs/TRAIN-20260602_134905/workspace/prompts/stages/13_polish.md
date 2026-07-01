# 阶段提示词：`polish` - 事实保持润色

> 中文注释：使用阶段为 `polish`；使用场景是在修订关闭后，仅改进语言表达并保护数字、公式、引用和结果含义。

## 1. 阶段身份

```yaml
stage_id: polish
stage_name: 事实保持润色
stage_order: 13
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P5
```

## 2. 目标

在保留所有受保护事实原子和结果含义的前提下改进表达。

## 3. 必需输入

```text
- 已确认草稿章节
- 14_contracts/artifact_freeze_registry.csv
- 14_contracts/polish_diff_check.csv
```

## 4. 可选输入

```text
- 10_polish/polish_rules.md
- 人工语言风格偏好
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 02_latex_template/
- 09_paper/
- 10_polish/
- 14_contracts/
```

## 6. 允许写入路径

```text
- 02_latex_template/sections/
- 09_paper/
- 10_polish/
- 14_contracts/polish_diff_check.csv
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 不得改变数字、公式、标签、引用、文献、模型名或结果含义。
- 不得强化弱结论。
- 不得删除图表或公式引用。
- 不得把润色当作事实修订。
- 不得把中文论文润色成英文，或引入英文段落；必要的英文缩写、变量名、模型名和 LaTeX 命令除外。
```

## 8. 必需输出

```text
- 润色后的章节
- polish_diff_check.csv
- 受保护事实原子检查说明
- 阶段总结
- 润色后的正文、图注、表注和面向评审说明必须保持中文。
```

## 9. 合同更新

```text
可更新：polish_diff_check.csv
只读：其他合同和冻结登记
```

## 10. 允许技能

```text
- nature-polishing（如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 polish 阶段。
只改进语言流畅度和清晰度，不改变任何受保护事实。
润色前后必须比较数字、公式、标签、引用、模型名和结果含义。
润色输出必须保持中文表达，不得改写为英文；图题、表题、图注、表注和正文说明仍需为中文。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage polish
```

## 13. 人工确认问题

```text
润色后的章节是否在提升可读性的同时保留了全部事实？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 受保护事实变化 | 回滚该润色片段，记录 fail。 |
| LaTeX 被破坏 | 修复语法，不改变内容事实。 |
| 润色需要新增解释 | 转为 revision 任务，不在本阶段新增事实。 |
| 差异检查不可用 | 标记未运行，不声称通过。 |

## 15. 完成条件

```text
- polish_diff_check 没有受保护事实变化。
- LaTeX 结构保持可编译。
- 润色只改善表达。
- 润色后仍为中文论文文本。
```
