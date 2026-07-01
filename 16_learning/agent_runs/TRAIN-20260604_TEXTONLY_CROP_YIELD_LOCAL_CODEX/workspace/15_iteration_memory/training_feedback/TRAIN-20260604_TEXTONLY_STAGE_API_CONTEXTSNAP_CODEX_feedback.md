# Training Sandbox Feedback Bundle

- generated_at: 2026-06-04T07:03:35
- status: suggestion_only
- source_run_id: TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX
- formal_stage: intake
- validation_status: pass
- copy_risk_decision: pass
- csv: 15_iteration_memory/training_feedback/TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX_feedback.csv

These rows are validated training-sandbox enhancement candidates. They are not formal facts and must pass the normal revision, contract, and human-gate controls before changing formal prompts or protected artifacts.

## Candidate Corrections

- [major] `formal_prompt:training_sandbox_candidate`
  - issue: validated training enhancement (prompt): 沙盒训练发现该要求容易遗漏，可做成可执行检查项
  - proposed_action: 在 final_export 阶段增加对“所有可见文字为中文”的硬性检查步骤，并输出检查报告
  - acceptance_check: Human gate, contract validation, and stage-state control approve this suggestion before formal adoption.
- [major] `workflow:system`
  - issue: validated training enhancement (system): 减少后期修复工作量；增强合同一致性
  - proposed_action: 增加合同校验脚本对 figure_contract 中单行多 result_id 的严格检查，当前已由人工修复但自动化规则可前置
  - acceptance_check: Human gate, contract validation, and stage-state control approve this suggestion before formal adoption.
- [minor] `workflow_gate:training_sandbox_candidate`
  - issue: validated training enhancement (gate): 目前手工填写 formal_effect=none，但未强制包含中文检查，可扩展到闸门问题
  - proposed_action: 模拟人工闸门日志应包含对最终导出产物中文合规的确认项
  - acceptance_check: Human gate, contract validation, and stage-state control approve this suggestion before formal adoption.
- [minor] `formal_prompt:training_sandbox_candidate`
  - issue: validated training enhancement (prompt): 当前提示词虽提及可选但未详细说明内容禁止新增事实，可细化
  - proposed_action: final_export 阶段提示词中明确 PPT 生成条件与内容边界，避免过度生成
  - acceptance_check: Human gate, contract validation, and stage-state control approve this suggestion before formal adoption.
- [minor] `workflow:system`
  - issue: validated training enhancement (system): 当前 sandbox 无法验证字体渲染，可能影响实际排版
  - proposed_action: 集成 MCP 视觉反馈以验证图表中文字体渲染效果，避免仅依赖 meta 数据
  - acceptance_check: Human gate, contract validation, and stage-state control approve this suggestion before formal adoption.
