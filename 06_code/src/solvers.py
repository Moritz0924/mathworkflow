from __future__ import annotations

import math
from dataclasses import dataclass
from dataclasses import replace
from itertools import permutations
from typing import Mapping

import numpy as np
from scipy.optimize import differential_evolution, minimize

from .constants import TARGET_BASE_CENTER, TARGET_HEIGHT_M, UAVS, UAV_SPEED_MAX_MPS, UAV_SPEED_MIN_MPS
from .constraints import validate_plans
from .dynamics import maximum_delay_s, missile_hit_time, missile_position
from .entities import BombEvaluation, BombPlan
from .evaluator import EvaluatorConfig, evaluate_plan
from .intervals import interval_duration, merge_intervals


@dataclass(frozen=True)
class SolverConfig:
    evaluator: EvaluatorConfig = EvaluatorConfig()
    differential_evolution_maxiter: int = 8
    differential_evolution_popsize: int = 6
    local_refinement: bool = True
    random_seed: int = 20250701


@dataclass(frozen=True)
class CandidateSolution:
    question_id: str
    plans: tuple[BombPlan, ...]
    evaluations: tuple[BombEvaluation, ...]
    primary_durations_s: Mapping[str, float]
    objective: tuple[float, ...]
    diagnostics: Mapping[str, object]


def _candidate_plan(values: np.ndarray, uav_id: str, missile_id: str, bomb_id: int = 1) -> BombPlan:
    heading, speed, release, delay = (float(value) for value in values)
    return BombPlan(uav_id, bomb_id, missile_id, True, heading % (2.0 * math.pi), speed, release, delay)


def _single_bomb_bounds(uav_id: str, missile_id: str) -> list[tuple[float, float]]:
    return [
        (0.0, 2.0 * math.pi),
        (UAV_SPEED_MIN_MPS, UAV_SPEED_MAX_MPS),
        (0.0, missile_hit_time(missile_id)),
        (0.0, maximum_delay_s(uav_id)),
    ]


def _center_line_seed(question_id: str, uav_id: str, missile_id: str, config: SolverConfig) -> tuple[BombPlan, BombEvaluation] | None:
    uav = UAVS[uav_id]
    target_center = np.array(
        (TARGET_BASE_CENTER[0], TARGET_BASE_CENTER[1], TARGET_BASE_CENTER[2] + TARGET_HEIGHT_M / 2.0), dtype=float
    )
    hit_time = missile_hit_time(missile_id)
    best: tuple[BombPlan, BombEvaluation] | None = None
    for detonation_time in np.linspace(1.0, hit_time - 0.1, 30):
        missile = missile_position(missile_id, float(detonation_time))
        for line_fraction in np.linspace(0.05, 0.95, 19):
            smoke = missile + line_fraction * (target_center - missile)
            drop = uav.initial_position[2] - smoke[2]
            if drop < 0.0:
                continue
            delay = math.sqrt(2.0 * drop / 9.8)
            release = float(detonation_time) - delay
            if release < 0.0:
                continue
            horizontal_velocity = (smoke[:2] - np.asarray(uav.initial_position[:2], dtype=float)) / detonation_time
            speed = float(np.linalg.norm(horizontal_velocity))
            if not UAV_SPEED_MIN_MPS <= speed <= UAV_SPEED_MAX_MPS:
                continue
            plan = BombPlan(
                uav_id,
                1,
                missile_id,
                True,
                math.atan2(float(horizontal_velocity[1]), float(horizontal_velocity[0])) % (2.0 * math.pi),
                speed,
                release,
                delay,
            )
            evaluation = _evaluate_candidate(plan, question_id, config)
            if evaluation is not None and (best is None or evaluation.effective_duration_s > best[1].effective_duration_s):
                best = (plan, evaluation)
    return best


def _evaluate_candidate(plan: BombPlan, question_id: str, config: SolverConfig) -> BombEvaluation | None:
    if validate_plans(question_id, [plan]):
        return None
    return evaluate_plan(plan, str(plan.missile_id), config.evaluator)


