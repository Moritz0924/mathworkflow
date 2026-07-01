# Stage Prompt: auto_review - Multi-reviewer Auto Review

## 1. Stage Identity

```yaml
stage_id: auto_review
stage_name: Multi-reviewer Auto Review
stage_order: 11
gate_type: validation
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. Objective

Generate structured reviewer comments, scorecards, and revision tasks without directly editing deliverables.

## 3. Required Inputs

```text
- 09_paper/full_draft.tex or .md
- claim_evidence_map.csv
- result_contract.csv
```

## 4. Optional Inputs

```text
- human notes
- prior stage risk report
- relevant files explicitly named in TASK_PACKET.md
```

## 5. Allowed Read Paths

```text
- 09_paper/
- 05_model/
- 06_code/
- 07_results/
- 08_figures/
- 14_contracts/
- 11_review/
```

## 6. Allowed Write Paths

```text
- 11_review/*_reviewer_comments.md
- 11_review/review_scorecard.csv
- 14_contracts/revision_tasks.csv
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
may_update: revision_tasks.csv | read_only: deliverables and core contracts
```

## 10. Allowed Skills

```text
- nature-response
```

Skill output is advisory until it is written to an allowed output, bound to contracts when applicable, and passes validation.

## 11. Agent Prompt Template

```text
You are executing stage auto_review in the v3.2-MVP contract-driven mathematical modeling workflow.

Goal:
Generate structured reviewer comments, scorecards, and revision tasks without directly editing deliverables.

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
python scripts/validate_contracts.py --stage auto_review
```
```bash
python scripts/check_gates.py --dev-debug
```

## 13. Human Confirmation Question

```text
Which reviewer issues are mandatory, optional, or waived before revision begins?
```

## 14. Failure Recovery

| Failure Pattern | Safe Recovery |
|---|---|
| Free-form comment | convert to task. Direct edit proposal -> reject and rewrite as task. |
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
