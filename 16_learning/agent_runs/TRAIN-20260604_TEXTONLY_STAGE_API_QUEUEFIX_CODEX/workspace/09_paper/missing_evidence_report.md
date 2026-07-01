# 缺失证据报告 — paper_full 阶段

本报告列出 full_draft.md 中所有需要实证支撑的论断及其证据状态。

| 章节 | 论断 | 所需证据 | 当前状态 | 建议行动 |
|------|------|----------|----------|----------|
| 3.1 | "T01 R²=0.97" 等 | result_contract 中注册的指标值 | 缺失：result_contract 无对应条目 | 运行代码生成结果并冻结，登记到 result_contract.csv |
| 3.1 | "图 F001 展示散点图" | figure_contract 行 + 图文件 | 缺失：figure_contract 未注册该图，文件不存在 | 在 figures 阶段生成预测 vs 实际图，登记合同 |
| 3.2 | "LOOCV RMSE: T01=0.15" | 交叉验证结果 | 缺失 | 同上 |
| 3.3 | "残差诊断图 F003-F006" | 图形文件 | 缺失 | 创建残差图和 Q-Q 图 |
| 4.2 | "噪声敏感性图 F007" | 敏感性分析结果及图形 | 缺失 | 执行噪声扰动模拟并绘图 |
| 公式 (1)-(4) | Beer-Lambert、OLS 等 | formula_contract 登记 | 缺失 | 在 model_route 阶段补充 formula_contract |
| 全文 | 所有强度论断 | claim_evidence_map 绑定 | 缺失 | 补充 claim_evidence_map |

**结论:** 当前全文草稿为结构骨架，需等待上游阶段（model_route、codegen、results_freeze、figures）产出实证数据后，方可成为可提交论文。
