# Training Sandbox Prompt Backup: task_analysis

Formal source prompt: `prompts/stages/03_task_analysis.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Preserve the locked problem topic throughout the sandbox run; do not drift to unrelated prior benchmark topics such as AQI or wine quality.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`task_analysis` - 任务拆解

> 中文注释：使用阶段为 `task_analysis`；使用场景是在题面和数据初查后，将赛题拆成可建模子问题、交付物、评价标准、依赖关系和风险边界。

## 1. 阶段身份

```yaml
stage_id: task_analysis
stage_name: 任务拆解
stage_order: 3
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. 目标

将赛题拆解为子问题、交付物、假设、依赖关系和建模要求。算力集中在题目问法、数据可用性、问题类型、输出格式、评价标准和下游依赖上，不提前选择最终模型或写结果。

## 3. 必需输入

```text
- 00_problem/problem_statement.md
- 00_problem/attachments_overview.md
- 03_data/data_quality_report.md（如已有数据）
```

## 4. 可选输入

```text
- 04_eda/eda_summary_for_paper.md
- 人工任务理解说明
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 00_problem/
- 01_task_analysis/
- 03_data/
- 04_eda/
```

## 6. 允许写入路径

```text
- 01_task_analysis/
- 10_ai_logs/
```

## 7. 禁止动作

```text
- 不得选择最终模型。
- 不得写模型结果。
- 不得忽略题目显式交付要求。
- 不得把先验论文内容写入题目拆解。
- 不得把题面歧义强行解释成单一路线。
- 不得为迎合常见模板而改变题目目标。
```

## 8. 必需输出

```text
- 01_task_analysis/task_decomposition.md
- 01_task_analysis/problem_model_profile.csv
- 01_task_analysis/question_dependency_map.md 或同等说明
- 子问题输入/输出/风险/交付物矩阵
- 阶段总结和风险说明
```

## 9. 合同更新

```text
可更新：无
只读：14_contracts/*.csv
```

## 10. 允许技能

```text
- 无
```

## 11. 代理提示词模板

```text
你正在执行 task_analysis 阶段。

输入核验：
1. 读取题面、附件概览和已有数据质量报告。
2. 确认没有跳过 intake/eda 的必要风险。
3. 只读写本阶段允许路径。

阶段目标：
拆解子问题、交付物、依赖和风险，为 prior_retrieval 与 model_route 提供问题画像；不得直接给出最终模型或结果。

深度分析：
1. 按官方问法拆出 Q1、Q2、Q3 等子问题，标明每个问题的目标、输入、输出、约束和评价口径。
2. 判断每个子问题更接近数据评价型、优化决策型、预测分析型、机理仿真型、机器学习型或混合型，但不得锁定模型。
3. 建立依赖关系：哪些问题依赖前一问结果、哪些共享数据、哪些需要人工假设。
4. 提取交付物要求：公式、算法、结果表、图表、方案建议、敏感性分析、误差分析或提交说明。
5. 识别评分风险：问题边界不清、目标函数不明确、评价标准缺失、数据支撑不足、结果可解释性不足。
6. 为先验检索输出关键词和模型族候选，但所有候选保持 advisory。

证据绑定：
拆解中的每个子问题必须对应题面语句、附件数据或 EDA 风险；无法绑定的解释写为待确认项。

风险清单：
记录题面歧义、数据不匹配、交付物冲突、依赖顺序不明和人工确认需求。

自检清单：
1. 未选择最终模型。
2. 未产生结果。
3. 未复制历史论文结构或文本。
4. 每个子问题都有输入、输出和风险。
5. 校验命令已运行或记录 not_run。

人工确认输出：
请人类确认拆解是否覆盖官方题目要求，以及是否接受保留的歧义解释。
```

## 12. 校验命令

```bash
python scripts/check_gates.py --dev-debug
```

## 13. 人工确认问题

```text
拆解结果是否与官方题目交付要求一致，是否需要合并、拆分或重命名子问题？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 题面不完整 | 回到 intake 补齐题面。 |
| 子问题边界不清 | 记录多种解释，交给人工确认。 |
| 数据与题目不匹配 | 写入风险报告，不强行建模。 |
| 依赖关系不明确 | 保守标记依赖，等待模型路由复核。 |
| 交付要求冲突 | 明确冲突来源并请求人工裁决。 |

## 15. 完成条件

```text
- 每个子问题都有输入、输出、依赖和风险描述。
- problem_model_profile.csv 能支持先验检索和模型路由。
- 后续阶段能读取问题画像。
- 未产生越权模型结论。
- 未触发本阶段禁止动作。
```

