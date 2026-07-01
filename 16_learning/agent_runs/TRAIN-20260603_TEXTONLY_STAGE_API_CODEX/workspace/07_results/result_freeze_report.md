# Results Freeze Report

**Stage:** results_freeze
**Status:** blocked
**Date:** 2025-06-03 (simulated)

## Summary

The results_freeze stage cannot proceed because the required inputs are missing or unverified:
- No model outputs found in `07_results/`.
- No run logs found in `06_code/`.
- The `14_contracts/result_contract.csv` baseline is empty or absent.

Without concrete, reproducible outputs, no results can be frozen for paper use.

## Next Steps
- Return to `model_route` or `codegen` stages to generate model outputs.
- Ensure each output is accompanied by a run log and a unique `run_id`.
- Populate `result_contract.csv` with candidate results before re-attempting freeze.

## Human Gate
Awaiting confirmation that prior stages are complete and outputs are ready for freeze.
