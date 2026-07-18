# 数学建模双 AI 正式工作流 v4 代理规则

本仓库使用 8 阶段、文件交接、合同驱动的正式流水线。ChatGPT 网页端负责建模决策与论文表达；Codex 负责本地事实、代码复现与数值核验；控制器独占状态推进权。

## 权威顺序

1. 人工闸门与比赛规则
2. v4 控制器和 `workflow_state.yaml`
3. 本地数据、可复现代码输出与合同总线
4. 已导入的 ChatGPT 阶段决策
5. Codex 实现与核验意见
6. 可选文献和 Prior DB 参考

发生冲突时服从更高层级。Codex 可以修复实现问题；涉及模型假设、路线、口径或结论的冲突必须记录并退回 ChatGPT，不得静默改写。

## 硬性约束

- 只能按 `intake → data_analysis → model_design → implementation → result_freeze → evidence_design → paper_review → finalize` 顺序推进。
- 只有 `scripts/workflow.py` 经状态机校验后可以推进状态；前端不得直接写状态。
- 任何 AI 都不得确认人工闸门，也不得伪造人工确认记录。
- 不直接调用任何模型 API；ChatGPT 与 Codex 只通过结构化文件交接。
- 没有真实代码输出和 `result_contract.csv` 条目时，不得写结果分析。
- 图未登记到 `figure_contract.csv` 或文件不存在时，不得在论文中引用。
- 未登记的论断、公式和引用不得进入论文。
- 润色不得改变数字、公式、标签、引用、文献、模型名或结果含义。
- 不得复制历史论文的摘要、正文、图注、表格或结论。
- 审稿意见只能写入审稿/修订工件，不得直接篡改冻结的正式产物。

## 双 AI 边界

| 主体 | 负责 | 不得做 |
|---|---|---|
| ChatGPT | 问题拆解、建模决策、公式与假设、解释、证据叙事、论文与修订建议 | 声称运行了本地代码、虚构数据/结果、推进状态或确认闸门 |
| Codex | 数据检查、代码实现、从零运行、数值/来源/合同核验、实现缺陷修复 | 静默改变模型路线、假设或结论，代替人工确认 |
| 控制器 | 哈希、状态转换、交接不可变性、阶段验收、闸门锁定 | 替任一 AI 做建模决策 |

## 交接协议

每次交接写入 `10_ai_logs/handoffs/<handoff_id>/`：

```text
manifest.yaml
chatgpt_prompt.md
chatgpt_response.md
codex_task.md
codex_receipt.json
```

ChatGPT 回复必须携带与清单完全一致的 `protocol`、`project_id`、`stage`、`handoff_id`、`context_sha256`。原始回复和 Codex 回执不可覆盖；旧哈希、重复回复、错阶段、合同缺失或验证冲突必须阻止推进。

## 阶段与闸门

| 阶段 | 责任重点 | 人工闸门 |
|---|---|---|
| `intake` | 题面、附件、指纹和敏感信息检查 | — |
| `data_analysis` | 数据质量、EDA 与问题拆解复现 | — |
| `model_design` | 模型、公式、假设、备选方案与可实现性 | `model_freeze_gate` |
| `implementation` | 正式代码、依赖、测试与从零运行 | — |
| `result_freeze` | 数值、敏感性、稳定性及来源核验 | `result_freeze_gate` |
| `evidence_design` | 图表、表格、论断与论文提纲绑定 | `evidence_gate` |
| `paper_review` | 草稿、审稿、修订和全局一致性 | `paper_gate` |
| `finalize` | PDF、提交包、视觉与合同总检 | `final_submission_gate` |

## 合同总线

正式内容必须记录在：

- `14_contracts/result_contract.csv`
- `14_contracts/figure_contract.csv`
- `14_contracts/formula_contract.csv`
- `14_contracts/claim_evidence_map.csv`
- `14_contracts/citation_contract.csv`
- `14_contracts/artifact_freeze_registry.csv`
- `14_contracts/polish_diff_check.csv`
- `14_contracts/revision_tasks.csv`

## 旧提示词保护

`prompts/stages/*.md` 与 `prompts/stage_prompt_contract.md` 是只读历史资产：禁止删除、重命名、修改或覆盖。新提示词只能写入 `prompts/formal_v4/`。变更前后必须运行旧提示词哈希测试。

## 可选证据边界

`02_literature/` 和 `13_prior_db/` 可以提供经验与文献线索，但不参与状态推进，不提供当前题目的事实答案。引用必须重新核验并登记；历史文本不得复用。

## 最终交付

形成最终提交前必须同时满足：

- `scripts/check_gates.py` 通过；
- `scripts/validate_contracts.py --stage current` 通过；
- `11_review/review_scorecard.csv` 没有未关闭的 fail/major 问题；
- 所有必需修订已关闭或由人类明确豁免；
- `final_submission_gate` 已由人类确认。
