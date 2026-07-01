import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy import stats

# Chinese font configuration (fallback chain)
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Data
C = np.array([0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0])
R = np.array([0.91,0.85,0.79,0.72,0.66,0.60,0.54,0.49,0.43,0.39])
G = np.array([0.23,0.29,0.35,0.42,0.49,0.55,0.61,0.67,0.72,0.76])
B = np.array([0.18,0.21,0.26,0.31,0.37,0.43,0.50,0.57,0.63,0.69])

# F001 coefficient bar
coef = [1.0672, -1.8214, 0.9956, 5.6310]
labels = ['Intercept', 'R', 'G', 'B']
fig, ax = plt.subplots()
ax.bar(labels, coef, color=['gray','red','green','blue'])
ax.set_title('OLS Coefficient Estimates')
ax.set_ylabel('Coefficient Value')
ax.axhline(0, color='black', linewidth=0.5)
plt.tight_layout()
plt.savefig('08_figures/main_figures/F001_coefficient_bar.svg')
plt.close()

# F002 pred vs actual
X = np.column_stack([np.ones(10), R, G, B])
beta = np.linalg.inv(X.T @ X) @ X.T @ C
C_pred = X @ beta
fig, ax = plt.subplots()
ax.scatter(C, C_pred)
ax.plot([0.5,5.0],[0.5,5.0], 'k--')
ax.set_xlabel('Actual Concentration (mg/L)')
ax.set_ylabel('Predicted Concentration (mg/L)')
ax.set_title('Predicted vs Actual')
plt.tight_layout()
plt.savefig('08_figures/main_figures/F002_pred_vs_actual.svg')
plt.close()

# F003 residuals vs fitted
resid = C - C_pred
fig, ax = plt.subplots()
ax.scatter(C_pred, resid)
ax.axhline(0, color='gray', linestyle='--')
ax.set_xlabel('Fitted Values')
ax.set_ylabel('Residuals')
ax.set_title('Residuals vs Fitted')
plt.tight_layout()
plt.savefig('08_figures/main_figures/F003_resid_fitted.svg')
plt.close()

# F004 QQ plot
fig, ax = plt.subplots()
stats.probplot(resid, dist="norm", plot=ax)
ax.set_title('Normal Q-Q Plot of Residuals')
plt.tight_layout()
plt.savefig('08_figures/main_figures/F004_qq_resid.svg')
plt.close()

# F005 scatter matrix
fig, axes = plt.subplots(1,3,figsize=(12,4))
axes[0].scatter(R, C, color='red')
axes[0].set_xlabel('R channel')
axes[0].set_ylabel('Concentration')
axes[1].scatter(G, C, color='green')
axes[1].set_xlabel('G channel')
axes[2].scatter(B, C, color='blue')
axes[2].set_xlabel('B channel')
fig.suptitle('Concentration vs Color Channels')
plt.tight_layout()
plt.savefig('08_figures/main_figures/F005_channel_scatter.svg')
plt.close()

# F006 correlation heatmap
data_df = pd.DataFrame({'R':R,'G':G,'B':B,'C':C})
corr = data_df.corr()
fig, ax = plt.subplots()
im = ax.imshow(corr, cmap='coolwarm')
ax.set_xticks(np.arange(4))
ax.set_yticks(np.arange(4))
ax.set_xticklabels(['R','G','B','C'])
ax.set_yticklabels(['R','G','B','C'])
plt.colorbar(im)
ax.set_title('Correlation Heatmap')
plt.tight_layout()
plt.savefig('08_figures/main_figures/F006_correlation_heatmap.svg')
plt.close()
