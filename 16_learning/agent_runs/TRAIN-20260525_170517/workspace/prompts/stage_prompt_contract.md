# Stage Prompt Contract v0.1

## 0. Purpose

This document standardizes how every stage prompt in the math modeling workflow must be written and executed.

The goal is not to make the agent more verbose. The goal is to make every stage output:

```text
traceable
reviewable
contract-bound
recoverable
human-controllable
```

A stage prompt is valid only if it clearly defines:

```text
inputs
outputs
permissions
contract updates
validation commands
human confirmation questions
failure recovery strategy
```

This contract is the P0 foundation for later P1 Skill Router, P3 Auto Review, P4 Result Contract, P5 Claim-bound Writing, and P6 Figure Contract strengthening.

---

## 1. Authority Order

When a stage prompt conflicts with another instruction, follow this order:

```text
1. Human final decision or explicit task packet
2. AGENTS.md
3. workflow_state.yaml and config/execution_policy.yaml
4. prompts/stage_prompt_contract.md
5. current prompts/stages/<stage>.md
6. specialist skill instructions
7. prior database notes
8. free-form agent suggestions
```

No stage prompt may weaken higher-level rules.

---

## 2. Global Execution Rules

All stage prompts must obey these rules:

```text
- Use deep_sequential mode only.
- Do not skip locked stages.
- Do not run multiple workflow stages in parallel.
- Do not generate full paper text before result and claim contracts exist.
- Do not invent numerical results, citations, figure files, formulas, or data fields.
- Do not copy text from prior papers or prior solutions.
- Do not delete contracts, logs, or review files to make validation pass.
- Do not allow reviewer prompts to directly edit deliverables.
- Do not allow polishing prompts to change numbers, formulas, labels, citations, model names, or result meanings.
```

---

## 3. Stage Prompt Required Schema

Each file under `prompts/stages/` must contain the following sections.

### 3.1 Stage Identity

Required fields:

```yaml
stage_id: <workflow stage id>
stage_name: <human readable name>
stage_order: <integer>
roadmap_item: P0
controller: workflow_state.yaml
execution_mode: deep_sequential
```

### 3.2 Objective

Must answer:

```text
What decision or artifact does this stage produce?
Why does it exist in the workflow?
What downstream stage depends on it?
```

### 3.3 Inputs

Must separate:

```text
required_inputs: must exist before the stage can run
optional_inputs: useful but not mandatory
human_inputs: questions that may require human answer
```

### 3.4 Allowed Read Paths

List exact paths or path groups the stage may inspect.

Example:

```text
00_problem/
03_data/raw/
14_contracts/result_contract.csv
```

### 3.5 Allowed Write Paths

List exact paths or path groups the stage may create or modify.

A stage must not write outside its allowed paths unless a later task packet explicitly authorizes it.

### 3.6 Forbidden Actions

Every stage must include local forbidden actions in addition to the global forbidden actions.

Example:

```text
- Do not edit frozen result rows.
- Do not create paper claims without claim_id.
- Do not cite a figure that is not registered in figure_contract.csv.
```

### 3.7 Required Outputs

Must define minimum deliverables.

Use concrete file names whenever possible.

### 3.8 Contract Updates

Must state:

```text
which contract files may be updated
which rows or fields are expected
which contract files are read-only at this stage
```

A formal claim, result, figure, formula, citation, frozen artifact, polish diff, or revision task must eventually have a contract row.

### 3.9 Skill Permissions

Must state allowed specialist skills for this stage.

If no skill is allowed, write:

```text
allowed_skills: none
```

Skill output is advisory unless it is entered into the appropriate contract and passes validation.

### 3.10 Validation Commands

Must include exact commands.

If a command is planned but does not exist yet, mark it explicitly:

```text
status: planned, not implemented
```

Do not claim a command passed unless it was actually run.

### 3.11 Human Confirmation Question

Every stage must include one concise human-facing question.

For non-gate stages, the question may be optional.

For gate stages, the question must require an explicit answer.

### 3.12 Failure Recovery

Every stage must define:

```text
common failure
likely cause
safe recovery action
rollback boundary
when to ask human
```

