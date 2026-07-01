import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.metrics import mean_squared_error

# Standard sample data
data = {
    'R': [0.91,0.85,0.79,0.72,0.66,0.60,0.54,0.49,0.43,0.39],
    'G': [0.23,0.29,0.35,0.42,0.49,0.55,0.61,0.67,0.72,0.76],
    'B': [0.18,0.21,0.26,0.31,0.37,0.43,0.50,0.57,0.63,0.69],
    'C': [0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0]
}
df = pd.DataFrame(data)
X = df[['R','G','B']].values
y = df['C'].values

# LOOCV
loo = LeaveOneOut()

# Model 1: Linear OLS
ols = LinearRegression()
ols_scores = cross_val_score(ols, X, y, cv=loo, scoring='neg_root_mean_squared_error')
cv_rmse_ols = -ols_scores.mean()
ols.fit(X, y)
train_rmse_ols = np.sqrt(mean_squared_error(y, ols.predict(X)))

# Model 2: Polynomial degree 2
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)
poly_scores = cross_val_score(LinearRegression(), X_poly, y, cv=loo, scoring='neg_root_mean_squared_error')
cv_rmse_poly = -poly_scores.mean()
poly_model = LinearRegression().fit(X_poly, y)
train_rmse_poly = np.sqrt(mean_squared_error(y, poly_model.predict(X_poly)))

# Model 3: Ridge
ridge = Ridge(alpha=0.1)
ridge_scores = cross_val_score(ridge, X, y, cv=loo, scoring='neg_root_mean_squared_error')
cv_rmse_ridge = -ridge_scores.mean()
ridge.fit(X, y)
train_rmse_ridge = np.sqrt(mean_squared_error(y, ridge.predict(X)))

# AIC/BIC for OLS (using statsmodels for exact calculation)
import statsmodels.api as sm
X_sm = sm.add_constant(X)
model_sm = sm.OLS(y, X_sm).fit()
aic_ols = model_sm.aic
bic_ols = model_sm.bic

results = pd.DataFrame({
    'model': ['linear_OLS', 'polynomial_degree2', 'ridge'],
    'CV_RMSE_LOOCV': [cv_rmse_ols, cv_rmse_poly, cv_rmse_ridge],
    'train_RMSE': [train_rmse_ols, train_rmse_poly, train_rmse_ridge],
    'AIC': [aic_ols, None, None],
    'BIC': [bic_ols, None, None]
})
results.to_csv('07_results/q2_comparison.csv', index=False)
