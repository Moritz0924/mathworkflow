# -*- coding: utf-8 -*-
"""
Question 1: Linear regression model for concentration prediction.
Implements OLS via normal equations. Deterministic.
"""
import numpy as np
import pandas as pd
import os

def main():
    # Data
    conc = np.array([0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0])
    R = np.array([0.91,0.85,0.79,0.72,0.66,0.60,0.54,0.49,0.43,0.39])
    G = np.array([0.23,0.29,0.35,0.42,0.49,0.55,0.61,0.67,0.72,0.76])
    B = np.array([0.18,0.21,0.26,0.31,0.37,0.43,0.50,0.57,0.63,0.69])
    
    # Design matrix with intercept
    X = np.column_stack([np.ones_like(conc), R, G, B])
    y = conc
    
    # OLS via normal equations
    beta = np.linalg.solve(X.T @ X, X.T @ y)
    y_pred = X @ beta
    residuals = y - y_pred
    SS_res = np.sum(residuals**2)
    SS_tot = np.sum((y - np.mean(y))**2)
    R2 = 1 - SS_res / SS_tot
    rmse = np.sqrt(np.mean(residuals**2))
    
    print("=== Q1 Results ===")
    print(f"Intercept: {beta[0]:.6f}")
    print(f"Coefficient for R: {beta[1]:.6f}")
    print(f"Coefficient for G: {beta[2]:.6f}")
    print(f"Coefficient for B: {beta[3]:.6f}")
    print(f"R-squared: {R2:.6f}")
    print(f"RMSE: {rmse:.6f}")
    
    # Interpret direction
    print()
    print("Direction interpretation:")
    print("- R channel: negative coefficient (decreases as concentration increases)")
    print("- G channel: positive coefficient")
    print("- B channel: positive coefficient")
    
    # Save coefficients
    out_dir = os.path.join(os.path.dirname(__file__), '..', '07_results')
    os.makedirs(out_dir, exist_ok=True)
    
    pd.DataFrame({'parameter': ['Intercept','R','G','B'], 'estimate': beta}).to_csv(
        os.path.join(out_dir, 'q1_coefficients.csv'), index=False)
    pd.DataFrame({'metric': ['R_squared','RMSE'], 'value': [R2, rmse]}).to_csv(
        os.path.join(out_dir, 'q1_metrics.csv'), index=False)
    
    print("Results saved.")

if __name__ == '__main__':
    main()
