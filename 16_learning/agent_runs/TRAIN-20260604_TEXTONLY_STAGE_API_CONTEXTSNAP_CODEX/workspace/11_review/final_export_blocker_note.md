# Final Export Blocker Note

- stage: final_export
- timestamp: 2026-06-04T18:00:00Z
- run_id: TRAIN-20260604_TEXTONLY_STAGE_API_CONTEXTSNAP_CODEX

## Summary

Final export cannot complete because contract validation (reported in `11_review/contract_validation_report.md`) still has 8 **fail** items:

- `figure_unknown_result` (6): figure_contract.csv references result_id fields that use semicolon separators (`R01;R02;...`) which the validator interprets as a single non-existent ID. All referenced IDs exist in result_contract.csv but the separator causes false positives.
- `unsupported_claim` (1): claim C06 in claim_evidence_map.csv has a misaligned field that places the support_grade `moderate` in the citation_id column, making the citation reference invalid.
- `polish_changed_protected_atom` (1): polish_diff_check line POL-000 has `decision=blocked` despite zero actual changes, creating a spurious block.

## Stage constraint

According to the final_export prompt, contracts in `14_contracts/` are **read-only** and cannot be updated in this stage. These fixes must be applied in an earlier stage (e.g., revision or polish) or waived by a human gate. Therefore the export pipeline stops here.

## Impact

- Final submission package (12_submission/) cannot be stamped as verified.
- Paper content and figures are complete and consistent with results, but the contractual traceability layer is broken.
- The simulated human gate log records that this gate is blocked until the above issues are resolved upstream.

## Recommended actions

1. In a prior stage, rewrite figure_contract.csv using comma-separated result_id lists and validate.
2. Correct claim_evidence_map.csv row C06 to place citation_id as empty and support_grade as `moderate`.
3. Change polish_diff_check.csv POL-000 decision to `pass`.
4. Rerun `scripts/validate_contracts.py` until 0 fails.
5. Re-enter final_export with a clean contract bus.
