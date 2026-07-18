from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from mmwf.dashboard import DashboardService
from mmwf.errors import WorkflowError
from tests.test_formal_workflow import write_policy, write_prompt_templates


ROOT = Path(__file__).resolve().parents[1]


class DashboardServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp.name)
        write_policy(self.workspace)
        write_prompt_templates(self.workspace)
        (self.workspace / "00_problem").mkdir()
        (self.workspace / "00_problem" / "problem_statement.md").write_text("demo", encoding="utf-8")
        self.service = DashboardService(self.workspace, ROOT / "scripts" / "workflow.py")
        self.service.run_cli(["init", "--project-id", "demo"])

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_prepare_and_list_handoffs_use_cli_results(self) -> None:
        payload = self.service.prepare({"target": "chatgpt", "handoff_id": "H-WEB"})
        self.assertEqual("H-WEB", payload["handoff_id"])
        rows = self.service.list_handoffs()
        self.assertEqual(1, len(rows))
        self.assertEqual("awaiting_chatgpt", rows[0]["status"])

    def test_training_sandbox_action_is_not_supported(self) -> None:
        with self.assertRaisesRegex(WorkflowError, "unsupported dashboard action"):
            self.service.dispatch("sandbox_start", {})

    def test_gate_check_is_available_through_dashboard_service(self) -> None:
        result = self.service.dispatch("check_gates", {})
        self.assertEqual(0, result["fail_count"])


if __name__ == "__main__":
    unittest.main()
