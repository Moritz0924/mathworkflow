# 阶段提示词：`paper_full` - 全文组装

> 中文注释：使用阶段为 `paper_full`；使用场景是在分章节草稿完成后，组装全文并检查跨章节一致性、证据缺口和最终审稿入口。

## 1. 阶段身份

```yaml
stage_id: paper_full
stage_name: 全文组装
stage_order: 10
gate_type: hard
execution_mode: deep_sequential
roadmap_item: P5
```

## 2. 目标

将分章节草稿组装成连贯全文，但不得新增事实或掩盖证据缺口。算力集中在跨章节逻辑、术语一致性、结果一致性、图表/公式/引用一致性、缺口显式暴露和审稿准备上。

## 3. 必需输入

```text
- 02_latex_template/sections/
- 09_paper/missing_evidence_report.md（如存在）
- 14_contracts/claim_evidence_map.csv
```

## 4. 可选输入

```text
- 09_paper/section_generation_plan.csv
- 11_review/阶段总结
- 人工全文结构意见
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 02_latex_template/
- 09_paper/
- 14_contracts/
- 11_review/
```

## 6. 允许写入路径

```text
- 02_latex_template/sections/
- 09_paper/
- 14_contracts/artifact_freeze_registry.csv
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 不得新增未经合同支撑的事实。
- 不得隐藏缺失证据。
- 不得改变冻结结果含义。
- 不得跳过草稿审阅闸门。
- 不得将中文论文组装成英文正文或混入英文段落；必要的英文缩写、变量名、模型名和 LaTeX 命令除外。
- 不得为了连贯性改写数字、公式、图表标签或引用。
- 不得复制历史论文结构性段落或结论。
```

## 8. 必需输出

```text
- 全文草稿或组装记录
- 全文一致性风险说明
- 需要审稿的问题清单
- 图表/表格/公式/引用一致性检查说明
- 阶段总结和人工闸门说明
- 全文草稿必须为中文；图题、表题、图注、表注和所有面向评审的说明必须为中文。
```

## 9. 合同更新

```text
可更新：artifact_freeze_registry.csv（如冻结全文候选）
只读：其他合同
```

## 10. 允许技能

```text
- nature-writing（如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 paper_full 阶段。

输入核验：
1. 检查各章节草稿、missing_evidence_report 和 claim_evidence_map。
2. 检查 result、figure、formula、citation 合同是否支持全文引用。
3. 若需要参考先验资产，只能使用上游已写入允许路径的摘要；不得直接读取未授权路径。

阶段目标：
整合章节、检查前后逻辑和引用一致性。不得添加新事实；未解决缺口必须单独列出。

深度分析：
1. 检查全文主线：问题提出、模型建立、求解、结果、分析、优缺点和结论是否形成闭环。
2. 检查术语一致性：子问题编号、模型名、变量名、指标名、单位和章节标题。
3. 检查冻结数字一致性：正文、表格、图注和结论不得出现不同版本数值。
4. 检查图表密度和位置：核心结果附近应有相应图/表/公式支撑；不充分时列为审稿前缺口。
5. 检查所有图表引用是否有 latex_label 且在 figure_contract 中登记。
6. 检查公式符号是否定义，引用是否验证，弱证据是否被写成强结论。
7. 只做结构衔接和一致性调整；任何事实新增都应回到 paper_draft 或上游合同阶段。

证据绑定：
全文中的强论断必须可追踪到 claim_evidence_map；全文候选冻结时登记 artifact_freeze_registry 并记录 protected_atoms。

风险清单：
记录章节矛盾、证据缺口、图表不足、标签冲突、引用未核验、结论过强、中文排版和人工闸门风险。

自检清单：
1. 未新增事实。
2. 未隐藏缺口。
3. 未改变冻结结果。
4. 全文和图表说明为中文。
5. 未解决问题已单独列出。
6. 校验命令已运行或记录 not_run。

人工确认输出：
请人类批准这版全文草稿提交审稿，并确认未解决缺口单独列出。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage paper_full
```

```bash
python scripts/check_gates.py
```

## 13. 人工确认问题

```text
是否批准将这版全文草稿提交审稿，并把未解决缺口单独列出？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 章节矛盾 | 返回相关章节修订，不强行润色。 |
| 证据缺口 | 写入缺口清单，等待补证或删除论断。 |
| 图表引用不一致 | 返回 figures 或合同修正。 |
| 数值不一致 | 返回 results_freeze 或相关章节修正。 |
| 人工未确认 | 停在 `draft_review_gate`。 |

## 15. 完成条件

```text
- 全文草稿可审阅。
- 未解决问题已单独列出。
- 全文强论断可追踪到合同。
- 进入 auto_review 前已满足闸门状态。
- 全文和图表说明已检查为中文。
- 未触发本阶段禁止动作。
```
