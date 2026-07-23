from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = ROOT / "06_code"
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from run_all import run_pipeline  # noqa: E402
from src.entities import BombPlan  # noqa: E402
from src.evaluator import EvaluatorConfig  # noqa: E402
from src.result_freeze import independently_evaluate_plans, select_q5_assignment  # noqa: E402
from src.solvers import SolverConfig  # noqa: E402


VALIDATION_ROOT = ROOT / "07_results" / "result_freeze_validation"


def _solver_config(
    *,
    seed: int,
    angular_samples: int = 12,
    height_samples: int = 3,
    radial_samples: int = 2,
    scan_step_s: float = 0.1,
    root_tolerance_s: float = 1e-5,
    maxiter: int = 6,
    popsize: int = 5,
    local_refinement: bool = True,
) -> SolverConfig:
    return SolverConfig(
        evaluator=EvaluatorConfig(
            angular_samples=angular_samples,
            height_samples=height_samples,
            radial_samples=radial_samples,
            scan_step_s=scan_step_s,
            root_tolerance_s=root_tolerance_s,
        ),
        differential_evolution_maxiter=maxiter,
        differential_evolution_popsize=popsize,
        local_refinement=local_refinement,
        random_seed=seed,
    )


def _read_plans(path: Path) -> tuple[BombPlan, ...]:
    plans: list[BombPlan] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            is_used = str(row["is_used"]).strip() == "1"
            plans.append(
                BombPlan(
                    uav_id=row["uav_id"],
                    bomb_id=int(row["bomb_id"]),
                    missile_id=row["missile_id"] or None,
                    is_used=is_used,
                    heading_rad=float(row["heading_deg"] or 0.0) * 3.141592653589793 / 180.0,
                    speed_mps=float(row["speed_mps"] or 0.0),
                    release_time_s=float(row["release_time_s"] or 0.0),
                    delay_s=float(row["delay_s"] or 0.0),
                )
            )
    return tuple(plans)


