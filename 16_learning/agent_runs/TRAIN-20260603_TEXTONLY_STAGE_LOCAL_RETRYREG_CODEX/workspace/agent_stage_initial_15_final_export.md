# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_LOCAL_RETRYREG_CODEX\workspace`
Run dir: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_LOCAL_RETRYREG_CODEX`
Call id: `initial_15_final_export`
Iteration: 1
Max iterations: 3
Current simulated stage: `final_export`
Stage order: 15
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_LOCAL_RETRYREG_CODEX/reports/prompt_route_manifest.md`
Training sandbox stage prompt bundle: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_LOCAL_RETRYREG_CODEX/reports/stage_prompt_bundle.md`

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
- Write `12_submission/final_submit_package.md` with included artifacts and residual risks.
- Write `reports/training_enhancement_points.csv` and `.md`; CSV must include at least one target_area each of system, prompt, and gate.
- Ensure simulated gate log has at least four rows and formal_effect is `none` for every row.

