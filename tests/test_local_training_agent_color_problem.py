from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import local_training_agent as agent  # noqa: E402
from validate_agent_run import topic_alignment_issue  # noqa: E402


COLOR_PROBLEM = """# Color and material concentration recognition

Known standard samples provide normalized `R`, `G`, `B` readings and
`concentration_mg_L`. Predict the material concentration for test samples
`T01`, `T02`, and `T03` from color channels only.

| sample_id | concentration_mg_L | R | G | B |
|---|---:|---:|---:|---:|
| S01 | 0.5 | 0.91 | 0.23 | 0.18 |
| S02 | 1.0 | 0.85 | 0.29 | 0.21 |
| S03 | 1.5 | 0.79 | 0.35 | 0.26 |
| S04 | 2.0 | 0.72 | 0.42 | 0.31 |
| S05 | 2.5 | 0.66 | 0.49 | 0.37 |
| S06 | 3.0 | 0.60 | 0.55 | 0.43 |
| S07 | 3.5 | 0.54 | 0.61 | 0.50 |
| S08 | 4.0 | 0.49 | 0.67 | 0.57 |
| S09 | 4.5 | 0.43 | 0.72 | 0.63 |
| S10 | 5.0 | 0.39 | 0.76 | 0.69 |

| sample_id | R | G | B |
|---|---:|---:|---:|
| T01 | 0.77 | 0.37 | 0.28 |
| T02 | 0.58 | 0.57 | 0.46 |
| T03 | 0.45 | 0.70 | 0.61 |
"""


class LocalTrainingAgentColorProblemTests(unittest.TestCase):
    def test_color_problem_generates_aligned_paper_and_figure_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            run_dir = root / "run"
            (workspace / "00_problem").mkdir(parents=True)
            (run_dir / "reports").mkdir(parents=True)
            (workspace / "00_problem" / "problem_statement.md").write_text(COLOR_PROBLEM, encoding="utf-8")

            self.assertEqual(agent.topic_kind(COLOR_PROBLEM), "color_concentration")

            for stage in agent.STAGES:
                agent.run_stage(stage, run_dir, workspace, COLOR_PROBLEM, 1, f"test_{stage}", "")

            paper = (workspace / "12_submission" / "final_submit_paper.md").read_text(encoding="utf-8")
            self.assertEqual(topic_alignment_issue(COLOR_PROBLEM, paper), "")
            self.assertIn("T01", paper)
            self.assertIn("T02", paper)
            self.assertIn("T03", paper)
            self.assertIn("concentration", paper.lower())
            self.assertIn("RGB", paper)
            self.assertIn("训练验收条件与通过记录", paper)

            with (workspace / "14_contracts" / "figure_contract.csv").open("r", encoding="utf-8-sig", newline="") as f:
                figure_rows = list(csv.DictReader(f))

            self.assertGreaterEqual(len({row["figure_id"] for row in figure_rows}), 8)
            self.assertTrue(all(row.get("script_path") for row in figure_rows))
            self.assertTrue(all(row.get("execution_log") for row in figure_rows))
            self.assertTrue(all((workspace / row["script_path"]).exists() for row in figure_rows))
            self.assertTrue(all((workspace / row["execution_log"]).exists() for row in figure_rows))


if __name__ == "__main__":
    unittest.main()
