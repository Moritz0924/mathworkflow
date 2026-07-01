# 技能晋升说明

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
reason: <说明为什么该决定有效>
```

## 4. 合同绑定

```text
required_bindings:
- <claim_id | result_id | figure_id | formula_id | citation_id | reviewer_issue_id>

resolved_bindings:
- id: ""
  source_contract: ""
  status: missing | valid | invalid | not_required
```

## 5. 校验

```text
validation_status: not_run | passed | failed | waived
validation_commands:
- command: ""
  result: not_run | passed | failed
  notes: ""
```

## 6. 人工确认

```text
human_confirmation_required: false
human_decision_id: ""
human_decision: accept | accept_with_edits | reject | archive_only | retry_with_constraints | return_to_upstream_stage | waive_with_reason | not_required
```

## 7. 受保护事实原子检查

写作、润色、图表、引用和最终导出相关输出必须填写本节。所有面向评审或提交的最终内容必须为中文；图表、图片和 PPT 中的可见文字也必须为中文，必要英文缩写、变量名和文件名除外。

```text
numbers_preserved: true | false | not_applicable
formulas_preserved: true | false | not_applicable
labels_preserved: true | false | not_applicable
references_preserved: true | false | not_applicable
citations_preserved: true | false | not_applicable
model_names_preserved: true | false | not_applicable
result_meanings_preserved: true | false | not_applicable
chinese_output_checked: true | false | not_applicable
visible_image_text_chinese: true | false | not_applicable
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
