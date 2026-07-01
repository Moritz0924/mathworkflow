# Training Sandbox Prompt Backup: paper_draft

Formal source prompt: `prompts/stages/09_paper_draft.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Preserve the locked problem topic throughout the sandbox run; do not drift to unrelated prior benchmark topics such as AQI or wine quality.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

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

一次只草拟一个章节，内容必须来自已登记论断、结果、公式、图表和引用。算力集中在章节论证链、证据密度、图表密度、公式解释、风险边界和中文表达上，不生成全文、不新增无证据事实。

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
- 不得为弥补图表或证据不足而编造解释。
- 不得复制历史论文段落、摘要、图注、表格或结论。
```

## 8. 必需输出

```text
- 指定章节草稿
- 09_paper/missing_evidence_report.md（如有缺口）
- 章节论断记录或更新
- 章节图表/公式/引用使用清单
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

输入核验：
1. 检查 claim_evidence_map、result_contract、figure_contract、formula_contract、citation_contract。
2. 确认只写当前指定章节，不生成全文。
3. 若需要参考先验资产 13_prior_db/cards/prior_cards.jsonl、16_learning/training_data/corpus_features.csv 或 training_report，只能使用上游已写入允许路径的摘要；不得直接读取未授权路径。

阶段目标：
只写当前章节，只使用合同中可追踪的论断和证据。证据不足时写入缺失证据报告，而不是写强结论。

深度分析：
1. 为本章节列出 claim_id 清单，逐项检查 evidence_type、result_id、figure_id、formula_id、citation_id 和 support_grade。
2. 设计章节论证链：问题背景、方法逻辑、关键公式、结果解释、图表证据、局限边界。
3. 检查图表密度和证据密度：图、表、公式不机械追求数量，但必须足以支撑核心论断；若核心结果没有图表或表格支撑，写入 missing_evidence_report。
4. 对每个结果数字只从 result_contract 引用；不得改写数值、单位和指标含义。
5. 对每张图只从 figure_contract 引用；图题、图注和正文解释必须与 core_claim 和 caption_source 一致。
6. 对公式只使用 formula_contract 中已定义符号；未定义符号不得进入正文。
7. 对引用只用于背景、方法或假设支撑，不得用文献元数据支撑当前数值结果。

证据绑定：
每个段落的核心句必须能追踪到 claim_id 或明确标记为过渡性说明；强结论必须有 result_id、figure_id、formula_id 或 citation_id。

风险清单：
记录无证据论断、图表不足、公式未定义、引用未核验、结果数值缺失、章节逻辑断裂和中文表达风险。

自检清单：
1. 只写当前章节。
2. 没有新增未登记结果。
3. 没有引用未登记图表。
4. 没有复制历史文本。
5. 章节正文、图注和表注为中文。
6. 校验命令已运行或记录 not_run。

人工确认输出：
请人类确认是否有重要论断缺少证据，因此不应写入正文。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage paper_draft
```

## 13. 人工确认问题

```text
是否有重要论断缺少证据，因此不应写入正文或应返回上游补证？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 论断无证据 | 写入缺失证据报告，不写正文强结论。 |
| 图表合同缺失 | 返回 figures 补合同。 |
| 图表密度不足 | 写入缺口报告或返回 figures，不凑装饰图。 |
| 结果合同缺失 | 返回 results_freeze。 |
| 引用未验证 | 降级为背景说明或删除引用句。 |
| 公式符号未定义 | 返回 model_route 或公式合同补齐。 |

## 15. 完成条件

```text
- 章节文本可追踪到合同。
- 缺失证据已显式记录。
- 没有越权写入未证实结论。
- 图表、表格、公式和引用密度足以支撑章节核心论证，或缺口已记录。
- 章节正文、图注和表注为中文。
- 未触发本阶段禁止动作。
```

