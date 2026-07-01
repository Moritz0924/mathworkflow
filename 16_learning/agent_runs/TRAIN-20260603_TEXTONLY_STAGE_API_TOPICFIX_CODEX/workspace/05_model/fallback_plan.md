# Fallback Plan

If a main model fails to produce valid results (due to data, computation, or performance issues), the following fallback routes are activated.

## Q1: Efficiency Evaluation

| Trigger | Fallback Action |
|---|---|
| Expert weights unavailable or inconsistent | Switch to entropy-weighted TOPSIS (no subjective input). |
| TOPSIS rank instable under reasonable perturbation | Use DEA; if DEA also fails, fall back to simple weighted sum with equally weighted normalized indicators. |

## Q2: Route Optimization

| Trigger | Fallback Action |
|---|---|
| NSGA-II fails to converge or runtime exceeds budget | Simplify to single-objective LP with weighted sum; manually explore trade-off by varying weights. |
| LP infeasible due to tight constraints | Relax coverage constraints, reduce number of routes, or use heuristic (greedy insertion). |
| Data too sparse for meaningful optimization | Instead of full optimization, produce a comparative scenario analysis (e.g., adjust frequencies of top-5 routes). |

## Q3: Ridership Prediction

| Trigger | Fallback Action |
|---|---|
| Random forest overfits or has poor validation performance | Use ARIMA (or seasonal ARIMA) as simpler, interpretable model. |
| ARIMA residuals show non-stationarity | Apply differencing, or use exponential smoothing (ETS). |
| Neither model gives acceptable error | Report only descriptive statistics with uncertainty; use naive forecast as baseline. |

## General Fallbacks
- If any sub-problem cannot be solved with available data, the paper will explicitly state that the question is answered partially, with limitations discussed.
- Computational fallback: all models should have a lightweight version that can run on a standard laptop within 1 hour.

All fallback activations must be recorded in `10_ai_logs/` and justified in the final paper.
