# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX\workspace`
Run dir: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX`
Call id: `iteration_02_08_figures`
Iteration: 2
Max iterations: 5
Current simulated stage: `figures`
Stage order: 8
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX/reports/prompt_route_manifest.md`
Training sandbox stage prompt bundle: `16_learning/agent_runs/TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX/reports/stage_prompt_bundle.md`

Revision queue: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX\reports\agent_revision_queue.csv`

Open fail/major queue items:
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-002: Resolve validation failure training_final_paper_placeholder: submit-ready paper still contains placeholder markers | acceptance: validate_agent_run.py no longer reports training_final_paper_placeholder. | notes: validation_item=training_final_paper_placeholder
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-003: Resolve validation failure training_claim_missing_figure_link: C001: 图F001 | acceptance: validate_agent_run.py no longer reports training_claim_missing_figure_link. | notes: validation_item=training_claim_missing_figure_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-004: Resolve validation failure training_claim_missing_figure_link: C001: 图F002 | acceptance: validate_agent_run.py no longer reports training_claim_missing_figure_link. | notes: validation_item=training_claim_missing_figure_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-005: Resolve validation failure training_claim_missing_figure_link: C001: 图F007 | acceptance: validate_agent_run.py no longer reports training_claim_missing_figure_link. | notes: validation_item=training_claim_missing_figure_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-006: Resolve validation failure training_claim_missing_formula_link: C001: 公式(3) | acceptance: validate_agent_run.py no longer reports training_claim_missing_formula_link. | notes: validation_item=training_claim_missing_formula_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-007: Resolve validation failure training_claim_missing_figure_link: C002: 图F002 | acceptance: validate_agent_run.py no longer reports training_claim_missing_figure_link. | notes: validation_item=training_claim_missing_figure_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-008: Resolve validation failure training_claim_missing_figure_link: C002: 图F004 | acceptance: validate_agent_run.py no longer reports training_claim_missing_figure_link. | notes: validation_item=training_claim_missing_figure_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-009: Resolve validation failure training_claim_missing_formula_link: C002: 公式(3) | acceptance: validate_agent_run.py no longer reports training_claim_missing_formula_link. | notes: validation_item=training_claim_missing_formula_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-010: Resolve validation failure training_claim_missing_figure_link: C003: 图F002 | acceptance: validate_agent_run.py no longer reports training_claim_missing_figure_link. | notes: validation_item=training_claim_missing_figure_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-011: Resolve validation failure training_claim_missing_formula_link: C003: 公式(3) | acceptance: validate_agent_run.py no longer reports training_claim_missing_formula_link. | notes: validation_item=training_claim_missing_formula_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-012: Resolve validation failure training_claim_missing_figure_link: C004: 图F002 | acceptance: validate_agent_run.py no longer reports training_claim_missing_figure_link. | notes: validation_item=training_claim_missing_figure_link
- [fail] TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-013: Resolve validation failure training_claim_missing_formula_link: C004: 公式(3) | acceptance: validate_agent_run.py no longer reports training_claim_missing_formula_link. | notes: validation_item=training_claim_missing_formula_link

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
- Write `14_contracts/figure_contract.csv` with this schema when possible: figure_id,result_id,evidence_source,chart_type,title_cn,output_svg,output_png,output_pdf,quality_score,used_in_section,latex_label,caption_cn,notes.
- Every figure_contract row must have result_id or evidence_source, and at least one existing output_svg/output_png/output_pdf/file_path.
- Prefer canonical figure ids `F001`, `F002`, ... in every contract and paper reference; do not invent `figF001` aliases.
- Create the referenced figure files under `08_figures/`; text placeholders are acceptable only if they are explicit sandbox figures.
- Do not cite figures in paper text unless they are registered and files exist.
- When a `figure_density` blocker is open, generate enough result-bound figures to meet the benchmark target; use at least seven registered figure ids when the queue threshold is above 6.
- Use exactly the same figure ids in text and contract, such as `图F001`; do not use bare `F1` as a figure reference.

