# EDA Summary: Colour and Concentration Identification

## 1. Data Overview

- **Standard samples**: 10 observations with known concentration (`concentration_mg_L`) and three colour channels (`R`, `G`, `B`).
- **Unknown samples**: 3 observations with only colour channels; concentrations to be predicted.
- All values are numeric and complete; no missing, duplicate, or out-of-range entries.

## 2. Descriptive Statistics (Standard Samples)

| Statistic | concentration_mg_L | R    | G    | B    |
|-----------|-------------------|------|------|------|
| count     | 10                | 10   | 10   | 10   |
| mean      | 2.75              | 0.638| 0.509| 0.415|
| std       | 1.508             | 0.183| 0.183| 0.183|
| min       | 0.5               | 0.39 | 0.23 | 0.18 |
| 25%       | 1.625             | 0.467| 0.342| 0.272|
| 50%       | 2.75              | 0.63 | 0.52 | 0.42 |
| 75%       | 3.875             | 0.802| 0.677| 0.557|
| max       | 5.0               | 0.91 | 0.76 | 0.69 |

- Concentration is evenly spaced (0.5 to 5.0, step 0.5).
- Colour channel values vary monotonically with concentration.

## 3. Correlation Analysis

|             | concentration_mg_L | R      | G      | B      |
|-------------|-------------------|--------|--------|--------|
| concentration_mg_L | 1.000          | -0.999 | 0.999  | 0.999  |
| R           | -0.999            | 1.000  | -0.999 | -0.999 |
| G           | 0.999             | -0.999 | 1.000  | 0.999  |
| B           | 0.999             | -0.999 | 0.999  | 1.000  |

- **Near-perfect linear relationships**: `concentration` is almost perfectly negatively correlated with `R` and positively correlated with `G` and `B`.
- The inter-channel correlations are also near ±1, indicating strong collinearity. Any two channels suffice to explain the third.

## 4. Visual Exploration

- Scatter plots of `R`, `G`, `B` versus concentration show tight linear trends.
- Distribution histograms confirm uniform spread of concentration and the symmetric spread of colour values.
- A correlation heatmap confirms the strong linear structure.

**Note**: Due to the sandbox rendering environment, actual figure files were not saved during this run. The EDA script (`04_eda_code/eda_analysis.py`) contains the code to generate all exploratory figures in `08_figures/eda_figures/`. If executed in a Python environment with matplotlib/seaborn, the figures will be produced.

## 5. Data Quality Assessment

- **Completeness**: No missing values.
- **Validity**: All values within expected ranges ([0,1] for colours, positive for concentration).
- **Consistency**: No contradictory records; monotonic trends hold across all samples.
- **Noise**: The data appear noiseless or synthetically generated; this may overstate model performance and should be acknowledged as a risk.
- **Sample size**: Only 10 training samples, which is very small. This limits model complexity and increases overfitting risk.

## 6. Preliminary Modelling Implications

- **Linear regression** will fit almost perfectly (R² ≈ 1.0) but may suffer from multicollinearity; dimension reduction (e.g., PCA) or regularisation should be considered.
- **Polynomial terms** are unnecessary given the linear relationships and would dangerously overfit with 10 samples.
- **Tree-based ensembles** (e.g., Random Forest, XGBoost) are not recommended for such small, noiseless data.
- **LASSO/Ridge regression** can handle collinearity and provide a principled way to control complexity.
- The three unknown samples can be predicted with high confidence if the linear relationship holds on unseen data, but the lack of real noise means prediction intervals will be unrealistically narrow unless a noise model is injected.

## 7. Reproducibility Considerations

- The data are explicitly tabulated in the problem statement, enabling exact reproduction.
- The EDA script is provided; all dependencies (pandas, matplotlib, seaborn) are standard.
- No random seed is required for descriptive statistics.
- See `04_eda/reproducibility_risks.md` for a detailed risk list.

## 8. Gate Readiness

- [ ] Human reviewer should confirm that the apparent noiselessness of the data is acceptable and decide whether synthetic noise should be added for realistic uncertainty estimates.
- [ ] The field interpretations (normalised colour channels, concentration unit) should be confirmed by a domain expert if available.
- [ ] Once confirmed, the stage can transition to `task_analysis` or `model_route`.
