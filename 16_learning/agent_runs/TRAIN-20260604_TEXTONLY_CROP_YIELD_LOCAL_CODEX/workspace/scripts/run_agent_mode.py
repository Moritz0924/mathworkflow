from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence

from agent_mode_utils import (
    AGENT_RUNS_ROOT,
    INDEX_PATH,
    append_run_index,
    default_timeout,
    ensure_run_root,
    make_run_id,
    now_local,
    prepare_sandbox_workspace,
    read_agent_policy,
    resolve_agent_command,
    run_agent_command,
    safe_rel,
    validate_problem_source_lock,
    write_manifest,
    write_environment_diagnostics,
    write_protected_snapshot,
    write_run_copy_risk,
)
from benchmark_agent_run import QUEUE_FIELDS, benchmark_run, find_or_build_draft
from validate_agent_run import validate_run
from workflow_utils import ROOT, dump_yaml, load_yaml, read_csv_dict, read_state, write_csv_dicts


TRAINING_FEEDBACK_ROOT = ROOT / "15_iteration_memory" / "training_feedback"
TRAINING_FEEDBACK_FIELDS = [
    "feedback_id",
    "source_task_id",
    "source_run_id",
    "formal_stage",
    "severity",
    "formal_target",
    "sandbox_target",
    "issue_summary",
    "proposed_action",
    "acceptance_check",
    "status",
    "safety_note",
]

PROMPT_ROUTE_FIELDS = [
    "stage_order",
    "stage_id",
    "prompt_file",
    "formal_prompt_file",
    "sandbox_prompt_file",
    "sha256",
    "formal_sha256",
    "sandbox_sha256",
    "size_bytes",
    "included_in_training",
]

STAGE_EXECUTION_FIELDS = [
    "call_id",
    "iteration",
    "stage_order",
    "stage_id",
    "prompt_path",
    "log_path",
    "exit_code",
    "status",
    "started_at",
    "finished_at",
    "notes",
]

GAP_STAGE_MAP = {
    "contract_binding": ["results_freeze", "paper_full", "final_export"],
    "figure_density": ["figures", "paper_full", "final_export"],
    "validation_completeness": ["results_freeze", "paper_full", "final_export"],
    "structure_depth": ["paper_full", "final_export"],
    "formula_and_model_detail": ["paper_full", "final_export"],
}

VALIDATION_STAGE_MAP = {
    "missing_training_enhancement_points": ["auto_review", "final_export"],
    "missing_training_enhancement_markdown": ["auto_review", "final_export"],
    "training_enhancement_area_missing": ["auto_review", "final_export"],
    "missing_submit_ready_training_artifact": ["paper_full", "final_export"],
    "training_final_paper_too_thin": ["paper_full", "final_export"],
    "training_final_paper_placeholder": ["paper_full", "final_export"],
    "training_final_paper_missing_section_signal": ["paper_full", "final_export"],
    "training_topic_alignment_drift": ["paper_full", "final_export"],
    "training_contract_empty": ["results_freeze", "paper_full", "final_export"],
    "training_figure_contract_missing_output": ["figures"],
    "training_figure_contract_file_missing": ["figures"],
    "training_figure_contract_missing_evidence_source": ["figures", "paper_full", "final_export"],
    "training_claim_missing_result_link": ["results_freeze", "paper_full", "final_export"],
    "training_claim_missing_figure_link": ["figures", "paper_full", "final_export"],
    "training_claim_missing_formula_link": ["paper_full", "final_export"],
    "training_paper_unregistered_figure_reference": ["figures", "paper_full", "final_export"],
    "training_simulated_gate_log_incomplete": ["auto_review", "final_export"],
    "training_simulated_gate_has_formal_effect": ["auto_review", "final_export"],
    "training_review_scorecard_missing": ["auto_review", "final_export"],
    "training_review_fail_unclosed": ["auto_review", "final_export"],
    "training_review_score_below_threshold": ["results_freeze", "figures", "paper_full", "revision", "auto_review", "final_export"],
    "training_revision_task_unresolved": ["revision", "auto_review", "final_export"],
    "deepseek_protocol_violation": ["revision"],
    "problem_source_drift": ["intake"],
}

CONTRACT_STAGE_MAP = {
    "result_without_source_file": ["results_freeze", "paper_full", "final_export"],
    "result_metric_missing": ["results_freeze", "paper_full", "final_export"],
    "result_value_missing": ["results_freeze", "paper_full", "final_export"],
    "figure_without_result_source": ["figures", "paper_full", "final_export"],
    "figure_unknown_result": ["figures", "paper_full", "final_export"],
    "figure_file_missing": ["figures"],
    "figure_quality_low": ["figures", "auto_review", "final_export"],
    "unsupported_claim": ["paper_full", "final_export"],
    "claim_without_result_or_citation": ["paper_full", "final_export"],
    "citation_without_support_grade": ["prior_retrieval", "paper_full", "final_export"],
    "citation_metadata_unverified": ["prior_retrieval", "paper_full", "final_export"],
    "review_score_below_threshold": ["results_freeze", "figures", "paper_full", "revision", "auto_review", "final_export"],
    "review_fail_unclosed": ["auto_review", "final_export"],
    "revision_task_unresolved": ["revision", "auto_review", "final_export"],
    "empty_final_required_contract": ["results_freeze", "figures", "paper_full", "final_export"],
}

VALIDATION_QUEUE_SKIP_ITEMS = {
    "open_blocking_revision_queue",
    "missing_copy_risk_report",
    "copy_risk_not_run",
    "empty_gap_report",
}

STAGE_OUTPUT_REQUIREMENTS = {
    "results_freeze": [
        "Write non-empty `14_contracts/result_contract.csv` with result_id, metric_name, metric_value, source_file, used_by_claim_ids, freeze_status.",
        "Every numerical result cited later must have a result_contract row.",
        "Write or update reproducible result files under `07_results/` before freezing numbers.",
    ],
    "figures": [
        "Write `14_contracts/figure_contract.csv` with this schema when possible: figure_id,result_id,evidence_source,chart_type,title_cn,output_svg,output_png,output_pdf,quality_score,used_in_section,latex_label,caption_cn,notes.",
        "Every figure_contract row must have result_id or evidence_source, and at least one existing output_svg/output_png/output_pdf/file_path.",
        "Prefer canonical figure ids `F001`, `F002`, ... in every contract and paper reference; do not invent `figF001` aliases.",
        "Create the referenced figure files under `08_figures/`; text placeholders are acceptable only if they are explicit sandbox figures.",
        "Do not cite figures in paper text unless they are registered and files exist.",
        "When a `figure_density` blocker is open, generate enough result-bound figures to meet the benchmark target; use at least seven registered figure ids when the queue threshold is above 6.",
        "Use exactly the same figure ids in text and contract, such as `图F001`; do not use bare `F1` as a figure reference.",
    ],
    "paper_full": [
        "Write substantive `09_paper/full_draft.md` with at least 摘要, 问题分析, 模型建立, 结果分析, 验证/敏感性, 结论.",
        "Keep the paper topic aligned with the locked problem statement: color channels R/G/B and concentration prediction for T01/T02/T03; do not switch to AQI, wine quality, or unrelated benchmark topics.",
        "Write non-empty `14_contracts/claim_evidence_map.csv`; each major claim must bind to result_id and, where applicable, figure_id/formula_id.",
        "Write `14_contracts/formula_contract.csv` for important equations and symbol definitions.",
        "If the paper uses references, write `14_contracts/citation_contract.csv` with support_grade, metadata_verified=true, and bibtex_key for every active citation, or mark unused citation rows inactive.",
        "When `figure_density` is open, cite the registered figures in the paper using `图F001`, `图F002`, ... and include at least seven figure references if the benchmark threshold is above 6.",
    ],
    "auto_review": [
        "Write current `11_review/review_scorecard.csv` and `14_contracts/revision_tasks.csv`; do not leave stale fail rows from earlier missing artifacts.",
        "Review scorecard rows should use score/max_score and must be at least 85% after the sandbox artifacts are fixed; on a 10-point scale use 9 or 10 for pass, otherwise keep the item as an open blocker.",
        "Write `11_review/simulated_human_gate_log.csv` with columns stage_id, gate_id, agent_decision, evidence, residual_risk, formal_effect.",
        "Every simulated gate row must set formal_effect to `none`; never use confirmed/approved as a formal workflow effect.",
    ],
    "final_export": [
        "Write `12_submission/final_submit_paper.md` as the submit-ready paper text copied or assembled from `09_paper/full_draft.md` after contracts exist.",
        "The final submit paper must preserve the latest full_draft topic markers, especially T01/T02/T03, RGB, and concentration; do not replace it with a generic paper.",
        "If `09_paper/full_draft.md` changed in the same iteration, final_export must refresh `12_submission/final_submit_paper.md` from that latest draft.",
        "Write `12_submission/final_submit_package.md` with included artifacts and residual risks.",
        "Write `reports/training_enhancement_points.csv` and `.md`; CSV must include at least one target_area each of system, prompt, and gate.",
        "Ensure simulated gate log has at least four rows and formal_effect is `none` for every row.",
        "Before final_export, every active citation_contract row must include support_grade, metadata_verified=true, and bibtex_key; remove or mark inactive any unused citation rows.",
    ],
}

RUN_REPORT_SYNC_FILES = [
    "reports/training_enhancement_points.csv",
    "reports/training_enhancement_points.md",
]

SIMULATED_GATE_FIELDS = ["stage_id", "gate_id", "agent_decision", "evidence", "residual_risk", "formal_effect"]

STAGE_CONTEXT_COMMON_FILES = [
    ("workspace", "00_problem/problem_statement.md", 6000),
    ("run", "reports/agent_revision_queue.csv", 12000),
    ("run", "reports/gap_report.csv", 5000),
    ("run", "reports/full_gap_report.md", 5000),
    ("workspace", "14_contracts/result_contract.csv", 8000),
    ("workspace", "14_contracts/claim_evidence_map.csv", 8000),
    ("workspace", "14_contracts/figure_contract.csv", 8000),
    ("workspace", "14_contracts/formula_contract.csv", 5000),
    ("workspace", "11_review/review_scorecard.csv", 5000),
    ("workspace", "11_review/revision_tasks.csv", 5000),
    ("workspace", "14_contracts/revision_tasks.csv", 5000),
]