def _solve_single_bomb(question_id: str, uav_id: str, missile_id: str, config: SolverConfig) -> CandidateSolution:
    bounds = _single_bomb_bounds(uav_id, missile_id)

    def objective(values: np.ndarray) -> float:
        plan = _candidate_plan(values, uav_id, missile_id)
        evaluation = _evaluate_candidate(plan, question_id, config)
        if evaluation is None:
            return 1_000_000.0 + max(0.0, plan.detonation_time_s - missile_hit_time(missile_id))
        return -evaluation.effective_duration_s

    global_result = differential_evolution(
        objective,
        bounds=bounds,
        maxiter=config.differential_evolution_maxiter,
        popsize=config.differential_evolution_popsize,
        seed=config.random_seed,
        polish=False,
        updating="immediate",
    )
    values = np.asarray(global_result.x, dtype=float)
    if config.local_refinement:
        local_result = minimize(objective, values, method="Powell", bounds=bounds, options={"maxiter": 80})
        if local_result.fun <= global_result.fun:
            values = np.asarray(local_result.x, dtype=float)

    plan = _candidate_plan(values, uav_id, missile_id)
    evaluation = _evaluate_candidate(plan, question_id, config)
    if evaluation is None:
        raise RuntimeError("optimizer returned an infeasible single-bomb candidate")
    center_line_seed = _center_line_seed(question_id, uav_id, missile_id, config)
    if center_line_seed is not None and center_line_seed[1].effective_duration_s > evaluation.effective_duration_s:
        plan, evaluation = center_line_seed
    if uav_id == "FY1" and missile_id == "M1":
        q1_anchor = BombPlan("FY1", 1, "M1", True, math.pi, 120.0, 1.5, 3.6)
        anchor_evaluation = _evaluate_candidate(q1_anchor, question_id, config)
        if anchor_evaluation is not None and anchor_evaluation.effective_duration_s > evaluation.effective_duration_s:
            plan = q1_anchor
            evaluation = anchor_evaluation
    return CandidateSolution(
        question_id=question_id,
        plans=(plan,),
        evaluations=(evaluation,),
        primary_durations_s={missile_id: evaluation.effective_duration_s},
        objective=(evaluation.effective_duration_s,),
        diagnostics={
            "global_method": "differential_evolution",
            "local_method": "Powell" if config.local_refinement else None,
            "random_seed": config.random_seed,
            "global_message": str(global_result.message),
        },
    )


def solve_q2(config: SolverConfig) -> CandidateSolution:
    return _solve_single_bomb("Q2", "FY1", "M1", config)


def _evaluate_same_missile_plans(plans: tuple[BombPlan, ...], missile_id: str, config: SolverConfig) -> tuple[tuple[BombEvaluation, ...], float]:
    evaluations = tuple(evaluate_plan(plan, missile_id, config.evaluator) for plan in plans if plan.is_used)
    intervals = merge_intervals(
        interval
        for evaluation in evaluations
        for interval in evaluation.occlusion_intervals
    )
    return evaluations, interval_duration(intervals)


def solve_q3(config: SolverConfig) -> CandidateSolution:
    hit_time = missile_hit_time("M1")
    max_delay = maximum_delay_s("FY1")
    bounds = [
        (0.0, 2.0 * math.pi),
        (UAV_SPEED_MIN_MPS, UAV_SPEED_MAX_MPS),
        (0.0, hit_time),
        (1.0, hit_time),
        (1.0, hit_time),
        (0.0, max_delay),
        (0.0, max_delay),
        (0.0, max_delay),
    ]

    def decode(values: np.ndarray) -> tuple[BombPlan, ...]:
        heading, speed, first_release, second_gap, third_gap, delay_1, delay_2, delay_3 = (float(value) for value in values)
        releases = (first_release, first_release + second_gap, first_release + second_gap + third_gap)
        delays = (delay_1, delay_2, delay_3)
        return tuple(
            BombPlan("FY1", bomb_id, "M1", True, heading % (2.0 * math.pi), speed, releases[bomb_id - 1], delays[bomb_id - 1])
            for bomb_id in (1, 2, 3)
        )

    def objective(values: np.ndarray) -> float:
        plans = decode(values)
        if validate_plans("Q3", plans):
            return 1_000_000.0 + max(0.0, plans[-1].detonation_time_s - hit_time)
        _, duration = _evaluate_same_missile_plans(plans, "M1", config)
        return -duration

    global_result = differential_evolution(
        objective,
        bounds=bounds,
        maxiter=config.differential_evolution_maxiter,
        popsize=config.differential_evolution_popsize,
        seed=config.random_seed,
        polish=False,
        updating="immediate",
    )
    values = np.asarray(global_result.x, dtype=float)
    if config.local_refinement:
        local_result = minimize(objective, values, method="Powell", bounds=bounds, options={"maxiter": 120})
        if local_result.fun <= global_result.fun:
            values = np.asarray(local_result.x, dtype=float)
    plans = decode(values)
    violations = validate_plans("Q3", plans)
    if violations:
        raise RuntimeError(f"optimizer returned an infeasible Q3 candidate: {violations}")
    evaluations, duration = _evaluate_same_missile_plans(plans, "M1", config)
    anchor_plans = tuple(
        BombPlan("FY1", bomb_id, "M1", True, math.pi, 120.0, 0.5 + bomb_id, 3.6)
        for bomb_id in (1, 2, 3)
    )
    anchor_evaluations, anchor_duration = _evaluate_same_missile_plans(anchor_plans, "M1", config)
    if anchor_duration > duration:
        plans, evaluations, duration = anchor_plans, anchor_evaluations, anchor_duration
    q2_anchor = _solve_single_bomb("Q2", "FY1", "M1", config).plans[0]
    q2_extended_anchor = tuple(
        BombPlan(
            "FY1",
            bomb_id,
            "M1",
            True,
            q2_anchor.heading_rad,
            q2_anchor.speed_mps,
            q2_anchor.release_time_s + bomb_id - 1,
            q2_anchor.delay_s,
        )
        for bomb_id in (1, 2, 3)
    )
    if not validate_plans("Q3", q2_extended_anchor):
        q2_anchor_evaluations, q2_anchor_duration = _evaluate_same_missile_plans(q2_extended_anchor, "M1", config)
        if q2_anchor_duration > duration:
            plans, evaluations, duration = q2_extended_anchor, q2_anchor_evaluations, q2_anchor_duration
    return CandidateSolution(
        question_id="Q3",
        plans=plans,
        evaluations=evaluations,
        primary_durations_s={"M1": duration},
        objective=(duration,),
        diagnostics={
            "global_method": "differential_evolution",
            "local_method": "Powell" if config.local_refinement else None,
            "random_seed": config.random_seed,
            "global_message": str(global_result.message),
        },
    )


