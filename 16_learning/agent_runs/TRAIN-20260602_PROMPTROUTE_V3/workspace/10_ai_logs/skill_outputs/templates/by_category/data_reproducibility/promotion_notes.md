# 数据可复现性技能晋升说明

> 中文注释：用于数据相关阶段或任务的 `nature-data` 输出。晋升前必须确认数据说明、限制说明和可复现性说明为中文；文件名、字段名和单位符号可按原样保留。

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
reason: <说明为什么该数据说明可以或不可以晋升>
```

## 3. 中文与数据来源检查

```text
data_notes_chinese: true | false | not_applicable
limitation_notes_chinese: true | false | not_applicable
reproducibility_notes_chinese: true | false | not_applicable
data_source_verified: true | false | not_applicable
fabricated_data_claim: false
```

## 4. 合同绑定

```text
required_bindings:
- data_source_id | dataset_id | section_id

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
category: data_reproducibility
allowed_skills: nature-data
allowed_stages: data, eda, paper_draft
allowed_output_types: data_quality_note, reproducibility_note, data_limitation_note, data_source_risk_note
required_bindings: data_source_id_or_dataset_id_or_section_id
promotion_targets: 03_data/, 14_contracts/data_contract.yaml, 09_paper/
validation_expectations: no_fabricated_data, chinese_data_explanation
```
