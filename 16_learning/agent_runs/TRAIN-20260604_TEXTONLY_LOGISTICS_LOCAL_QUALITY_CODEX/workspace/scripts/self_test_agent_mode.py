from __future__ import annotations

import csv
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_contracts  # noqa: E402
from agent_mode_utils import validate_problem_source_lock, write_problem_source_lock  # noqa: E402
from deepseek_agent_runner import apply_file_actions, extract_strict_json_object, normalize_simulated_gate_csv, protocol_issues_for_response, sanitized_call_id  # noqa: E402
from run_agent_mode import QUEUE_FIELDS, enhancement_feedback_severity, first_row_text, merge_contract_failures_into_queue, merge_validation_failures_into_queue, normalize_training_gate_log, refresh_training_final_submit, stages_for_blockers, write_stage_execution_prompt  # noqa: E402
from validate_agent_run import final_paper_is_structurally_thin, figure_output_paths, no_formal_effect, normalize_figure_id, paper_figure_references, paper_structure_counts, topic_alignment_issue  # noqa: E402


def write_header(path: Path, fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        csv.DictWriter(f, fieldnames=fields).writeheader()


def test_strict_protocol() -> None:
    obj, issues = extract_strict_json_object('{"status":"ok","files":[{"path":"11_review/a.md","content":"ok"}]}')
    assert obj and not issues
    obj, issues = extract_strict_json_object("<read_file path='x'/>")
    assert obj is None and "pseudo_tool_tag" in issues
    actions, issues = protocol_issues_for_response('{"status":"ok","files":[]}', "training_sandbox", "paper_full")
    assert actions == [] and "empty_file_actions" in issues
    assert sanitized_call_id("stage 01/intake", "fallback") == "stage_01_intake"


def test_problem_lock_drift() -> None:
    with tempfile.TemporaryDirectory() as tmp_raw:
        tmp = Path(tmp_raw)
        run_dir = tmp / "run"
        workspace = run_dir / "workspace"
        source = tmp / "problem.md"
        source_text = "# 颜色与物质浓度的辨识问题\n\nR G B concentration sample_id"
        source.write_text(source_text, encoding="utf-8")
        statement = workspace / "00_problem" / "problem_statement.md"
        statement.parent.mkdir(parents=True)
        statement.write_text(source_text, encoding="utf-8")
        write_problem_source_lock(run_dir, workspace, source, source_text)
        assert validate_problem_source_lock(run_dir, workspace) == []
        statement.write_text("# 2022 C 古代玻璃制品\n\nPbO BaO SiO2", encoding="utf-8")
        issues = validate_problem_source_lock(run_dir, workspace)
        assert issues and issues[0]["item"] == "problem_source_drift"


def test_final_contract_nonempty_gate() -> None:
    with tempfile.TemporaryDirectory() as tmp_raw:
        tmp = Path(tmp_raw)
        contracts = tmp / "14_contracts"
        write_header(contracts / "result_contract.csv", ["result_id"])
        write_header(contracts / "claim_evidence_map.csv", ["claim_id"])
        write_header(contracts / "figure_contract.csv", ["figure_id", "output_svg"])
        write_header(contracts / "formula_contract.csv", ["formula_id"])
        write_header(contracts / "citation_contract.csv", ["citation_id"])
        write_header(contracts / "artifact_freeze_registry.csv", ["artifact_id"])
        write_header(contracts / "polish_diff_check.csv", ["check_id"])
        write_header(contracts / "revision_tasks.csv", ["task_id"])
        original_root = validate_contracts.ROOT
        try:
            validate_contracts.ROOT = tmp
            issues = validate_contracts.validate_contract_bus("final_export")
        finally:
            validate_contracts.ROOT = original_root
        assert any(issue["item"] == "empty_final_required_contract" for issue in issues), issues


def test_active_citation_contract_metadata_gate() -> None:
    complete_issues: list[dict[str, str]] = []
    validate_contracts.validate_citation_contract(
        [
            {
                "citation_id": "CIT01",
                "status": "active",
                "support_grade": "method",
                "metadata_verified": "true",
                "bibtex_key": "BoxDraper1987",
            }
        ],
        complete_issues,
    )
    assert not [issue for issue in complete_issues if issue["level"] == "fail"], complete_issues
    missing_issues: list[dict[str, str]] = []
    validate_contracts.validate_citation_contract([{"citation_id": "CIT02", "status": "active"}], missing_issues)
    assert {issue["item"] for issue in missing_issues if issue["level"] == "fail"} == {
        "citation_without_support_grade",
        "citation_metadata_unverified",
    }


def test_contract_aliases_and_indirect_figure_binding() -> None:
    with tempfile.TemporaryDirectory() as tmp_raw:
        tmp = Path(tmp_raw)
        contracts = tmp / "14_contracts"
        contracts.mkdir(parents=True)
        figure_file = tmp / "08_figures" / "figF001.png"
        figure_file.parent.mkdir(parents=True)
        figure_file.write_text("sandbox figure", encoding="utf-8")
        with (contracts / "result_contract.csv").open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["result_id", "source_file"])
            writer.writeheader()
            writer.writerow({"result_id": "R001", "source_file": "07_results/metrics.csv"})
            writer.writerow({"result_id": "R002", "source_file": "07_results/metrics.csv"})
        claim_fields = ["claim_id", "claim_text", "evidence_type", "evidence_ref", "status", "figure_ids"]
        with (contracts / "claim_evidence_map.csv").open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=claim_fields)
            writer.writeheader()
            writer.writerow(
                {
                    "claim_id": "C001",
                    "claim_text": "RGB channels predict concentration.",
                    "evidence_type": "result",
                    "evidence_ref": "R001",
                    "status": "validated",
                    "figure_ids": "",
                }
            )
            writer.writerow(
                {
                    "claim_id": "C002",
                    "claim_text": "Residuals are stable.",
                    "evidence_type": "result",
                    "evidence_ref": "R001",
                    "status": "validated",
                    "figure_ids": "F002",
                }
            )
        with (contracts / "figure_contract.csv").open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["figure_id", "file_path", "caption", "claim_ids", "result_id"])
            writer.writeheader()
            writer.writerow({"figure_id": "figF001", "file_path": "08_figures/figF001.png", "caption": "Prediction chart", "claim_ids": "C001"})
            writer.writerow({"figure_id": "F002", "file_path": "08_figures/figF001.png", "caption": "Residual chart", "claim_ids": ""})
            writer.writerow({"figure_id": "F003", "file_path": "08_figures/figF001.png", "caption": "Multi-result chart", "claim_ids": "", "result_id": "R001;R002"})
        for name, fields in {
            "formula_contract.csv": ["formula_id"],
            "citation_contract.csv": ["citation_id"],
            "artifact_freeze_registry.csv": ["artifact_id"],
            "polish_diff_check.csv": ["check_id"],
            "revision_tasks.csv": ["task_id"],
        }.items():
            write_header(contracts / name, fields)
        original_root = validate_contracts.ROOT
        try:
            validate_contracts.configure_root(tmp)
            issues = validate_contracts.validate_contract_bus("final_export")
        finally:
            validate_contracts.configure_root(original_root)
        fail_items = {issue["item"] for issue in issues if issue["level"] == "fail"}
        assert "unsupported_claim" not in fail_items, issues
        assert "figure_without_result_source" not in fail_items, issues
        assert "figure_unknown_result" not in fail_items, issues
        assert normalize_figure_id("figF001") == "F001"


