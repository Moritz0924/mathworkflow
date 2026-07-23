from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATION_ROOT = ROOT / "07_results" / "result_freeze_validation"
SOURCE_RUN = VALIDATION_ROOT / "runs" / "refined"
READY_ROOT = ROOT / "07_results" / "ready_for_freeze"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run() -> dict[str, object]:
    READY_ROOT.mkdir(parents=True, exist_ok=True)
    freeze_id = f"RF-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    plan_rows = read_csv(VALIDATION_ROOT / "plan_validation.csv")
    strict_by_plan = {
        (row["question_id"], row["uav_id"], row["bomb_id"]): row
        for row in plan_rows
    }
    template_inputs: dict[str, list[dict[str, object]]] = {"Q3": [], "Q4": [], "Q5": []}
    mapping_rows: list[dict[str, object]] = []
    source_map_rows: list[dict[str, object]] = []

    for question_id in ("Q1", "Q2", "Q3", "Q4", "Q5"):
        source_rows = read_csv(SOURCE_RUN / f"{question_id.lower()}_results.csv")
        fields = list(source_rows[0])
        ready_rows: list[dict[str, object]] = []
        for source in source_rows:
            key = (question_id, source["uav_id"], source["bomb_id"])
            strict = strict_by_plan[key]
            row = dict(source)
            row["effective_duration_s"] = strict["effective_duration_s"]
            row["occlusion_intervals"] = strict["occlusion_intervals"]
            row["result_status"] = "ready"
            ready_rows.append(row)
            if question_id in template_inputs:
                template_inputs[question_id].append(row)
        output_path = READY_ROOT / f"{question_id.lower()}_results.csv"
        write_csv(output_path, ready_rows, fields)
        source_map_rows.append(
            {
                "result_id": f"ready_{question_id.lower()}_plans",
                "question_id": question_id,
                "source_file": output_path.relative_to(ROOT).as_posix(),
                "result_status": "ready",
                "producing_run_id": freeze_id,
                "source_candidate_run": "result_freeze_validation/runs/refined",
            }
        )

    metrics_source = read_csv(VALIDATION_ROOT / "primary_recomputation.csv")
    metrics_rows: list[dict[str, object]] = []
    q5_durations: dict[str, float] = {}
    for source in metrics_source:
        row = {
            "question_id": source["question_id"],
            "metric_name": source["metric_name"],
            "metric_value": source["metric_value_s"],
            "unit": "s",
            "result_status": "ready",
            "source_record": f"{source['question_id']}/{source['missile_id']}",
        }
        metrics_rows.append(row)
        if source["question_id"] == "Q5":
            q5_durations[source["missile_id"]] = float(source["metric_value_s"])
    metrics_rows.extend(
        [
            {
                "question_id": "Q5",
                "metric_name": "objective_total_duration",
                "metric_value": sum(q5_durations.values()),
                "unit": "s",
                "result_status": "ready",
                "source_record": "Q5/M1;M2;M3",
            },
            {
                "question_id": "Q5",
                "metric_name": "objective_minimum_duration",
                "metric_value": min(q5_durations.values()),
                "unit": "s",
                "result_status": "ready",
                "source_record": "Q5/M1;M2;M3",
            },
        ]
    )
    write_csv(
        READY_ROOT / "metrics_summary.csv",
        metrics_rows,
        ["question_id", "metric_name", "metric_value", "unit", "result_status", "source_record"],
    )
    write_csv(
        READY_ROOT / "result_source_map.csv",
        source_map_rows,
        ["result_id", "question_id", "source_file", "result_status", "producing_run_id", "source_candidate_run"],
    )

    row_mapping = {
        "Q3": lambda row: int(row["bomb_id"]) + 1,
        "Q4": lambda row: {"FY1": 2, "FY2": 3, "FY3": 4}[str(row["uav_id"])],
        "Q5": lambda row: 2 + (int(row["uav_id"].removeprefix("FY")) - 1) * 3 + int(row["bomb_id"]) - 1,
    }
    for question_id, rows in template_inputs.items():
        template_name = {"Q3": "result1.xlsx", "Q4": "result2.xlsx", "Q5": "result3.xlsx"}[question_id]
        for row in rows:
            mapping_rows.append(
                {
                    "question_id": question_id,
                    "template_file": template_name,
                    "template_row": row_mapping[question_id](row),
                    "uav_id": row["uav_id"],
                    "bomb_id": row["bomb_id"],
                    "is_used": row["is_used"],
                    "missile_id": row["missile_id"],
                    "heading_deg": row["heading_deg"],
                    "speed_mps": row["speed_mps"],
                    "effective_duration_s": row["effective_duration_s"],
                }
            )
    write_csv(
        READY_ROOT / "template_mapping_expected.csv",
        mapping_rows,
        [
            "question_id",
            "template_file",
            "template_row",
            "uav_id",
            "bomb_id",
            "is_used",
            "missile_id",
            "heading_deg",
            "speed_mps",
            "effective_duration_s",
        ],
    )
    (READY_ROOT / "template_inputs.json").write_text(json.dumps(template_inputs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    validation = json.loads((VALIDATION_ROOT / "validation_summary.json").read_text(encoding="utf-8"))
    manifest = {
        "freeze_id": freeze_id,
        "result_status": "ready",
        "human_gate": "result_freeze_gate",
        "human_gate_status": "pending",
        "source_candidate_run": "07_results/result_freeze_validation/runs/refined",
        "strict_recomputation": "07_results/result_freeze_validation/primary_recomputation.csv",
        "questions": ["Q1", "Q2", "Q3", "Q4", "Q5"],
        "validation_checks": validation["checks"],
        "notice": "Prepared for human result-freeze review. No AI has confirmed the human gate.",
    }
    (READY_ROOT / "ready_for_freeze_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
