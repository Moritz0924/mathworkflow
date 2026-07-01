# paper_full Blocked Report

**Timestamp**: 2026-06-03 (simulated)
**Stage**: paper_full (iteration 02)
**Status**: Blocked

## Reason

The paper_full stage requires completed outputs from earlier stages, specifically:
- Section drafts under `02_latex_template/sections/` (from paper_draft)
- `09_paper/missing_evidence_report.md`
- `14_contracts/claim_evidence_map.csv`

Current workflow state shows only `latex_template` completed; `intake`, `task_analysis`, `paper_draft`, and all intermediate stages are locked or pending.

## Actions Taken
No assembly performed. Logged this blocker and notified controller.

## Recommendations
Execute stages in order: intake → task_analysis → prior_retrieval → model_route → codegen → results_freeze → figures → paper_draft, then retry paper_full.
