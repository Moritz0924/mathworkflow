from __future__ import annotations

import math

import numpy as np

from .constants import TARGET_BASE_CENTER, TARGET_HEIGHT_M, TARGET_RADIUS_M


def target_sample_points(
    angular_samples: int,
    height_samples: int,
    radial_samples: int,
) -> tuple[np.ndarray, ...]:
    if angular_samples < 3:
        raise ValueError("angular_samples must be at least 3")
    if height_samples < 2:
        raise ValueError("height_samples must be at least 2")
    if radial_samples < 1:
        raise ValueError("radial_samples must be at least 1")

    x0, y0, z0 = TARGET_BASE_CENTER
    points: list[np.ndarray] = []
    angles = [2.0 * math.pi * index / angular_samples for index in range(angular_samples)]
    heights = [z0 + TARGET_HEIGHT_M * index / (height_samples - 1) for index in range(height_samples)]

    for height in heights:
        for angle in angles:
            points.append(
                np.array(
                    (x0 + TARGET_RADIUS_M * math.cos(angle), y0 + TARGET_RADIUS_M * math.sin(angle), height),
                    dtype=float,
                )
            )

    for height in (z0, z0 + TARGET_HEIGHT_M):
        points.append(np.array((x0, y0, height), dtype=float))
        for ring in range(1, radial_samples + 1):
            radius = TARGET_RADIUS_M * ring / radial_samples
            for angle in angles:
                points.append(
                    np.array((x0 + radius * math.cos(angle), y0 + radius * math.sin(angle), height), dtype=float)
                )

    unique: dict[tuple[float, float, float], np.ndarray] = {}
    for point in points:
        rounded = tuple(round(float(value), 12) for value in point)
        unique[rounded] = np.array(rounded, dtype=float)
    return tuple(unique[key] for key in sorted(unique))
