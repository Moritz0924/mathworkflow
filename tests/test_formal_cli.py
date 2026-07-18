from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path

from mmwf.cli import main
from mmwf.state import read_state
from tests.test_formal_workflow import write_policy, write_prompt_templates


class FormalCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        write_policy(self.root)
        write_prompt_templates(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_cli(self, *args: str) -> tuple[int, dict]:
        output = io.StringIO()
        code = main(list(args), root=self.root, output=output)
        return code, json.loads(output.getvalue())

    def test_init_status_and_prepare_chatgpt(self) -> None:
        (self.root / "00_problem").mkdir()
        (self.root / "00_problem" / "problem_statement.md").write_text("demo", encoding="utf-8")

        code, initialized = self.run_cli("init", "--project-id", "demo")
        self.assertEqual(0, code)
        self.assertEqual("demo", initialized["project_id"])

        code, status = self.run_cli("status")
        self.assertEqual(0, code)
        self.assertEqual("pending_chatgpt", status["status"])

        code, handoff = self.run_cli("prepare", "--target", "chatgpt", "--handoff-id", "H-CLI")
        self.assertEqual(0, code)
        self.assertEqual("H-CLI", handoff["handoff_id"])
        self.assertTrue((self.root / "10_ai_logs" / "handoffs" / "H-CLI" / "chatgpt_prompt.md").exists())

    def test_cli_import_prepare_codex_and_verify_blocked(self) -> None:
        (self.root / "00_problem").mkdir()
        (self.root / "00_problem" / "problem_statement.md").write_text("demo", encoding="utf-8")
        self.run_cli("init", "--project-id", "demo")
        _, handoff = self.run_cli("prepare", "--target", "chatgpt", "--handoff-id", "H-ROUND")
        response = self.root / "response.md"
        response.write_text(
            "---\nprotocol: mmwf-handoff/v1\nproject_id: demo\nstage: intake\n"
            f"handoff_id: H-ROUND\ncontext_sha256: {handoff['context_sha256']}\n---\n\nproposal\n",
            encoding="utf-8",
        )
        code, _ = self.run_cli("import", "--handoff-id", "H-ROUND", "--response", str(response))
        self.assertEqual(0, code)
        code, _ = self.run_cli("prepare", "--target", "codex", "--handoff-id", "H-ROUND")
        self.assertEqual(0, code)

        report = self.root / "report.json"
        report.write_text(
            json.dumps(
                {
                    "verdict": "blocked",
                    "checks": [],
                    "artifacts": [],
                    "contract_rows": [],
                    "conflicts": [{"type": "data", "summary": "missing", "evidence": "none", "owner": "human"}],
                    "next_action": "supply data",
                }
            ),
            encoding="utf-8",
        )
        code, receipt = self.run_cli("verify", "--handoff-id", "H-ROUND", "--report", str(report))
        self.assertEqual(0, code)
        self.assertEqual("blocked", receipt["verdict"])
        self.assertEqual("blocked", read_state(self.root)["status"])


if __name__ == "__main__":
    unittest.main()
