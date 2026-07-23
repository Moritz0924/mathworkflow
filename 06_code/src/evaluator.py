from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

from .constants import GRAVITY_MPS2, SMOKE_RADIUS_M
from .dynamics import detonation_point, missile_position, release_point, smoke_center, smoke_valid_end_time
from .entities import BombEvaluation, BombPlan
from .intervals import find_true_intervals, find_true_intervals_fixed_grid, interval_duration
from .occlusion import fraction_points_occluded, is_all_points_occluded
from .target_geometry import target_sample_points


@dataclass(frozen=True)
class EvaluatorConfig:
    angular_samples: int = 12
    height_samples: int = 3
    radial_samples: int = 2
    scan_step_s: float = 0.1
    root_tolerance_s: float = 1e-5
    gravity_mps2: float = GRAVITY_MPS2
    bomb_horizontal_velocity_factor: float = 1.0
    smoke_ground_mode: str = "terminate"
    interval_method: str = "refined"
    min_coverage_fraction: float = 1.0


def evaluate_plan(
    plan: BombPlan,
    missile_id: str,
    config: EvaluatorConfig,
    *,
    points: Iterable[tuple[float, float, float]] | None = None,
) -> BombEvaluation:
    if not plan.is_used:
        return BombEvaluation(plan, None, None, plan.detonation_time_s, (), 0.0)
    evaluation_points = tuple(points) if points is not None else target_sample_points(
        config.angular_samples, config.height_samples, config.radial_samples
    )
    if not 0.0 <= config.min_coverage_fraction <= 1.0:
        raise ValueError("min_coverage_fraction must be between 0 and 1")
    valid_end_s = smoke_valid_end_time(
        plan,
        missile_id,
        gravity_mps2=config.gravity_mps2,
        horizontal_velocity_factor=config.bomb_horizontal_velocity_factor,
        smoke_ground_mode=config.smoke_ground_mode,
    )
    if valid_end_s <= plan.detonation_time_s:
        intervals: list[tuple[float, float]] = []
    else:
        def is_occluded_at(time_s: float) -> bool:
            missile = missile_position(missile_id, time_s)
            smoke = smoke_center(
                plan,
                time_s,
                gravity_mps2=config.gravity_mps2,
                horizontal_velocity_factor=config.bomb_horizontal_velocity_factor,
                smoke_ground_mode=config.smoke_ground_mode,
            )
            if config.min_coverage_fraction == 1.0:
                return is_all_points_occluded(missile, evaluation_points, smoke, SMOKE_RADIUS_M)
            return (
                fraction_points_occluded(missile, evaluation_points, smoke, SMOKE_RADIUS_M)
                >= config.min_coverage_fraction
            )

        if config.interval_method == "refined":
            intervals = find_true_intervals(
                is_occluded_at,
                plan.detonation_time_s,
                valid_end_s,
                scan_step_s=config.scan_step_s,
                tolerance_s=config.root_tolerance_s,
            )
        elif config.interval_method == "fixed_grid":
            intervals = find_true_intervals_fixed_grid(
                is_occluded_at,
                plan.detonation_time_s,
                valid_end_s,
                scan_step_s=config.scan_step_s,
            )
        else:
            raise ValueError("interval_method must be 'refined' or 'fixed_grid'")
    release = tuple(float(value) for value in release_point(plan))
    detonation = tuple(
        float(value)
        for value in detonation_point(
            plan,
            gravity_mps2=config.gravity_mps2,
            horizontal_velocity_factor=config.bomb_horizontal_velocity_factor,
        )
    )
    return BombEvaluation(
        plan=plan,
        release_point_xyz=release,
        detonation_point_xyz=detonation,
        smoke_valid_end_s=valid_end_s,
        occlusion_intervals=tuple(intervals),
        effective_duration_s=interval_duration(intervals),
    )


def evaluate_q1(config: EvaluatorConfig) -> BombEvaluation:
    plan = BombPlan(
        uav_id="FY1",
        bomb_id=1,
        missile_id="M1",
        is_used=True,
        heading_rad=math.pi,
        speed_mps=120.0,
        release_time_s=1.5,
        delay_s=3.6,
    )
    return evaluate_plan(plan, "M1", config)
