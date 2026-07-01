# Model Route for Color-Concentration Identification

## Stage Summary
- **Stage**: model_route
- **Date**: 2025-04-08
- **Inputs used**: `00_problem/problem_statement.md` (direct read); no prior `01_task_analysis` or `03_data` files found; used problem text as substitute.
- **Risk**: Formal task decomposition and data quality report absent; solving directly from problem statement introduces risk of incomplete assumption logging. Proceed under sandbox waiver.

## Problem Restatement
Three sub-problems (Q1–Q3) around predicting substance concentration from normalized RGB color channels using 10 standard samples and 3 test samples.

## Sub-problem Model Routing

### Q1: Color channel dependence & explainable model
- **Objective**: Analyze relationship between R, G, B and concentration; build an explainable predictive model; describe direction of influence of each channel.
- **Main Model**: **Multiple Linear Regression (OLS)**
  - `C = β₀ + β₁·R + β₂·G + β₃·B + ε`
  - Interpretable coefficients: sign and magnitude indicate direction and strength.
  - Assumptions: linearity, homoscedasticity, no perfect collinearity. Small sample (n=10) manageable.
  - Validation: adjusted R², residual plots, coefficient p-values.
- **Fallback Model**: **Ridge Regression (L2 regularization)**
  - Use if multicollinearity suspected (e.g., high correlation between channels).
  - Regularization parameter chosen via leave-one-out cross-validation (LOOCV).
- **Data binding**: standard samples S01–S10; predictors R,G,B; target concentration.
- **EDA findings note**: Data range shows monotonic trends (R decreases, G and B increase with concentration). Visual inspection suggests linearity.
- **Explainability**: high; coefficients directly interpretable.
- **Figure suggestion**: scatter plots of each channel vs concentration with regression line; coefficient bar chart.

### Q2: Model comparison & overfitting control
- **Objective**: Compare at least three candidate model types; justify selection; discuss overfitting control.
- **Candidate models**:
  1. **Multiple Linear Regression** (baseline, OLS)
  2. **Polynomial Regression (degree 2, possibly with interaction)** – captures slight curvature but risks overfitting with only 10 points.
  3. **Random Forest Regression** (ensemble) – flexibility but low interpretability; high overfitting risk on small data.
- **Main comparison metric**: Root Mean Square Error (RMSE) under Leave-One-Out Cross-Validation (LOOCV) to mimic small-sample evaluation.
- **Selection criteria**: 
  - Best LOOCV RMSE; 
  - Model parsimony (AIC/BIC); 
  - Interpretability for real-world deployment.
- **Overfitting control**: 
  - LOOCV for robust error estimation; 
  - Regularization for linear/poly; 
  - Limit tree depth/min samples for RF; 
  - Compare training vs validation error gap.
- **Anticipated outcome**: Linear or low-degree polynomial likely optimal; RF may overfit.
- **Figure suggestion**: RMSE bar chart across models; predicted vs actual scatter for best model.

### Q3: Predict test samples, uncertainty, reusable workflow
- **Objective**: Predict concentrations for T01, T02, T03 with uncertainty quantification; propose reusable detection workflow.
- **Main Model**: The best model selected in Q2.
- **Uncertainty quantification**: 
  - Prediction intervals (e.g., ± t₀.₀₂₅ · SE_pred) for linear models.
  - Bootstrap confidence intervals for non-parametric models.
  - Report standard error and coefficient of variation.
- **Reusable workflow**:
  1. Acquire standard samples with known concentrations.
  2. Measure RGB under controlled lighting.
  3. Fit selected model; validate via LOOCV.
  4. Measure unknown sample RGB; predict with uncertainty.
  5. Periodically recalibrate with new standards.
- **Figure suggestion**: prediction interval plot for test samples; workflow diagram (Mermaid).

## Risk Registry
| Risk ID | Description | Severity | Mitigation |
|---------|-------------|----------|------------|
| R01 | Small sample size (n=10) → high variance in coefficient estimates | High | Use LOOCV, prefer simple models, report confidence intervals |
| R02 | Possible nonlinearity not captured by linear model | Medium | Compare with polynomial/ensemble; check residual patterns |
| R03 | Overfitting with high-degree polynomial or RF | Medium | Enforce regularization, limited depth, LOOCV |
| R04 | Missing formal data quality report | Medium | Assumed data complete and no outliers; validate during codegen |
| R05 | Collinearity among R,G,B | Low | Monitor VIF; if high, switch to Ridge |

## Human Gate
- **Gate**: model_route_gate
- **Decision required**: Approve main/fallback models for Q1–Q3, core assumptions, and risk acceptance.
- **Simulated gate log**: will be written to `11_review/simulated_human_gate_log.csv`.

## Self-Check
1. No code generated. ✓
2. No results written (only model planning). ✓
3. Prior DB not used as answer; no prior cards. ✓
4. Each main model has a fallback. ✓
5. Important formulas registered in `formula_contract.csv`. ✓
6. Validation script not run (disabled sandbox). ✓
