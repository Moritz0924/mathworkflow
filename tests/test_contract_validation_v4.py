from __future__ import annotations

import csv
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


class ContractValidationV4Tests(unittest.TestCase):
    def test_current_pending_stage_does_not_require_its_future_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            workspace = Path(raw)
            write_policy(workspace)
            state = default_state("demo")
            state.update(
                {
                    "current_stage": "model_design",
                    "status": "pending_chatgpt",
                    "completed_stages": ["intake", "data_analysis"],
                }
            )
            write_state(workspace, state)

            policy = yaml.safe_load((ROOT / "config" / "contract_policy.yaml").read_text(encoding="utf-8"))
            target = workspace / "config" / "contract_policy.yaml"
            target.write_text(yaml.safe_dump(policy, allow_unicode=True, sort_keys=False), encoding="utf-8")
            for source in (ROOT / "14_contracts").glob("*.csv"):
                relative = source.relative_to(ROOT)
                path = workspace / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                with source.open("r", encoding="utf-8-sig", newline="") as handle:
                    header = next(csv.reader(handle))
                with path.open("w", encoding="utf-8-sig", newline="") as handle:
                    csv.writer(handle).writerow(header)

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "validate_contracts.py"),
                    "--root",
                    str(workspace),
                    "--stage",
                    "current",
                ],
                cwd=str(ROOT),
                text=True,
                capture_output=True,
                check=False,
            )
            report = json.loads((workspace / "11_review" / "contract_validation_report.json").read_text(encoding="utf-8"))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual("model_design", report["stage"])
            self.assertEqual(0, report["fail_count"])


if __name__ == "__main__":
    unittest.main()
