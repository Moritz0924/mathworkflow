# 缺失证据报告 — paper_draft 启动受阻

## 原因
paper_draft 阶段要求以下合同已存在且填充完毕：
- 14_contracts/claim_evidence_map.csv
- 14_contracts/result_contract.csv
- 14_contracts/figure_contract.csv
- 14_contracts/formula_contract.csv
- 14_contracts/citation_contract.csv

当前工作流状态显示所有前置阶段 (intake 至 figures) 均为 locked，以上合同均不存在。

## 影响
无法为任何章节构建基于证据的论证链。无合同即无合法来源的数字、图表、公式或引用，因此不允许生成任何章节草稿。

## 建议
依次完成前置阶段并填充对应合同后，再重新触发 paper_draft。
