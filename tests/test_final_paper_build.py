from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = ROOT / "06_code"
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))
FIGURE_IDS = {f"PF{index:03d}" for index in range(1, 9)}
BLUEPRINT_COLUMNS = [
    "figure_id",
    "question_id",
    "core_claim",
    "result_id/evidence_source",
    "chart_type",
    "panel_plan",
    "used_in_section",
    "latex_label",
    "review_risk",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def pdfinfo_path() -> Path:
    bundled = (
        Path.home()
        / ".cache"
        / "codex-runtimes"
        / "codex-primary-runtime"
        / "dependencies"
        / "native"
        / "poppler"
        / "Library"
        / "bin"
        / "pdfinfo.exe"
    )
    if bundled.exists():
        return bundled
    discovered = shutil.which("pdfinfo")
    if discovered:
        return Path(discovered)
    raise AssertionError("pdfinfo is required to verify the final PDF")


class FinalFigureContractTests(unittest.TestCase):
    def test_panel_label_supports_three_dimensional_axes(self) -> None:
        import matplotlib.pyplot as plt

        from build_final_figures import panel_label

        figure = plt.figure()
        axis = figure.add_subplot(111, projection="3d")
        try:
            panel_label(axis, "(a)")
        finally:
            plt.close(figure)

    def test_scene_los_figure_can_be_rendered(self) -> None:
        import matplotlib.pyplot as plt

        from build_final_figures import configure_style, draw_pf002

        configure_style()
        figure = draw_pf002()
        try:
            figure.canvas.draw()
        finally:
            plt.close(figure)

    def test_blueprint_has_exact_required_schema_and_eight_distinct_figures(self) -> None:
        blueprint = ROOT / "08_figures" / "final_figure_blueprint.csv"
        rows = read_csv(blueprint)

        with blueprint.open("r", encoding="utf-8-sig", newline="") as handle:
            self.assertEqual(BLUEPRINT_COLUMNS, next(csv.reader(handle)))
        self.assertEqual(FIGURE_IDS, {row["figure_id"] for row in rows})
        self.assertEqual(8, len(rows))
        for row in rows:
            self.assertTrue(row["core_claim"].strip())
            self.assertTrue(row["result_id/evidence_source"].strip())
            self.assertTrue(row["review_risk"].strip())
            self.assertTrue(row["latex_label"].startswith("fig:"))

    def test_every_formal_figure_has_three_exports_and_passes_quality_gate(self) -> None:
        rows = read_csv(ROOT / "08_figures" / "final_figure_quality.csv")
        self.assertEqual(FIGURE_IDS, {row["figure_id"] for row in rows})

        for row in rows:
            self.assertGreaterEqual(float(row["quality_score"]), 4.2)
            self.assertEqual("ready", row["status"])
            stem = row["file_stem"]
            for extension in ("png", "svg", "pdf"):
                artifact = ROOT / "08_figures" / "final_figures" / f"{stem}.{extension}"
                self.assertTrue(artifact.exists(), artifact)
                self.assertGreater(artifact.stat().st_size, 2_000, artifact)


class FinalModelValidationTests(unittest.TestCase):
    def test_model_validation_passes_all_checks_and_preserves_frozen_metrics(self) -> None:
        report_path = ROOT / "11_review" / "final_model_validation.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))

        self.assertEqual("pass", report["status"])
        self.assertTrue(report["checks"])
        self.assertTrue(all(item["status"] == "pass" for item in report["checks"]))
        expected = {
            "Q1/primary_duration_M1": 1.3622014999389869,
            "Q2/primary_duration_M1": 2.2381643772125575,
            "Q5/objective_total_duration": 6.097008562088021,
            "Q5/objective_minimum_duration": 1.8768008708953303,
        }
        for key, value in expected.items():
            self.assertAlmostEqual(value, report["headline_metrics"][key], places=10)


class FinalPaperArtifactTests(unittest.TestCase):
    def test_executable_resolver_prefers_a_verified_fallback(self) -> None:
        from build_final_paper import resolve_executable

        with tempfile.TemporaryDirectory() as raw:
            fallback = Path(raw) / "pdfinfo.exe"
            fallback.touch()
            with patch("build_final_paper.shutil.which", return_value="C:/broken/pdfinfo.cmd"):
                self.assertEqual(fallback, resolve_executable("pdfinfo", fallback))

    def test_tex_is_contest_facing_and_contains_figures_formulas_and_references(self) -> None:
        tex_path = ROOT / "09_paper" / "final_submission.tex"
        tex = tex_path.read_text(encoding="utf-8")

        for forbidden in ("引用合同登记", "修订任务", "审稿回复", "证据合同审计"):
            self.assertNotIn(forbidden, tex)
        self.assertGreaterEqual(tex.count("\\includegraphics"), 8)
        self.assertGreaterEqual(tex.count("\\begin{equation}"), 8)
        self.assertIn("\\bibliography{final_references}", tex)
        for index in range(1, 9):
            self.assertIn(f"fig:pf{index:03d}", tex.lower())

    def test_tex_defines_the_registered_tau_vector_macro(self) -> None:
        tex = (ROOT / "09_paper" / "final_submission.tex").read_text(encoding="utf-8")
        self.assertIn("\\Tau", tex)
        self.assertIn("\\newcommand{\\Tau}{\\boldsymbol{\\tau}}", tex)

    def test_final_pdf_has_expected_page_count_and_clean_latex_log(self) -> None:
        pdf = ROOT / "12_submission" / "final_paper.pdf"
        self.assertTrue(pdf.exists())
        self.assertGreater(pdf.stat().st_size, 300_000)

        completed = subprocess.run(
            [str(pdfinfo_path()), str(pdf)],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        match = re.search(r"^Pages:\s+(\d+)$", completed.stdout, flags=re.MULTILINE)
        self.assertIsNotNone(match, completed.stdout)
        self.assertGreaterEqual(int(match.group(1)), 10)
        self.assertLessEqual(int(match.group(1)), 14)

        log = (ROOT / "tmp" / "latex" / "final_paper" / "final_submission.log").read_text(
            encoding="utf-8", errors="replace"
        )
        for marker in (
            "LaTeX Warning: There were undefined references",
            "LaTeX Warning: Label(s) may have changed",
            "Missing character:",
            "Overfull \\hbox",
            "fancyhdr Warning: \\headheight is too small",
        ):
            self.assertNotIn(marker, log)


if __name__ == "__main__":
    unittest.main()
