# 文献检索技能晋升说明

> 中文注释：用于文献检索相关阶段或任务的 `nature-academic-search` 输出。晋升前必须确认检索计划、候选文献说明和缺口报告为中文；文献标题、DOI、期刊名等原始元数据可保留原文。

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
reason: <说明为什么该检索输出可以或不可以晋升>
```

## 3. 合同绑定

```text
required_bindings:
- citation_id | claim_id | section_id

resolved_bindings:
- id: ""
  source_contract: ""
  status: missing | valid | invalid | not_required
```

## 4. 校验与中文检查

```text
validation_status: not_run | passed | failed | waived
search_notes_chinese: true | false | not_applicable
gap_report_chinese: true | false | not_applicable
metadata_original_language_allowed: true
fabricated_citation_check: passed | failed | not_run
```

## 5. 失败处理

```text
failure_code: NONE | SKILL_NOT_INSTALLED | UNKNOWN_SKILL | STAGE_NOT_ALLOWED | LEGACY_STAGE_NAME | REQUIRED_INPUT_MISSING | CONTRACT_MISSING | CONTRACT_INVALID | OUTPUT_PATH_VIOLATION | FABRICATED_DATA_OR_RESULT | FABRICATED_CITATION | PRIOR_COPY_RISK | PROTECTED_ATOM_CHANGED | VALIDATION_FAILED | HUMAN_CONFIRMATION_REQUIRED | UNKNOWN_SKILL_OUTPUT
fallback_action: none | archive_output_as_advisory_only | retry_once_with_stronger_constraints_if_safe | skip_optional_skill | create_stage_blocker_note | create_revision_task_if_downstream_impact_exists | ask_human_if_decision_cannot_be_recovered_safely
```

## 6. 最终说明

```text
promotion_ready: false
next_required_action: <一个具体下一步>
```

## 7. 类别专用检查

```text
category: literature_search
allowed_skills: nature-academic-search
allowed_stages: literature
allowed_output_types: search_query_plan, candidate_paper_list, search_gap_report
required_bindings: citation_id_or_section_id
promotion_targets: 02_literature/
validation_expectations: no_fabricated_metadata, chinese_explanatory_notes
```