STAGE_CONTEXT_EXTRA_FILES = {
    "results_freeze": [
        ("workspace", "05_model/model_plan.md", 5000),
        ("workspace", "06_code/model_code.py", 5000),
        ("workspace", "07_results/metrics/model_metrics.csv", 5000),
    ],
    "figures": [
        ("workspace", "09_paper/full_draft.md", 8000),
    ],
    "paper_draft": [
        ("workspace", "01_task_analysis/task_analysis.md", 6000),
        ("workspace", "05_model/model_plan.md", 5000),
        ("workspace", "09_paper/draft.md", 8000),
    ],
    "paper_full": [
        ("workspace", "01_task_analysis/task_analysis.md", 6000),
        ("workspace", "05_model/model_plan.md", 5000),
        ("workspace", "09_paper/full_draft.md", 12000),
    ],
    "auto_review": [
        ("workspace", "09_paper/full_draft.md", 12000),
        ("workspace", "12_submission/final_submit_paper.md", 8000),
    ],
    "revision": [
        ("workspace", "09_paper/full_draft.md", 12000),
        ("workspace", "12_submission/final_submit_paper.md", 8000),
        ("workspace", "11_review/contract_validation_report.md", 8000),
    ],
    "final_export": [
        ("workspace", "09_paper/full_draft.md", 16000),
        ("workspace", "12_submission/final_submit_paper.md", 12000),
        ("workspace", "11_review/simulated_human_gate_log.csv", 5000),
        ("workspace", "11_review/contract_validation_report.md", 8000),
    ],
}

STAGE_CONTEXT_LIST_DIRS = [
    "07_results",
    "08_figures",
    "09_paper",
    "11_review",
    "12_submission",
]


def write_training_prompt(run_dir: Path, workspace: Path, max_iterations: int, route_manifest: Mapping[str, Any]) -> Path:
    prompt = workspace / "agent_prompt.md"
    text = f"""# Full-Agent Training Sandbox Wrapper

You are operating inside a sandbox workspace, not the formal project root.

Workspace: `{workspace}`
Max iterations: {max_iterations}
Prompt route manifest: `{route_manifest.get('markdown_path')}`
Prompt route CSV: `{route_manifest.get('csv_path')}`
Training sandbox stage prompt bundle: `{route_manifest.get('bundle_path')}`

This wrapper is not a replacement for the formal prompt system. The training route uses sandbox-specific backup prompts derived from the normal competition prompts:

1. Global prompt contract: `prompts/stage_prompt_contract.md`
2. Formal source prompts: `prompts/stages/00_*.md` through `prompts/stages/15_*.md`
3. Sandbox backup prompts: `prompts/training_sandbox/stages/00_*.md` through `prompts/training_sandbox/stages/15_*.md`
4. Stage order and prompt file mapping: the prompt route manifest above
5. Exact assembled sandbox prompts with formal sources: the stage prompt bundle above

Full-agent training rules:
- Use the sandbox backup prompt for each stage; never modify the formal source prompt files during a training run.
- Sandbox prompt changes are candidate workflow improvements only until they pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.
- Walk the 16 stage prompts in deep_sequential order inside the sandbox.
- A human gate in a formal stage becomes a simulated sandbox gate, not a formal confirmation. Record each simulated gate in `11_review/simulated_human_gate_log.csv` with stage, gate name, agent decision, evidence, and residual risk.
- Do not write outside the sandbox workspace.
- Do not copy prior paper abstracts, body text, captions, tables, or conclusions.
- Keep the entire sandbox solution aligned with the locked problem statement. For the text-only color problem, paper/results/figures must stay about RGB color channels, concentration prediction, and T01/T02/T03; never switch to AQI, wine quality, or another prior benchmark topic.
- Generate paper facts only from sandbox code, contracts, data, figures, and review artifacts.
- Keep result numbers in `14_contracts/result_contract.csv`.
- Keep claims in `14_contracts/claim_evidence_map.csv`.
- Keep figures in `14_contracts/figure_contract.csv` and cite only existing files.
- After a draft exists, use local prior DB only for gap comparison, not as an answer key.
- A single training run may contain multiple revision turns, but the run output must represent one full simulated competition pass.

Full-agent final outputs:
- Produce or assemble a complete Chinese paper in `09_paper/full_draft.md`.
- Copy the submit-ready version to `12_submission/final_submit_paper.md`.
- Produce `12_submission/final_submit_package.md`.
- Produce training improvement outputs for the workflow itself:
  - `reports/training_enhancement_points.csv`
  - `reports/training_enhancement_points.md`
  - include at least one `system`, one `prompt`, and one `gate` enhancement item.

Final expected sandbox artifacts:
- `09_paper/full_draft.md`
- `12_submission/final_submit_paper.md`
- `12_submission/final_submit_package.md`
- `14_contracts/result_contract.csv`
- `14_contracts/claim_evidence_map.csv`
- `14_contracts/figure_contract.csv`
- `11_review/review_scorecard.csv`
- `14_contracts/revision_tasks.csv`
- `reports/prompt_route_manifest.csv`
- `reports/training_enhancement_points.csv`
- `reports/training_enhancement_points.md`
"""
    prompt.write_text(text, encoding="utf-8")
    (run_dir / "agent_prompt.md").write_text(text, encoding="utf-8")
    return prompt


def write_iteration_prompt(run_dir: Path, workspace: Path, iteration: int) -> Path:
    queue = run_dir / "reports" / "agent_revision_queue.csv"
    prompt = workspace / f"agent_iteration_{iteration:02d}_prompt.md"
    text = f"""# Agent Training Iteration {iteration}

Use the structured revision queue at:
`{queue}`

Work only inside:
`{workspace}`

Tasks:
- Address open fail/major items first.
- Re-enter the stage prompt route from `10_ai_logs/prompt_route_manifest.csv` before changing paper, contract, figure, review, or submission artifacts.
- Preserve result numbers unless regenerated by executable sandbox code.
- Update contracts before updating draft text.
- Do not copy prior-paper text.
- Leave unresolved items open with a clear blocker note.
- Keep `reports/training_enhancement_points.csv` current with system, prompt, and gate enhancement candidates.
"""
    prompt.write_text(text, encoding="utf-8")
    return prompt


def read_context_text(path: Path, max_chars: int) -> str:
    if not path.exists() or not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="ignore")
    if len(text) > max_chars:
        return text[:max_chars] + f"\n[truncated to {max_chars} chars]"
    return text


def context_file_section(label: str, path: Path, max_chars: int) -> str:
    text = read_context_text(path, max_chars)
    if not text.strip():
        return ""
    safe_text = text.replace("```", "'''")
    return f"## {label}\n\n```text\n{safe_text.rstrip()}\n```\n"


def context_file_listing(workspace: Path, rel_dirs: Sequence[str], max_entries: int = 120) -> str:
    lines: List[str] = []
    for rel_dir in rel_dirs:
        base = workspace / rel_dir
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            try:
                rel = safe_rel(path, workspace)
                size = path.stat().st_size
            except OSError:
                continue
            lines.append(f"- {rel} ({size} bytes)")
            if len(lines) >= max_entries:
                lines.append(f"- [truncated after {max_entries} files]")
                return "## Workspace File Listing\n\n" + "\n".join(lines) + "\n"
    if not lines:
        return ""
    return "## Workspace File Listing\n\n" + "\n".join(lines) + "\n"


def stage_context_sources(stage_id: str) -> List[tuple[str, str, int]]:
    sources: List[tuple[str, str, int]] = []
    seen: set[tuple[str, str]] = set()
    for source in STAGE_CONTEXT_COMMON_FILES + STAGE_CONTEXT_EXTRA_FILES.get(stage_id, []):
        key = (source[0], source[1])
        if key in seen:
            continue
        seen.add(key)
        sources.append(source)
    return sources


def build_stage_context_snapshot(run_dir: Path, workspace: Path, stage_id: str, max_chars: int = 52000) -> str:
    sections: List[str] = [
        "# Workspace Context Snapshot",
        "This bounded snapshot is the API agent's read context for the current stage. Use it instead of pseudo-tools or file-read requests.",
    ]
    listing = context_file_listing(workspace, STAGE_CONTEXT_LIST_DIRS)
    if listing:
        sections.append(listing.rstrip())
    for root_name, rel_path, char_limit in stage_context_sources(stage_id):
        root = run_dir if root_name == "run" else workspace
        section = context_file_section(rel_path, root / rel_path, char_limit)
        if section:
            sections.append(section.rstrip())
    snapshot = "\n\n".join(sections).rstrip() + "\n"
    if len(snapshot) > max_chars:
        snapshot = snapshot[:max_chars] + f"\n[workspace context snapshot truncated to {max_chars} chars]\n"
    return snapshot


