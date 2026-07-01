# Revision Blocker Note

## Date
2026-06-03

## Stage
revision (stage 12)

## Block Reason
Required inputs are absent:
- `14_contracts/revision_tasks.csv` not found or empty.
- `11_review/review_scorecard.csv` not found.
- Prior stages `paper_draft` and `auto_review` are locked or not completed in workflow state.

Without these artifacts, there are no approved revision tasks to execute. The revision stage cannot proceed.

## Recommended Action
1. Complete prior stages up to `auto_review` to produce a paper draft, review comments, and revision tasks.
2. Populate `14_contracts/revision_tasks.csv` and `11_review/review_scorecard.csv`.
3. Re-enter the revision stage with valid inputs.

## Decision
No tasks closed. Simulated human gate remains blocked.
