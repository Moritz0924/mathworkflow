# Stage Prompt: results_freeze - Result Freeze

## 1. Stage Identity

```yaml
stage_id: results_freeze
stage_name: Result Freeze
stage_order: 7
gate_type: hard
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. Objective

Promote verified code outputs into frozen result rows, making result_contract the highest structured source for paper numbers.

## 3. Required Inputs

```text
- 07_results/q*_results.csv or metrics_summary.csv
- 06_code/execution_log.md
- 14_contracts/result_contract.csv
```

## 4. Optional Inputs

```text
- human notes
- prior stage risk report
- relevant files explicitly named in TASK_PACKET.md
```

## 5. Allowed Read Paths

```text
- 06_code/
- 07_results/
- 05_model/
- 14_contracts/result_contract.csv
```

## 6. Allowed Write Paths

```text
- 07_results/result_freeze_report.md
- 14_contracts/result_contract.csv
- 14_contracts/artifact_freeze_registry.csv
- 10_ai_logs/
```

## 7. Forbidden Actions

```text
- Do not violate AGENTS.md or config/execution_policy.yaml.
- Do not write outside the allowed write paths.
- Do not invent data, results, citations, formulas, figures, or human approvals.
- Do not delete contracts, logs, or review files to make validation pass.
```

## 8. Required Outputs

```text
- stage-specific artifacts listed in Allowed Write Paths
- stage summary block
- risk report
- contract update notes
- validation status notes
```

## 9. Contract Updates

```text
may_update: result_contract.csv; artifact_freeze_registry.csv | read_only: figure_contract.csv; claim_evidence_map.csv
```

## 10. Allowed Skills

```text
- none
```

Skill output is advisory until it is written to an allowed output, bound to contracts when applicable, and passes validation.

## 11. Agent Prompt Template

```text
You are executing stage results_freeze in the v3.2-MVP contract-driven mathematical modeling workflow.

Goal:
Promote verified code outputs into frozen result rows, making result_contract the highest structured source for paper numbers.

Use only allowed read paths and allowed write paths from this file.

Before writing:
1. Check required inputs.
2. Check workflow_state.yaml stage compatibility or explicit task-packet authorization.
3. Check relevant contract requirements.
4. Refuse any action listed in Forbidden Actions.

Produce:
1. Required stage artifacts.
2. Contract update notes.
3. Validation command results or planned validation notes.
4. Risk report.
5. Human confirmation question.
6. Standard Stage Summary block.
```

## 12. Validation Commands

```bash
python scripts/validate_contracts.py --stage figures
```
```bash
python scripts/check_gates.py --dev-debug
```

## 13. Human Confirmation Question

```text
Do you approve freezing these numerical results as the only paper-eligible result source?
```

## 14. Failure Recovery

| Failure Pattern | Safe Recovery |
|---|---|
| Missing provenance | keep row draft. Human rejects -> mark blocked and return upstream. |
| Required input missing | Record the missing input, do not infer it, and ask human if it blocks downstream work. |
| Validation command unavailable | Mark as planned or not implemented. Do not claim it passed. |
| Contract conflict | Preserve the contract, report the conflict, and return to the upstream stage that owns the contract. |

## 15. Done When

```text
- Required outputs exist or blockers are explicitly recorded.
- Contract update notes are consistent with allowed permissions.
- Validation commands are run, or not-run status is honestly recorded.
- Human confirmation question is present.
- No forbidden action was required to complete the stage.
```
