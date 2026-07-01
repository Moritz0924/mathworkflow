# 章节写作技能晋升说明

> 中文注释：用于 `paper_draft` 和 `paper_full` 阶段的 `nature-writing` 输出。晋升前必须确认正文、图注、表注和面向评审说明均为中文。

## 1. 调用身份

```text
call_id: SKILL-<stage_id>-<skill_id>-<YYYYMMDDTHHMMSSZ>
stage_id: <stage_id>
skill_id: <skill_id>
permission_level: advisory | contract_suggest | draft_assist | post_final
output_type: <registered_output_type>
```

## 2. 归档状态

```text
input_manifest: input_manifest.yaml
raw_output: raw_output.md
archive_complete: false
```

## 3. 晋升决定

```text
promotion_decision: archive_only | promote | promote_with_edits | reject | retry_required
promotion_target: <target path or archive_only>
reason: <说明为什么该写作输出可以或不可以晋升>
```

## 4. 合同绑定

```text
required_bindings:
- claim_id
- result_id | figure_id | formula_id | citation_id

resolved_bindings:
- id: ""
  source_contract: ""
  status: missing | valid | invalid | not_required
```

## 5. 中文写作检查

```text
body_text_chinese: true | false | not_applicable
figure_captions_chinese: true | false | not_applicable
table_captions_chinese: true | false | not_applicable
reviewer_facing_notes_chinese: true | false | not_applicable
allowed_non_chinese: abbreviations | variable_names | model_names | latex_commands | file_names | none
```

## 6. 校验

```text
validation_status: not_run | passed | failed | waived
validation_commands:
- command: ""
  result: not_run | passed | failed
  notes: ""
```

## 7. 受保护事实原子检查

```text
numbers_preserved: true | false | not_applicable
formulas_preserved: true | false | not_applicable
labels_preserved: true | false | not_applicable
references_preserved: true | false | not_applicable
citations_preserved: true | false | not_applicable
model_names_preserved: true | false | not_applicable
result_meanings_preserved: true | false | not_applicable
violations: []
```

## 8. 失败处理

```text
failure_code: NONE | SKILL_NOT_INSTALLED | UNKNOWN_SKILL | STAGE_NOT_ALLOWED | LEGACY_STAGE_NAME | REQUIRED_INPUT_MISSING | CONTRACT_MISSING | CONTRACT_INVALID | OUTPUT_PATH_VIOLATION | FABRICATED_DATA_OR_RESULT | FABRICATED_CITATION | PRIOR_COPY_RISK | PROTECTED_ATOM_CHANGED | VALIDATION_FAILED | HUMAN_CONFIRMATION_REQUIRED | UNKNOWN_SKILL_OUTPUT
fallback_action: none | archive_output_as_advisory_only | retry_once_with_stronger_constraints_if_safe | skip_optional_skill | create_stage_blocker_note | create_revision_task_if_downstream_impact_exists | ask_human_if_decision_cannot_be_recovered_safely
```

## 9. 最终说明

```text
promotion_ready: false
next_required_action: <一个具体下一步>
```

## 10. 类别专用检查

```text
category: section_writing
allowed_skills: nature-writing
allowed_stages: paper_draft, paper_full
allowed_output_types: section_draft, claim_rewrite, paragraph_structure, transition_suggestion, coherence_note
required_bindings: claim_id, evidence_id_or_result_id_or_figure_id_or_formula_id_or_citation_id
promotion_targets: 02_latex_template/sections/, 09_paper/
validation_expectations: evidence_bound, no_new_claims_without_contract, chinese_paper_text
```
