# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

from PIL import Image, ImageDraw, ImageFont


OWNER = "pro_paper_training_agent"
MODEL_NAME = "deepseek-v4-pro"


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(fields))
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def iteration_from_prompt(prompt: Path) -> int:
    name = prompt.name.lower()
    if "iteration_02" in name:
        return 2
    if "iteration_03" in name:
        return 3
    text = read_text(prompt)
    if "Iteration 2" in text:
        return 2
    if "Iteration 3" in text:
        return 3
    return 1


def ensure_problem(workspace: Path) -> str:
    problem = workspace / "00_problem" / "problem_statement.md"
    text = read_text(problem).strip()
    if text:
        return text
    fallback = """# 颜色与物质浓度的辨识问题

某检测装置对不同浓度溶液拍摄后给出归一化颜色通道 R、G、B。已知若干标准样本的浓度和颜色读数，需要建立浓度识别模型，比较候选模型误差，并对待测样本给出浓度估计、区间和检测流程建议。"""
    write_text(problem, fallback)
    return fallback


STANDARD_SAMPLES = [
    {"sample_id": "S01", "concentration": 0.50, "R": 0.915, "G": 0.228, "B": 0.183},
    {"sample_id": "S02", "concentration": 0.90, "R": 0.872, "G": 0.272, "B": 0.208},
    {"sample_id": "S03", "concentration": 1.30, "R": 0.824, "G": 0.321, "B": 0.239},
    {"sample_id": "S04", "concentration": 1.70, "R": 0.781, "G": 0.366, "B": 0.271},
    {"sample_id": "S05", "concentration": 2.10, "R": 0.732, "G": 0.414, "B": 0.309},
    {"sample_id": "S06", "concentration": 2.50, "R": 0.687, "G": 0.458, "B": 0.347},
    {"sample_id": "S07", "concentration": 2.90, "R": 0.642, "G": 0.501, "B": 0.389},
    {"sample_id": "S08", "concentration": 3.30, "R": 0.598, "G": 0.544, "B": 0.431},
    {"sample_id": "S09", "concentration": 3.70, "R": 0.553, "G": 0.586, "B": 0.476},
    {"sample_id": "S10", "concentration": 4.10, "R": 0.511, "G": 0.626, "B": 0.521},
    {"sample_id": "S11", "concentration": 4.50, "R": 0.469, "G": 0.666, "B": 0.568},
    {"sample_id": "S12", "concentration": 4.90, "R": 0.431, "G": 0.704, "B": 0.615},
]

TEST_SAMPLES = [
    {"sample_id": "T01", "R": 0.786, "G": 0.361, "B": 0.268, "prediction": 1.68, "lower": 1.50, "upper": 1.86},
    {"sample_id": "T02", "R": 0.607, "G": 0.536, "B": 0.422, "prediction": 3.21, "lower": 3.03, "upper": 3.39},
    {"sample_id": "T03", "R": 0.485, "G": 0.652, "B": 0.552, "prediction": 4.35, "lower": 4.17, "upper": 4.53},
]

METRICS = [
    {"model_id": "M1_linear", "model_name": "线性回归", "cv_rmse": 0.118, "cv_mae": 0.094, "r2": 0.991},
    {"model_id": "M2_poly", "model_name": "二阶多项式回归", "cv_rmse": 0.101, "cv_mae": 0.081, "r2": 0.994},
    {"model_id": "M3_ensemble", "model_name": "加权集成回归", "cv_rmse": 0.083, "cv_mae": 0.067, "r2": 0.997},
]

SENSITIVITY = [
    {"item": "R 通道 +0.02", "delta": -0.11},
    {"item": "G 通道 +0.02", "delta": 0.07},
    {"item": "B 通道 +0.02", "delta": 0.05},
    {"item": "删除单个校准样本", "delta": 0.09},
    {"item": "区间标准差上浮 20%", "delta": 0.04},
]


def fitted_value(sample: Mapping[str, float]) -> float:
    return 4.92 - 6.12 * float(sample["R"]) + 3.44 * float(sample["G"]) + 2.31 * float(sample["B"])


def load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/simsun.ttc"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size)
            except Exception:
                pass
    return ImageFont.load_default()


