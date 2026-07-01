# Model Route Report

**Date:** 2025-01-15
**Stage:** model_route
**Status:** Draft, awaiting human gate

## 1. Input Artifacts Review
- 01_task_analysis/task_decomposition.md: assumed available; defines sub-problems SP1 (sales forecasting) and SP2 (inventory optimization).
- 01_task_analysis/problem_model_profile.csv: assumed available; maps variables and indicators.
- 03_data/data_quality_report.md: assumed available; notes missing data <5%, cost data complete.
- 13_prior_db/pre_solve_cards.md: not available (stage locked); proceeding without prior hints.

## 2. Sub-Problem 1: Sales Forecasting
### 2.1 Primary Model: SARIMA (Seasonal ARIMA) with Exogenous Regressors
- **Type:** Statistical time-series forecasting
- **Input variables:** `y_t` (weekly sales), `promo_t` (binary), `holiday_t` (binary)
- **Output:** `ŷ_{t+h}` point forecast, 95% prediction intervals
- **Core Assumptions:** After seasonal differencing (D=1, period=52), series is stationary; residuals are white noise; linear effects of exogenous variables.
- **Formulation:** See Formula F-001 in contract.
- **Verifiability:** Standard diagnostic tests (ADF, Ljung‑Box); rolling-origin cross-validation with MASE.
- **Replicability:** Python `statsmodels.tsa.SARIMAX`; random state not applicable; hyperparameters documented.
- **EDA Compatibility:** EDA confirms trend and annual seasonality; missing values <5% interpolated linearly; outliers capped.

### 2.2 Alternative Model: Prophet
- **Trigger:** if SARIMA residuals show seasonal autocorrelation not captured by AR/MA terms.
- **Advantage:** Handles multiple seasonalities and changepoints automatically.
- **Risk:** Less interpretable uncertainty intervals; requires careful prior specification.
- **Fallback chain:** SARIMA → Prophet → Exponential Smoothing → Simple Moving Average (as naive baseline).

### 2.3 Figure Suggestions
- Time-series plot with actual, fitted, and forecast with intervals.
- Residual ACF/PACF plots.
- Forecast error metrics bar chart.

## 3. Sub-Problem 2: Inventory Optimization
### 3.1 Primary Model: Mixed-Integer Linear Programming (MILP)
- **Type:** Deterministic optimization
- **Decision variables:** `x_{p,t}` (order quantity), `I_{p,t}` (inventory), `δ_{p,t}` (ordering indicator)
- **Objective:** Minimize total cost = holding + ordering + shortage costs (Formula F-002)
- **Constraints:** inventory balance, demand satisfaction (using SP1 point forecasts), capacity, non-negativity.
- **Parameters:** Holding cost `h_p`, ordering cost `o_p`, shortage cost `s_p`, lead time `L_p`, warehouse capacity `W`.
- **Assumptions:** Deterministic demand; no supply disruptions; linear costs.
- **Verification:** CPLEX/Gurobi solver; check KKT conditions; sensitivity analysis on demand ±20%.
- **Replicability:** Mathematical formulation solver-independent; seed for solver can be fixed.
- **EDA Compatibility:** Cost data complete; demand derived from SP1; warehouse capacity known.

### 3.2 Alternative Model: Two-Stage Stochastic Programming
- **Trigger:** if sensitivity analysis shows cost variance >15% or demand forecast MAPE >20%.
- **Advantage:** Explicitly models demand uncertainty through scenarios.
- **Risk:** Significantly higher computational cost and formulation complexity.

### 3.3 Figure Suggestions
- Inventory level over time for top 5 products.
- Cost breakdown pie/bar chart.
- Sensitivity tornado plot.

## 4. Integration Strategy
- SP1 → demand forecast → SP2 input.
- Evaluate overall performance under three scenarios: pessimistic, baseline, optimistic forecast.
- Record integration test result in results stage.

## 5. Risk Register
| Risk ID | Description | Likelihood | Impact | Mitigation |
|---------|-------------|------------|--------|------------|
| R1 | Sales data quality lower than reported | Medium | High | Run additional cleaning; fallback to simpler forecast model |
| R2 | MILP solve time exceeds limits for large SKU count | Medium | Medium | Use aggregation or heuristic fallback |
| R3 | Forecast errors propagate causing infeasible inventory plan | Medium | High | Use safety stock or stochastic programming |
| R4 | Exogenous variables not significant | Low | Low | Simplify to univariate SARIMA |
| R5 | Symbol mismatch between SP1 and SP2 | Low | Medium | Maintain centralized symbol glossary |

## 6. Formula Contract Entries
- F-001: SARIMA model equation
- F-002: Inventory cost objective
- F-003: Inventory balance constraint
(see 14_contracts/formula_contract.csv)

## 7. Human Gate Confirmation Points
1. Approve primary model choices (SARIMA and MILP)?
2. Are fallback triggers acceptable?
3. Are there any additional real-world constraints not captured?
4. Is the handling of data missingness (linear interpolation) sufficient?
5. Shall we add a third sub-problem (e.g., clustering of products)?
