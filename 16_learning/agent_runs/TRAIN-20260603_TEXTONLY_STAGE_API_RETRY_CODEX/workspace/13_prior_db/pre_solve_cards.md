# Pre-Solve Experience Cards

**Stage:** `prior_retrieval`  
**Status:** advisory_only  
**Generated:** 2026-06-03  
**Policy:** `config/prior_db_policy.yaml`

---

## Problem–Prior Mapping Summary

| Sub-problem | Prior Card ID | Problem Type | Model Family | Figure Hints | Scoring Risks | Copy Risk |
|-------------|---------------|--------------|--------------|---------------|---------------|-----------|
| 1 | card_opt_001 | Constrained optimization | LP/NLP, Surrogate-based optimization | Feasibility region plot, objective convergence trace | Constraint violation undocumented, local-optimum trap | abstracted_pass |
| 2 | card_pred_002 | Time-series forecasting | ARIMA, LSTM, Prophet | Forecast vs actual overlay, residual ACF/PACF | Naïve stationarity assumption, forecast horizon untested | abstracted_pass |
| 3 | card_eval_003 | Multi-criteria evaluation | AHP, TOPSIS, DEA | Weight heatmap, sensitivity tornado chart | Subjective weight source, rank reversal potential | abstracted_pass |

---

## Experience Cards

### Card 1 — Constrained Optimization
- **Source:** `13_prior_db/cards/prior_cards.jsonl` (id: opt_001, family: LP-NLP, source_count: 45)
- **Advisory model hints:** Start with continuous relaxation; test multiple solvers (Gurobi, Ipopt); handle non-convexity via multi-start or Bayesian optimization.
- **Advisory figure hints:** Feasible region polygon (2D slice), objective improvement per iteration, constraint slack heatmap.
- **Scoring risk alerts:**
  - If constraints cannot be proven satisfied in closed-form, judges will note “unvalidated constraints.”
  - Missing residual diagnostics for KKT conditions lowers model rigor score.
- **Pre-processing patterns:** Normalize decision variables; remove redundant constraints; check scaling.

### Card 2 — Time-series Forecasting
- **Source:** `13_prior_db/cards/prior_cards.jsonl` (id: pred_002, family: ARIMA-LSTM, source_count: 52)
- **Advisory model hints:** Baseline with seasonal-naïve; then ARIMA/SARIMA; add exogenous regressors; neural models only if data volume > 500 points.
- **Advisory figure hints:** Forecast with 90% prediction interval bands, ACF/PACF of residuals, Ljung-Box p-value dashboard.
- **Scoring risk alerts:**
  - Extrapolation beyond the historical range without explicit boundary statement → “over-extrapolation” comment.
  - No stationarity test → model mis-specification suspicion.
- **Pre-processing patterns:** Log-transform if variance grows with level; handle missing values via interpolation or Kalman smoothing.

### Card 3 — Multi-criteria Evaluation
- **Source:** `13_prior_db/cards/prior_cards.jsonl` (id: eval_003, family: AHP-TOPSIS, source_count: 31)
- **Advisory model hints:** AHP for weight derivation but report CR; TOPSIS for final ranking; sensitivity on criterion weights is mandatory.
- **Advisory figure hints:** Weight heatmap with dendrogram reordering, tornado plot of criteria sensitivity, rank difference waterfall.
- **Scoring risk alerts:**
  - Subjective pairwise comparisons without consistency ratio → “weight source weak.”
  - No sensitivity analysis → “robustness unproven.”
  - Rank reversal not discussed → deduction in evaluation design.
- **Pre-processing patterns:** Normalize criteria to [0,1]; handle negative directions before aggregation.

---

## Cross-cutting Scoring Risks

- **Constraint traceability:** Every constraint must be linked to an equation, code line, and diagnostic output.
- **Residual diagnostics:** Always include standardized residuals, Q-Q plot, and Durbin-Watson for regression components.
- **Extrapolation boundary:** State explicitly where the model applies and where it does not.
- **Weight provenance:** All weights must come from data, elicitation, or sensitivity-driven ranges; never arbitrary.

## Self-check (Stage 13)

1. Output is advisory_only and marked as such. ✅
2. No historical paper text, captions, tables, or conclusions copied. ✅
3. No fact answers provided for the current problem. ✅
4. Prior cards are not written into result, figure, or paper contracts. ✅
5. Copy-risk check script recommendation: `scripts/check_prior_copy_risk.py --warn-only` (not run, recorded as pending).

**Simulated human gate required before model route stage.**
