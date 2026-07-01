# Fallback Plan

This document describes degradation paths if primary models fail or assumptions are violated.

## Q1: Explainable Model
- **Primary failure**: Severe heteroscedasticity or non-linearity makes linear model unreliable.
- **Fallback**: 
  1. Move to **Ridge Regression** if collinearity is the only issue.
  2. If non-linearity is evident, switch to **Polynomial Regression (degree 2)** but require justification via LOOCV.
  3. If both fail, consider **Gaussian Process Regression** with simple kernel (e.g., RBF) for flexible yet probabilistic prediction; however, interpretability drops.

## Q2: Model Comparison
- **Primary failure**: RF overfits excessively (LOOCV error >> linear).
- **Fallback**: 
  1. Replace RF with **Support Vector Regression (SVR)** with RBF kernel; tune C and epsilon via LOOCV.
  2. Alternatively, use **K-Nearest Neighbors (K=3)** as a simple baseline.
- **Overfitting control fallback**: If LOOCV is computationally unstable (very small n), supplement with bootstrap .632 estimator.

## Q3: Prediction & Workflow
- **Primary failure**: Prediction intervals too wide to be useful.
- **Fallback**: Report only point estimates with qualitative uncertainty caveats; recommend additional standard samples to tighten intervals.
- **Workflow failure**: If RGB measurement not reproducible under varying conditions, add normalization step using reference white/black standards.

## General Fallback Principles
- Prefer simpler, well-understood models over black-box.
- Always quantify and report uncertainty.
- If any model assumption fails irrecoverably, abort model route and return to `task_analysis` or `data` stage.
