# 未解决审稿问题清单

> 本文档汇总 paper_full 阶段识别出的、且当前尚未关闭的审稿与合同问题。

## 审稿评分问题

| 行 | 评审员 | 维度 | 得分/满分 | 严重性 | 状态 | 描述 |
|---|---|---|---|---|---|
| 2 | problem_reviewer | Problem Coverage | 3/10 | fail | open | Q2 和 Q3 解决方案缺失（已在 revision 中关闭 RV-001~RV-003 但从评分看可能未更新） |
| 7 | judge_reviewer | Overall Judgment | 3/10 | fail | open | 提交未满足核心要求 |

*注：多数与评分偏低相关的修订任务（RV-001~RV-008）已在 `14_contracts/revision_tasks.csv` 中标记为 closed，但 `review_scorecard.csv` 尚未重新评估。*  

## 合同验证问题

来自 `11_review/revision_tasks.csv` 中仍 `open` 的条目：

| 任务ID | 严重性 | 描述 | 需处理 |
|---|---|---|---|
| RV-007 | minor | 中文字体渲染风险 | 重新生成图像 |
| RV-008 | minor | 结论语言过于确定 | 弱化措辞 |

另，合约总体验证报告指出：
- 多项 `figure_contract` 中 `result_id` 指向未知结果（可能为历史遗留，因当前结果合同已包含所有 id）。
- `claim_evidence_map` 中存在未绑定引用（可能与 citation_id 有关）。
- `polish_diff_check.csv` 有 blocked 项。

## 论文特定缺口

1. **citation_contract.csv 缺失**：正文引用了 [1]–[4]，但合同目录中无对应文件。需创建。
2. **C03、C06 支持度较低**：应在结论中进一步保留，或提供补充统计检验。

## 建议行动

- 执行 `auto_review` 或直接运行合同验证脚本，获得最新 `review_scorecard` 和合同状态。
- 关闭所有 open 的 minor 任务，并更新合同以消除 figure_contract 中的幽灵引用。
- 创建 `citation_contract.csv` 并填入正式条目。
