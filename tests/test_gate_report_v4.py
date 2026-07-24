from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

from mmwf.state import default_state, write_state
from tests.test_formal_workflow import write_policy


ROOT = Path(__file__).resolve().parents[1]


class GateReportTests(unittest.TestCase):
    def run_check(self, workspace: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check_gates.py"), "--root", str(workspace), "--json"],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=False,
        )

    def test_valid_v4_state_passes_gate_invariant_check(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            workspace = Path(raw)
            write_policy(workspace)
            write_state(workspace, default_state("demo"))
            result = self.run_check(workspace)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual(0, json.loads(result.stdout)["fail_count"])

    def test_pending_human_without_gate_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            workspace = Path(raw)
            write_policy(workspace)
            invalid = default_state("demo")
            invalid["status"] = "pending_human"
            (workspace / "workflow_state.yaml").write_text(yaml.safe_dump(invalid), encoding="utf-8")
            result = self.run_check(workspace)
            self.assertEqual(1, result.returncode)
            self.assertGreater(json.loads(result.stdout)["fail_count"], 0)


if __name__ == "__main__":
    unittest.main()
