# Code Documentation (Revision RV-017)

This directory contains the scripts used for model estimation, comparison, and prediction.

## Scripts

- `q1_linear_model.py`: Fits the multiple linear regression model using statsmodels OLS on standard sample data. Outputs coefficient estimates, standard errors, t-values, p-values, R-squared, and RMSE. Writes results to `07_results/q1_coefficients.csv`, `q1_metrics.csv`, and `q1_stats.csv`.

- `q2_model_comparison.py`: Implements LOOCV evaluation for three models: OLS linear regression, degree-2 polynomial regression (via sklearn.PolynomialFeatures and LinearRegression), and Ridge regression (alpha tuned by grid search). Outputs CV RMSE values to `07_results/q2_comparison.csv`.

- `q3_uncertainty.py`: Uses the trained OLS model to predict concentrations for test samples T01–T03, computes 95% prediction intervals (using statsmodels' get_prediction method), and writes predictions and intervals to `07_results/q3_predictions.csv`.

All scripts are designed to run deterministically (random seed where applicable). See each file for inline comments.
