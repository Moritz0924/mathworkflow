# Training Prompt Route Manifest

- generated_at: 2026-06-02T18:17:19
- global_contract: prompts/stage_prompt_contract.md
- stage_count: 16

The training sandbox must follow these stage prompt files in deep_sequential order. A training round may simulate multiple stages, but every artifact must remain bound to the stage prompt, path permissions, contracts, and human-gate rules.

| order | stage | prompt | status |
|---:|---|---|---|
| 0 | latex_template | prompts/stages/latex_template.md | missing |
| 1 | intake | prompts/stages/intake.md | missing |
| 2 | eda | prompts/stages/eda.md | missing |
| 3 | task_analysis | prompts/stages/task_analysis.md | missing |
| 4 | prior_retrieval | prompts/stages/prior_retrieval.md | missing |
| 5 | model_route | prompts/stages/model_route.md | missing |
| 6 | codegen | prompts/stages/codegen.md | missing |
| 7 | results_freeze | prompts/stages/results_freeze.md | missing |
| 8 | figures | prompts/stages/figures.md | missing |
| 9 | paper_draft | prompts/stages/paper_draft.md | missing |
| 10 | paper_full | prompts/stages/paper_full.md | missing |
| 11 | auto_review | prompts/stages/auto_review.md | missing |
| 12 | revision | prompts/stages/revision.md | missing |
| 13 | polish | prompts/stages/polish.md | missing |
| 14 | compile | prompts/stages/compile.md | missing |
| 15 | final_export | prompts/stages/final_export.md | missing |