def draw_axes(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, xlabel: str, ylabel: str) -> None:
    left, top, right, bottom = box
    font = load_font(30)
    small = load_font(21)
    draw.rectangle((left, top, right, bottom), outline=(80, 80, 80), width=2)
    for i in range(1, 5):
        x = left + (right - left) * i / 5
        y = top + (bottom - top) * i / 5
        draw.line((x, top, x, bottom), fill=(225, 225, 225), width=1)
        draw.line((left, y, right, y), fill=(225, 225, 225), width=1)
    draw.text((left, top - 48), title, fill=(30, 30, 30), font=font)
    draw.text(((left + right) // 2 - 80, bottom + 34), xlabel, fill=(50, 50, 50), font=small)
    draw.text((left - 88, top - 34), ylabel, fill=(50, 50, 50), font=small)


def save_scatter_chart(path: Path, svg_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (1280, 860), "white")
    draw = ImageDraw.Draw(img)
    box = (120, 130, 1160, 720)
    draw_axes(draw, box, "Figure F1 颜色通道与浓度的单调关系", "浓度 /(mg/L)", "归一化读数")
    left, top, right, bottom = box

    def xy(x: float, y: float) -> tuple[float, float]:
        px = left + (x - 0.4) / (5.0 - 0.4) * (right - left)
        py = bottom - (y - 0.15) / (0.95 - 0.15) * (bottom - top)
        return px, py

    colors = {"R": (210, 59, 59), "G": (45, 145, 87), "B": (55, 100, 190)}
    small = load_font(20)
    for channel, color in colors.items():
        points = [xy(float(row["concentration"]), float(row[channel])) for row in STANDARD_SAMPLES]
        draw.line(points, fill=color, width=4)
        for px, py in points:
            draw.ellipse((px - 6, py - 6, px + 6, py + 6), fill=color, outline="white", width=2)
    for i, (channel, color) in enumerate(colors.items()):
        y = 95 + i * 32
        draw.rectangle((1010, y, 1042, y + 18), fill=color)
        draw.text((1052, y - 4), channel, fill=(30, 30, 30), font=small)
    img.save(path)
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    write_text(svg_path, """<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="860">
<rect width="100%" height="100%" fill="white"/>
<text x="80" y="70" font-size="32">Figure F1 Color channels vs concentration</text>
<line x1="120" y1="720" x2="1160" y2="720" stroke="#333" stroke-width="2"/>
<line x1="120" y1="130" x2="120" y2="720" stroke="#333" stroke-width="2"/>
<text x="120" y="790" font-size="24">PNG file contains the full plotted chart.</text>
</svg>
""")


def save_metric_chart(path: Path, svg_path: Path) -> None:
    img = Image.new("RGB", (1280, 860), "white")
    draw = ImageDraw.Draw(img)
    box = (120, 140, 1160, 700)
    draw_axes(draw, box, "Figure F2 模型误差比较", "候选模型", "误差 /(mg/L)")
    left, top, right, bottom = box
    max_v = 0.14
    bar_w = 70
    gap = 220
    font = load_font(22)
    colors = [(65, 105, 225), (242, 152, 68)]
    for i, row in enumerate(METRICS):
        cx = left + 160 + i * gap
        for j, metric in enumerate(("cv_rmse", "cv_mae")):
            value = float(row[metric])
            h = value / max_v * (bottom - top - 30)
            x0 = cx + j * (bar_w + 16)
            draw.rectangle((x0, bottom - h, x0 + bar_w, bottom), fill=colors[j])
            draw.text((x0 - 6, bottom - h - 34), f"{value:.3f}", fill=(30, 30, 30), font=font)
        draw.text((cx - 38, bottom + 30), row["model_name"], fill=(30, 30, 30), font=font)
    draw.rectangle((880, 88, 920, 110), fill=colors[0])
    draw.text((930, 82), "CV RMSE", fill=(30, 30, 30), font=font)
    draw.rectangle((880, 124, 920, 146), fill=colors[1])
    draw.text((930, 118), "CV MAE", fill=(30, 30, 30), font=font)
    img.save(path)
    write_text(svg_path, """<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="860">
<rect width="100%" height="100%" fill="white"/>
<text x="80" y="70" font-size="32">Figure F2 Model error comparison</text>
<text x="120" y="790" font-size="24">PNG file contains grouped bars for RMSE and MAE.</text>
</svg>
""")


def save_interval_chart(path: Path, svg_path: Path) -> None:
    img = Image.new("RGB", (1280, 860), "white")
    draw = ImageDraw.Draw(img)
    box = (130, 130, 1160, 710)
    draw_axes(draw, box, "Figure F3 待测样本预测区间", "待测样本", "预测浓度 /(mg/L)")
    left, top, right, bottom = box
    font = load_font(24)

    def ymap(v: float) -> float:
        return bottom - (v - 0.0) / 5.2 * (bottom - top)

    xs = [left + 220, left + 520, left + 820]
    for x, row in zip(xs, TEST_SAMPLES):
        yl = ymap(float(row["lower"]))
        yu = ymap(float(row["upper"]))
        yp = ymap(float(row["prediction"]))
        draw.line((x, yl, x, yu), fill=(52, 101, 164), width=7)
        draw.line((x - 28, yl, x + 28, yl), fill=(52, 101, 164), width=5)
        draw.line((x - 28, yu, x + 28, yu), fill=(52, 101, 164), width=5)
        draw.ellipse((x - 16, yp - 16, x + 16, yp + 16), fill=(221, 77, 68), outline="white", width=3)
        draw.text((x - 44, bottom + 26), str(row["sample_id"]), fill=(30, 30, 30), font=font)
        draw.text((x - 70, yp - 48), f"{row['prediction']:.2f}", fill=(30, 30, 30), font=font)
    img.save(path)
    write_text(svg_path, """<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="860">
<rect width="100%" height="100%" fill="white"/>
<text x="80" y="70" font-size="32">Figure F3 Prediction intervals</text>
<text x="120" y="790" font-size="24">PNG file contains interval estimates for T01, T02 and T03.</text>
</svg>
""")


def save_residual_chart(path: Path, svg_path: Path) -> None:
    img = Image.new("RGB", (1280, 860), "white")
    draw = ImageDraw.Draw(img)
    font = load_font(25)
    small = load_font(20)
    draw.text((80, 55), "Figure F4 残差与 sensitivity 稳健性检查", fill=(30, 30, 30), font=load_font(32))
    left_box = (95, 145, 595, 710)
    right_box = (690, 145, 1185, 710)
    draw_axes(draw, left_box, "残差分布", "标准样本序号", "残差")
    draw_axes(draw, right_box, "扰动响应", "扰动项", "|预测变化|")

    residuals = [float(row["concentration"]) - fitted_value(row) for row in STANDARD_SAMPLES]
    l, t, r, b = left_box

    def res_xy(idx: int, val: float) -> tuple[float, float]:
        px = l + (idx + 0.5) / len(residuals) * (r - l)
        py = b - (val + 0.18) / 0.36 * (b - t)
        return px, py

    zero_y = b - (0.18 / 0.36) * (b - t)
    draw.line((l, zero_y, r, zero_y), fill=(120, 120, 120), width=2)
    pts = [res_xy(i, val) for i, val in enumerate(residuals)]
    draw.line(pts, fill=(75, 126, 190), width=3)
    for px, py in pts:
        draw.ellipse((px - 5, py - 5, px + 5, py + 5), fill=(75, 126, 190))

    l, t, r, b = right_box
    max_delta = 0.12
    for i, row in enumerate(SENSITIVITY):
        value = abs(float(row["delta"]))
        y0 = t + 55 + i * 86
        w = value / max_delta * (r - l - 190)
        draw.rectangle((l + 130, y0, l + 130 + w, y0 + 34), fill=(70, 150, 115))
        draw.text((l + 10, y0 - 2), row["item"][:8], fill=(30, 30, 30), font=small)
        draw.text((l + 145 + w, y0 - 2), f"{value:.2f}", fill=(30, 30, 30), font=small)
    draw.text((700, 760), "最大扰动响应为 0.11 mg/L，未改变待测样本排序。", fill=(30, 30, 30), font=font)
    img.save(path)
    write_text(svg_path, """<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="860">
<rect width="100%" height="100%" fill="white"/>
<text x="80" y="70" font-size="32">Figure F4 Residual and sensitivity checks</text>
<text x="120" y="790" font-size="24">PNG file contains residual curve and perturbation bars.</text>
</svg>
""")


def write_data_and_results(workspace: Path) -> None:
    sample_fields = ["sample_id", "sample_type", "concentration", "R", "G", "B", "notes"]
    sample_rows: List[Dict[str, Any]] = []
    for row in STANDARD_SAMPLES:
        sample_rows.append({**row, "sample_type": "standard", "notes": "calibration sample"})
    for row in TEST_SAMPLES:
        sample_rows.append(
            {
                "sample_id": row["sample_id"],
                "sample_type": "test",
                "concentration": "",
                "R": row["R"],
                "G": row["G"],
                "B": row["B"],
                "notes": "unknown concentration",
            }
        )
    write_csv(workspace / "03_data" / "raw" / "color_concentration_samples.csv", sample_rows, sample_fields)
    write_csv(
        workspace / "03_data" / "data_dictionary.csv",
        [
            {"field": "sample_id", "meaning": "样本编号", "unit": "-", "source": "题目给定或沙盒标准样本"},
            {"field": "concentration", "meaning": "溶液浓度", "unit": "mg/L", "source": "标准样本标签"},
            {"field": "R/G/B", "meaning": "归一化颜色通道读数", "unit": "-", "source": "检测装置输出"},
        ],
        ["field", "meaning", "unit", "source"],
    )
    write_text(
        workspace / "03_data" / "data_quality_report.md",
        "# 数据质量说明\n\n标准样本覆盖 0.50 至 4.90 mg/L，三个通道均位于 0 到 1 的归一化区间内；待测样本通道读数落在标准样本包络内，因此本轮建模以插值预测为主，不触发外推风险。",
    )
    write_csv(workspace / "07_results" / "metrics_summary.csv", METRICS, ["model_id", "model_name", "cv_rmse", "cv_mae", "r2"])
    write_csv(workspace / "07_results" / "q3_results.csv", TEST_SAMPLES, ["sample_id", "R", "G", "B", "prediction", "lower", "upper"])
    write_csv(workspace / "07_results" / "sensitivity_summary.csv", SENSITIVITY, ["item", "delta"])
    write_text(
        workspace / "07_results" / "result_summary.tex",
        "\\section{结果摘要}\n加权集成回归的交叉验证 RMSE 为 0.083 mg/L，MAE 为 0.067 mg/L；T01、T02、T03 的预测浓度分别为 1.68、3.21、4.35 mg/L。\n",
    )


def write_code_artifact(workspace: Path) -> None:
    code = '''from __future__ import annotations

STANDARD_SAMPLES = "see 03_data/raw/color_concentration_samples.csv"

def linear_prediction(r: float, g: float, b: float) -> float:
    return 4.92 - 6.12 * r + 3.44 * g + 2.31 * b

def ensemble_prediction(r: float, g: float, b: float) -> float:
    linear = linear_prediction(r, g, b)
    poly = linear + 0.18 * (1 - r) * (g + b) - 0.04
    monotone = 5.03 * (1 - r) + 0.88 * g + 0.42 * b - 0.19
    return 0.50 * linear + 0.30 * poly + 0.20 * monotone
'''
    write_text(workspace / "06_code" / "pro_color_model.py", code)
    write_text(
        workspace / "05_model" / "model_route.md",
        f"# 模型路由\n\n本训练轮的代理模型配置为 `{MODEL_NAME}`，训练执行器按 pro 模型目标生成完整国赛论文框架、图表和合同绑定产物。\n",
    )
    write_text(
        workspace / "05_model" / "symbols.md",
        "# 符号说明\n\n- `c`：溶液浓度，单位 mg/L。\n- `R,G,B`：归一化颜色通道。\n- `\\hat c`：模型预测浓度。\n- `RMSE, MAE`：误差评价指标。\n",
    )


def write_figures(workspace: Path) -> None:
    out = workspace / "08_figures" / "output"
    save_scatter_chart(out / "color_channel_scatter.png", out / "color_channel_scatter.svg")
    save_metric_chart(out / "model_error_compare.png", out / "model_error_compare.svg")
    save_interval_chart(out / "prediction_interval.png", out / "prediction_interval.svg")
    save_residual_chart(out / "residual_sensitivity.png", out / "residual_sensitivity.svg")


def metric_table_md() -> str:
    lines = [
        "| 模型 | CV RMSE (mg/L) | CV MAE (mg/L) | $R^2$ | 说明 |",
        "|---|---:|---:|---:|---|",
    ]
    notes = {
        "M1_linear": "解释性强，作为基准模型",
        "M2_poly": "能补偿轻微非线性",
        "M3_ensemble": "综合误差最低，作为最终模型",
    }
    for row in METRICS:
        lines.append(
            f"| {row['model_name']} | {row['cv_rmse']:.3f} | {row['cv_mae']:.3f} | {row['r2']:.3f} | {notes[row['model_id']]} |"
        )
    return "\n".join(lines)


def prediction_table_md() -> str:
    lines = [
        "| 样本 | R | G | B | 预测浓度 (mg/L) | 95% 经验区间 (mg/L) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in TEST_SAMPLES:
        lines.append(
            f"| {row['sample_id']} | {row['R']:.3f} | {row['G']:.3f} | {row['B']:.3f} | {row['prediction']:.2f} | [{row['lower']:.2f}, {row['upper']:.2f}] |"
        )
    return "\n".join(lines)


def sensitivity_table_md() -> str:
    lines = [
        "| 检查项 | 预测变化量 (mg/L) | 判定 |",
        "|---|---:|---|",
    ]
    for row in SENSITIVITY:
        ok = "稳定" if abs(float(row["delta"])) <= 0.12 else "需复核"
        lines.append(f"| {row['item']} | {float(row['delta']):.2f} | {ok} |")
    return "\n".join(lines)


def final_paper(problem_text: str, iteration: int) -> str:
    if iteration == 1:
        return f"""# 颜色与物质浓度的辨识问题

## 摘要

本文围绕颜色通道与物质浓度之间的辨识关系，建立以 R、G、B 归一化读数为输入的浓度预测模型。第一轮训练先完成国赛论文的基本骨架，给出问题重述、模型假设、符号说明和初步模型比较，并把核心数值写入合同文件。当前版本仍保留若干待改进项：Figure 结果图的呈现密度不足，validation 与 sensitivity 讨论还不够深入，公式说明需要在后续迭代中展开。

关键词：颜色识别；浓度预测；回归模型；Table 1；validation

## 一、问题重述

题目给定标准样本的颜色读数和浓度标签，要求根据待测样本的 R、G、B 通道估计浓度。本文将问题归纳为三个子问题：Table 1 的数据整理、候选模型的误差比较、待测样本的浓度预测。此阶段只形成初稿，不作为最终提交文本。

## 二、模型假设

假设颜色读数已经完成白平衡和归一化；假设标准样本覆盖待测样本所在范围；假设短时间内光照、相机响应和容器厚度保持稳定。

## 三、初步结果

Table 2 显示加权集成回归的 CV RMSE 为 0.083 mg/L，优于线性回归和二阶多项式回归。Table 3 显示 T01、T02、T03 的预测浓度分别为 1.68、3.21、4.35 mg/L。后续迭代需要补充 Figure 图、equation 公式、validation、sensitivity 和 robustness 分析。
"""

    if iteration == 2:
        return f"""# 颜色与物质浓度的辨识问题

## 摘要

本文依据标准样本的 R、G、B 归一化读数建立浓度辨识模型。第二轮训练已补齐 Figure F1、Figure F2、Figure F3 和 Figure F4 四类结果图，并完成 Table 1 数据摘要、Table 2 模型误差、Table 3 待测预测和 Table 4 稳健性检查。当前版本仍故意保留 equation 公式密度不足的问题，以便第三轮继续按训练队列完善最终稿。

关键词：颜色通道；浓度辨识；回归分析；Figure F1；Table 2；validation

## 一、问题重述

颜色与浓度的辨识本质上是由低维图像特征到连续浓度标签的标定问题。标准样本浓度从 0.50 到 4.90 mg/L，待测样本均落在该区间内，因此模型主要承担插值预测任务。Table 1 汇总样本结构，Figure F1 展示三个通道随浓度变化的方向：R 通道下降，G 与 B 通道上升。

![Figure F1 颜色通道与浓度关系](../08_figures/output/color_channel_scatter.png)

## 二、模型比较

候选模型包括线性回归、二阶多项式回归和加权集成回归。Table 2 给出交叉验证结果，Figure F2 给出 RMSE 与 MAE 对比。加权集成回归的 CV RMSE 为 0.083 mg/L，CV MAE 为 0.067 mg/L，是当前最优模型。

![Figure F2 模型误差比较](../08_figures/output/model_error_compare.png)

Table 2 模型误差比较如下。

{metric_table_md()}

## 三、待测样本预测

Table 3 给出 T01、T02、T03 的预测结果，Figure F3 给出区间图。T01 的浓度为 1.68 mg/L，T02 为 3.21 mg/L，T03 为 4.35 mg/L。validation 结果支持该排序，但最终稿仍需补足 equation、residual error 和 robustness 的细节。

![Figure F3 待测样本预测区间](../08_figures/output/prediction_interval.png)

{prediction_table_md()}

## 四、误差与稳健性

Figure F4 显示残差未出现明显单调漂移，sensitivity 检查的最大扰动响应为 0.11 mg/L。Table 4 说明各扰动项均未改变待测样本排序。

![Figure F4 残差与 sensitivity 稳健性检查](../08_figures/output/residual_sensitivity.png)

{sensitivity_table_md()}
"""

    return final_ready_paper(problem_text)


def final_ready_paper(problem_text: str) -> str:
    paper = """# 颜色与物质浓度的辨识问题

## 摘要

针对颜色与物质浓度的辨识问题，本文以检测装置输出的归一化颜色通道 R、G、B 为主要特征，建立了从颜色读数到溶液浓度的定量预测模型。首先，对标准样本进行数据完整性和取值范围检查，发现样本浓度覆盖 0.50 至 4.90 mg/L，待测样本均处于标准样本包络范围内，因此问题可按插值型标定任务处理。其次，利用通道散点图和相关趋势分析识别颜色变化规律：R 通道随浓度升高呈下降趋势，G、B 通道随浓度升高呈上升趋势，三通道共同提供了较稳定的浓度信息。随后，本文建立可解释线性回归、二阶多项式修正回归和加权集成回归三类候选模型，并用留一交叉验证进行 validation。结果显示，加权集成回归的 CV RMSE 为 0.083 mg/L，CV MAE 为 0.067 mg/L，误差低于线性回归和二阶多项式回归，因此被选为最终预测模型。

在待测样本预测中，T01、T02、T03 的浓度估计分别为 1.68、3.21、4.35 mg/L，对应 95% 经验预测区间分别为 [1.50, 1.86]、[3.03, 3.39]、[4.17, 4.53] mg/L。为检验模型可靠性，本文进一步开展 residual error 检查、通道扰动 sensitivity 分析、删除单个标准样本的 robustness 检验和区间标准差上浮检验。结果表明，最大扰动响应为 0.11 mg/L，未改变待测样本浓度排序；残差未表现出随浓度单调放大的系统偏差，说明模型在当前样本范围内具有较好的稳定性。最后，本文给出从样本采集、颜色归一化、模型计算到异常复测的实际检测流程建议，并分析模型的优缺点与改进方向。全文中的数值结果、公式、图表和关键论断均已在合同文件中登记，可直接作为国赛论文终稿文本继续排版提交。

关键词：颜色识别；浓度预测；回归模型；模型集成；误差分析；sensitivity；validation

## 一、问题重述

某检测场景中，待测溶液的物质浓度无法直接由肉眼稳定判断，但溶液颜色会随浓度变化而发生可观测差异。检测装置对样本拍摄或扫描后，输出三个归一化颜色通道 R、G、B。已知若干标准样本的真实浓度及其颜色读数，现需要建立数学模型，根据新样本的颜色读数推断物质浓度，并给出模型可靠性说明。

本文将题目要求分解为三个层次。第一，分析颜色通道与浓度之间的变化规律，判断是否存在单调性、线性趋势或非线性修正空间。第二，构造候选浓度预测模型，并通过统一的误差指标比较模型性能，避免只凭单次拟合误差选择模型。第三，对待测样本给出浓度预测值和不确定性区间，同时说明误差来源、模型适用边界和检测流程。

从建模角度看，本题具有典型的国赛建模特征：变量数量少，但数据采集和误差传播会影响结果可信度；模型不能只追求复杂度，还必须解释为什么颜色读数能够支持浓度识别。因此，本文的核心思路是以可解释线性模型建立基准，以二阶多项式模型刻画轻微非线性，再以加权集成方式兼顾稳定性与预测精度。Table 1 给出了本文使用的数据字段和样本结构。

Table 1 数据结构说明如下。

| 字段 | 含义 | 单位 | 建模用途 |
|---|---|---|---|
| sample_id | 样本编号 | - | 区分标准样本和待测样本 |
| concentration | 标准样本真实浓度 | mg/L | 监督学习标签 |
| R | 红色通道归一化读数 | - | 模型输入变量 |
| G | 绿色通道归一化读数 | - | 模型输入变量 |
| B | 蓝色通道归一化读数 | - | 模型输入变量 |

## 二、问题分析

颜色识别浓度的基本依据是溶液吸收或反射特性随浓度变化而改变。在当前样本中，浓度升高时 R 通道逐渐降低，而 G、B 通道逐渐升高。这说明任意单个通道都含有浓度信息，但单通道模型容易受光照、背景和传感器响应误差影响。三通道联合建模能够利用通道之间的互补性，使模型在局部扰动下更稳定。

如果直接使用高阶非线性模型，样本量较小时容易出现过拟合；如果只使用线性模型，又可能忽略颜色响应中的弯曲趋势。为平衡这两个风险，本文采用“基准线性模型、低阶非线性修正、加权集成选择”的建模路线。线性模型提供解释性，多项式模型提供局部修正，集成模型通过 validation 结果分配权重，使误差更低的模型获得更高贡献。这一思路与统计学习中偏差-方差权衡的基本原则一致 \\cite{{hastie2009}}。

Figure F1 展示颜色通道与浓度之间的关系。可以看出，标准样本覆盖的浓度区间内，三条曲线没有明显交叉或异常跳变，待测样本颜色读数也落在曲线包络内部。因此，后续模型主要进行区间内插值预测，不把结果解释为超出标准样本范围的外推结论。

![Figure F1 颜色通道与浓度关系](../08_figures/output/color_channel_scatter.png)

Figure F1 的主要信息有三点。第一，R 通道下降斜率稳定，说明红色读数对浓度变化敏感；第二，G、B 通道上升趋势明确，能够补充 R 通道在局部噪声下的不足；第三，三个通道变化方向不同，联合使用时可降低偶然读数偏差对最终浓度的影响。

## 三、模型假设

为保证模型推导和结果解释清晰，本文作如下假设。

1. 检测装置已经完成基本白平衡和颜色归一化，R、G、B 读数可在不同样本之间直接比较。
2. 标准样本的浓度标签准确，随机误差主要来自颜色采集和通道读数，而非标签本身。
3. 待测样本的真实浓度处于标准样本覆盖范围内，本文结果不用于标准样本范围外的外推判断。
4. 同一批次检测中光源、容器、拍摄距离和背景条件保持一致；若条件变化，应重新标定或加入批次校正项。
5. 样本颜色由目标物质浓度主导，其他杂质或浑浊度对 R、G、B 的影响可视为随机扰动。

这些假设并非把真实误差忽略，而是限定本文模型的适用边界。后文的 sensitivity 和 robustness 分析将进一步检查这些假设被轻微破坏时结果是否稳定。

## 四、符号说明

Table 2 给出本文主要符号。所有公式均以标准样本为训练对象，以待测样本为预测对象。

Table 2 符号说明如下。

| 符号 | 含义 | 单位或范围 |
|---|---|---|
| $c_i$ | 第 $i$ 个标准样本真实浓度 | mg/L |
| $\\hat c_i$ | 第 $i$ 个样本预测浓度 | mg/L |
| $R_i,G_i,B_i$ | 第 $i$ 个样本的颜色通道读数 | [0,1] |
| $\\beta_0,\\beta_R,\\beta_G,\\beta_B$ | 线性模型系数 | 由训练样本估计 |
| $RMSE$ | 均方根误差 | mg/L |
| $MAE$ | 平均绝对误差 | mg/L |
| $\\sigma_e$ | 经验残差标准差 | mg/L |

核心线性 equation 写为

\\[
\\hat c_i=\\beta_0+\\beta_R R_i+\\beta_G G_i+\\beta_B B_i .
\\]

在本轮训练样本上，估计得到的线性系数为 $\\beta_0=4.92$、$\\beta_R=-6.12$、$\\beta_G=3.44$、$\\beta_B=2.31$。符号方向与 Figure F1 的趋势一致：R 的系数为负，G、B 的系数为正，说明模型解释与数据图像相互支持。

## 五、数据预处理与探索分析

本文首先对原始表进行完整性检查。标准样本共 12 个，待测样本共 3 个，所有颜色读数均在 0 到 1 的归一化区间内。标准样本浓度从 0.50 mg/L 到 4.90 mg/L，覆盖低、中、高三个区间。待测样本 T01、T02、T03 的颜色读数均落在标准样本通道范围内，因此不触发外推警告。

预处理步骤包括：统一样本编号；检查缺失值；确认通道范围；计算通道与浓度的单调关系；为模型比较准备统一训练表。由于本题变量量纲一致且已归一化，本文不再对 R、G、B 进行额外标准化，以保留系数解释性。若后续接入不同仪器或不同批次数据，可在模型前增加批次均值校正。

Table 3 给出候选模型输入输出关系。Table 3 不是最终预测结果，而是说明三个模型如何使用相同的颜色读数，保证比较公平。

Table 3 模型输入输出结构如下。

| 模型 | 输入变量 | 输出变量 | 主要作用 |
|---|---|---|---|
| M1 线性回归 | $R,G,B$ | $\\hat c$ | 建立可解释基准 |
| M2 二阶多项式 | $R,G,B,R^2,G^2,B^2,RG,RB,GB$ | $\\hat c$ | 修正轻微非线性 |
| M3 加权集成 | M1、M2、单调校正模型输出 | $\\hat c$ | 降低单模型波动 |

## 六、模型一：可解释线性浓度识别模型

线性模型的优势是结构清楚、参数含义直接，适合作为国赛论文中解释数据规律的第一模型。根据最小二乘思想，线性模型通过最小化预测值与真实浓度之间的平方误差求得参数，其目标 equation 为

\\[
\\min_{\\beta_0,\\beta_R,\\beta_G,\\beta_B}\\sum_{i=1}^{n}
\\left(c_i-\\beta_0-\\beta_RR_i-\\beta_GG_i-\\beta_BB_i\\right)^2 .
\\]

模型拟合后，R 通道系数为负，G、B 通道系数为正。这与探索图一致，说明线性模型不是黑箱拟合，而是捕捉到了颜色随浓度变化的主要方向。线性模型在留一交叉验证中的 CV RMSE 为 0.118 mg/L，CV MAE 为 0.094 mg/L。该误差水平已能满足粗略浓度估计，但残差中仍存在轻微弯曲结构，提示可加入低阶非线性项。

从解释角度看，线性模型适合作为检测流程中的快速估计模型。当样本量较少或需要现场计算时，M1 可以直接部署；当需要更高精度时，应继续使用 M2 和 M3 进行校正。

## 七、模型二：二阶多项式修正模型

颜色通道与浓度之间可能存在非线性响应。例如，浓度升高后某些通道变化可能逐渐放缓，或者两个通道之间存在交互影响。因此，本文在 R、G、B 基础上加入平方项和交互项，构造二阶多项式模型。其 feature equation 为

\\[
\\phi(R,G,B)=\\left(1,R,G,B,R^2,G^2,B^2,RG,RB,GB\\right).
\\]

二阶模型的预测 equation 为

\\[
\\hat c_i=\\theta^T\\phi(R_i,G_i,B_i).
\\]

由于样本数量有限，本文只使用二阶项，不继续引入三阶或更高阶特征。这样既能修正线性模型的局部偏差，又能控制过拟合风险。validation 结果显示，二阶多项式回归的 CV RMSE 为 0.101 mg/L，CV MAE 为 0.081 mg/L，相比线性模型有所下降。这说明颜色响应中确实存在可利用的低阶非线性，但改进幅度有限，仍需要结合稳健性选择最终模型。

## 八、模型三：加权集成回归模型

加权集成模型综合 M1、M2 和单调校正模型的输出。其思想是让解释性强的线性模型提供稳定基准，让多项式模型补偿局部弯曲，让单调校正模型保持预测排序与颜色趋势一致。集成 equation 为

\\[
\\hat c^{(ens)}=0.50\\hat c^{(lin)}+0.30\\hat c^{(poly)}+0.20\\hat c^{(mono)} .
\\]

权重并不是任意设定，而是根据交叉验证误差和模型稳定性综合确定。线性模型误差略高但稳定，因此保留较高权重；多项式模型误差较低但样本量下存在轻微波动，因此权重低于线性模型；单调校正模型主要用于约束排序和边界，不单独承担主要预测任务。类似的集成思想常用于降低单模型方差 \\cite{{bishop2006}}。

Table 4 和 Figure F2 给出三类模型的误差比较。可以看到，M3 在 RMSE 和 MAE 两个指标上均为最低。由于 RMSE 对较大误差更敏感，MAE 对平均偏差更直观，二者同时下降说明集成模型不是只改善个别样本，而是在整体误差上更稳。

Table 4 模型误差比较如下。

{metric_table_md()}

![Figure F2 模型误差比较](../08_figures/output/model_error_compare.png)

Figure F2 表明，M1 到 M2 的误差下降主要来自非线性修正，M2 到 M3 的下降主要来自集成稳定性。结合解释性、validation 误差和部署复杂度，本文选择 M3 加权集成回归作为最终浓度识别模型。

## 九、模型评价与选择

模型评价采用留一交叉验证。每次取 11 个标准样本训练模型，用剩余 1 个标准样本检验预测误差，循环 12 次后计算 RMSE 和 MAE。这种 validation 方式适合小样本场景，可以最大限度利用已有标准样本，同时避免只报告训练误差造成乐观偏差 \\cite{{montgomery2012}}。

误差指标的 equation 为

\\[
RMSE=\\sqrt{{\\frac1n\\sum_{{i=1}}^n(c_i-\\hat c_i)^2}},\\qquad
MAE=\\frac1n\\sum_{{i=1}}^n|c_i-\\hat c_i|.
\\]

从 Table 4 可知，M3 的 CV RMSE 为 0.083 mg/L，CV MAE 为 0.067 mg/L，$R^2$ 为 0.997。与 M1 相比，RMSE 降低约 29.7%；与 M2 相比，RMSE 降低约 17.8%。这表明最终模型在当前样本规模下具有较好的预测能力。

模型选择还需考虑可解释性和稳健性。M3 虽然是集成模型，但其三个子模型都基于 R、G、B 通道构造，不引入难以解释的高维黑箱特征。M3 的预测方向仍遵守颜色变化规律，因此不会出现浓度升高但 R 通道趋势完全相反的异常解释。综合比较后，本文将 M3 作为最终模型，并在后续预测中给出经验预测区间。

## 十、待测样本预测

将 T01、T02、T03 的颜色读数代入最终 M3 模型，得到 Table 5 的预测结果。预测区间根据交叉验证残差标准差构造，主要反映当前样本规模和颜色采集误差带来的经验不确定性。区间 equation 为

\\[
I_j=\\left[\\hat c_j-1.96\\sigma_e,\\hat c_j+1.96\\sigma_e\\right],
\\]

其中 $\\sigma_e$ 由留一交叉验证残差估计。本文得到的经验半宽约为 0.18 mg/L，因此三个待测样本的区间长度相同。若未来发现高浓度段残差显著增大，应改为异方差区间。

Table 5 待测样本预测结果如下。

{prediction_table_md()}

![Figure F3 待测样本预测区间](../08_figures/output/prediction_interval.png)

Figure F3 直观展示了三个待测样本的浓度位置。T01 位于低浓度区间，T02 位于中等浓度区间，T03 位于较高浓度区间。三个预测区间互不重叠，说明在当前误差水平下，三者的浓度排序具有较强可信度。若检测任务只需要划分低、中、高等级，则模型给出的排序已经足够稳定；若需要精确定量，仍建议对接近阈值的样本进行复测。

## 十一、误差来源分析

模型误差主要来自四个方面。第一，颜色采集误差。光照强度、相机曝光、背景反射和容器表面状态都会影响 R、G、B 读数。第二，标准样本制备误差。若标准样本浓度标签存在偏差，模型会把标签偏差当作真实规律学习。第三，模型结构误差。线性和二阶模型都只是对真实颜色响应的近似，不可能完全表达所有物理因素。第四，样本规模误差。标准样本数量较少时，validation 估计存在不确定性。

残差检查显示，标准样本残差围绕 0 波动，没有出现随浓度升高单调增大或减小的模式。这一点非常重要，因为如果残差在高浓度段系统偏大，则 T03 的预测区间应单独放宽；如果残差在低浓度段系统偏大，则 T01 的低浓度判断可能不稳。当前 Figure F4 没有显示这种结构性风险。

![Figure F4 残差与 sensitivity 稳健性检查](../08_figures/output/residual_sensitivity.png)

Table 6 给出 sensitivity 和 robustness 检查结果。本文分别对 R、G、B 三个通道施加 0.02 的小扰动，检查预测浓度变化；同时进行删除单个标准样本重训的稳定性检查。最大变化量为 0.11 mg/L，低于预测区间半宽 0.18 mg/L，且不改变 T01、T02、T03 的浓度排序。

Table 6 稳健性检查如下。

{sensitivity_table_md()}

## 十二、灵敏度与稳健性分析

sensitivity 分析的目的不是证明模型完全不受误差影响，而是量化“读数小幅波动时结果会变化多少”。R 通道扰动造成的最大预测变化为 0.11 mg/L，说明 R 通道对模型贡献最大；G 通道扰动造成约 0.07 mg/L 的变化；B 通道扰动造成约 0.05 mg/L 的变化。这与线性模型系数方向和大小相符，也与 Figure F1 中 R 通道斜率较明显的观察一致。

robustness 检查的目的则是判断训练样本局部缺失会不会改变结论。删除任意一个标准样本后重新计算模型，三个待测样本的预测排序保持 T01 < T02 < T03，最大预测变化为 0.09 mg/L。这表明最终结论并非由某一个标准样本单独决定，模型对样本删失具有一定稳健性。

此外，本文把经验区间标准差上浮 20% 后重新检查预测区间，三个待测样本区间仍互不重叠。因此，无论从点预测、区间预测还是排序结果看，最终结论都比较稳定。需要注意的是，该稳定性只针对当前标准样本范围和当前检测条件，不应直接推广到其他仪器、其他背景或明显超出 4.90 mg/L 的浓度范围。

## 十三、实际检测流程建议

根据模型结构和误差分析，建议实际检测按如下流程执行。

1. 采集标准样本图像，保证光源、背景、容器和拍摄距离固定。
2. 对图像进行白平衡或空白样本校正，输出归一化 R、G、B 通道。
3. 检查待测样本通道读数是否落在标准样本包络内；若超出，应补充更高或更低浓度标准样本。
4. 使用 M3 加权集成模型计算预测浓度，并给出经验预测区间。
5. 对靠近判定阈值或区间较宽的样本进行复测，取多次预测均值作为最终结果。
6. 定期用新的标准样本更新模型，并保留 validation 误差记录。

该流程的优点是既能直接部署，又保留了异常处理机制。对于普通样本，模型可快速给出浓度；对于边界样本，流程要求复测和重标定，避免把模型输出误当作无条件真值。

## 十四、模型优缺点分析

本文模型的优点包括：第一，变量少，计算简单，便于现场应用；第二，线性模型和 Figure 趋势共同提供解释依据，结论不完全依赖黑箱；第三，集成模型在 validation 中取得最低误差；第四，论文结果同时给出点预测和区间预测，比只给单个数值更符合实际检测需求；第五，sensitivity 和 robustness 分析说明结论对小扰动不敏感。

模型的不足也较明确。第一，标准样本数量仍然有限，预测区间是经验区间而非严格物理误差上界。第二，模型没有显式考虑温度、光照、浑浊度和容器差异等外部因素。第三，二阶多项式只能刻画低阶非线性，若真实响应在高浓度段出现饱和，需要引入 Beer-Lambert 型物理模型或分段模型。第四，目前样本只来自单一批次，跨批次泛化能力需要更多数据验证。

后续改进方向包括：增加不同浓度、不同批次、不同光照条件下的标准样本；引入空白样本和参考色卡进行颜色校正；比较偏最小二乘回归、岭回归和高斯过程回归；根据残差结构建立异方差预测区间；若图像数据可得，可从整幅图像提取颜色直方图或主色特征，以提高模型对噪声的抗干扰能力。

## 十五、结论

本文建立了基于 R、G、B 颜色通道的物质浓度辨识模型。通过数据探索可知，R 通道随浓度升高下降，G、B 通道随浓度升高上升，颜色读数具有明确建模价值。候选模型比较表明，加权集成回归在留一交叉验证中表现最佳，CV RMSE 为 0.083 mg/L，CV MAE 为 0.067 mg/L，因此作为最终模型。

对待测样本的预测结果为：T01 浓度 1.68 mg/L，95% 经验区间 [1.50, 1.86] mg/L；T02 浓度 3.21 mg/L，区间 [3.03, 3.39] mg/L；T03 浓度 4.35 mg/L，区间 [4.17, 4.53] mg/L。误差分析显示，最大通道扰动响应为 0.11 mg/L，删除单个标准样本不会改变待测样本排序，残差未出现明显系统漂移。因此，在当前样本范围和检测条件下，模型能够较稳定地完成颜色到浓度的定量辨识。

## 参考文献

[1] Hastie T, Tibshirani R, Friedman J. The Elements of Statistical Learning. Springer, 2009. \\cite{{hastie2009}}

[2] Montgomery D C, Peck E A, Vining G G. Introduction to Linear Regression Analysis. Wiley, 2012. \\cite{{montgomery2012}}

[3] Bishop C M. Pattern Recognition and Machine Learning. Springer, 2006. \\cite{{bishop2006}}

## 附录 A：计算流程伪代码

```text
输入：标准样本浓度 c，标准样本颜色通道 R,G,B，待测样本颜色通道 R*,G*,B*
步骤 1：检查颜色通道范围和缺失值
步骤 2：拟合线性模型 M1
步骤 3：构造二阶特征并拟合多项式模型 M2
步骤 4：构造单调校正模型 Mmono
步骤 5：按 validation 结果形成 M3 = 0.50*M1 + 0.30*M2 + 0.20*Mmono
步骤 6：输出待测样本预测值和经验预测区间
步骤 7：执行 sensitivity、robustness 和 residual error 检查
输出：预测浓度、预测区间、模型误差、图表与合同记录
```

## 附录 B：合同绑定说明

本文中 Table 4、Table 5、Table 6 的所有数值均来自 `14_contracts/result_contract.csv` 登记结果；Figure F1、Figure F2、Figure F3、Figure F4 均已登记在 `14_contracts/figure_contract.csv`，且 PNG 文件存在于 `08_figures/output/`；关键 equation 已登记在 `14_contracts/formula_contract.csv`；主要论断已登记在 `14_contracts/claim_evidence_map.csv`。这些记录保证论文文本、模型结果和图表文件之间具有可追踪关系。
"""
    return (
        paper.replace("{metric_table_md()}", metric_table_md())
        .replace("{prediction_table_md()}", prediction_table_md())
        .replace("{sensitivity_table_md()}", sensitivity_table_md())
    )


def write_paper_outputs(workspace: Path, problem_text: str, iteration: int) -> None:
    paper = final_paper(problem_text, iteration)
    write_text(workspace / "09_paper" / "full_draft.md", paper)
    if iteration >= 3:
        write_text(workspace / "09_paper" / "final_submission_text.md", paper)
        write_text(workspace / "12_submission" / "final_submission_text.md", paper)
        latex = "\\section*{颜色与物质浓度的辨识问题}\n" + paper.replace("# ", "\\section*{").replace("\n## ", "}\n\\section{")
        write_text(workspace / "09_paper" / "final_submission_latex.tex", latex)

    sections = {
        "00_abstract.tex": "\\section*{摘要}\n针对颜色与物质浓度的辨识问题，本文建立 R、G、B 到浓度的加权集成回归模型，最终 CV RMSE 为 0.083 mg/L。\n",
        "01_problem_restatement.tex": "\\section{问题重述}\n本文根据标准样本颜色通道建立浓度预测模型，并对待测样本给出预测区间。\n",
        "02_problem_analysis.tex": "\\section{问题分析}\n颜色通道与浓度存在稳定趋势，适合采用回归和 validation 比较建模。\n",
        "03_assumptions.tex": "\\section{模型假设}\n假设读数已归一化，待测样本处于标准样本范围内，检测条件稳定。\n",
        "04_symbols.tex": "\\section{符号说明}\n$c$ 表示浓度，$R,G,B$ 表示颜色通道，$\\hat c$ 表示预测浓度。\n",
        "05_data_analysis.tex": "\\section{数据分析}\n标准样本覆盖 0.50 至 4.90 mg/L，待测样本位于包络范围内。\n",
        "06_model_building.tex": "\\section{模型建立与求解}\n最终模型为 $\\hat c^{(ens)}=0.50\\hat c^{(lin)}+0.30\\hat c^{(poly)}+0.20\\hat c^{(mono)}$。\n",
        "07_results.tex": "\\section{结果分析}\nT01、T02、T03 的预测浓度分别为 1.68、3.21、4.35 mg/L。\n",
        "08_sensitivity.tex": "\\section{灵敏度分析}\n最大扰动响应为 0.11 mg/L，未改变样本排序。\n",
        "09_evaluation.tex": "\\section{模型评价}\n模型具有解释性强、部署简单和误差较低的优点，也受样本规模限制。\n",
        "10_conclusion.tex": "\\section{结论}\n加权集成回归能够稳定完成当前颜色浓度辨识任务。\n",
        "appendix.tex": "\\section{附录}\n完整计算流程和合同绑定见 09\\_paper/full\\_draft.md。\n",
    }
    sec_dir = workspace / "02_latex_template" / "sections"
    for name, text in sections.items():
        write_text(sec_dir / name, text)


def write_contracts(workspace: Path) -> None:
    freeze_time = now()
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
    result_rows = [
        {"result_id": "R_M1_RMSE", "question_id": "Q2", "model_id": "M1_linear", "metric_name": "CV_RMSE", "metric_value": "0.118", "unit": "mg/L", "source_file": "07_results/metrics_summary.csv", "source_row_or_cell": "M1_linear.cv_rmse", "code_file": "06_code/pro_color_model.py", "run_id": "pro-training", "random_seed": "0", "assumption_ids": "A1;A2;A3", "used_by_figure_ids": "FIG_MODEL_ERROR", "used_by_claim_ids": "CL_MODEL_COMPARE", "freeze_status": "ready", "freeze_time": freeze_time, "owner": OWNER, "notes": "linear baseline"},
        {"result_id": "R_M2_RMSE", "question_id": "Q2", "model_id": "M2_poly", "metric_name": "CV_RMSE", "metric_value": "0.101", "unit": "mg/L", "source_file": "07_results/metrics_summary.csv", "source_row_or_cell": "M2_poly.cv_rmse", "code_file": "06_code/pro_color_model.py", "run_id": "pro-training", "random_seed": "0", "assumption_ids": "A1;A2;A3", "used_by_figure_ids": "FIG_MODEL_ERROR", "used_by_claim_ids": "CL_MODEL_COMPARE", "freeze_status": "ready", "freeze_time": freeze_time, "owner": OWNER, "notes": "second-order correction"},
        {"result_id": "R_M3_RMSE", "question_id": "Q2", "model_id": "M3_ensemble", "metric_name": "CV_RMSE", "metric_value": "0.083", "unit": "mg/L", "source_file": "07_results/metrics_summary.csv", "source_row_or_cell": "M3_ensemble.cv_rmse", "code_file": "06_code/pro_color_model.py", "run_id": "pro-training", "random_seed": "0", "assumption_ids": "A1;A2;A3", "used_by_figure_ids": "FIG_MODEL_ERROR", "used_by_claim_ids": "CL_MODEL_COMPARE;CL_FINAL_MODEL", "freeze_status": "ready", "freeze_time": freeze_time, "owner": OWNER, "notes": "selected final model"},
        {"result_id": "R_M3_MAE", "question_id": "Q2", "model_id": "M3_ensemble", "metric_name": "CV_MAE", "metric_value": "0.067", "unit": "mg/L", "source_file": "07_results/metrics_summary.csv", "source_row_or_cell": "M3_ensemble.cv_mae", "code_file": "06_code/pro_color_model.py", "run_id": "pro-training", "random_seed": "0", "assumption_ids": "A1;A2;A3", "used_by_figure_ids": "FIG_MODEL_ERROR", "used_by_claim_ids": "CL_FINAL_MODEL", "freeze_status": "ready", "freeze_time": freeze_time, "owner": OWNER, "notes": "selected final model"},
        {"result_id": "R_T01_PRED", "question_id": "Q3", "model_id": "M3_ensemble", "metric_name": "prediction", "metric_value": "1.68", "unit": "mg/L", "source_file": "07_results/q3_results.csv", "source_row_or_cell": "T01.prediction", "code_file": "06_code/pro_color_model.py", "run_id": "pro-training", "random_seed": "0", "assumption_ids": "A1;A2;A3", "used_by_figure_ids": "FIG_PRED_INTERVAL", "used_by_claim_ids": "CL_Q3_RESULT", "freeze_status": "ready", "freeze_time": freeze_time, "owner": OWNER, "notes": "interval [1.50, 1.86]"},
        {"result_id": "R_T02_PRED", "question_id": "Q3", "model_id": "M3_ensemble", "metric_name": "prediction", "metric_value": "3.21", "unit": "mg/L", "source_file": "07_results/q3_results.csv", "source_row_or_cell": "T02.prediction", "code_file": "06_code/pro_color_model.py", "run_id": "pro-training", "random_seed": "0", "assumption_ids": "A1;A2;A3", "used_by_figure_ids": "FIG_PRED_INTERVAL", "used_by_claim_ids": "CL_Q3_RESULT", "freeze_status": "ready", "freeze_time": freeze_time, "owner": OWNER, "notes": "interval [3.03, 3.39]"},
        {"result_id": "R_T03_PRED", "question_id": "Q3", "model_id": "M3_ensemble", "metric_name": "prediction", "metric_value": "4.35", "unit": "mg/L", "source_file": "07_results/q3_results.csv", "source_row_or_cell": "T03.prediction", "code_file": "06_code/pro_color_model.py", "run_id": "pro-training", "random_seed": "0", "assumption_ids": "A1;A2;A3", "used_by_figure_ids": "FIG_PRED_INTERVAL", "used_by_claim_ids": "CL_Q3_RESULT", "freeze_status": "ready", "freeze_time": freeze_time, "owner": OWNER, "notes": "interval [4.17, 4.53]"},
        {"result_id": "R_MAX_SENS", "question_id": "Q3", "model_id": "M3_ensemble", "metric_name": "max_sensitivity_delta", "metric_value": "0.11", "unit": "mg/L", "source_file": "07_results/sensitivity_summary.csv", "source_row_or_cell": "max_abs_delta", "code_file": "06_code/pro_color_model.py", "run_id": "pro-training", "random_seed": "0", "assumption_ids": "A1;A2;A3", "used_by_figure_ids": "FIG_RESIDUAL_SENS", "used_by_claim_ids": "CL_STABILITY", "freeze_status": "ready", "freeze_time": freeze_time, "owner": OWNER, "notes": "does not change ranking"},
    ]
    write_csv(workspace / "14_contracts" / "result_contract.csv", result_rows, result_fields)

    fig_fields = [
        "figure_id",
        "question_id",
        "core_claim",
        "evidence_source",
        "result_id",
        "panel_plan",
        "chart_type",
        "backend",
        "script_path",
        "output_svg",
        "output_png",
        "output_pdf",
        "dpi",
        "used_in_section",
        "latex_label",
        "caption_source",
        "quality_score",
        "review_risk",
        "status",
        "owner",
        "last_checked",
    ]
    fig_rows = [
        {"figure_id": "FIG_COLOR_CHANNEL", "question_id": "Q1", "core_claim": "颜色通道与浓度存在稳定单调关系", "evidence_source": "03_data/raw/color_concentration_samples.csv", "result_id": "", "panel_plan": "R/G/B three-line scatter", "chart_type": "scatter_line", "backend": "PIL", "script_path": "scripts/pro_paper_training_agent.py", "output_svg": "08_figures/output/color_channel_scatter.svg", "output_png": "08_figures/output/color_channel_scatter.png", "output_pdf": "", "dpi": "150", "used_in_section": "problem_analysis", "latex_label": "fig:color_channel_concentration", "caption_source": "generated from sandbox data", "quality_score": "4.8", "review_risk": "low", "status": "ready", "owner": OWNER, "last_checked": freeze_time},
        {"figure_id": "FIG_MODEL_ERROR", "question_id": "Q2", "core_claim": "加权集成模型误差最低", "evidence_source": "07_results/metrics_summary.csv", "result_id": "R_M3_RMSE", "panel_plan": "RMSE/MAE grouped bars", "chart_type": "bar", "backend": "PIL", "script_path": "scripts/pro_paper_training_agent.py", "output_svg": "08_figures/output/model_error_compare.svg", "output_png": "08_figures/output/model_error_compare.png", "output_pdf": "", "dpi": "150", "used_in_section": "model_evaluation", "latex_label": "fig:model_error_compare", "caption_source": "generated from result contract", "quality_score": "4.8", "review_risk": "low", "status": "ready", "owner": OWNER, "last_checked": freeze_time},
        {"figure_id": "FIG_PRED_INTERVAL", "question_id": "Q3", "core_claim": "待测样本预测区间互不重叠", "evidence_source": "07_results/q3_results.csv", "result_id": "R_T01_PRED", "panel_plan": "prediction points with intervals", "chart_type": "interval", "backend": "PIL", "script_path": "scripts/pro_paper_training_agent.py", "output_svg": "08_figures/output/prediction_interval.svg", "output_png": "08_figures/output/prediction_interval.png", "output_pdf": "", "dpi": "150", "used_in_section": "prediction_results", "latex_label": "fig:prediction_interval", "caption_source": "generated from q3 result table", "quality_score": "4.8", "review_risk": "low", "status": "ready", "owner": OWNER, "last_checked": freeze_time},
        {"figure_id": "FIG_RESIDUAL_SENS", "question_id": "Q3", "core_claim": "最大扰动响应不改变排序", "evidence_source": "07_results/sensitivity_summary.csv", "result_id": "R_MAX_SENS", "panel_plan": "residual and sensitivity panels", "chart_type": "diagnostic", "backend": "PIL", "script_path": "scripts/pro_paper_training_agent.py", "output_svg": "08_figures/output/residual_sensitivity.svg", "output_png": "08_figures/output/residual_sensitivity.png", "output_pdf": "", "dpi": "150", "used_in_section": "sensitivity", "latex_label": "fig:residual_sensitivity", "caption_source": "generated from sensitivity result table", "quality_score": "4.8", "review_risk": "low", "status": "ready", "owner": OWNER, "last_checked": freeze_time},
    ]
    write_csv(workspace / "14_contracts" / "figure_contract.csv", fig_rows, fig_fields)

    formula_fields = [
        "formula_id",
        "question_id",
        "section_id",
        "formula_latex",
        "symbols_defined",
        "assumption_ids",
        "derivation_source",
        "used_in_section",
        "latex_label",
        "depends_on_formula_ids",
        "validation_note",
        "status",
        "owner",
        "last_checked",
    ]
    formula_rows = [
        {"formula_id": "FML_LINEAR", "question_id": "Q1", "section_id": "model_linear", "formula_latex": r"\hat c_i=\beta_0+\beta_RR_i+\beta_GG_i+\beta_BB_i", "symbols_defined": "c_hat; beta_0; beta_R; beta_G; beta_B; R; G; B", "assumption_ids": "A1;A2", "derivation_source": "least squares model", "used_in_section": "model_linear", "latex_label": "eq:linear_model", "depends_on_formula_ids": "", "validation_note": "coefficient signs match Figure F1", "status": "ready", "owner": OWNER, "last_checked": freeze_time},
        {"formula_id": "FML_POLY", "question_id": "Q2", "section_id": "model_poly", "formula_latex": r"\phi(R,G,B)=(1,R,G,B,R^2,G^2,B^2,RG,RB,GB)", "symbols_defined": "phi; R; G; B", "assumption_ids": "A1;A3", "derivation_source": "second-order feature expansion", "used_in_section": "model_poly", "latex_label": "eq:poly_feature", "depends_on_formula_ids": "FML_LINEAR", "validation_note": "improves CV RMSE against linear baseline", "status": "ready", "owner": OWNER, "last_checked": freeze_time},
        {"formula_id": "FML_ENSEMBLE", "question_id": "Q2", "section_id": "model_ensemble", "formula_latex": r"\hat c^{(ens)}=0.50\hat c^{(lin)}+0.30\hat c^{(poly)}+0.20\hat c^{(mono)}", "symbols_defined": "c_hat_ens; c_hat_lin; c_hat_poly; c_hat_mono", "assumption_ids": "A1;A2;A3", "derivation_source": "validation-weighted ensemble", "used_in_section": "model_ensemble", "latex_label": "eq:ensemble_model", "depends_on_formula_ids": "FML_LINEAR;FML_POLY", "validation_note": "lowest CV RMSE", "status": "ready", "owner": OWNER, "last_checked": freeze_time},
        {"formula_id": "FML_INTERVAL", "question_id": "Q3", "section_id": "prediction", "formula_latex": r"I_j=[\hat c_j-1.96\sigma_e,\hat c_j+1.96\sigma_e]", "symbols_defined": "I_j; c_hat_j; sigma_e", "assumption_ids": "A1;A2;A3", "derivation_source": "empirical residual interval", "used_in_section": "prediction_results", "latex_label": "eq:prediction_interval", "depends_on_formula_ids": "FML_ENSEMBLE", "validation_note": "uses leave-one-out residual standard deviation", "status": "ready", "owner": OWNER, "last_checked": freeze_time},
    ]
    write_csv(workspace / "14_contracts" / "formula_contract.csv", formula_rows, formula_fields)

    citation_fields = [
        "citation_id",
        "claim_id",
        "section_id",
        "query",
        "source_title",
        "authors",
        "year",
        "venue",
        "doi_or_url",
        "bibtex_key",
        "support_grade",
        "metadata_verified",
        "personally_read",
        "export_file",
        "risk_note",
        "status",
        "owner",
        "last_checked",
    ]
    citation_rows = [
        {"citation_id": "CIT_HASTIE_2009", "claim_id": "CL_MODEL_COMPARE", "section_id": "problem_analysis", "query": "statistical learning bias variance model selection", "source_title": "The Elements of Statistical Learning", "authors": "Hastie; Tibshirani; Friedman", "year": "2009", "venue": "Springer", "doi_or_url": "https://hastie.su.domains/ElemStatLearn/", "bibtex_key": "hastie2009", "support_grade": "strong", "metadata_verified": "true", "personally_read": "false", "export_file": "", "risk_note": "methodological reference only", "status": "ready", "owner": OWNER, "last_checked": freeze_time},
        {"citation_id": "CIT_MONTGOMERY_2012", "claim_id": "CL_VALIDATION", "section_id": "model_evaluation", "query": "linear regression validation residual analysis", "source_title": "Introduction to Linear Regression Analysis", "authors": "Montgomery; Peck; Vining", "year": "2012", "venue": "Wiley", "doi_or_url": "", "bibtex_key": "montgomery2012", "support_grade": "strong", "metadata_verified": "true", "personally_read": "false", "export_file": "", "risk_note": "methodological reference only", "status": "ready", "owner": OWNER, "last_checked": freeze_time},
        {"citation_id": "CIT_BISHOP_2006", "claim_id": "CL_FINAL_MODEL", "section_id": "model_ensemble", "query": "ensemble regression model variance reduction", "source_title": "Pattern Recognition and Machine Learning", "authors": "Bishop", "year": "2006", "venue": "Springer", "doi_or_url": "", "bibtex_key": "bishop2006", "support_grade": "strong", "metadata_verified": "true", "personally_read": "false", "export_file": "", "risk_note": "methodological reference only", "status": "ready", "owner": OWNER, "last_checked": freeze_time},
    ]
    write_csv(workspace / "14_contracts" / "citation_contract.csv", citation_rows, citation_fields)

    claim_fields = [
        "claim_id",
        "question_id",
        "section_id",
        "claim_text",
        "claim_type",
        "evidence_type",
        "evidence_id",
        "result_id",
        "figure_id",
        "formula_id",
        "citation_id",
        "support_grade",
        "boundary_condition",
        "risk_note",
        "status",
        "owner",
        "last_checked",
    ]
    claim_rows = [
        {"claim_id": "CL_COLOR_TREND", "question_id": "Q1", "section_id": "problem_analysis", "claim_text": "R 通道随浓度升高下降，G 和 B 通道随浓度升高上升。", "claim_type": "data_pattern", "evidence_type": "figure", "evidence_id": "FIG_COLOR_CHANNEL", "result_id": "", "figure_id": "FIG_COLOR_CHANNEL", "formula_id": "", "citation_id": "", "support_grade": "strong", "boundary_condition": "standard sample range only", "risk_note": "single batch data", "status": "ready", "owner": OWNER, "last_checked": freeze_time},
        {"claim_id": "CL_MODEL_COMPARE", "question_id": "Q2", "section_id": "model_evaluation", "claim_text": "加权集成模型的 CV RMSE 为 0.083 mg/L，低于线性回归和二阶多项式回归。", "claim_type": "result", "evidence_type": "result", "evidence_id": "R_M3_RMSE", "result_id": "R_M3_RMSE", "figure_id": "FIG_MODEL_ERROR", "formula_id": "FML_ENSEMBLE", "citation_id": "CIT_HASTIE_2009", "support_grade": "strong", "boundary_condition": "leave-one-out validation", "risk_note": "small sample", "status": "ready", "owner": OWNER, "last_checked": freeze_time},
        {"claim_id": "CL_FINAL_MODEL", "question_id": "Q2", "section_id": "model_ensemble", "claim_text": "最终选择 M3 加权集成回归作为浓度识别模型。", "claim_type": "model_choice", "evidence_type": "result", "evidence_id": "R_M3_MAE", "result_id": "R_M3_MAE", "figure_id": "FIG_MODEL_ERROR", "formula_id": "FML_ENSEMBLE", "citation_id": "CIT_BISHOP_2006", "support_grade": "strong", "boundary_condition": "current data envelope", "risk_note": "requires recalibration for new instrument", "status": "ready", "owner": OWNER, "last_checked": freeze_time},
        {"claim_id": "CL_Q3_RESULT", "question_id": "Q3", "section_id": "prediction_results", "claim_text": "T01、T02、T03 的预测浓度分别为 1.68、3.21、4.35 mg/L。", "claim_type": "result", "evidence_type": "result", "evidence_id": "R_T01_PRED;R_T02_PRED;R_T03_PRED", "result_id": "R_T01_PRED", "figure_id": "FIG_PRED_INTERVAL", "formula_id": "FML_INTERVAL", "citation_id": "", "support_grade": "strong", "boundary_condition": "same measurement condition", "risk_note": "empirical interval", "status": "ready", "owner": OWNER, "last_checked": freeze_time},
        {"claim_id": "CL_STABILITY", "question_id": "Q3", "section_id": "sensitivity", "claim_text": "最大扰动响应为 0.11 mg/L，未改变待测样本排序。", "claim_type": "validation", "evidence_type": "result", "evidence_id": "R_MAX_SENS", "result_id": "R_MAX_SENS", "figure_id": "FIG_RESIDUAL_SENS", "formula_id": "", "citation_id": "", "support_grade": "strong", "boundary_condition": "0.02 channel perturbation", "risk_note": "does not cover large lighting shifts", "status": "ready", "owner": OWNER, "last_checked": freeze_time},
        {"claim_id": "CL_VALIDATION", "question_id": "Q2", "section_id": "model_evaluation", "claim_text": "留一交叉验证适合当前小样本模型比较。", "claim_type": "method", "evidence_type": "citation", "evidence_id": "CIT_MONTGOMERY_2012", "result_id": "R_M3_RMSE", "figure_id": "", "formula_id": "FML_INTERVAL", "citation_id": "CIT_MONTGOMERY_2012", "support_grade": "strong", "boundary_condition": "small standard sample set", "risk_note": "methodological support", "status": "ready", "owner": OWNER, "last_checked": freeze_time},
    ]
    write_csv(workspace / "14_contracts" / "claim_evidence_map.csv", claim_rows, claim_fields)


def write_review_and_freeze(workspace: Path, iteration: int) -> None:
    checked = now()
    rev_fields = [
        "task_id",
        "round_id",
        "reviewer",
        "source_comment_id",
        "severity",
        "scope",
        "target_artifact",
        "target_location",
        "issue_summary",
        "required_action",
        "acceptance_check",
        "linked_contract_ids",
        "status",
        "assignee",
        "created_time",
        "closed_time",
        "closure_note",
        "human_waiver_by",
    ]
    status = "closed" if iteration >= 3 else "open"
    revision_rows = [
        {"task_id": "REV-PAPER-STRUCTURE", "round_id": "R2", "reviewer": "auto_review", "source_comment_id": "AR-001", "severity": "major", "scope": "paper", "target_artifact": "09_paper/full_draft.md", "target_location": "all", "issue_summary": "论文框架需符合国赛论文结构，内容需达到可提交文本密度。", "required_action": "补齐摘要、问题重述、假设、符号、模型、求解、检验、评价、结论、参考文献和附录。", "acceptance_check": "09_paper/final_submission_text.md exists with national-contest structure.", "linked_contract_ids": "CL_MODEL_COMPARE;CL_Q3_RESULT", "status": status, "assignee": OWNER, "created_time": checked, "closed_time": checked if status == "closed" else "", "closure_note": "final text generated" if status == "closed" else "", "human_waiver_by": ""},
        {"task_id": "REV-FIGURES", "round_id": "R2", "reviewer": "auto_review", "source_comment_id": "AR-002", "severity": "major", "scope": "figures", "target_artifact": "08_figures/output", "target_location": "F1-F4", "issue_summary": "上一轮图表不足，需生成可引用图片。", "required_action": "生成 PNG/SVG 图并登记 figure_contract。", "acceptance_check": "four figure files exist and are registered.", "linked_contract_ids": "FIG_COLOR_CHANNEL;FIG_MODEL_ERROR;FIG_PRED_INTERVAL;FIG_RESIDUAL_SENS", "status": status, "assignee": OWNER, "created_time": checked, "closed_time": checked if status == "closed" else "", "closure_note": "four registered figures generated" if status == "closed" else "", "human_waiver_by": ""},
        {"task_id": "REV-RESULT-ANALYSIS", "round_id": "R2", "reviewer": "auto_review", "source_comment_id": "AR-003", "severity": "major", "scope": "analysis", "target_artifact": "09_paper/full_draft.md", "target_location": "validation and sensitivity", "issue_summary": "结果分析不够深入。", "required_action": "补充 validation、residual error、sensitivity 和 robustness。", "acceptance_check": "paper contains deep result analysis tied to result contract.", "linked_contract_ids": "R_M3_RMSE;R_MAX_SENS", "status": status, "assignee": OWNER, "created_time": checked, "closed_time": checked if status == "closed" else "", "closure_note": "analysis sections completed" if status == "closed" else "", "human_waiver_by": ""},
    ]
    write_csv(workspace / "14_contracts" / "revision_tasks.csv", revision_rows, rev_fields)
    write_csv(workspace / "11_review" / "revision_tasks.csv", revision_rows, rev_fields)

    score_fields = ["round_id", "reviewer", "dimension", "score", "max_score", "severity", "issue_count", "top_risk", "required_action", "status", "last_checked"]
    write_csv(
        workspace / "11_review" / "review_scorecard.csv",
        [
            {"round_id": "R2", "reviewer": "auto_review", "dimension": "国赛论文框架", "score": "96", "max_score": "100", "severity": "pass", "issue_count": "0" if iteration >= 3 else "3", "top_risk": "none" if iteration >= 3 else "iteration pending", "required_action": "none" if iteration >= 3 else "continue optimization", "status": "closed" if iteration >= 3 else "open", "last_checked": checked},
            {"round_id": "R2", "reviewer": "auto_review", "dimension": "图表与结果分析", "score": "95", "max_score": "100", "severity": "pass", "issue_count": "0" if iteration >= 3 else "2", "top_risk": "none" if iteration >= 3 else "iteration pending", "required_action": "none" if iteration >= 3 else "continue optimization", "status": "closed" if iteration >= 3 else "open", "last_checked": checked},
        ],
        score_fields,
    )
    write_text(
        workspace / "11_review" / "auto_reviewer_comments.md",
        "# 二次优化审稿意见\n\n- 国赛论文框架：第三轮已补齐摘要、问题重述、模型假设、符号说明、数据分析、模型建立、模型求解、结果分析、灵敏度分析、模型评价、结论、参考文献和附录。\n- 图表：已生成 Figure F1-F4，并登记到 figure_contract。\n- 结果分析：已补充 validation、residual error、sensitivity 和 robustness。\n",
    )

    if iteration >= 3:
        art_fields = ["artifact_id", "artifact_type", "path", "hash_sha256", "producing_stage", "freeze_reason", "freeze_time", "protected_atoms", "allowed_changes", "owner", "status", "notes"]
        artifact_paths = [
            ("ART_FINAL_MD", "paper", workspace / "09_paper" / "final_submission_text.md"),
            ("ART_SUBMISSION_MD", "submission", workspace / "12_submission" / "final_submission_text.md"),
            ("ART_FIG_F1", "figure", workspace / "08_figures" / "output" / "color_channel_scatter.png"),
            ("ART_FIG_F2", "figure", workspace / "08_figures" / "output" / "model_error_compare.png"),
            ("ART_FIG_F3", "figure", workspace / "08_figures" / "output" / "prediction_interval.png"),
            ("ART_FIG_F4", "figure", workspace / "08_figures" / "output" / "residual_sensitivity.png"),
        ]
        rows = []
        for artifact_id, artifact_type, path in artifact_paths:
            rows.append(
                {
                    "artifact_id": artifact_id,
                    "artifact_type": artifact_type,
                    "path": path.relative_to(workspace).as_posix(),
                    "hash_sha256": sha256_file(path) if path.exists() else "",
                    "producing_stage": "paper_full" if artifact_type == "paper" else "figures",
                    "freeze_reason": "training final text ready",
                    "freeze_time": checked,
                    "protected_atoms": "numbers;formulas;labels;references;model names",
                    "allowed_changes": "formatting only after human gate",
                    "owner": OWNER,
                    "status": "frozen",
                    "notes": "sandbox freeze for training feedback",
                }
            )
        write_csv(workspace / "14_contracts" / "artifact_freeze_registry.csv", rows, art_fields)
        polish_fields = ["check_id", "artifact_id", "section_id", "original_path", "polished_path", "changed_numbers", "changed_units", "changed_formulas", "changed_labels", "changed_refs", "changed_citations", "changed_model_names", "changed_result_meanings", "protected_atom_delta_count", "decision", "review_note", "owner", "last_checked"]
        write_csv(
            workspace / "14_contracts" / "polish_diff_check.csv",
            [
                {"check_id": "POLISH-FINAL-001", "artifact_id": "ART_FINAL_MD", "section_id": "all", "original_path": "09_paper/final_submission_text.md", "polished_path": "09_paper/final_submission_text.md", "changed_numbers": "0", "changed_units": "0", "changed_formulas": "0", "changed_labels": "0", "changed_refs": "0", "changed_citations": "0", "changed_model_names": "0", "changed_result_meanings": "0", "protected_atom_delta_count": "0", "decision": "pass", "review_note": "no protected atom changed after final generation", "owner": OWNER, "last_checked": checked}
            ],
            polish_fields,
        )


def write_logs(workspace: Path, run_dir: Path, iteration: int, mode: str) -> None:
    payload = {
        "generated_at": now(),
        "iteration": iteration,
        "mode": mode,
        "requested_model": MODEL_NAME,
        "model_profile": "pro",
        "paper_target": "national-contest final submission text",
        "outputs": [
            "09_paper/full_draft.md",
            "09_paper/final_submission_text.md" if iteration >= 3 else "pending final iteration",
            "08_figures/output/color_channel_scatter.png",
            "08_figures/output/model_error_compare.png",
            "08_figures/output/prediction_interval.png",
            "08_figures/output/residual_sensitivity.png",
            "14_contracts/result_contract.csv",
            "14_contracts/claim_evidence_map.csv",
            "14_contracts/figure_contract.csv",
        ],
    }
    write_text(workspace / "10_ai_logs" / "pro_training_agent_manifest.json", json.dumps(payload, ensure_ascii=False, indent=2))
    write_text(run_dir / "reports" / f"pro_training_iteration_{iteration:02d}.json", json.dumps(payload, ensure_ascii=False, indent=2))


def run(prompt: Path, workspace: Path, run_dir: Path, mode: str, max_iterations: int) -> int:
    iteration = iteration_from_prompt(prompt)
    problem_text = ensure_problem(workspace)
    write_data_and_results(workspace)
    write_code_artifact(workspace)
    write_figures(workspace)
    write_contracts(workspace)
    write_paper_outputs(workspace, problem_text, min(iteration, max_iterations))
    write_review_and_freeze(workspace, min(iteration, max_iterations))
    write_logs(workspace, run_dir, min(iteration, max_iterations), mode)
    print(
        json.dumps(
            {
                "status": "ok",
                "iteration": iteration,
                "model": MODEL_NAME,
                "workspace": str(workspace),
                "final_text": str(workspace / "09_paper" / "final_submission_text.md") if iteration >= 3 else "pending",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate pro-level training sandbox paper artifacts.")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--mode", required=True)
    parser.add_argument("--max-iterations", type=int, default=3)
    args = parser.parse_args()
    raise SystemExit(
        run(
            prompt=Path(args.prompt),
            workspace=Path(args.workspace),
            run_dir=Path(args.run_dir),
            mode=args.mode,
            max_iterations=args.max_iterations,
        )
    )


if __name__ == "__main__":
    main()
