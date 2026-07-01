"""NetworkX graph template for relation, route, and propagation diagrams.

Expected edge list columns:
    source, target, weight(optional)
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC", "Microsoft YaHei", "SimHei", "PingFang SC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False
import networkx as nx


def draw_weighted_network(edges: pd.DataFrame, output_stem: str, title: str = "Network structure"):
    required = {"source", "target"}
    if not required.issubset(edges.columns):
        raise ValueError(f"Edges must contain columns: {required}")
    graph = nx.from_pandas_edgelist(edges, "source", "target", edge_attr=True, create_using=nx.Graph())
    weights = [graph[u][v].get("weight", 1.0) for u, v in graph.edges()]
    pos = nx.spring_layout(graph, seed=42, weight="weight")
    fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=150)
    nx.draw_networkx_nodes(graph, pos, node_size=520, node_color="#3288BD", alpha=0.9, ax=ax)
    nx.draw_networkx_edges(graph, pos, width=[0.8 + float(w) for w in weights], alpha=0.45, edge_color="#666666", ax=ax)
    nx.draw_networkx_labels(graph, pos, font_size=9, font_color="white", ax=ax)
    ax.set_title(title, pad=12)
    ax.axis("off")
    Path(output_stem).parent.mkdir(parents=True, exist_ok=True)
    for suffix in ["png", "svg", "pdf"]:
        fig.savefig(f"{output_stem}.{suffix}", bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    sample = pd.DataFrame({"source": ["A", "A", "B"], "target": ["B", "C", "D"], "weight": [1.0, 2.0, 1.5]})
    draw_weighted_network(sample, "../export/png_300dpi/sample_network")
