# Fallback Plan

## Principle
If a primary model fails to meet verification criteria, we degrade to a simpler, more robust alternative rather than abandoning the solution.

## Sub-Problem 1: Sales Forecasting
| Failure Condition | Detection | Fallback Model | Justification |
|------------------|-----------|---------------|---------------|
| Residual autocorrelation (Ljung-Box p<0.05) | Diagnostic | Prophet | More flexible seasonality handling |
| Forecast MASE >1.5 on validation | Cross-validation | Exponential Smoothing (ETS) | Robust for trend/seasonal data |
| Data missingness exceeds 10% after re-inspection | Data quality check | Simple Moving Average (12 weeks) | Minimal parameter, no imputation bias |
| Exogenous variables not significant (p>0.1) | t-test | ARIMA without regressors | Prevents overfitting |

## Sub-Problem 2: Inventory Optimization
| Failure Condition | Detection | Fallback Model | Justification |
|------------------|-----------|---------------|---------------|
| MILP optimality gap >5% after 10 min | Solver log | Greedy heuristic (least-unit-cost) | Provides feasible solution quickly |
| Demand forecast MAPE >30% | SP1 evaluation | Two-stage stochastic with 10 scenarios | Explicit uncertainty handling |
| Holding/shortage cost ratio unrealistic (>100) | Data sanity check | Newsvendor model with critical ratio | Simpler, analytically solvable |
| Infeasible due to capacity | Solver status | Relax capacity constraint & report violation | Identify bottleneck |

## Global Escalation
- If both primary and fallback fail for a sub-problem, report as `blocked` and request human intervention.
- Document failure in `11_review/blocker_notes.md`.

## Fallback Execution Protocol
1. Identify failure via automated test in `06_code/`.
2. Log the trigger in `10_ai_logs/fallback_trigger.log`.
3. Switch model and re-run pipeline.
4. Compare results against primary model results (if any) and report discrepancies.
5. Update `14_contracts/result_contract.csv` with fallback flag.

## Cost of Fallback
- May increase computational time (e.g., stochastic programming).
- May decrease accuracy or optimality; this trade-off must be accepted by human.
