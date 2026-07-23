from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READY_ROOT = ROOT / "07_results" / "ready_for_freeze"
VALIDATION_ROOT = ROOT / "07_results" / "result_freeze_validation"
CONTRACT_ROOT = ROOT / "14_contracts"
REPORT_PATH = ROOT / "07_results" / "result_freeze_report.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def contract_assumptions(question_id: str) -> str:
    base = "A01;A02;A03;A04;A05;A06;A07;A08;A09"
    return base if question_id != "Q5" else base + ";A10;A11;A12;A13"


def build_report(manifest: dict[str, object], metrics: list[dict[str, str]], verification: dict[str, object]) -> None:
    metric_rows = "\n".join(
        f"| {row['question_id']} | {row['metric_name']} | {float(row['metric_value']):.9f} | s |"
        for row in metrics
    )
    REPORT_PATH.write_text(
        "\n".join(
            [
                "# 结果冻结核验报告",
                "",
                "## 状态",
                "",
                f"- 冻结包 ID：`{manifest['freeze_id']}`",
                "- 包状态：`ready`（待人工确认 `result_freeze_gate`）",
                "- 人工闸门尚未由任何 AI 确认；下列数值不得在闸门确认前表述为最终提交结论。",
                "- 来源：加密候选运行后，以 20×5×4 目标代表点、0.025 s 扫描和 1e-7 s 根定位容差独立复算。",
                "",
                "## 主口径待冻结数值",
                "",
                "| 问题 | 指标 | 数值 | 单位 |",
                "|---|---|---:|---|",
                metric_rows,
                "",
                "## 核验结论",
                "",
                "- 三个随机种子下每个输出的跨度为 0；加大搜索预算与加密采样仅产生数值积分层面的微小差异。",
                "- 全部计划通过速度、起爆高度、投放间隔、Q3/Q4 结构和 Q5 前缀弹位约束检查；Q5 三个主目标均为正时长。",
                f"- 三份官方模板的映射检查为 `{verification['status']}`，失败数为 `{verification['failure_count']}`；未使用弹位均为空。",
                "- Q3、Q4 的额外已用弹在当前候选中各自有效时长为 0，区间并集与 Q2 相同；该事实已保留在逐弹明细中，不宣称存在额外收益。",
                "",
                "## 基线与敏感性（仅对照，不改写主模型）",
                "",
                "- A03：取消投弹后水平速度继承时，当前计划的遮挡时长均为 0，说明结果对这一已人工确认的物理假设敏感。",
                "- A07：烟幕到地面后停留的替代口径未改变当前遮挡区间。",
                "- A08：中心点、80% 覆盖率与固定时间格点基线均已登记；主口径仍为全代表点遮挡和连续边界细化。",
                "- A11：公平优先对照会改选 Q5 分配，主口径仍严格遵从已冻结的“总时长优先、最短时长次之”目标；该取舍不可由实现阶段静默替换。",
                "- A12：取消“三目标均正时长”约束的对照没有改变总时长优先的分配。",
                "",
                "## 产物与可追溯性",
                "",
                "- 逐弹明细、指标表、模板映射和运行清单位于 `07_results/ready_for_freeze/`。",
                "- 收敛、稳定性、基线与敏感性证据位于 `07_results/result_freeze_validation/`。",
                "- 本报告、结果合同和产物登记均采用 `ready` 状态，等待人工闸门后才可视为正式冻结。",
                "",
            ]
        ),
        encoding="utf-8",
    )