def _read_metric_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: Iterable[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _metric_rows_from_recomputation(
    scenario: str,
    question_id: str,
    recomputation: dict[str, object],
) -> list[dict[str, object]]:
    intervals = recomputation["merged_intervals"]
    durations = recomputation["primary_durations_s"]
    return [
        {
            "scenario": scenario,
            "question_id": question_id,
            "missile_id": missile_id,
            "metric_name": f"primary_duration_{missile_id}",
            "metric_value_s": duration,
            "merged_intervals": json.dumps(intervals[missile_id], ensure_ascii=False),
            "constraint_issues": ";".join(recomputation["constraint_issues"]),
        }
        for missile_id, duration in durations.items()
    ]


def _plans_by_question(run_dir: Path) -> dict[str, tuple[BombPlan, ...]]:
    return {
        question_id: _read_plans(run_dir / f"{question_id.lower()}_results.csv")
        for question_id in ("Q1", "Q2", "Q3", "Q4", "Q5")
    }


def metric_stability(rows: Iterable[dict[str, object]], seed_scenarios: set[str]) -> dict[str, object]:
    grouped: dict[str, list[float]] = {}
    for row in rows:
        if str(row["scenario"]) not in seed_scenarios:
            continue
        key = f"{row['question_id']}/{row['metric_name']}"
        grouped.setdefault(key, []).append(float(row["metric_value_s"]))
    by_metric = {key: max(values) - min(values) for key, values in grouped.items()}
    return {
        "by_metric": by_metric,
        "maximum_span_s": max(by_metric.values(), default=0.0),
    }


def _assignment_rows(score_matrix: list[dict[str, object]]) -> list[dict[str, object]]:
    scores = {
        (str(row["uav_id"]), str(row["missile_id"])): float(row["effective_duration_s"])
        for row in score_matrix
    }
    uav_ids = tuple(sorted({uav_id for uav_id, _ in scores}))
    missile_ids = ("M1", "M2", "M3")
    selections = {
        "A11_primary_total_then_min": select_q5_assignment(scores, uav_ids, missile_ids),
        "A11_fairness_first": select_q5_assignment(scores, uav_ids, missile_ids, priority="min_then_total"),
        "A12_relaxed_positive_coverage": select_q5_assignment(
            scores,
            uav_ids,
            missile_ids,
            require_positive=False,
        ),
    }
    rows: list[dict[str, object]] = []
    for variant, selection in selections.items():
        if selection is None:
            rows.append(
                {
                    "variant": variant,
                    "assignment": "",
                    "total_duration_s": "",
                    "minimum_duration_s": "",
                    "require_positive": "",
                    "priority": "",
                }
            )
            continue
        rows.append(
            {
                "variant": variant,
                "assignment": json.dumps(selection["assignment"], ensure_ascii=False, sort_keys=True),
                "total_duration_s": selection["objective"][0],
                "minimum_duration_s": selection["objective"][1],
                "require_positive": selection["require_positive"],
                "priority": selection["priority"],
            }
        )
    return rows


def run_validation(output_root: Path = VALIDATION_ROOT) -> dict[str, object]:
    output_root.mkdir(parents=True, exist_ok=True)
    scenarios = {
        "seed_20250722": _solver_config(seed=20250722),
        "seed_20250723": _solver_config(seed=20250723),
        "seed_20250724": _solver_config(seed=20250724),
        "budget_plus": _solver_config(seed=20250722, maxiter=12, popsize=8),
        "refined": _solver_config(
            seed=20250722,
            angular_samples=16,
            height_samples=4,
            radial_samples=3,
            scan_step_s=0.05,
            root_tolerance_s=1e-6,
            maxiter=12,
            popsize=8,
        ),
    }
    manifests: dict[str, dict[str, object]] = {}
    convergence_rows: list[dict[str, object]] = []
    for name, config in scenarios.items():
        run_dir = output_root / "runs" / name
        manifest = run_pipeline(output_dir=run_dir, solver_config=config, export_templates=False)
        manifests[name] = manifest
        for metric in _read_metric_rows(run_dir / "metrics_summary.csv"):
            convergence_rows.append(
                {
                    "scenario": name,
                    "question_id": metric["question_id"],
                    "metric_name": metric["metric_name"],
                    "metric_value_s": metric["metric_value"],
                    "seed": config.random_seed,
                    "angular_samples": config.evaluator.angular_samples,
                    "height_samples": config.evaluator.height_samples,
                    "radial_samples": config.evaluator.radial_samples,
                    "scan_step_s": config.evaluator.scan_step_s,
                    "root_tolerance_s": config.evaluator.root_tolerance_s,
                    "maxiter": config.differential_evolution_maxiter,
                    "popsize": config.differential_evolution_popsize,
                    "local_refinement": config.local_refinement,
                }
            )
    _write_csv(
        output_root / "convergence_and_stability.csv",
        convergence_rows,
        [
            "scenario",
            "question_id",
            "metric_name",
            "metric_value_s",
            "seed",
            "angular_samples",
            "height_samples",
            "radial_samples",
            "scan_step_s",
            "root_tolerance_s",
            "maxiter",
            "popsize",
            "local_refinement",
        ],
    )

    primary_plans = _plans_by_question(output_root / "runs" / "refined")
    strict_config = EvaluatorConfig(
        angular_samples=20,
        height_samples=5,
        radial_samples=4,
        scan_step_s=0.025,
        root_tolerance_s=1e-7,
    )
    primary_recomputations = {
        question_id: independently_evaluate_plans(question_id, plans, strict_config)
        for question_id, plans in primary_plans.items()
    }
    primary_rows = [
        row
        for question_id, recomputation in primary_recomputations.items()
        for row in _metric_rows_from_recomputation("primary_strict_recomputation", question_id, recomputation)
    ]
    _write_csv(
        output_root / "primary_recomputation.csv",
        primary_rows,
        ["scenario", "question_id", "missile_id", "metric_name", "metric_value_s", "merged_intervals", "constraint_issues"],
    )

    plan_rows: list[dict[str, object]] = []
    for question_id, recomputation in primary_recomputations.items():
        by_plan = {(evaluation.plan.uav_id, evaluation.plan.bomb_id): evaluation for evaluation in recomputation["evaluations"]}
        issues = ";".join(recomputation["constraint_issues"])
        for plan in primary_plans[question_id]:
            evaluation = by_plan.get((plan.uav_id, plan.bomb_id))
            plan_rows.append(
                {
                    "question_id": question_id,
                    "uav_id": plan.uav_id,
                    "bomb_id": plan.bomb_id,
                    "is_used": int(plan.is_used),
                    "missile_id": plan.missile_id or "",
                    "heading_deg": plan.heading_rad * 180.0 / 3.141592653589793 if plan.is_used else "",
                    "speed_mps": plan.speed_mps if plan.is_used else "",
                    "release_time_s": plan.release_time_s if plan.is_used else "",
                    "delay_s": plan.delay_s if plan.is_used else "",
                    "detonation_time_s": plan.detonation_time_s if plan.is_used else "",
                    "effective_duration_s": evaluation.effective_duration_s if evaluation else "",
                    "occlusion_intervals": json.dumps(evaluation.occlusion_intervals if evaluation else (), ensure_ascii=False),
                    "constraint_issues": issues,
                }
            )
    _write_csv(
        output_root / "plan_validation.csv",
        plan_rows,
        [
            "question_id",
            "uav_id",
            "bomb_id",
            "is_used",
            "missile_id",
            "heading_deg",
            "speed_mps",
            "release_time_s",
            "delay_s",
            "detonation_time_s",
            "effective_duration_s",
            "occlusion_intervals",
            "constraint_issues",
        ],
    )

    sensitivity_specs = {
        "baseline_center_point": (strict_config, ((0.0, 200.0, 5.0),)),
        "baseline_fixed_grid": (replace(strict_config, interval_method="fixed_grid", scan_step_s=0.25), None),
        "A03_no_horizontal_inheritance": (replace(strict_config, bomb_horizontal_velocity_factor=0.0), None),
        "A07_hold_smoke_at_ground": (replace(strict_config, smoke_ground_mode="hold"), None),
        "A08_80pct_coverage": (replace(strict_config, min_coverage_fraction=0.8), None),
    }
    sensitivity_rows = [
        row
        for scenario, (config, points) in sensitivity_specs.items()
        for question_id, plans in primary_plans.items()
        for row in _metric_rows_from_recomputation(
            scenario,
            question_id,
            independently_evaluate_plans(question_id, plans, config, points=points),
        )
    ]
    _write_csv(
        output_root / "baseline_and_sensitivity.csv",
        sensitivity_rows,
        ["scenario", "question_id", "missile_id", "metric_name", "metric_value_s", "merged_intervals", "constraint_issues"],
    )

    assignment_rows = _assignment_rows(manifests["refined"]["q5_diagnostics"]["score_matrix"])
    _write_csv(
        output_root / "q5_assignment_sensitivity.csv",
        assignment_rows,
        ["variant", "assignment", "total_duration_s", "minimum_duration_s", "require_positive", "priority"],
    )

    seed_stability = metric_stability(
        convergence_rows,
        {"seed_20250722", "seed_20250723", "seed_20250724"},
    )
    seed_stability_span = float(seed_stability["maximum_span_s"])
    constraints_clear = all(not recomputation["constraint_issues"] for recomputation in primary_recomputations.values())
    primary_positive = all(
        duration > 0.0
        for recomputation in primary_recomputations.values()
        for duration in recomputation["primary_durations_s"].values()
    )
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "result_status": "candidate_validation",
        "source_run": "refined",
        "strict_evaluation_config": asdict(strict_config),
        "scenario_manifests": manifests,
        "checks": {
            "constraints_clear": constraints_clear,
            "primary_durations_positive": primary_positive,
            "seed_metric_span_s": seed_stability_span,
            "seed_metric_spans_by_output": seed_stability["by_metric"],
            "seed_stability_tolerance_s": 0.05,
            "seed_stable": seed_stability_span <= 0.05,
        },
        "notice": "This validation bundle is evidence for result-freeze review; it does not itself confirm the human result_freeze_gate.",
    }
    (output_root / "validation_summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def refresh_stability_summary(output_root: Path) -> dict[str, object]:
    summary_path = output_root / "validation_summary.json"
    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    stability = metric_stability(
        _read_metric_rows(output_root / "convergence_and_stability.csv"),
        {"seed_20250722", "seed_20250723", "seed_20250724"},
    )
    checks = payload.setdefault("checks", {})
    checks["seed_metric_span_s"] = stability["maximum_span_s"]
    checks["seed_metric_spans_by_output"] = stability["by_metric"]
    checks["seed_stable"] = float(stability["maximum_span_s"]) <= float(checks["seed_stability_tolerance_s"])
    payload["summary_refreshed_at"] = datetime.now(timezone.utc).isoformat()
    summary_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run reproducible result-freeze validation scenarios.")
    parser.add_argument("--output", default=str(VALIDATION_ROOT), help="Directory for candidate validation evidence.")
    parser.add_argument("--refresh-summary-only", action="store_true", help="Refresh stability fields from existing evidence files.")
    args = parser.parse_args()
    payload = refresh_stability_summary(Path(args.output)) if args.refresh_summary_only else run_validation(Path(args.output))
    print(json.dumps(payload["checks"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
