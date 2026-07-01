# Training Sandbox Prompt Backup: polish

Formal source prompt: `prompts/stages/13_polish.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Preserve the locked problem topic throughout the sandbox run; do not drift to unrelated prior benchmark topics such as AQI or wine quality.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`polish` - 事实保持润色

> 中文注释：使用阶段为 `polish`；使用场景是在修订关闭后，仅改进语言表达并保护数字、单位、公式、标签、引用、模型名和结果含义。

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

在保留所有受保护事实原子和结果含义的前提下改进表达。算力集中在句式清晰、段落衔接、中文学术表达、冗余压缩和逐项差异核验上。

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
- 不得改动单位、随机种子、指标名称、图表编号、表格编号或 citation key。
- 不得让 protected_atom_delta_count 大于 0。
```

## 8. 必需输出

```text
- 润色后的章节
- polish_diff_check.csv
- 受保护事实原子检查说明
- 润色差异说明
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

输入核验：
1. 检查 artifact_freeze_registry.csv 和 polish_diff_check.csv。
2. 确认 revision 阶段已关闭 fail/major 问题或有人类豁免。
3. 确认只做语言润色，不新增事实。

阶段目标：
只改进语言流畅度、逻辑衔接和中文表达，不改变任何受保护事实。

深度分析：
1. 提取受保护事实原子：数字、单位、公式、标签、引用、citation key、文献、模型名、结果含义、图表编号、表格编号。
2. 逐段润色：压缩冗余、增强中文学术表达、消除歧义、改善段落衔接。
3. 对每个润色片段执行前后比对：changed_numbers、changed_units、changed_formulas、changed_labels、changed_refs、changed_citations、changed_model_names、changed_result_meanings。
4. 若任何保护原子变化，回滚该片段或转为 revision 任务，不在 polish 阶段强行处理。
5. 弱证据句只能更谨慎，不得润色成强结论。

证据绑定：
polish_diff_check.csv 必须记录 check_id、artifact_id、original_path、polished_path、protected_atom_delta_count、decision 和 review_note；默认 protected_atom_delta_count=0。

风险清单：
记录事实原子变化、LaTeX 破坏、中文表达歧义、弱结论强化、引用丢失和差异检查不可用风险。

自检清单：
1. protected_atom_delta_count 为 0。
2. changed_numbers/changed_formulas/changed_labels/changed_refs 均为否或空。
3. 没有新增事实。
4. 润色后仍为中文。
5. LaTeX 结构未破坏。
6. 校验命令已运行或记录 not_run。

人工确认输出：
请人类确认润色后的章节是否在提升可读性的同时保留了全部事实。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage polish
```

## 13. 人工确认问题

```text
润色后的章节是否在提升可读性的同时保留了全部数字、单位、公式、标签、引用、模型名和结果含义？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 受保护事实变化 | 回滚该润色片段，记录 fail。 |
| LaTeX 被破坏 | 修复语法，不改变内容事实。 |
| 润色需要新增解释 | 转为 revision 任务，不在本阶段新增事实。 |
| 弱结论被强化 | 改回谨慎表达，并记录风险。 |
| 差异检查不可用 | 标记未运行，不声称通过。 |

## 15. 完成条件

```text
- polish_diff_check 没有受保护事实变化。
- protected_atom_delta_count 默认且实际为 0。
- LaTeX 结构保持可编译。
- 润色只改善表达。
- 润色后仍为中文论文文本。
- 未触发本阶段禁止动作。
```

