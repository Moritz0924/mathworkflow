"""Advanced publication-style Chinese plotting helpers for math modeling papers.

All functions deliberately avoid default Matplotlib colors and set Chinese font fallbacks.
"""
from pathlib import Path
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

PALETTES = {
    "muted_blue_gold": ["#2F5597", "#D8A31A", "#5B8C5A", "#7A7A7A", "#C06C54"],
    "teal_orange_diverging": ["#2166AC", "#F7F7F7", "#B2182B"],
    "deep_blue_vermilion": ["#264653", "#E76F51", "#2A9D8F", "#8D99AE"],
}


def apply_chinese_publication_style(font_size: int = 10):
    plt.rcParams.update({
        "figure.dpi": 160,
        "savefig.dpi": 320,
        "font.size": font_size,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "legend.fontsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "font.sans-serif": ["Noto Sans CJK SC", "Microsoft YaHei", "SimHei", "PingFang SC", "Arial Unicode MS"],
        "axes.unicode_minus": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.18,
        "grid.linewidth": 0.8,
    })


def save_all(fig, output_stem: str):
    Path(output_stem).parent.mkdir(parents=True, exist_ok=True)
    for suffix in ["png", "svg", "pdf"]:
        fig.savefig(f"{output_stem}.{suffix}", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def slope_rank_chart(data: pd.DataFrame, item: str, stage: str, value: str, output_stem: str, title: str, y_label: str = "指标值"):
    required = {item, stage, value}
    if not required.issubset(data.columns):
        raise ValueError(f"数据必须包含列：{required}")
    apply_chinese_publication_style()
    stages = list(dict.fromkeys(data[stage].tolist()))
    if len(stages) != 2:
        raise ValueError("坡度图需要且只需要两个阶段")
    pivot = data.pivot(index=item, columns=stage, values=value).dropna()
    colors = PALETTES["muted_blue_gold"]
    fig, ax = plt.subplots(figsize=(7.2, max(4.2, 0.34 * len(pivot))))
    x = [0, 1]
    for name, row in pivot.iterrows():
        y = [row[stages[0]], row[stages[1]]]
        ax.plot(x, y, color=colors[0], alpha=0.45, linewidth=1.8)
        ax.scatter(x, y, color=[colors[0], colors[1]], s=42, zorder=3)
        ax.text(-0.04, y[0], str(name), va="center", ha="right", fontsize=9)
        ax.text(1.04, y[1], str(name), va="center", ha="left", fontsize=9)
    ax.set_xlim(-0.35, 1.35)
    ax.set_xticks(x, stages)
    ax.set_ylabel(y_label)
    ax.set_title(title, pad=12, fontweight="bold")
    save_all(fig, output_stem)


def annotated_heatmap(data: pd.DataFrame, output_stem: str, title: str, x_label: str = "指标", y_label: str = "对象"):
    numeric = data.select_dtypes(include="number")
    if numeric.empty:
        raise ValueError("没有可用于热力图的数值列")
    apply_chinese_publication_style()
    arr = numeric.to_numpy(dtype=float)
    cmap = LinearSegmentedColormap.from_list("teal_orange_diverging", PALETTES["teal_orange_diverging"])
    fig, ax = plt.subplots(figsize=(max(6.5, 0.45 * numeric.shape[1]), max(4.8, 0.28 * numeric.shape[0])))
    im = ax.imshow(arr, aspect="auto", cmap=cmap)
    ax.set_xticks(range(numeric.shape[1]), numeric.columns, rotation=35, ha="right")
    ax.set_yticks(range(numeric.shape[0]), data.index.astype(str))
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title, pad=12, fontweight="bold")
    cb = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
    cb.ax.tick_params(labelsize=8)
    # Annotate only strong cells to keep the figure clean.
    finite = arr[np.isfinite(arr)]
    if finite.size:
        lo, hi = np.nanpercentile(finite, [10, 90])
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                v = arr[i, j]
                if np.isfinite(v) and (v <= lo or v >= hi):
                    ax.text(j, i, f"{v:.2g}", ha="center", va="center", fontsize=8, color="#222222")
    save_all(fig, output_stem)


def pareto_front(data: pd.DataFrame, x: str, y: str, output_stem: str, title: str, label: str | None = None):
    required = {x, y}
    if not required.issubset(data.columns):
        raise ValueError(f"数据必须包含列：{required}")
    apply_chinese_publication_style()
    colors = PALETTES["deep_blue_vermilion"]
    df = data.sort_values(x)
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    ax.scatter(df[x], df[y], s=62, color=colors[0], alpha=0.78, edgecolor="white", linewidth=0.7)
    ax.plot(df[x], df[y].cummin() if df[y].iloc[-1] < df[y].iloc[0] else df[y].cummax(), color=colors[1], linewidth=2.2, label="前沿趋势")
    if label and label in df.columns:
        for _, row in df.iterrows():
            ax.annotate(str(row[label]), (row[x], row[y]), xytext=(4, 4), textcoords="offset points", fontsize=8)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title, pad=12, fontweight="bold")
    ax.legend(frameon=False)
    save_all(fig, output_stem)


def residual_diagnostics(data: pd.DataFrame, y_true: str, y_pred: str, output_stem: str, title: str = "残差诊断"):
    required = {y_true, y_pred}
    if not required.issubset(data.columns):
        raise ValueError(f"数据必须包含列：{required}")
    apply_chinese_publication_style()
    df = data.copy()
    df["残差"] = df[y_true] - df[y_pred]
    colors = PALETTES["deep_blue_vermilion"]
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.scatter(df[y_pred], df["残差"], s=42, color=colors[2], alpha=0.72, edgecolor="white", linewidth=0.6)
    ax.axhline(0, color=colors[1], linewidth=1.8, linestyle="--", label="零残差")
    ax.set_xlabel("预测值")
    ax.set_ylabel("残差")
    ax.set_title(title, pad=12, fontweight="bold")
    ax.legend(frameon=False)
    save_all(fig, output_stem)


if __name__ == "__main__":
    demo = pd.DataFrame({"对象": ["甲", "乙", "丙"], "阶段": ["前", "前", "前"], "指标": [0.3, 0.5, 0.4]})
