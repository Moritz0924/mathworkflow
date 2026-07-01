# 阶段提示词：`paper_draft` - 分章节论文草稿

> 中文注释：使用阶段为 `paper_draft`；使用场景是在结果、图表、公式、引用和论断合同齐备后，逐章节生成证据绑定草稿。

## 1. 阶段身份

```yaml
stage_id: paper_draft
stage_name: 分章节论文草稿
stage_order: 9
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P5
```

## 2. 目标

一次只草拟一个章节，内容必须来自已登记论断、结果、公式、图表和引用。

## 3. 必需输入

```text
- 14_contracts/claim_evidence_map.csv
- 14_contracts/result_contract.csv
- 14_contracts/figure_contract.csv
- 14_contracts/formula_contract.csv
- 14_contracts/citation_contract.csv
```

## 4. 可选输入

```text
- 02_latex_template/sections/
- 09_paper/section_generation_plan.csv
- 人工写作要求
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 00_problem/
- 01_task_analysis/
- 02_latex_template/
- 05_model/
- 07_results/
- 08_figures/
- 09_paper/
- 14_contracts/
```

## 6. 允许写入路径

```text
- 02_latex_template/sections/
- 09_paper/
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 不得写无证据论断。
- 不得引用未登记图表。
- 不得新增未登记结果数字。
- 不得一次性生成全文。
- 不得生成英文正文作为论文最终内容；必要的英文缩写、变量名、模型名和 LaTeX 命令除外。
```

## 8. 必需输出

```text
- 指定章节草稿
- 09_paper/missing_evidence_report.md（如有缺口）
- 章节论断记录或更新
- 阶段总结
- 指定章节草稿必须为中文；图表标题、图注和正文中对图表的解释必须使用中文。
```

## 9. 合同更新

```text
可更新：claim_evidence_map.csv 草稿行（如流程允许）
只读：result_contract.csv, figure_contract.csv, formula_contract.csv, citation_contract.csv
```

## 10. 允许技能

```text
- nature-writing（如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 paper_draft 阶段。
只写当前章节，只使用合同中可追踪的论断和证据。
证据不足时写入缺失证据报告，而不是写强结论。
最终写入论文的章节内容必须为中文。图题、表题、图注、表注和对图表的解释必须为中文；必要英文缩写、变量名、文件名、LaTeX 命令和指标名可以保留。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage paper_draft
```

## 13. 人工确认问题

```text
是否有重要论断缺少证据，因此不应写入正文？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 论断无证据 | 写入缺失证据报告，不写正文强结论。 |
| 图表合同缺失 | 返回 figures 补合同。 |
| 结果合同缺失 | 返回 results_freeze。 |
| 引用未验证 | 降级为背景说明或删除引用句。 |

## 15. 完成条件

```text
- 章节文本可追踪到合同。
- 缺失证据已显式记录。
- 没有越权写入未证实结论。
- 章节正文、图注和表注为中文。
```
