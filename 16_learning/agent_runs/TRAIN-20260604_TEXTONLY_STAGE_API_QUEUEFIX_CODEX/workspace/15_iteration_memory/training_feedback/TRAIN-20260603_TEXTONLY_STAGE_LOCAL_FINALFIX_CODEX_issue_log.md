# TRAIN-20260603 Sandbox Issue Log

## Current Verdict

- Latest safe acceptance run: `TRAIN-20260603_TEXTONLY_STAGE_LOCAL_FINALFIX_CODEX`
- Executor: repo-only local staged executor via `MMWF_AGENT_CMD_JSON`
- Result: completed
- Benchmark: gap_count=0, queue_count=0
- Agent validation: pass, fail_count=0, warn_count=1 (`empty_gap_report`)
- Contract validation: pass, fail_count=0, warn_count=0
- Copy risk: pass, max_overlap_ratio=0.001642
- Feedback promotion dry-run: `FORMAL-20260603_FEEDBACK_LOCAL_FINALFIX_DRYRUN_CODEX`
- Feedback bundle: `15_iteration_memory/training_feedback/TRAIN-20260603_TEXTONLY_STAGE_LOCAL_FINALFIX_CODEX_feedback.*`

## External API Status

The requested live DeepSeek validation was attempted after user consent, but tool escalation was rejected by the environment reviewer because sending project workspace context and prompts to an untrusted external API is disallowed by tenant policy. No workaround was attempted. The run was therefore replaced with a materially safer repo-only local validation run.

## Problems Observed And Fixes

| ID | Problem | Root Cause | Fix / Status | Evidence |
|---|---|---|---|---|
| P01 | Earlier API sandbox could complete benchmark while still failing validation | Benchmark gap report did not include all contract/reviewer gates | Kept benchmark as one gate only; validation and contract blockers now prevent promotion | `agent_run_validation.json`, `contract_validation_report.json` |
| P02 | `final_submit_paper.md` drifted away from latest `09_paper/full_draft.md` | Final export stage wrote a generic paper instead of refreshing from full draft | Added `refresh_training_final_submit()` runner guard and report | `workspace/reports/final_export_refresh.json` |
| P03 | Topic drift missed when paper kept RGB/concentration but omitted T01/T02/T03 | Topic checker accepted 2 of 3 marker groups | Tightened topic alignment to require locked target IDs when source contains them | `scripts/self_test_agent_mode.py` |
| P04 | `figF001` and `F001` were treated as unrelated figures | Validator compared raw figure ids | Added figure-id normalization for `figF001`/`F001`/zero-padding aliases | `normalize_figure_id()` tests |
| P05 | Figure rows using `claim_ids` were treated as lacking evidence | Validator only accepted direct `result_id`/`evidence_source` | Accept figure -> claim -> result evidence binding, but still reject unbound generic source rows | contract alias self-test |
| P06 | DeepSeek wrote `simulated_none` instead of required `none` | Prompt instruction was not enough to enforce exact CSV value | Normalized simulated gate CSV file actions before write | `test_gate_file_action_normalizes_formal_effect` |
| P07 | Contract validation ran only at final closeout | Contract failures did not seed next iteration queue | Added `merge_contract_failures_into_queue()` and stage routing for contract items | `test_contract_failures_seed_stage_routed_queue` |
| P08 | Queue task ids could duplicate across repeated merge passes | Validation merge restarted numbering from 001 each call | Task ids now use current queue length | code change in `merge_validation_failures_into_queue` |
| P09 | `evidence_ref` result claims were flagged unsupported | Contract validator only read `result_id` fields | Added `evidence_ref/evidence_id` support by evidence_type | contract alias self-test |
| P10 | `validated`/`verified` statuses produced noisy warnings | Status whitelist was too narrow | Added `validated`, `verified`, `pass` as accepted active statuses | contract validation self-test |
| P11 | Review scores below 85 remained open blockers | Old API artifact still had 8/10 and 7/10 pass rows | Kept as a real quality gate; prompt now says 9/10 or 10/10 is required for pass on 10-point scale | old API revalidation still fails, local finalfix passes |
| P12 | Citation rows in old API artifact lacked support metadata | Old API generated active citation rows without support_grade/metadata_verified | Contract queue now routes citation failures to prior_retrieval/paper_full/final_export | old API contract revalidation |
| P13 | Live API verification unavailable | Environment policy forbids external disclosure to DeepSeek | Blocked for live API; safe local validation substituted | escalation rejection |

## Verification Commands

- `python scripts/self_test_agent_mode.py` -> pass
- `python -m py_compile scripts/deepseek_agent_runner.py scripts/run_agent_mode.py scripts/benchmark_agent_run.py scripts/validate_contracts.py scripts/validate_agent_run.py scripts/self_test_agent_mode.py` -> pass
- `python scripts/deepseek_agent_runner.py --self-test --offline` -> pass
- `python scripts/validate_agent_run.py --run-id TRAIN-20260603_TEXTONLY_STAGE_LOCAL_CONTRACTINTEGRATED_CODEX` -> pass
- `python scripts/validate_contracts.py --root 16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_LOCAL_CONTRACTINTEGRATED_CODEX/workspace --stage final_export` -> pass
- Local full sandbox with `MMWF_AGENT_CMD_JSON` -> `TRAIN-20260603_TEXTONLY_STAGE_LOCAL_FINALFIX_CODEX` completed, validation pass, contract pass
- `python scripts/run_agent_mode.py --mode formal_assist --dry-run --feedback-run-id TRAIN-20260603_TEXTONLY_STAGE_LOCAL_FINALFIX_CODEX --run-id FORMAL-20260603_FEEDBACK_LOCAL_FINALFIX_DRYRUN_CODEX` -> dry-run pass

## Promotion Boundary

The validated training run contributes workflow suggestions only. It does not promote sandbox paper facts into the formal paper. Formal adoption still requires human gate, contract validation, and stage-state control.
