# Stage Prompt: model_route - Model Family Routing

## 1. Stage Identity

```yaml
stage_id: model_route
stage_name: Model Family Routing
stage_order: 5
gate_type: hard
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. Objective

Select model families and fallback approaches for each subquestion using feasibility, data state, and scoring risk.

## 3. Required Inputs

```text
- 01_task_analysis/problem_model_profile.csv
- task_decomposition.md
- 05_model/model_family_weight_config.csv
```

## 4. Optional Inputs

```text
- human notes
- prior stage risk report
- relevant files explicitly named in TASK_PACKET.md
```

## 5. Allowed Read Paths

```text
- 01_task_analysis/
- 04_eda/
- 05_model/
- 13_prior_db/
- config/
```

## 6. Allowed Write Paths

```text
- 05_model/model_route.md
- 05_model/question_dependency_map.md
- 05_model/fallback_plan.md
- 05_model/model_freeze.md
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
may_update: formula_contract.csv draft rows only | read_only: result_contract.csv; figure_contract.csv; claim_evidence_map.csv
```

## 10. Allowed Skills

```text
- none
```

Skill output is advisory until it is written to an allowed output, bound to contracts when applicable, and passes validation.

## 11. Agent Prompt Template

```text
You are executing stage model_route in the v3.2-MVP contract-driven mathematical modeling workflow.

Goal:
Select model families and fallback approaches for each subquestion using feasibility, data state, and scoring risk.

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
python scripts/route_weight_config.py
```
```bash
python scripts/check_gates.py --dev-debug
```

## 13. Human Confirmation Question

```text
Do you approve the selected model family and fallback plan for each subquestion?
```

## 14. Failure Recovery

| Failure Pattern | Safe Recovery |
|---|---|
| Top model infeasible | switch to fallback. Similar candidates -> create comparison and ask human. |
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
