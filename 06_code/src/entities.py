from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


Vector3 = Tuple[float, float, float]


@dataclass(frozen=True)
class Missile:
    missile_id: str
    initial_position: Vector3
    speed_mps: float


@dataclass(frozen=True)
class UAV:
    uav_id: str
    initial_position: Vector3


@dataclass(frozen=True)
class BombPlan:
    uav_id: str
    bomb_id: int
    missile_id: Optional[str]
    is_used: bool
    heading_rad: float
    speed_mps: float
    release_time_s: float
    delay_s: float

    @property
    def detonation_time_s(self) -> float:
        return self.release_time_s + self.delay_s


@dataclass(frozen=True)
class BombEvaluation:
    plan: BombPlan
    release_point_xyz: Optional[Vector3]
    detonation_point_xyz: Optional[Vector3]
    smoke_valid_end_s: float
    occlusion_intervals: Tuple[Tuple[float, float], ...]
    effective_duration_s: float
