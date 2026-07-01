"""Publication-style matplotlib templates for math modeling papers.

Expected CSV format for grouped bar:
    group, category, value
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC", "Microsoft YaHei", "SimHei", "PingFang SC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

PALETTE = {
    "primary": "#2F5597",
    "secondary": "#ED7D31",
    "neutral": "#A6A6A6",
    "background": "#FFFFFF",
}


def apply_publication_style():
    plt.rcParams.update({
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "font.size": 10,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "legend.fontsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linewidth": 0.8,
    })


def grouped_bar(data: pd.DataFrame, title: str, x_label: str, y_label: str, output_stem: str):
    required = {"group", "category", "value"}
    if not required.issubset(data.columns):
        raise ValueError(f"Data must contain columns: {required}")
    apply_publication_style()
    pivot = data.pivot(index="group", columns="category", values="value")
    ax = pivot.plot(kind="bar", figsize=(8, 4.8), width=0.78)
    ax.set_title(title, pad=12)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend(frameon=False, ncol=min(3, len(pivot.columns)))
    ax.tick_params(axis="x", rotation=0)
    max_value = data["value"].max()
    ax.axhline(max_value, linewidth=1, linestyle="--", alpha=0.35)
    ax.annotate("best", xy=(0.98, max_value), xycoords=("axes fraction", "data"),
                ha="right", va="bottom", fontsize=9)
    Path(output_stem).parent.mkdir(parents=True, exist_ok=True)
    for suffix in ["png", "svg", "pdf"]:
        plt.savefig(f"{output_stem}.{suffix}", bbox_inches="tight", facecolor="white")
    plt.close()


if __name__ == "__main__":
    sample = pd.DataFrame({
        "group": ["Q1", "Q1", "Q2", "Q2"],
        "category": ["baseline", "main", "baseline", "main"],
        "value": [0.72, 0.86, 0.65, 0.81],
    })
    grouped_bar(sample, "Model comparison", "Question", "Score", "../export/png_300dpi/sample_grouped_bar")
