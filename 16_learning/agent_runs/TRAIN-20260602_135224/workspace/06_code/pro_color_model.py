from __future__ import annotations

STANDARD_SAMPLES = "see 03_data/raw/color_concentration_samples.csv"

def linear_prediction(r: float, g: float, b: float) -> float:
    return 4.92 - 6.12 * r + 3.44 * g + 2.31 * b

def ensemble_prediction(r: float, g: float, b: float) -> float:
    linear = linear_prediction(r, g, b)
    poly = linear + 0.18 * (1 - r) * (g + b) - 0.04
    monotone = 5.03 * (1 - r) + 0.88 * g + 0.42 * b - 0.19
    return 0.50 * linear + 0.30 * poly + 0.20 * monotone
