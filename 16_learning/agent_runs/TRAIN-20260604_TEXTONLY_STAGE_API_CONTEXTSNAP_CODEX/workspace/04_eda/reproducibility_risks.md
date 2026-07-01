# Reproducibility Risks

## 1. Data Availability
- **Risk**: The standard and unknown sample data are embedded in the problem statement. If the problem statement is altered or lost, the raw data could disappear.
- **Mitigation**: Raw CSV copies are now stored in `03_data/raw/`. The problem statement remains the authoritative source.

## 2. Data Provenance
- **Risk**: The origin of the colour readings (instrument, preprocessing, normalisation) is undocumented. Any modelling conclusions are conditional on the assumption that the data faithfully represent the physical measurement.
- **Mitigation**: State the assumption explicitly in the final paper.

## 3. Environment Dependencies
- **Risk**: The EDA script uses Python 3.8+ with pandas, matplotlib, and seaborn. If these library versions are not pinned, future reproduction may yield different figure styling (not analysis results).
- **Mitigation**: A `requirements.txt` can be added; actual numeric computations do not depend on plotting libraries.

## 4. Figure Generation
- **Risk**: In the current sandbox execution, no actual PNG/SVG files were produced because a graphical backend was not available. The code to generate the figures is provided and can be executed in any standard environment.
- **Mitigation**: Mark figures as exploratory; before final paper, ensure figures are regenerated and registered in `figure_contract.csv`.

## 5. Randomness
- **Risk**: The EDA uses no random processes. The script is deterministic. No seed is required.

## 6. Small Data Leakage
- **Risk**: Using only 10 points, any exploratory split (e.g., train/validation) could leak information if not documented. For now, no split is performed; all 10 points are for modelling.
- **Mitigation**: Future modelling stages should define a clear resampling/cross-validation strategy and record it in the model contract.

## 7. Proprietary or Confidential Data
- **Risk**: The data appear to be a simple academic exercise; no sensitivity is assumed.
- **Mitigation**: Not applicable.

## 8. Long-term Archival
- **Risk**: The raw CSV files may not be sufficient if the problem statement is the actual ground truth. Ensure the CSV matches the problem statement exactly.
- **Mitigation**: A checksum comparison could be implemented; for now, the CSV was created by direct transcription from the problem statement.