def solve_q4(config: SolverConfig) -> CandidateSolution:
    uav_ids = ("FY1", "FY2", "FY3")
    hit_time = missile_hit_time("M1")
    bounds: list[tuple[float, float]] = []
    for uav_id in uav_ids:
        bounds.extend(_single_bomb_bounds(uav_id, "M1"))

    def decode(values: np.ndarray) -> tuple[BombPlan, ...]:
        return tuple(
            _candidate_plan(values[index * 4 : index * 4 + 4], uav_id, "M1")
            for index, uav_id in enumerate(uav_ids)
        )

    def objective(values: np.ndarray) -> float:
        plans = decode(values)
        if validate_plans("Q4", plans):
            latest_detonation = max(plan.detonation_time_s for plan in plans)
            return 1_000_000.0 + max(0.0, latest_detonation - hit_time)
        _, duration = _evaluate_same_missile_plans(plans, "M1", config)
        return -duration

    global_result = differential_evolution(
        objective,
        bounds=bounds,
        maxiter=config.differential_evolution_maxiter,
        popsize=config.differential_evolution_popsize,
        seed=config.random_seed,
        polish=False,
        updating="immediate",
    )
    values = np.asarray(global_result.x, dtype=float)
    if config.local_refinement:
        local_result = minimize(objective, values, method="Powell", bounds=bounds, options={"maxiter": 160})
        if local_result.fun <= global_result.fun:
            values = np.asarray(local_result.x, dtype=float)
    plans = decode(values)
    violations = validate_plans("Q4", plans)
    if violations:
        raise RuntimeError(f"optimizer returned an infeasible Q4 candidate: {violations}")
    evaluations, duration = _evaluate_same_missile_plans(plans, "M1", config)
    anchor_plans = (
        BombPlan("FY1", 1, "M1", True, math.pi, 120.0, 1.5, 3.6),
        BombPlan("FY2", 1, "M1", True, math.pi, 120.0, 1.5, 3.6),
        BombPlan("FY3", 1, "M1", True, math.pi, 120.0, 1.5, 3.6),
    )
    anchor_evaluations, anchor_duration = _evaluate_same_missile_plans(anchor_plans, "M1", config)
    if anchor_duration > duration:
        plans, evaluations, duration = anchor_plans, anchor_evaluations, anchor_duration
    q2_anchor = _solve_single_bomb("Q2", "FY1", "M1", config).plans[0]
    q2_extended_anchor = (
        q2_anchor,
        BombPlan("FY2", 1, "M1", True, math.pi, 120.0, 1.5, 3.6),
        BombPlan("FY3", 1, "M1", True, math.pi, 120.0, 1.5, 3.6),
    )
    if not validate_plans("Q4", q2_extended_anchor):
        q2_anchor_evaluations, q2_anchor_duration = _evaluate_same_missile_plans(q2_extended_anchor, "M1", config)
        if q2_anchor_duration > duration:
            plans, evaluations, duration = q2_extended_anchor, q2_anchor_evaluations, q2_anchor_duration
    return CandidateSolution(
        question_id="Q4",
        plans=plans,
        evaluations=evaluations,
        primary_durations_s={"M1": duration},
        objective=(duration,),
        diagnostics={
            "global_method": "differential_evolution",
            "local_method": "Powell" if config.local_refinement else None,
            "random_seed": config.random_seed,
            "global_message": str(global_result.message),
        },
    )


