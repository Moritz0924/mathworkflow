from __future__ import annotations

from itertools import permutations
from typing import Iterable, Mapping, Sequence

from .constraints import validate_plans
from .entities import BombPlan
from .evaluator import EvaluatorConfig, evaluate_plan
from .intervals import interval_duration, merge_intervals


def select_q5_assignment(
    scores: Mapping[tuple[str, str], float],
    uav_ids: Sequence[str],
    missile_ids: Sequence[str],
    *,
    priority: str = "total_then_min",
    require_positive: bool = True,
) -> dict[str, object] | None:
    """Select a one-UAV-per-primary-target assignment for Q5 sensitivity checks."""
    if priority not in {"total_then_min", "min_then_total"}:
        raise ValueError("priority must be 'total_then_min' or 'min_then_total'")
    if len(missile_ids) > len(uav_ids):
        raise ValueError("each primary target requires a distinct UAV")

    selected: dict[str, object] | None = None
    selected_key: tuple[float, float] | None = None
    for assignment in permutations(uav_ids, len(missile_ids)):
        durations = tuple(float(scores[(uav_id, missile_id)]) for uav_id, missile_id in zip(assignment, missile_ids))
        if require_positive and min(durations) <= 0.0:
            continue
        total = float(sum(durations))
        minimum = float(min(durations))
        objective_key = (total, minimum) if priority == "total_then_min" else (minimum, total)
        if selected_key is None or objective_key > selected_key:
            selected_key = objective_key
            selected = {
                "assignment": {missile_id: uav_id for uav_id, missile_id in zip(assignment, missile_ids)},
                "durations": {missile_id: duration for missile_id, duration in zip(missile_ids, durations)},
                "objective": (total, minimum),
                "priority": priority,
                "require_positive": require_positive,
            }
    return selected


def independently_evaluate_plans(
    question_id: str,
    plans: Iterable[BombPlan],
    config: EvaluatorConfig,
    *,
    points: Iterable[tuple[float, float, float]] | None = None,
) -> dict[str, object]:
    """Recompute every used plan and merge intervals by registered primary target."""
    materialized = tuple(plans)
    evaluations = tuple(
        evaluate_plan(plan, str(plan.missile_id), config, points=points)
        for plan in materialized
        if plan.is_used and plan.missile_id is not None
    )
    merged_intervals: dict[str, tuple[tuple[float, float], ...]] = {}
    primary_durations: dict[str, float] = {}
    for missile_id in sorted({str(plan.missile_id) for plan in materialized if plan.is_used and plan.missile_id}):
        intervals = merge_intervals(
            interval
            for evaluation in evaluations
            if evaluation.plan.missile_id == missile_id
            for interval in evaluation.occlusion_intervals
        )
        merged_intervals[missile_id] = tuple(intervals)
        primary_durations[missile_id] = interval_duration(intervals)
    return {
        "constraint_issues": [issue.code for issue in validate_plans(question_id, materialized)],
        "evaluations": evaluations,
        "merged_intervals": merged_intervals,
        "primary_durations_s": primary_durations,
    }
