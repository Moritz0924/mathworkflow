# Data Quality Report

## Dataset: Standard Samples (`standard_samples.csv`)

### Completeness
- All 10 rows have complete observations (no NA, NaN, or blank cells).

### Validity
- `concentration_mg_L`: strictly positive, strictly increasing with sample ID.
- R, G, B: all in [0,1], consistent with normalised colour channels.

### Uniqueness
- `sample_id` is unique.
- Colour value triplets are unique across samples.

### Consistency
- Monotonic trends: concentration ↑ ⇒ R ↓, G ↑, B ↑.
- No logical contradictions between numeric values and sample ordering.

### Accuracy
- The exact source of the colour values (instrument, normalisation method) is not documented. Assuming they are direct sensor outputs with no further processing.
- No obvious digitisation artefacts (e.g., excessive rounding).

### Timeliness
- Not applicable; static dataset for modelling exercise.

### Volume
- 10 observations × 4 variables is extremely small. Generalisation ability will be limited. Any model trained on this data should be treated as illustrative.

## Dataset: Unknown Samples (`unknown_samples.csv`)

### Completeness
- All 3 rows complete.

### Validity
- All R, G, B within [0,1]; within the same ranges as standard samples.
- `T01` values (0.77, 0.37, 0.28) fall within the standard sample envelope.
- `T02` (0.58, 0.57, 0.46) also within envelope.
- `T03` (0.45, 0.70, 0.61) within envelope.

### Risk
- No ground truth for unknown samples is available in this file; prediction will be unvalidated unless external truth is later provided.

## Common Issues

1. **Noiseless Data**: The linear relationships are almost perfect (|r| > 0.999). This suggests the data may be synthetically generated from a deterministic formula, or the measurement process has negligible noise. This is a major risk for real-world applicability.
2. **Small Sample Size**: 10 points is insufficient to reliably estimate model variance or to detect non-linearity.
3. **Multicollinearity**: The colour channels are highly correlated, which can inflate coefficient standard errors and make interpretation difficult.
4. **Lack of Domain Context**: We do not know the physical or chemical basis for the relationship; the linear model may be an approximation that fails outside the observed range.

## Recommended Actions

- Confirm with problem owner whether noise should be artificially added to enable more realistic uncertainty quantification.
- Consider collecting more samples if this were a real project.
- When modelling, use regularisation or dimension reduction to address collinearity.
- Document all assumptions transparently in the modelling report.
