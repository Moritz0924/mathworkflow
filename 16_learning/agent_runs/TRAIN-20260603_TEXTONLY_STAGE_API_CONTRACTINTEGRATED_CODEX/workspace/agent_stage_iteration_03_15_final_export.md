# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_API_CONTRACTINTEGRATED_CODEX\workspace`
Run dir: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_API_CONTRACTINTEGRATED_CODEX`
Call id: `iteration_03_15_final_export`
Iteration: 3
Max iterations: 3
Current simulated stage: `final_export`
Stage order: 15
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_API_CONTRACTINTEGRATED_CODEX/reports/prompt_route_manifest.md`
Training sandbox stage prompt bundle: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_API_CONTRACTINTEGRATED_CODEX/reports/stage_prompt_bundle.md`

Revision queue: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_API_CONTRACTINTEGRATED_CODEX\reports\agent_revision_queue.csv`

Open fail/major queue items:
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_CONTRACTINTEGRATED_CODEX-VAL-001: Rewrite the paper and contracts to match the locked color-channel/concentration problem; remove AQI, wine-quality, or unrelated benchmark content. | acceptance: final_submit_paper.md mentions the locked problem markers such as color/RGB/concentration/T01-T03 and no unrelated topic markers. | notes: validation_item=training_topic_alignment_drift
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_CONTRACTINTEGRATED_CODEX-VAL-002: Expand 12_submission/final_submit_paper.md from the latest full_draft with substantive problem analysis, model, results, validation, and conclusion sections. | acceptance: final_submit_paper.md has at least 2500 characters and at least seven sections. | notes: validation_item=training_final_paper_too_thin
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_CONTRACTINTEGRATED_CODEX-VAL-003: Resolve validation failure training_claim_missing_formula_link: C007: medium | acceptance: validate_agent_run.py no longer reports training_claim_missing_formula_link. | notes: validation_item=training_claim_missing_formula_link
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_CONTRACTINTEGRATED_CODEX-VAL-004: Resolve validation failure training_claim_missing_formula_link: C008: strong | acceptance: validate_agent_run.py no longer reports training_claim_missing_formula_link. | notes: validation_item=training_claim_missing_formula_link
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_CONTRACTINTEGRATED_CODEX-VAL-005: Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied. | acceptance: All major/fail revision_tasks.csv rows have status closed/resolved/waived. | notes: validation_item=training_revision_task_unresolved
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_CONTRACTINTEGRATED_CODEX-VAL-006: Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied. | acceptance: All major/fail revision_tasks.csv rows have status closed/resolved/waived. | notes: validation_item=training_revision_task_unresolved
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_CONTRACTINTEGRATED_CODEX-VAL-007: Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied. | acceptance: All major/fail revision_tasks.csv rows have status closed/resolved/waived. | notes: validation_item=training_revision_task_unresolved
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_CONTRACTINTEGRATED_CODEX-VAL-008: Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied. | acceptance: All major/fail revision_tasks.csv rows have status closed/resolved/waived. | notes: validation_item=training_revision_task_unresolved
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_CONTRACTINTEGRATED_CODEX-VAL-009: Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied. | acceptance: All major/fail revision_tasks.csv rows have status closed/resolved/waived. | notes: validation_item=training_revision_task_unresolved
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_CONTRACTINTEGRATED_CODEX-VAL-010: Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied. | acceptance: All major/fail revision_tasks.csv rows have status closed/resolved/waived. | notes: validation_item=training_revision_task_unresolved
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_CONTRACTINTEGRATED_CODEX-VAL-011: Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied. | acceptance: All major/fail revision_tasks.csv rows have status closed/resolved/waived. | notes: validation_item=training_revision_task_unresolved
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_CONTRACTINTEGRATED_CODEX-VAL-012: Update review scoring only after actual sandbox fixes raise the artifact quality above threshold. | acceptance: Every review_scorecard row is at least 85% of max_score. | notes: validation_item=training_review_score_below_threshold

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
- If `09_paper/full_draft.md` changed in the same iteration, final_export must refresh `12_submission/final_submit_paper.md` from that latest draft.
- Write `12_submission/final_submit_package.md` with included artifacts and residual risks.
- Write `reports/training_enhancement_points.csv` and `.md`; CSV must include at least one target_area each of system, prompt, and gate.
- Ensure simulated gate log has at least four rows and formal_effect is `none` for every row.

