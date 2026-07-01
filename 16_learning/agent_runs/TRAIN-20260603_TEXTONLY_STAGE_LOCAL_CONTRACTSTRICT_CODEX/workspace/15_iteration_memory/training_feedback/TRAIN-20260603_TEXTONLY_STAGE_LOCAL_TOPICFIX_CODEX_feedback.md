# Training Sandbox Feedback Bundle

- generated_at: 2026-06-03T19:12:35
- status: suggestion_only
- source_run_id: TRAIN-20260603_TEXTONLY_STAGE_LOCAL_TOPICFIX_CODEX
- formal_stage: intake
- validation_status: pass
- copy_risk_decision: pass
- csv: 15_iteration_memory/training_feedback/TRAIN-20260603_TEXTONLY_STAGE_LOCAL_TOPICFIX_CODEX_feedback.csv

These rows are validated training-sandbox enhancement candidates. They are not formal facts and must pass the normal revision, contract, and human-gate controls before changing formal prompts or protected artifacts.

## Candidate Corrections

- [major] `workflow_gate:training_sandbox_candidate`
  - issue: validated training enhancement (gate): 训练完成门禁应同时检查三类增强点、可提交论文、提交包和核心合同非空，而不是只检查 gap report。
  - proposed_action: 训练完成门禁应同时检查三类增强点、可提交论文、提交包和核心合同非空，而不是只检查 gap report。
  - acceptance_check: validate_agent_run.py 对 training_enhancement_points.csv、final_submit_paper.md、final_submit_package.md 和核心合同给出 fail 级校验。
- [major] `formal_prompt:training_sandbox_candidate`
  - issue: validated training enhancement (prompt): 训练提示词应要求每个阶段输出目标重述、输入核验、合同绑定、风险清单、自检清单和人工闸门状态。
  - proposed_action: 训练提示词应要求每个阶段输出目标重述、输入核验、合同绑定、风险清单、自检清单和人工闸门状态。
  - acceptance_check: agent_prompt.md 包含 stage prompt route 和每阶段执行骨架要求。
- [major] `workflow:system`
  - issue: validated training enhancement (system): 训练模式应强制生成 prompt route manifest，并在 run 级验证中检查训练是否覆盖全部 16 个阶段提示词。
  - proposed_action: 训练模式应强制生成 prompt route manifest，并在 run 级验证中检查训练是否覆盖全部 16 个阶段提示词。
  - acceptance_check: validate_agent_run.py 对完成训练 run 检查 prompt_route_manifest.csv 行数不少于 16 且无 missing stage prompt。
- [minor] `formal_prompt:training_sandbox_candidate`
  - issue: validated training enhancement (prompt): figures 阶段提示词在训练模式中应要求图表选择说明绑定数据特征，不允许只生成装饰性图片。
  - proposed_action: figures 阶段提示词在训练模式中应要求图表选择说明绑定数据特征，不允许只生成装饰性图片。
  - acceptance_check: 训练论文图表说明段落引用 figure_contract.csv 中的 result_id 或 evidence_source。
