# Model Route Report

**Stage**: `model_route`  
**Status**: Draft for human gate  
**Date**: 2026-06-03 (simulated)

---

## 1. Input Verification

| Required Input | Status | Notes |
|---|---|---|
| `01_task_analysis/task_decomposition.md` | NOT FOUND (simulated) | Used generic sub-questions: Q1 (evaluation), Q2 (optimization), Q3 (prediction). |
| `01_task_analysis/problem_model_profile.csv` | NOT FOUND (simulated) | Assumed typical profile. |
| `03_data/data_quality_report.md` | NOT FOUND (simulated) | No real data bound; risk documented. |
| `13_prior_db/pre_solve_cards.md` | NOT FOUND | Prior search not executed; no prior cards used. |

**Action**: Because sandbox does not contain the required stage outputs, model routing proceeds with generic plausible sub-questions that are typical for a public-transport optimization topic. All choices must be validated against actual task decomposition and data before proceeding to codegen.

---

## 2. Sub-Question Modelling Matrix

| QID | Type | Main Model | Backup Model | Input Variables | Output Metrics | Core Assumptions | Verification Approach | Figure Suggestions |
|---|---|---|---|---|---|---|---|---|
| Q1 | Evaluation | AHP + TOPSIS | DEA | Route length, frequency, ridership, punctuality | Composite efficiency score | Weights from expert judgement or entropy | Sensitivity to weight changes, rank stability | Bar chart of scores, radar chart of criteria |
| Q2 | Optimization | Multi-Objective GA (NSGA-II) | Linear Programming (simplified) | Demand matrix, travel times, fleet size | Pareto front: cost, avg wait time | Capacity constraints, no stochastic demand | Compare with baseline; extreme-case simulation | Pareto frontier plot, route map before/after |
| Q3 | Prediction | Random Forest Regression | ARIMA (univariate) | Historical ridership, time features, weather, holiday | Forecast ridership, error bands | Feature stationarity, no structural break | Time-series cross-validation, residual diagnostics | Time series line plot with forecast, error distribution |

---

## 3. Detailed Model Routes

### Q1: Efficiency Evaluation of Existing Routes

- **Main Model**: AHP (Analytic Hierarchy Process) to derive criteria weights from expert questionnaires, combined with TOPSIS to rank routes based on closeness to ideal solution.
- **Rationale**: Transparent weight derivation, easy to explain to stakeholders, handles mixed-scale criteria.
- **Data Requirements**: Route-level performance indicators (frequency, travel time, ridership, cost efficiency). Data quality issues (missing values) handled by interpolation or exclusion.
- **Verification**: Rank correlation with alternative weighting methods (entropy, CRITIC). Stability test: perturb weights by ±10% and check rank reversals.
- **Risk**: Subjective weights may be contested; if expert input unavailable, fallback to entropy-TOPSIS.
- **Backup Model**: Data Envelopment Analysis (DEA) if we have clear input/output definition; non-parametric, no weight elicitation, but sensitive to outliers.
- **Figure Suggestions**: 
  - Figure 1: Bar chart of composite scores with error bars from sensitivity.
  - Figure 2: Radar chart comparing top-3 and bottom-3 routes across criteria.

### Q2: Route Network Optimization

- **Main Model**: Multi-objective genetic algorithm (NSGA-II). Decision variables: binary stops served, headway adjustments. Objectives: (1) minimize total operational cost, (2) minimize passenger average waiting time. Constraints: budget, fleet size, coverage.
- **Rationale**: Handles discrete combinatorial problem, provides trade-off frontier, widely used in transit design literature.
- **Data Requirements**: Origin-destination demand matrix, travel time matrices, cost parameters. If demand matrix unavailable, assume uniform demand or proxy from smart card data.
- **Verification**: 
  - Compare Pareto front with baseline (current network).
  - Test with small synthetic instance where optimal solution is known.
  - Run with different random seeds to check convergence stability.
- **Risk**: NSGA-II is stochastic; results may vary. Long runtime. Must fix random seed. If computational budget is limited, use LP relaxation.
- **Backup Model**: Linear programming (LP) simplification: aggregate to corridors, continuous headway variables, single weighted objective. Less realistic but faster and deterministic.
- **Figure Suggestions**:
  - Figure 3: Pareto front (cost vs wait time) with baseline marked.
  - Figure 4: Map showing current and optimized route network.

### Q3: Forecast of Post-Optimization Ridership

- **Main Model**: Random forest regression with features: day of week, holiday indicator, weather, historical ridership lags, and indicator for post-optimization period.
- **Rationale**: Captures non-linear interactions, robust to outliers, provides feature importance.
- **Data Requirements**: Time series of daily ridership, weather data, calendar. Must ensure no data leakage (future information). Training: pre-optimization data; test: post-optimization data (counterfactual).
- **Verification**:
  - Time series cross-validation: rolling origin.
  - Residual analysis: no autocorrelation, zero mean.
  - Prediction intervals via quantile regression forests.
  - Compare with naive historical average baseline.
- **Risk**: Small dataset may lead to overfitting. If ridership is highly seasonal and trend-stationary, ARIMA may suffice.
- **Backup Model**: ARIMA (or SARIMA) univariate model. Simpler, less data hungry, but cannot incorporate external regressors.
- **Figure Suggestions**:
  - Figure 5: Time series line plot of actual vs fitted vs forecast with confidence bands.
  - Figure 6: Residual diagnostic plots (ACF, histogram).

---

## 4. Formula Contract Draft

Key formulas identified for registration. See `14_contracts/formula_contract.csv` for detailed rows.

- **F1**: TOPSIS closeness coefficient (Q1)
- **F2**: NSGA-II crowding distance (Q2)
- **F3**: Total operational cost function (Q2)
- **F4**: Mean Absolute Percentage Error (MAPE) for evaluation (Q3)
- **F5**: Random forest prediction equation (Q3)

---

## 5. Risk Register

| Risk ID | Description | Severity | Mitigation |
|---|---|---|---|
| R1 | Task decomposition and data report missing: model choices may be misaligned | High | Block codegen until confirmed; route choices are provisional. |
| R2 | Subjective weights for AHP may be unavailable | Medium | Use entropy method as fallback. |
| R3 | Demand matrix missing for Q2 | High | Use simplified LP model or synthetic demand. |
| R4 | Stochastic optimization results not reproducible | Medium | Fix random seed, run multiple seeds, report variability. |
| R5 | Insufficient data for machine learning (Q3) | Medium | Use simpler ARIMA; document data limits. |

---

## 6. Self-Check

- [x] No code generated.
- [x] No results written.
- [x] Did not treat prior cards as answers (prior cards not used).
- [x] Each main model has a backup model.
- [x] Important formulas registered or noted as draft.
- [ ] Validation script not run (not available in sandbox).
- [ ] Awaiting human confirmation (simulated gate recorded).

---

## 7. Human Gate Questions

1. Do you approve the main and backup models for Q1 (AHP-TOPSIS / DEA)?
2. Do you approve the main and backup models for Q2 (NSGA-II / LP)?
3. Do you approve the main and backup models for Q3 (Random Forest / ARIMA)?
4. Are the risks acceptable, and do you want to impose additional constraints (e.g., required data sources, interpretability requirements)?
5. Is the provisional nature of this plan acceptable given missing upstream artifacts?
