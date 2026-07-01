# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_API_RETRY_CODEX\workspace`
Run dir: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_API_RETRY_CODEX`
Call id: `iteration_02_11_auto_review`
Iteration: 2
Max iterations: 3
Current simulated stage: `auto_review`
Stage order: 11
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_API_RETRY_CODEX/reports/prompt_route_manifest.md`
Training sandbox stage prompt bundle: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_API_RETRY_CODEX/reports/stage_prompt_bundle.md`

Revision queue: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_API_RETRY_CODEX\reports\agent_revision_queue.csv`

Open fail/major queue items:
- [major] TRAIN-20260603_TEXTONLY_STAGE_API_RETRY_CODEX-TASK-001: Add validation, sensitivity, robustness, or error analysis tied to model outputs. | acceptance: Validation section cites frozen result rows or reproducible code outputs. | notes: from TRAIN-20260603_TEXTONLY_STAGE_API_RETRY_CODEX-GAP-003
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_RETRY_CODEX-VAL-001: Create reports/training_enhancement_points.csv with at least system, prompt, and gate target_area rows. | acceptance: training_enhancement_points.csv exists and contains system/prompt/gate rows. | notes: validation_item=missing_training_enhancement_points
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_RETRY_CODEX-VAL-002: Create reports/training_enhancement_points.md summarizing candidate workflow improvements. | acceptance: training_enhancement_points.md is non-empty. | notes: validation_item=missing_training_enhancement_markdown
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_RETRY_CODEX-VAL-003: Resolve validation failure training_final_paper_too_thin: chars=1490, sections=6 | acceptance: validate_agent_run.py no longer reports training_final_paper_too_thin. | notes: validation_item=training_final_paper_too_thin
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_RETRY_CODEX-VAL-004: Resolve validation failure training_final_paper_missing_section_signal: 问题分析 | acceptance: validate_agent_run.py no longer reports training_final_paper_missing_section_signal. | notes: validation_item=training_final_paper_missing_section_signal
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_RETRY_CODEX-VAL-005: Resolve validation failure training_claim_missing_result_link: UPSTREAM_MISSING: NA | acceptance: validate_agent_run.py no longer reports training_claim_missing_result_link. | notes: validation_item=training_claim_missing_result_link
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_RETRY_CODEX-VAL-006: Resolve validation failure training_claim_missing_figure_link: UPSTREAM_MISSING: NA | acceptance: validate_agent_run.py no longer reports training_claim_missing_figure_link. | notes: validation_item=training_claim_missing_figure_link
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_RETRY_CODEX-VAL-007: Resolve validation failure training_claim_missing_formula_link: UPSTREAM_MISSING: NA | acceptance: validate_agent_run.py no longer reports training_claim_missing_formula_link. | notes: validation_item=training_claim_missing_formula_link

Rules:
- Follow only deep_sequential behavior for this stage.
- Do not edit `00_problem/problem_statement.md` or `00_problem/inbox/`; write intake analysis to `01_task_analysis/`.
- A formal human gate becomes a simulated sandbox gate. Record it in `11_review/simulated_human_gate_log.csv`.
- Update contracts before writing paper claims, result analysis, figures, or submission text.
- Reply only through runner file actions. The external runner will reject prose-only or pseudo-tool responses.

Stage output target:
- Create or update the artifacts normally owned by `auto_review`.
- If this stage cannot close a blocker, update review/revision artifacts with a concrete blocker note.
- Keep `reports/training_enhancement_points.csv` current once a full draft or review finding exists.

Stage-specific required outputs:
- Write `11_review/review_scorecard.csv` and `14_contracts/revision_tasks.csv`.
- Write `11_review/simulated_human_gate_log.csv` with columns stage_id, gate_id, agent_decision, evidence, residual_risk, formal_effect.
- Every simulated gate row must set formal_effect to `none`; never use confirmed/approved as a formal workflow effect.

