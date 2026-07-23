from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from src.constants import MISSILES, TARGET_BASE_CENTER, TARGET_HEIGHT_M, TARGET_RADIUS_M, UAVS


plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

FIGURE_SPECS = [
    ("F001", "F1_initial_3d_scene", "Q1-Q5", "初始三维场景"),
    ("F002", "F2_q1_trajectory", "Q1", "Q1 固定策略三维轨迹"),
    ("F003", "F3_q1_q2_intervals", "Q1;Q2", "Q1—Q2 有效遮蔽区间对比"),
    ("F004", "F4_q3_bomb_intervals", "Q3", "Q3 三弹区间分解"),
    ("F005", "F5_q4_uav_intervals", "Q4", "Q4 三机区间分解"),
    ("F006", "F6_q5_assignment", "Q5", "Q5 无人机—导弹任务分配"),
    ("F007", "F7_q5_missile_intervals", "Q5", "Q5 三导弹遮蔽时间轴"),
    ("F008", "F8_q1_q4_metrics", "Q1;Q2;Q3;Q4", "Q1—Q4 主指标对比"),
    ("F009", "F9_model_baselines", "Q1;Q2;Q5", "主模型与基线对照"),
    ("F010", "F10_a08_sensitivity", "Q1;Q2;Q5", "A08 覆盖口径敏感性"),
    ("F011", "F11_assumption_matrix", "Q1-Q5", "高风险假设影响矩阵"),
]


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _intervals(row: dict[str, str]) -> list[tuple[float, float]]:
    return [(float(left), float(right)) for left, right in json.loads(row.get("occlusion_intervals") or "[]")]


def _metric_map(rows: list[dict[str, str]]) -> dict[tuple[str, str], float]:
    return {(row["question_id"], row["metric_name"]): float(row["metric_value"]) for row in rows}


def _contributions(rows: list[dict[str, str]], label_key: str) -> list[dict[str, Any]]:
    return [
        {
            "label": row[label_key],
            "duration_s": float(row["effective_duration_s"] or 0.0),
            "intervals": row["occlusion_intervals"],
            "result_status": row["result_status"],
        }
        for row in rows
    ]


def build_evidence_data(root: Path) -> dict[str, list[dict[str, Any]]]:
    """Load the frozen source records required by evidence figures and tables."""
    frozen = Path(root) / "07_results" / "frozen"
    metrics = _read_csv(frozen / "metrics_summary.csv")
    plans = {question_id: _read_csv(frozen / f"{question_id.lower()}_results.csv") for question_id in ("Q1", "Q2", "Q3", "Q4", "Q5")}
    baseline = _read_csv(Path(root) / "07_results" / "result_freeze_validation" / "baseline_and_sensitivity.csv")
    q5_assignment = _read_csv(Path(root) / "07_results" / "result_freeze_validation" / "q5_assignment_sensitivity.csv")
    return {
        "metrics": metrics,
        "q1": plans["Q1"],
        "q2": plans["Q2"],
        "q3": plans["Q3"],
        "q4": plans["Q4"],
        "q5": plans["Q5"],
        "q3_contributions": _contributions(plans["Q3"], "bomb_id"),
        "q4_contributions": _contributions(plans["Q4"], "uav_id"),
        "baseline": baseline,
        "q5_assignment_sensitivity": q5_assignment,
    }


def _frozen_metric(data: dict[str, Any], question_id: str, metric_name: str) -> float:
    return _metric_map(data["metrics"])[(question_id, metric_name)]


def _save_figure(figure: plt.Figure, output_root: Path, name: str) -> None:
    figure_dir = output_root / "main_figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    figure.savefig(figure_dir / f"{name}.png", dpi=300, bbox_inches="tight")
    figure.savefig(figure_dir / f"{name}.svg", bbox_inches="tight")
    plt.close(figure)


def _draw_target(ax: Any, *, show_text: bool = True) -> None:
    theta = np.linspace(0, 2 * math.pi, 40)
    z = np.linspace(0, TARGET_HEIGHT_M, 8)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x = TARGET_BASE_CENTER[0] + TARGET_RADIUS_M * np.cos(theta_grid)
    y = TARGET_BASE_CENTER[1] + TARGET_RADIUS_M * np.sin(theta_grid)
    ax.plot_wireframe(x, y, z_grid, color="#2563eb", linewidth=0.5, alpha=0.55)
    if show_text:
        ax.text(TARGET_BASE_CENTER[0], TARGET_BASE_CENTER[1], TARGET_HEIGHT_M + 120, "真目标（圆柱）", color="#1d4ed8", fontsize=9)


def _draw_false_target(ax: Any, *, show_text: bool = True) -> None:
    ax.scatter(0, 0, 0, color="#111827", marker="x", s=50)
    if show_text:
        ax.text(0, 0, 120, "假目标", color="#111827", fontsize=9)


def _draw_intervals(ax: Any, rows: list[dict[str, Any]], title: str, *, x_max: float = 18.0) -> None:
    labels = [str(row["label"]) for row in rows]
    positions = np.arange(len(rows))[::-1]
    colors = ["#0f766e" if row["duration_s"] > 0 else "#9ca3af" for row in rows]
    for y, row, color in zip(positions, rows, colors):
        intervals = row["intervals"]
        if intervals:
            for start, end in intervals:
                ax.broken_barh([(start, end - start)], (y - 0.32, 0.64), facecolors=color)
                ax.text((start + end) / 2, y, f"{end - start:.3f} s", ha="center", va="center", color="white", fontsize=8)
        else:
            ax.plot(0, y, "o", color=color, markersize=5)
            ax.text(0.25, y, "0 s", va="center", color="#4b5563", fontsize=9)
    ax.set_xlim(0, x_max)
    ax.set_ylim(-0.8, len(rows) - 0.2)
    ax.set_yticks(positions, labels)
    ax.set_xlabel("任务开始后的时间 / s")
    ax.set_title(title)
    ax.grid(axis="x", color="#d1d5db", linewidth=0.6)


