# 审稿回复技能晋升说明

> 中文注释：用于 `auto_review` 或 `revision` 阶段的 `nature-response` 输出。晋升前必须确认审稿意见、修订任务候选和关闭说明为中文，且不直接修改正式交付物。

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
reason: <说明为什么该审稿输出可以或不可以晋升>
```

## 4. 合同绑定

```text
required_bindings:
- reviewer_issue_id | task_id | claim_id | figure_id | result_id

resolved_bindings:
- id: ""
  source_contract: ""
  status: missing | valid | invalid | not_required
```

## 5. 校验与中文检查

```text
validation_status: not_run | passed | failed | waived
review_notes_chinese: true | false | not_applicable
revision_tasks_chinese: true | false | not_applicable
closure_notes_chinese: true | false | not_applicable
direct_deliverable_edit: false
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
category: review_response
allowed_skills: nature-response
allowed_stages: auto_review, revision
allowed_output_types: review_issue_triage, revision_task_candidate, reviewer_response_draft, closure_check_note
required_bindings: reviewer_issue_id_or_task_id
promotion_targets: 11_review/, 14_contracts/revision_tasks.csv
validation_expectations: task_traceable, no_direct_deliverable_edit, chinese_review_output
```
