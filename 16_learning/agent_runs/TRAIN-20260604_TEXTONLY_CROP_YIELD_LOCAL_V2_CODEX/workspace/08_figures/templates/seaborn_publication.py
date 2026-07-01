"""Seaborn-based templates for correlation heatmaps and distribution diagnostics."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def correlation_heatmap(data: pd.DataFrame, output_stem: str, title: str = "Correlation heatmap"):
    numeric = data.select_dtypes(include="number")
    if numeric.empty:
        raise ValueError("No numeric columns available for correlation heatmap.")
    corr = numeric.corr()
    plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 300, "font.size": 10})
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, ax=ax, cmap="vlag", center=0, square=True, linewidths=0.4,
                cbar_kws={"shrink": 0.78}, annot=False)
    ax.set_title(title, pad=12)
    Path(output_stem).parent.mkdir(parents=True, exist_ok=True)
    for suffix in ["png", "svg", "pdf"]:
        fig.savefig(f"{output_stem}.{suffix}", bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [4, 3, 2, 1], "c": [1, 3, 2, 5]})
    correlation_heatmap(df, "../export/png_300dpi/sample_heatmap")
