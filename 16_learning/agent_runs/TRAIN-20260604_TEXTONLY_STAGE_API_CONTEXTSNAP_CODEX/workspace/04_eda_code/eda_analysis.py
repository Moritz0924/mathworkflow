#!/usr/bin/env python3
"""
EDA script for the "Colour and Concentration Identification" problem.
Generates descriptive statistics, correlation analysis, and exploratory plots.
"""
import pandas as pd
import numpy as np
import os
import sys

# Add project root if needed
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Paths
DATA_DIR = os.path.join('..', '03_data', 'raw')
FIG_DIR = os.path.join('..', '08_figures', 'eda_figures')
os.makedirs(FIG_DIR, exist_ok=True)

# Load data
standard = pd.read_csv(os.path.join(DATA_DIR, 'standard_samples.csv'))
unknown  = pd.read_csv(os.path.join(DATA_DIR, 'unknown_samples.csv'))

print("=== Standard Samples ===")
print(standard.describe())
print("\n=== Unknown Samples ===")
print(unknown.describe())

# Correlation matrix
corr = standard[['concentration_mg_L', 'R', 'G', 'B']].corr()
print("\n=== Correlation Matrix ===")
print(corr.round(3))

# Try to generate plots; if backends unavailable, exit gracefully
try:
    import matplotlib
    matplotlib.use('Agg')  # non-interactive backend
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_style("whitegrid")

    # 1. Scatter matrix
    g = sns.pairplot(standard, x_vars=['R','G','B'], y_vars=['concentration_mg_L'],
                     height=3, aspect=1.2)
    g.fig.suptitle('Colour channels vs Concentration', y=1.02)
    g.savefig(os.path.join(FIG_DIR, 'scatter_vs_concentration.png'), dpi=150)
    plt.close('all')

    # 2. Correlation heatmap
    plt.figure(figsize=(6,5))
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, square=True)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'correlation_heatmap.png'), dpi=150)
    plt.close('all')

    # 3. Distributions
    fig, axes = plt.subplots(2, 2, figsize=(8,6))
    for ax, col in zip(axes.flat, ['concentration_mg_L', 'R', 'G', 'B']):
        ax.hist(standard[col], bins=6, alpha=0.7, color='steelblue', edgecolor='white')
        ax.set_title(f'Distribution of {col}')
    plt.suptitle('Standard Sample Distributions', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'distributions.png'), dpi=150)
    plt.close('all')

    print(f"\nFigures saved to {FIG_DIR}")
except Exception as e:
    print(f"\nFigure generation skipped: {e}")
    print("Descriptive analysis continues.")

# Save summary statistics to markdown table
summary = standard.describe().T
summary.to_csv(os.path.join('..', '04_eda', 'summary_stats.csv'))

print("\nEDA complete.")
