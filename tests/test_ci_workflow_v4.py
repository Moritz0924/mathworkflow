from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CiWorkflowTests(unittest.TestCase):
    def test_pytest_runs_through_repository_python(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "formal-workflow.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn("- run: python -m pytest -q", workflow)
        self.assertIsNone(
            re.search(r"(?m)^\s*-\s+run:\s+pytest\s+-q\s*$", workflow),
            "The pytest console entry point may omit the repository root from sys.path.",
        )


if __name__ == "__main__":
    unittest.main()
