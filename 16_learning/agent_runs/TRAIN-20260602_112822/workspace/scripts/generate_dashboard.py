from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "11_dashboard/progress_snapshot.md"


def count_files(folder):
    p = ROOT / folder
    return len([x for x in p.rglob("*") if x.is_file() and x.name != ".gitkeep"])


def main():
    lines = [
        "# 进度快照",
        "",
        f"生成时间：{datetime.now().isoformat(timespec='seconds')}",
        "",
        "| 模块 | 文件数 |",
        "|---|---:|",
    ]
    for folder in ["00_problem", "01_task_analysis", "02_literature", "03_data", "05_model", "07_results", "08_figures", "09_paper", "10_ai_logs", "11_dashboard"]:
        lines.append(f"| {folder} | {count_files(folder)} |")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
