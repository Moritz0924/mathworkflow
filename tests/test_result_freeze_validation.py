from __future__ import annotations

import sys
import unittest
from pathlib import Path


CODE_ROOT = Path(__file__).resolve().parents[1] / "06_code"
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))


class Q5AssignmentSensitivityTests(unittest.TestCase):
    def test_fairness_first_can_choose_a_different_positive_assignment(self) -> None:
        from src.result_freeze import select_q5_assignment

        scores = {
            ("U1", "M1"): 20.0,
            ("U1", "M2"): 19.0,
            ("U1", "M3"): 2.0,
            ("U2", "M1"): 19.0,
            ("U2", "M2"): 20.0,
            ("U2", "M3"): 2.0,
            ("U3", "M1"): 2.0,
            ("U3", "M2"): 2.0,
            ("U3", "M3"): 1.0,
        }

        total_first = select_q5_assignment(scores, ("U1", "U2", "U3"), ("M1", "M2", "M3"))
        fair_first = select_q5_assignment(
            scores,
            ("U1", "U2", "U3"),
            ("M1", "M2", "M3"),
            priority="min_then_total",
        )

        self.assertEqual((41.0, 1.0), total_first["objective"])
        self.assertEqual((24.0, 2.0), fair_first["objective"])
        self.assertNotEqual(total_first["assignment"], fair_first["assignment"])

    def test_positive_coverage_requirement_can_exclude_an_assignment(self) -> None:
        from src.result_freeze import select_q5_assignment

        scores = {
            ("U1", "M1"): 2.0,
            ("U1", "M2"): 0.0,
            ("U1", "M3"): 0.0,
            ("U2", "M1"): 0.0,
            ("U2", "M2"): 2.0,
            ("U2", "M3"): 0.0,
            ("U3", "M1"): 0.0,
            ("U3", "M2"): 0.0,
            ("U3", "M3"): 0.0,
        }

        self.assertIsNone(select_q5_assignment(scores, ("U1", "U2", "U3"), ("M1", "M2", "M3")))
        relaxed = select_q5_assignment(
            scores,
            ("U1", "U2", "U3"),
            ("M1", "M2", "M3"),
            require_positive=False,
        )

        self.assertEqual((4.0, 0.0), relaxed["objective"])


class IndependentRecomputationTests(unittest.TestCase):
    def test_recomputation_reports_union_duration_and_constraint_status(self) -> None:
        from src.entities import BombPlan
        from src.evaluator import EvaluatorConfig, evaluate_plan
        from src.result_freeze import independently_evaluate_plans

        plan = BombPlan("FY1", 1, "M1", True, 3.141592653589793, 120.0, 1.5, 3.6)
        config = EvaluatorConfig(angular_samples=6, height_samples=2, radial_samples=1, scan_step_s=0.25)
        expected = evaluate_plan(plan, "M1", config).effective_duration_s

        recomputed = independently_evaluate_plans("Q1", (plan,), config)

        self.assertEqual([], recomputed["constraint_issues"])
        self.assertAlmostEqual(expected, recomputed["primary_durations_s"]["M1"], places=8)
        self.assertEqual(1, len(recomputed["evaluations"]))


class StabilitySummaryTests(unittest.TestCase):
    def test_stability_is_grouped_by_question_and_metric(self) -> None:
        from run_result_freeze_validation import metric_stability

        rows = [
            {"scenario": "seed_a", "question_id": "Q1", "metric_name": "duration", "metric_value_s": "1.00"},
            {"scenario": "seed_b", "question_id": "Q1", "metric_name": "duration", "metric_value_s": "1.02"},
            {"scenario": "seed_a", "question_id": "Q5", "metric_name": "objective", "metric_value_s": "6.00"},
            {"scenario": "seed_b", "question_id": "Q5", "metric_name": "objective", "metric_value_s": "6.00"},
        ]

        summary = metric_stability(rows, {"seed_a", "seed_b"})

        self.assertAlmostEqual(0.02, summary["by_metric"]["Q1/duration"])
        self.assertEqual(0.0, summary["by_metric"]["Q5/objective"])
        self.assertAlmostEqual(0.02, summary["maximum_span_s"])


if __name__ == "__main__":
    unittest.main()
