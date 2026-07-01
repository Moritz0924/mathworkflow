# Data Dictionary

## Standard Samples (`standard_samples.csv`)

| Field | Type | Description | Unit | Missing | Range/Values |
|---|---|---|---|---|---|
| sample_id | categorical (string) | Standard sample identifier | – | 0/10 | S01–S10 |
| concentration_mg_L | numeric (float) | True substance concentration | mg/L | 0/10 | 0.5–5.0 |
| R | numeric (float) | Normalised red channel intensity | dimensionless [0,1] | 0/10 | 0.39–0.91 |
| G | numeric (float) | Normalised green channel intensity | dimensionless [0,1] | 0/10 | 0.23–0.76 |
| B | numeric (float) | Normalised blue channel intensity | dimensionless [0,1] | 0/10 | 0.18–0.69 |

## Unknown Samples (`unknown_samples.csv`)

| Field | Type | Description | Unit | Missing | Range/Values |
|---|---|---|---|---|---|
| sample_id | categorical (string) | Unknown sample identifier | – | 0/3 | T01–T03 |
| R | numeric (float) | Normalised red channel intensity | dimensionless [0,1] | 0/3 | 0.45–0.77 |
| G | numeric (float) | Normalised green channel intensity | dimensionless [0,1] | 0/3 | 0.37–0.70 |
| B | numeric (float) | Normalised blue channel intensity | dimensionless [0,1] | 0/3 | 0.28–0.61 |

**Notes:**
- All colour values are assumed to be normalised to [0,1]. No further unit conversion is required.
- The standard set contains 10 observations; the unknown set contains 3 observations.
- No missing, duplicate, or out-of-range values are present in the provided data.