def test_gate_file_action_normalizes_formal_effect() -> None:
    with tempfile.TemporaryDirectory() as tmp_raw:
        workspace = Path(tmp_raw)
        policy = {"permissions": {"training_sandbox": {"apply_file_actions": True, "allow_workspace_writes": True}}}
        content = "timestamp,stage,gate_type,decision,comment,formal_effect\n2026-06-03T00:00:00Z,intake,human_gate,approved,simulated,无\n"
        result = apply_file_actions(
            [{"path": "11_review/simulated_human_gate_log.csv", "operation": "write", "content": content}],
            workspace,
            "training_sandbox",
            "final_export",
            policy,
        )
        assert result[0]["applied"]
        written = (workspace / "11_review" / "simulated_human_gate_log.csv").read_text(encoding="utf-8")
        assert "simulated_none" not in written
        assert written.strip().endswith(",none")
        assert no_formal_effect("无")


def test_gate_file_action_normalizes_prefixed_none() -> None:
    with tempfile.TemporaryDirectory() as tmp_raw:
        workspace = Path(tmp_raw)
        policy = {"permissions": {"training_sandbox": {"apply_file_actions": True, "allow_workspace_writes": True}}}
        content = "timestamp,stage,gate_type,decision,comment,formal_effect\n2026-06-03T00:00:00Z,intake,human_gate,approved,simulated,formal_effect=none\n"
        result = apply_file_actions(
            [{"path": "11_review/simulated_human_gate_log.csv", "operation": "write", "content": content}],
            workspace,
            "training_sandbox",
            "final_export",
            policy,
        )
        assert result[0]["applied"]
        written = (workspace / "11_review" / "simulated_human_gate_log.csv").read_text(encoding="utf-8")
        assert written.strip().endswith(",none")
        assert no_formal_effect("formal_effect=none")