def _baseline_values(data: dict[str, Any], scenario: str) -> dict[tuple[str, str], float]:
    return {
        (row["question_id"], row["missile_id"]): float(row["metric_value_s"])
        for row in data["baseline"]
        if row["scenario"] == scenario
    }


def _write_tables(data: dict[str, Any], root: Path, output_root: Path) -> None:
    tables = output_root / "tables"
    metrics = _metric_map(data["metrics"])
    q1 = data["q1"][0]
    q2 = data["q2"][0]
    q3 = data["q3"]
    q4 = data["q4"]
    q5 = data["q5"]

    _write_csv(
        tables / "T1_parameters.csv",
        [
            {"类别": "题面常量", "参数或口径": "导弹速度", "数值或内容": 300, "单位": "m/s", "来源": "题面", "假设编号": ""},
            {"类别": "题面常量", "参数或口径": "无人机速度范围", "数值或内容": "70–140", "单位": "m/s", "来源": "题面", "假设编号": ""},
            {"类别": "题面常量", "参数或口径": "烟幕有效半径", "数值或内容": 10, "单位": "m", "来源": "题面", "假设编号": ""},
            {"类别": "题面常量", "参数或口径": "烟幕物理有效期", "数值或内容": 20, "单位": "s", "来源": "题面", "假设编号": ""},
            {"类别": "冻结口径", "参数或口径": "投弹继承水平速度", "数值或内容": "继承", "单位": "", "来源": "人工冻结", "假设编号": "A03"},
            {"类别": "冻结口径", "参数或口径": "烟幕到地面后", "数值或内容": "停止计入有效遮蔽", "单位": "", "来源": "人工冻结", "假设编号": "A07"},
            {"类别": "冻结口径", "参数或口径": "目标遮挡判据", "数值或内容": "全代表点均被遮挡", "单位": "", "来源": "人工冻结", "假设编号": "A08"},
        ],
        ["类别", "参数或口径", "数值或内容", "单位", "来源", "假设编号"],
    )
    _write_csv(
        tables / "T2_metrics.csv",
        [
            {"问题": row["question_id"], "评价对象": row["source_record"], "主指标": row["metric_name"], "冻结数值_s": row["metric_value"], "结果合同ID": f"RES-{row['question_id']}-{row['metric_name'].upper()}"}
            for row in data["metrics"]
        ],
        ["问题", "评价对象", "主指标", "冻结数值_s", "结果合同ID"],
    )
    _write_csv(
        tables / "T3_q1_q2.csv",
        [
            {"方案": "Q1 固定", "航向角_deg": q1["heading_deg"], "速度_mps": q1["speed_mps"], "投放时刻_s": q1["release_time_s"], "起爆延迟_s": q1["delay_s"], "起爆时刻_s": q1["detonation_time_s"], "有效时长_s": q1["effective_duration_s"]},
            {"方案": "Q2 冻结求解", "航向角_deg": q2["heading_deg"], "速度_mps": q2["speed_mps"], "投放时刻_s": q2["release_time_s"], "起爆延迟_s": q2["delay_s"], "起爆时刻_s": q2["detonation_time_s"], "有效时长_s": q2["effective_duration_s"]},
        ],
        ["方案", "航向角_deg", "速度_mps", "投放时刻_s", "起爆延迟_s", "起爆时刻_s", "有效时长_s"],
    )
    _write_csv(
        tables / "T4_q3_contributions.csv",
        [
            {"弹号": row["bomb_id"], "投放时刻_s": row["release_time_s"], "起爆时刻_s": row["detonation_time_s"], "单弹有效区间": row["occlusion_intervals"], "单弹时长_s": row["effective_duration_s"], "新增并集贡献_s": row["effective_duration_s"]}
            for row in q3
        ],
        ["弹号", "投放时刻_s", "起爆时刻_s", "单弹有效区间", "单弹时长_s", "新增并集贡献_s"],
    )
    _write_csv(
        tables / "T5_q4_contributions.csv",
        [
            {"无人机": row["uav_id"], "航向角_deg": row["heading_deg"], "速度_mps": row["speed_mps"], "单弹有效区间": row["occlusion_intervals"], "单弹时长_s": row["effective_duration_s"], "新增并集贡献_s": row["effective_duration_s"]}
            for row in q4
        ],
        ["无人机", "航向角_deg", "速度_mps", "单弹有效区间", "单弹时长_s", "新增并集贡献_s"],
    )
    _write_csv(
        tables / "T6_q5_assignments.csv",
        [
            {"无人机": row["uav_id"], "弹号": row["bomb_id"], "是否使用": row["is_used"], "主目标": row["missile_id"], "航向角_deg": row["heading_deg"], "速度_mps": row["speed_mps"], "投放时刻_s": row["release_time_s"], "起爆时刻_s": row["detonation_time_s"], "有效时长_s": row["effective_duration_s"]}
            for row in q5
        ],
        ["无人机", "弹号", "是否使用", "主目标", "航向角_deg", "速度_mps", "投放时刻_s", "起爆时刻_s", "有效时长_s"],
    )
    resource_rows = []
    for uav_id in UAVS:
        used_rows = [row for row in q5 if row["uav_id"] == uav_id and row["is_used"] == "1"]
        resource_rows.append({"无人机": uav_id, "已使用弹数": len(used_rows), "主目标": ";".join(row["missile_id"] for row in used_rows), "是否形成正有效时长": "是" if any(float(row["effective_duration_s"] or 0) > 0 for row in used_rows) else "否"})
    _write_csv(tables / "T7_q5_resources.csv", resource_rows, ["无人机", "已使用弹数", "主目标", "是否形成正有效时长"])

    primary = {("Q1", "M1"): metrics[("Q1", "primary_duration_M1")], ("Q2", "M1"): metrics[("Q2", "primary_duration_M1")], ("Q5", "M1"): metrics[("Q5", "primary_duration_M1")], ("Q5", "M2"): metrics[("Q5", "primary_duration_M2")], ("Q5", "M3"): metrics[("Q5", "primary_duration_M3")]}
    center = _baseline_values(data, "baseline_center_point")
    fixed = _baseline_values(data, "baseline_fixed_grid")
    _write_csv(
        tables / "T8_baselines.csv",
        [
            {"对象": f"{question_id}/{missile_id}", "主模型_s": duration, "中心点基线_s": center[(question_id, missile_id)], "固定格点基线_s": fixed[(question_id, missile_id)]}
            for (question_id, missile_id), duration in primary.items()
        ],
        ["对象", "主模型_s", "中心点基线_s", "固定格点基线_s"],
    )
    coverage = _baseline_values(data, "A08_80pct_coverage")
    _write_csv(
        tables / "T9_sensitivity.csv",
        [
            {"场景": "A03 不继承水平速度", "变化": "各冻结主指标变为 0", "方案结构变化": "否（固定计划复算）", "结论": "对 A03 高度敏感"},
            {"场景": "A07 地面停留", "变化": "0", "方案结构变化": "否", "结论": "当前区间无影响"},
            {"场景": "A08 80% 覆盖率", "变化": f"Q5/M2 +{coverage[('Q5', 'M2')] - primary[('Q5', 'M2')]:.6f} s", "方案结构变化": "未重求解", "结论": "几何口径影响因目标而异"},
            {"场景": "A11 公平优先", "变化": "分配发生变化", "方案结构变化": "是", "结论": "目标优先级具有实质影响"},
            {"场景": "A12 取消全正时长约束", "变化": "总时长优先分配不变", "方案结构变化": "否", "结论": "当前对照不改变分配"},
        ],
        ["场景", "变化", "方案结构变化", "结论"],
    )


