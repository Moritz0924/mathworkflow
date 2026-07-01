# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX\workspace`
Run dir: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX`
Call id: `iteration_05_15_final_export`
Iteration: 5
Max iterations: 5
Current simulated stage: `final_export`
Stage order: 15
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX/reports/prompt_route_manifest.md`
Training sandbox stage prompt bundle: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX/reports/stage_prompt_bundle.md`

Revision queue: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX\reports\agent_revision_queue.csv`

Open fail/major queue items:
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-002: Add existing output_svg/output_png/output_pdf files for every figure_contract row. | acceptance: Each figure_contract row references at least one existing figure file. | notes: validation_item=training_figure_contract_missing_output
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-003: Add existing output_svg/output_png/output_pdf files for every figure_contract row. | acceptance: Each figure_contract row references at least one existing figure file. | notes: validation_item=training_figure_contract_missing_output
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-004: Add existing output_svg/output_png/output_pdf files for every figure_contract row. | acceptance: Each figure_contract row references at least one existing figure file. | notes: validation_item=training_figure_contract_missing_output
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-005: Add existing output_svg/output_png/output_pdf files for every figure_contract row. | acceptance: Each figure_contract row references at least one existing figure file. | notes: validation_item=training_figure_contract_missing_output
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-006: Resolve validation failure training_claim_missing_figure_link: C005: F006 | acceptance: validate_agent_run.py no longer reports training_claim_missing_figure_link. | notes: validation_item=training_claim_missing_figure_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-007: Resolve validation failure training_claim_missing_figure_link: C007: F005 | acceptance: validate_agent_run.py no longer reports training_claim_missing_figure_link. | notes: validation_item=training_claim_missing_figure_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-008: Make paper figure references match figure_contract ids exactly and register each cited figure with an existing file. | acceptance: Every `图F###` paper reference has a matching figure_contract.csv row and existing output file. | notes: validation_item=training_paper_unregistered_figure_reference
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-009: Make paper figure references match figure_contract ids exactly and register each cited figure with an existing file. | acceptance: Every `图F###` paper reference has a matching figure_contract.csv row and existing output file. | notes: validation_item=training_paper_unregistered_figure_reference
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-010: Make paper figure references match figure_contract ids exactly and register each cited figure with an existing file. | acceptance: Every `图F###` paper reference has a matching figure_contract.csv row and existing output file. | notes: validation_item=training_paper_unregistered_figure_reference
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-011: Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied. | acceptance: All major/fail revision_tasks.csv rows have status closed/resolved/waived. | notes: validation_item=training_revision_task_unresolved
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-012: Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied. | acceptance: All major/fail revision_tasks.csv rows have status closed/resolved/waived. | notes: validation_item=training_revision_task_unresolved
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-013: Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied. | acceptance: All major/fail revision_tasks.csv rows have status closed/resolved/waived. | notes: validation_item=training_revision_task_unresolved

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