def test_gate_file_action_forces_any_formal_effect_to_none() -> None:
    with tempfile.TemporaryDirectory() as tmp_raw:
        workspace = Path(tmp_raw)
        policy = {"permissions": {"training_sandbox": {"apply_file_actions": True, "allow_workspace_writes": True}}}
        content = "timestamp,stage,gate_type,decision,comment,formal_effect\n2026-06-03T00:00:00Z,figures,human_gate,approved,simulated,passed\n"
        result = apply_file_actions(
            [{"path": "11_review/simulated_human_gate_log.csv", "operation": "write", "content": content}],
            workspace,
            "training_sandbox",
            "final_export",
            policy,
        )
        assert result[0]["applied"]
        written = (workspace / "11_review" / "simulated_human_gate_log.csv").read_text(encoding="utf-8")
        assert written.strip().endswith(",none")


def test_gate_normalization_fills_missing_formal_effect() -> None:
    content = (
        "stage_id,gate_id,agent_decision,evidence,residual_risk,formal_effect\n"
        "revision_stage,revision_closure_gate,simulated_pass,closed,simulated\n"
    )
    normalized = normalize_simulated_gate_csv(content)
    assert normalized.strip().endswith(",simulated,none")
    with tempfile.TemporaryDirectory() as tmp_raw:
        workspace = Path(tmp_raw)
        path = workspace / "11_review" / "simulated_human_gate_log.csv"
        path.parent.mkdir(parents=True)
        path.write_text(content, encoding="utf-8")
        result = normalize_training_gate_log(workspace)
        assert result["normalized"] is True
        assert path.read_text(encoding="utf-8-sig").strip().endswith(",simulated,none")


def test_training_agent_cannot_write_revision_queue() -> None:
    with tempfile.TemporaryDirectory() as tmp_raw:
        workspace = Path(tmp_raw)
        policy = {"permissions": {"training_sandbox": {"apply_file_actions": True, "allow_workspace_writes": True}}}
        result = apply_file_actions(
            [{"path": "reports/agent_revision_queue.csv", "operation": "write", "content": "task_id,status\nBAD,closed\n"}],
            workspace,
            "training_sandbox",
            "final_export",
            policy,
        )
        assert not result[0]["applied"]
        assert result[0]["reason"] == "runner managed path is protected"
        assert not (workspace / "reports" / "agent_revision_queue.csv").exists()


def test_stage_prompt_includes_workspace_context_snapshot() -> None:
    with tempfile.TemporaryDirectory() as tmp_raw:
        run_dir = Path(tmp_raw) / "RUN"
        workspace = run_dir / "workspace"
        (workspace / "00_problem").mkdir(parents=True)
        (workspace / "14_contracts").mkdir(parents=True)
        (workspace / "09_paper").mkdir(parents=True)
        (run_dir / "reports").mkdir(parents=True)
        (workspace / "00_problem" / "problem_statement.md").write_text("RGB concentration task for T01 T02 T03", encoding="utf-8")
        (workspace / "14_contracts" / "figure_contract.csv").write_text(
            "figure_id,file_path,result_id,evidence_source,status\nF001,,R001,,draft\n",
            encoding="utf-8",
        )
        (workspace / "09_paper" / "full_draft.md").write_text("Draft cites Figure F001 for RGB concentration.", encoding="utf-8")
        with (run_dir / "reports" / "agent_revision_queue.csv").open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=QUEUE_FIELDS)
            writer.writeheader()
            writer.writerow(
                {
                    "task_id": "RUN-VAL-001",
                    "run_id": "RUN",
                    "iteration": "validation",
                    "severity": "fail",
                    "target_artifact": "14_contracts/figure_contract.csv",
                    "issue_summary": "F001 missing file_path",
                    "proposed_action": "Bind F001 to an existing figure file.",
                    "acceptance_check": "F001 has file_path and result_id.",
                    "status": "open",
                    "human_decision": "",
                    "notes": "validation_item=training_figure_contract_missing_output",
                }
            )
        prompt = write_stage_execution_prompt(
            run_dir,
            workspace,
            3,
            {"markdown_path": "route.md", "bundle_path": "bundle.md"},
            "figures",
            8,
            "iteration_02_08_figures",
            2,
            queue_path=run_dir / "reports" / "agent_revision_queue.csv",
        )
        text = prompt.read_text(encoding="utf-8")
        assert "# Workspace Context Snapshot" in text
        assert "14_contracts/figure_contract.csv" in text
        assert "F001,,R001" in text
        assert "RGB concentration task for T01 T02 T03" in text


