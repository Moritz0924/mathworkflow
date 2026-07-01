from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def make_minimal_run(tmp_path: Path) -> Path:
    run_dir = tmp_path / "TRAIN-QUALITY"
    workspace = run_dir / "workspace"
    (run_dir / "reports").mkdir(parents=True)
    (workspace / "12_submission").mkdir(parents=True)
    (workspace / "14_contracts").mkdir(parents=True)
    (workspace / "11_review").mkdir(parents=True)
    (workspace / "08_figures" / "output").mkdir(parents=True)

    (run_dir / "run_manifest.yaml").write_text("run_id: TRAIN-QUALITY\nmode: training_sandbox\nstatus: completed\n", encoding="utf-8")
    write_csv(
        run_dir / "reports" / "stage_acceptance_checklist.csv",
        [
            {"call_id": f"initial_{idx:02d}", "iteration": "1", "stage_id": f"stage_{idx:02d}", "check_item": "completion_conditions", "status": "pass", "evidence": "stage output", "notes": ""}
            for idx in range(16)
        ],
        ["call_id", "iteration", "stage_id", "check_item", "status", "evidence", "notes"],
    )
    (run_dir / "reports" / "agent_run_validation.json").write_text(
        json.dumps({"status": "pass", "fail_count": 0, "warn_count": 0, "issues": []}, ensure_ascii=False),
        encoding="utf-8",
    )
    (workspace / "11_review" / "contract_validation_report.json").write_text(
        json.dumps({"status": "pass", "fail_count": 0, "warn_count": 0, "issues": []}, ensure_ascii=False),
        encoding="utf-8",
    )
    write_csv(run_dir / "reports" / "copy_risk_report.csv", [{"decision": "pass", "max_overlap_ratio": "0.01"}], ["decision", "max_overlap_ratio"])
    write_csv(
        workspace / "11_review" / "simulated_human_gate_log.csv",
        [
            {"stage_id": "model_route", "gate_id": "model_route_gate", "agent_decision": "pass", "evidence": "ok", "residual_risk": "low", "formal_effect": "none"},
            {"stage_id": "results_freeze", "gate_id": "results_freeze_gate", "agent_decision": "pass", "evidence": "ok", "residual_risk": "low", "formal_effect": "none"},
            {"stage_id": "paper_full", "gate_id": "draft_review_gate", "agent_decision": "pass", "evidence": "ok", "residual_risk": "low", "formal_effect": "none"},
            {"stage_id": "compile", "gate_id": "final_submission_gate", "agent_decision": "pass", "evidence": "ok", "residual_risk": "low", "formal_effect": "none"},
        ],
        ["stage_id", "gate_id", "agent_decision", "evidence", "residual_risk", "formal_effect"],
    )
    write_csv(
        workspace / "11_review" / "review_scorecard.csv",
        [{"item": "overall", "status": "pass", "severity": "", "score": "92", "max_score": "100", "evidence": "paper", "notes": ""}],
        ["item", "status", "severity", "score", "max_score", "evidence", "notes"],
    )
    write_csv(
        workspace / "14_contracts" / "revision_tasks.csv",
        [{"task_id": "REV-001", "source": "training", "severity": "major", "target_artifact": "paper", "issue": "quality", "action": "fixed", "status": "closed", "owner": "agent", "notes": ""}],
        ["task_id", "source", "severity", "target_artifact", "issue", "action", "status", "owner", "notes"],
    )

    for idx in range(1, 7):
        fig = workspace / "08_figures" / "output" / f"F{idx:03d}.svg"
        fig.write_text(
            f"<svg xmlns='http://www.w3.org/2000/svg' width='640' height='360'><rect width='640' height='360' fill='#f8fafc'/><text x='20' y='40'>图 {idx}：中文图表</text><path d='M40 320 L600 80' stroke='#2563eb' stroke-width='4'/></svg>",
            encoding="utf-8",
        )
    write_csv(
        workspace / "14_contracts" / "figure_contract.csv",
        [
            {"figure_id": f"F{idx:03d}", "title": f"图 {idx}", "result_id": "R001", "evidence_source": "07_results/metrics.csv", "output_svg": f"08_figures/output/F{idx:03d}.svg", "output_png": "", "output_pdf": "", "used_in_section": "结果分析", "latex_label": f"fig:f{idx:03d}", "quality_score": "4.8", "status": "ready", "owner": "agent", "notes": ""}
            for idx in range(1, 7)
        ],
        ["figure_id", "title", "result_id", "evidence_source", "output_svg", "output_png", "output_pdf", "used_in_section", "latex_label", "quality_score", "status", "owner", "notes"],
    )
    write_csv(
        workspace / "14_contracts" / "formula_contract.csv",
        [
            {"formula_id": f"EQ{idx}", "used_in_section": "模型建立", "formula_latex": f"y={idx}x", "meaning": "公式", "symbols_defined": "y,x", "assumption_ids": "A1", "result_ids": "R001", "status": "ready", "owner": "agent", "notes": ""}
            for idx in range(1, 4)
        ],
        ["formula_id", "used_in_section", "formula_latex", "meaning", "symbols_defined", "assumption_ids", "result_ids", "status", "owner", "notes"],
    )
    paper = "\n".join(
        [
            "# 训练结果论文",
            "## 训练验收条件与通过记录",
            "门禁、合同、图表、审稿、导出、复制风险和知识库质量基准均已记录。",
            "表 1 测试表\n\n| 指标 | 数值 |\n|---|---:|\n| a | 1 |",
            "表 2 测试表\n\n| 指标 | 数值 |\n|---|---:|\n| b | 2 |",
            "表 3 测试表\n\n| 指标 | 数值 |\n|---|---:|\n| c | 3 |",
            "表 4 测试表\n\n| 指标 | 数值 |\n|---|---:|\n| d | 4 |",
            *(f"## 第 {idx} 节\n图 F{idx:03d} 表 {idx} 公式 EQ{min(idx,3)} validation sensitivity robustness residual error 验证 稳健 残差。\n" + "正文内容。" * 450 for idx in range(1, 8)),
        ]
    )
    (workspace / "12_submission" / "final_submit_paper.md").write_text(paper, encoding="utf-8")
    (workspace / "12_submission" / "final_submit_paper.docx").write_bytes(b"PK\x03\x04fake-docx")
    (workspace / "12_submission" / "final_submit_paper.pdf").write_bytes(b"%PDF-1.4\n%%EOF\n")
    (workspace / "12_submission" / "export_manifest.json").write_text(
        json.dumps(
            {
                "docx": "12_submission/final_submit_paper.docx",
                "pdf": "12_submission/final_submit_paper.pdf",
                "rendered_pages": ["12_submission/rendered_pages/page-1.png"],
                "visual_qa": {"status": "pass", "page_count": 1, "pdf_page_count": 1},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (workspace / "12_submission" / "rendered_pages").mkdir()
    (workspace / "12_submission" / "rendered_pages" / "page-1.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    return run_dir


class TrainingQualityAcceptanceTests(unittest.TestCase):
    def test_training_acceptance_requires_mixed_quality_gates(self) -> None:
        from validate_training_acceptance import evaluate_training_acceptance

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_minimal_run(Path(tmp))
            payload = evaluate_training_acceptance(run_dir, profile="excellent")
        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["thresholds"]["min_chars"], 12000)
        self.assertEqual(payload["thresholds"]["min_figures"], 6)
        self.assertEqual(payload["thresholds"]["min_tables"], 4)
        self.assertEqual(payload["thresholds"]["min_formulas"], 3)
        self.assertFalse([issue for issue in payload["issues"] if issue["level"] == "fail"])


    def test_training_acceptance_fails_missing_export_and_appendix(self) -> None:
        from validate_training_acceptance import evaluate_training_acceptance

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_minimal_run(Path(tmp))
            workspace = run_dir / "workspace"
            (workspace / "12_submission" / "final_submit_paper.docx").unlink()
            paper = (workspace / "12_submission" / "final_submit_paper.md").read_text(encoding="utf-8")
            (workspace / "12_submission" / "final_submit_paper.md").write_text(paper.replace("训练验收条件与通过记录", "普通附录"), encoding="utf-8")
            payload = evaluate_training_acceptance(run_dir, profile="excellent")

        items = {issue["item"] for issue in payload["issues"] if issue["level"] == "fail"}
        self.assertIn("missing_docx_export", items)
        self.assertIn("missing_acceptance_appendix", items)
        self.assertEqual(payload["status"], "fail")


    def test_problem_reuse_detection_uses_problem_source_sha(self) -> None:
        from run_agent_mode import find_reused_problem_source

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            problem = tmp_path / "new_problem.md"
            problem.write_text("# A\nsame body\n", encoding="utf-8")
            old_run = tmp_path / "runs" / "OLD" / "reports"
            old_run.mkdir(parents=True)
            old_run.joinpath("problem_source_lock.json").write_text(
                json.dumps({"source_path": "00_problem/inbox/old.md", "source": {"sha256": "will-be-overwritten"}}),
                encoding="utf-8",
            )
            import agent_mode_utils

            lock = json.loads(old_run.joinpath("problem_source_lock.json").read_text(encoding="utf-8"))
            lock["source"]["sha256"] = agent_mode_utils.sha256_text(problem.read_text(encoding="utf-8"))
            old_run.joinpath("problem_source_lock.json").write_text(json.dumps(lock), encoding="utf-8")
            reused = find_reused_problem_source(problem, runs_root=tmp_path / "runs")

        self.assertTrue(reused)
        self.assertEqual(reused[0]["run_id"], "OLD")


if __name__ == "__main__":
    unittest.main()
