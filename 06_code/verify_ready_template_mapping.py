from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READY_ROOT = ROOT / "07_results" / "ready_for_freeze"


def equivalent(expected: object, actual: object) -> bool:
    if expected in (None, ""):
        return actual is None or actual == ""
    try:
        return abs(float(expected) - float(actual)) <= 1e-7
    except (TypeError, ValueError):
        return expected == actual


def main() -> int:
    inputs = json.loads((READY_ROOT / "template_inputs.json").read_text(encoding="utf-8"))
    verification = json.loads((READY_ROOT / "template_mapping_verification.json").read_text(encoding="utf-8"))
    inspections = {item["question_id"]: item["inspection"]["values"] for item in verification["verification"]}
    failures: list[dict[str, object]] = []

    mappings = {
        "Q3": (lambda row: int(row["bomb_id"]) + 1, (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)),
        "Q4": (lambda row: {"FY1": 2, "FY2": 3, "FY3": 4}[row["uav_id"]], (1, 2, 3, 4, 5, 6, 7, 8, 9)),
        "Q5": (
            lambda row: 2 + (int(row["uav_id"].removeprefix("FY")) - 1) * 3 + int(row["bomb_id"]) - 1,
            (1, 2, 4, 5, 6, 7, 8, 9, 10, 11),
        ),
    }
    for question_id, rows in inputs.items():
        row_number, relevant_columns = mappings[question_id]
        table = inspections[question_id]
        for row in rows:
            values = table[row_number(row) - 1]
            if row["is_used"] == "1":
                expected = [
                    row["heading_deg"], row["speed_mps"],
                    *([] if question_id != "Q3" else [int(row["bomb_id"])]),
                    row["release_x_m"], row["release_y_m"], row["release_z_m"],
                    row["detonation_x_m"], row["detonation_y_m"], row["detonation_z_m"], row["effective_duration_s"],
                    *([] if question_id != "Q5" else [row["missile_id"]]),
                ]
                actual = [values[column] for column in relevant_columns]
                for column, expect, got in zip(relevant_columns, expected, actual):
                    if not equivalent(expect, got):
                        failures.append(
                            {
                                "question_id": question_id,
                                "uav_id": row["uav_id"],
                                "bomb_id": row["bomb_id"],
                                "column": column + 1,
                                "expected": expect,
                                "actual": got,
                            }
                        )
            else:
                for column in relevant_columns:
                    if values[column] is not None:
                        failures.append(
                            {
                                "question_id": question_id,
                                "uav_id": row["uav_id"],
                                "bomb_id": row["bomb_id"],
                                "column": column + 1,
                                "expected": None,
                                "actual": values[column],
                            }
                        )
    payload = {"status": "pass" if not failures else "fail", "failure_count": len(failures), "failures": failures}
    (READY_ROOT / "template_mapping_check.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
