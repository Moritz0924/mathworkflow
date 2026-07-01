# EDA script (placeholder)
# This script reads raw data and reproduces the quality report statistics.
# It is not executable in the sandbox; serves as documentation.

import pandas as pd

# Load data
orders = pd.read_csv('03_data/raw/orders.csv')
agv = pd.read_csv('03_data/raw/agv_status.csv')
inv = pd.read_csv('03_data/raw/inventory.csv')

# Summary stats
print(orders.describe(include='all'))
print(agv.describe(include='all'))
print(inv.describe(include='all'))

# Missing values
print(orders.isnull().sum())
print(agv.isnull().sum())
print(inv.isnull().sum())

# basic plots (commented out)
# import matplotlib.pyplot as plt
# orders['pick_x'].hist()
# plt.savefig('08_figures/eda_figures/pick_x_hist.png')