def write_stage_execution_prompt(
    run_dir: Path,
    workspace: Path,
    max_iterations: int,
    route_manifest: Mapping[str, Any],
    stage_id: str,
    stage_order: int,
    call_id: str,
    iteration: int,
    queue_path: Optional[Path] = None,
) -> Path:
    prompt = workspace / f"agent_stage_{call_id}.md"
    queue_text = ""
    if queue_path:
        queue_rows = blocking_queue_rows(run_dir)
        queue_lines = [
            f"- [{row.get('severity')}] {row.get('task_id')}: {row.get('proposed_action') or row.get('issue_summary')} | acceptance: {row.get('acceptance_check')} | notes: {row.get('notes')}"
            for row in queue_rows[:12]
        ]
        queue_text = f"\nRevision queue: `{queue_path}`\n\nOpen fail/major queue items:\n" + ("\n".join(queue_lines) if queue_lines else "- none") + "\n"
    stage_requirements = "\n".join(f"- {item}" for item in STAGE_OUTPUT_REQUIREMENTS.get(stage_id, []))
    if stage_requirements:
        stage_requirements = "\nStage-specific required outputs:\n" + stage_requirements + "\n"
    context_snapshot = build_stage_context_snapshot(run_dir, workspace, stage_id)
    text = f"""# Training Sandbox Stage Call

You are executing one simulated formal stage inside the training sandbox.

Workspace: `{workspace}`
Run dir: `{run_dir}`
Call id: `{call_id}`
Iteration: {iteration}
Max iterations: {max_iterations}
Current simulated stage: `{stage_id}`
Stage order: {stage_order}
Prompt route manifest: `{route_manifest.get('markdown_path')}`
Training sandbox stage prompt bundle: `{route_manifest.get('bundle_path')}`
{queue_text}
Rules:
- Follow only deep_sequential behavior for this stage.
- Do not edit `00_problem/problem_statement.md` or `00_problem/inbox/`; write intake analysis to `01_task_analysis/`.
- A formal human gate becomes a simulated sandbox gate. Record it in `11_review/simulated_human_gate_log.csv`.
- Update contracts before writing paper claims, result analysis, figures, or submission text.
- Use the Workspace Context Snapshot below as the current file context; do not request read_file/list_files pseudo-tools.
- Reply only through runner file actions. The external runner will reject prose-only or pseudo-tool responses.

Stage output target:
- Create or update the artifacts normally owned by `{stage_id}`.
- If this stage cannot close a blocker, update review/revision artifacts with a concrete blocker note.
- Keep `reports/training_enhancement_points.csv` current once a full draft or review finding exists.
{stage_requirements}
{context_snapshot}
"""
    prompt.write_text(text, encoding="utf-8")
    return prompt


def update_status(run_dir: Path, status: str, extra: Optional[Mapping[str, Any]] = None) -> Path:
    payload: Dict[str, Any] = {"status": status, "updated_at": now_local()}
    if extra:
        payload.update(dict(extra))
    return write_manifest(run_dir, payload)


def sync_workspace_reports(run_dir: Path, workspace: Path) -> List[str]:
    synced: List[str] = []
    for rel_path in RUN_REPORT_SYNC_FILES:
        src = workspace / rel_path
        if not src.exists() or not src.is_file():
            continue
        dst = run_dir / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())
        synced.append(rel_path)
    return synced


def normalize_training_gate_log(workspace: Path) -> Dict[str, Any]:
    path = workspace / "11_review" / "simulated_human_gate_log.csv"
    result: Dict[str, Any] = {"normalized": False, "path": safe_rel(path, workspace), "rows": 0, "reason": ""}
    if not path.exists() or not path.is_file():
        result["reason"] = "missing_gate_log"
        return result
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            rows = [dict(row) for row in reader]
            fieldnames = [str(field) for field in (reader.fieldnames or []) if field]
    except Exception as exc:
        result["reason"] = f"read_error:{exc}"
        return result
    if not rows:
        result["reason"] = "empty_gate_log"
        return result
    if not fieldnames:
        fieldnames = list(SIMULATED_GATE_FIELDS)
    if "formal_effect" not in fieldnames:
        fieldnames.append("formal_effect")
    for row in rows:
        row.pop(None, None)
        row["formal_effect"] = "none"
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    result.update({"normalized": True, "rows": len(rows), "reason": "formal_effect_forced_none"})
    return result


def refresh_training_final_submit(workspace: Path) -> Dict[str, Any]:
    draft = workspace / "09_paper" / "full_draft.md"
    final = workspace / "12_submission" / "final_submit_paper.md"
    report = workspace / "reports" / "final_export_refresh.json"
    draft_text = draft.read_text(encoding="utf-8", errors="ignore") if draft.exists() else ""
    final_text = final.read_text(encoding="utf-8", errors="ignore") if final.exists() else ""
    result: Dict[str, Any] = {
        "refreshed": False,
        "reason": "",
        "draft": safe_rel(draft, workspace),
        "final": safe_rel(final, workspace),
        "draft_chars": len(draft_text),
        "final_chars": len(final_text),
    }
    if not draft_text.strip():
        result["reason"] = "missing_full_draft"
    else:
        marker_terms = ["T01", "T02", "T03", "RGB", "concentration", "浓度", "颜色"]
        draft_markers = {term for term in marker_terms if term.lower() in draft_text.lower()}
        final_markers = {term for term in marker_terms if term.lower() in final_text.lower()}
        final_missing_section = "问题分析" not in final_text and "问题分析" in draft_text
        final_missing_targets = any(term in draft_markers and term not in final_markers for term in ("T01", "T02", "T03"))
        final_too_short = len(final_text) < max(1200, len(draft_text) * 0.65)
        if not final_text.strip() or final_missing_section or final_missing_targets or final_too_short:
            final.parent.mkdir(parents=True, exist_ok=True)
            final.write_text(draft_text.rstrip() + "\n", encoding="utf-8")
            result.update(
                {
                    "refreshed": True,
                    "reason": "final_submit_refreshed_from_latest_full_draft",
                    "draft_marker_count": len(draft_markers),
                    "final_marker_count_before": len(final_markers),
                }
            )
        else:
            result.update(
                {
                    "reason": "final_submit_already_consistent",
                    "draft_marker_count": len(draft_markers),
                    "final_marker_count_before": len(final_markers),
                }
            )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def validate_sandbox_contracts(workspace: Path) -> Dict[str, Any]:
    import validate_contracts

    original_root = validate_contracts.ROOT
    try:
        validate_contracts.configure_root(workspace)
        issues = validate_contracts.run_validation("final_export", write=True)
    finally:
        validate_contracts.configure_root(original_root)
    fail_count = sum(1 for issue in issues if issue.get("level") == "fail")
    warn_count = sum(1 for issue in issues if issue.get("level") == "warn")
    return {
        "status": "pass" if fail_count == 0 else "fail",
        "fail_count": fail_count,
        "warn_count": warn_count,
        "issue_count": len(issues),
        "issues": issues,
        "report": safe_rel(workspace / "11_review" / "contract_validation_report.json"),
    }


def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return {}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sandbox_stage_prompt_text(stage_id: str, formal_source: str, formal_text: str) -> str:
    overlay = f"""# Training Sandbox Prompt Backup: {stage_id}

Formal source prompt: `{formal_source}`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Preserve the locked problem topic throughout the sandbox run; do not drift to unrelated prior benchmark topics such as AQI or wine quality.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

"""
    return overlay + (formal_text or "[missing formal prompt]") + "\n"


def command_requires_external_api(cmd: Sequence[str]) -> bool:
    lowered = " ".join(str(part).replace("\\", "/").lower() for part in cmd)
    return "deepseek_agent_runner.py" in lowered