def _unused_q5_plan(uav_id: str, bomb_id: int) -> BombPlan:
    return BombPlan(uav_id, bomb_id, None, False, 0.0, 0.0, 0.0, 0.0)


def solve_q5(config: SolverConfig) -> CandidateSolution:
    missile_ids = ("M1", "M2", "M3")
    uav_ids = tuple(UAVS)
    single_candidates: dict[tuple[str, str], CandidateSolution] = {}
    scores: dict[tuple[str, str], float] = {}

    for uav_index, uav_id in enumerate(uav_ids):
        for missile_index, missile_id in enumerate(missile_ids):
            pair_config = replace(config, random_seed=config.random_seed + uav_index * len(missile_ids) + missile_index)
            candidate = _solve_single_bomb("Q5", uav_id, missile_id, pair_config)
            single_candidates[(uav_id, missile_id)] = candidate
            scores[(uav_id, missile_id)] = candidate.primary_durations_s[missile_id]

    score_matrix = tuple(
        {
            "uav_id": uav_id,
            "missile_id": missile_id,
            "effective_duration_s": scores[(uav_id, missile_id)],
        }
        for uav_id in uav_ids
        for missile_id in missile_ids
    )

    selected_assignment: tuple[str, str, str] | None = None
    selected_objective = (-math.inf, -math.inf)
    for assignment in permutations(uav_ids, len(missile_ids)):
        durations = tuple(scores[(uav_id, missile_id)] for uav_id, missile_id in zip(assignment, missile_ids))
        if min(durations) <= 0.0:
            continue
        objective = (sum(durations), min(durations))
        if objective > selected_objective:
            selected_assignment = assignment
            selected_objective = objective

    if selected_assignment is None:
        plans = tuple(_unused_q5_plan(uav_id, bomb_id) for uav_id in uav_ids for bomb_id in (1, 2, 3))
        return CandidateSolution(
            question_id="Q5",
            plans=plans,
            evaluations=(),
            primary_durations_s={missile_id: 0.0 for missile_id in missile_ids},
            objective=(0.0, 0.0),
            diagnostics={
                "feasible": False,
                "reason": "No primary-target assignment produced positive coverage for all three missiles under the frozen criterion.",
                "global_method": "differential_evolution",
                "local_method": "Powell" if config.local_refinement else None,
                "random_seed": config.random_seed,
                "score_matrix": score_matrix,
            },
        )

    used_by_uav = {
        uav_id: single_candidates[(uav_id, missile_id)]
        for uav_id, missile_id in zip(selected_assignment, missile_ids)
    }
    plans: list[BombPlan] = []
    evaluations: list[BombEvaluation] = []
    durations: dict[str, float] = {}
    for uav_id in uav_ids:
        selected = used_by_uav.get(uav_id)
        if selected is None:
            plans.extend(_unused_q5_plan(uav_id, bomb_id) for bomb_id in (1, 2, 3))
            continue
        plan = selected.plans[0]
        plans.append(plan)
        plans.extend(_unused_q5_plan(uav_id, bomb_id) for bomb_id in (2, 3))
        evaluations.extend(selected.evaluations)
        durations[str(plan.missile_id)] = selected.primary_durations_s[str(plan.missile_id)]

    for missile_id in missile_ids:
        durations.setdefault(missile_id, 0.0)
    return CandidateSolution(
        question_id="Q5",
        plans=tuple(plans),
        evaluations=tuple(evaluations),
        primary_durations_s=durations,
        objective=(sum(durations.values()), min(durations.values())),
        diagnostics={
            "feasible": all(duration > 0.0 for duration in durations.values()),
            "assignment": {missile_id: uav_id for uav_id, missile_id in zip(selected_assignment, missile_ids)},
            "global_method": "differential_evolution",
            "local_method": "Powell" if config.local_refinement else None,
            "random_seed": config.random_seed,
            "q5_credit_policy": "primary_target_only",
            "score_matrix": score_matrix,
        },
    )
