from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

from .constants import MIN_RELEASE_GAP_S, MISSILES, UAVS, UAV_SPEED_MAX_MPS, UAV_SPEED_MIN_MPS
from .dynamics import detonation_altitude, maximum_delay_s, missile_hit_time
from .entities import BombPlan


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    uav_id: str | None = None
    bomb_id: int | None = None


def validate_plans(question_id: str, plans: Iterable[BombPlan]) -> list[ValidationIssue]:
    materialized = list(plans)
    issues: list[ValidationIssue] = []
    by_uav: dict[str, list[BombPlan]] = defaultdict(list)

    for plan in materialized:
        by_uav[plan.uav_id].append(plan)
        if plan.uav_id not in UAVS:
            issues.append(ValidationIssue("unknown_uav", "无人机编号不在题面范围内", plan.uav_id, plan.bomb_id))
            continue
        if plan.is_used:
            if plan.missile_id not in MISSILES:
                issues.append(ValidationIssue("unknown_missile", "已使用弹必须有题面导弹主目标", plan.uav_id, plan.bomb_id))
            if not UAV_SPEED_MIN_MPS <= plan.speed_mps <= UAV_SPEED_MAX_MPS:
                issues.append(ValidationIssue("speed_range", "无人机速度超出70–140 m/s", plan.uav_id, plan.bomb_id))
            if not 0.0 <= plan.heading_rad < 2.0 * math.pi:
                issues.append(ValidationIssue("heading_range", "航向必须在[0, 2π)内", plan.uav_id, plan.bomb_id))
            if plan.release_time_s < 0.0:
                issues.append(ValidationIssue("release_time", "投放时刻必须非负", plan.uav_id, plan.bomb_id))
            if not 0.0 <= plan.delay_s <= maximum_delay_s(plan.uav_id):
                issues.append(ValidationIssue("delay_range", "起爆延迟不满足地面以上起爆约束", plan.uav_id, plan.bomb_id))
            elif detonation_altitude(plan) < -1e-9:
                issues.append(ValidationIssue("detonation_altitude", "起爆点位于地面以下", plan.uav_id, plan.bomb_id))
            if plan.missile_id in MISSILES and plan.detonation_time_s > missile_hit_time(plan.missile_id):
                issues.append(ValidationIssue("detonation_after_hit", "起爆时刻晚于主目标导弹命中时刻", plan.uav_id, plan.bomb_id))

    for uav_id, uav_plans in by_uav.items():
        used = sorted((plan for plan in uav_plans if plan.is_used), key=lambda plan: plan.release_time_s)
        if not used:
            continue
        reference = used[0]
        for plan in used[1:]:
            if not math.isclose(plan.heading_rad, reference.heading_rad, abs_tol=1e-12):
                issues.append(ValidationIssue("shared_heading", "同一无人机的已使用弹必须共享航向", uav_id, plan.bomb_id))
            if not math.isclose(plan.speed_mps, reference.speed_mps, abs_tol=1e-12):
                issues.append(ValidationIssue("shared_speed", "同一无人机的已使用弹必须共享速度", uav_id, plan.bomb_id))
        for previous, current in zip(used, used[1:]):
            if current.release_time_s - previous.release_time_s < MIN_RELEASE_GAP_S - 1e-12:
                issues.append(ValidationIssue("release_gap", "同一无人机相邻投放间隔小于1 s", uav_id, current.bomb_id))

    if question_id == "Q1":
        if len(materialized) != 1:
            issues.append(ValidationIssue("q1_count", "Q1必须恰有一枚干扰弹"))
        elif materialized[0].is_used:
            plan = materialized[0]
            if plan.uav_id != "FY1" or plan.missile_id != "M1":
                issues.append(ValidationIssue("q1_target", "Q1固定为FY1干扰M1", plan.uav_id, plan.bomb_id))
            if not math.isclose(plan.speed_mps, 120.0, abs_tol=1e-12):
                issues.append(ValidationIssue("q1_speed", "Q1速度固定为120 m/s", plan.uav_id, plan.bomb_id))
            if not math.isclose(plan.release_time_s, 1.5, abs_tol=1e-12) or not math.isclose(plan.delay_s, 3.6, abs_tol=1e-12):
                issues.append(ValidationIssue("q1_timing", "Q1投放和起爆延迟必须使用题面固定值", plan.uav_id, plan.bomb_id))

    if question_id == "Q3":
        if len(materialized) != 3 or any(plan.uav_id != "FY1" or plan.missile_id != "M1" for plan in materialized):
            issues.append(ValidationIssue("q3_shape", "Q3必须由FY1的三枚弹干扰M1"))

    if question_id == "Q4":
        expected = {"FY1", "FY2", "FY3"}
        if len(materialized) != 3 or {plan.uav_id for plan in materialized} != expected:
            issues.append(ValidationIssue("q4_shape", "Q4必须由FY1/FY2/FY3各投一枚弹"))

    if question_id == "Q5":
        for uav_id, uav_plans in by_uav.items():
            by_bomb_id = {plan.bomb_id: plan for plan in uav_plans}
            for bomb_id in (2, 3):
                if by_bomb_id.get(bomb_id) and by_bomb_id[bomb_id].is_used and not by_bomb_id.get(bomb_id - 1, BombPlan(uav_id, bomb_id - 1, None, False, 0, 0, 0, 0)).is_used:
                    issues.append(ValidationIssue("q5_prefix_use", "Q5弹位必须按编号前缀使用", uav_id, bomb_id))
    return issues
