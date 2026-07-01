# paper_draft 阶段缺失证据报告

**日期**: 2026-06-03
**阶段**: paper_draft
**状态**: 阻塞

## 问题描述

paper_draft 阶段要求存在以下合同文件才能生成章节草稿，但这些文件均未就绪：

- `14_contracts/claim_evidence_map.csv`（论断证据映射）
- `14_contracts/result_contract.csv`（结果合同）
- `14_contracts/figure_contract.csv`（图表合同）
- `14_contracts/formula_contract.csv`（公式合同）
- `14_contracts/citation_contract.csv`（引用合同）

由于前置阶段 `results_freeze`、`figures`、`model_route`、`prior_retrieval` 均为 locked 状态，上述合同尚未生成。没有合同支持的论断、结果、图表、公式和引用，paper_draft 无法满足“证据绑定”要求，亦无法保证章节正文可追踪。

## 缺失项清单

| 缺失项 | 描述 | 影响 |
|---|---|---|
| claim_evidence_map.csv | 所有正式论断及其证据链 | 无法建立章节论证链 |
| result_contract.csv | 所有数值结果 | 无法引用任何定量结论 |
| figure_contract.csv | 图表登记 | 无法插入或引用任何图表 |
| formula_contract.csv | 符号定义与公式 | 无法使用数学表达式 |
| citation_contract.csv | 核验后的引用 | 无法提供背景支撑 |

## 恢复建议

1. 按工作流顺序完成 `intake`、`task_analysis`、`prior_retrieval`、`model_route`、`codegen`、`results_freeze`、`figures` 等阶段，生成所需合同。
2. 合同生成后重新进入 `paper_draft`。

## 临时措施

本阶段未生成任何正文，仅记录缺失状态。
