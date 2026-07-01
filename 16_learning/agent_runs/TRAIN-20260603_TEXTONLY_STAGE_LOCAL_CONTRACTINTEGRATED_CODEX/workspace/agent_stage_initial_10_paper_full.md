# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_LOCAL_CONTRACTINTEGRATED_CODEX\workspace`
Run dir: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_LOCAL_CONTRACTINTEGRATED_CODEX`
Call id: `initial_10_paper_full`
Iteration: 1
Max iterations: 3
Current simulated stage: `paper_full`
Stage order: 10
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_LOCAL_CONTRACTINTEGRATED_CODEX/reports/prompt_route_manifest.md`
Training sandbox stage prompt bundle: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_LOCAL_CONTRACTINTEGRATED_CODEX/reports/stage_prompt_bundle.md`

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

Stage-specific required outputs:
- Write substantive `09_paper/full_draft.md` with at least 摘要, 问题分析, 模型建立, 结果分析, 验证/敏感性, 结论.
- Keep the paper topic aligned with the locked problem statement: color channels R/G/B and concentration prediction for T01/T02/T03; do not switch to AQI, wine quality, or unrelated benchmark topics.
- Write non-empty `14_contracts/claim_evidence_map.csv`; each major claim must bind to result_id and, where applicable, figure_id/formula_id.
- Write `14_contracts/formula_contract.csv` for important equations and symbol definitions.
- When `figure_density` is open, cite the registered figures in the paper using `图F001`, `图F002`, ... and include at least seven figure references if the benchmark threshold is above 6.

