# Agent Training Sandbox Task

You are operating inside a sandbox workspace, not the formal project root.

Workspace: `E:\math-module\math-workflow\math-workflow\16_learning\agent_runs\TRAIN-20260529_122952\workspace`
Max iterations: 3

Rules:
- Use deep_sequential order only.
- Do not write outside this workspace.
- Do not copy prior paper abstracts, body text, captions, tables, or conclusions.
- Generate outputs only from code, contracts, and sandbox artifacts.
- Keep result numbers in `14_contracts/result_contract.csv`.
- Keep claims in `14_contracts/claim_evidence_map.csv`.
- Keep figures in `14_contracts/figure_contract.csv` and cite only existing files.
- After a draft exists, use local prior DB only for gap comparison, not as an answer key.

Suggested command sequence:
1. Inspect `workflow_state.yaml`, `00_problem/`, `03_data/`, and `prompts/stages/`.
2. Run one stage at a time through `python scripts/run_current_stage.py --stage current`.
3. Stop at any human gate marker inside the sandbox and write the blocker into `11_review/`.
4. Produce or assemble `09_paper/full_draft.md`.
5. Record review issues in `11_review/` and `14_contracts/revision_tasks.csv`.

Final expected sandbox artifacts:
- `09_paper/full_draft.md`
- `14_contracts/result_contract.csv`
- `14_contracts/claim_evidence_map.csv`
- `14_contracts/figure_contract.csv`
- `11_review/review_scorecard.csv`
- `14_contracts/revision_tasks.csv`
