from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = ROOT / "06_code"
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))


class FrozenEvidenceDataTests(unittest.TestCase):
    def test_build_evidence_data_preserves_q3_q4_zero_contributions(self) -> None:
        from generate_evidence import build_evidence_data

        evidence = build_evidence_data(ROOT)

        self.assertEqual([2.2381643772125575, 0.0, 0.0], [row["duration_s"] for row in evidence["q3_contributions"]])
        self.assertEqual([2.2381643772125575, 0.0, 0.0], [row["duration_s"] for row in evidence["q4_contributions"]])
        self.assertTrue(all(row["result_status"] == "frozen" for row in evidence["metrics"]))

    def test_generation_writes_zero_contribution_figures_and_tables(self) -> None:
        from generate_evidence import generate_artifacts

        with self.subTest("generated artifacts retain Q3/Q4 evidence"):
            import tempfile

            with tempfile.TemporaryDirectory() as raw:
                output_root = Path(raw)
                artifacts = generate_artifacts(ROOT, output_root=output_root)

                self.assertTrue((output_root / "tables" / "T4_q3_contributions.csv").exists())
                self.assertTrue((output_root / "main_figures" / "F4_q3_bomb_intervals.png").exists())
                self.assertTrue((output_root / "main_figures" / "F5_q4_uav_intervals.png").exists())
                self.assertIn("F004", {item["figure_id"] for item in artifacts})

    def test_contract_rows_reference_existing_results_and_generated_files(self) -> None:
        from generate_evidence import build_contract_rows, generate_artifacts

        import tempfile

        with tempfile.TemporaryDirectory() as raw:
            output_root = Path(raw)
            artifacts = generate_artifacts(ROOT, output_root=output_root)
            rows = build_contract_rows(ROOT, artifacts)

            figure_ids = {row["figure_id"] for row in rows["figures"]}
            self.assertEqual({f"F{index:03d}" for index in range(1, 12)}, figure_ids)
            self.assertTrue(all(row["result_id"].startswith("RES-") for row in rows["figures"]))
            self.assertTrue(all(Path(row["output_png"]).exists() for row in rows["figures"]))
            self.assertTrue({"F004", "F005", "F006"}.issubset({row["figure_id"] for row in rows["claims"]}))

    def test_a08_sensitivity_figure_has_one_legend_item_per_compared_object(self) -> None:
        from generate_evidence import generate_artifacts

        import tempfile

        with tempfile.TemporaryDirectory() as raw:
            output_root = Path(raw)
            generate_artifacts(ROOT, output_root=output_root)
            svg = (output_root / "main_figures" / "F10_a08_sensitivity.svg").read_text(encoding="utf-8")

            self.assertNotIn("Q1/M1，Q2/M1", svg)
            for label in ("Q1/M1", "Q2/M1", "Q5/M1", "Q5/M2", "Q5/M3"):
                self.assertIn(f"<!-- {label} -->", svg)
            self.assertIn("stroke-dasharray", svg)
            self.assertIn("Q2/M1 与 Q5/M1", svg)

    def test_3d_scene_figures_label_the_target_at_full_coordinate_scale(self) -> None:
        from generate_evidence import generate_artifacts

        import tempfile

        with tempfile.TemporaryDirectory() as raw:
            output_root = Path(raw)
            generate_artifacts(ROOT, output_root=output_root)
            for name in ("F1_initial_3d_scene", "F2_q1_trajectory"):
                svg = (output_root / "main_figures" / f"{name}.svg").read_text(encoding="utf-8")
                self.assertIn("<!-- 假目标 -->", svg)
                self.assertIn("<!-- 真目标（圆柱） -->", svg)
            self.assertIn('id="legend_1"', (output_root / "main_figures" / "F1_initial_3d_scene.svg").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
