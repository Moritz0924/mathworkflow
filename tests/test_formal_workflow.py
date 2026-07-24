from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import yaml

from mmwf.config import read_policy
from mmwf.context import build_context_manifest
from mmwf.errors import WorkflowError
from mmwf.handoff import import_chatgpt_response, prepare_handoff, record_codex_verification
from mmwf.migration import migrate_v32
from mmwf.state import confirm_gate, default_state, read_state, write_state


STAGES = [
    "intake",
    "data_analysis",
    "model_design",
    "implementation",
    "result_freeze",
    "evidence_design",
    "paper_review",
    "finalize",
]


def write_policy(root: Path) -> None:
    config = root / "config"
    config.mkdir(parents=True, exist_ok=True)
    policy = {
        "version": "v4",
        "protocol": "mmwf-handoff/v1",
        "stages": STAGES,
        "gates": {
            "model_design": "model_freeze_gate",
            "result_freeze": "result_freeze_gate",
            "evidence_design": "evidence_gate",
            "paper_review": "paper_gate",
            "finalize": "final_submission_gate",
        },
        "stage_contracts": {
            "intake": {"context_paths": ["00_problem"], "required_artifacts": ["00_problem/problem_statement.md"]},
            "data_analysis": {
                "context_paths": ["00_problem", "01_task_analysis", "03_data", "04_eda"],
                "required_artifacts": ["03_data/data_quality_report.md"],
            },
            "model_design": {"context_paths": ["00_problem", "03_data", "05_model"], "required_artifacts": ["05_model/model_route.md"]},
            "implementation": {"context_paths": ["05_model", "06_code"], "required_artifacts": ["06_code/run_all.py"]},
            "result_freeze": {"context_paths": ["06_code", "07_results", "14_contracts"], "required_artifacts": ["07_results/result.csv"]},
            "evidence_design": {"context_paths": ["07_results", "08_figures", "14_contracts"], "required_artifacts": ["08_figures/figure.png"]},
            "paper_review": {"context_paths": ["08_figures", "09_paper", "14_contracts"], "required_artifacts": ["09_paper/full_draft.md"]},
            "finalize": {"context_paths": ["09_paper", "12_submission", "14_contracts"], "required_artifacts": ["12_submission/final_paper.pdf"]},
        },
    }
    (config / "formal_workflow.yaml").write_text(yaml.safe_dump(policy, allow_unicode=True, sort_keys=False), encoding="utf-8")


def write_prompt_templates(root: Path) -> None:
    for stage in STAGES:
        stage_dir = root / "prompts" / "formal_v4" / stage
        stage_dir.mkdir(parents=True, exist_ok=True)
        (stage_dir / "chatgpt.md").write_text(f"# {stage}\n\nProduce the accepted stage outcome.\n", encoding="utf-8")
        (stage_dir / "codex.md").write_text(f"# {stage}\n\nVerify the accepted stage outcome.\n", encoding="utf-8")


class FormalWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        write_policy(self.root)
        write_prompt_templates(self.root)
        (self.root / "00_problem").mkdir()
        (self.root / "00_problem" / "problem_statement.md").write_text("demo problem", encoding="utf-8")
        write_state(self.root, default_state("demo"))

    def tearDown(self) -> None:
        self.temp.cleanup()

    def prepare_and_import(self, stage: str = "intake", handoff_id: str = "H001") -> None:
        state = read_state(self.root)
        state["current_stage"] = stage
        state["status"] = "pending_chatgpt"
        state["completed_stages"] = STAGES[: STAGES.index(stage)]
        write_state(self.root, state)
        manifest = prepare_handoff(self.root, "chatgpt", handoff_id=handoff_id)
        response = self.root / "response.md"
        response.write_text(
            "---\n"
            "protocol: mmwf-handoff/v1\n"
            "project_id: demo\n"
            f"stage: {stage}\n"
            f"handoff_id: {handoff_id}\n"
            f"context_sha256: {manifest['context_sha256']}\n"
            "---\n\nAccepted proposal.\n",
            encoding="utf-8",
        )
        import_chatgpt_response(self.root, handoff_id, response)

    def test_default_state_uses_eight_stage_protocol(self) -> None:
        state = default_state("demo")
        self.assertEqual("v4", state["version"])
        self.assertEqual("intake", state["current_stage"])
        self.assertEqual("pending_chatgpt", state["status"])
        self.assertEqual([], state["completed_stages"])

    def test_policy_cannot_reorder_stages_or_remove_a_human_gate(self) -> None:
        policy_path = self.root / "config" / "formal_workflow.yaml"
        original = yaml.safe_load(policy_path.read_text(encoding="utf-8"))

        reordered = dict(original)
        reordered["stages"] = list(reversed(STAGES))
        policy_path.write_text(yaml.safe_dump(reordered), encoding="utf-8")
        with self.assertRaisesRegex(WorkflowError, "fixed eight-stage order"):
            read_policy(self.root)

        missing_gate = dict(original)
        missing_gate["gates"] = dict(original["gates"])
        missing_gate["gates"].pop("model_design")
        policy_path.write_text(yaml.safe_dump(missing_gate), encoding="utf-8")
        with self.assertRaisesRegex(WorkflowError, "fixed five human gates"):
            read_policy(self.root)

    def test_gate_cannot_be_confirmed_without_exact_pending_gate(self) -> None:
        with self.assertRaisesRegex(WorkflowError, "no pending human gate"):
            confirm_gate(self.root, "model_freeze_gate")

    def test_state_rejects_skipped_or_out_of_order_completed_stages(self) -> None:
        state = default_state("demo")
        state["current_stage"] = "model_design"
        state["completed_stages"] = ["data_analysis", "intake"]
        with self.assertRaisesRegex(WorkflowError, "completed_stages"):
            write_state(self.root, state)

    def test_context_manifest_excludes_secrets_hidden_files_and_large_files(self) -> None:
        (self.root / "00_problem" / "safe.csv").write_text("a,b\n1,2\n", encoding="utf-8")
        (self.root / "00_problem" / ".env").write_text("API_KEY=do-not-export", encoding="utf-8")
        (self.root / "00_problem" / ".hidden.txt").write_text("hidden", encoding="utf-8")
        (self.root / "00_problem" / "private.key").write_text("secret", encoding="utf-8")
        (self.root / "00_problem" / "large.bin").write_bytes(b"x" * 128)
        (self.root / "00_problem" / "secret.txt").write_text(
            "API_KEY=abcdefghijklmnopqrstuvwxyz123456", encoding="utf-8"
        )
        (self.root / "00_problem" / "risk-notes.md").write_text(
            "risk-driven-validation-boundary", encoding="utf-8"
        )

        manifest = build_context_manifest(self.root, ["00_problem"], max_file_bytes=64)
        included = {item["path"] for item in manifest["files"]}
        excluded = {item["path"] for item in manifest["excluded"]}

        self.assertIn("00_problem/safe.csv", included)
        self.assertIn("00_problem/problem_statement.md", included)
        self.assertIn("00_problem/risk-notes.md", included)
        self.assertIn("00_problem/.env", excluded)
        self.assertIn("00_problem/.hidden.txt", excluded)
        self.assertIn("00_problem/private.key", excluded)
        self.assertIn("00_problem/large.bin", excluded)
        self.assertIn("00_problem/secret.txt", excluded)

    def test_import_rejects_stale_hash_and_replay(self) -> None:
        manifest = prepare_handoff(self.root, "chatgpt", handoff_id="H002")
        response = self.root / "bad-response.md"
        response.write_text(
            "---\nprotocol: mmwf-handoff/v1\nproject_id: demo\nstage: intake\n"
            "handoff_id: H002\ncontext_sha256: stale\n---\n\nproposal\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(WorkflowError, "context_sha256"):
            import_chatgpt_response(self.root, "H002", response)

        response.write_text(response.read_text(encoding="utf-8").replace("stale", manifest["context_sha256"]), encoding="utf-8")
        import_chatgpt_response(self.root, "H002", response)
        with self.assertRaisesRegex(WorkflowError, "already imported"):
            import_chatgpt_response(self.root, "H002", response)

    def test_handoff_id_cannot_escape_handoff_directory(self) -> None:
        with self.assertRaisesRegex(WorkflowError, "invalid handoff_id"):
            prepare_handoff(self.root, "chatgpt", handoff_id="../escape")
        self.assertFalse((self.root / "10_ai_logs" / "escape").exists())

    def test_codex_conflict_returns_same_stage_to_chatgpt(self) -> None:
        self.prepare_and_import()
        report = {
            "verdict": "needs_revision",
            "checks": [{"id": "reproduce", "status": "fail", "evidence": "result differs"}],
            "artifacts": [],
            "contract_rows": [],
            "conflicts": [{"type": "model_assumption", "summary": "unsupported", "evidence": "data", "owner": "chatgpt"}],
            "next_action": "revise model proposal",
        }

        record_codex_verification(self.root, "H001", report)
        state = read_state(self.root)
        self.assertEqual("intake", state["current_stage"])
        self.assertEqual("pending_chatgpt", state["status"])
        self.assertIsNone(state["active_handoff_id"])

    def test_pass_verdict_cannot_hide_failed_checks_or_conflicts(self) -> None:
        self.prepare_and_import(handoff_id="H-CONFLICT")
        inconsistent = {
            "verdict": "pass",
            "checks": [{"id": "reproduce", "status": "fail", "evidence": "mismatch"}],
            "artifacts": [],
            "contract_rows": [],
            "conflicts": [{"type": "model_assumption", "summary": "conflict"}],
            "next_action": "advance",
        }
        with self.assertRaisesRegex(WorkflowError, "pass verdict"):
            record_codex_verification(self.root, "H-CONFLICT", inconsistent)
        state = read_state(self.root)
        self.assertEqual("pending_codex", state["status"])
        self.assertFalse((self.root / "10_ai_logs" / "handoffs" / "H-CONFLICT" / "codex_receipt.json").exists())

    def test_blocked_stage_can_start_a_new_chatgpt_revision(self) -> None:
        self.prepare_and_import(handoff_id="H-BLOCKED")
        record_codex_verification(
            self.root,
            "H-BLOCKED",
            {
                "verdict": "blocked",
                "checks": [{"id": "input", "status": "fail", "evidence": "missing clarification"}],
                "artifacts": [],
                "contract_rows": [],
                "conflicts": [],
                "next_action": "obtain clarification and retry",
            },
        )
        self.assertEqual("blocked", read_state(self.root)["status"])

        manifest = prepare_handoff(self.root, "chatgpt", handoff_id="H-RETRY")
        state = read_state(self.root)
        self.assertEqual("pending_chatgpt", state["status"])
        self.assertEqual("H-RETRY", state["active_handoff_id"])
        self.assertEqual(2, manifest["revision"])

    def test_pass_advances_non_gate_stage_and_waits_at_gate_stage(self) -> None:
        self.prepare_and_import()
        passed = {
            "verdict": "pass",
            "checks": [{"id": "files", "status": "pass", "evidence": "00_problem/problem_statement.md"}],
            "artifacts": [{"path": "00_problem/problem_statement.md", "role": "input"}],
            "contract_rows": [],
            "conflicts": [],
            "next_action": "advance",
        }
        record_codex_verification(self.root, "H001", passed)
        state = read_state(self.root)
        self.assertEqual("data_analysis", state["current_stage"])
        self.assertEqual("pending_chatgpt", state["status"])
        self.assertEqual(["intake"], state["completed_stages"])

        (self.root / "05_model").mkdir()
        (self.root / "05_model" / "model_route.md").write_text("approved model", encoding="utf-8")
        self.prepare_and_import("model_design", "H003")
        record_codex_verification(self.root, "H003", passed)
        state = read_state(self.root)
        self.assertEqual("model_design", state["current_stage"])
        self.assertEqual("pending_human", state["status"])
        self.assertEqual("model_freeze_gate", state["pending_gate"])


class MigrationTests(unittest.TestCase):
    def test_v32_model_route_maps_to_validated_model_design_pending(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            write_policy(root)
            old_state = {
                "version": "v3.2-mvp",
                "current_stage": "model_route",
                "completed_stages": ["latex_template", "intake", "eda", "task_analysis", "prior_retrieval"],
            }
            (root / "workflow_state.yaml").write_text(yaml.safe_dump(old_state), encoding="utf-8")
            required = {
                "00_problem/problem_statement.md": "problem",
                "03_data/data_quality_report.md": "quality",
            }
            for relative, text in required.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")

            result = migrate_v32(root, project_id="current-competition")

            self.assertEqual("model_design", result["current_stage"])
            self.assertEqual("pending_chatgpt", result["status"])
            self.assertEqual(["intake", "data_analysis"], result["completed_stages"])
            self.assertTrue((root / "workflow_state.v3.2.yaml").exists())


if __name__ == "__main__":
    unittest.main()
