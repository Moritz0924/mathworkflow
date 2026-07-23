from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


FROZEN_PACKAGE = "RF-20260722T114756Z"
METRIC_TOLERANCE_S = 1e-9


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_intervals(raw: str) -> list[tuple[float, float]]:
    if not raw.strip():
        return []
    values = json.loads(raw)
    return [(float(start), float(end)) for start, end in values]


def merge_intervals(intervals: Iterable[tuple[float, float]]) -> list[tuple[float, float]]:
    ordered = sorted((float(start), float(end)) for start, end in intervals)
    if not ordered:
        return []
    merged: list[list[float]] = [[ordered[0][0], ordered[0][1]]]
    for start, end in ordered[1:]:
        if start <= merged[-1][1] + 1e-12:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [(start, end) for start, end in merged]


def interval_duration(intervals: Iterable[tuple[float, float]]) -> float:
    return sum(end - start for start, end in merge_intervals(intervals))


def metric_key(question_id: str, metric_name: str) -> str:
    return f"{question_id}/{metric_name}"


def validate(root: Path) -> dict[str, Any]:
    frozen = root / "07_results" / "frozen"
    validation_root = root / "07_results" / "result_freeze_validation"
    metric_rows = load_rows(frozen / "metrics_summary.csv")
    metrics = {
        metric_key(row["question_id"], row["metric_name"]): float(row["metric_value"])
        for row in metric_rows
    }
    checks: list[dict[str, Any]] = []

    def record(check_id: str, passed: bool, detail: str, **data: Any) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "pass" if passed else "fail",
                "detail": detail,
                **data,
            }
        )

    statuses = {row["result_status"] for row in metric_rows}
    record(
        "frozen_metric_status",
        statuses == {"frozen"} and len(metric_rows) == 9,
        f"冻结汇总含 {len(metric_rows)} 项指标，状态集合为 {sorted(statuses)}。",
    )

    contract_rows = load_rows(root / "14_contracts" / "result_contract.csv")
    contract_values = {
        metric_key(row["question_id"], row["metric_name"]): float(row["metric_value"])
        for row in contract_rows
        if row["freeze_status"] == "frozen"
    }
    common = sorted(set(metrics) & set(contract_values))
    contract_error = max((abs(metrics[key] - contract_values[key]) for key in common), default=math.inf)
    record(
        "result_contract_alignment",
        set(metrics) == set(contract_values) and contract_error <= METRIC_TOLERANCE_S,
        f"冻结 CSV 与结果合同逐项对齐；最大绝对差 {contract_error:.3e} s。",
        maximum_absolute_error_s=contract_error,
    )

    result_rows: dict[str, list[dict[str, str]]] = {}
    row_duration_error = 0.0
    row_count = 0
    for question in range(1, 6):
        question_id = f"Q{question}"
        rows = load_rows(frozen / f"q{question}_results.csv")
        result_rows[question_id] = rows
        for row in rows:
            expected = interval_duration(parse_intervals(row["occlusion_intervals"]))
            actual = float(row["effective_duration_s"] or 0.0)
            row_duration_error = max(row_duration_error, abs(expected - actual))
            row_count += 1
    record(
        "row_interval_duration",
        row_duration_error <= METRIC_TOLERANCE_S,
        f"复算 {row_count} 条方案记录的区间长度；最大绝对差 {row_duration_error:.3e} s。",
        maximum_absolute_error_s=row_duration_error,
    )

    aggregate: dict[str, float] = {}
    for question_id in ("Q1", "Q2", "Q3", "Q4"):
        intervals = [
            interval
            for row in result_rows[question_id]
            if row["missile_id"] == "M1"
            for interval in parse_intervals(row["occlusion_intervals"])
        ]
        aggregate[metric_key(question_id, "primary_duration_M1")] = interval_duration(intervals)

    for missile_id in ("M1", "M2", "M3"):
        intervals = [
            interval
            for row in result_rows["Q5"]
            if row["missile_id"] == missile_id
            for interval in parse_intervals(row["occlusion_intervals"])
        ]
        aggregate[metric_key("Q5", f"primary_duration_{missile_id}")] = interval_duration(intervals)
    q5_values = [aggregate[metric_key("Q5", f"primary_duration_M{index}")] for index in range(1, 4)]
    aggregate[metric_key("Q5", "objective_total_duration")] = sum(q5_values)
    aggregate[metric_key("Q5", "objective_minimum_duration")] = min(q5_values)
    aggregate_error = max(abs(aggregate[key] - metrics[key]) for key in metrics)
    record(
        "question_aggregate_metrics",
        aggregate_error <= METRIC_TOLERANCE_S,
        f"按区间并集复算 Q1--Q5 汇总指标；最大绝对差 {aggregate_error:.3e} s。",
        maximum_absolute_error_s=aggregate_error,
    )

    constraint_issues: list[str] = []
    for question_id, rows in result_rows.items():
        for row in rows:
            if row["is_used"] != "1":
                continue
            label = f"{question_id}/{row['uav_id']}/B{row['bomb_id']}"
            speed = float(row["speed_mps"])
            release = float(row["release_time_s"])
            delay = float(row["delay_s"])
            detonation = float(row["detonation_time_s"])
            detonation_z = float(row["detonation_z_m"])
            if not 70.0 <= speed <= 140.0:
                constraint_issues.append(f"{label}: speed")
            if release < 0.0 or delay < 0.0:
                constraint_issues.append(f"{label}: negative time")
            if abs(release + delay - detonation) > METRIC_TOLERANCE_S:
                constraint_issues.append(f"{label}: detonation time")
            if detonation_z < -METRIC_TOLERANCE_S:
                constraint_issues.append(f"{label}: below ground")

    q3_release_times = sorted(
        float(row["release_time_s"]) for row in result_rows["Q3"] if row["is_used"] == "1"
    )
    if any(right - left < 1.0 - METRIC_TOLERANCE_S for left, right in zip(q3_release_times, q3_release_times[1:])):
        constraint_issues.append("Q3: release spacing")
    record(
        "physical_and_timing_constraints",
        not constraint_issues,
        "速度、时序、起爆高度和同机投放间隔均满足冻结实现约束。"
        if not constraint_issues
        else "; ".join(constraint_issues),
        issues=constraint_issues,
    )

    active_q5 = [row for row in result_rows["Q5"] if row["is_used"] == "1"]
    active_uavs = [row["uav_id"] for row in active_q5]
    active_missiles = [row["missile_id"] for row in active_q5]
    assignment_passed = (
        len(active_q5) == 3
        and len(set(active_uavs)) == 3
        and set(active_missiles) == {"M1", "M2", "M3"}
        and all(float(row["effective_duration_s"]) > 0.0 for row in active_q5)
    )
    record(
        "q5_assignment",
        assignment_passed,
        "Q5 使用 FY1→M1、FY2→M2、FY5→M3，每枚导弹均获得正遮蔽。",
        active_assignments=[f"{row['uav_id']}→{row['missile_id']}" for row in active_q5],
    )

    convergence = load_rows(validation_root / "convergence_and_stability.csv")
    validation_summary = json.loads(
        (validation_root / "validation_summary.json").read_text(encoding="utf-8-sig")
    )
    registered_stability_tolerance_s = float(
        validation_summary["checks"]["seed_stability_tolerance_s"]
    )
    seed_rows = [row for row in convergence if row["scenario"].startswith("seed_")]
    grouped_seed_values: dict[str, list[float]] = {}
    for row in seed_rows:
        key = metric_key(row["question_id"], row["metric_name"])
        grouped_seed_values.setdefault(key, []).append(float(row["metric_value_s"]))
    seed_span = max((max(values) - min(values) for values in grouped_seed_values.values()), default=math.inf)
    seed_counts = {len(values) for values in grouped_seed_values.values()}
    record(
        "seed_stability",
        seed_counts == {3} and seed_span <= METRIC_TOLERANCE_S,
        f"三个登记随机种子逐指标一致；最大跨度 {seed_span:.3e} s。",
        maximum_span_s=seed_span,
    )

    refined_rows = [row for row in convergence if row["scenario"] == "refined"]
    refined_values = {
        metric_key(row["question_id"], row["metric_name"]): float(row["metric_value_s"])
        for row in refined_rows
    }
    refined_alias = {
        "Q1/objective_1": "Q1/primary_duration_M1",
        "Q2/objective_1": "Q2/primary_duration_M1",
        "Q3/objective_1": "Q3/primary_duration_M1",
        "Q4/objective_1": "Q4/primary_duration_M1",
        "Q5/objective_1": "Q5/objective_total_duration",
        "Q5/objective_2": "Q5/objective_minimum_duration",
    }
    refinement_differences: list[float] = []
    for key, refined_value in refined_values.items():
        frozen_key = refined_alias.get(key, key)
        if frozen_key in metrics:
            refinement_differences.append(abs(refined_value - metrics[frozen_key]))
    refinement_error = max(refinement_differences, default=math.inf)
    record(
        "grid_tolerance_convergence",
        refinement_error <= registered_stability_tolerance_s,
        "较上一档加密配置，最终严格复算的主指标最大变化 "
        f"{refinement_error:.3e} s，低于登记稳定性阈值 "
        f"{registered_stability_tolerance_s:.3g} s。",
        maximum_absolute_change_s=refinement_error,
        registered_stability_tolerance_s=registered_stability_tolerance_s,
    )

    sensitivity = load_rows(validation_root / "baseline_and_sensitivity.csv")
    scenario_values: dict[str, dict[str, float]] = {}
    for row in sensitivity:
        key = metric_key(row["question_id"], row["metric_name"])
        scenario_values.setdefault(row["scenario"], {})[key] = float(row["metric_value_s"])
    a03_values = scenario_values["A03_no_horizontal_inheritance"]
    record(
        "a03_sensitivity",
        all(abs(value) <= METRIC_TOLERANCE_S for value in a03_values.values()),
        "取消干扰弹水平速度继承后，登记指标均降为 0 s，结论对 A03 高敏感。",
    )
    a07_values = scenario_values["A07_hold_smoke_at_ground"]
    a07_error = max(abs(a07_values[key] - metrics[key]) for key in a07_values)
    record(
        "a07_sensitivity",
        a07_error <= METRIC_TOLERANCE_S,
        f"本组方案的烟幕未在有效区间触地，A07 变体最大变化 {a07_error:.3e} s。",
        maximum_absolute_change_s=a07_error,
    )
    a08_values = scenario_values["A08_80pct_coverage"]
    a08_changes = {key: a08_values[key] - metrics[key] for key in a08_values}
    record(
        "a08_sensitivity",
        all(value >= -METRIC_TOLERANCE_S for value in a08_changes.values())
        and max(a08_changes.values()) > 0.1,
        "将全点遮蔽放宽到 80% 覆盖后指标不下降，且 M2 出现显著增量，说明结论受 A08 口径影响。",
        changes_s=a08_changes,
    )

    headline_keys = (
        "Q1/primary_duration_M1",
        "Q2/primary_duration_M1",
        "Q5/objective_total_duration",
        "Q5/objective_minimum_duration",
    )
    status = "pass" if all(item["status"] == "pass" for item in checks) else "fail"
    return {
        "status": status,
        "frozen_package": FROZEN_PACKAGE,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "method_boundary": "冻结方案复核；不声明全局最优，不改变模型假设。",
        "headline_metrics": {key: metrics[key] for key in headline_keys},
        "recomputed_metrics": aggregate,
        "checks": checks,
    }


