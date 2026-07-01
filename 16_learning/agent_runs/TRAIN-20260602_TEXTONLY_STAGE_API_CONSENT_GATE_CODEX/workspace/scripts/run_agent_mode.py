from __future__ import annotations

import argparse
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
from benchmark_agent_run import benchmark_run, find_or_build_draft
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
    "sha256",
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
    "contract_binding": ["results_freeze", "paper_full"],
    "figure_density": ["figures", "paper_full"],
    "validation_completeness": ["results_freeze", "paper_full"],
    "structure_depth": ["paper_full"],
    "formula_and_model_detail": ["paper_full"],
}


def write_training_prompt(run_dir: Path, workspace: Path, max_iterations: int, route_manifest: Mapping[str, Any]) -> Path:
    prompt = workspace / "agent_prompt.md"
    text = f"""# Full-Agent Training Sandbox Wrapper

You are operating inside a sandbox workspace, not the formal project root.

Workspace: `{workspace}`
Max iterations: {max_iterations}
Prompt route manifest: `{route_manifest.get('markdown_path')}`
Prompt route CSV: `{route_manifest.get('csv_path')}`
Formal stage prompt bundle: `{route_manifest.get('bundle_path')}`

This wrapper is not a replacement prompt. The actual training route is the normal competition route:

1. Global prompt contract: `prompts/stage_prompt_contract.md`
2. Stage prompts: `prompts/stages/00_*.md` through `prompts/stages/15_*.md`
3. Stage order and prompt file mapping: the prompt route manifest above
4. Exact assembled formal prompts: the stage prompt bundle above

Full-agent training rules:
- Reuse the exact formal stage prompts. Do not invent a separate training-stage prompt.
- Walk the 16 stage prompts in deep_sequential order inside the sandbox.
- A human gate in a formal stage becomes a simulated sandbox gate, not a formal confirmation. Record each simulated gate in `11_review/simulated_human_gate_log.csv` with stage, gate name, agent decision, evidence, and residual risk.
- Do not write outside the sandbox workspace.
- Do not copy prior paper abstracts, body text, captions, tables, or conclusions.
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
    queue_text = f"\nRevision queue: `{queue_path}`\n" if queue_path else ""
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
Formal stage prompt bundle: `{route_manifest.get('bundle_path')}`
{queue_text}
Rules:
- Follow only deep_sequential behavior for this stage.
- Do not edit `00_problem/problem_statement.md` or `00_problem/inbox/`; write intake analysis to `01_task_analysis/`.
- A formal human gate becomes a simulated sandbox gate. Record it in `11_review/simulated_human_gate_log.csv`.
- Update contracts before writing paper claims, result analysis, figures, or submission text.
- Reply only through runner file actions. The external runner will reject prose-only or pseudo-tool responses.

Stage output target:
- Create or update the artifacts normally owned by `{stage_id}`.
- If this stage cannot close a blocker, update review/revision artifacts with a concrete blocker note.
- Keep `reports/training_enhancement_points.csv` current once a full draft or review finding exists.
"""
    prompt.write_text(text, encoding="utf-8")
    return prompt


def update_status(run_dir: Path, status: str, extra: Optional[Mapping[str, Any]] = None) -> Path:
    payload: Dict[str, Any] = {"status": status, "updated_at": now_local()}
    if extra:
        payload.update(dict(extra))
    return write_manifest(run_dir, payload)


def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return {}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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
        for stage in GAP_STAGE_MAP.get(dimension, ["paper_full"]):
            if stage in stage_rows and stage not in selected:
                selected.append(stage)
    return selected or ["paper_full"]


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
        stage_order = int(stage_row.get("stage_order") or index)
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
                "sha256": sha256_text(text) if text else "",
                "size_bytes": len(text.encode("utf-8")) if text else 0,
                "included_in_training": "yes" if text else "missing",
            }
        )
    return rows


