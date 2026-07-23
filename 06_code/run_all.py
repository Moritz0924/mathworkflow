from __future__ import annotations

import argparse
import csv
import importlib.metadata
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import yaml

from src.entities import BombEvaluation, BombPlan
from src.evaluator import EvaluatorConfig, evaluate_q1
from src.exporters import export_candidate_template
from src.solvers import CandidateSolution, SolverConfig, solve_q2, solve_q3, solve_q4, solve_q5


ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = ROOT / "06_code"
DEFAULT_OUTPUT_DIR = ROOT / "07_results"
CONFIG_PATH = CODE_ROOT / "solver_config.yaml"
EXECUTION_LOG = CODE_ROOT / "execution_log.md"


def _read_config(quick: bool) -> SolverConfig:
    raw = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}
    section = raw["quick" if quick else "candidate"]
    target = section["target"]
    timing = section["time_evaluation"]
    optimization = section["optimization"]
    return SolverConfig(
        evaluator=EvaluatorConfig(
            angular_samples=int(target["angular_samples"]),
            height_samples=int(target["height_samples"]),
            radial_samples=int(target["radial_samples"]),
            scan_step_s=float(timing["scan_step_s"]),
            root_tolerance_s=float(timing["root_tolerance_s"]),
        ),
        differential_evolution_maxiter=int(optimization["maxiter"]),
        differential_evolution_popsize=int(optimization["popsize"]),
        local_refinement=bool(optimization["local_refinement"]),
        random_seed=int(optimization["random_seed"]),
    )


def _as_q1_solution(evaluation: BombEvaluation) -> CandidateSolution:
    return CandidateSolution(
        question_id="Q1",
        plans=(evaluation.plan,),
        evaluations=(evaluation,),
        primary_durations_s={"M1": evaluation.effective_duration_s},
        objective=(evaluation.effective_duration_s,),
        diagnostics={"solver": "fixed_strategy_evaluation", "feasible": True},
    )


def _evaluation_map(evaluations: Iterable[BombEvaluation]) -> dict[tuple[str, int], BombEvaluation]:
    return {(evaluation.plan.uav_id, evaluation.plan.bomb_id): evaluation for evaluation in evaluations}


def _write_solution_csv(path: Path, solution: CandidateSolution) -> None:
    evaluation_by_key = _evaluation_map(solution.evaluations)
    fields = [
        "question_id",
        "uav_id",
        "bomb_id",
        "missile_id",
        "is_used",
        "heading_deg",
        "speed_mps",
        "release_time_s",
        "delay_s",
        "detonation_time_s",
        "release_x_m",
        "release_y_m",
        "release_z_m",
        "detonation_x_m",
        "detonation_y_m",
        "detonation_z_m",
        "effective_duration_s",
        "occlusion_intervals",
        "result_status",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for plan in solution.plans:
            evaluation = evaluation_by_key.get((plan.uav_id, plan.bomb_id))
            release = evaluation.release_point_xyz if evaluation else (None, None, None)
            detonation = evaluation.detonation_point_xyz if evaluation else (None, None, None)
            writer.writerow(
                {
                    "question_id": solution.question_id,
                    "uav_id": plan.uav_id,
                    "bomb_id": plan.bomb_id,
                    "missile_id": plan.missile_id or "",
                    "is_used": int(plan.is_used),
                    "heading_deg": (plan.heading_rad * 180.0 / 3.141592653589793) % 360.0 if plan.is_used else "",
                    "speed_mps": plan.speed_mps if plan.is_used else "",
                    "release_time_s": plan.release_time_s if plan.is_used else "",
                    "delay_s": plan.delay_s if plan.is_used else "",
                    "detonation_time_s": plan.detonation_time_s if plan.is_used else "",
                    "release_x_m": release[0],
                    "release_y_m": release[1],
                    "release_z_m": release[2],
                    "detonation_x_m": detonation[0],
                    "detonation_y_m": detonation[1],
                    "detonation_z_m": detonation[2],
                    "effective_duration_s": evaluation.effective_duration_s if evaluation else "",
                    "occlusion_intervals": json.dumps(evaluation.occlusion_intervals if evaluation else (), ensure_ascii=False),
                    "result_status": "candidate",
                }
            )


def _write_metrics(path: Path, solutions: Iterable[CandidateSolution]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["question_id", "metric_name", "metric_value", "unit", "result_status"])
        writer.writeheader()
        for solution in solutions:
            for missile_id, duration in solution.primary_durations_s.items():
                writer.writerow(
                    {
                        "question_id": solution.question_id,
                        "metric_name": f"primary_duration_{missile_id}",
                        "metric_value": duration,
                        "unit": "s",
                        "result_status": "candidate",
                    }
                )
            for index, value in enumerate(solution.objective, start=1):
                writer.writerow(
                    {
                        "question_id": solution.question_id,
                        "metric_name": f"objective_{index}",
                        "metric_value": value,
                        "unit": "s",
                        "result_status": "candidate",
                    }
                )


def _versions() -> dict[str, str]:
    return {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "pandas", "openpyxl", "PyYAML")}


