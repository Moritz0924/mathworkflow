# 终稿后展示材料晋升说明

> 中文注释：用于 `final_export` 阶段的 `nature-paper2ppt` 输出。晋升前必须确认 PPT、图片、图表和所有可见文字均为中文，并且只来源于已批准论文。

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
reason: <说明为什么该展示材料可以或不可以晋升>
```

## 4. 来源与合同绑定

```text
required_bindings:
- final_paper_id_or_artifact_id

resolved_bindings:
- id: ""
  source_contract: ""
  status: missing | valid | invalid | not_required
```

## 5. 中文展示检查

```text
slide_text_chinese: true | false | not_applicable
image_text_chinese: true | false | not_applicable
chart_text_chinese: true | false | not_applicable
speaker_notes_chinese: true | false | not_applicable
image_prompt_requires_chinese_text: true | false | not_applicable
allowed_non_chinese: abbreviations | variable_names | metric_names | file_names | none
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
category: post_final_presentation
allowed_skills: nature-paper2ppt
allowed_stages: final_export
allowed_output_types: presentation_outline, slide_draft, defense_talking_points
required_bindings: final_paper_id_or_artifact_id
promotion_targets: 12_export/pptx/
validation_expectations: post_final_only, based_on_approved_paper, no_new_results, chinese_visible_text
```
