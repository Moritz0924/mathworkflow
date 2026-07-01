# Revision Stage Blocker

## Timestamp
2026-06-03T00:00:00Z (sandbox)

## Reason
Revision stage cannot proceed because the following prerequisite artifacts cannot be read or verified:
- `14_contracts/revision_tasks.csv`
- `11_review/review_scorecard.csv`

The current execution environment provides no read mechanism for the agent; only file-write operations are supported. Without the task list and scorecard, no targeted revision can be performed.

## Impact
- No revision tasks can be processed.
- No contracts can be updated for revision closure.
- The stage remains blocked until the artifacts are provided or confirmed present.

## Required Action
1. Human operator or upstream controller must ensure these files exist in the workspace.
2. If the `auto_review` stage was not run, it must be executed first to generate the review scorecard and revision tasks.
3. Alternatively, provide explicit task data via another channel.

## Blocker Classification
- Severity: CRITICAL
- Type: missing_input
- Suggested immediate action: confirm file presence and rerun stage.
