# Data Quality Report

**Status: BLOCKED** – No raw data files accessible in `03_data/raw/`.

## Planned Quality Checks (to be executed once data is supplied)

1. **Structural integrity**: row counts, column counts, duplicate records.
2. **Missing values**: per‑variable missing rate, patterns of missingness.
3. **Outlier detection**: IQR‑based for numerical features, frequency‑based for categorical.
4. **Type consistency**: each column matches declared schema.
5. **Temporal/spatial coherence**: if applicable, chronological order of timestamps, geographic identifiers.
6. **Data leakage risks**: presence of future information, IDs that could leak targets.
7. **Balance checks**: class/target distribution, sampling weights.

## Current Risks
- **No data file found**: absolute blocker for any EDA step.
- **Field interpretation unknown**: all semantic meaning must be supplied externally.

## Next Steps
- Human operator must place original data files into `03_data/raw/`.
- Re‑run `04_eda_code/eda_check.py` to populate the quality report.
