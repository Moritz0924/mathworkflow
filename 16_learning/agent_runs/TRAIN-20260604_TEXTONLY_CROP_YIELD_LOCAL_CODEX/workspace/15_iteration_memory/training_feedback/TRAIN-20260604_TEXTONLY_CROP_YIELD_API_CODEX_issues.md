# TRAIN-20260604_TEXTONLY_CROP_YIELD_API_CODEX 运行问题记录

## 运行概况

- 赛题文件：`00_problem/inbox/text_only_crop_yield_problem.md`
- 运行模式：`training_sandbox`
- 最大迭代：`3`
- run_id：`TRAIN-20260604_TEXTONLY_CROP_YIELD_API_CODEX`
- 运行时间：`2026-06-04T21:11:55`
- 最终状态：`agent_failed`
- run 目录：`16_learning/agent_runs/TRAIN-20260604_TEXTONLY_CROP_YIELD_API_CODEX/`

## 根因问题

1. 首个阶段 `initial_00_latex_template` 未能完成。
   - 记录位置：`16_learning/agent_runs/TRAIN-20260604_TEXTONLY_CROP_YIELD_API_CODEX/reports/stage_execution_manifest.csv`
   - exit_code：`2`
   - failure_code：`DEEPSEEK_AGENT_ERROR`
   - 失败信息：DeepSeek request failed，Windows socket 权限拒绝，`WinError 10013`。
   - 影响：训练没有进入完整 16 阶段顺序执行，后续产物缺失主要是该失败的连锁结果。

2. 外部 API 提权重试未获批准。
   - 重试 run_id：`TRAIN-20260604_TEXTONLY_CROP_YIELD_API_CODEX_NETRETRY`
   - 审核结果：拒绝。
   - 拒绝原因：需要用户明确批准将沙盒赛题、提示和可能的 workspace 上下文发送到外部 API。
   - 影响：本轮无法在当前权限条件下完成真实 API 沙盒训练。

## 验证器暴露的问题

以下问题来自 `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_CROP_YIELD_API_CODEX/reports/agent_run_validation.md`：

- `missing_copy_risk_report`：缺少 copy risk 报告。
- `stage_execution_incomplete`：验证器报告初始阶段调用不足；实际 manifest 中存在 1 个失败阶段调用，说明验证口径可能没有把失败阶段计入有效调用。
- `missing_training_enhancement_points`：缺少训练改进建议 CSV。
- `missing_training_enhancement_markdown`：缺少训练改进建议 Markdown。
- `missing_submit_ready_training_artifact`：缺少 `final_submit_paper.md`。
- `training_contract_empty`：`result_contract.csv` 为空。
- `training_contract_empty`：`claim_evidence_map.csv` 为空。
- `training_contract_empty`：`figure_contract.csv` 为空。
- `open_blocking_revision_queue`：论文结构不足。
- `open_blocking_revision_queue`：缺少结果绑定图表与图表合同登记。
- `open_blocking_revision_queue`：缺少与模型输出绑定的验证、敏感性或稳健性分析。
- `open_blocking_revision_queue`：未填充 `result_contract` 和 `claim_evidence_map`。
- `training_simulated_gate_log_incomplete`：缺少模拟人工闸门日志。
- `training_review_scorecard_missing`：缺少审稿评分表。

## 建议处理

- 若要完成 API 训练，需要人工明确批准外部 API 数据传输范围：沙盒赛题、阶段提示、run 上下文和必要的工作区片段。
- 若不批准外部 API，应切换或配置一个本地执行器，并保持 `deep_sequential` 阶段顺序。
- 建议修正验证器提示：当 `stage_execution_manifest.csv` 中有失败阶段调用时，`stage_execution_incomplete` 的 detail 应区分 `0 calls`、`failed calls` 与 `completed calls`，避免误判为完全未启动。
