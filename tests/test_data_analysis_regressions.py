from __future__ import annotations

import csv
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_eda_visuals():
    path = ROOT / "04_eda_code" / "eda_visuals.py"
    spec = importlib.util.spec_from_file_location("eda_visuals", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_template_inspector():
    path = ROOT / "04_eda_code" / "inspect_result_templates.py"
    spec = importlib.util.spec_from_file_location("inspect_result_templates", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DataAnalysisRegressionTests(unittest.TestCase):
    def test_q1_timing_rows_preserve_pdf_semantics_and_scope(self) -> None:
        path = ROOT / "03_data" / "input_decision_table.csv"
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = {row["input_id"]: row for row in csv.DictReader(handle)}

        self.assertEqual(rows["IN05"]["field_name"], "Q1投放时刻")
        self.assertEqual(rows["IN05"]["question"], "Q1")
        self.assertEqual(rows["IN05"]["decision"], "接令后1.5 s")
        self.assertEqual(rows["IN06"]["field_name"], "Q1投放至起爆间隔")
        self.assertEqual(rows["IN06"]["question"], "Q1")
        self.assertEqual(rows["IN06"]["decision"], "3.6 s")

    def test_duration_rule_allows_unused_bomb_slots_but_rejects_negative_duration(self) -> None:
        content = (ROOT / "03_data" / "cleaning_rules.md").read_text(encoding="utf-8")

        self.assertIn("已使用弹", content)
        self.assertIn("未使用弹", content)
        self.assertIn("负值", content)

    def test_empty_result_templates_are_not_correlation_ready(self) -> None:
        eda_visuals = load_eda_visuals()

        self.assertFalse(
            eda_visuals.has_correlation_ready_columns(
                {"烟幕干扰弹编号": 3, "投放点x": 0, "投放点y": 0}
            )
        )
        self.assertTrue(
            eda_visuals.has_correlation_ready_columns({"投放点x": 3, "投放点y": 3})
        )

    def test_template_inspector_finds_the_official_input_rows(self) -> None:
        inspector = load_template_inspector()

        result1 = inspector.inspect_workbook(ROOT / "03_data" / "raw" / "result1.xlsx")
        result2 = inspector.inspect_workbook(ROOT / "03_data" / "raw" / "result2.xlsx")
        result3 = inspector.inspect_workbook(ROOT / "03_data" / "raw" / "result3.xlsx")

        self.assertEqual(result1["data_rows"], [2, 3, 4])
        self.assertEqual(result2["data_rows"], [2, 3, 4])
        self.assertEqual(result3["data_rows"], list(range(2, 17)))
        self.assertFalse(result1["has_formulas"])
        self.assertFalse(result2["is_protected"])
        self.assertEqual(result3["headers"][-1], "干扰的导弹编号")

    def test_eda_pipeline_uses_v4_local_inspector_not_removed_v3_controller(self) -> None:
        source = (ROOT / "04_eda_code" / "run_eda_pipeline.py").read_text(encoding="utf-8")

        self.assertNotIn("workflow_utils", source)
        self.assertNotIn("complete_stage", source)
        self.assertIn("inspect_result_templates", source)


if __name__ == "__main__":
    unittest.main()
