# Contract validation report

- stage: final_export
- fail_count: 12
- warn_count: 6

- [fail] figure_without_result_source (14_contracts/figure_contract.csv): F001 has neither result_id nor evidence_source
- [fail] figure_without_result_source (14_contracts/figure_contract.csv): F002 has neither result_id nor evidence_source
- [fail] figure_without_result_source (14_contracts/figure_contract.csv): F003 has neither result_id nor evidence_source
- [fail] figure_without_result_source (14_contracts/figure_contract.csv): F004 has neither result_id nor evidence_source
- [fail] figure_without_result_source (14_contracts/figure_contract.csv): F005 has neither result_id nor evidence_source
- [fail] figure_without_result_source (14_contracts/figure_contract.csv): F006 has neither result_id nor evidence_source
- [fail] figure_without_result_source (14_contracts/figure_contract.csv): F007 has neither result_id nor evidence_source
- [warn] claim_support_grade_missing (14_contracts/claim_evidence_map.csv): C001 support_grade=<empty>
- [warn] claim_support_grade_missing (14_contracts/claim_evidence_map.csv): C002 support_grade=<empty>
- [warn] claim_support_grade_missing (14_contracts/claim_evidence_map.csv): C003 support_grade=<empty>
- [warn] claim_support_grade_missing (14_contracts/claim_evidence_map.csv): C004 support_grade=<empty>
- [warn] claim_support_grade_missing (14_contracts/claim_evidence_map.csv): C005 support_grade=<empty>
- [warn] frozen_artifact_hash_missing (14_contracts/artifact_freeze_registry.csv): ART001 has no hash_sha256
- [fail] review_score_below_threshold (11_review/review_scorecard.csv): row 2: 0.0 < 85.0
- [fail] review_score_below_threshold (11_review/review_scorecard.csv): row 3: 0.0 < 85.0
- [fail] review_score_below_threshold (11_review/review_scorecard.csv): row 4: 0.0 < 85.0
- [fail] review_score_below_threshold (11_review/review_scorecard.csv): row 5: 0.0 < 85.0
- [fail] review_score_below_threshold (11_review/review_scorecard.csv): row 6: 0.0 < 85.0
