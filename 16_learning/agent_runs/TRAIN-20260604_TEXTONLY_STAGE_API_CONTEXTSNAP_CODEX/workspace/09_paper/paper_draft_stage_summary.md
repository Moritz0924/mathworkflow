# paper_draft 阶段总结

## 生成章节
- `09_paper/draft_sec_q1_model.md`：问题一的模型建立与求解草案。

## 合同更新
- `14_contracts/claim_evidence_map.csv`：新增 6 条论断记录，涵盖模型拟合、通道系数解释、残差诊断等。
- `14_contracts/citation_contract.csv`：初始化空表头（仍缺失实际引用条目）。

## 缺失证据
- 见 `09_paper/missing_evidence_report.md`：缺少显著性检验（p 值、置信区间、VIF）、预测区间、部分诊断图、引用文献。

## 人工闸门
- 模拟闸门已记录到 `11_review/simulated_human_gate_log.csv`。

## 风险与待办
- 草稿中关于 B 通道方向性的光学解释缺乏文献支撑，若不能补充引用，应考虑降级为纯数据相关陈述。
- 缺少多重共线性量化指标，可能影响因果关系论断，建议返回代码阶段生成 VIF 并登记结果合同。
- 后续章节（问题二、三）需基于 result_contract 补充模型比较结果和预测值。
