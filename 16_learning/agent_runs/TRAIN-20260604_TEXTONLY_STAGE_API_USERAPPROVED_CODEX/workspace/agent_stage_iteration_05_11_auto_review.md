# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX\workspace`
Run dir: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX`
Call id: `iteration_05_11_auto_review`
Iteration: 5
Max iterations: 5
Current simulated stage: `auto_review`
Stage order: 11
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX/reports/prompt_route_manifest.md`
Training sandbox stage prompt bundle: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX/reports/stage_prompt_bundle.md`

Revision queue: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX\reports\agent_revision_queue.csv`

Open fail/major queue items:
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX-VAL-002: Expand 12_submission/final_submit_paper.md from the latest full_draft with substantive problem analysis, model, results, validation, and conclusion sections. | acceptance: final_submit_paper.md has at least 2500 characters and at least seven sections. | notes: validation_item=training_final_paper_too_thin
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX-VAL-003: Resolve validation failure training_claim_missing_figure_link: C01: F001 | acceptance: validate_agent_run.py no longer reports training_claim_missing_figure_link. | notes: validation_item=training_claim_missing_figure_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX-VAL-004: Resolve validation failure training_claim_missing_figure_link: C02: F004 | acceptance: validate_agent_run.py no longer reports training_claim_missing_figure_link. | notes: validation_item=training_claim_missing_figure_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX-VAL-005: Resolve validation failure training_claim_missing_figure_link: C04: F003 | acceptance: validate_agent_run.py no longer reports training_claim_missing_figure_link. | notes: validation_item=training_claim_missing_figure_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX-VAL-006: Resolve validation failure training_claim_missing_figure_link: C05: F002 | acceptance: validate_agent_run.py no longer reports training_claim_missing_figure_link. | notes: validation_item=training_claim_missing_figure_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX-VAL-007: Resolve validation failure training_claim_missing_figure_link: C07: F001 | acceptance: validate_agent_run.py no longer reports training_claim_missing_figure_link. | notes: validation_item=training_claim_missing_figure_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX-VAL-008: Resolve validation failure training_claim_missing_figure_link: C07: F002 | acceptance: validate_agent_run.py no longer reports training_claim_missing_figure_link. | notes: validation_item=training_claim_missing_figure_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX-VAL-009: Resolve validation failure training_claim_missing_figure_link: C07: F003 | acceptance: validate_agent_run.py no longer reports training_claim_missing_figure_link. | notes: validation_item=training_claim_missing_figure_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX-VAL-010: Resolve validation failure training_claim_missing_figure_link: C07: F004 | acceptance: validate_agent_run.py no longer reports training_claim_missing_figure_link. | notes: validation_item=training_claim_missing_figure_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX-VAL-011: Make paper figure references match figure_contract ids exactly and register each cited figure with an existing file. | acceptance: Every `图F###` paper reference has a matching figure_contract.csv row and existing output file. | notes: validation_item=training_paper_unregistered_figure_reference
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX-VAL-012: Make paper figure references match figure_contract ids exactly and register each cited figure with an existing file. | acceptance: Every `图F###` paper reference has a matching figure_contract.csv row and existing output file. | notes: validation_item=training_paper_unregistered_figure_reference
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX-VAL-013: Make paper figure references match figure_contract ids exactly and register each cited figure with an existing file. | acceptance: Every `图F###` paper reference has a matching figure_contract.csv row and existing output file. | notes: validation_item=training_paper_unregistered_figure_reference

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

