# Live DeepSeek API Acceptance Handoff

## Status

Codex attempted to start a live DeepSeek API validation run for the training sandbox after user consent. The escalation reviewer rejected the call because sending project workspace context, prompts, and problem text to an untrusted external DeepSeek API is disallowed by the current environment policy.

This file is a handoff for a human/operator to run the same acceptance step only in an environment where external API disclosure is allowed.

## Current Safe Acceptance Baseline

- Safe local run: `TRAIN-20260603_TEXTONLY_STAGE_LOCAL_FINALFIX_CODEX`
- Executor: repo-only staged executor
- Result: completed
- Benchmark: `gap_count=0`, `queue_count=0`
- Agent validation: pass, `fail_count=0`, one non-blocking `empty_gap_report` warning
- Contract validation: pass, `fail_count=0`, `warn_count=0`
- Copy risk: pass
- Feedback dry-run: `FORMAL-20260603_FEEDBACK_LOCAL_FINALFIX_DRYRUN_CODEX`

## External Data Scope

The live API command sends the following to the configured DeepSeek endpoint:

- `00_problem/inbox/text_only_color_concentration_problem.md`
- sandbox stage prompts derived from the formal prompt set
- per-stage sandbox workspace context required by `scripts/deepseek_agent_runner.py`
- revision queue, benchmark, contract, and validation context when present

Do not run this command unless the environment owner permits that disclosure.

## Command

Use a new run id so previous failed runs remain preserved as audit evidence:

```powershell
python scripts/run_agent_mode.py `
  --mode training_sandbox `
  --problem 00_problem/inbox/text_only_color_concentration_problem.md `
  --max-iterations 5 `
  --run-id TRAIN-20260604_TEXTONLY_STAGE_API_HANDOFF_CODEX `
  --external-api-approved
```

The default remains 3 iterations in config. This handoff uses 5 only for acceptance because the runner is gap-driven and will stop early when open fail/major blockers clear; it will also stop when the same blocking gap stops improving.

## Expected Evidence

After the run, inspect these files:

- `16_learning/agent_runs/<run_id>/run_manifest.yaml`
- `16_learning/agent_runs/<run_id>/reports/stage_execution_manifest.csv`
- `16_learning/agent_runs/<run_id>/reports/agent_run_validation.json`
- `16_learning/agent_runs/<run_id>/reports/agent_revision_queue.csv`
- `16_learning/agent_runs/<run_id>/reports/copy_risk_report.csv`
- `16_learning/agent_runs/<run_id>/workspace/11_review/contract_validation_report.json`
- `16_learning/agent_runs/<run_id>/deepseek_calls/*/deepseek_stream_status.jsonl`
- `16_learning/agent_runs/<run_id>/reports/training_enhancement_points.csv`

## Acceptance Criteria

- Initial stage execution contains all 16 stages and is not stuck at `intake`.
- At least one later iteration reads open validation/contract blockers if blockers exist after the initial pass.
- Stream heartbeats exist for live DeepSeek calls and record chunk counts, content chars, reasoning chars, idle seconds, and elapsed seconds.
- `agent_run_validation.json` has `status=pass` and `fail_count=0`.
- `contract_validation_report.json` has `fail_count=0`.
- `copy_risk_report.csv` decision is `pass`.
- `agent_revision_queue.csv` has no open `fail` or `major` rows.
- `training_enhancement_points.csv` contains at least `system`, `prompt`, and `gate` target areas.
- Any generated formal feedback remains suggestion-only and is not auto-applied to protected formal deliverables.

## Promotion Step

If the live API run passes, generate a formal-assist dry run:

```powershell
python scripts/run_agent_mode.py `
  --mode formal_assist `
  --dry-run `
  --feedback-run-id TRAIN-20260604_TEXTONLY_STAGE_API_HANDOFF_CODEX `
  --run-id FORMAL-20260604_FEEDBACK_API_HANDOFF_DRYRUN_CODEX
```

This should create `15_iteration_memory/training_feedback/<run_id>_feedback.*`. The feedback rows are suggestions only and still require human gate, contract validation, and stage-state control before formal adoption.
