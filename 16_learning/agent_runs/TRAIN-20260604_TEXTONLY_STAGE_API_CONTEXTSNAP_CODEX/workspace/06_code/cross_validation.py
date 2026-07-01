import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import LeaveOneOut, cross_val_score

data = {
    'R': [0.91,0.85,0.79,0.72,0.66,0.60,0.54,0.49,0.43,0.39],
    'G': [0.23,0.29,0.35,0.42,0.49,0.55,0.61,0.67,0.72,0.76],
    'B': [0.18,0.21,0.26,0.31,0.37,0.43,0.50,0.57,0.63,0.69],
    'C': [0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0]
}
df = pd.DataFrame(data)
X = df[['R','G','B']]
y = df['C']
loo = LeaveOneOut()
scores = cross_val_score(LinearRegression(), X, y, cv=loo, scoring='neg_root_mean_squared_error')
cv_rmse = -scores.mean()
pd.DataFrame({'CV_RMSE_LOOCV': [cv_rmse]}).to_csv('07_results/cv_results.csv', index=False)
