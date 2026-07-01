# 全文组装后未解决问题清单（提交审稿前）

## 合同冲突
- **C06 claim_evidence_map 错位**：`citation_id` 字段误为“moderate”，需在修订阶段修正为 `citation_id=` 空，`support_grade=moderate`。
- **POL-000 polish_changed_protected_atom**：当前阻塞，需要 polish 阶段解决或人类豁免。

## 结果缺失
- Bootstrap 系数分布的具体数值未存入结果合同，仅在正文中定性提及。建议补充为独立的 `result_id`。

## 审稿风险
- 中文图表标签渲染未最终验证（RV-010）。
- 参考文献列表可能需要按目标期刊格式调整。

## 建议动作
1. 修订阶段优先修正 claim_evidence_map.csv C06。
2. 若可能，运行一次 `validate_contracts.py` 以刷新合同状态。
3. 在 `auto_review` 阶段关注上述问题的评论。
