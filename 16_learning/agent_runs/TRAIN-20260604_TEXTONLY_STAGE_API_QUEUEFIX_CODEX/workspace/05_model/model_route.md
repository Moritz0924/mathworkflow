# Model Route - BLOCKED

## Status

The `model_route` stage cannot be executed because required inputs from prior stages are missing.

## Required Inputs

- `01_task_analysis/task_decomposition.md` — missing (stage `task_analysis` not completed)
- `01_task_analysis/problem_model_profile.csv` — missing
- `03_data/data_quality_report.md` — missing (stage `data` not completed)

## Optional Inputs (also missing)

- `04_eda/eda_summary_for_paper.md` — missing
- `13_prior_db/pre_solve_cards.md` — not yet retrieved

## Next Steps

Complete the following stages before re-running `model_route`:
1. `intake` — analyze problem statement and produce task decomposition
2. `task_analysis` — formalize sub-questions, variables, and model profile
3. `data` — acquire, clean, and document data; produce quality report
4. `eda` — exploratory analysis and summary for modeling

Once these are completed, `model_route` can select primary and fallback models for each sub-question and register formulas.

## Artificial Gate

The simulated human gate for `model_route` is recorded in `11_review/simulated_human_gate_log.csv`. This gate must be passed before the model route is frozen.