def test_sandbox_contract_validation_payload_includes_issues() -> None:
    from run_agent_mode import validate_sandbox_contracts

    with tempfile.TemporaryDirectory() as tmp_raw:
        workspace = Path(tmp_raw)
        contracts = workspace / "14_contracts"
        write_header(contracts / "result_contract.csv", ["result_id"])
        write_header(contracts / "claim_evidence_map.csv", ["claim_id"])
        write_header(contracts / "figure_contract.csv", ["figure_id"])
        write_header(contracts / "formula_contract.csv", ["formula_id"])
        write_header(contracts / "citation_contract.csv", ["citation_id"])
        write_header(contracts / "artifact_freeze_registry.csv", ["artifact_id"])
        write_header(contracts / "polish_diff_check.csv", ["check_id"])
        write_header(contracts / "revision_tasks.csv", ["task_id"])
        payload = validate_sandbox_contracts(workspace)
        assert payload["fail_count"] > 0
        assert payload["issues"]


def test_training_final_submit_refreshes_from_latest_full_draft() -> None:
    with tempfile.TemporaryDirectory() as tmp_raw:
        workspace = Path(tmp_raw)
        draft = workspace / "09_paper" / "full_draft.md"
        final = workspace / "12_submission" / "final_submit_paper.md"
        draft.parent.mkdir(parents=True)
        final.parent.mkdir(parents=True)
        draft.write_text("# RGB concentration draft\n\n## 摘要\nT01 T02 T03 R G B concentration\n\n## 问题分析\nlocked topic\n", encoding="utf-8")
        final.write_text("# Generic water pollutant paper\n\n## 摘要\nno locked samples\n", encoding="utf-8")
        refreshed = refresh_training_final_submit(workspace)
        assert refreshed["refreshed"] is True
        assert "T01 T02 T03" in final.read_text(encoding="utf-8")


def test_final_paper_subsections_count_as_structure() -> None:
    sections = [
        "## Abstract\n" + "substance " * 80,
        "## 1 Analysis\n" + "substance " * 80,
        "## 2 Model\n### 2.1 Linear\n" + "substance " * 80,
        "### 2.2 Robustness\n" + "substance " * 80,
        "## 3 Results\n### 3.1 Prediction\n" + "substance " * 80,
        "### 3.2 Residuals\n" + "substance " * 80,
        "## 4 Validation\n### 4.1 Cross validation\n" + "substance " * 80,
        "## 5 Conclusion\n" + "substance " * 80,
    ]
    text = "# Title\n\n" + "\n\n".join(sections)
    counts = paper_structure_counts(text)
    assert counts["h2"] == 6
    assert counts["headings"] >= 9
    assert not final_paper_is_structurally_thin(text)
    assert final_paper_is_structurally_thin("# Title\n\n## Only section\nshort")


def test_training_enhancement_feedback_field_aliases() -> None:
    row = {
        "id": "TEP-001",
        "target_area": "prompt",
        "suggestion": "Require final_export to refresh citations before submit.",
        "rationale": "Live sandbox exposed missing citation metadata.",
        "priority": "high",
        "status": "draft",
    }
    assert first_row_text(row, "enhancement_id", "id") == "TEP-001"
    assert first_row_text(row, "proposed_change", "suggestion") == "Require final_export to refresh citations before submit."
    assert enhancement_feedback_severity(row) == "major"


def test_contract_failures_seed_stage_routed_queue() -> None:
    with tempfile.TemporaryDirectory() as tmp_raw:
        run_dir = Path(tmp_raw) / "RUN"
        reports = run_dir / "reports"
        reports.mkdir(parents=True)
        write_header(reports / "agent_revision_queue.csv", QUEUE_FIELDS)
        write_header(reports / "gap_report.csv", ["gap_id", "dimension"])
        payload = {
            "issues": [
                {"level": "fail", "item": "figure_without_result_source", "detail": "F001", "path": "14_contracts/figure_contract.csv"},
                {"level": "fail", "item": "review_score_below_threshold", "detail": "row 5", "path": "11_review/review_scorecard.csv"},
            ]
        }
        assert merge_contract_failures_into_queue(run_dir, payload) == 2
        with (reports / "agent_revision_queue.csv").open("r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        stages = stages_for_blockers(
            run_dir,
            rows,
            {
                "figures": {"stage_order": 8},
                "paper_full": {"stage_order": 10},
                "auto_review": {"stage_order": 11},
                "final_export": {"stage_order": 15},
            },
        )
        assert stages == ["figures", "paper_full", "auto_review", "final_export"]


