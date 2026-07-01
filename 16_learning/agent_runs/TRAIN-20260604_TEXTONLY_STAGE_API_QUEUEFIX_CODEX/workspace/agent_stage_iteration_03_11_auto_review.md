# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX\workspace`
Run dir: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX`
Call id: `iteration_03_11_auto_review`
Iteration: 3
Max iterations: 5
Current simulated stage: `auto_review`
Stage order: 11
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX/reports/prompt_route_manifest.md`
Training sandbox stage prompt bundle: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX/reports/stage_prompt_bundle.md`

Revision queue: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX\reports\agent_revision_queue.csv`

Open fail/major queue items:
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-002: Refresh final_submit_paper.md from a topic-aligned full_draft and include the missing required section signal. | acceptance: validate_agent_run.py no longer reports training_final_paper_missing_section_signal. | notes: validation_item=training_final_paper_missing_section_signal
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-003: Add result_id or evidence_source for every figure_contract row and keep the cited figure file path registered. | acceptance: Every figure_contract row has result_id or evidence_source and an existing output path. | notes: validation_item=training_figure_contract_missing_evidence_source
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-004: Create the figure files referenced by figure_contract.csv or update the contract to existing files. | acceptance: All registered figure outputs exist in the sandbox workspace. | notes: validation_item=training_figure_contract_file_missing
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-005: Add result_id or evidence_source for every figure_contract row and keep the cited figure file path registered. | acceptance: Every figure_contract row has result_id or evidence_source and an existing output path. | notes: validation_item=training_figure_contract_missing_evidence_source
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-006: Create the figure files referenced by figure_contract.csv or update the contract to existing files. | acceptance: All registered figure outputs exist in the sandbox workspace. | notes: validation_item=training_figure_contract_file_missing
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-007: Add result_id or evidence_source for every figure_contract row and keep the cited figure file path registered. | acceptance: Every figure_contract row has result_id or evidence_source and an existing output path. | notes: validation_item=training_figure_contract_missing_evidence_source
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-008: Create the figure files referenced by figure_contract.csv or update the contract to existing files. | acceptance: All registered figure outputs exist in the sandbox workspace. | notes: validation_item=training_figure_contract_file_missing
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-009: Add result_id or evidence_source for every figure_contract row and keep the cited figure file path registered. | acceptance: Every figure_contract row has result_id or evidence_source and an existing output path. | notes: validation_item=training_figure_contract_missing_evidence_source
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-010: Create the figure files referenced by figure_contract.csv or update the contract to existing files. | acceptance: All registered figure outputs exist in the sandbox workspace. | notes: validation_item=training_figure_contract_file_missing
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-011: Make paper figure references match figure_contract ids exactly and register each cited figure with an existing file. | acceptance: Every `图F###` paper reference has a matching figure_contract.csv row and existing output file. | notes: validation_item=training_paper_unregistered_figure_reference
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-012: Make paper figure references match figure_contract ids exactly and register each cited figure with an existing file. | acceptance: Every `图F###` paper reference has a matching figure_contract.csv row and existing output file. | notes: validation_item=training_paper_unregistered_figure_reference
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-013: Make paper figure references match figure_contract ids exactly and register each cited figure with an existing file. | acceptance: Every `图F###` paper reference has a matching figure_contract.csv row and existing output file. | notes: validation_item=training_paper_unregistered_figure_reference

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
- Write current `11_review/review_scorecard.csv` and `14_contracts/revision_tasks.csv`; do not leave stale fail rows from earlier missing artifacts.
- Review scorecard rows should use score/max_score and must be at least 85% after the sandbox artifacts are fixed; on a 10-point scale use 9 or 10 for pass, otherwise keep the item as an open blocker.
- Write `11_review/simulated_human_gate_log.csv` with columns stage_id, gate_id, agent_decision, evidence, residual_risk, formal_effect.
- Every simulated gate row must set formal_effect to `none`; never use confirmed/approved as a formal workflow effect.

