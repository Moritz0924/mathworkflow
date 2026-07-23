from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def resolve_executable(name: str, fallback: Path) -> Path:
    if fallback.exists():
        return fallback
    discovered = shutil.which(name)
    if discovered:
        return Path(discovered)
    raise FileNotFoundError(f"Required executable not found: {name}")


def run_checked(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if completed.returncode != 0:
        output = (completed.stdout + "\n" + completed.stderr)[-12_000:]
        raise RuntimeError(f"Command failed ({completed.returncode}): {' '.join(command)}\n{output}")
    return completed


def parse_pages(pdfinfo: Path, pdf: Path) -> int:
    completed = run_checked([str(pdfinfo), str(pdf)], cwd=pdf.parent)
    match = re.search(r"^Pages:\s+(\d+)$", completed.stdout, flags=re.MULTILINE)
    if not match:
        raise RuntimeError(f"Unable to read page count from pdfinfo output:\n{completed.stdout}")
    return int(match.group(1))


def build(root: Path) -> dict[str, object]:
    paper_root = root / "09_paper"
    source = paper_root / "final_submission.tex"
    bibliography = paper_root / "final_references.bib"
    figure_root = root / "08_figures" / "final_figures"
    build_root = root / "tmp" / "latex" / "final_paper"
    output_pdf = root / "12_submission" / "final_paper.pdf"
    report_path = root / "11_review" / "final_paper_build.json"

    required_figures = [
        "PF001_model_chain.pdf",
        "PF002_scene_los.pdf",
        "PF003_q1_q2_comparison.pdf",
        "PF004_q3_q4_contribution.pdf",
        "PF005_q5_assignment.pdf",
        "PF006_q5_intervals.pdf",
        "PF007_convergence_stability.pdf",
        "PF008_sensitivity.pdf",
    ]
    missing = [name for name in required_figures if not (figure_root / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing formal figures: {missing}")
    if not source.exists() or not bibliography.exists():
        raise FileNotFoundError("The XeLaTeX source and bibliography must exist before compilation.")

    build_root.mkdir(parents=True, exist_ok=True)
    for name in (
        "final_submission.aux",
        "final_submission.bbl",
        "final_submission.blg",
        "final_submission.log",
        "final_submission.out",
        "final_submission.pdf",
        "final_submission.toc",
        "final_submission.tex",
        "final_references.bib",
    ):
        target = build_root / name
        if target.exists():
            target.unlink()
    shutil.copy2(source, build_root / source.name)
    shutil.copy2(bibliography, build_root / bibliography.name)

    miktex_root = Path("C:/Users/admin/AppData/Local/Programs/MiKTeX/miktex/bin/x64")
    xelatex = resolve_executable("xelatex", miktex_root / "xelatex.exe")
    bibtex = resolve_executable("bibtex", miktex_root / "bibtex.exe")
    pdfinfo = resolve_executable(
        "pdfinfo",
        Path.home()
        / ".cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdfinfo.exe",
    )

    latex_command = [str(xelatex), "-interaction=nonstopmode", "-halt-on-error", "final_submission.tex"]
    run_checked(latex_command, build_root)
    run_checked([str(bibtex), "final_submission"], build_root)
    run_checked(latex_command, build_root)
    run_checked(latex_command, build_root)

    built_pdf = build_root / "final_submission.pdf"
    log_path = build_root / "final_submission.log"
    if not built_pdf.exists() or not log_path.exists():
        raise RuntimeError("XeLaTeX completed without the expected PDF/log outputs.")
    log = log_path.read_text(encoding="utf-8", errors="replace")
    forbidden_markers = [
        "LaTeX Warning: There were undefined references",
        "LaTeX Warning: Label(s) may have changed",
        "Citation `",
        "Missing character:",
        "! LaTeX Error:",
        "Overfull \\hbox",
        "fancyhdr Warning: \\headheight is too small",
    ]
    found_markers = [marker for marker in forbidden_markers if marker in log]
    if found_markers:
        raise RuntimeError(f"Final XeLaTeX log still contains blocking markers: {found_markers}")

    pages = parse_pages(pdfinfo, built_pdf)
    if not 10 <= pages <= 14:
        raise RuntimeError(f"Final paper has {pages} pages; expected 10--14.")

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(built_pdf, output_pdf)
    report = {
        "status": "pass",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(source.relative_to(root)).replace("\\", "/"),
        "output": str(output_pdf.relative_to(root)).replace("\\", "/"),
        "pages": pages,
        "figures": 8,
        "figure_formats": ["pdf", "svg", "png"],
        "latex_log": str(log_path.relative_to(root)).replace("\\", "/"),
        "blocking_log_markers": found_markers,
        "human_gate": "final_submission_gate remains pending human confirmation",
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile and verify the final XeLaTeX contest paper.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    build(args.root.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
