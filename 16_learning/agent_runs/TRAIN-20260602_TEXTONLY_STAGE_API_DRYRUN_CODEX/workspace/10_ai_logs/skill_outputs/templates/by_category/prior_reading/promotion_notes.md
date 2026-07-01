# 先验阅读技能晋升说明

> 中文注释：用于 `prior_retrieval` 阶段的 `nature-reader` 输出。晋升前必须确认输出为中文经验卡片，且没有复制历史论文正文、摘要、图注、表格或结论。

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
reason: <说明为什么该先验输出可以或不可以晋升>
```

## 3. 中文与拷贝风险检查

```text
prior_card_chinese: true | false | not_applicable
copy_risk_checked: true | false | not_applicable
copied_source_text: false
contains_historical_conclusion_as_answer: false
allowed_use: problem_type_experience | model_family_hint | figure_type_hint | scoring_risk_hint
```

## 4. 合同或来源绑定

```text
required_bindings:
- source_id | prior_card_id | question_id

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
category: prior_reading
allowed_skills: nature-reader
allowed_stages: prior_retrieval
allowed_output_types: prior_card, model_family_hint, figure_type_hint, scoring_risk_hint, structure_gap_hint
required_bindings: source_id_or_prior_card_id_or_question_id
promotion_targets: 13_prior_db/
validation_expectations: advisory_only, no_prior_text_copy, chinese_prior_cards
```