def test_stale_validation_queue_rows_are_resolved() -> None:
    with tempfile.TemporaryDirectory() as tmp_raw:
        run_dir = Path(tmp_raw) / "RUN"
        reports = run_dir / "reports"
        reports.mkdir(parents=True)
        rows = [
            {
                "task_id": "T1",
                "run_id": "RUN",
                "iteration": "validation",
                "severity": "fail",
                "target_artifact": "figure_contract.csv",
                "issue_summary": "F001",
                "proposed_action": "fix figure",
                "acceptance_check": "figure fixed",
                "status": "open",
                "human_decision": "",
                "notes": "validation_item=training_figure_contract_missing_evidence_source",
            },
            {
                "task_id": "T2",
                "run_id": "RUN",
                "iteration": "validation",
                "severity": "fail",
                "target_artifact": "review_scorecard.csv",
                "issue_summary": "row 2: 3.0/10.0",
                "proposed_action": "fix review",
                "acceptance_check": "review fixed",
                "status": "open",
                "human_decision": "",
                "notes": "validation_item=training_review_score_below_threshold",
            },
        ]
        with (reports / "agent_revision_queue.csv").open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=QUEUE_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        validation = {
            "issues": [
                {
                    "level": "fail",
                    "item": "training_review_score_below_threshold",
                    "detail": "row 2: 3.0/10.0",
                    "path": "review_scorecard.csv",
                }
            ]
        }
        assert merge_validation_failures_into_queue(run_dir, validation) == 0
        with (reports / "agent_revision_queue.csv").open("r", encoding="utf-8-sig", newline="") as f:
            updated = {row["task_id"]: row for row in csv.DictReader(f)}
        assert updated["T1"]["status"] == "resolved"
        assert updated["T2"]["status"] == "open"


def test_topic_alignment_and_figure_refs() -> None:
    source = "颜色与物质浓度的辨识问题\nsample_id concentration_mg_L R G B T01 T02 T03"
    drifted = "## 摘要\n本文研究AQI空气质量预测，使用PM2.5和PM10建立回归模型。"
    aligned = "## 摘要\n本文基于RGB颜色通道R、G、B预测T01、T02、T03待测样本的物质浓度。"
    missing_targets = "## 摘要\n本文使用RGB颜色通道预测污染物浓度，但没有给出锁定题面的待测样本。"
    assert topic_alignment_issue(source, drifted)
    assert topic_alignment_issue(source, missing_targets)
    aligned = "## 摘要\nThis paper uses RGB color channels R G B to predict concentration for T01 T02 T03."
    assert topic_alignment_issue(source, aligned) == ""
    text = "加权F1分数为0.84。图F001展示散点，Figure F002 shows residuals."
    assert paper_figure_references(text) == ["F001", "F002"]
    assert figure_output_paths({"figure_id": "F001", "file_path": "08_figures/F001.svg"}) == ["08_figures/F001.svg"]


def main() -> None:
    tests = [
        test_strict_protocol,
        test_problem_lock_drift,
        test_final_contract_nonempty_gate,
        test_active_citation_contract_metadata_gate,
        test_contract_aliases_and_indirect_figure_binding,
        test_gate_file_action_normalizes_formal_effect,
        test_gate_file_action_normalizes_prefixed_none,
        test_gate_file_action_forces_any_formal_effect_to_none,
        test_gate_normalization_fills_missing_formal_effect,
        test_training_agent_cannot_write_revision_queue,
        test_stage_prompt_includes_workspace_context_snapshot,
        test_sandbox_contract_validation_payload_includes_issues,
        test_training_final_submit_refreshes_from_latest_full_draft,
        test_final_paper_subsections_count_as_structure,
        test_training_enhancement_feedback_field_aliases,
        test_contract_failures_seed_stage_routed_queue,
        test_stale_validation_queue_rows_are_resolved,
        test_topic_alignment_and_figure_refs,
    ]
    passed = []
    for test in tests:
        test()
        passed.append(test.__name__)
    print(json.dumps({"status": "pass", "tests": passed}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