### 3.13 Completion Definition

Must define a clear `done_when` checklist.

A stage is not complete just because a document exists.

---

## 4. Standard Prompt Skeleton

Use this skeleton when adding a new stage prompt.

````markdown
# Stage Prompt: <stage_id> — <stage_name>

## 1. Stage Identity

```yaml
stage_id: <stage_id>
stage_name: <stage_name>
stage_order: <integer>
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. Objective

<Define the stage purpose in 3 to 6 lines.>

## 3. Required Inputs

```text
- <path or human input>
```

## 4. Optional Inputs

```text
- <path or human input>
```

## 5. Allowed Read Paths

```text
- <path>
```

## 6. Allowed Write Paths

```text
- <path>
```

## 7. Forbidden Actions

```text
- <action>
```

## 8. Required Outputs

```text
- <path>: <purpose>
```

## 9. Contract Updates

```text
may_update:
- <contract path or none>

read_only:
- <contract path or none>

required_fields:
- <field or none>
```

## 10. Allowed Skills

```text
- <skill name or none>
```

## 11. Agent Prompt Template

```text
You are executing stage <stage_id> in the v3.2-MVP contract-driven mathematical modeling workflow.

Goal:
<goal>

Use only the allowed inputs and write only to allowed outputs.

Before writing, check:
1. required inputs exist
2. current stage matches workflow_state.yaml
3. no forbidden action is needed

Produce:
1. required outputs
2. stage summary
3. risk report
4. contract update notes
5. validation command results or planned validation notes
6. human confirmation question
```

## 12. Validation Commands

```bash
<command>
```

## 13. Human Confirmation Question

```text
<question>
```

## 14. Failure Recovery

| Failure | Likely Cause | Safe Recovery | Rollback Boundary | Human Needed |
|---|---|---|---|---|
| ... | ... | ... | ... | yes/no |

## 15. Done When

```text
- <condition>
```
````

---

## 5. Stage Gate Types

### 5.1 Soft Gate

The stage may continue after recording warnings.

Examples:

```text
intake
eda
task_analysis
prior_retrieval
```

### 5.2 Hard Gate

The stage must pause for explicit human confirmation.

Current hard gates:

```text
model_route
results_freeze
paper_full
revision
compile
```

### 5.3 Validation Gate

The stage must pass a script check before downstream use.

Examples:

```text
figures
paper_draft
auto_review
polish
final_export
```

---

## 6. Contract Authority Rules

### 6.1 Result Authority

```text
Raw data and executed code output
→ result_contract.csv
→ figure_contract.csv / claim_evidence_map.csv
→ paper text
```

Paper text must not override results.

### 6.2 Claim Authority

A paper claim is valid only when supported by at least one of:

```text
result_id
figure_id
formula_id
citation_id
```

Unsupported claims should be written into a missing evidence report, not into final paper text.

### 6.3 Figure Authority

A figure is paper-eligible only when:

```text
figure_id exists
result_id or evidence_source exists
output file exists
quality_score passes threshold
latex_label exists if used in paper
caption_source is traceable
```

### 6.4 Polish Authority

Polish may improve wording only.

Protected atoms include:

```text
numbers
units
formulas
labels
references
citations
model names
result meanings
```

Any protected atom change must be blocked unless explicitly authorized by human task packet.

---

## 7. Standard Stage Report Block

Every stage output should end with this block:

```markdown
## Stage Summary

- stage_id:
- status: completed / blocked / needs_human / failed
- files_read:
- files_written:
- contracts_updated:
- validation_commands_run:
- validation_result:
- unresolved_risks:
- human_confirmation_required:
- next_stage_candidate:
```

---

## 8. Rollback Rule

Rollback must never delete user data, raw data, frozen results, or historical logs.

Safe rollback scope is limited to files created by the current stage unless the human explicitly authorizes a broader rollback.

---

## 9. Maintenance Rule

When a stage prompt changes, update:

```text
CHANGELOG_AI.md
TASK_PACKET.md if the active task changes
DECISIONS.md if the change affects long-term architecture
```

Do not silently modify stage permissions.
