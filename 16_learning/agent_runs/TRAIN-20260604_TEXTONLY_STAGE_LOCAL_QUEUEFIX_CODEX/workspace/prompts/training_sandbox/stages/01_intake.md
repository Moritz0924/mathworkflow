# Training Sandbox Prompt Backup: intake

Formal source prompt: `prompts/stages/01_intake.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Preserve the locked problem topic throughout the sandbox run; do not drift to unrelated prior benchmark topics such as AQI or wine quality.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`intake` - 赛题接收

> 中文注释：使用阶段为 `intake`；使用场景是在收到赛题和附件后，整理题面、附件清单、比赛元数据、变量单位、显式约束和缺失信息风险。

## 1. 阶段身份

```yaml
stage_id: intake
stage_name: 赛题接收
stage_order: 1
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. 目标

在不求解问题的前提下，规范化赛题文本、附件清单、比赛元数据和缺失信息风险。算力集中在准确抽取题面事实、数据附件、变量单位、目标约束、交付物和评分暗示上，为 EDA 与任务拆解提供可靠入口。

## 3. 必需输入

```text
- workflow_state.yaml
- config/execution_policy.yaml
- 00_problem/inbox/
```

## 4. 可选输入

```text
- 03_data/raw/
- 人工补充的题面文本
- TASK_PACKET.md 中明确点名的相关文件
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 00_problem/
- 03_data/raw/
```

## 6. 允许写入路径

```text
- 00_problem/
- 01_task_analysis/
- 10_ai_logs/
```

## 7. 禁止动作

```text
- 不得求解问题或给出模型结论。
- 不得虚构附件内容。
- 不得跳过扫描版、损坏文件、缺失附件或 OCR 风险。
- 不得写入允许写入路径之外的位置。
- 不得把题面重述改写成带有解题假设的版本。
- 不得把历史论文或先验材料写入题面整理。
```

## 8. 必需输出

```text
- 00_problem/problem_statement.md
- 00_problem/attachments_overview.md
- 01_task_analysis/missing_information.md
- 题面事实清单：变量、单位、对象、时空范围、目标、约束、显式交付物
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
你正在执行 intake 阶段。

输入核验：
1. 检查 00_problem/inbox/ 与 03_data/raw/ 中的题面和附件。
2. 确认当前 workflow_state 允许执行 intake，且未跨过锁定阶段。
3. 只读写本文件列出的路径。

阶段目标：
整理题面、附件和缺失信息，不建模、不求解、不写结果。

深度分析：
1. 逐项提取题目对象、变量、单位、时间范围、空间范围、约束、目标函数暗示和交付要求。
2. 区分官方事实、附件事实、人工补充、无法确认信息和代理推测；推测不得进入题面事实。
3. 建立附件清单：文件名、类型、可读性、字段概览、是否需要 OCR、是否可能缺失。
4. 识别评分风险：题目问法不清、附件不全、单位口径不一致、数据来源不明、提交格式不明。
5. 为 task_analysis 留出问题编号候选，但不确定子问题边界时只写多种解释。

证据绑定：
所有题面事实必须能追溯到题面原文、附件或人工补充说明；缺少来源的内容写入 missing_information。

风险清单：
记录 OCR、附件缺失、字段含义不明、单位不明、比赛元数据缺失和题目解释歧义。

自检清单：
1. 未选择模型。
2. 未写任何结果或论文结论。
3. 未复制先验论文文本。
4. 未把不确定信息写成事实。
5. 校验命令已运行或记录 not_run。

人工确认输出：
请人类确认题面和附件清单是否完整，以及哪些歧义解释应保留。
```

## 12. 校验命令

```bash
python scripts/check_gates.py --dev-debug
```

## 13. 人工确认问题

```text
题面和附件清单是否完整，是否存在需要人工补录或澄清的官方要求？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 题面无法读取 | 记录 OCR 或文本缺失风险，并请求人工补录。 |
| 附件缺失 | 在缺失信息报告中列明，不得虚构。 |
| 格式无法识别 | 只登记文件与风险，等待人工处理。 |
| 题面解释冲突 | 保留多种解释并要求人工确认，不提前建模。 |
| 阶段锁不匹配 | 停止执行并报告当前 `current_stage`。 |

## 15. 完成条件

```text
- 题面和附件状态已记录。
- 变量、单位、对象、约束和交付要求已尽力抽取。
- 不确定信息已进入 missing_information。
- 未产生任何模型、结果或论文结论。
- 未触发本阶段禁止动作。
```