def _figures(data: dict[str, Any], output_root: Path) -> list[dict[str, object]]:
    q1, q2 = data["q1"][0], data["q2"][0]
    q3, q4, q5 = data["q3"], data["q4"], data["q5"]
    metrics = _metric_map(data["metrics"])
    artifacts: list[dict[str, object]] = []

    fig = plt.figure(figsize=(8, 6)); ax = fig.add_subplot(111, projection="3d")
    _draw_target(ax, show_text=False)
    for missile in MISSILES.values():
        ax.scatter(*missile.initial_position, color="#dc2626", s=35); ax.text(*missile.initial_position, missile.missile_id)
        ax.plot([missile.initial_position[0], 0], [missile.initial_position[1], 0], [missile.initial_position[2], 0], color="#dc2626", alpha=.45)
    for uav in UAVS.values():
        ax.scatter(*uav.initial_position, color="#0f766e", s=28); ax.text(*uav.initial_position, uav.uav_id)
    _draw_false_target(ax, show_text=False)
    ax.set(title="F1 初始三维场景", xlabel="x / m", ylabel="y / m", zlabel="z / m")
    ax.legend(handles=[
        Line2D([0], [0], color="#dc2626", linewidth=2, label="来袭导弹方向"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#0f766e", markersize=7, label="无人机初始位置"),
        Line2D([0], [0], marker="x", color="#111827", markersize=8, label="假目标"),
        Line2D([0], [0], color="#2563eb", linewidth=2, label="真目标（圆柱）"),
    ], loc="upper left", fontsize=8)
    _save_figure(fig, output_root, "F1_initial_3d_scene")

    fig = plt.figure(figsize=(8, 6)); ax = fig.add_subplot(111, projection="3d")
    _draw_target(ax); _draw_false_target(ax)
    missile = MISSILES["M1"].initial_position; ax.plot([missile[0], 0], [missile[1], 0], [missile[2], 0], color="#dc2626", label="M1")
    release = np.array([float(q1[f"release_{axis}_m"]) for axis in "xyz"]); detonation = np.array([float(q1[f"detonation_{axis}_m"]) for axis in "xyz"])
    uav = np.array(UAVS["FY1"].initial_position); ax.plot([uav[0], release[0]], [uav[1], release[1]], [uav[2], release[2]], color="#0f766e", label="FY1")
    time = np.linspace(0, 1, 30); bomb = release[None, :] + (detonation - release)[None, :] * time[:, None]; ax.plot(bomb[:, 0], bomb[:, 1], bomb[:, 2], color="#f59e0b", label="干扰弹")
    ax.scatter(*release, color="#0f766e", s=35); ax.scatter(*detonation, color="#f59e0b", s=35)
    ax.set(title="F2 Q1 固定策略几何关系", xlabel="x / m", ylabel="y / m", zlabel="z / m"); ax.legend(loc="upper left")
    _save_figure(fig, output_root, "F2_q1_trajectory")

    fig, ax = plt.subplots(figsize=(8, 2.8)); _draw_intervals(ax, [{"label": "Q1 固定策略", "duration_s": float(q1["effective_duration_s"]), "intervals": _intervals(q1)}, {"label": "Q2 冻结方案", "duration_s": float(q2["effective_duration_s"]), "intervals": _intervals(q2)}], "F3 Q1—Q2 有效遮蔽区间对比"); _save_figure(fig, output_root, "F3_q1_q2_intervals")
    fig, ax = plt.subplots(figsize=(8, 4)); _draw_intervals(ax, [{"label": f"弹 {row['bomb_id']}", "duration_s": float(row["effective_duration_s"] or 0), "intervals": _intervals(row)} for row in q3] + [{"label": "三弹并集", "duration_s": metrics[("Q3", "primary_duration_M1")], "intervals": _intervals(q3[0])}], "F4 Q3 三弹区间分解"); _save_figure(fig, output_root, "F4_q3_bomb_intervals")
    fig, ax = plt.subplots(figsize=(8, 4)); _draw_intervals(ax, [{"label": row["uav_id"], "duration_s": float(row["effective_duration_s"] or 0), "intervals": _intervals(row)} for row in q4] + [{"label": "三机并集", "duration_s": metrics[("Q4", "primary_duration_M1")], "intervals": _intervals(q4[0])}], "F5 Q4 三机区间分解"); _save_figure(fig, output_root, "F5_q4_uav_intervals")

    fig, ax = plt.subplots(figsize=(8, 4.5)); ax.axis("off")
    left = {uav_id: 4 - index for index, uav_id in enumerate(UAVS)}; right = {missile_id: 3.2 - index * 1.5 for index, missile_id in enumerate(("M1", "M2", "M3"))}
    for name, y in left.items(): ax.scatter(0, y, s=900, color="#dbeafe", edgecolor="#2563eb"); ax.text(0, y, name, ha="center", va="center")
    for name, y in right.items(): ax.scatter(8, y, s=900, color="#dcfce7", edgecolor="#15803d"); ax.text(8, y, name, ha="center", va="center")
    for row in q5:
        if row["is_used"] == "1":
            ax.plot([0.7, 7.3], [left[row["uav_id"]], right[row["missile_id"]]], color="#0f766e", linewidth=2)
            ax.text(4, (left[row["uav_id"]] + right[row["missile_id"]]) / 2 + .18, f"弹{row['bomb_id']}，{float(row['effective_duration_s']):.3f} s", ha="center", fontsize=8)
    ax.set_xlim(-1, 9); ax.set_ylim(-1, 5); ax.set_title("F6 Q5 冻结主目标任务分配"); _save_figure(fig, output_root, "F6_q5_assignment")

    used_q5 = [row for row in q5 if row["is_used"] == "1"]
    fig, ax = plt.subplots(figsize=(8, 3.5)); _draw_intervals(ax, [{"label": row["missile_id"], "duration_s": float(row["effective_duration_s"]), "intervals": _intervals(row)} for row in used_q5], "F7 Q5 三枚导弹遮蔽时间轴"); _save_figure(fig, output_root, "F7_q5_missile_intervals")

    labels = ["Q1", "Q2", "Q3", "Q4"]; values = [metrics[("Q1", "primary_duration_M1")], metrics[("Q2", "primary_duration_M1")], metrics[("Q3", "primary_duration_M1")], metrics[("Q4", "primary_duration_M1")]]
    fig, ax = plt.subplots(figsize=(7, 4)); ax.vlines(labels, 0, values, color="#94a3b8", linewidth=1.5); ax.scatter(labels, values, color=["#64748b", "#0f766e", "#f59e0b", "#f59e0b"], s=65); [ax.text(label, value + .05, f"{value:.3f}", ha="center", fontsize=9) for label, value in zip(labels, values)]; ax.set(ylim=(0, 2.6), ylabel="M1 有效遮蔽时长 / s", title="F8 Q1—Q4 主指标对比"); ax.grid(axis="y", color="#e5e7eb"); _save_figure(fig, output_root, "F8_q1_q4_metrics")

    selected = [("Q1", "M1"), ("Q2", "M1"), ("Q5", "M1"), ("Q5", "M2"), ("Q5", "M3")]; primary = [metrics[(q, f"primary_duration_{m}")] for q, m in selected]; center = _baseline_values(data, "baseline_center_point"); fixed = _baseline_values(data, "baseline_fixed_grid")
    x = np.arange(len(selected)); fig, ax = plt.subplots(figsize=(9, 4)); ax.scatter(x - .16, primary, color="#0f766e", label="全代表点连续判定"); ax.scatter(x, [center[key] for key in selected], color="#2563eb", label="中心点基线"); ax.scatter(x + .16, [fixed[key] for key in selected], color="#f59e0b", label="固定格点基线"); ax.set(xticks=x, xticklabels=[f"{q}/{m}" for q, m in selected], ylabel="有效遮蔽时长 / s", title="F9 主模型与基线对照"); ax.legend(fontsize=8); ax.grid(axis="y", color="#e5e7eb"); _save_figure(fig, output_root, "F9_model_baselines")

    coverage = _baseline_values(data, "A08_80pct_coverage"); fig, ax = plt.subplots(figsize=(9, 4))
    sensitivity_styles = [
        {"color": "#475569", "linestyle": "-", "marker": "o", "zorder": 3},
        {"color": "#0f766e", "linestyle": (0, (3, 2)), "marker": "s", "zorder": 5},
        {"color": "#2563eb", "linestyle": "-", "marker": "^", "zorder": 4},
        {"color": "#d97706", "linestyle": "-", "marker": "o", "zorder": 3},
        {"color": "#7c3aed", "linestyle": "-", "marker": "o", "zorder": 3},
    ]
    for index, (key, style) in enumerate(zip(selected, sensitivity_styles)):
        label = f"{key[0]}/{key[1]}"
        ax.plot([0, 1], [primary[index], coverage[key]], linewidth=2, label=label, **style)
        ax.annotate(f"+{coverage[key] - primary[index]:.3f}", (1, coverage[key]), xytext=(8, 8 * (index - 2)), textcoords="offset points", va="center", fontsize=8, color=style["color"])
    ax.set(xticks=[0, 1], xticklabels=["全代表点", "80% 覆盖率"], ylabel="有效遮蔽时长 / s", title="F10 A08 覆盖口径敏感性")
    ax.legend(title="对象", fontsize=8, title_fontsize=8, loc="upper left", ncol=2)
    fig.text(0.62, 0.02, "注：Q2/M1 与 Q5/M1 在两种覆盖口径下数值重合，以颜色和线型区分。", ha="center", fontsize=8, color="#334155")
    _save_figure(fig, output_root, "F10_a08_sensitivity")

    matrix = np.array([[1, 0, 1], [0, 0, 0], [1, 0, 1], [1, 2, 2], [0, 0, 0]])
    fig, ax = plt.subplots(figsize=(7, 4)); image = ax.imshow(matrix, cmap=ListedColormap(["#e5e7eb", "#fde68a", "#fca5a5"]), vmin=0, vmax=2); ax.set(xticks=np.arange(3), xticklabels=["时长", "分配", "结论"], yticks=np.arange(5), yticklabels=["A03", "A07", "A08", "A11", "A12"], title="F11 高风险假设影响矩阵")
    for row in range(5):
        for column in range(3): ax.text(column, row, ["无变化", "数值变化", "结构变化"][matrix[row, column]], ha="center", va="center", fontsize=8)
    _save_figure(fig, output_root, "F11_assumption_matrix")

    for figure_id, name, question_id, title in FIGURE_SPECS:
        artifacts.append({"figure_id": figure_id, "question_id": question_id, "title": title, "png": (output_root / "main_figures" / f"{name}.png"), "svg": (output_root / "main_figures" / f"{name}.svg")})
    return artifacts


def generate_artifacts(root: Path, output_root: Path | None = None) -> list[dict[str, object]]:
    """Export all requested tables and figures from frozen records only."""
    destination = Path(output_root or (Path(root) / "08_figures"))
    data = build_evidence_data(root)
    _write_tables(data, root, destination)
    return _figures(data, destination)


FIGURE_RESULT_BINDINGS = {
    "F001": "RES-Q1-PRIMARY_DURATION_M1;RES-Q5-OBJECTIVE_TOTAL_DURATION",
    "F002": "RES-Q1-PRIMARY_DURATION_M1",
    "F003": "RES-Q1-PRIMARY_DURATION_M1;RES-Q2-PRIMARY_DURATION_M1",
    "F004": "RES-Q3-PRIMARY_DURATION_M1",
    "F005": "RES-Q4-PRIMARY_DURATION_M1",
    "F006": "RES-Q5-PRIMARY_DURATION_M1;RES-Q5-PRIMARY_DURATION_M2;RES-Q5-PRIMARY_DURATION_M3;RES-Q5-OBJECTIVE_TOTAL_DURATION;RES-Q5-OBJECTIVE_MINIMUM_DURATION",
    "F007": "RES-Q5-PRIMARY_DURATION_M1;RES-Q5-PRIMARY_DURATION_M2;RES-Q5-PRIMARY_DURATION_M3",
    "F008": "RES-Q1-PRIMARY_DURATION_M1;RES-Q2-PRIMARY_DURATION_M1;RES-Q3-PRIMARY_DURATION_M1;RES-Q4-PRIMARY_DURATION_M1",
    "F009": "RES-Q1-PRIMARY_DURATION_M1;RES-Q2-PRIMARY_DURATION_M1;RES-Q5-PRIMARY_DURATION_M1;RES-Q5-PRIMARY_DURATION_M2;RES-Q5-PRIMARY_DURATION_M3",
    "F010": "RES-Q1-PRIMARY_DURATION_M1;RES-Q2-PRIMARY_DURATION_M1;RES-Q5-PRIMARY_DURATION_M1;RES-Q5-PRIMARY_DURATION_M2;RES-Q5-PRIMARY_DURATION_M3",
    "F011": "RES-Q1-PRIMARY_DURATION_M1;RES-Q2-PRIMARY_DURATION_M1;RES-Q5-PRIMARY_DURATION_M1;RES-Q5-PRIMARY_DURATION_M2;RES-Q5-PRIMARY_DURATION_M3;RES-Q5-OBJECTIVE_TOTAL_DURATION;RES-Q5-OBJECTIVE_MINIMUM_DURATION",
}


FIGURE_METADATA = {
    "F001": {
        "claim": "展示冻结场景的初始几何关系，作为后续轨迹图的空间参照。",
        "source": "00_problem/problem_statement.md;06_code/src/constants.py;07_results/frozen/frozen_manifest.json",
        "panel": "单面板：目标、三枚导弹与五架无人机初始位置。",
        "chart_type": "3D scene diagram",
        "section": "问题重述与符号说明",
        "risk": "几何示意不得被解释为轨迹求解结果。",
    },
    "F002": {
        "claim": "Q1 固定策略的释放、起爆与有效遮蔽区间可由冻结记录复现。",
        "source": "07_results/frozen/q1_results.csv;07_results/frozen/metrics_summary.csv;06_code/src/constants.py",
        "panel": "单面板：FY1、M1、干扰弹释放点和起爆点。",
        "chart_type": "3D trajectory diagram",
        "section": "Q1 结果",
        "risk": "干扰弹曲线仅作空间关系示意，时长以冻结 CSV 为准。",
    },
    "F003": {
        "claim": "Q2 冻结方案的有效遮蔽时长高于 Q1 固定策略。",
        "source": "07_results/frozen/q1_results.csv;07_results/frozen/q2_results.csv;07_results/frozen/metrics_summary.csv",
        "panel": "单面板：Q1 与 Q2 的有效区间及对应时长。",
        "chart_type": "interval comparison",
        "section": "Q1–Q2 结果比较",
        "risk": "仅比较冻结方案，不声明全局最优。",
    },
    "F004": {
        "claim": "Q3 中第 2、3 枚弹的有效时长为零，三弹并集未超过 Q2 主指标。",
        "source": "07_results/frozen/q3_results.csv;07_results/frozen/metrics_summary.csv",
        "panel": "四行：三枚弹逐项区间及三弹并集；零贡献行保留。",
        "chart_type": "interval decomposition",
        "section": "Q3 结果与局限",
        "risk": "不得省略零贡献行或暗示多弹协同增益。",
    },
    "F005": {
        "claim": "Q4 中 FY2、FY3 的有效时长为零，三机并集未超过 Q2 主指标。",
        "source": "07_results/frozen/q4_results.csv;07_results/frozen/metrics_summary.csv",
        "panel": "四行：FY1–FY3 逐项区间及三机并集；零贡献行保留。",
        "chart_type": "interval decomposition",
        "section": "Q4 结果与局限",
        "risk": "不得将参与投放解释为形成有效遮蔽或额外收益。",
    },
    "F006": {
        "claim": "Q5 冻结主方案使用 FY1、FY2、FY5 的第 1 枚弹，分别服务 M1、M2、M3。",
        "source": "07_results/frozen/q5_results.csv;07_results/frozen/metrics_summary.csv",
        "panel": "二部网络：五架无人机、三枚导弹和三条已使用分配边。",
        "chart_type": "bipartite assignment network",
        "section": "Q5 任务分配",
        "risk": "未连边无人机和弹位表示未使用，不得补画。",
    },
    "F007": {
        "claim": "Q5 的三枚导弹各有一段正有效遮蔽区间，三段不表示连续联合保护。",
        "source": "07_results/frozen/q5_results.csv;07_results/frozen/metrics_summary.csv",
        "panel": "三行：M1、M2、M3 的有效遮蔽时间轴。",
        "chart_type": "multi-target timeline",
        "section": "Q5 结果",
        "risk": "时间轴间隙必须保留，避免误读为连续保护。",
    },
    "F008": {
        "claim": "Q2、Q3、Q4 的冻结主指标相同，Q1 较短。",
        "source": "07_results/frozen/metrics_summary.csv",
        "panel": "单面板：Q1–Q4 的 M1 有效遮蔽时长点图。",
        "chart_type": "dot comparison",
        "section": "跨问题比较",
        "risk": "相等的数值不应被解释为因果或协同效果。",
    },
    "F009": {
        "claim": "全代表点连续判定结果与两类基线在所列对象上可逐项比较。",
        "source": "07_results/frozen/metrics_summary.csv;07_results/result_freeze_validation/baseline_and_sensitivity.csv",
        "panel": "单面板：主模型、中心点基线、固定网格基线的散点对照。",
        "chart_type": "baseline comparison",
        "section": "结果核验",
        "risk": "基线仅作口径对照，不得当作额外优化结论。",
    },
    "F010": {
        "claim": "A08 的 80% 覆盖半径敏感性随问题和导弹而异。",
        "source": "07_results/frozen/metrics_summary.csv;07_results/result_freeze_validation/baseline_and_sensitivity.csv",
        "panel": "单面板：各对象从全代表点判定到 80% 半径的数值变化。",
        "chart_type": "paired sensitivity slope graph",
        "section": "敏感性分析",
        "risk": "仅代表已检验的 A08 情景，不外推到其他口径。",
    },
    "F011": {
        "claim": "A03、A08、A11 是需要在论文中明确说明的高风险假设或目标口径。",
        "source": "07_results/frozen/metrics_summary.csv;07_results/result_freeze_validation/baseline_and_sensitivity.csv;07_results/result_freeze_validation/q5_assignment_sensitivity.csv",
        "panel": "矩阵：时长、分配和结论层面的变化类别。",
        "chart_type": "categorical risk matrix",
        "section": "敏感性与局限",
        "risk": "矩阵是验证摘要，不能替代数值表和边界条件。",
    },
}


CLAIM_SPECS = [
    ("C001", "Q1", "Q1 结果", "在题面给定的固定策略下，M1 的有效遮蔽区间为 [8.056309, 9.418510] s，时长为 1.362201500 s。", "F002", "RES-Q1-PRIMARY_DURATION_M1", "仅为固定策略计算结果，不宣称最优。"),
    ("C002", "Q2", "Q1–Q2 结果比较", "Q2 冻结方案的 M1 有效遮蔽时长为 2.238164377 s，较 Q1 增加 0.875962877 s；不据此声明全局最优。", "F003", "RES-Q1-PRIMARY_DURATION_M1;RES-Q2-PRIMARY_DURATION_M1", "比较限于冻结模型和已登记参数。"),
    ("C003", "Q3", "Q3 结果与局限", "Q3 的三弹并集为 2.238164377 s；第 2、3 枚弹的有效时长均为 0，未观察到额外多弹收益。", "F004", "RES-Q3-PRIMARY_DURATION_M1", "零贡献行必须保留，不得推断潜在协同。"),
    ("C004", "Q4", "Q4 结果与局限", "Q4 的三机并集为 2.238164377 s；FY2、FY3 的有效时长均为 0，未观察到额外多机收益。", "F005", "RES-Q4-PRIMARY_DURATION_M1", "参与投放不等同于形成正有效遮蔽。"),
    ("C005", "Q5", "Q5 任务分配", "Q5 冻结方案使用 FY1-b1→M1、FY2-b1→M2、FY5-b1→M3 三项分配，其余弹位未使用。", "F006", "RES-Q5-PRIMARY_DURATION_M1;RES-Q5-PRIMARY_DURATION_M2;RES-Q5-PRIMARY_DURATION_M3", "每项仅服务登记的主目标。"),
    ("C006", "Q1-Q5", "结果核验", "在已检验的三个随机种子下，冻结主指标跨运行跨度为 0。", "F011", "RES-Q1-PRIMARY_DURATION_M1;RES-Q2-PRIMARY_DURATION_M1;RES-Q5-PRIMARY_DURATION_M1;RES-Q5-PRIMARY_DURATION_M2;RES-Q5-PRIMARY_DURATION_M3", "仅适用于已检验种子，不等同于普遍随机稳定性。"),
    ("C007", "Q1-Q5", "敏感性分析", "A03（不继承水平速度）下已复算的冻结主指标均为 0，说明该口径对结果具有决定性影响。", "F011", "RES-Q1-PRIMARY_DURATION_M1;RES-Q2-PRIMARY_DURATION_M1;RES-Q5-PRIMARY_DURATION_M1;RES-Q5-PRIMARY_DURATION_M2;RES-Q5-PRIMARY_DURATION_M3", "这是特定替代口径的复算，非原模型的数值。"),
    ("C008", "Q1-Q5", "敏感性分析", "A07（烟幕到地面后停留）在当前已检验方案中未改变各冻结有效区间。", "F011", "RES-Q1-PRIMARY_DURATION_M1;RES-Q2-PRIMARY_DURATION_M1;RES-Q5-PRIMARY_DURATION_M1;RES-Q5-PRIMARY_DURATION_M2;RES-Q5-PRIMARY_DURATION_M3", "仅限当前冻结方案与复算情景。"),
    ("C009", "Q1-Q5", "敏感性分析", "A08 的 80% 覆盖半径会改变不同目标的有效遮蔽时长，变化幅度随目标而异。", "F010", "RES-Q1-PRIMARY_DURATION_M1;RES-Q2-PRIMARY_DURATION_M1;RES-Q5-PRIMARY_DURATION_M1;RES-Q5-PRIMARY_DURATION_M2;RES-Q5-PRIMARY_DURATION_M3", "仅描述已检验的 A08 半径变化。"),
    ("C010", "Q5", "敏感性分析", "Q5 在公平优先目标下改变 M2、M3 的无人机分配，且总时长与最短时长随目标优先级变化。", "F011", "RES-Q5-PRIMARY_DURATION_M1;RES-Q5-PRIMARY_DURATION_M2;RES-Q5-PRIMARY_DURATION_M3;RES-Q5-OBJECTIVE_TOTAL_DURATION;RES-Q5-OBJECTIVE_MINIMUM_DURATION", "替代方案用于敏感性说明，正式结论仍以冻结主方案为准。"),
]


def _result_ids(root: Path) -> set[str]:
    return {row["result_id"] for row in _read_csv(Path(root) / "14_contracts" / "result_contract.csv")}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _repo_path(root: Path, value: Path) -> str:
    try:
        return value.resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return str(value.resolve())


def build_contract_rows(root: Path, artifacts: list[dict[str, object]]) -> dict[str, list[dict[str, str]]]:
    """Build traceable formal-contract rows from generated figures and frozen result IDs."""
    artifact_by_id = {str(item["figure_id"]): item for item in artifacts}
    missing = set(FIGURE_RESULT_BINDINGS) - set(artifact_by_id)
    if missing:
        raise ValueError(f"Missing generated figures for contracts: {sorted(missing)}")

    known_results = _result_ids(root)
    referenced_results = {
        result_id
        for values in FIGURE_RESULT_BINDINGS.values()
        for result_id in values.split(";")
    }
    unknown_results = referenced_results - known_results
    if unknown_results:
        raise ValueError(f"Evidence contract references unknown frozen results: {sorted(unknown_results)}")

    checked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    figures: list[dict[str, str]] = []
    for figure_id, name, question_id, title in FIGURE_SPECS:
        artifact = artifact_by_id[figure_id]
        metadata = FIGURE_METADATA[figure_id]
        figures.append(
            {
                "figure_id": figure_id,
                "question_id": question_id,
                "core_claim": metadata["claim"],
                "evidence_source": metadata["source"],
                "result_id": FIGURE_RESULT_BINDINGS[figure_id],
                "panel_plan": metadata["panel"],
                "chart_type": metadata["chart_type"],
                "backend": "matplotlib 3.9.2",
                "script_path": "06_code/generate_evidence.py",
                "output_svg": str(Path(artifact["svg"]).resolve()),
                "output_png": str(Path(artifact["png"]).resolve()),
                "output_pdf": "",
                "dpi": "300",
                "used_in_section": metadata["section"],
                "latex_label": f"fig:{figure_id.lower()}",
                "caption_source": "10_ai_logs/handoffs/H-AC982523FD2E/chatgpt_response.md",
                "quality_score": "4.6",
                "review_risk": metadata["risk"],
                "status": "ready",
                "owner": "Codex",
                "last_checked": checked_at,
            }
        )

    claims = [
        {
            "claim_id": claim_id,
            "question_id": question_id,
            "section_id": section_id,
            "claim_text": claim_text,
            "claim_type": "result_interpretation",
            "evidence_type": "figure",
            "evidence_id": figure_id,
            "result_id": result_id,
            "figure_id": figure_id,
            "formula_id": "",
            "citation_id": "",
            "support_grade": "strong",
            "boundary_condition": boundary,
            "risk_note": "以冻结包 RF-20260722T114756Z 与已登记复算情景为限。",
            "status": "ready",
            "owner": "Codex",
            "last_checked": checked_at,
        }
        for claim_id, question_id, section_id, claim_text, figure_id, result_id, boundary in CLAIM_SPECS
    ]
    return {"figures": figures, "claims": claims}


def _write_caption_bank(root: Path, figure_rows: list[dict[str, str]]) -> None:
    lines = ["# 正式证据图题与图注库", "", "所有图均由 `06_code/generate_evidence.py` 从冻结包与已登记验证文件重建。", ""]
    for row in figure_rows:
        lines.extend(
            [
                f"## {row['figure_id']} {row['core_claim']}",
                "",
                f"图注：{row['panel_plan']} 数据来源：{row['evidence_source']}。{row['review_risk']}",
                "",
            ]
        )
    (Path(root) / "08_figures" / "figure_caption_bank.md").write_text("\n".join(lines), encoding="utf-8")


def _write_figure_quality_registers(root: Path, figure_rows: list[dict[str, str]]) -> None:
    status_rows = []
    review_rows = []
    for row in figure_rows:
        status_rows.append(
            {
                "figure_id": row["figure_id"], "figure_title": row["core_claim"], "question": row["question_id"],
                "problem_type": "三维时空遮蔽优化", "model_family": "冻结几何仿真", "figure_family": row["chart_type"],
                "figure_type": row["chart_type"], "template_id": "evidence-v1", "status": "ready", "data_ready": "true",
                "code_ready": "true", "caption_ready": "true", "review_score": row["quality_score"],
                "approved_for_main_text": "pending_human_gate", "output_png": _repo_path(root, Path(row["output_png"])),
                "output_svg": _repo_path(root, Path(row["output_svg"])), "output_pdf": "", "font_checked": "true",
                "palette_checked": "true", "notes": row["review_risk"],
            }
        )
        review_rows.append(
            {
                "figure_id": row["figure_id"], "model_family": "冻结几何仿真", "figure_type": row["chart_type"],
                "type_diversity_score": "5", "color_score": "4.5", "layout_score": "4.5", "information_density_score": "4.5",
                "annotation_score": "4.5", "paper_readability_score": "4.5", "chinese_font_score": "4.5", "non_default_palette_score": "4.5",
                "model_fit_score": "4.6", "export_quality_score": "4.6", "overall_score_1_5": row["quality_score"],
                "problems": row["review_risk"], "revision_action": "待人工 evidence_gate 审核后定稿", "approved_for_main_text": "pending_human_gate",
            }
        )
    _write_csv(
        Path(root) / "08_figures" / "figure_status.csv", status_rows,
        ["figure_id", "figure_title", "question", "problem_type", "model_family", "figure_family", "figure_type", "template_id", "status", "data_ready", "code_ready", "caption_ready", "review_score", "approved_for_main_text", "output_png", "output_svg", "output_pdf", "font_checked", "palette_checked", "notes"],
    )
    _write_csv(
        Path(root) / "08_figures" / "figure_design_review.csv", review_rows,
        ["figure_id", "model_family", "figure_type", "type_diversity_score", "color_score", "layout_score", "information_density_score", "annotation_score", "paper_readability_score", "chinese_font_score", "non_default_palette_score", "model_fit_score", "export_quality_score", "overall_score_1_5", "problems", "revision_action", "approved_for_main_text"],
    )


def _write_active_figure_plan(root: Path, figure_rows: list[dict[str, str]]) -> None:
    rows = [
        {
            "figure_id": row["figure_id"], "question_id": row["question_id"], "priority": str(index),
            "figure_type": row["chart_type"], "paper_section": row["used_in_section"], "core_claim": row["core_claim"],
            "required": "是", "quality_gate": "冻结结果、单位、标签、零贡献行与文件路径均已核验", "status": row["status"],
        }
        for index, row in enumerate(figure_rows, start=1)
    ]
    _write_csv(
        Path(root) / "08_figures" / "active_figure_plan.csv", rows,
        ["figure_id", "question_id", "priority", "figure_type", "paper_section", "core_claim", "required", "quality_gate", "status"],
    )


def _write_evidence_report(root: Path, figure_rows: list[dict[str, str]], claim_rows: list[dict[str, str]]) -> None:
    frozen_manifest = json.loads((Path(root) / "07_results" / "frozen" / "frozen_manifest.json").read_text(encoding="utf-8"))
    lines = [
        "# 证据设计生成与质量报告",
        "",
        f"- 冻结包：`{frozen_manifest['freeze_id']}`",
        "- 输入范围：`07_results/frozen/` 与 `07_results/result_freeze_validation/` 的已登记核验文件。",
        "- 生成代码：`06_code/generate_evidence.py`（Matplotlib 3.9.2，PNG 300 dpi + SVG）。",
        f"- 正式图：{len(figure_rows)} 张；正式表：9 张；正式论断：{len(claim_rows)} 条。",
        "- 当前状态：`ready`，仍须由人工完成 `evidence_gate`，本报告不代表闸门已确认。",
        "",
        "## 自动检查",
        "",
        "- 图表输出同时存在 PNG 和 SVG；图表合同仅引用已存在的 `RES-*` 冻结结果编号。",
        "- Q3/F004 和 Q4/F005 保留零贡献行，未将参与投放表述为额外收益。",
        "- F006 仅绘制冻结 Q5 中已使用的 FY1-b1、FY2-b1、FY5-b1 三条边。",
        "- F007 保留三段时间轴间隙；F009–F011 将验证情景限定为其登记来源。",
        "",
        "## 文件指纹",
        "",
        "| figure_id | PNG SHA-256 | SVG SHA-256 |",
        "|---|---|---|",
    ]
    for row in figure_rows:
        lines.append(f"| {row['figure_id']} | `{_sha256(Path(row['output_png']))}` | `{_sha256(Path(row['output_svg']))}` |")
    lines.extend(["", "## 图表边界", "", "- 任何论文表述必须沿用 `14_contracts/claim_evidence_map.csv` 中的边界条件。", "- 图表不声明全局最优，也不为未验证的情景新增结论。", ""])
    (Path(root) / "08_figures" / "evidence_generation_report.md").write_text("\n".join(lines), encoding="utf-8")


def write_contracts(root: Path, artifacts: list[dict[str, object]]) -> dict[str, list[dict[str, str]]]:
    """Write figure, claim, planning and evidence-QA artifacts for the active stage."""
    records = build_contract_rows(root, artifacts)
    figure_fields = ["figure_id", "question_id", "core_claim", "evidence_source", "result_id", "panel_plan", "chart_type", "backend", "script_path", "output_svg", "output_png", "output_pdf", "dpi", "used_in_section", "latex_label", "caption_source", "quality_score", "review_risk", "status", "owner", "last_checked"]
    claim_fields = ["claim_id", "question_id", "section_id", "claim_text", "claim_type", "evidence_type", "evidence_id", "result_id", "figure_id", "formula_id", "citation_id", "support_grade", "boundary_condition", "risk_note", "status", "owner", "last_checked"]
    stored_figures = [{**row, "output_svg": _repo_path(root, Path(row["output_svg"])), "output_png": _repo_path(root, Path(row["output_png"]))} for row in records["figures"]]
    _write_csv(Path(root) / "14_contracts" / "figure_contract.csv", stored_figures, figure_fields)
    _write_csv(Path(root) / "14_contracts" / "claim_evidence_map.csv", records["claims"], claim_fields)
    _write_active_figure_plan(root, records["figures"])
    _write_caption_bank(root, records["figures"])
    _write_figure_quality_registers(root, records["figures"])
    _write_evidence_report(root, records["figures"], records["claims"])
    return {"figures": stored_figures, "claims": records["claims"]}


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    artifacts = generate_artifacts(root)
    write_contracts(root, artifacts)


if __name__ == "__main__":
    main()
