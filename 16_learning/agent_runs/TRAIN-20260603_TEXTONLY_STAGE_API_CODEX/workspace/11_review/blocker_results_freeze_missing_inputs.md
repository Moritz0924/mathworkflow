# Blocker: results_freeze stage cannot start

**Blocked by:** missing required inputs.
**Details:**
- `07_results/`: no output files present.
- `06_code/`: no run logs present.
- `14_contracts/result_contract.csv`: empty or unreachable.

**Action:** Complete codegen stage and produce verifiable outputs before re-entering results_freeze.
