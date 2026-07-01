import numpy as np
import pandas as pd
import statsmodels.api as sm

# Data
data = {
    'R': [0.91,0.85,0.79,0.72,0.66,0.60,0.54,0.49,0.43,0.39],
    'G': [0.23,0.29,0.35,0.42,0.49,0.55,0.61,0.67,0.72,0.76],
    'B': [0.18,0.21,0.26,0.31,0.37,0.43,0.50,0.57,0.63,0.69],
    'C': [0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0]
}
df = pd.DataFrame(data)
X = sm.add_constant(df[['R','G','B']])
y = df['C']
model = sm.OLS(y, X).fit()

# Extract coefficient statistics
summary_table = model.summary2().tables[1]
summary_table.to_csv('07_results/q1_stats.csv')

# Predict test samples
test_data = {
    'R': [0.77,0.58,0.45],
    'G': [0.37,0.57,0.70],
    'B': [0.28,0.46,0.61],
    'sample': ['T01','T02','T03']
}
test_df = pd.DataFrame(test_data)
X_test = sm.add_constant(test_df[['R','G','B']])
pred = model.get_prediction(X_test)
pred_summary = pred.summary_frame(alpha=0.05)
output = pd.DataFrame({
    'sample': test_df['sample'],
    'prediction': pred_summary['mean'],
    'lower_95PI': pred_summary['obs_ci_lower'],
    'upper_95PI': pred_summary['obs_ci_upper']
})
output.to_csv('07_results/q3_predictions.csv', index=False)
