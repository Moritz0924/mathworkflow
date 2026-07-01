# Stage Prompt: codegen - Question-level Code Generation

## 1. Stage Identity

```yaml
stage_id: codegen
stage_name: Question-level Code Generation
stage_order: 6
gate_type: validation
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. Objective

Generate and run reproducible solving code one question at a time, producing candidate result files.

## 3. Required Inputs

```text
- 05_model/model_route.md
- q*_model.md or selected model spec
- data or no-data mode
```

## 4. Optional Inputs

```text
- human notes
- prior stage risk report
- relevant files explicitly named in TASK_PACKET.md
```

## 5. Allowed Read Paths

```text
- 03_data/
- 04_eda/
- 05_model/
- 06_code/
- 06_solution_code/
- config/
```

## 6. Allowed Write Paths

```text
- 06_code/src/
- 06_code/notebooks/
- 06_code/run_all.py
- 06_code/execution_log.md
- 07_results/
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
may_update: result_contract.csv draft rows after code output exists | read_only: figure_contract.csv; claim_evidence_map.csv
```

## 10. Allowed Skills

```text
- none
```

Skill output is advisory until it is written to an allowed output, bound to contracts when applicable, and passes validation.

## 11. Agent Prompt Template

```text
You are executing stage codegen in the v3.2-MVP contract-driven mathematical modeling workflow.

Goal:
Generate and run reproducible solving code one question at a time, producing candidate result files.

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
python scripts/generate_model_code.py --question Q1 --mode deep
```
```bash
python 06_code/run_all.py
```
```bash
python scripts/validate_contracts.py --stage figures
```

## 13. Human Confirmation Question

```text
Does the generated code implement the approved model rather than a convenient shortcut?
```

## 14. Failure Recovery

| Failure Pattern | Safe Recovery |
|---|---|
| Execution fail | fix current question code only. Output not credible -> return to model_route or codegen with risk note. |
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
