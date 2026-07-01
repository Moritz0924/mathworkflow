from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from workflow_utils import ROOT, assert_stage_allowed, complete_stage, read_state, rel, run_python

SCRIPT_MAP: Dict[str, Optional[Path]] = {
    "latex_template": ROOT / "scripts" / "generate_latex_template.py",
    "intake": ROOT / "scripts" / "start_from_inputs.py",
    "eda": ROOT / "04_eda_code" / "run_eda_pipeline.py",
    "task_analysis": ROOT / "scripts" / "decompose_problem.py",
    "prior_retrieval": ROOT / "scripts" / "retrieve_prior_cards.py",
    "model_route": ROOT / "scripts" / "route_weight_config.py",
    "codegen": ROOT / "scripts" / "generate_model_code.py",
    "results_freeze": None,
    "figures": ROOT / "scripts" / "check_figure_quality.py",
    "paper_draft": ROOT / "scripts" / "generate_paper_sections.py",
    "paper_full": ROOT / "scripts" / "generate_paper_sections.py",
    "auto_review": None,
    "revision": None,
    "polish": ROOT / "scripts" / "polish_latex_sections.py",
    "compile": ROOT / "scripts" / "compile_latex.py",
    "final_export": None,
}

PRECHECK_STAGES = {
    "prior_retrieval",
    "figures",
    "paper_draft",
    "paper_full",
    "auto_review",
    "polish",
    "compile",
    "final_export",
}


def ensure_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(text, encoding="utf-8")


def precheck(stage: str, skip_precheck: bool = False) -> None:
    if skip_precheck or stage not in PRECHECK_STAGES:
        return
    rc = run_python(ROOT / "scripts" / "validate_contracts.py", ["--stage", stage])
    if rc != 0:
        raise SystemExit(rc)


def builtin_prior_retrieval() -> None:
    base = ROOT / "13_prior_db"
    for sub in [base, base / "cards", base / "screening", base / "fulltext_index"]:
        sub.mkdir(parents=True, exist_ok=True)
    ensure_file(
        base / "pre_solve_cards.md",
        "# Prior DB pre-solve cards\n\n"
        "This MVP placeholder is intentionally conservative. Fill it with problem type experience, "
        "common model families, common figure types, scoring risks and preprocessing patterns only.\n\n"
        "Do not copy prior abstracts, body text, captions, tables or conclusions.\n",
    )
    complete_stage(
        "prior_retrieval",
        "Created/checked 13_prior_db scaffold. Only experience cards are allowed before solving.",
    )
    print(f"[OK] prepared {rel(base)}")


def builtin_results_freeze() -> None:
    ensure_file(
        ROOT / "07_results" / "result_freeze_report.md",
        "# Result freeze report\n\n"
        "Fill this after real model runs. Every paper-ready number must be mirrored in "
        "14_contracts/result_contract.csv with freeze_status=frozen.\n",
    )
    ensure_file(
        ROOT / "14_contracts" / "artifact_freeze_registry.csv",
        "artifact_id,artifact_type,path,hash_sha256,producing_stage,freeze_reason,freeze_time,protected_atoms,allowed_changes,owner,status,notes\n",
    )
    complete_stage(
        "results_freeze",
        "Prepared result freeze report and artifact freeze registry. Human gate must verify real outputs before figures/paper.",
    )
    print("[OK] results_freeze scaffold checked")


