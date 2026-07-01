# Revision Stage Blocker Note

Date: 2025-06-04
Stage: revision (call: initial_12_revision)

## Reason
Required inputs missing:
- `14_contracts/revision_tasks.csv`
- `11_review/review_scorecard.csv`

Cannot execute revision tasks without an approved, scoped task list and a review scorecard that records fail/major findings.

## Recommended Action
1. Run the `auto_review` stage to produce reviewer comments, scorecard, and populate `revision_tasks.csv`.
2. Alternately, manually prepare `revision_tasks.csv` with approved tasks and ensure `review_scorecard.csv` is present.
3. Once inputs are available, re-run the revision stage.

## Impact
- Stage blocked; no target files modified.
- Revision task closure cannot begin.
- Gate `revision_closure_gate` cannot be passed.
