"""Geopandas map template.

This template is optional. It requires geopandas and a valid geometry column.
"""
from pathlib import Path
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC", "Microsoft YaHei", "SimHei", "PingFang SC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False


def choropleth_map(gdf, value_col: str, output_stem: str, title: str = "Spatial distribution"):
    if value_col not in gdf.columns:
        raise ValueError(f"{value_col} not found in GeoDataFrame.")
    fig, ax = plt.subplots(figsize=(7.5, 6), dpi=150)
    gdf.plot(column=value_col, ax=ax, cmap="YlGnBu", legend=True,
             edgecolor="white", linewidth=0.4)
    ax.set_title(title, pad=12)
    ax.axis("off")
    Path(output_stem).parent.mkdir(parents=True, exist_ok=True)
    for suffix in ["png", "svg", "pdf"]:
        fig.savefig(f"{output_stem}.{suffix}", bbox_inches="tight", facecolor="white")
    plt.close(fig)
