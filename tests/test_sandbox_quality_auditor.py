from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))

from test_training_quality_acceptance import make_minimal_run, write_csv  # noqa: E402


class SandboxQualityAuditorTests(unittest.TestCase):
    def test_quality_auditor_writes_snapshot_verdict_scorecard_and_tasks(self) -> None:
        from sandbox_quality_auditor import run_quality_audit

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_minimal_run(Path(tmp))
            payload = run_quality_audit(run_dir, target_tier="training_draft")
            workspace = run_dir / "workspace"

            verdict_path = workspace / "11_review" / "quality_verdict.json"
            scorecard_path = workspace / "11_review" / "quality_scorecard.csv"
            findings_path = workspace / "11_review" / "quality_findings.csv"
            tasks_path = workspace / "14_contracts" / "quality_revision_tasks.csv"

            verdict = json.loads(verdict_path.read_text(encoding="utf-8"))
            scorecard_exists = scorecard_path.exists()
            findings_exists = findings_path.exists()
            tasks_exists = tasks_path.exists()
            snapshot_manifest_exists = (run_dir / "audit_snapshot" / "snapshot_manifest.json").exists()

        self.assertEqual(payload["status"], "pass")
        self.assertIn(verdict["recommended_decision"], {"training_draft", "submission_candidate", "excellent_training_sample"})
        self.assertGreaterEqual(verdict["total_score"], 75)
        self.assertTrue(verdict["snapshot_id"].startswith("AUDIT-"))
        self.assertTrue(scorecard_exists)
        self.assertTrue(findings_exists)
        self.assertTrue(tasks_exists)
        self.assertTrue(snapshot_manifest_exists)

    def test_quality_auditor_flags_duplicate_and_untraceable_figures(self) -> None:
        from sandbox_quality_auditor import run_quality_audit

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_minimal_run(Path(tmp))
            workspace = run_dir / "workspace"
            write_csv(
                workspace / "14_contracts" / "figure_contract.csv",
                [
                    {
                        "figure_id": "F001",
                        "title": "重复图 1",
                        "result_id": "",
                        "evidence_source": "",
                        "output_svg": "08_figures/output/F001.svg",
                        "output_png": "",
                        "output_pdf": "",
                        "used_in_section": "结果分析",
                        "latex_label": "fig:f001",
                        "quality_score": "4.8",
                        "status": "ready",
                        "owner": "agent",
                        "notes": "",
                    },
                    {
                        "figure_id": "F001",
                        "title": "重复图 2",
                        "result_id": "",
                        "evidence_source": "",
                        "output_svg": "08_figures/output/F001.svg",
                        "output_png": "",
                        "output_pdf": "",
                        "used_in_section": "结果分析",
                        "latex_label": "fig:f001-dup",
                        "quality_score": "4.8",
                        "status": "ready",
                        "owner": "agent",
                        "notes": "",
                    },
                ],
                [
                    "figure_id",
                    "title",
                    "result_id",
                    "evidence_source",
                    "output_svg",
                    "output_png",
                    "output_pdf",
                    "used_in_section",
                    "latex_label",
                    "quality_score",
                    "status",
                    "owner",
                    "notes",
                ],
            )
            payload = run_quality_audit(run_dir, target_tier="training_draft")
            with (workspace / "11_review" / "quality_findings.csv").open("r", encoding="utf-8-sig", newline="") as f:
                rows = list(csv.DictReader(f))

        self.assertEqual(payload["status"], "fail")
        items = {row["finding_id"] for row in rows}
        self.assertIn("QF-FIG-DUPLICATE-ID", items)
        self.assertIn("QF-FIG-MISSING-EVIDENCE", items)

    def test_quality_auditor_does_not_overstate_tier_when_higher_thresholds_are_missing(self) -> None:
        from sandbox_quality_auditor import run_quality_audit

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_minimal_run(Path(tmp))
            payload = run_quality_audit(run_dir, target_tier="training_draft")

        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["recommended_decision"], "training_draft")
        self.assertEqual(payload["quality_tier"], "training_draft")


if __name__ == "__main__":
    unittest.main()
