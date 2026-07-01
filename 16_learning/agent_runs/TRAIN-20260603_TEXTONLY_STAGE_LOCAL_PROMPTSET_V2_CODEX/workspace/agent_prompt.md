# Full-Agent Training Sandbox Wrapper

You are operating inside a sandbox workspace, not the formal project root.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260603_TEXTONLY_STAGE_LOCAL_PROMPTSET_V2_CODEX\workspace`
Max iterations: 3
Prompt route manifest: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_LOCAL_PROMPTSET_V2_CODEX/reports/prompt_route_manifest.md`
Prompt route CSV: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_LOCAL_PROMPTSET_V2_CODEX/reports/prompt_route_manifest.csv`
Training sandbox stage prompt bundle: `16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_LOCAL_PROMPTSET_V2_CODEX/reports/stage_prompt_bundle.md`

This wrapper is not a replacement for the formal prompt system. The training route uses sandbox-specific backup prompts derived from the normal competition prompts:

1. Global prompt contract: `prompts/stage_prompt_contract.md`
2. Formal source prompts: `prompts/stages/00_*.md` through `prompts/stages/15_*.md`
3. Sandbox backup prompts: `prompts/training_sandbox/stages/00_*.md` through `prompts/training_sandbox/stages/15_*.md`
4. Stage order and prompt file mapping: the prompt route manifest above
5. Exact assembled sandbox prompts with formal sources: the stage prompt bundle above

Full-agent training rules:
- Use the sandbox backup prompt for each stage; never modify the formal source prompt files during a training run.
- Sandbox prompt changes are candidate workflow improvements only until they pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.
- Walk the 16 stage prompts in deep_sequential order inside the sandbox.
- A human gate in a formal stage becomes a simulated sandbox gate, not a formal confirmation. Record each simulated gate in `11_review/simulated_human_gate_log.csv` with stage, gate name, agent decision, evidence, and residual risk.
- Do not write outside the sandbox workspace.
- Do not copy prior paper abstracts, body text, captions, tables, or conclusions.
- Generate paper facts only from sandbox code, contracts, data, figures, and review artifacts.
- Keep result numbers in `14_contracts/result_contract.csv`.
- Keep claims in `14_contracts/claim_evidence_map.csv`.
- Keep figures in `14_contracts/figure_contract.csv` and cite only existing files.
- After a draft exists, use local prior DB only for gap comparison, not as an answer key.
- A single training run may contain multiple revision turns, but the run output must represent one full simulated competition pass.

Full-agent final outputs:
- Produce or assemble a complete Chinese paper in `09_paper/full_draft.md`.
- Copy the submit-ready version to `12_submission/final_submit_paper.md`.
- Produce `12_submission/final_submit_package.md`.
- Produce training improvement outputs for the workflow itself:
  - `reports/training_enhancement_points.csv`
  - `reports/training_enhancement_points.md`
  - include at least one `system`, one `prompt`, and one `gate` enhancement item.

Final expected sandbox artifacts:
- `09_paper/full_draft.md`
- `12_submission/final_submit_paper.md`
- `12_submission/final_submit_package.md`
- `14_contracts/result_contract.csv`
- `14_contracts/claim_evidence_map.csv`
- `14_contracts/figure_contract.csv`
- `11_review/review_scorecard.csv`
- `14_contracts/revision_tasks.csv`
- `reports/prompt_route_manifest.csv`
- `reports/training_enhancement_points.csv`
- `reports/training_enhancement_points.md`
