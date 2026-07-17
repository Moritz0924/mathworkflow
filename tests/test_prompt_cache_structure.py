from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


class PromptCacheStructureTests(unittest.TestCase):
    def test_training_system_prompt_is_stable_across_stage_and_gate(self) -> None:
        from deepseek_agent_runner import build_system_prompt

        first = build_system_prompt("training_sandbox", "paper_full", "draft_review_gate")
        second = build_system_prompt("training_sandbox", "figures", "figure_gate")

        self.assertEqual(first, second)
        self.assertNotIn("paper_full", first)
        self.assertNotIn("draft_review_gate", first)

    def test_user_prompt_places_stable_prefix_before_run_delta(self) -> None:
        from deepseek_agent_runner import build_user_prompt

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            (workspace / "prompts" / "training_sandbox" / "stages").mkdir(parents=True)
            (workspace / "config").mkdir()
            (workspace / "AGENTS.md").write_text("stable repo rule", encoding="utf-8")
            (workspace / "workflow_state.yaml").write_text("current_stage: paper_full\npending_gate: gate_a\n", encoding="utf-8")
            (workspace / "prompts" / "training_sandbox" / "stages" / "10_paper_full.md").write_text("stage delta text", encoding="utf-8")
            prompt = workspace / "agent_stage_prompt.md"
            prompt.write_text("controller task text", encoding="utf-8")

            text, meta = build_user_prompt(workspace, prompt, "paper_full", [], mode="training_sandbox")

        self.assertLess(text.index("# Stable System Prefix"), text.index("# Stage Delta"))
        self.assertLess(text.index("# Stage Delta"), text.index("# Run Delta"))
        self.assertGreater(meta["stable_prefix_chars"], 0)
        self.assertGreater(meta["run_delta_chars"], 0)
        self.assertIn("stable_prefix_sha256", meta)
        self.assertIn("Current stage: `paper_full`", text)
        self.assertIn("Pending gate: `gate_a`", text)

    def test_training_agent_cannot_write_quality_auditor_outputs(self) -> None:
        from deepseek_agent_runner import is_write_allowed, load_yaml

        policy = load_yaml(ROOT / "config" / "llm_router_policy.yaml")
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            target = workspace / "11_review" / "quality_verdict.json"
            allowed, reason = is_write_allowed(target, workspace, "training_sandbox", "final_export", policy)

        self.assertFalse(allowed)
        self.assertIn("quality auditor", reason)


if __name__ == "__main__":
    unittest.main()
