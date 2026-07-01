# Prior Experience Cards (Pre-Solve Retrieval)

**Advisory Only – Do not copy as solution.**

All cards sourced from `13_prior_db/cards/prior_cards.jsonl` with `copy_risk_status=abstracted_pass`. No historical text, labels, or conclusions are reproduced.

## Card P1: Time Series Forecasting with ARIMA Family
- **Source card_id:** `TS-ARIMA-23`
- **Family:** ARIMA / SARIMA / ARIMAX
- **source_count:** 15 (high sample)
- **Model hints:** Consider ARIMA or SARIMA for short-term univariate forecasting. Use AIC/BIC for order selection. Key preprocessing: stationarity check (ADF/KPSS) and differencing; residual diagnostics (Ljung-Box) are mandatory. Exogenous regressors can improve accuracy if available.
- **Figure hints:** Abstract suggestions: decomposed time series (trend, seasonal, residual), residual ACF/PACF panel, forecast vs actual overlay.
- **Scoring risks:** Missing seasonality or structural break may degrade fit; failure to document residual diagnostics often penalised.

## Card P2: LSTM/RNN for Sequence Prediction
- **Source card_id:** `DL-LSTM-07`
- **Family:** RNN / LSTM / GRU
- **source_count:** 9 (low-sample warning)
- **Model hints:** LSTM with attention can capture mid-length dependencies. Suited when data volume is moderate. Tuning critical (units, learning rate, dropout, batch size). Risk of overfitting if dataset small; use validation split and early stopping.
- **Figure hints:** Training/validation loss curves, predicted vs actual with confidence shading, attention weight heatmap.
- **Scoring risks:** Overfitting on small data; limited interpretability may attract critic reviews. Computational cost may exceed typical competition timeline; keep architecture simple if data sparse.

## Card P3: Uncertainty Quantification via Bootstrap/PI
- **Source card_id:** `UQ-BOOT-11`
- **Family:** Bootstrap / Monte Carlo / Conformal
- **source_count:** 12 (medium sample)
- **Model hints:** Bootstrap residuals for prediction intervals around deterministic forecasts. For LSTM, Monte Carlo dropout provides approximate Bayesian intervals. Conformal prediction offers distribution-free coverage guarantees.
- **Figure hints:** Prediction interval fan chart over horizon, coverage probability versus nominal level, interval width growth.
- **Scoring risks:** Under-coverage if model misspecified; parametric assumptions may be violated; must validate with hold-out period.

## Mapping to Problem Model Profile (`01_task_analysis/problem_model_profile.csv`)
- **Sub-problem A (short-term point prediction):** Aligns with Card P1 (ARIMA) and P2 (LSTM). Ensemble strategy could be considered if time permits.
- **Sub-problem B (distributional forecast):** Card P3 directly relevant for constructing prediction intervals or full distribution.
- **Sub-problem C (feature impact analysis):** No direct high-sample card found; low-sample warning applies to ad-hoc investigation.

**All cards are advisory.** Final model route must be driven by task analysis, data properties revealed by EDA, and validation contracts.