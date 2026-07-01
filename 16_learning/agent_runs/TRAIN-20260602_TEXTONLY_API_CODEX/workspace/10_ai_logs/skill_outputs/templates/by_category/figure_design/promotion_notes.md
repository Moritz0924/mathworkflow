# 图表设计技能晋升说明

> 中文注释：用于 `figures` 阶段的 `nature-figure` 输出。晋升前必须确认图表绑定冻结结果或论断，并且图中所有可见文字为中文。

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
reason: <说明为什么该图表输出可以或不可以晋升>
```

## 4. 合同绑定

```text
required_bindings:
- figure_id
- result_id
- claim_id_or_section_id

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

## 6. 中文图表检查

正式图表、图片生成提示词和图表说明必须满足：

```text
figure_title_chinese: true | false | not_applicable
axis_labels_chinese: true | false | not_applicable
legend_chinese: true | false | not_applicable
annotations_chinese: true | false | not_applicable
node_text_chinese: true | false | not_applicable
image_prompt_requires_chinese_text: true | false | not_applicable
allowed_non_chinese: abbreviations | variable_names | metric_names | file_names | none
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
category: figure_design
allowed_skills: nature-figure
allowed_stages: figures
allowed_output_types: figure_blueprint, caption_candidate, visual_quality_review, chart_type_recommendation, figure_argument_note
required_bindings: figure_id, result_id, claim_id_or_section_id
promotion_targets: 08_figures/chart_blueprint.csv, 08_figures/figure_caption_bank.md, 08_figures/figure_design_review.csv
validation_expectations: registered_figure, result_bound, caption_supported, not_decorative_only, chinese_visible_text
```
