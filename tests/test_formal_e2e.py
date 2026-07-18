from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from mmwf.handoff import import_chatgpt_response, prepare_handoff, record_codex_verification
from mmwf.state import confirm_gate, default_state, read_state, write_state
from tests.test_formal_workflow import STAGES, write_policy, write_prompt_templates


class FormalWorkflowEndToEndTests(unittest.TestCase):
    def test_all_eight_stages_complete_without_external_model_calls(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            write_policy(root)
            write_prompt_templates(root)
            write_state(root, default_state("simulation"))

            artifacts = {
                "intake": "00_problem/problem_statement.md",
                "data_analysis": "03_data/data_quality_report.md",
                "model_design": "05_model/model_route.md",
                "implementation": "06_code/run_all.py",
                "result_freeze": "07_results/result.csv",
                "evidence_design": "08_figures/figure.png",
                "paper_review": "09_paper/full_draft.md",
                "finalize": "12_submission/final_paper.pdf",
            }
            gates = {
                "model_design": "model_freeze_gate",
                "result_freeze": "result_freeze_gate",
                "evidence_design": "evidence_gate",
                "paper_review": "paper_gate",
                "finalize": "final_submission_gate",
            }

            for index, stage in enumerate(STAGES, start=1):
                state = read_state(root)
                self.assertEqual(stage, state["current_stage"])
                self.assertEqual("pending_chatgpt", state["status"])

                handoff_id = f"E2E-{index:02d}"
                manifest = prepare_handoff(root, "chatgpt", handoff_id=handoff_id)
                response = root / f"response-{index:02d}.md"
                response.write_text(
                    "---\n"
                    "protocol: mmwf-handoff/v1\n"
                    "project_id: simulation\n"
                    f"stage: {stage}\n"
                    f"handoff_id: {handoff_id}\n"
                    f"context_sha256: {manifest['context_sha256']}\n"
                    "---\n\nAccepted simulated stage result.\n",
                    encoding="utf-8",
                )
                import_chatgpt_response(root, handoff_id, response)
                prepare_handoff(root, "codex", handoff_id=handoff_id)

                artifact = root / artifacts[stage]
                artifact.parent.mkdir(parents=True, exist_ok=True)
                artifact.write_bytes(b"simulated verified artifact\n")
                record_codex_verification(
                    root,
                    handoff_id,
                    {
                        "verdict": "pass",
                        "checks": [{"id": "simulation", "status": "pass", "evidence": artifacts[stage]}],
                        "artifacts": [{"path": artifacts[stage], "role": "stage_output"}],
                        "contract_rows": [],
                        "conflicts": [],
                        "next_action": "advance",
                    },
                )

                if stage in gates:
                    waiting = read_state(root)
                    self.assertEqual("pending_human", waiting["status"])
                    self.assertEqual(gates[stage], waiting["pending_gate"])
                    confirm_gate(root, gates[stage])

            final = read_state(root)
            self.assertEqual("completed", final["status"])
            self.assertEqual(STAGES, final["completed_stages"])
            self.assertEqual("finalize", final["current_stage"])
            self.assertIsNone(final["pending_gate"])


if __name__ == "__main__":
    unittest.main()
