from __future__ import annotations

from typing import Iterable, Sequence

import numpy as np


def _array(values: Sequence[float]) -> np.ndarray:
    return np.asarray(values, dtype=float)


def line_of_sight_clearance(
    missile_xyz: Sequence[float],
    target_xyz: Sequence[float],
    smoke_xyz: Sequence[float],
) -> tuple[float, float]:
    missile = _array(missile_xyz)
    target = _array(target_xyz)
    smoke = _array(smoke_xyz)
    sight = target - missile
    denominator = float(np.dot(sight, sight))
    if denominator == 0.0:
        raise ValueError("target point must differ from missile position")
    relative_smoke = smoke - missile
    line_lambda = float(np.dot(relative_smoke, sight) / denominator)
    clearance = float(np.linalg.norm(relative_smoke - line_lambda * sight))
    return line_lambda, clearance


def is_all_points_occluded(
    missile_xyz: Sequence[float],
    target_points: Iterable[Sequence[float]],
    smoke_xyz: Sequence[float],
    smoke_radius_m: float,
    *,
    tolerance: float = 1e-10,
) -> bool:
    for target_xyz in target_points:
        line_lambda, clearance = line_of_sight_clearance(missile_xyz, target_xyz, smoke_xyz)
        if line_lambda < -tolerance or line_lambda > 1.0 + tolerance:
            return False
        if clearance > smoke_radius_m + tolerance:
            return False
    return True


def fraction_points_occluded(
    missile_xyz: Sequence[float],
    target_points: Iterable[Sequence[float]],
    smoke_xyz: Sequence[float],
    smoke_radius_m: float,
    *,
    tolerance: float = 1e-10,
) -> float:
    """Return the share of sampled target points whose missile-to-target sight line is blocked."""
    materialized = tuple(target_points)
    if not materialized:
        raise ValueError("target_points must not be empty")
    blocked = 0
    for target_xyz in materialized:
        line_lambda, clearance = line_of_sight_clearance(missile_xyz, target_xyz, smoke_xyz)
        if -tolerance <= line_lambda <= 1.0 + tolerance and clearance <= smoke_radius_m + tolerance:
            blocked += 1
    return blocked / len(materialized)