def builtin_auto_review() -> None:
    review_dir = ROOT / "11_review"
    review_dir.mkdir(parents=True, exist_ok=True)
    reviewers = [
        "problem_reviewer",
        "model_reviewer",
        "code_reviewer",
        "figure_reviewer",
        "paper_reviewer",
        "judge_reviewer",
    ]
    for reviewer in reviewers:
        ensure_file(
            review_dir / f"{reviewer}_comments.md",
            f"# {reviewer} comments\n\n"
            "MVP placeholder. Reviewer agents may write comments here only; they must not directly edit deliverables.\n",
        )
    ensure_file(
        review_dir / "review_scorecard.csv",
        "round_id,reviewer,dimension,score,max_score,severity,issue_count,top_risk,required_action,status,last_checked\n",
    )
    ensure_file(
        ROOT / "14_contracts" / "revision_tasks.csv",
        "task_id,round_id,reviewer,source_comment_id,severity,scope,target_artifact,target_location,issue_summary,required_action,acceptance_check,linked_contract_ids,status,assignee,created_time,closed_time,closure_note,human_waiver_by\n",
    )
    complete_stage(
        "auto_review",
        "Prepared reviewer comment files, scorecard and revision task contract. Reviewers output tasks only.",
    )
    print(f"[OK] prepared {rel(review_dir)}")


def builtin_revision() -> None:
    rc = run_python(ROOT / "scripts" / "validate_contracts.py", ["--stage", "revision"])
    if rc != 0:
        raise SystemExit(rc)
    ensure_file(
        ROOT / "15_iteration_memory" / "task_closure_log.md",
        "# Task closure log\n\nRecord each revision task, evidence of fix, rerun proof and human decision here.\n",
    )
    complete_stage(
        "revision",
        "Validated contract bus and revision task closure state. Human gate must confirm before polishing.",
    )
    print("[OK] revision validation passed")


def builtin_final_export() -> None:
    ppt_dir = ROOT / "12_export" / "pptx"
    ppt_dir.mkdir(parents=True, exist_ok=True)
    ensure_file(
        ppt_dir / "README.md",
        "# PPT export\n\nUse nature-paper2ppt only after final paper compilation and human confirmation.\n",
    )
    complete_stage("final_export", "Prepared post-final PPT export directory. Main submission remains the compiled paper package.")
    print(f"[OK] prepared {rel(ppt_dir)}")


def run_builtin(stage: str) -> int:
    handlers = {
        "prior_retrieval": builtin_prior_retrieval,
        "results_freeze": builtin_results_freeze,
        "auto_review": builtin_auto_review,
        "revision": builtin_revision,
        "final_export": builtin_final_export,
    }
    handler = handlers.get(stage)
    if not handler:
        print(f"[FAIL] no script or built-in handler for stage: {stage}")
        return 127
    handler()
    return 0


def script_args(stage: str, question: str, section: str, dev_debug: bool) -> List[str]:
    args: List[str] = []
    if stage == "codegen":
        args += ["--question", question, "--mode", "deep"]
    if stage in {"paper_draft", "paper_full", "polish"}:
        args += ["--section", section, "--mode", "deep"]
    if dev_debug:
        args.append("--dev-debug")
    return args


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the current v3.2-MVP workflow stage.")
    parser.add_argument("--stage", default="current", help="Stage to run. Defaults to workflow_state current_stage.")
    parser.add_argument("--question", default="Q1", help="Question id for codegen stage.")
    parser.add_argument("--section", default="current", help="Section id for paper/polish stages.")
    parser.add_argument("--dev-debug", action="store_true", help="Bypass stage lock checks for development only.")
    parser.add_argument("--skip-precheck", action="store_true", help="Skip contract precheck. Use only while filling templates.")
    args = parser.parse_args()

    stage = str(read_state().get("current_stage")) if args.stage == "current" else args.stage
    if stage not in SCRIPT_MAP:
        raise SystemExit(f"[FAIL] unknown stage: {stage}")

    assert_stage_allowed(stage, args.dev_debug)
    precheck(stage, skip_precheck=args.skip_precheck or args.dev_debug)

    script = SCRIPT_MAP[stage]
    if script is None:
        raise SystemExit(run_builtin(stage))

    env = {"MMWF_CURRENT_STAGE": stage, "MMWF_RUN_AT": datetime.now().isoformat(timespec="seconds")}
    raise SystemExit(run_python(script, script_args(stage, args.question, args.section, args.dev_debug), env=env))


if __name__ == "__main__":
    main()
