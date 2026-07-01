# Training Prompt Route Manifest

- generated_at: 2026-06-02T23:52:00
- global_contract: prompts/stage_prompt_contract.md
- stage_count: 16

The training sandbox must follow these stage prompt files in deep_sequential order. A training round may simulate multiple stages, but every artifact must remain bound to the stage prompt, path permissions, contracts, and human-gate rules.

| order | stage | prompt | status |
|---:|---|---|---|
| 0 | latex_template | prompts/stages/00_latex_template.md | yes |
| 1 | intake | prompts/stages/01_intake.md | yes |
| 2 | eda | prompts/stages/02_eda.md | yes |
| 3 | task_analysis | prompts/stages/03_task_analysis.md | yes |
| 4 | prior_retrieval | prompts/stages/04_prior_retrieval.md | yes |
| 5 | model_route | prompts/stages/05_model_route.md | yes |
| 6 | codegen | prompts/stages/06_codegen.md | yes |
| 7 | results_freeze | prompts/stages/07_results_freeze.md | yes |
| 8 | figures | prompts/stages/08_figures.md | yes |
| 9 | paper_draft | prompts/stages/09_paper_draft.md | yes |
| 10 | paper_full | prompts/stages/10_paper_full.md | yes |
| 11 | auto_review | prompts/stages/11_auto_review.md | yes |
| 12 | revision | prompts/stages/12_revision.md | yes |
| 13 | polish | prompts/stages/13_polish.md | yes |
| 14 | compile | prompts/stages/14_compile.md | yes |
| 15 | final_export | prompts/stages/15_final_export.md | yes |
