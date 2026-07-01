# Stage Prompt: paper_draft - Section-level Paper Draft

## 1. Stage Identity

```yaml
stage_id: paper_draft
stage_name: Section-level Paper Draft
stage_order: 9
gate_type: validation
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. Objective

Draft one section at a time from registered claims, results, formulas, figures, and citations.

## 3. Required Inputs

```text
- claim_evidence_map.csv
- result_contract.csv
- figure_contract.csv
- formula_contract.csv
- citation_contract.csv
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
- 02_latex_template/sections/
- 05_model/
- 07_results/
- 08_figures/
- 14_contracts/
```

## 6. Allowed Write Paths

```text
- 09_paper/sections/
- 09_paper/section_generation_plan.csv
- 09_paper/section_claims.csv
- 09_paper/missing_evidence_report.md
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
may_update: claim_evidence_map.csv draft rows only | read_only: result_contract.csv; figure_contract.csv; formula_contract.csv; citation_contract.csv
```

## 10. Allowed Skills

```text
- nature-writing
```

Skill output is advisory until it is written to an allowed output, bound to contracts when applicable, and passes validation.

## 11. Agent Prompt Template

```text
You are executing stage paper_draft in the v3.2-MVP contract-driven mathematical modeling workflow.

Goal:
Draft one section at a time from registered claims, results, formulas, figures, and citations.

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
python scripts/validate_contracts.py --stage paper_draft
```
```bash
python scripts/generate_paper_sections.py --section current --mode deep
```
```bash
python scripts/check_gates.py --dev-debug
```

## 13. Human Confirmation Question

```text
Are any important claims missing evidence and therefore unsafe to include?
```

## 14. Failure Recovery

| Failure Pattern | Safe Recovery |
|---|---|
| Missing evidence | report it instead of writing claim. Contract mismatch -> remove reference and repair upstream. |
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
