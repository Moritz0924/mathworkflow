# Pre-Solve Experience Cards (Placeholder)

**Date:** (unknown)
**Stage:** prior_retrieval
**Status:** BLOCKED - missing inputs

## Summary

No prior database (`13_prior_db/`, `13_sample_prior/`) detected, and `config/prior_db_policy.yaml` not available. Required `01_task_analysis/problem_model_profile.csv` missing. Unable to retrieve experience cards.

According to recovery procedure: create empty experience card placeholder and indicate no available priors.

## Advisory Only

All output in this file is advisory only and must not be taken as factual answers or copied into paper.

## Extracted Cards

None.

## Risk List

- Missing problem model profile: cannot map question to prior types.
- Prior database absent: no model hints, figure hints, or scoring risks can be extracted.
- Copy-risk: N/A (no text generated).

## Next Steps

1. Run task_analysis stage to produce `01_task_analysis/problem_model_profile.csv`.
2. Ensure `config/prior_db_policy.yaml` exists.
3. Rerun prior_retrieval stage.