def append_stage_execution_rows(run_dir: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path = run_dir / "reports" / "stage_execution_manifest.csv"
    existing = read_csv_dict(path)
    merged = existing + [{field: row.get(field, "") for field in STAGE_EXECUTION_FIELDS} for row in rows]
    write_csv_dicts(path, merged, STAGE_EXECUTION_FIELDS)


def stage_rows_by_id(policy: Mapping[str, Any], workspace: Path) -> Dict[str, Dict[str, Any]]:
    return {str(row.get("stage_id") or ""): dict(row) for row in stage_prompt_rows(policy, workspace)}


def gap_dimension_for_blocker(run_dir: Path, row: Mapping[str, str]) -> str:
    note = str(row.get("notes") or "")
    validation_match = re.search(r"validation_item=([A-Za-z0-9_:-]+)", note)
    if validation_match:
        return f"validation:{validation_match.group(1)}"
    contract_match = re.search(r"contract_item=([A-Za-z0-9_:-]+)", note)
    if contract_match:
        return f"contract:{contract_match.group(1)}"
    match = re.search(r"from\s+(\S+)", note)
    gap_id = match.group(1) if match else ""
    for gap in read_csv_dict(run_dir / "reports" / "gap_report.csv"):
        if gap_id and str(gap.get("gap_id") or "") != gap_id:
            continue
        dimension = str(gap.get("dimension") or "")
        if dimension:
            return dimension
    text = " ".join(str(row.get(key) or "") for key in ("issue_summary", "proposed_action", "target_artifact")).lower()
    for dimension in GAP_STAGE_MAP:
        if dimension in text:
            return dimension
    if "contract" in text or "合同" in text:
        return "contract_binding"
    if "figure" in text or "图" in text:
        return "figure_density"
    return ""


def stages_for_blockers(run_dir: Path, blockers: Sequence[Mapping[str, str]], stage_rows: Mapping[str, Mapping[str, Any]]) -> List[str]:
    selected: List[str] = []
    for blocker in blockers:
        dimension = gap_dimension_for_blocker(run_dir, blocker)
        if dimension.startswith("validation:"):
            stages = VALIDATION_STAGE_MAP.get(dimension.split(":", 1)[1], ["paper_full"])
        elif dimension.startswith("contract:"):
            stages = CONTRACT_STAGE_MAP.get(dimension.split(":", 1)[1], ["paper_full", "final_export"])
        else:
            stages = GAP_STAGE_MAP.get(dimension, ["paper_full"])
        for stage in stages:
            if stage in stage_rows and stage not in selected:
                selected.append(stage)
    if not selected:
        return ["paper_full"]

    def stage_sort_key(stage_id: str) -> Tuple[int, str]:
        raw_order = stage_rows.get(stage_id, {}).get("stage_order", 999)
        try:
            return int(str(raw_order)), stage_id
        except (TypeError, ValueError):
            return 999, stage_id

    return sorted(selected, key=stage_sort_key)


def validation_issue_action(item: str, detail: str) -> Tuple[str, str]:
    actions = {
        "missing_training_enhancement_points": (
            "Create reports/training_enhancement_points.csv with at least system, prompt, and gate target_area rows.",
            "training_enhancement_points.csv exists and contains system/prompt/gate rows.",
        ),
        "missing_training_enhancement_markdown": (
            "Create reports/training_enhancement_points.md summarizing candidate workflow improvements.",
            "training_enhancement_points.md is non-empty.",
        ),
        "missing_submit_ready_training_artifact": (
            "Create the missing submit-ready training artifact, especially workspace/12_submission/final_submit_paper.md.",
            "final_submit_paper.md and final_submit_package.md are non-empty.",
        ),
        "training_final_paper_too_thin": (
            "Expand 12_submission/final_submit_paper.md from the latest full_draft with substantive problem analysis, model, results, validation, and conclusion sections.",
            "final_submit_paper.md has at least 2500 characters and at least seven sections.",
        ),
        "training_final_paper_missing_section_signal": (
            "Refresh final_submit_paper.md from a topic-aligned full_draft and include the missing required section signal.",
            "validate_agent_run.py no longer reports training_final_paper_missing_section_signal.",
        ),
        "training_topic_alignment_drift": (
            "Rewrite the paper and contracts to match the locked color-channel/concentration problem; remove AQI, wine-quality, or unrelated benchmark content.",
            "final_submit_paper.md mentions the locked problem markers such as color/RGB/concentration/T01-T03 and no unrelated topic markers.",
        ),
        "training_contract_empty": (
            "Populate the empty sandbox contract with rows bound to results, claims, or figures as required.",
            "Required contract files contain rows and validate_agent_run no longer reports training_contract_empty.",
        ),
        "training_figure_contract_missing_output": (
            "Add existing output_svg/output_png/output_pdf files for every figure_contract row.",
            "Each figure_contract row references at least one existing figure file.",
        ),
        "training_figure_contract_file_missing": (
            "Create the figure files referenced by figure_contract.csv or update the contract to existing files.",
            "All registered figure outputs exist in the sandbox workspace.",
        ),
        "training_figure_contract_missing_evidence_source": (
            "Add result_id or evidence_source for every figure_contract row and keep the cited figure file path registered.",
            "Every figure_contract row has result_id or evidence_source and an existing output path.",
        ),
        "training_paper_unregistered_figure_reference": (
            "Make paper figure references match figure_contract ids exactly and register each cited figure with an existing file.",
            "Every `图F###` paper reference has a matching figure_contract.csv row and existing output file.",
        ),
        "training_simulated_gate_log_incomplete": (
            "Write at least four simulated gate log rows for major sandbox gates.",
            "simulated_human_gate_log.csv has at least four rows.",
        ),
        "training_simulated_gate_has_formal_effect": (
            "Rewrite simulated gate log rows so formal_effect is exactly none.",
            "Every simulated gate row has formal_effect=none.",
        ),
        "training_review_scorecard_missing": (
            "Write 11_review/review_scorecard.csv for the current sandbox artifacts.",
            "review_scorecard.csv exists and contains current review rows.",
        ),
        "training_review_fail_unclosed": (
            "Resolve or close fail-level review scorecard items after applying the corresponding sandbox fixes.",
            "No review_scorecard row has severity/fail_level=fail unless status is closed/resolved/waived.",
        ),
        "training_review_score_below_threshold": (
            "Fix the underlying low-score artifacts first: result sources, figure files/contracts, paper sections, evidence bindings, and revision tasks; then rerun auto_review so scores rise above threshold.",
            "Every review_scorecard row is at least 85% of max_score, with supporting artifact fixes present.",
        ),
        "training_revision_task_unresolved": (
            "Close or resolve major/fail revision tasks only after the corresponding sandbox artifact fix is applied.",
            "All major/fail revision_tasks.csv rows have status closed/resolved/waived.",
        ),
    }
    return actions.get(
        item,
        (
            f"Resolve validation failure {item}: {detail}",
            f"validate_agent_run.py no longer reports {item}.",
        ),
    )


def contract_issue_action(item: str, detail: str) -> Tuple[str, str]:
    actions = {
        "figure_without_result_source": (
            "Bind each active figure to a result_id/evidence_source, or to claim_ids whose claims cite a result evidence_ref.",
            "validate_contracts.py no longer reports figure_without_result_source.",
        ),
        "figure_unknown_result": (
            "Update figure_contract.csv so every result_id exists in result_contract.csv.",
            "Every figure result_id is present in result_contract.csv.",
        ),
        "figure_file_missing": (
            "Create the referenced figure file or update figure_contract.csv to an existing output path.",
            "Every active figure_contract row references an existing output file.",
        ),
        "unsupported_claim": (
            "Bind each active claim to an existing result_id, figure_id, formula_id, citation_id, or evidence_ref.",
            "validate_contracts.py no longer reports unsupported_claim for claim_evidence_map.csv.",
        ),
        "claim_without_result_or_citation": (
            "Add result/citation/formula/figure evidence fields to every active claim.",
            "Every active claim has explicit evidence binding.",
        ),
        "citation_without_support_grade": (
            "Add support_grade for active citation_contract.csv rows, or remove citations that are not used by current claims.",
            "Active citation rows have a non-empty support_grade.",
        ),
        "citation_metadata_unverified": (
            "Verify citation metadata or mark unused citation rows inactive before final_export.",
            "Active citation rows have metadata_verified=true or are removed from active claims.",
        ),
        "review_score_below_threshold": (
            "Improve the underlying result sources, figures, paper, and evidence bindings before rerunning auto_review.",
            "review_scorecard.csv scores are at least 85% of max_score and the artifact fixes are present.",
        ),
        "review_fail_unclosed": (
            "Close or resolve fail-level review rows only after the corresponding sandbox fix is applied.",
            "No fail-level review scorecard row remains open.",
        ),
        "revision_task_unresolved": (
            "Close or resolve fail/major revision tasks after applying the corresponding sandbox fix.",
            "All fail/major revision tasks are closed/resolved/waived.",
        ),
        "empty_final_required_contract": (
            "Populate final required contracts before final_export.",
            "result, claim, and figure contracts are non-empty at final_export.",
        ),
        "result_without_source_file": (
            "Add source_file for frozen or cited result_contract.csv rows, pointing to a real reproducible result artifact.",
            "validate_contracts.py no longer reports result_without_source_file.",
        ),
        "result_metric_missing": (
            "Add metric_name/metric or equivalent metric label for result_contract.csv rows.",
            "Result contract rows include metric labels.",
        ),
        "result_value_missing": (
            "Add metric_value/value for result_contract.csv rows.",
            "Result contract rows include numeric or textual result values.",
        ),
    }
    return actions.get(
        item,
        (
            f"Resolve contract validation failure {item}: {detail}",
            f"validate_contracts.py no longer reports {item}.",
        ),
    )


def merge_validation_failures_into_queue(run_dir: Path, validation: Mapping[str, Any]) -> int:
    queue_path = run_dir / "reports" / "agent_revision_queue.csv"
    rows = read_csv_dict(queue_path)
    direct_fail_keys = {
        (str(issue.get("item") or ""), str(issue.get("detail") or ""))
        for issue in validation.get("issues") or []
        if str(issue.get("level") or "") == "fail" and str(issue.get("item") or "") not in VALIDATION_QUEUE_SKIP_ITEMS
    }
    changed = False
    for row in rows:
        status = str(row.get("status") or "").strip().lower()
        severity = str(row.get("severity") or "").strip().lower()
        match = re.search(r"validation_item=([A-Za-z0-9_:-]+)", str(row.get("notes") or ""))
        if status == "open" and severity in {"fail", "major"} and match:
            key = (match.group(1), str(row.get("issue_summary") or ""))
            if key not in direct_fail_keys:
                row["status"] = "resolved"
                row["human_decision"] = row.get("human_decision") or "auto_resolved_by_validation"
                row["notes"] = str(row.get("notes") or "") + ";resolved_by_current_validation"
                changed = True
    existing_keys = {
        (str(row.get("notes") or ""), str(row.get("target_artifact") or ""), str(row.get("issue_summary") or ""))
        for row in rows
        if str(row.get("status") or "").strip().lower() == "open"
    }
    added = 0
    for issue in validation.get("issues") or []:
        if str(issue.get("level") or "") != "fail":
            continue
        item = str(issue.get("item") or "")
        if item in VALIDATION_QUEUE_SKIP_ITEMS:
            continue
        detail = str(issue.get("detail") or "")
        target = str(issue.get("path") or "workspace")
        note = f"validation_item={item}"
        key = (note, target, detail)
        if key in existing_keys:
            continue
        action, acceptance = validation_issue_action(item, detail)
        added += 1
        task_number = len(rows) + 1
        rows.append(
            {
                "task_id": f"{run_dir.name}-VAL-{task_number:03d}",
                "run_id": run_dir.name,
                "iteration": "validation",
                "severity": "fail",
                "target_artifact": target,
                "issue_summary": detail,
                "proposed_action": action,
                "acceptance_check": acceptance,
                "status": "open",
                "human_decision": "",
                "notes": note,
            }
        )
        existing_keys.add(key)
    if added or changed:
        write_csv_dicts(queue_path, rows, QUEUE_FIELDS)
    return added


def merge_contract_failures_into_queue(run_dir: Path, contract_validation: Mapping[str, Any]) -> int:
    queue_path = run_dir / "reports" / "agent_revision_queue.csv"
    rows = read_csv_dict(queue_path)
    direct_fail_keys = {
        (str(issue.get("item") or ""), str(issue.get("detail") or ""))
        for issue in contract_validation.get("issues") or []
        if str(issue.get("level") or "") == "fail"
    }
    changed = False
    for row in rows:
        status = str(row.get("status") or "").strip().lower()
        severity = str(row.get("severity") or "").strip().lower()
        match = re.search(r"contract_item=([A-Za-z0-9_:-]+)", str(row.get("notes") or ""))
        if status == "open" and severity in {"fail", "major"} and match:
            key = (match.group(1), str(row.get("issue_summary") or ""))
            if key not in direct_fail_keys:
                row["status"] = "resolved"
                row["human_decision"] = row.get("human_decision") or "auto_resolved_by_contract_validation"
                row["notes"] = str(row.get("notes") or "") + ";resolved_by_current_contract_validation"
                changed = True
    existing_keys = {
        (str(row.get("notes") or ""), str(row.get("target_artifact") or ""), str(row.get("issue_summary") or ""))
        for row in rows
        if str(row.get("status") or "").strip().lower() == "open"
    }
    added = 0
    for issue in contract_validation.get("issues") or []:
        if str(issue.get("level") or "") != "fail":
            continue
        item = str(issue.get("item") or "")
        detail = str(issue.get("detail") or "")
        target = str(issue.get("path") or "14_contracts")
        note = f"contract_item={item}"
        key = (note, target, detail)
        if key in existing_keys:
            continue
        action, acceptance = contract_issue_action(item, detail)
        added += 1
        task_number = len(rows) + 1
        rows.append(
            {
                "task_id": f"{run_dir.name}-CONTRACT-{task_number:03d}",
                "run_id": run_dir.name,
                "iteration": "contract_validation",
                "severity": "fail",
                "target_artifact": target,
                "issue_summary": detail,
                "proposed_action": action,
                "acceptance_check": acceptance,
                "status": "open",
                "human_decision": "",
                "notes": note,
            }
        )
        existing_keys.add(key)
    if added or changed:
        write_csv_dicts(queue_path, rows, QUEUE_FIELDS)
    return added


def run_stage_agent_sequence(
    *,
    run_dir: Path,
    workspace: Path,
    policy: Mapping[str, Any],
    route_manifest: Mapping[str, Any],
    max_iterations: int,
    stages: Sequence[str],
    iteration: int,
    call_prefix: str,
    queue_path: Optional[Path] = None,
) -> Tuple[int, str, List[Dict[str, Any]]]:
    rows_by_id = stage_rows_by_id(policy, workspace)
    records: List[Dict[str, Any]] = []
    last_tail = ""
    for index, stage_id in enumerate(stages, start=1):
        stage_row = rows_by_id.get(stage_id, {"stage_order": index, "stage_id": stage_id})
        try:
            stage_order = int(str(stage_row.get("stage_order")))
        except (TypeError, ValueError):
            stage_order = index
        call_id = f"{call_prefix}_{stage_order:02d}_{stage_id}"
        prompt = write_stage_execution_prompt(
            run_dir,
            workspace,
            max_iterations,
            route_manifest,
            stage_id,
            stage_order,
            call_id,
            iteration,
            queue_path=queue_path,
        )
        log_path = run_dir / "logs" / f"agent_{call_id}.log"
        cmd = resolve_agent_command(policy, prompt, workspace, run_dir, "training_sandbox", max_iterations, stage=stage_id, call_id=call_id)
        started = now_local()
        rc, tail = run_agent_command(cmd, workspace, log_path, default_timeout(policy))
        finished = now_local()
        last_tail = tail
        record = {
            "call_id": call_id,
            "iteration": iteration,
            "stage_order": stage_order,
            "stage_id": stage_id,
            "prompt_path": safe_rel(prompt),
            "log_path": safe_rel(log_path),
            "exit_code": rc,
            "status": "pass" if rc == 0 else "fail",
            "started_at": started,
            "finished_at": finished,
            "notes": "",
        }
        records.append(record)
        append_stage_execution_rows(run_dir, [record])
        if rc != 0:
            return rc, last_tail, records
    return 0, last_tail, records


def stage_prompt_rows(policy: Mapping[str, Any], workspace: Path) -> List[Dict[str, Any]]:
    router_policy = load_yaml(workspace / "config" / "skill_router_policy.yaml")
    stage_policy = (router_policy.get("stage_identity_policy") or {})
    stages = [str(item) for item in (stage_policy.get("ordered_stages") or []) if str(item).strip()]
    prompt_files = stage_policy.get("stage_prompt_files") or {}
    if not stages:
        stages = [
            "latex_template",
            "intake",
            "eda",
            "task_analysis",
            "prior_retrieval",
            "model_route",
            "codegen",
            "results_freeze",
            "figures",
            "paper_draft",
            "paper_full",
            "auto_review",
            "revision",
            "polish",
            "compile",
            "final_export",
        ]

    rows: List[Dict[str, Any]] = []
    for index, stage in enumerate(stages):
        raw = str(prompt_files.get(stage) or "")
        path = workspace / raw if raw else workspace / "prompts" / "stages" / f"{stage}.md"
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        rows.append(
            {
                "stage_order": index,
                "stage_id": stage,
                "prompt_file": raw or safe_rel(path, workspace),
                "formal_prompt_file": raw or safe_rel(path, workspace),
                "sandbox_prompt_file": "",
                "sha256": sha256_text(text) if text else "",
                "formal_sha256": sha256_text(text) if text else "",
                "sandbox_sha256": "",
                "size_bytes": len(text.encode("utf-8")) if text else 0,
                "included_in_training": "yes" if text else "missing",
            }
        )
    return rows


def write_prompt_route_manifest(run_dir: Path, workspace: Path, policy: Mapping[str, Any]) -> Dict[str, Any]:
    rows = stage_prompt_rows(policy, workspace)
    sandbox_prompt_dir = workspace / "prompts" / "training_sandbox" / "stages"
    sandbox_prompt_dir.mkdir(parents=True, exist_ok=True)
    enriched_rows: List[Dict[str, Any]] = []
    for row in rows:
        formal_prompt = workspace / str(row.get("formal_prompt_file") or row.get("prompt_file") or "")
        formal_text = formal_prompt.read_text(encoding="utf-8", errors="ignore") if formal_prompt.exists() else ""
        stage_id = str(row.get("stage_id") or "")
        stage_order = int(row.get("stage_order") or 0)
        sandbox_rel = f"prompts/training_sandbox/stages/{stage_order:02d}_{stage_id}.md"
        sandbox_path = workspace / sandbox_rel
        sandbox_text = sandbox_stage_prompt_text(stage_id, str(row.get("formal_prompt_file") or ""), formal_text)
        sandbox_path.write_text(sandbox_text, encoding="utf-8")
        updated = dict(row)
        updated.update(
            {
                "prompt_file": sandbox_rel,
                "sandbox_prompt_file": sandbox_rel,
                "sandbox_sha256": sha256_text(sandbox_text),
                "sha256": sha256_text(sandbox_text),
                "size_bytes": len(sandbox_text.encode("utf-8")),
                "included_in_training": "yes" if formal_text else "missing",
            }
        )
        enriched_rows.append(updated)
    rows = enriched_rows
    csv_path = run_dir / "reports" / "prompt_route_manifest.csv"
    md_path = run_dir / "reports" / "prompt_route_manifest.md"
    bundle_path = run_dir / "reports" / "stage_prompt_bundle.md"
    write_csv_dicts(csv_path, rows, PROMPT_ROUTE_FIELDS)
    write_csv_dicts(workspace / "10_ai_logs" / "prompt_route_manifest.csv", rows, PROMPT_ROUTE_FIELDS)

    lines = [
        "# Training Prompt Route Manifest",
        "",
        f"- generated_at: {now_local()}",
        f"- global_contract: prompts/stage_prompt_contract.md",
        f"- stage_count: {len(rows)}",
        "",
        "The training sandbox follows sandbox-specific prompt backups derived from the formal prompt system. Formal prompt files remain separate; useful training enhancement points may later be promoted only as suggestion-only formal workflow changes after validation and human gates.",
        "",
        "| order | stage | sandbox prompt | formal source | status |",
        "|---:|---|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['stage_order']} | {row['stage_id']} | {row['sandbox_prompt_file']} | {row['formal_prompt_file']} | {row['included_in_training']} |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (workspace / "10_ai_logs" / "prompt_route_manifest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    bundle_lines = [
        "# Formal Stage Prompt Bundle For Full-Agent Training",
        "",
        "This file is assembled from sandbox prompt backups derived from the normal competition prompts. The formal source prompt for each stage is listed; sandbox overlays are allowed only inside training runs.",
        "",
        "## Global Contract",
        "",
        "Source: `prompts/stage_prompt_contract.md`",
        "",
    ]
    global_contract = workspace / "prompts" / "stage_prompt_contract.md"
    bundle_lines.append(global_contract.read_text(encoding="utf-8", errors="ignore") if global_contract.exists() else "[missing prompts/stage_prompt_contract.md]")
    for row in rows:
        prompt_file = workspace / str(row.get("sandbox_prompt_file") or row.get("prompt_file") or "")
        bundle_lines += [
            "",
            f"## Stage {row.get('stage_order')}: {row.get('stage_id')}",
            "",
            f"Sandbox source: `{row.get('sandbox_prompt_file')}`",
            f"Formal source: `{row.get('formal_prompt_file')}`",
            "",
        ]
        bundle_lines.append(prompt_file.read_text(encoding="utf-8", errors="ignore") if prompt_file.exists() else "[missing stage prompt]")
    bundle_text = "\n".join(bundle_lines) + "\n"
    bundle_path.write_text(bundle_text, encoding="utf-8")
    (workspace / "10_ai_logs" / "stage_prompt_bundle.md").write_text(bundle_text, encoding="utf-8")
    return {
        "csv_path": safe_rel(csv_path),
        "markdown_path": safe_rel(md_path),
        "bundle_path": safe_rel(bundle_path),
        "stage_count": len(rows),
        "missing_count": sum(1 for row in rows if row.get("included_in_training") != "yes"),
        "prompt_set": "training_sandbox_backup",
    }


def feedback_policy(policy: Mapping[str, Any]) -> Dict[str, Any]:
    formal = policy.get("formal_assist") or {}
    cfg = formal.get("training_feedback") or {}
    return {
        "enabled": bool(cfg.get("enabled", True)),
        "source": str(cfg.get("source") or "latest_validated_training_sandbox"),
        "bundle_dir": str(cfg.get("bundle_dir") or "15_iteration_memory/training_feedback"),
        "max_items": int(cfg.get("max_items") or 12),
        "require_validation_pass": bool(cfg.get("require_validation_pass", True)),
        "require_copy_risk_pass": bool(cfg.get("require_copy_risk_pass", True)),
        "suggestion_only": bool(cfg.get("suggestion_only", True)),
    }


def latest_training_run_id() -> str:
    rows = read_csv_dict(INDEX_PATH)
    rows = [row for row in rows if row.get("mode") == "training_sandbox"]
    rows.sort(key=lambda row: row.get("created_at", ""), reverse=True)
    for row in rows:
        run_id = str(row.get("run_id") or "")
        if not run_id:
            continue
        run_dir = AGENT_RUNS_ROOT / run_id
        validation_status = str(read_json(run_dir / "reports" / "agent_run_validation.json").get("status") or "").lower()
        if validation_status == "pass" and not blocking_queue_rows(run_dir) and copy_risk_decision(run_dir) == "pass":
            return run_id
    return str(rows[0].get("run_id") or "") if rows else ""


def copy_risk_decision(run_dir: Path) -> str:
    rows = read_csv_dict(run_dir / "reports" / "copy_risk_report.csv")
    if not rows:
        return "missing"
    decisions = {str(row.get("decision") or "").lower() for row in rows}
    if "fail" in decisions:
        return "fail"
    if "pass" in decisions:
        return "pass"
    return sorted(decisions)[0] if decisions else "unknown"


def blocking_queue_rows(run_dir: Path) -> List[Dict[str, str]]:
    rows = read_csv_dict(run_dir / "reports" / "agent_revision_queue.csv")
    blockers: List[Dict[str, str]] = []
    for row in rows:
        status = str(row.get("status") or "").strip().lower()
        severity = str(row.get("severity") or "").strip().lower()
        if status == "open" and severity in {"fail", "major"}:
            blockers.append(row)
    return blockers


def queue_issue_keys(rows: Sequence[Mapping[str, str]]) -> set[str]:
    keys: set[str] = set()
    for row in rows:
        key = "|".join(
            [
                str(row.get("severity") or ""),
                str(row.get("target_artifact") or ""),
                str(row.get("issue_summary") or ""),
                str(row.get("proposed_action") or ""),
                str(row.get("notes") or ""),
            ]
        )
        keys.add(key)
    return keys


def normalize_feedback_target(value: str, run_id: str) -> str:
    normalized = str(value or "").replace("\\", "/")
    markers = [
        f"16_learning/agent_runs/{run_id}/workspace/",
        f"{(AGENT_RUNS_ROOT / run_id / 'workspace').as_posix()}/",
        "workspace/",
    ]
    for marker in markers:
        if normalized.startswith(marker):
            return normalized[len(marker) :]
    return normalized


def training_enhancement_rows(run_dir: Path) -> List[Dict[str, str]]:
    rows = read_csv_dict(run_dir / "reports" / "training_enhancement_points.csv")
    return [
        row
        for row in rows
        if str(row.get("status") or "candidate").strip().lower() not in {"rejected", "discarded", "closed"}
    ]


def training_enhancement_missing_areas(rows: Sequence[Mapping[str, str]]) -> List[str]:
    required = {"system", "prompt", "gate"}
    areas = {str(row.get("target_area") or "").strip().lower() for row in rows}
    return sorted(required - areas)


def first_row_text(row: Mapping[str, Any], *keys: str) -> str:
    for key in keys:
        value = str(row.get(key) or "").strip()
        if value:
            return value
    return ""


def enhancement_feedback_severity(row: Mapping[str, Any]) -> str:
    severity = first_row_text(row, "severity", "fail_level").lower()
    if severity:
        return severity
    priority = first_row_text(row, "priority").lower()
    if priority in {"critical", "high"}:
        return "major"
    if priority in {"medium", "mid"}:
        return "minor"
    return "suggestion"


def feedback_target_from_enhancement(row: Mapping[str, str]) -> str:
    area = str(row.get("target_area") or "").strip().lower() or "workflow"
    if area == "prompt":
        return "formal_prompt:training_sandbox_candidate"
    if area == "gate":
        return "workflow_gate:training_sandbox_candidate"
    return f"workflow:{area}"


def run_feedback_eligibility(run_id: str, cfg: Mapping[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
    reasons: List[str] = []
    run_dir = AGENT_RUNS_ROOT / run_id
    if not run_id:
        return False, ["no training run selected"], {}
    if not run_dir.exists():
        return False, [f"training run not found: {run_id}"], {}
    manifest = load_yaml(run_dir / "run_manifest.yaml")
    status = str(manifest.get("status") or "")
    status_is_terminal = status in {"completed", "completed_with_open_gaps", "agent_passed", "iteration_passed"}
    if not status_is_terminal:
        reasons.append(f"run status is {status or 'unknown'}, not terminal")

    queue_path = run_dir / "reports" / "agent_revision_queue.csv"
    queue = read_csv_dict(queue_path)
    blockers = blocking_queue_rows(run_dir)
    if blockers:
        reasons.append(f"agent_revision_queue.csv has {len(blockers)} open fail/major item(s)")

    enhancement_rows = training_enhancement_rows(run_dir)
    missing_enhancement_areas = training_enhancement_missing_areas(enhancement_rows)
    if missing_enhancement_areas:
        reasons.append("training_enhancement_points.csv missing target_area: " + ",".join(missing_enhancement_areas))
    if not queue and not enhancement_rows:
        reasons.append("no queue corrections or validated training enhancement candidates found")

    validation = read_json(run_dir / "reports" / "agent_run_validation.json")
    validation_status = str(validation.get("status") or "missing").lower()
    if cfg.get("require_validation_pass") and validation_status != "pass":
        reasons.append(f"agent validation status is {validation_status}")

    copy_decision = copy_risk_decision(run_dir)
    if cfg.get("require_copy_risk_pass") and copy_decision != "pass":
        reasons.append(f"copy risk decision is {copy_decision}")

    meta = {
        "run_dir": safe_rel(run_dir),
        "manifest_status": status,
        "validation_status": validation_status,
        "copy_risk_decision": copy_decision,
        "queue_count": len(queue),
        "blocking_queue_count": len(blockers),
        "training_enhancement_count": len(enhancement_rows),
        "training_enhancement_missing_areas": missing_enhancement_areas,
    }
    return not reasons, reasons, meta


def training_feedback_prompt_section(payload: Mapping[str, Any], rows: Sequence[Mapping[str, Any]]) -> str:
    if payload.get("status") != "ready":
        reason_text = "; ".join(str(item) for item in payload.get("reasons", []) or []) or "no eligible training feedback"
        return (
            "\n## Training Sandbox Feedback\n\n"
            f"No validated training feedback was attached. Reason: {reason_text}.\n"
        )

    lines = [
        "## Training Sandbox Feedback",
        "",
        f"- source_run_id: {payload.get('source_run_id')}",
        f"- feedback_bundle: {payload.get('markdown_path')}",
        f"- validation_status: {payload.get('validation_status')}",
        f"- copy_risk_decision: {payload.get('copy_risk_decision')}",
        "- safety: suggestion_only; do not auto-apply to protected formal deliverables.",
        "",
        "Use these rows as candidate workflow, prompt, and gate improvements only. If an item is accepted, record it through the formal revision task flow and contract checks before changing formal prompts, paper, result, figure, formula, or submission artifacts.",
        "",
    ]
    for row in rows:
        lines += [
            f"- [{row.get('severity')}] {row.get('feedback_id')}",
            f"  target: {row.get('formal_target')}",
            f"  issue: {row.get('issue_summary')}",
            f"  proposed_action: {row.get('proposed_action')}",
            f"  acceptance_check: {row.get('acceptance_check')}",
        ]
    return "\n" + "\n".join(lines) + "\n"


def build_training_feedback_bundle(policy: Mapping[str, Any], requested_run_id: str, formal_stage: str) -> Dict[str, Any]:
    cfg = feedback_policy(policy)
    if not cfg.get("enabled"):
        return {
            "status": "disabled",
            "requested_run_id": requested_run_id,
            "source_run_id": "",
            "reasons": ["training feedback is disabled by policy"],
            "prompt_section": "",
        }

    run_id = requested_run_id or latest_training_run_id()
    eligible, reasons, meta = run_feedback_eligibility(run_id, cfg)
    if not eligible:
        payload = {
            "status": "not_attached",
            "requested_run_id": requested_run_id,
            "source_run_id": run_id,
            "reasons": reasons,
            **meta,
        }
        payload["prompt_section"] = training_feedback_prompt_section(payload, [])
        return payload

    run_dir = AGENT_RUNS_ROOT / run_id
    queue = read_csv_dict(run_dir / "reports" / "agent_revision_queue.csv")
    enhancement_rows = training_enhancement_rows(run_dir)
    max_items = int(cfg.get("max_items") or 12)
    feedback_rows: List[Dict[str, Any]] = []
    severity_order = {"fail": 0, "major": 1, "minor": 2, "suggestion": 3}
    if enhancement_rows:
        enhancement_rows.sort(
            key=lambda row: (
                severity_order.get(enhancement_feedback_severity(row), 99),
                str(row.get("target_area") or ""),
                first_row_text(row, "enhancement_id", "id"),
            )
        )
        for index, row in enumerate(enhancement_rows[:max_items], start=1):
            evidence = first_row_text(row, "evidence", "sandbox_target", "target_area")
            target_area = str(row.get("target_area") or "").strip().lower()
            proposed_change = first_row_text(row, "proposed_change", "suggestion", "proposed_action")
            rationale = first_row_text(row, "issue_summary", "rationale", "notes")
            acceptance_check = first_row_text(row, "acceptance_check", "validation_check")
            if not acceptance_check:
                acceptance_check = "Human gate, contract validation, and stage-state control approve this suggestion before formal adoption."
            feedback_rows.append(
                {
                    "feedback_id": f"{run_id}-FB-{index:03d}",
                    "source_task_id": first_row_text(row, "enhancement_id", "id"),
                    "source_run_id": run_id,
                    "formal_stage": formal_stage,
                    "severity": enhancement_feedback_severity(row),
                    "formal_target": feedback_target_from_enhancement(row),
                    "sandbox_target": evidence,
                    "issue_summary": f"validated training enhancement ({target_area or 'workflow'}): {rationale or proposed_change}",
                    "proposed_action": proposed_change,
                    "acceptance_check": acceptance_check,
                    "status": "candidate",
                    "safety_note": "suggestion_only; may sync to formal workflow or prompt set only after human gate, contract validation, and stage-state control",
                }
            )
    else:
        queue.sort(key=lambda row: (severity_order.get(str(row.get("severity") or ""), 99), str(row.get("task_id") or "")))
        for index, row in enumerate(queue[:max_items], start=1):
            sandbox_target = str(row.get("target_artifact") or "")
            feedback_rows.append(
                {
                    "feedback_id": f"{run_id}-FB-{index:03d}",
                    "source_task_id": row.get("task_id", ""),
                    "source_run_id": run_id,
                    "formal_stage": formal_stage,
                    "severity": row.get("severity", ""),
                    "formal_target": normalize_feedback_target(sandbox_target, run_id),
                    "sandbox_target": sandbox_target,
                    "issue_summary": row.get("issue_summary", ""),
                    "proposed_action": row.get("proposed_action", ""),
                    "acceptance_check": row.get("acceptance_check", ""),
                    "status": "candidate",
                    "safety_note": "suggestion_only; requires human gate, revision task trace, and contract validation before formal changes",
                }
            )

    bundle_root = ROOT / str(cfg.get("bundle_dir") or "15_iteration_memory/training_feedback")
    bundle_root.mkdir(parents=True, exist_ok=True)
    csv_path = bundle_root / f"{run_id}_feedback.csv"
    md_path = bundle_root / f"{run_id}_feedback.md"
    write_csv_dicts(csv_path, feedback_rows, TRAINING_FEEDBACK_FIELDS)
    lines = [
        "# Training Sandbox Feedback Bundle",
        "",
        f"- generated_at: {now_local()}",
        "- status: suggestion_only",
        f"- source_run_id: {run_id}",
        f"- formal_stage: {formal_stage}",
        f"- validation_status: {meta.get('validation_status')}",
        f"- copy_risk_decision: {meta.get('copy_risk_decision')}",
        f"- csv: {safe_rel(csv_path)}",
        "",
        "These rows are validated training-sandbox enhancement candidates. They are not formal facts and must pass the normal revision, contract, and human-gate controls before changing formal prompts or protected artifacts.",
        "",
        "## Candidate Corrections",
        "",
    ]
    for row in feedback_rows:
        lines += [
            f"- [{row['severity']}] `{row['formal_target']}`",
            f"  - issue: {row['issue_summary']}",
            f"  - proposed_action: {row['proposed_action']}",
            f"  - acceptance_check: {row['acceptance_check']}",
        ]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    payload = {
        "status": "ready",
        "requested_run_id": requested_run_id,
        "source_run_id": run_id,
        "csv_path": safe_rel(csv_path),
        "markdown_path": safe_rel(md_path),
        "item_count": len(feedback_rows),
        **meta,
    }
    payload["prompt_section"] = training_feedback_prompt_section(payload, feedback_rows)
    return payload


def run_training_sandbox(args: argparse.Namespace, policy: Mapping[str, Any]) -> int:
    ensure_run_root()
    run_id = args.run_id or make_run_id("training_sandbox")
    run_dir = AGENT_RUNS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "reports").mkdir(exist_ok=True)
    (run_dir / "logs").mkdir(exist_ok=True)
    snapshot = write_protected_snapshot(run_dir, policy)
    workspace = prepare_sandbox_workspace(run_dir, Path(args.problem) if args.problem else None, policy)
    environment_diagnostics = write_environment_diagnostics(run_dir)
    max_iterations = args.max_iterations or int(((policy.get("training_sandbox") or {}).get("max_iterations")) or 3)
    route_manifest = write_prompt_route_manifest(run_dir, workspace, policy)
    prompt = write_training_prompt(run_dir, workspace, max_iterations, route_manifest)
    stage_rows = [row for row in stage_prompt_rows(policy, workspace) if row.get("included_in_training") == "yes"]
    initial_stages = [str(row.get("stage_id") or "") for row in stage_rows if str(row.get("stage_id") or "")]
    stage_execution_enabled = bool((policy.get("agent_executor") or {}).get("stage_execution", True))
    manifest = write_manifest(
        run_dir,
        {
            "run_id": run_id,
            "mode": "training_sandbox",
            "status": "created",
            "created_at": now_local(),
            "workspace": safe_rel(workspace),
            "problem": args.problem,
            "max_iterations": max_iterations,
            "formal_protected_snapshot": safe_rel(snapshot),
            "agent_prompt": safe_rel(prompt),
            "prompt_route_manifest": route_manifest,
            "environment_diagnostics": safe_rel(environment_diagnostics),
            "stage_execution_enabled": stage_execution_enabled,
            "training_required_outputs": [
                "reports/training_enhancement_points.csv",
                "reports/training_enhancement_points.md",
                "workspace/09_paper/full_draft.md",
                "workspace/12_submission/final_submit_paper.md",
                "workspace/12_submission/final_submit_package.md",
            ],
        },
    )

    cmd = resolve_agent_command(
        policy,
        prompt,
        workspace,
        run_dir,
        "training_sandbox",
        max_iterations,
        stage=initial_stages[0] if initial_stages else "",
        call_id="initial_probe",
    )
    external_cfg = policy.get("external_api") or {}
    external_requires_consent = bool(external_cfg.get("requires_explicit_consent", False))
    if cmd and command_requires_external_api(cmd) and external_requires_consent and not bool(args.external_api_approved):
        status = "needs_external_api_consent"
        update_status(
            run_dir,
            status,
            {
                "agent_command_present": True,
                "external_api_consent_required": True,
                "external_api_consent_scope": "training sandbox problem, prompts, workspace context",
            },
        )
        append_run_index(run_id, "training_sandbox", status, workspace, manifest, run_dir / "reports" / "full_gap_report.md", "external API consent required")
        print(json.dumps({"run_id": run_id, "status": status, "reason": "external_api_consent_required"}, ensure_ascii=False, indent=2))
        return 1
    if args.dry_run:
        status = "dry_run"
        update_status(run_dir, status, {"agent_command_present": bool(cmd), "dry_run": True})
    elif not cmd:
        status = "needs_agent_executor"
        update_status(run_dir, status, {"agent_command_present": False, "fallback": args.fallback})
    else:
        if stage_execution_enabled:
            rc, tail, stage_records = run_stage_agent_sequence(
                run_dir=run_dir,
                workspace=workspace,
                policy=policy,
                route_manifest=route_manifest,
                max_iterations=max_iterations,
                stages=initial_stages,
                iteration=1,
                call_prefix="initial",
            )
            initial_extra: Dict[str, Any] = {"initial_stage_call_count": len(stage_records)}
        else:
            rc, tail = run_agent_command(cmd, workspace, run_dir / "logs" / "agent_initial.log", default_timeout(policy))
            initial_extra = {}
        status = "agent_passed" if rc == 0 else "agent_failed"
        initial_final_refresh = refresh_training_final_submit(workspace)
        initial_gate_normalization = normalize_training_gate_log(workspace)
        initial_synced_reports = sync_workspace_reports(run_dir, workspace)
        update_status(
            run_dir,
            status,
            {
                "agent_command_present": True,
                "initial_exit_code": rc,
                "initial_log_tail": tail,
                "initial_final_refresh": initial_final_refresh,
                "initial_gate_normalization": initial_gate_normalization,
                "initial_synced_reports": initial_synced_reports,
                **initial_extra,
            },
        )
        if rc != 0:
            benchmark = benchmark_run(run_id)
            validation = validate_run(run_id)
            append_run_index(run_id, "training_sandbox", status, workspace, manifest, run_dir / "reports" / "full_gap_report.md", "agent command failed")
            print(json.dumps({"run_id": run_id, "status": status, "benchmark": benchmark, "validation": validation}, ensure_ascii=False, indent=2))
            return 1

    benchmark = benchmark_run(run_id)
    validation_for_queue = validate_run(run_id)
    validation_queue_added = merge_validation_failures_into_queue(run_dir, validation_for_queue)
    contract_for_queue = validate_sandbox_contracts(workspace)
    contract_queue_added = merge_contract_failures_into_queue(run_dir, contract_for_queue)
    if validation_queue_added or contract_queue_added:
        update_status(
            run_dir,
            "validation_queue_seeded",
            {"initial_validation_queue_added": validation_queue_added, "initial_contract_queue_added": contract_queue_added},
        )

    no_improvement_streak = 0
    iteration_stop_reason = ""
    if cmd and not args.dry_run and status == "agent_passed":
        for iteration in range(2, max_iterations + 1):
            blockers_before = blocking_queue_rows(run_dir)
            if not blockers_before:
                iteration_stop_reason = "blocking_queue_cleared"
                break
            before_keys = queue_issue_keys(blockers_before)
            iter_prompt = write_iteration_prompt(run_dir, workspace, iteration)
            if stage_execution_enabled:
                stage_targets = stages_for_blockers(run_dir, blockers_before, stage_rows_by_id(policy, workspace))
                rc, tail, iter_records = run_stage_agent_sequence(
                    run_dir=run_dir,
                    workspace=workspace,
                    policy=policy,
                    route_manifest=route_manifest,
                    max_iterations=max_iterations,
                    stages=stage_targets,
                    iteration=iteration,
                    call_prefix=f"iteration_{iteration:02d}",
                    queue_path=run_dir / "reports" / "agent_revision_queue.csv",
                )
                iteration_extra: Dict[str, Any] = {
                    f"iteration_{iteration}_stage_targets": stage_targets,
                    f"iteration_{iteration}_stage_call_count": len(iter_records),
                }
            else:
                iter_cmd = resolve_agent_command(policy, iter_prompt, workspace, run_dir, "training_sandbox", max_iterations)
                rc, tail = run_agent_command(iter_cmd, workspace, run_dir / "logs" / f"agent_iteration_{iteration:02d}.log", default_timeout(policy))
                iteration_extra = {}
            status = "iteration_failed" if rc else "agent_passed"
            iteration_final_refresh = refresh_training_final_submit(workspace)
            iteration_gate_normalization = normalize_training_gate_log(workspace)
            iteration_synced_reports = sync_workspace_reports(run_dir, workspace)
            update_status(
                run_dir,
                "iteration_failed" if rc else "iteration_passed",
                {
                    f"iteration_{iteration}_exit_code": rc,
                    f"iteration_{iteration}_log_tail": tail,
                    f"iteration_{iteration}_blocking_queue_before": len(blockers_before),
                    f"iteration_{iteration}_final_refresh": iteration_final_refresh,
                    f"iteration_{iteration}_gate_normalization": iteration_gate_normalization,
                    f"iteration_{iteration}_synced_reports": iteration_synced_reports,
                    **iteration_extra,
                },
            )
            benchmark = benchmark_run(run_id)
            validation_for_queue = validate_run(run_id)
            validation_queue_added = merge_validation_failures_into_queue(run_dir, validation_for_queue)
            contract_for_queue = validate_sandbox_contracts(workspace)
            contract_queue_added = merge_contract_failures_into_queue(run_dir, contract_for_queue)
            blockers_after = blocking_queue_rows(run_dir)
            after_keys = queue_issue_keys(blockers_after)
            if blockers_after and after_keys == before_keys:
                no_improvement_streak += 1
            else:
                no_improvement_streak = 0
            update_status(
                run_dir,
                "iteration_failed" if rc else "iteration_passed",
                {
                    f"iteration_{iteration}_blocking_queue_after": len(blockers_after),
                    f"iteration_{iteration}_no_improvement_streak": no_improvement_streak,
                    f"iteration_{iteration}_validation_queue_added": validation_queue_added,
                    f"iteration_{iteration}_contract_queue_added": contract_queue_added,
                },
            )
            if rc != 0:
                iteration_stop_reason = "agent_iteration_failed"
                break
            if not blockers_after:
                iteration_stop_reason = "blocking_queue_cleared"
                break
            if no_improvement_streak >= 2:
                iteration_stop_reason = "same_blocking_gap_not_improving"
                break

    final_refresh = refresh_training_final_submit(workspace)
    final_gate_normalization = normalize_training_gate_log(workspace)
    draft_path, draft_status = find_or_build_draft(workspace)
    copy_risk_payload: Dict[str, Any] = {"copy_risk": "skipped_no_draft"}
    if draft_path.exists() and draft_status != "missing":
        copy_csv, copy_md, copy_rows = write_run_copy_risk(run_dir, draft_path, policy)
        copy_risk_payload = {
            "copy_risk": copy_rows[0].get("decision"),
            "copy_risk_report": safe_rel(copy_csv),
            "copy_risk_markdown": safe_rel(copy_md),
        }

    pre_final_validation = validate_run(run_id)
    pre_final_validation_queue_added = merge_validation_failures_into_queue(run_dir, pre_final_validation)
    pre_final_contract_validation = validate_sandbox_contracts(workspace)
    pre_final_contract_queue_added = merge_contract_failures_into_queue(run_dir, pre_final_contract_validation)
    final_blockers = blocking_queue_rows(run_dir)
    final_status = status
    if status == "agent_passed":
        final_status = "completed" if not final_blockers else "completed_with_open_gaps"
    update_status(
        run_dir,
        final_status,
        {
            "benchmark": benchmark,
            "blocking_queue_count": len(final_blockers),
            "iteration_stop_reason": iteration_stop_reason or ("blocking_queue_open" if final_blockers else "blocking_queue_cleared"),
            "final_refresh": final_refresh,
            "final_gate_normalization": final_gate_normalization,
            "pre_final_validation_queue_added": pre_final_validation_queue_added,
            "pre_final_contract_queue_added": pre_final_contract_queue_added,
            **copy_risk_payload,
        },
    )
    validation = validate_run(run_id)
    contract_validation = validate_sandbox_contracts(workspace)
    if contract_validation.get("fail_count"):
        final_status = "completed_with_contract_issues" if final_status == "completed" else final_status
        update_status(run_dir, final_status, {"contract_validation": contract_validation})
    else:
        update_status(run_dir, final_status, {"contract_validation": contract_validation})
    append_run_index(run_id, "training_sandbox", final_status, workspace, manifest, run_dir / "reports" / "full_gap_report.md")
    print(json.dumps({"run_id": run_id, "status": final_status, "benchmark": benchmark, "validation": validation, "contract_validation": contract_validation}, ensure_ascii=False, indent=2))
    return 0 if not validation.get("fail_count") and not contract_validation.get("fail_count") else 1


def formal_stage_prompt(current_stage: str, pending_gate: str, stage_prompt_text: str, training_feedback_text: str = "") -> str:
    return f"""# Formal Assist Task

You are assisting the formal deep_sequential workflow.

Current stage: `{current_stage}`
Pending gate before run: `{pending_gate or 'none'}`

Rules:
- Do not run `--stage all`.
- Do not call `scripts/confirm_gate.py`.
- Use only the current stage path through `python scripts/run_current_stage.py --stage current`.
- Stop immediately if a pending gate appears.
- Do not bypass contract validation.
{training_feedback_text}

Stage prompt:

```markdown
{stage_prompt_text}
```
"""


def resolve_stage_prompt_file(current_stage: str) -> Path:
    direct = ROOT / "prompts" / "stages" / f"{current_stage}.md"
    if direct.exists():
        return direct
    matches = sorted((ROOT / "prompts" / "stages").glob(f"*_{current_stage}.md"))
    return matches[0] if matches else direct


def run_formal_assist(args: argparse.Namespace, policy: Mapping[str, Any]) -> int:
    ensure_run_root()
    run_id = args.run_id or make_run_id("formal_assist")
    run_dir = AGENT_RUNS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "reports").mkdir(exist_ok=True)
    (run_dir / "logs").mkdir(exist_ok=True)
    state_before = read_state()
    current_stage = str(state_before.get("current_stage") or "")
    pending_gate = str(state_before.get("pending_gate") or "")
    prompt_file = resolve_stage_prompt_file(current_stage)
    stage_prompt_text = prompt_file.read_text(encoding="utf-8", errors="ignore") if prompt_file.exists() else ""
    feedback = (
        {
            "status": "disabled",
            "requested_run_id": args.feedback_run_id,
            "source_run_id": "",
            "reasons": ["disabled by --no-training-feedback"],
            "prompt_section": "",
        }
        if args.no_training_feedback
        else build_training_feedback_bundle(policy, args.feedback_run_id, current_stage)
    )
    prompt = run_dir / "formal_agent_prompt.md"
    prompt.write_text(
        formal_stage_prompt(current_stage, pending_gate, stage_prompt_text, str(feedback.get("prompt_section") or "")),
        encoding="utf-8",
    )
    manifest = write_manifest(
        run_dir,
        {
            "run_id": run_id,
            "mode": "formal_assist",
            "status": "created",
            "created_at": now_local(),
            "formal_root": safe_rel(ROOT),
            "current_stage_before": current_stage,
            "pending_gate_before": pending_gate,
            "agent_prompt": safe_rel(prompt),
            "training_feedback": {key: value for key, value in feedback.items() if key != "prompt_section"},
        },
    )
    cmd = resolve_agent_command(policy, prompt, ROOT, run_dir, "formal_assist", 1)
    if args.dry_run:
        status = "dry_run"
        update_status(run_dir, status, {"agent_command_present": bool(cmd), "dry_run": True})
    elif not cmd:
        status = "needs_agent_executor"
        update_status(run_dir, status, {"agent_command_present": False, "fallback": args.fallback})
    else:
        rc, tail = run_agent_command(cmd, ROOT, run_dir / "logs" / "formal_agent.log", default_timeout(policy))
        status = "agent_passed" if rc == 0 else "agent_failed"
        update_status(run_dir, status, {"exit_code": rc, "log_tail": tail})

    state_after = read_state()
    report = run_dir / "reports" / "formal_assist_report.md"
    lines = [
        "# Formal Assist Report",
        "",
        f"- run_id: {run_id}",
        f"- status: {status}",
        f"- current_stage_before: {current_stage}",
        f"- pending_gate_before: {pending_gate or 'none'}",
        f"- current_stage_after: {state_after.get('current_stage')}",
        f"- pending_gate_after: {state_after.get('pending_gate') or 'none'}",
        "",
        "Formal assist never confirms human gates. If `pending_gate_after` is not none, human review is required.",
    ]
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    update_status(run_dir, status, {"formal_assist_report": safe_rel(report), "pending_gate_after": state_after.get("pending_gate")})
    append_run_index(run_id, "formal_assist", status, ROOT, manifest, report)
    print(json.dumps({"run_id": run_id, "status": status, "report": safe_rel(report)}, ensure_ascii=False, indent=2))
    return 0 if status != "agent_failed" else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Run agent-mode training sandbox or formal assist.")
    parser.add_argument("--mode", choices=["training_sandbox", "formal_assist"], default="")
    parser.add_argument("--problem", default="00_problem/problem_statement.md")
    parser.add_argument("--max-iterations", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--fallback", default="prompt_bundle")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--feedback-run-id", default="", help="Training sandbox run_id to attach as formal-assist feedback.")
    parser.add_argument("--no-training-feedback", action="store_true", help="Do not attach training sandbox feedback to formal_assist prompts.")
    parser.add_argument("--external-api-approved", action="store_true", help="Confirm this run may send sandbox problem, prompts, and context to the configured external API.")
    args = parser.parse_args()

    policy = read_agent_policy()
    mode = args.mode or str(policy.get("default_mode") or "training_sandbox")
    if mode == "training_sandbox":
        raise SystemExit(run_training_sandbox(args, policy))
    if mode == "formal_assist":
        raise SystemExit(run_formal_assist(args, policy))
    raise SystemExit(f"[FAIL] unknown mode: {mode}")


if __name__ == "__main__":
    main()
