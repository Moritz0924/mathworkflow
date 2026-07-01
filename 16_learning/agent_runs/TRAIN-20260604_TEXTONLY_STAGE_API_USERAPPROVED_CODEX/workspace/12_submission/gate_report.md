# 最终提交门禁报告 (Final Submission Gate Report)

生成时间: 2025-06-04T10:20:00Z (simulated)
状态: BLOCKED (多个 FAIL 级问题)

## 1. 编译状态

| 检查项 | 结果 | 详情 |
|---|---|---|
| LaTeX 编译成功 | FAIL | 缺少 sections/ 下所有 .tex 文件，编译立即终止。 |
| 无重复 label | N/A | 无文件，无法检查。 |
| 所有引用可解析 | N/A | 同上。 |
| 图表文件存在 | FAIL | 08_figures/ 为空，未在 paper_draft 阶段创建图表。 |
| 无 TODO/占位文本 | N/A | 无法检查 sections 内容。 |

## 2. 合同一致性校验

| 合同文件 | 检查结果 | 备注 |
|---|---|---|
| claim_evidence_map.csv | NOT_FOUND | 未创建，paper_draft 未执行。 |
| result_contract.csv | NOT_FOUND | 未创建，results_freeze 未执行。 |
| figure_contract.csv | NOT_FOUND | 未创建，figures 未执行。 |
| formula_contract.csv | NOT_FOUND | 未创建。 |
| citation_contract.csv | NOT_FOUND | 未创建，literature 阶段未执行。 |
| polish_diff_check.csv | NOT_FOUND | 未创建，polish 未执行。 |
| revision_tasks.csv | NOT_FOUND | 未创建，revision 未执行。 |
| artifact_freeze_registry.csv | NOT_FOUND | 未创建，final_export 未执行。 |

## 3. 修订任务状态

- 未关闭的 fail/major 修订任务: 未知（revision_tasks.csv 缺失）。
- 需要返回 revision 阶段。

## 4. 语言与格式检查

| 检查项 | 结果 | 备注 |
|---|---|---|
| 正文是否为英文/目标语言 | N/A | 无法检查。 |
| 图表题注是否为中文 | N/A | 无法检查。 |
| 提交格式符合要求 | N/A | 无提交格式说明。 |

## 5. 人工确认

- 人工最终确认: 未开始 (final_submission_gate blocked)。

## 6. 恢复路径

所有 FAIL 级问题需按顺序返回上游阶段：
1. **paper_draft** – 生成所有 sections 文件、claim_evidence_map.csv、citation_contract.csv、formula_contract.csv。
2. **figures** – 创建 figure_contract.csv 及所有图表文件（在 paper_draft 之后或与之协调）。
3. **results_freeze** – 冻结数值结果并写入 result_contract.csv。
4. **revision** – 解决所有 fail/major 审稿意见，关闭修订任务。
5. **polish** – 语言润色并通过 polish_diff_check.csv 验证。
6. **compile** – 重新运行本阶段。

只有当上述阶段全部通过且人工闸门确认后，才可进入 final_export。
