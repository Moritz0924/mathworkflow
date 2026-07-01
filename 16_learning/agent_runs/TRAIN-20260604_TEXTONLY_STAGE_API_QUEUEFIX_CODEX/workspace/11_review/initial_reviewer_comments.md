# Prerequisite Check: Auto Review Blocked

## Summary
Auto-review stage cannot proceed because the full paper draft is missing from `09_paper/`. Additionally, required contract files (`claim_evidence_map.csv`, `result_contract.csv`, `figure_contract.csv`) have not been verified.

## Expected Inputs
- Full paper draft (likely `09_paper/full_draft.tex` or similar)
- `14_contracts/claim_evidence_map.csv`
- `14_contracts/result_contract.csv`
- `14_contracts/figure_contract.csv`

## Current Status
None of the above inputs were found in the workspace at the time of this review attempt. Without the draft and contracts, the multi-perspective review (problem, model, data, results, figures, writing, scoring) cannot be performed.

## Recommended Action
- Execute `paper_full` stage to generate the full paper draft and update all contracts.
- Then re-run `auto_review` stage.

## Blocker Severity: Fail
