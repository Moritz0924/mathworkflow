# Result Freeze Report

## Stage Info
- Stage: results_freeze
- Execution: deep_sequential, iteration 5
- Date: 2026-06-04
- Status: completed

## Verification Summary
All 22 candidate results were examined:
- Source CSV files present in 07_results/ and match the values recorded in result_contract.csv.
- Code run logs (06_code/ q1_run.log, etc.) indicate successful execution with deterministic seed.
- Metric definitions, units, and direction agree with model_route.md.
- No manual alteration of output numbers detected.

## Frozen Results
| result_id | metric_name | metric_value | unit | source_file | freeze_status |
|-----------|-------------|--------------|------|-------------|---------------|
| R01 | coefficient_Intercept | 1.067247 | dimensionless | q1_coefficients.csv | frozen |
| R02 | coefficient_R | -1.821404 | dimensionless | q1_coefficients.csv | frozen |
| R03 | coefficient_G | 0.995618 | dimensionless | q1_coefficients.csv | frozen |
| R04 | coefficient_B | 5.630987 | dimensionless | q1_coefficients.csv | frozen |
| R05 | R_squared | 0.997747 | dimensionless | q1_metrics.csv | frozen |
| R06 | RMSE | 0.067418 | mg/L | q1_metrics.csv | frozen |
| R07 | CV_RMSE_LOOCV | 0.0748 | mg/L | q2_comparison.csv | frozen |
| R08 | CV_RMSE_LOOCV | 0.347 | mg/L | q2_comparison.csv | frozen |
| R09 | CV_RMSE_LOOCV | 0.098 | mg/L | q2_comparison.csv | frozen |
| R10 | prediction_T01 | 1.61 | mg/L | q3_predictions.csv | frozen |
| R11 | lower_95PI_T01 | 1.35 | mg/L | q3_predictions.csv | frozen |
| R12 | upper_95PI_T01 | 1.87 | mg/L | q3_predictions.csv | frozen |
| R13 | prediction_T02 | 3.17 | mg/L | q3_predictions.csv | frozen |
| R14 | lower_95PI_T02 | 2.90 | mg/L | q3_predictions.csv | frozen |
| R15 | upper_95PI_T02 | 3.44 | mg/L | q3_predictions.csv | frozen |
| R16 | prediction_T03 | 4.38 | mg/L | q3_predictions.csv | frozen |
| R17 | lower_95PI_T03 | 4.10 | mg/L | q3_predictions.csv | frozen |
| R18 | upper_95PI_T03 | 4.66 | mg/L | q3_predictions.csv | frozen |
| R19 | SE_Intercept | 0.05 | dimensionless | q1_stats.csv | frozen |
| R20 | SE_R | 0.08 | dimensionless | q1_stats.csv | frozen |
| R21 | SE_G | 0.15 | dimensionless | q1_stats.csv | frozen |
| R22 | SE_B | 0.20 | dimensionless | q1_stats.csv | frozen |

## Reproducibility
- All results computed by Python scripts in 06_code/ with deterministic seed.
- No random variation; results are exactly reproducible given the same input data.
- Run IDs: run_001 (Q1), run_002 (Q2, Q3).

## Risk & Anomalies
- No missing source files.
- No metric ambiguity.
- Values were cross-checked against output CSV and logs; no discrepancies.

## Human Gate
The results_freeze gate is simulated. All frozen results are ready for downstream stages (figures, paper_draft), pending human approval.

## Next Steps
- Proceed to figures stage only after human gate.
- Ensure all downstream figures and claims reference these frozen result_ids.
