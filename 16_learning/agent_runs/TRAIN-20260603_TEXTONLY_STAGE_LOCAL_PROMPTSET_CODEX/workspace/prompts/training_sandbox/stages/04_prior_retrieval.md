# Training Sandbox Prompt Backup: prior_retrieval

Formal source prompt: `prompts/stages/04_prior_retrieval.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`prior_retrieval` - 先验经验卡片检索

> 中文注释：使用阶段为 `prior_retrieval`；使用场景是在模型路由前，从先验材料中提取经验卡片、图表族提示和评分风险提示，但不复制历史论文文本。

## 1. 阶段身份

```yaml
stage_id: prior_retrieval
stage_name: 先验经验卡片检索
stage_order: 4
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P2
```

## 2. 目标

从先验材料中抽取可复用建模经验卡片，不复制历史论文文本。算力集中在题型匹配、模型族倾向、常见图表族、评分风险和结构缺口上，输出必须保持 advisory_only。

## 3. 必需输入

```text
- config/prior_db_policy.yaml
- 01_task_analysis/problem_model_profile.csv
```

## 4. 可选输入

```text
- 13_prior_db/
- 13_sample_prior/
- 01_task_analysis/task_decomposition.md
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 01_task_analysis/
- 13_prior_db/
- 13_sample_prior/
```

## 6. 允许写入路径

```text
- 13_prior_db/
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 不得复制历史论文摘要、正文、表格、图注或结论。
- 不得把历史论文当作当前题目的事实答案。
- 不得输出可直接粘贴到论文的段落。
- 不得绕过 prior_db_policy.yaml。
- 不得使用先验材料替代题面、数据、代码或合同证据。
- 不得把低样本类别提示包装成强推荐。
```

## 8. 必需输出

```text
- 13_prior_db/pre_solve_cards.md 或等价经验卡片
- copy-risk 或风险说明
- 与 problem_model_profile.csv 对齐的模型族、图表族、评分风险摘要
- 阶段总结
```

## 9. 合同更新

```text
可更新：无
只读：14_contracts/*.csv
```

## 10. 允许技能

```text
- nature-reader（如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 prior_retrieval 阶段。

输入核验：
1. 检查 config/prior_db_policy.yaml 和 01_task_analysis/problem_model_profile.csv。
2. 若 13_prior_db/cards/prior_cards.jsonl 可读，则优先使用其中 copy_risk_status=abstracted_pass 的抽象卡片。
3. 可参考 13_prior_db/screening/pdf_manifest.csv 的类别、模型族和 source_count；不得读取未授权路径。

阶段目标：
只抽取题型经验、常见模型族、常见图表类型、评分风险和预处理模式；不得生成当前题目的答案。

深度分析：
1. 将每个子问题画像映射到先验卡片的 problem_type、family、model_hints、figure_hints 和 scoring_risks。
2. 对候选模型族给出支持理由和风险理由，区分高样本规律与低样本警告。
3. 对图表族只输出抽象建议，例如权重热力图、Pareto 前沿图、残差诊断组图、机制示意图；不得复用历史图注。
4. 对评分风险输出可行动提醒，例如约束不可追踪、残差诊断缺失、外推边界不清、权重来源弱。
5. 若检索结果与题面或 EDA 冲突，优先题面和数据，先验只记录为风险。

证据绑定：
每张经验卡片必须记录来源卡片 ID、类别、模型族、source_count 或 copy_risk_status；不得引用历史论文正文。

风险清单：
记录拷贝风险、低样本风险、题型不匹配风险、先验与题面冲突风险和技能不可用风险。

自检清单：
1. 输出保持 advisory_only。
2. 没有历史论文可复制文本。
3. 没有当前题目事实答案。
4. 没有把先验卡片写入结果、图表或论文合同。
5. 校验命令已运行或记录 not_run。

人工确认输出：
请人类确认这些先验卡片只作为提示使用，且无复制历史表述或结构。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage prior_retrieval
```

```bash
python scripts/check_prior_copy_risk.py --warn-only
```

## 13. 人工确认问题

```text
这些先验卡片是否只作为提示使用，且没有复制历史表述、图注、表格或结论？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 先验库不存在 | 创建空经验卡片占位，并说明没有可用先验。 |
| 拷贝风险过高 | 丢弃相关文本，只保留抽象经验标签。 |
| 问题画像缺失 | 返回 task_analysis 补齐画像。 |
| 技能不可用 | 记录未运行，使用本地保守模板。 |
| 先验与题面冲突 | 保留题面优先原则，将先验记录为风险而非建议。 |

## 15. 完成条件

```text
- 输出只包含经验卡片和风险提示。
- 没有历史论文可复制文本。
- 每条建议标明 advisory_only。
- 下游模型路由能读取卡片 ID 或提示。
- 未触发本阶段禁止动作。
```