def write_prompt_route_manifest(run_dir: Path, workspace: Path, policy: Mapping[str, Any]) -> Dict[str, Any]:
    rows = stage_prompt_rows(policy, workspace)
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
        "The training sandbox must follow these stage prompt files in deep_sequential order. A training round may simulate multiple stages, but every artifact must remain bound to the stage prompt, path permissions, contracts, and human-gate rules.",
        "",
        "| order | stage | prompt | status |",
        "|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['stage_order']} | {row['stage_id']} | {row['prompt_file']} | {row['included_in_training']} |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (workspace / "10_ai_logs" / "prompt_route_manifest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    bundle_lines = [
        "# Formal Stage Prompt Bundle For Full-Agent Training",
        "",
        "This file is assembled from the same prompt files used by normal competition mode. The training wrapper may define sandbox execution, but stage behavior comes from the sections below.",
        "",
        "## Global Contract",
        "",
        "Source: `prompts/stage_prompt_contract.md`",
        "",
    ]
    global_contract = workspace / "prompts" / "stage_prompt_contract.md"
    bundle_lines.append(global_contract.read_text(encoding="utf-8", errors="ignore") if global_contract.exists() else "[missing prompts/stage_prompt_contract.md]")
    for row in rows:
        prompt_file = workspace / str(row.get("prompt_file") or "")
        bundle_lines += [
            "",
            f"## Stage {row.get('stage_order')}: {row.get('stage_id')}",
            "",
            f"Source: `{row.get('prompt_file')}`",
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
        if row.get("status") == "completed":
            return str(row.get("run_id") or "")
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


def run_feedback_eligibility(run_id: str, cfg: Mapping[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
    reasons: List[str] = []
    run_dir = AGENT_RUNS_ROOT / run_id
    if not run_id:
        return False, ["no training run selected"], {}
    if not run_dir.exists():
        return False, [f"training run not found: {run_id}"], {}
    manifest = load_yaml(run_dir / "run_manifest.yaml")
    status = str(manifest.get("status") or "")
    if status not in {"completed", "agent_passed", "iteration_passed"}:
        reasons.append(f"run status is {status or 'unknown'}, not completed")

    queue_path = run_dir / "reports" / "agent_revision_queue.csv"
    queue = read_csv_dict(queue_path)
    if not queue:
        reasons.append("agent_revision_queue.csv has no candidate corrections")
    blockers = blocking_queue_rows(run_dir)
    if blockers:
        reasons.append(f"agent_revision_queue.csv has {len(blockers)} open fail/major item(s)")

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
        "Use these items as candidate corrections. If an item is accepted, record it through the formal revision task flow and contract checks before changing any paper, result, figure, formula, or submission artifact.",
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
    max_items = int(cfg.get("max_items") or 12)
    feedback_rows: List[Dict[str, Any]] = []
    severity_order = {"fail": 0, "major": 1, "minor": 2, "suggestion": 3}
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
        "These rows are candidate corrections from the training sandbox. They are not formal facts and must pass the normal revision, contract, and human-gate controls before changing protected artifacts.",
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
        update_status(run_dir, status, {"agent_command_present": True, "initial_exit_code": rc, "initial_log_tail": tail, **initial_extra})
        if rc != 0:
            benchmark = benchmark_run(run_id)
            validation = validate_run(run_id)
            append_run_index(run_id, "training_sandbox", status, workspace, manifest, run_dir / "reports" / "full_gap_report.md", "agent command failed")
            print(json.dumps({"run_id": run_id, "status": status, "benchmark": benchmark, "validation": validation}, ensure_ascii=False, indent=2))
            return 1

    benchmark = benchmark_run(run_id)

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
            update_status(
                run_dir,
                "iteration_failed" if rc else "iteration_passed",
                {
                    f"iteration_{iteration}_exit_code": rc,
                    f"iteration_{iteration}_log_tail": tail,
                    f"iteration_{iteration}_blocking_queue_before": len(blockers_before),
                    **iteration_extra,
                },
            )
            benchmark = benchmark_run(run_id)
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

    draft_path, draft_status = find_or_build_draft(workspace)
    copy_risk_payload: Dict[str, Any] = {"copy_risk": "skipped_no_draft"}
    if draft_path.exists() and draft_status != "missing":
        copy_csv, copy_md, copy_rows = write_run_copy_risk(run_dir, draft_path, policy)
        copy_risk_payload = {
            "copy_risk": copy_rows[0].get("decision"),
            "copy_risk_report": safe_rel(copy_csv),
            "copy_risk_markdown": safe_rel(copy_md),
        }

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
            **copy_risk_payload,
        },
    )
    validation = validate_run(run_id)
    append_run_index(run_id, "training_sandbox", final_status, workspace, manifest, run_dir / "reports" / "full_gap_report.md")
    print(json.dumps({"run_id": run_id, "status": final_status, "benchmark": benchmark, "validation": validation}, ensure_ascii=False, indent=2))
    return 0 if not validation.get("fail_count") else 1


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
