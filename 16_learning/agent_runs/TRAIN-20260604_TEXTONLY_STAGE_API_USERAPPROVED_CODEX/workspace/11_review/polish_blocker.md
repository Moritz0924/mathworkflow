## Polish Stage Blocker

**Issue**: Polish stage simulation called without required inputs.

**Required inputs**:
- Artifact freeze registry (`14_contracts/artifact_freeze_registry.csv`)
- Polish diff check scaffold (`14_contracts/polish_diff_check.csv`)
- Confirmed paper chapters (from revision close)

**Recommendation**: Run prior stages (revision) to generate the confirmed chapters and register artifacts before polish.

**Severity**: BLOCKER