def run_pipeline(
    *,
    quick: bool = True,
    output_dir: Path | None = None,
    solver_config: SolverConfig | None = None,
    export_templates: bool = True,
) -> dict[str, object]:
    output = Path(output_dir or DEFAULT_OUTPUT_DIR)
    output.mkdir(parents=True, exist_ok=True)
    config = solver_config or _read_config(quick)
    solutions = [
        _as_q1_solution(evaluate_q1(config.evaluator)),
        solve_q2(config),
        solve_q3(config),
        solve_q4(config),
        solve_q5(config),
    ]
    for solution in solutions:
        _write_solution_csv(output / f"{solution.question_id.lower()}_results.csv", solution)
    _write_metrics(output / "metrics_summary.csv", solutions)
    if export_templates:
        for solution in solutions:
            if solution.question_id in {"Q3", "Q4", "Q5"}:
                template_number = {"Q3": 1, "Q4": 2, "Q5": 3}[solution.question_id]
                export_candidate_template(
                    solution.question_id,
                    solution.plans,
                    solution.evaluations,
                    output / f"result{template_number}_candidate.xlsx",
                )
    source_rows = [
        {
            "result_id": f"candidate_{solution.question_id.lower()}",
            "question_id": solution.question_id,
            "source_file": f"07_results/{solution.question_id.lower()}_results.csv",
            "result_status": "candidate",
            "generated_by": "06_code/run_all.py",
        }
        for solution in solutions
    ]
    with (output / "result_source_map.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(source_rows[0]))
        writer.writeheader()
        writer.writerows(source_rows)
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "result_status": "candidate",
        "mode": "quick" if quick else "candidate",
        "questions": [solution.question_id for solution in solutions],
        "solver_config": {
            "target": config.evaluator.__dict__,
            "differential_evolution_maxiter": config.differential_evolution_maxiter,
            "differential_evolution_popsize": config.differential_evolution_popsize,
            "local_refinement": config.local_refinement,
            "random_seed": config.random_seed,
        },
        "dependencies": _versions(),
        "q5_feasible": bool(solutions[-1].diagnostics.get("feasible")),
        "q5_diagnostics": dict(solutions[-1].diagnostics),
        "notice": "Candidate artifacts are not result-freeze outputs and are not registered in result_contract.csv.",
    }
    (output / "candidate_run_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def _append_execution_log(status: str, output: str, error: str = "") -> None:
    line = "| {run_id} | {time} | {command} | {status} | {output} | {error} | {repair} |\n".format(
        run_id=f"RUN-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        time=datetime.now(timezone.utc).isoformat(),
        command="python 06_code/run_all.py",
        status=status,
        output=output,
        error=error.replace("|", "/"),
        repair="candidate run; no result freeze",
    )
    with EXECUTION_LOG.open("a", encoding="utf-8") as handle:
        handle.write(line)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run candidate smoke-screen solver artifacts.")
    parser.add_argument("--full", action="store_true", help="Use the higher-resolution candidate configuration.")
    args = parser.parse_args()
    try:
        manifest = run_pipeline(quick=not args.full)
        _append_execution_log("success", "07_results/q1_results.csv ... q5_results.csv")
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        _append_execution_log("failed", "", str(exc))
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
