"""
EDA check script – placeholder.
To be run once raw data files are placed in 03_data/raw/.
"""

import os
import sys

DATA_DIR = "03_data/raw"

def main():
    print("Searching for data files...")
    if not os.path.isdir(DATA_DIR):
        print(f"ERROR: Directory '{DATA_DIR}' does not exist.")
        sys.exit(1)
    files = [f for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f))]
    if not files:
        print("ERROR: No data files found. Please add original data and re-run.")
        sys.exit(1)
    print(f"Found {len(files)} file(s): {files}")

    # TO DO: Add pandas read, summary statistics, missing report, outlier checks, correlation matrix, etc.
    # Generate reports under 04_eda/ and charts under 08_figures/eda_figures/

if __name__ == "__main__":
    main()
