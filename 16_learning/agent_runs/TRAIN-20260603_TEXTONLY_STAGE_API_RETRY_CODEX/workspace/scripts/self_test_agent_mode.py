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
from deepseek_agent_runner import extract_strict_json_object, protocol_issues_for_response, sanitized_call_id  # noqa: E402


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


def main() -> None:
    tests = [test_strict_protocol, test_problem_lock_drift, test_final_contract_nonempty_gate]
    passed = []
    for test in tests:
        test()
        passed.append(test.__name__)
    print(json.dumps({"status": "pass", "tests": passed}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
