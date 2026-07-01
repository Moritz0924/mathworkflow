from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "workflow_state.yaml"
CONFIG_DIR = ROOT / "config"
POLICY_PATH = CONFIG_DIR / "execution_policy.yaml"
CONTRACT_POLICY_PATH = CONFIG_DIR / "contract_policy.yaml"
LOG_DIR = ROOT / "07_results" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_STAGES: List[str] = [
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

DEFAULT_GATE_AFTER_STAGE: Dict[str, str] = {
    "model_route": "model_route_gate",
    "results_freeze": "results_freeze_gate",
    "paper_full": "draft_review_gate",
    "revision": "revision_closure_gate",
    "compile": "final_submission_gate",
}

# Compatibility shim for v3.0 scripts that reused one script for multiple stages.
# Example: generate_paper_sections.py still calls assert_stage_allowed("paper_draft")
# even when invoked for the paper_full stage.
SCRIPT_STAGE_ALIASES: Dict[str, set[str]] = {
    "paper_draft": {"paper_full"},
}

TRUTHY = {"1", "true", "yes", "y", "on", "是", "已确认", "confirmed"}
FALSY = {"0", "false", "no", "n", "off", "否", "未确认", "none", "null", ""}


def load_yaml(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if not text.strip():
        return {}
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
        return data or {}
    except Exception:
        try:
            return json.loads(text)
        except Exception:
            try:
                from simple_yaml import loads as simple_yaml_load

                data = simple_yaml_load(text)
                return data or {}
            except Exception:
                return {}


def dump_yaml(data: Mapping[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        import yaml  # type: ignore

        path.write_text(
            yaml.safe_dump(dict(data), allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
    except Exception:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def read_config(filename: str) -> Dict[str, Any]:
    if not filename.endswith(".yaml"):
        filename += ".yaml"
    return load_yaml(CONFIG_DIR / filename)


def read_policy() -> Dict[str, Any]:
    policy = load_yaml(POLICY_PATH)
    if not policy:
        policy = {
            "version": "v3.2-mvp-default",
            "mode": "deep_sequential",
            "parallel_execution": {"enabled": False},
            "stage_flow": {"ordered_stages": DEFAULT_STAGES},
            "human_gates": {"after_stages": DEFAULT_GATE_AFTER_STAGE},
        }
    return policy


def ordered_stages() -> List[str]:
    policy = read_policy()
    stages = (((policy.get("stage_flow") or {}).get("ordered_stages")) or DEFAULT_STAGES)
    stages = [str(s) for s in stages if str(s).strip()]
    return stages or DEFAULT_STAGES


def gate_after_stage() -> Dict[str, str]:
    policy = read_policy()
    gates = (((policy.get("human_gates") or {}).get("after_stages")) or DEFAULT_GATE_AFTER_STAGE)
    return {str(k): str(v) for k, v in dict(gates).items()}


def next_stage_map() -> Dict[str, Optional[str]]:
    stages = ordered_stages()
    return {stage: (stages[i + 1] if i + 1 < len(stages) else None) for i, stage in enumerate(stages)}


def default_state() -> Dict[str, Any]:
    stages = ordered_stages()
    return {
        "version": "v3.2-mvp",
        "execution_mode": "deep_sequential",
        "allow_parallel": False,
        "current_stage": stages[0],
        "pending_gate": None,
        "last_confirmed_gate": None,
        "completed_stages": [],
        "locked_stages": stages[1:],
        "stage_status": {stages[0]: "pending", **{s: "locked" for s in stages[1:]}},
    }


def normalize_state(state: Dict[str, Any]) -> Dict[str, Any]:
    base = default_state()
    merged = dict(base)
    merged.update(state or {})

    stages = ordered_stages()
    completed = [s for s in (merged.get("completed_stages") or []) if s in stages]
    current = merged.get("current_stage")
    if current not in stages:
        current = next((s for s in stages if s not in completed), stages[-1])
    merged["current_stage"] = current
    merged["completed_stages"] = completed

    status = dict(merged.get("stage_status") or {})
    for s in stages:
        status.setdefault(s, "locked")
    for s in completed:
        status[s] = status.get(s) or "completed"
    if current:
        status[current] = "pending" if status.get(current) in {None, "locked"} else status[current]
    merged["stage_status"] = status

    current_index = stages.index(current) if current in stages else 0
    future_locked = [s for s in stages[current_index + 1 :] if s not in completed]
    existing_locked = [s for s in (merged.get("locked_stages") or []) if s in stages and s != current and s not in completed]
    merged["locked_stages"] = list(dict.fromkeys(existing_locked + future_locked))

    merged.setdefault("execution_mode", "deep_sequential")
    merged.setdefault("allow_parallel", False)
    return merged


def read_state() -> Dict[str, Any]:
    if not STATE_PATH.exists():
        state = default_state()
        write_state(state)
        return state
    return normalize_state(load_yaml(STATE_PATH))


def write_state(state: Dict[str, Any]) -> None:
    dump_yaml(normalize_state(state), STATE_PATH)


def truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in TRUTHY


def falsey(value: Any) -> bool:
    if isinstance(value, bool):
        return not value
    return str(value).strip().lower() in FALSY


def require_deep_mode(dev_debug: bool = False) -> None:
    state = read_state()
    policy = read_policy()
    mode = state.get("execution_mode") or policy.get("mode")
    parallel = policy.get("parallel_execution") or {}
    allow_parallel = truthy(state.get("allow_parallel")) or any(
        truthy(parallel.get(key))
        for key in ("enabled", "allow_multi_stage", "allow_multi_question_codegen", "allow_full_paper_one_shot")
    )
    if mode != "deep_sequential" and not dev_debug:
        raise SystemExit(f"[FAIL] current execution_mode is not deep_sequential: {mode}")
    if allow_parallel and not dev_debug:
        raise SystemExit("[FAIL] formal mode forbids parallel execution")


def resolve_stage_for_current(requested_stage: str, state: Optional[Dict[str, Any]] = None) -> str:
    state = state or read_state()
    current = str(state.get("current_stage") or "")
    if requested_stage == current:
        return requested_stage
    if current in SCRIPT_STAGE_ALIASES.get(requested_stage, set()):
        return current
    return requested_stage


def assert_stage_allowed(stage: str, dev_debug: bool = False) -> None:
    require_deep_mode(dev_debug)
    stages = ordered_stages()
    if stage not in stages and stage not in SCRIPT_STAGE_ALIASES:
        raise SystemExit(f"[FAIL] unknown stage: {stage}")

    state = read_state()
    current = str(state.get("current_stage") or "")
    locked = set(state.get("locked_stages") or [])
    allowed = stage == current or current in SCRIPT_STAGE_ALIASES.get(stage, set())

    if not allowed and not dev_debug:
        raise SystemExit(f"[FAIL] current stage is {current}; refusing to run {stage}")
    actual = resolve_stage_for_current(stage, state)
    if actual in locked and not dev_debug:
        raise SystemExit(f"[FAIL] stage {actual} is locked")


def stage_index(stage: str) -> int:
    stages = ordered_stages()
    return stages.index(stage) if stage in stages else -1


def is_stage_at_or_after(stage: str, reference: str) -> bool:
    si = stage_index(stage)
    ri = stage_index(reference)
    return si >= 0 and ri >= 0 and si >= ri


def write_stage_summary(stage: str, summary: str) -> Path:
    out = ROOT / "11_review" / f"{stage}_stage_summary.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "\n".join(
            [
                f"# {stage} stage summary",
                "",
                f"- generated_at: {datetime.now().isoformat(timespec='seconds')}",
                "- execution_mode: deep_sequential",
                "",
                "## Summary",
                "",
                summary,
                "",
                "## Human gate checklist",
                "",
                "- [ ] Reviewed this stage's artifacts",
                "- [ ] Confirmed no skipped stage output was created",
                "- [ ] Logged rollback or revision needs",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return out


def complete_stage(stage: str, summary: str = "") -> None:
    state = read_state()
    actual_stage = resolve_stage_for_current(stage, state)
    stages = ordered_stages()
    gates = gate_after_stage()
    next_map = next_stage_map()

    if actual_stage not in stages:
        raise SystemExit(f"[FAIL] cannot complete unknown stage: {actual_stage}")

    completed = list(state.get("completed_stages") or [])
    if actual_stage not in completed:
        completed.append(actual_stage)

    status = dict(state.get("stage_status") or {})
    if actual_stage in gates:
        status[actual_stage] = "completed_waiting_gate"
        state["current_stage"] = actual_stage
        state["pending_gate"] = gates[actual_stage]
    else:
        status[actual_stage] = "completed"
        nxt = next_map.get(actual_stage)
        if nxt:
            state["current_stage"] = nxt
            locked = [s for s in (state.get("locked_stages") or []) if s != nxt]
            state["locked_stages"] = locked
            status[nxt] = "pending"
        else:
            state["current_stage"] = actual_stage

    state["completed_stages"] = completed
    state["stage_status"] = status
    write_state(state)
    write_stage_summary(actual_stage, summary or f"{actual_stage} completed")


def confirm_gate(gate: str) -> None:
    state = read_state()
    gates = gate_after_stage()
    pending = state.get("pending_gate")
    if pending and pending != gate:
        raise SystemExit(f"[FAIL] pending gate is {pending}, not {gate}")

    stage = next((s for s, g in gates.items() if g == gate), None)
    if not stage:
        raise SystemExit(f"[FAIL] unknown gate: {gate}")

    stages = ordered_stages()
    if stage not in stages:
        raise SystemExit(f"[FAIL] gate {gate} maps to unknown stage: {stage}")

    status = dict(state.get("stage_status") or {})
    status[stage] = "completed_confirmed"
    nxt = next_stage_map().get(stage)
    if nxt:
        state["current_stage"] = nxt
        state["locked_stages"] = [s for s in (state.get("locked_stages") or []) if s != nxt]
        status[nxt] = "pending"
    state["stage_status"] = status
    state["last_confirmed_gate"] = gate
    state["pending_gate"] = None
    write_state(state)


def run_python(script: Path, args: Iterable[str] = (), env: Optional[Mapping[str, str]] = None) -> int:
    if not script.exists():
        print(f"[FAIL] missing script: {script.relative_to(ROOT)}")
        return 127
    cmd = [sys.executable, str(script), *list(args)]
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log = LOG_DIR / f"{script.stem}.log"
    run_env = os.environ.copy()
    if env:
        run_env.update({str(k): str(v) for k, v in env.items()})
    p = subprocess.run(
        cmd,
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=run_env,
    )
    previous = log.read_text(encoding="utf-8") if log.exists() else ""
    log.write_text(previous + "\n$ " + " ".join(cmd) + "\n" + (p.stdout or ""), encoding="utf-8")
    if p.stdout:
        print(p.stdout)
    return p.returncode


def read_csv_dict(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def read_csv_header(path: Path) -> List[str]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        try:
            return next(reader)
        except StopIteration:
            return []


def write_csv_dicts(path: Path, rows: Sequence[Mapping[str, Any]], fieldnames: Optional[Sequence[str]] = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        if rows:
            fieldnames = list(rows[0].keys())
        else:
            fieldnames = []
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(fieldnames))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def append_csv_row(path: Path, row: Mapping[str, Any], fieldnames: Optional[Sequence[str]] = None) -> None:
    rows = read_csv_dict(path)
    if fieldnames is None:
        fieldnames = list(row.keys()) if not rows else list(rows[0].keys())
    rows.append({k: row.get(k, "") for k in fieldnames})
    write_csv_dicts(path, rows, fieldnames)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)
