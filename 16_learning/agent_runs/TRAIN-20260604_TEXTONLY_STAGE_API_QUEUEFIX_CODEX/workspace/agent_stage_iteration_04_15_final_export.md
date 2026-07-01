# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX\workspace`
Run dir: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX`
Call id: `iteration_04_15_final_export`
Iteration: 4
Max iterations: 5
Current simulated stage: `final_export`
Stage order: 15
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX/reports/prompt_route_manifest.md`
Training sandbox stage prompt bundle: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX/reports/stage_prompt_bundle.md`

Revision queue: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX\reports\agent_revision_queue.csv`

Open fail/major queue items:
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-002: Make paper figure references match figure_contract ids exactly and register each cited figure with an existing file. | acceptance: Every `图F###` paper reference has a matching figure_contract.csv row and existing output file. | notes: validation_item=training_paper_unregistered_figure_reference
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-003: Make paper figure references match figure_contract ids exactly and register each cited figure with an existing file. | acceptance: Every `图F###` paper reference has a matching figure_contract.csv row and existing output file. | notes: validation_item=training_paper_unregistered_figure_reference
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-004: Make paper figure references match figure_contract ids exactly and register each cited figure with an existing file. | acceptance: Every `图F###` paper reference has a matching figure_contract.csv row and existing output file. | notes: validation_item=training_paper_unregistered_figure_reference
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-005: Rewrite simulated gate log rows so formal_effect is exactly none. | acceptance: Every simulated gate row has formal_effect=none. | notes: validation_item=training_simulated_gate_has_formal_effect
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-006: Rewrite simulated gate log rows so formal_effect is exactly none. | acceptance: Every simulated gate row has formal_effect=none. | notes: validation_item=training_simulated_gate_has_formal_effect
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-007: Rewrite simulated gate log rows so formal_effect is exactly none. | acceptance: Every simulated gate row has formal_effect=none. | notes: validation_item=training_simulated_gate_has_formal_effect
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-008: Rewrite simulated gate log rows so formal_effect is exactly none. | acceptance: Every simulated gate row has formal_effect=none. | notes: validation_item=training_simulated_gate_has_formal_effect
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-009: Rewrite simulated gate log rows so formal_effect is exactly none. | acceptance: Every simulated gate row has formal_effect=none. | notes: validation_item=training_simulated_gate_has_formal_effect
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-010: Rewrite simulated gate log rows so formal_effect is exactly none. | acceptance: Every simulated gate row has formal_effect=none. | notes: validation_item=training_simulated_gate_has_formal_effect
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-011: Fix the underlying low-score artifacts first: result sources, figure files/contracts, paper sections, evidence bindings, and revision tasks; then rerun auto_review so scores rise above threshold. | acceptance: Every review_scorecard row is at least 85% of max_score, with supporting artifact fixes present. | notes: validation_item=training_review_score_below_threshold
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-012: Fix the underlying low-score artifacts first: result sources, figure files/contracts, paper sections, evidence bindings, and revision tasks; then rerun auto_review so scores rise above threshold. | acceptance: Every review_scorecard row is at least 85% of max_score, with supporting artifact fixes present. | notes: validation_item=training_review_score_below_threshold
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-013: Fix the underlying low-score artifacts first: result sources, figure files/contracts, paper sections, evidence bindings, and revision tasks; then rerun auto_review so scores rise above threshold. | acceptance: Every review_scorecard row is at least 85% of max_score, with supporting artifact fixes present. | notes: validation_item=training_review_score_below_threshold

Rules:
- Follow only deep_sequential behavior for this stage.
- Do not edit `00_problem/problem_statement.md` or `00_problem/inbox/`; write intake analysis to `01_task_analysis/`.
- A formal human gate becomes a simulated sandbox gate. Record it in `11_review/simulated_human_gate_log.csv`.
- Update contracts before writing paper claims, result analysis, figures, or submission text.
- Reply only through runner file actions. The external runner will reject prose-only or pseudo-tool responses.

Stage output target:
- Create or update the artifacts normally owned by `final_export`.
- If this stage cannot close a blocker, update review/revision artifacts with a concrete blocker note.
- Keep `reports/training_enhancement_points.csv` current once a full draft or review finding exists.

Stage-specific required outputs:
- Write `12_submission/final_submit_paper.md` as the submit-ready paper text copied or assembled from `09_paper/full_draft.md` after contracts exist.
- The final submit paper must preserve the latest full_draft topic markers, especially T01/T02/T03, RGB, and concentration; do not replace it with a generic paper.
- If `09_paper/full_draft.md` changed in the same iteration, final_export must refresh `12_submission/final_submit_paper.md` from that latest draft.
- Write `12_submission/final_submit_package.md` with included artifacts and residual risks.
- Write `reports/training_enhancement_points.csv` and `.md`; CSV must include at least one target_area each of system, prompt, and gate.
- Ensure simulated gate log has at least four rows and formal_effect is `none` for every row.

