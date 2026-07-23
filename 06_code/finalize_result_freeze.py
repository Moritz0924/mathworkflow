from __future__ import annotations

import csv
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
READY_ROOT = ROOT / "07_results" / "ready_for_freeze"
FROZEN_ROOT = ROOT / "07_results" / "frozen"
CONTRACT_ROOT = ROOT / "14_contracts"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def human_gate_event() -> dict[str, object]:
    state = yaml.safe_load((ROOT / "workflow_state.yaml").read_text(encoding="utf-8")) or {}
    for event in reversed(state.get("history") or []):
        if event.get("event") == "human_gate_confirmed" and event.get("stage") == "result_freeze":
            return event
    raise RuntimeError("result_freeze_gate has not been recorded by the controller")


def run() -> dict[str, object]:
    if FROZEN_ROOT.exists():
        raise RuntimeError(f"refusing to overwrite existing frozen package: {FROZEN_ROOT}")
    event = human_gate_event()
    ready_manifest = json.loads((READY_ROOT / "ready_for_freeze_manifest.json").read_text(encoding="utf-8"))
    if ready_manifest.get("result_status") != "ready":
        raise RuntimeError("ready package does not have result_status=ready")
    FROZEN_ROOT.mkdir(parents=True)
    frozen_at = str(event["at"])
    freeze_id = str(ready_manifest["freeze_id"])

    copied_csvs: list[str] = []
    for name in ("q1_results.csv", "q2_results.csv", "q3_results.csv", "q4_results.csv", "q5_results.csv", "metrics_summary.csv", "result_source_map.csv"):
        fields, rows = read_csv(READY_ROOT / name)
        if "result_status" in fields:
            for row in rows:
                row["result_status"] = "frozen"
        write_csv(FROZEN_ROOT / name, fields, rows)
        copied_csvs.append(name)

    copied_files = [
        "result1.xlsx",
        "result2.xlsx",
        "result3.xlsx",
        "template_mapping_check.json",
        "template_mapping_verification.json",
        "template_mapping_expected.csv",
    ]
    for name in copied_files:
        shutil.copy2(READY_ROOT / name, FROZEN_ROOT / name)

    provenance = {
        "freeze_id": freeze_id,
        "result_status": "frozen",
        "human_gate": "result_freeze_gate",
        "human_gate_status": "confirmed",
        "human_gate_confirmed_at": frozen_at,
        "controller_event": event,
        "source_ready_package": "07_results/ready_for_freeze",
        "source_ready_manifest_sha256": sha256(READY_ROOT / "ready_for_freeze_manifest.json"),
        "freeze_process": "06_code/finalize_result_freeze.py",
        "files": copied_csvs + copied_files,
        "contracts_verified": True,
        "template_mapping_status": "pass",
        "notice": "Created after the controller recorded the human result_freeze_gate confirmation; numerical values are copied from the ready package without recalculation or model changes.",
    }
    (FROZEN_ROOT / "frozen_manifest.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (FROZEN_ROOT / "freeze_confirmation.md").write_text(
        "\n".join(
            [
                "# 结果冻结确认记录",
                "",
                f"- freeze_id: `{freeze_id}`",
                "- result_status: `frozen`",
                "- human_gate: `result_freeze_gate`",
                f"- human_gate_confirmed_at: `{frozen_at}`",
                "- confirmation_source: `workflow_state.yaml` controller event",
                "- scope: ready package values, plan records, metrics, and official templates copied without numerical/model alteration.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    result_fields, result_rows = read_csv(CONTRACT_ROOT / "result_contract.csv")
    for row in result_rows:
        if row.get("freeze_status") == "ready":
            row["freeze_status"] = "frozen"
            row["freeze_time"] = frozen_at
            row["source_file"] = "07_results/frozen/metrics_summary.csv"
            row["owner"] = "Human gate confirmed; Codex recorded"
            row["notes"] = f"Frozen after controller event result_freeze_gate at {frozen_at}; package={freeze_id}."
    write_csv(CONTRACT_ROOT / "result_contract.csv", result_fields, result_rows)

    artifact_fields, existing_rows = read_csv(CONTRACT_ROOT / "artifact_freeze_registry.csv")
    frozen_artifacts = [
        ("FRZ-MANIFEST", "frozen_manifest", FROZEN_ROOT / "frozen_manifest.json"),
        ("FRZ-CONFIRM", "freeze_confirmation", FROZEN_ROOT / "freeze_confirmation.md"),
        ("FRZ-METRICS", "metrics", FROZEN_ROOT / "metrics_summary.csv"),
        ("FRZ-Q1", "plan_detail", FROZEN_ROOT / "q1_results.csv"),
        ("FRZ-Q2", "plan_detail", FROZEN_ROOT / "q2_results.csv"),
        ("FRZ-Q3", "plan_detail", FROZEN_ROOT / "q3_results.csv"),
        ("FRZ-Q4", "plan_detail", FROZEN_ROOT / "q4_results.csv"),
        ("FRZ-Q5", "plan_detail", FROZEN_ROOT / "q5_results.csv"),
        ("FRZ-TEMPLATE-1", "official_template", FROZEN_ROOT / "result1.xlsx"),
        ("FRZ-TEMPLATE-2", "official_template", FROZEN_ROOT / "result2.xlsx"),
        ("FRZ-TEMPLATE-3", "official_template", FROZEN_ROOT / "result3.xlsx"),
    ]
    existing_rows.extend(
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": path.relative_to(ROOT).as_posix(),
            "hash_sha256": sha256(path),
            "producing_stage": "result_freeze",
            "freeze_reason": "Human result_freeze_gate confirmed by the controller.",
            "freeze_time": frozen_at,
            "protected_atoms": "plans;coordinates;durations;intervals;template cells;manifest",
            "allowed_changes": "Only an authorized result-revision workflow may supersede this artifact.",
            "owner": "Human gate confirmed; Codex recorded",
            "status": "frozen",
            "notes": f"freeze_id={freeze_id}; copied from the verified ready package.",
        }
        for artifact_id, artifact_type, path in frozen_artifacts
    )
    write_csv(CONTRACT_ROOT / "artifact_freeze_registry.csv", artifact_fields, existing_rows)

    for path in [FROZEN_ROOT / name for name in copied_csvs + copied_files] + [FROZEN_ROOT / "frozen_manifest.json"]:
        if not path.exists() or not sha256(path):
            raise RuntimeError(f"frozen artifact verification failed: {path}")
    return {"freeze_id": freeze_id, "frozen_at": frozen_at, "frozen_artifacts": len(frozen_artifacts)}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False))
