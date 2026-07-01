# final_export 阶段阻塞器

- 阻塞时间：2026-06-03 初始调用
- 原因：最终人工闸门未确认，不存在已批准的最终论文包
- 缺失输入：
  - 已人工确认的最终论文包（09_paper/full_draft.md 等）
  - 11_review/final_submission_checklist.md
  - 14_contracts/ 全部合同校验通过（当前状态未知）
- 当前阶段无法继续，需要上游阶段完成后人工确认闸门。
- 建议：恢复 intake → task_analysis → … → compile 流程，确保所有合同校验通过，人工闸门确认后再执行 final_export。
