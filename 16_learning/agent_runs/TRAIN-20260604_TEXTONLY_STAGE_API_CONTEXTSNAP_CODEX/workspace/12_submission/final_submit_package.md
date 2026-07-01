# 最终提交包说明

## 包含产物

- **论文终稿**：`12_submission/final_submit_paper.md`，来源于 `09_paper/full_draft.md`，经过语言润色，保留全部数值、图表引用和模型结果。
- **代码包**：`06_code/` 下的 Python 脚本及 README，涵盖线性回归、多项式回归、岭回归、交叉验证、预测和图表生成。
- **数据包**：`07_results/` 下的所有结果文件（系数、预测值、交叉验证结果等），与 `14_contracts/result_contract.csv` 一致。
- **图表包**：`08_figures/main_figures/` 下的 SVG 图表，包含系数条形图、预测对比、残差诊断、相关系数热力图、模型对比、预测区间等，并与 `14_contracts/figure_contract.csv` 对应。
- **合同文件**：`14_contracts/` 下的所有合同，包括 `claim_evidence_map.csv`、`result_contract.csv`、`figure_contract.csv`、`formula_contract.csv`、`citation_contract.csv`、`revision_tasks.csv` 和 `artifact_freeze_registry.csv`。所有 fail 级别问题已通过修复或豁免关闭。
- **审稿与修订记录**：`11_review/` 下的审稿意见、评分卡（第4轮全部通过）、修订任务记录，以及模拟人工闸门日志。
- **AI 使用说明**：`12_submission/ai_usage_detail.pdf`。
- **最终提交清单**：`11_review/final_submission_checklist.md`。

## 质量确认

- 最终人工闸门已模拟并记录于 `11_review/simulated_human_gate_log.csv`，所有条目的 `formal_effect` 设为 `none`，满足沙盒要求。
- 合同校验证脚本已运行，无 fail 级别问题（训练沙盒中少数条目以豁免方式关闭，详见 `14_contracts/revision_tasks.csv`）。
- 所有图表文件存在并已冻结，图中文字均为中文（必要的英文缩写、变量名、文件名和指标名除外）。
- 论文终稿完全保留题目核心元素：T01、T02、T03 样本，RGB 通道，浓度范围等，未替换为通用内容。
- 每一数值论断均绑定到 `result_contract.csv` 条目，图表引用绑定到 `figure_contract.csv`。

## 遗留风险

1. **小样本局限**：标准样本仅 10 个，统计诊断效力有限，外推到浓度范围（<0.5 或 >5.0 mg/L）之外风险较高。
2. **模型假设**：线性关系在当前数据上成立，但不适用于其他检测设备、不同物质或更宽浓度范围的比色场景。
3. **预测不确定性**：95% 预测区间宽度约 0.52 mg/L，实际应用中若需更高精度，建议增加标定点或进行重复测量。
4. **沙盒环境限制**：部分 minor 级问题（如中文 SVG 字体渲染验证）仅在逻辑上通过，未在目标 viewer 中实测，存在排版风险。

## 合规声明

本提交包未复制任何历史论文的文本、摘要、图注、表格或结论。所有内容均为本次题目“颜色与物质浓度的辨识问题”的独立建模和分析产物，符合工作流防抄袭规则。