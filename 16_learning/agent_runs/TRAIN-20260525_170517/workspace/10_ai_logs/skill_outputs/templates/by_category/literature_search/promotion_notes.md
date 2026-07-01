# Skill Promotion Notes

## 1. Call identity

```text
call_id: SKILL-<stage_id>-<skill_id>-<YYYYMMDDTHHMMSSZ>
stage_id: <stage_id>
skill_id: <skill_id>
permission_level: advisory | contract_suggest | draft_assist | post_final
output_type: <registered_output_type>
```

## 2. Archive status

```text
input_manifest: input_manifest.yaml
raw_output: raw_output.md
archive_complete: false
```

## 3. Promotion decision

```text
promotion_decision: archive_only | promote | promote_with_edits | reject | retry_required
promotion_target: <target path or archive_only>
reason: <why this decision is valid>
```

## 4. Contract bindings

```text
required_bindings:
- <claim_id | result_id | figure_id | formula_id | citation_id | reviewer_issue_id>

resolved_bindings:
- id: ""
  source_contract: ""
  status: missing | valid | invalid | not_required
```

## 5. Validation

```text
validation_status: not_run | passed | failed | waived
validation_commands:
- command: ""
  result: not_run | passed | failed
  notes: ""
```

## 6. Human confirmation

```text
human_confirmation_required: false
human_decision_id: ""
human_decision: accept | accept_with_edits | reject | archive_only | retry_with_constraints | return_to_upstream_stage | waive_with_reason | not_required
```

## 7. Protected atoms check

Use this section for writing, polish, figures, citations, and final export.

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

## 8. Failure handling

```text
failure_code: NONE | SKILL_NOT_INSTALLED | UNKNOWN_SKILL | STAGE_NOT_ALLOWED | LEGACY_STAGE_NAME | REQUIRED_INPUT_MISSING | CONTRACT_MISSING | CONTRACT_INVALID | OUTPUT_PATH_VIOLATION | FABRICATED_DATA_OR_RESULT | FABRICATED_CITATION | PRIOR_COPY_RISK | PROTECTED_ATOM_CHANGED | VALIDATION_FAILED | HUMAN_CONFIRMATION_REQUIRED | UNKNOWN_SKILL_OUTPUT
fallback_action: none | archive_output_as_advisory_only | retry_once_with_stronger_constraints_if_safe | skip_optional_skill | create_stage_blocker_note | create_revision_task_if_downstream_impact_exists | ask_human_if_decision_cannot_be_recovered_safely
```

## 9. Final note

```text
promotion_ready: false
next_required_action: <one concrete next action>
```

## 10. Category-specific checks

```text
category: literature_search
allowed_skills: nature-academic-search
allowed_stages: paper_draft
allowed_output_types: search_query_plan, candidate_paper_list, search_gap_report
required_bindings: claim_id_or_section_id_when_search_fills_a_gap
promotion_targets: 02_literature/search_queries.csv, 02_literature/raw_search_results.csv, 02_literature/citation_gap_report.md
validation_expectations: no_fabricated_reference, query_scope_matches_claim_gap
```
