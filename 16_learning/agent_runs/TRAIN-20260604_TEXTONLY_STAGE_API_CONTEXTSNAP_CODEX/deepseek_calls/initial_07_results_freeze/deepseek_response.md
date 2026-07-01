{
  "status": "ok",
  "summary": "Frozen six Q1 OLS coefficient and metric results from validated source files; other result files remain unfrozen pending content verification.",
  "files": [
    {
      "path": "14_contracts/result_contract.csv",
      "operation": "write",
      "content": "result_id,question_id,model_id,metric_name,metric_value,unit,source_file,source_row_or_cell,code_file,run_id,random_seed,assumption_ids,used_by_figure_ids,used_by_claim_ids,freeze_status,freeze_time,owner,notes\nR01,Q1,linear_OLS,coefficient_Intercept,1.067247,dimensionless,07_results/q1_coefficients.csv,row 1,06_code/q1_linear_model.py,run_001,deterministic,F01,,,frozen,2026-06-04T12:00:00Z,system,validated source value 1.067247 from q1_coefficients.csv row 1; OLS intercept coefficient\nR02,Q1,linear_OLS,coefficient_R,-1.821404,dimensionless,07_results/q1_coefficients.csv,row 2,06_code/q1_linear_model.py,run_001,deterministic,F01,,,frozen,2026-06-04T12:00:00Z,system,validated source value -1.821404 from q1_coefficients.csv row 2; R channel coefficient\nR03,Q1,linear_OLS,coefficient_G,0.995618,dimensionless,07_results/q1_coefficients.csv,row 3,06_code/q1_linear_model.py,run_001,deterministic,F01,,,frozen,2026-06-04T12:00:00Z,system,validated source value 0.995618 from q1_coefficients.csv row 3; G channel coefficient\nR04,Q1,linear_OLS,coefficient_B,5.630987,dimensionless,07_results/q1_coefficients.csv,row 4,06_code/q1_linear_model.py,run_001,deterministic,F01,,,frozen,2026-06-04T12:00:00Z,system,validated source value 5.630987 from q1_coefficients.csv row 4; B channel coefficient\nR05,Q1,linear_OLS,R_squared,0.997747,dimensionless,07_results/q1_metrics.csv,row 1,06_code/q1_linear_model.py,run_001,deterministic,F01,,,frozen,2026-06-04T12:00:00Z,system,validated source value 0.997747 from q1_metrics.csv row 1; OLS R-squared\nR06,Q1,linear_OLS,RMSE,0.067418,mg/L,07_results/q1_metrics.csv,row 2,06_code/q1_linear_model.py,run_001,deterministic,F01,,,frozen,2026-06-04T12:00:00Z,system,validated source value 0.067418 from q1_metrics.csv row 2; OLS RMSE\n"
    },
    {
      "path": "14_contracts/artifact_freeze_registry.csv",
      "operation": "write",
      "content": "artifact_id,artifact_type,linked_result_ids,protected_atoms,freeze_time,owner,notes\nAF01,result_contract_row,R01,coefficient_Intercept=1.067247,2026-06-04T12:00:00Z,system,Frozen from q1_coefficients.csv validated run_001\nAF02,result_contract_row,R02,coefficient_R=-1.821404,2026-06-04T12:00:00Z,system,Frozen from q1_coefficients.csv validated run_001\nAF03,result_contract_row,R03,coefficient_G=0.995618,2026-06-04T12:00:00Z,system,Frozen from q1_coefficients.csv validated run_001\nAF04,result_contract_row,R04,coefficient_B=5.630987,2026-06-04T12:00:00Z,system,Frozen from q1_coefficients.csv validated run_001\nAF05,result_contract_row,R05,R_squared=0.997747,2026-06-04T12:00:00Z,system,Frozen from q1_metrics.csv validated run_001\nAF06,result_contract_row,R06,RMSE=0.067418,2026-06-04T12:00:00Z,system,Frozen from q1_metrics.csv validated run_001\n"
    },
    {
      "path": "07_results/result_freeze_report.md",
      "operation": "write",
      "content": "# Results Freeze Report\n\n**Stage**: results_freeze  \n**Date**: 2026-06-04T12:00:00Z  \n**Execution**: deep_sequential, run_id=initial_07_results_freeze\n\n## Summary\n\n- Total candidate results reviewed: 6\n- Frozen: 6 (R01--R06)\n- Blocked / not frozen: other present result files (q1_results.csv, q2_results.csv, q3_results.csv, metrics_summary.csv) require content verification before freezing.\n\n## Frozen Results\n\nAll frozen results originate from validated model runs (`run_001`) using code `06_code/q1_linear_model.py` with deterministic random seed. Source files were read and values matched the contract entries.\n\n| result_id | metric_name | metric_value | source_file | validation |\n|-----------|-------------|--------------|-------------|-------------|\n| R01 | coefficient_Intercept | 1.067247 | 07_results/q1_coefficients.csv | row 1 matched |\n| R02 | coefficient_R | -1.821404 | 07_results/q1_coefficients.csv | row 2 matched |\n| R03 | coefficient_G | 0.995618 | 07_results/q1_coefficients.csv | row 3 matched |\n| R04 | coefficient_B | 5.630987 | 07_results/q1_coefficients.csv | row 4 matched |\n| R05 | R_squared | 0.997747 | 07_results/q1_metrics.csv | row 1 matched |\n| R06 | RMSE | 0.067418 | 07_results/q1_metrics.csv | row 2 matched |\n\n## Unfrozen or Unverified Results\n\nThe following files exist under `07_results/` but their contents have not been verified and therefore are not frozen:\n\n- `07_results/q1_results.csv` — likely contains predicted concentration values for standard samples; contents unread.\n- `07_results/q2_results.csv` — expected to hold model comparison metrics for Q2; contents unread.\n- `07_results/q3_results.csv` — expected to hold concentration predictions and uncertainty for T01--T03; contents unread.\n- `07_results/metrics_summary.csv` — likely aggregated metrics across models; contents unread.\n\nThese files should be reviewed against run logs (`07_results/logs/q1_run.log` and others) and, if correct, promoted to result contract rows before figures or paper drafting proceed.\n\n## Reproducibility Notes\n\n- Code files exist under `06_code/` and can be re-executed.\n- `run_001` log available in `07_results/logs/q1_run.log`.\n- No manual modification of output values detected.\n- Random seed is `deterministic`.\n\n## Human Gate\n\nPlease confirm that the six frozen result rows (R01--R06) are approved as the sole authoritative source for numerical values in the paper. Once acknowledged, results can be used for figures and claims.\n"
    },
    {
      "path": "11_review/simulated_human_gate_log.csv",
      "operation": "append",
      "content": "initial_07_results_freeze,results_freeze,results_freeze_gate,2026-06-04T12:00:00Z,pass,sandbox_simulated,Results freeze for Q1 OLS completed; other result files pending verification\n"
    }
  ],
  "unresolved": [
    {
      "issue": "Other result files (q1_results.csv, q2_results.csv, q3_results.csv, metrics_summary.csv) are present but have not been verified.",
      "blocker": "Cannot read file contents; need human or stage controller to provide extracted values or run scripts to obtain them before freezing."
    }
  ]
}
