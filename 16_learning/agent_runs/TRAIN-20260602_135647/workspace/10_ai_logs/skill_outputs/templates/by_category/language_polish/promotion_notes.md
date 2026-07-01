# 语言润色技能晋升说明

> 中文注释：用于 `polish` 阶段的 `nature-polishing` 输出。晋升前必须确认润色结果仍为中文，且没有改变数字、公式、标签、引用、模型名或结果含义。

## 1. 调用身份

```text
call_id: SKILL-<stage_id>-<skill_id>-<YYYYMMDDTHHMMSSZ>
stage_id: <stage_id>
skill_id: <skill_id>
permission_level: advisory | contract_suggest | draft_assist | post_final
output_type: <registered_output_type>
```

## 2. 晋升决定

```text
promotion_decision: archive_only | promote | promote_with_edits | reject | retry_required
promotion_target: <target path or archive_only>
reason: <说明为什么该润色输出可以或不可以晋升>
```

## 3. 中文润色检查

```text
polished_text_chinese: true | false | not_applicable
figure_captions_chinese: true | false | not_applicable
table_captions_chinese: true | false | not_applicable
english_paragraph_introduced: false
allowed_non_chinese: abbreviations | variable_names | model_names | latex_commands | file_names | none
```

## 4. 受保护事实原子检查

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

## 5. 校验

```text
validation_status: not_run | passed | failed | waived
validation_commands:
- command: ""
  result: not_run | passed | failed
  notes: ""
```

## 6. 失败处理

```text
failure_code: NONE | SKILL_NOT_INSTALLED | UNKNOWN_SKILL | STAGE_NOT_ALLOWED | LEGACY_STAGE_NAME | REQUIRED_INPUT_MISSING | CONTRACT_MISSING | CONTRACT_INVALID | OUTPUT_PATH_VIOLATION | FABRICATED_DATA_OR_RESULT | FABRICATED_CITATION | PRIOR_COPY_RISK | PROTECTED_ATOM_CHANGED | VALIDATION_FAILED | HUMAN_CONFIRMATION_REQUIRED | UNKNOWN_SKILL_OUTPUT
fallback_action: none | archive_output_as_advisory_only | retry_once_with_stronger_constraints_if_safe | skip_optional_skill | create_stage_blocker_note | create_revision_task_if_downstream_impact_exists | ask_human_if_decision_cannot_be_recovered_safely
```

## 7. 最终说明

```text
promotion_ready: false
next_required_action: <一个具体下一步>
```

## 8. 类别专用检查

```text
category: language_polish
allowed_skills: nature-polishing
allowed_stages: polish
allowed_output_types: polish_diff, style_risk_note, readability_improvement, sentence_level_rewrite
required_bindings: artifact_id_or_section_id
promotion_targets: 02_latex_template/sections/, 10_polish/, 14_contracts/polish_diff_check.csv
validation_expectations: protected_atoms_preserved, chinese_polished_text
```
