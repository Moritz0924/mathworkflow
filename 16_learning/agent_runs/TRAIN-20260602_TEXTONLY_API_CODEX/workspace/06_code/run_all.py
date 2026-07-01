from pathlib import Path
from datetime import datetime
import pandas as pd

ROOT = Path(__file__).resolve().parents[0].parent
RESULT_DIR = ROOT / "07_results"
RESULT_DIR.mkdir(exist_ok=True)


def write_placeholder_results():
    for q in ["q1", "q2", "q3"]:
        df = pd.DataFrame([
            {"question": q.upper(), "metric": "placeholder", "value": "", "source": "manual_or_model_output"}
        ])
        df.to_csv(RESULT_DIR / f"{q}_results.csv", index=False, encoding="utf-8-sig")

    pd.DataFrame([
        {"metric_id": "M001", "question": "Q1", "metric_name": "", "value": "", "unit": "", "source_file": ""}
    ]).to_csv(RESULT_DIR / "metrics_summary.csv", index=False, encoding="utf-8-sig")

    pd.DataFrame([
        {"result_id": "R001", "question": "Q1", "result_file": "07_results/q1_results.csv", "generated_by": "run_all.py", "timestamp": datetime.now().isoformat(), "verified": False}
    ]).to_csv(RESULT_DIR / "result_source_map.csv", index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    write_placeholder_results()
    print("[OK] placeholder result files written to 07_results/")