def run() -> dict[str, object]:
    manifest_path = READY_ROOT / "ready_for_freeze_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    metrics = read_csv(READY_ROOT / "metrics_summary.csv")
    verification = json.loads((READY_ROOT / "template_mapping_check.json").read_text(encoding="utf-8"))
    if verification["status"] != "pass":
        raise RuntimeError("template mapping verification must pass before result-freeze registration")
    prepared_at = datetime.now(timezone.utc).isoformat()
    build_report(manifest, metrics, verification)

    result_fields = [
        "result_id",
        "question_id",
        "model_id",
        "metric_name",
        "metric_value",
        "unit",
        "source_file",
        "source_row_or_cell",
        "code_file",
        "run_id",
        "random_seed",
        "assumption_ids",
        "used_by_figure_ids",
        "used_by_claim_ids",
        "freeze_status",
        "freeze_time",
        "owner",
        "notes",
    ]
    result_rows = []
    for row_number, metric in enumerate(metrics, start=2):
        question_id = metric["question_id"]
        result_rows.append(
            {
                "result_id": f"RES-{question_id}-{metric['metric_name'].upper()}",
                "question_id": question_id,
                "model_id": "MDL-3D-ALLPOINT-UNION-V1",
                "metric_name": metric["metric_name"],
                "metric_value": metric["metric_value"],
                "unit": metric["unit"],
                "source_file": "07_results/ready_for_freeze/metrics_summary.csv",
                "source_row_or_cell": f"row={row_number};{metric['source_record']}",
                "code_file": "06_code/run_result_freeze_validation.py;06_code/prepare_result_freeze_package.py",
                "run_id": manifest["freeze_id"],
                "random_seed": "20250722;20250723;20250724",
                "assumption_ids": contract_assumptions(question_id),
                "used_by_figure_ids": "",
                "used_by_claim_ids": "",
                "freeze_status": "ready",
                "freeze_time": prepared_at,
                "owner": "Codex",
                "notes": "Strict recomputation passed; pending human result_freeze_gate.",
            }
        )
    write_csv(CONTRACT_ROOT / "result_contract.csv", result_rows, result_fields)

    manifest["contracts_registered"] = True
    manifest["template_mapping_status"] = verification["status"]
    manifest["prepared_at"] = prepared_at
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    artifact_paths = [
        ("RF-PACKAGE", "manifest", READY_ROOT / "ready_for_freeze_manifest.json"),
        ("RF-METRICS", "metrics", READY_ROOT / "metrics_summary.csv"),
        ("RF-Q1", "plan_detail", READY_ROOT / "q1_results.csv"),
        ("RF-Q2", "plan_detail", READY_ROOT / "q2_results.csv"),
        ("RF-Q3", "plan_detail", READY_ROOT / "q3_results.csv"),
        ("RF-Q4", "plan_detail", READY_ROOT / "q4_results.csv"),
        ("RF-Q5", "plan_detail", READY_ROOT / "q5_results.csv"),
        ("RF-TEMPLATE-1", "official_template", READY_ROOT / "result1.xlsx"),
        ("RF-TEMPLATE-2", "official_template", READY_ROOT / "result2.xlsx"),
        ("RF-TEMPLATE-3", "official_template", READY_ROOT / "result3.xlsx"),
        ("RF-VALIDATION", "validation_evidence", VALIDATION_ROOT / "validation_summary.json"),
        ("RF-REPORT", "result_freeze_report", REPORT_PATH),
    ]
    artifact_fields = [
        "artifact_id",
        "artifact_type",
        "path",
        "hash_sha256",
        "producing_stage",
        "freeze_reason",
        "freeze_time",
        "protected_atoms",
        "allowed_changes",
        "owner",
        "status",
        "notes",
    ]
    artifact_rows = [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": path.relative_to(ROOT).as_posix(),
            "hash_sha256": sha256(path),
            "producing_stage": "result_freeze",
            "freeze_reason": "Numerical evidence passed; package is ready for human gate review.",
            "freeze_time": prepared_at,
            "protected_atoms": "plans;coordinates;durations;intervals;template cells",
            "allowed_changes": "Only a new reproducible verification run with a new package ID.",
            "owner": "Codex",
            "status": "ready",
            "notes": "Human result_freeze_gate pending; not frozen by AI.",
        }
        for artifact_id, artifact_type, path in artifact_paths
    ]
    write_csv(CONTRACT_ROOT / "artifact_freeze_registry.csv", artifact_rows, artifact_fields)
    return {"freeze_id": manifest["freeze_id"], "result_contract_rows": len(result_rows), "artifact_rows": len(artifact_rows)}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False))
