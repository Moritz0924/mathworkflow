# Training Sandbox Issue Log

- run_id: TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX
- source_problem: 00_problem/inbox/text_only_color_concentration_problem.md
- status_after_revalidation: validation pass; benchmark gap_count=0; revision queue empty; copy-risk pass
- scope: issues observed while implementing and live-validating staged DeepSeek training sandbox

## Closed Issues

| issue | root cause | fix | verification |
|---|---|---|---|
| Initial API sandbox could stop after a single or partial stage | training_sandbox did not force per-stage deep_sequential execution | run_agent_mode now calls every routed stage with `--stage` and `--call-id`; stage manifest is required | live stage_execution_manifest has all 16 initial stages |
| Problem statement could drift or be overwritten | sandbox input paths were writable and benchmark did not fail on source drift | problem_source_lock.json, protected input paths, benchmark drift fail queue | self_test `test_problem_lock_drift`; live source lock present |
| Model responses could be prose, fenced JSON, or pseudo-tools | runner accepted weak protocol surfaces | strict JSON object protocol, pseudo-tool rejection, one protocol retry forced deep | deepseek self-test strict_protocol pass |
| Empty contracts could pass as warnings | final training gates only checked artifact existence | final/export validation requires non-empty result, claim, and figure contracts | self_test `test_final_contract_nonempty_gate` |
| Live API request could fail on transient disconnect | WinError 10054 aborted the whole staged sequence | network retry config and retryable request-error handling with stream status events | deepseek self-test; later live run completed all stages |
| Sandbox and formal prompts were not visibly separated | training prompt route reused formal prompt path semantics | sandbox backup prompts generated under `prompts/training_sandbox/stages/`, with formal source hashes retained | live prompt_route_manifest has formal/sandbox prompt columns |
| Training enhancements did not sync to formal feedback | formal feedback read queue items instead of validated enhancement candidates | feedback bundle now reads `training_enhancement_points.csv` after validation/copy-risk/no blockers | FORMAL-20260603_FEEDBACK_LIVE_DRYRUN_CODEX status ready |
| API writes to `workspace/reports` were invisible to run-level validation | runner applied file actions relative to workspace | run_agent_mode syncs selected workspace reports to run reports before benchmark/validation | live manifest has initial/iteration synced_reports |
| Iteration target order could run final_export before paper_full | stage target list preserved queue discovery order | iteration targets are sorted by formal stage_order | live iteration targets show figures/paper_full/final_export order |
| Model drifted to AQI/wine-style prior topics | source lock checked file drift, not paper topic alignment | topic-alignment validator and sandbox prompt topic lock | old AQI run now fails topic drift; later live run does not |
| `F1` metric was mistaken for a figure reference | figure regex matched any `F\d+` token | figure refs now require `图F###` or `Figure F###` | self_test `test_topic_alignment_and_figure_refs` |
| Figure contract used `file_path` instead of `output_svg` | model produced a common alternate schema | validators/reviewers accept `file_path` as an existing figure output alias | live validation now passes |
| Live API shell emitted PowerShell profile error | user PowerShell profile invokes `thefuck --alias` incompatibly | no repo mutation; issue recorded as environment noise | command output shows error after run completion |
| pytest unavailable | environment lacks pytest module | stdlib self-test added and used; pytest remains optional | `python scripts/self_test_agent_mode.py` pass; pytest reports missing module |

## Remaining Notes

- `agent_run_validation.json` has one warning, `empty_gap_report`, because no gaps remain. This is non-blocking.
- Original failed runs are preserved as evidence; successful live revalidation uses `TRAIN-20260603_TEXTONLY_STAGE_API_TOPICFIX_CODEX`.
- Formal workflow promotion remains suggestion-only and still requires human gate, contract validation, and stage-state control.
