from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

import yaml

from mmwf.errors import WorkflowError
from mmwf.legacy import verify_legacy_prompts


ROOT = Path(__file__).resolve().parents[1]
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


class LegacyPromptProtectionTests(unittest.TestCase):
    def test_repository_legacy_prompts_match_frozen_hash_manifest(self) -> None:
        result = verify_legacy_prompts(ROOT)
        self.assertEqual(17, result["verified_files"])
        self.assertEqual([], result["changed"])

    def test_changed_legacy_prompt_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            path = root / "prompts" / "stages" / "00_demo.md"
            path.parent.mkdir(parents=True)
            path.write_text("original", encoding="utf-8")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            config = root / "config"
            config.mkdir()
            (config / "legacy_prompt_hashes.yaml").write_text(
                yaml.safe_dump({"version": "v1", "files": {"prompts/stages/00_demo.md": digest}}, sort_keys=False),
                encoding="utf-8",
            )
            path.write_text("changed", encoding="utf-8")
            with self.assertRaisesRegex(WorkflowError, "legacy prompt protection failed"):
                verify_legacy_prompts(root)


class ActivePromptContractTests(unittest.TestCase):
    def test_all_new_prompts_are_result_contracts_without_scaffold_language(self) -> None:
        banned = ["chain of thought", "step-by-step reasoning", "你是一位", "你是一个"]
        required = ["结果", "边界", "交付", "验收", "阻塞"]
        for stage in STAGES:
            for target in ["chatgpt", "codex"]:
                path = ROOT / "prompts" / "formal_v4" / stage / f"{target}.md"
                self.assertTrue(path.exists(), path)
                text = path.read_text(encoding="utf-8")
                for word in required:
                    self.assertIn(word, text, f"{path} missing {word}")
                lowered = text.lower()
                for phrase in banned:
                    self.assertNotIn(phrase.lower(), lowered, f"{path} contains scaffold phrase {phrase}")


if __name__ == "__main__":
    unittest.main()
