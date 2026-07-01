# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_LOCAL_CONTRACTSTRICT_V2_CODEX\workspace`
Run dir: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_LOCAL_CONTRACTSTRICT_V2_CODEX`
Call id: `initial_07_results_freeze`
Iteration: 1
Max iterations: 3
Current simulated stage: `results_freeze`
Stage order: 7
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_LOCAL_CONTRACTSTRICT_V2_CODEX/reports/prompt_route_manifest.md`
Training sandbox stage prompt bundle: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_LOCAL_CONTRACTSTRICT_V2_CODEX/reports/stage_prompt_bundle.md`

Rules:
- Follow only deep_sequential behavior for this stage.
- Do not edit `00_problem/problem_statement.md` or `00_problem/inbox/`; write intake analysis to `01_task_analysis/`.
- A formal human gate becomes a simulated sandbox gate. Record it in `11_review/simulated_human_gate_log.csv`.
- Update contracts before writing paper claims, result analysis, figures, or submission text.
- Reply only through runner file actions. The external runner will reject prose-only or pseudo-tool responses.

Stage output target:
- Create or update the artifacts normally owned by `results_freeze`.
- If this stage cannot close a blocker, update review/revision artifacts with a concrete blocker note.
- Keep `reports/training_enhancement_points.csv` current once a full draft or review finding exists.

Stage-specific required outputs:
- Write non-empty `14_contracts/result_contract.csv` with result_id, metric_name, metric_value, source_file, used_by_claim_ids, freeze_status.
- Every numerical result cited later must have a result_contract row.
- Write or update reproducible result files under `07_results/` before freezing numbers.

