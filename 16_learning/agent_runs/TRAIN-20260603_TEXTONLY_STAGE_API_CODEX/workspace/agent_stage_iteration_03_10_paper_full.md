# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_API_CODEX\workspace`
Run dir: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_API_CODEX`
Call id: `iteration_03_10_paper_full`
Iteration: 3
Max iterations: 3
Current simulated stage: `paper_full`
Stage order: 10
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_API_CODEX/reports/prompt_route_manifest.md`
Formal stage prompt bundle: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_API_CODEX/reports/stage_prompt_bundle.md`

Revision queue: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_API_CODEX\reports\agent_revision_queue.csv`

Rules:
- Follow only deep_sequential behavior for this stage.
- Do not edit `00_problem/problem_statement.md` or `00_problem/inbox/`; write intake analysis to `01_task_analysis/`.
- A formal human gate becomes a simulated sandbox gate. Record it in `11_review/simulated_human_gate_log.csv`.
- Update contracts before writing paper claims, result analysis, figures, or submission text.
- Reply only through runner file actions. The external runner will reject prose-only or pseudo-tool responses.

Stage output target:
- Create or update the artifacts normally owned by `paper_full`.
- If this stage cannot close a blocker, update review/revision artifacts with a concrete blocker note.
- Keep `reports/training_enhancement_points.csv` current once a full draft or review finding exists.
