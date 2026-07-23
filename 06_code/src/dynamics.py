from __future__ import annotations

import math

import numpy as np

from .constants import (
    GRAVITY_MPS2,
    MISSILES,
    SMOKE_LIFETIME_S,
    SMOKE_SINK_SPEED_MPS,
    UAVS,
)
from .entities import BombPlan


E_Z = np.array((0.0, 0.0, 1.0), dtype=float)


def _vector(values: tuple[float, float, float]) -> np.ndarray:
    return np.asarray(values, dtype=float)


def horizontal_direction(heading_rad: float) -> np.ndarray:
    direction = np.array((math.cos(heading_rad), math.sin(heading_rad), 0.0), dtype=float)
    direction[np.abs(direction) < 1e-12] = 0.0
    return direction


def missile_hit_time(missile_id: str) -> float:
    missile = MISSILES[missile_id]
    return float(np.linalg.norm(_vector(missile.initial_position)) / missile.speed_mps)


def missile_position(missile_id: str, time_s: float) -> np.ndarray:
    missile = MISSILES[missile_id]
    initial = _vector(missile.initial_position)
    direction = -initial / np.linalg.norm(initial)
    return initial + missile.speed_mps * direction * float(time_s)


def uav_position(uav_id: str, heading_rad: float, speed_mps: float, time_s: float) -> np.ndarray:
    uav = UAVS[uav_id]
    return _vector(uav.initial_position) + float(speed_mps) * horizontal_direction(heading_rad) * float(time_s)


def release_point(plan: BombPlan) -> np.ndarray:
    return uav_position(plan.uav_id, plan.heading_rad, plan.speed_mps, plan.release_time_s)


def bomb_position_before_detonation(
    plan: BombPlan,
    time_s: float,
    gravity_mps2: float = GRAVITY_MPS2,
    horizontal_velocity_factor: float = 1.0,
) -> np.ndarray:
    if time_s < plan.release_time_s:
        raise ValueError("bomb position is undefined before release")
    elapsed = float(time_s) - plan.release_time_s
    horizontal_velocity = plan.speed_mps * horizontal_direction(plan.heading_rad)
    return (
        release_point(plan)
        + float(horizontal_velocity_factor) * horizontal_velocity * elapsed
        - 0.5 * gravity_mps2 * elapsed**2 * E_Z
    )


def detonation_point(
    plan: BombPlan,
    gravity_mps2: float = GRAVITY_MPS2,
    horizontal_velocity_factor: float = 1.0,
) -> np.ndarray:
    return bomb_position_before_detonation(
        plan,
        plan.detonation_time_s,
        gravity_mps2,
        horizontal_velocity_factor,
    )


def detonation_altitude(
    plan: BombPlan,
    gravity_mps2: float = GRAVITY_MPS2,
    horizontal_velocity_factor: float = 1.0,
) -> float:
    return float(detonation_point(plan, gravity_mps2, horizontal_velocity_factor)[2])


def maximum_delay_s(uav_id: str, gravity_mps2: float = GRAVITY_MPS2) -> float:
    altitude = UAVS[uav_id].initial_position[2]
    return math.sqrt(2.0 * altitude / gravity_mps2)


def smoke_center(
    plan: BombPlan,
    time_s: float,
    sink_speed_mps: float = SMOKE_SINK_SPEED_MPS,
    gravity_mps2: float = GRAVITY_MPS2,
    horizontal_velocity_factor: float = 1.0,
    smoke_ground_mode: str = "terminate",
) -> np.ndarray:
    if time_s < plan.detonation_time_s:
        raise ValueError("smoke center is undefined before detonation")
    detonation = detonation_point(plan, gravity_mps2, horizontal_velocity_factor)
    sink_distance = sink_speed_mps * (float(time_s) - plan.detonation_time_s)
    if smoke_ground_mode == "hold":
        sink_distance = min(sink_distance, float(detonation[2]))
    elif smoke_ground_mode != "terminate":
        raise ValueError("smoke_ground_mode must be 'terminate' or 'hold'")
    return detonation - sink_distance * E_Z


def smoke_valid_end_time(
    plan: BombPlan,
    missile_id: str,
    *,
    gravity_mps2: float = GRAVITY_MPS2,
    horizontal_velocity_factor: float = 1.0,
    smoke_ground_mode: str = "terminate",
) -> float:
    lifetime_end = plan.detonation_time_s + SMOKE_LIFETIME_S
    missile_end = missile_hit_time(missile_id)
    if smoke_ground_mode == "hold":
        return min(lifetime_end, missile_end)
    if smoke_ground_mode != "terminate":
        raise ValueError("smoke_ground_mode must be 'terminate' or 'hold'")
    ground_time = plan.detonation_time_s + detonation_altitude(
        plan,
        gravity_mps2,
        horizontal_velocity_factor,
    ) / SMOKE_SINK_SPEED_MPS
    return min(lifetime_end, ground_time, missile_end)
