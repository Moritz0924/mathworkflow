# Contract validation report

- stage: final_export
- fail_count: 18
- warn_count: 5

- [fail] figure_without_result_source (14_contracts/figure_contract.csv): figF002 has neither result_id nor evidence_source
- [fail] citation_without_support_grade (14_contracts/citation_contract.csv): B01 support_grade=<empty>
- [fail] citation_metadata_unverified (14_contracts/citation_contract.csv): B01 metadata_verified is not true
- [fail] citation_without_support_grade (14_contracts/citation_contract.csv): B02 support_grade=<empty>
- [fail] citation_metadata_unverified (14_contracts/citation_contract.csv): B02 metadata_verified is not true
- [fail] citation_without_support_grade (14_contracts/citation_contract.csv): B03 support_grade=<empty>
- [fail] citation_metadata_unverified (14_contracts/citation_contract.csv): B03 metadata_verified is not true
- [fail] citation_without_support_grade (14_contracts/citation_contract.csv): B04 support_grade=<empty>
- [fail] citation_metadata_unverified (14_contracts/citation_contract.csv): B04 metadata_verified is not true
- [fail] citation_without_support_grade (14_contracts/citation_contract.csv): B05 support_grade=<empty>
- [fail] citation_metadata_unverified (14_contracts/citation_contract.csv): B05 metadata_verified is not true
- [warn] claim_support_grade_missing (14_contracts/claim_evidence_map.csv): C001 support_grade=<empty>
- [fail] unsupported_claim (14_contracts/claim_evidence_map.csv): C002 support_grade=<empty>
- [warn] claim_support_grade_missing (14_contracts/claim_evidence_map.csv): C003 support_grade=<empty>
- [warn] claim_support_grade_missing (14_contracts/claim_evidence_map.csv): C004 support_grade=<empty>
- [fail] unsupported_claim (14_contracts/claim_evidence_map.csv): C005 support_grade=<empty>
- [fail] unsupported_claim (14_contracts/claim_evidence_map.csv): C006 support_grade=<empty>
- [warn] claim_support_grade_missing (14_contracts/claim_evidence_map.csv): C007 support_grade=<empty>
- [warn] claim_support_grade_missing (14_contracts/claim_evidence_map.csv): C008 support_grade=<empty>
- [fail] review_score_below_threshold (11_review/review_scorecard.csv): row 5: 80.0 < 85.0
- [fail] review_score_below_threshold (11_review/review_scorecard.csv): row 6: 80.0 < 85.0
- [fail] review_score_below_threshold (11_review/review_scorecard.csv): row 9: 80.0 < 85.0
- [fail] review_score_below_threshold (11_review/review_scorecard.csv): row 10: 70.0 < 85.0
