# Stage Prompt: final_export - Final Export and Optional PPT

## 1. Stage Identity

```yaml
stage_id: final_export
stage_name: Final Export and Optional PPT
stage_order: 15
gate_type: validation
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. Objective

Package final approved deliverables and optionally create slides derived only from the approved paper.

## 3. Required Inputs

```text
- 12_submission/final paper package
- human final gate approval
- gate_report.json
```

## 4. Optional Inputs

```text
- human notes
- prior stage risk report
- relevant files explicitly named in TASK_PACKET.md
```

## 5. Allowed Read Paths

```text
- 12_submission/
- 09_paper/
- 08_figures/
- 14_contracts/
- 11_review/
```

## 6. Allowed Write Paths

```text
- 12_export/
- 12_export/pptx/
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
may_update: none | read_only: 14_contracts/*.csv; 09_paper/; 12_submission/
```

## 10. Allowed Skills

```text
- nature-paper2ppt
```

Skill output is advisory until it is written to an allowed output, bound to contracts when applicable, and passes validation.

## 11. Agent Prompt Template

```text
You are executing stage final_export in the v3.2-MVP contract-driven mathematical modeling workflow.

Goal:
Package final approved deliverables and optionally create slides derived only from the approved paper.

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
python scripts/validate_contracts.py --stage final_export
```
```bash
python scripts/check_gates.py
```

## 13. Human Confirmation Question

```text
Do you want a post-final presentation deck generated from the approved paper only?
```

## 14. Failure Recovery

| Failure Pattern | Safe Recovery |
|---|---|
| Package missing | return to compile. Slide invents claim -> delete unsupported content and regenerate from paper only. |
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