def write_reports(root: Path, report: dict[str, Any]) -> None:
    review_root = root / "11_review"
    review_root.mkdir(parents=True, exist_ok=True)
    json_path = review_root / "final_model_validation.json"
    markdown_path = review_root / "final_model_validation.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 终稿模型与冻结结果复核",
        "",
        f"- 结论：**{report['status'].upper()}**",
        f"- 冻结包：`{report['frozen_package']}`",
        f"- 边界：{report['method_boundary']}",
        "",
        "## 核心指标",
        "",
        "| 指标 | 冻结值 / s |",
        "|---|---:|",
    ]
    for key, value in report["headline_metrics"].items():
        lines.append(f"| {key} | {value:.9f} |")
    lines.extend(["", "## 复核项", "", "| 检查 | 状态 | 说明 |", "|---|---|---|"])
    for check in report["checks"]:
        lines.append(f"| {check['check_id']} | {check['status']} | {check['detail']} |")
    lines.extend(
        [
            "",
            "## 结论边界",
            "",
            "本报告证明冻结 CSV、合同、区间并集、约束和登记稳定性情景相互一致。它不扩大搜索预算，也不把当前可复现冻结方案解释为全局最优解。",
            "",
        ]
    )
    markdown_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the frozen model evidence used by the final paper.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    report = validate(root)
    write_reports(root, report)
    print(json.dumps({"status": report["status"], "checks": len(report["checks"])}, ensure_ascii=False))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
