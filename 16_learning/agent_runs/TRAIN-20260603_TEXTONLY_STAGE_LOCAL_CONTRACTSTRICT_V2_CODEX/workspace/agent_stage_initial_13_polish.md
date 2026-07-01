# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_LOCAL_CONTRACTSTRICT_V2_CODEX\workspace`
Run dir: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_LOCAL_CONTRACTSTRICT_V2_CODEX`
Call id: `initial_13_polish`
Iteration: 1
Max iterations: 3
Current simulated stage: `polish`
Stage order: 13
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_LOCAL_CONTRACTSTRICT_V2_CODEX/reports/prompt_route_manifest.md`
Training sandbox stage prompt bundle: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_LOCAL_CONTRACTSTRICT_V2_CODEX/reports/stage_prompt_bundle.md`

Rules:
- Follow only deep_sequential behavior for this stage.
- Do not edit `00_problem/problem_statement.md` or `00_problem/inbox/`; write intake analysis to `01_task_analysis/`.
- A formal human gate becomes a simulated sandbox gate. Record it in `11_review/simulated_human_gate_log.csv`.
- Update contracts before writing paper claims, result analysis, figures, or submission text.
- Reply only through runner file actions. The external runner will reject prose-only or pseudo-tool responses.

Stage output target:
- Create or update the artifacts normally owned by `polish`.
- If this stage cannot close a blocker, update review/revision artifacts with a concrete blocker note.
- Keep `reports/training_enhancement_points.csv` current once a full draft or review finding exists.

