{
  "status": "blocked",
  "summary": "Results freeze blocked: no model outputs in 07_results/ and no execution logs in 06_code/. Created empty contract tables and freeze report. Gate logged as pending.",
  "files": [
    {
      "path": "07_results/result_freeze_report.md",
      "operation": "write",
      "content": "# Result Freeze Report\n\n**Stage:** results_freeze  \n**Date:** 2025-06-04 (simulated)  \n**Status:** BLOCKED — No model outputs available for freezing.\n\n## 1. Input Verification\n- `07_results/`: No model output files found.\n- `06_code/`: No execution logs found.\n- `14_contracts/result_contract.csv`: Table header only (created below).\n\n## 2. Freeze Audit Table\nNo candidate results to audit. To populate this table, run `codegen` stage to generate model outputs and execution logs.\n\n| result_id | question_id | model_id | metric_name | metric_value | unit | source_file | source_row_or_cell | code_file | run_id | random_seed | freeze_status |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n| — | — | — | — | — | — | — | — | — | — | — | — |\n\n## 3. Risk Register\n- **Missing inputs:** `07_results/` and `06_code/` are empty or inaccessible; cannot proceed.\n- **Reproducibility:** Not evaluable.\n- **Human gate:** Not requested (stage blocked).\n\n## 4. Self-Check\n1. No result values were altered. ✓ (N/A)\n2. No unrun results were frozen. ✓\n3. Every paper-usable result has source_file, metric_name, metric_value. ✓ (N/A)\n4. Downstream reference fields reserved or explained. ✓ (pending)\n5. Validation commands run or recorded as not_run. (not run)\n\n## 5. Recommendation\nReturn to `codegen` stage to produce actionable model outputs and execution logs. Once available, re-run `results_freeze` with the outputs present.\n\n## 6. Artifact Freeze Registry\nSee `14_contracts/artifact_freeze_registry.csv`. No artifacts frozen.\n\n## 7. Human Gate\nSimulated sandbox gate — no formal effect. Logged in `11_review/simulated_human_gate_log.csv`.\n"
    },
    {
      "path": "14_contracts/result_contract.csv",
      "operation": "write",
      "content": "result_id,question_id,model_id,metric_name,metric_value,unit,source_file,source_row_or_cell,code_file,run_id,random_seed,freeze_status,used_by_claim_ids\n"
    },
    {
      "path": "14_contracts/artifact_freeze_registry.csv",
      "operation": "write",
      "content": "artifact_id,artifact_type,path,description,freeze_date,protected_atoms\n"
    },
    {
      "path": "11_review/simulated_human_gate_log.csv",
      "operation": "write",
      "content": "timestamp,gate,decision,reason,formal_effect\n2025-06-04T00:00:00,results_freeze_gate,PENDING,No results to freeze; blocked by missing inputs.,none\n"
    },
    {
      "path": "reports/training_enhancement_points.csv",
      "operation": "write",
      "content": "timestamp,stage,enhancement_id,description,severity,status\n2025-06-04T00:00:00,results_freeze,TE001,Early detection of missing required stage inputs could prevent pointless stage execution.,low,open\n"
    }
  ],
  "unresolved": [
    {
      "issue": "Missing required inputs for results_freeze stage.",
      "blocker": "07_results/ and 06_code/ directories are empty or contain no executable outputs. Cannot freeze any results. Need to run codegen stage first."
    }
  ]
}
