from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def safe_read_csv(path):
    path = ROOT / path
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def main():
    gates = safe_read_csv("11_dashboard/gate_status.csv")
    risks = safe_read_csv("11_dashboard/risk_board.csv")
    figs = safe_read_csv("08_figures/figure_design_review.csv")
    ai = safe_read_csv("10_ai_logs/ai_anchor_map.csv")
    cites = safe_read_csv("02_literature/citation_anchor_map.csv")
    print("=== Math Modeling Workflow v2.3 Dashboard ===")
    print(f"Gates: {len(gates)}")
    print(f"Risks: {len(risks)}")
    print(f"Figure reviews: {len(figs)}")
    print(f"AI anchors: {len(ai)}")
    print(f"Citation anchors: {len(cites)}")


if __name__ == "__main__":
    main()
