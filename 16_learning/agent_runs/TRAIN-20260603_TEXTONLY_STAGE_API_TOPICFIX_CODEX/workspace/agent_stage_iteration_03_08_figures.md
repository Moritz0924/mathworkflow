# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX\workspace`
Run dir: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX`
Call id: `iteration_03_08_figures`
Iteration: 3
Max iterations: 3
Current simulated stage: `figures`
Stage order: 8
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX/reports/prompt_route_manifest.md`
Training sandbox stage prompt bundle: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX/reports/stage_prompt_bundle.md`

Revision queue: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX\reports\agent_revision_queue.csv`

Open fail/major queue items:
- [major] TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX-TASK-001: Add result-bound figures and register them in the sandbox figure contract before citing them. | acceptance: Figure mentions are backed by existing figure files and figure_contract rows. | notes: from TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX-GAP-002
- [major] TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX-TASK-002: Add validation, sensitivity, robustness, or error analysis tied to model outputs. | acceptance: Validation section cites frozen result rows or reproducible code outputs. | notes: from TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX-GAP-003
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX-VAL-001: Rewrite the paper and contracts to match the locked color-channel/concentration problem; remove AQI, wine-quality, or unrelated benchmark content. | acceptance: final_submit_paper.md mentions the locked problem markers such as color/RGB/concentration/T01-T03 and no unrelated topic markers. | notes: validation_item=training_topic_alignment_drift
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX-VAL-002: Expand 12_submission/final_submit_paper.md from the latest full_draft with substantive problem analysis, model, results, validation, and conclusion sections. | acceptance: final_submit_paper.md has at least 2500 characters and at least seven sections. | notes: validation_item=training_final_paper_too_thin
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX-VAL-003: Refresh final_submit_paper.md from a topic-aligned full_draft and include the missing required section signal. | acceptance: validate_agent_run.py no longer reports training_final_paper_missing_section_signal. | notes: validation_item=training_final_paper_missing_section_signal
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX-VAL-004: Refresh final_submit_paper.md from a topic-aligned full_draft and include the missing required section signal. | acceptance: validate_agent_run.py no longer reports training_final_paper_missing_section_signal. | notes: validation_item=training_final_paper_missing_section_signal
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX-VAL-005: Add existing output_svg/output_png/output_pdf files for every figure_contract row. | acceptance: Each figure_contract row references at least one existing figure file. | notes: validation_item=training_figure_contract_missing_output
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX-VAL-006: Add existing output_svg/output_png/output_pdf files for every figure_contract row. | acceptance: Each figure_contract row references at least one existing figure file. | notes: validation_item=training_figure_contract_missing_output
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX-VAL-007: Add existing output_svg/output_png/output_pdf files for every figure_contract row. | acceptance: Each figure_contract row references at least one existing figure file. | notes: validation_item=training_figure_contract_missing_output
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX-VAL-008: Add existing output_svg/output_png/output_pdf files for every figure_contract row. | acceptance: Each figure_contract row references at least one existing figure file. | notes: validation_item=training_figure_contract_missing_output
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX-VAL-009: Add existing output_svg/output_png/output_pdf files for every figure_contract row. | acceptance: Each figure_contract row references at least one existing figure file. | notes: validation_item=training_figure_contract_missing_output
- [fail] TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX-VAL-010: Add existing output_svg/output_png/output_pdf files for every figure_contract row. | acceptance: Each figure_contract row references at least one existing figure file. | notes: validation_item=training_figure_contract_missing_output

Rules:
- Follow only deep_sequential behavior for this stage.
- Do not edit `00_problem/problem_statement.md` or `00_problem/inbox/`; write intake analysis to `01_task_analysis/`.
- A formal human gate becomes a simulated sandbox gate. Record it in `11_review/simulated_human_gate_log.csv`.
- Update contracts before writing paper claims, result analysis, figures, or submission text.
- Reply only through runner file actions. The external runner will reject prose-only or pseudo-tool responses.

Stage output target:
- Create or update the artifacts normally owned by `figures`.
- If this stage cannot close a blocker, update review/revision artifacts with a concrete blocker note.
- Keep `reports/training_enhancement_points.csv` current once a full draft or review finding exists.

Stage-specific required outputs:
- Write `14_contracts/figure_contract.csv` with figure_id, result_id or evidence_source, and at least one existing output_svg/output_png/output_pdf per row.
- Create the referenced figure files under `08_figures/`; text placeholders are acceptable only if they are explicit sandbox figures.
- Do not cite figures in paper text unless they are registered and files exist.
- When a `figure_density` blocker is open, generate enough result-bound figures to meet the benchmark target; use at least seven registered figure ids when the queue threshold is above 6.
- Use exactly the same figure ids in text and contract, such as `图F001`; do not use bare `F1` as a figure reference.

