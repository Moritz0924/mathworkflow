# Reviewer Comments: Blocker

## Summary
The auto_review stage cannot proceed because the required full paper draft is missing from the expected location (09_paper/). Additionally, core contracts (claim_evidence_map.csv, result_contract.csv, figure_contract.csv) have not been verified. Without these inputs, no meaningful review can be conducted.

## Required Pre-conditions
1. Complete paper_full stage to produce a draft in 09_paper/.
2. Ensure 14_contracts/ contains claim_evidence_map.csv, result_contract.csv, and figure_contract.csv.
3. Validate contracts using `scripts/validate_contracts.py`.

## Recommended Action
Stop auto_review and roll back to paper_full stage. Update workflow state accordingly.
