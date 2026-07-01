"""Plotly interactive figure template.

Use HTML for exploration and export a static image for the final paper when kaleido is installed.
"""
from pathlib import Path
import pandas as pd
import plotly.express as px


def interactive_scatter(data: pd.DataFrame, x: str, y: str, color: str | None, output_html: str, title: str):
    if x not in data.columns or y not in data.columns:
        raise ValueError("x and y columns must exist in data.")
    fig = px.scatter(data, x=x, y=y, color=color, title=title, template="plotly_white")
    fig.update_traces(marker={"size": 9, "opacity": 0.82})
    fig.update_layout(legend_title_text=color or "")
    output = Path(output_html)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(output)
    return fig


if __name__ == "__main__":
    df = pd.DataFrame({"x": [1, 2, 3], "y": [2, 5, 4], "group": ["A", "B", "A"]})
    interactive_scatter(df, "x", "y", "group", "../export/sample_interactive.html", "Interactive result view")
