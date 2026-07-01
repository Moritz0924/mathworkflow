from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

from workflow_utils import (
    ROOT,
    append_csv_row,
    assert_stage_allowed,
    complete_stage,
    read_csv_dict,
    rel,
    sha256_file,
    write_csv_dicts,
)

SECTIONS_DIR = ROOT / "02_latex_template" / "sections"
OUT_DIR = ROOT / "10_polish" / "polished_sections"
LOG_PATH = ROOT / "10_polish" / "polish_log.csv"
POLISH_CONTRACT = ROOT / "14_contracts" / "polish_diff_check.csv"
FREEZE_REGISTRY = ROOT / "14_contracts" / "artifact_freeze_registry.csv"

POLISH_FIELDS = [
    "check_id",
    "artifact_id",
    "section_id",
    "original_path",
    "polished_path",
    "changed_numbers",
    "changed_units",
    "changed_formulas",
    "changed_labels",
    "changed_refs",
    "changed_citations",
    "changed_model_names",
    "changed_result_meanings",
    "protected_atom_delta_count",
    "decision",
    "review_note",
    "owner",
    "last_checked",
]

FREEZE_FIELDS = [
    "artifact_id",
    "artifact_type",
    "path",
    "hash_sha256",
    "producing_stage",
    "freeze_reason",
    "freeze_time",
    "protected_atoms",
    "allowed_changes",
    "owner",
    "status",
    "notes",
]

LOG_FIELDS = ["time", "section", "source", "output", "method", "decision", "protected_atom_delta_count", "risk_note"]

TEXT_REPLACEMENTS = [
    ("首先，本文", "本文首先"),
    ("然后，本文", "随后本文"),
    ("可以看出，", ""),
    ("综上所述，", "综上，"),
    ("因此可以得到", "因此得到"),
    ("本文将会", "本文"),
    ("进行了分析", "分析"),
    ("进行求解", "求解"),
    ("有着", "具有"),
]

MODEL_TOKEN_RE = re.compile(
    r"\b(?:ARIMA|LSTM|GRU|CNN|RNN|SVM|SVR|XGBoost|LightGBM|CatBoost|PCA|TOPSIS|AHP|KMeans|DBSCAN|RandomForest|LogisticRegression|LinearRegression|MIP|MILP|LP|MCMC)\b",
    re.I,
)

NUMBER_RE = re.compile(r"(?<![A-Za-z_])[-+]?(?:\d+\.\d+|\d+)(?:[eE][-+]?\d+)?%?")
UNIT_RE = re.compile(r"[-+]?(?:\d+\.\d+|\d+)(?:[eE][-+]?\d+)?\s*(?:%|kg|g|mg|km|m|cm|mm|h|min|s|天|小时|分钟|元|万元|亿元|人|次|件|吨|℃|°C|kWh|W|MW|ha|亩)\b")
LABEL_RE = re.compile(r"\\label\{[^{}]+\}")
REF_RE = re.compile(r"\\(?:ref|eqref|autoref|pageref)\{[^{}]+\}")
CITE_RE = re.compile(r"\\(?:cite|citep|citet|parencite|textcite)(?:\[[^\]]*\])?\{[^{}]+\}")
FORMULA_PATTERNS = [
    re.compile(r"\\begin\{equation\}.*?\\end\{equation\}", re.S),
    re.compile(r"\\begin\{align\}.*?\\end\{align\}", re.S),
    re.compile(r"\\begin\{aligned\}.*?\\end\{aligned\}", re.S),
    re.compile(r"\$\$.*?\$\$", re.S),
    re.compile(r"\\\[.*?\\\]", re.S),
    re.compile(r"(?<!\\)\$[^$\n]+(?<!\\)\$", re.S),
]


def clean(value: Any) -> str:
    return str(value or "").strip()


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def choose_current() -> str:
    files = sorted(SECTIONS_DIR.glob("*.tex"))
    return files[0].stem if files else "00_abstract"


def collect_contract_model_names() -> List[str]:
    names: List[str] = []
    for path in [ROOT / "14_contracts" / "result_contract.csv", ROOT / "14_contracts" / "formula_contract.csv"]:
        for row in read_csv_dict(path):
            for key in ["model_id", "metric_name", "formula_id", "latex_label"]:
                value = clean(row.get(key))
                if value:
                    names.append(value)
    return sorted(set(names))


def find_all(pattern: re.Pattern[str], text: str) -> List[str]:
    return [m.group(0) for m in pattern.finditer(text)]


def formula_atoms(text: str) -> List[str]:
    atoms: List[str] = []
    for pattern in FORMULA_PATTERNS:
        atoms.extend(find_all(pattern, text))
    return atoms


def protected_atoms(text: str, contract_model_names: Sequence[str]) -> Dict[str, Counter[str]]:
    atoms: Dict[str, Counter[str]] = {
        "numbers": Counter(find_all(NUMBER_RE, text)),
        "units": Counter(find_all(UNIT_RE, text)),
        "formulas": Counter(formula_atoms(text)),
        "labels": Counter(find_all(LABEL_RE, text)),
        "refs": Counter(find_all(REF_RE, text)),
        "citations": Counter(find_all(CITE_RE, text)),
        "model_names": Counter(find_all(MODEL_TOKEN_RE, text)),
    }
    for name in contract_model_names:
        if len(name) >= 2 and name in text:
            atoms["model_names"][name] += text.count(name)
    return atoms


def counter_delta(a: Counter[str], b: Counter[str]) -> int:
    return sum((a - b).values()) + sum((b - a).values())


def diff_atoms(original: str, polished: str) -> Dict[str, int]:
    contract_names = collect_contract_model_names()
    a = protected_atoms(original, contract_names)
    b = protected_atoms(polished, contract_names)
    return {key: counter_delta(a[key], b[key]) for key in a}


def hold_protected(text: str) -> Tuple[str, List[str]]:
    protected: List[str] = []

    def hold(match: re.Match[str]) -> str:
        protected.append(match.group(0))
        return f"@@MMWF_PROTECTED_{len(protected)-1}@@"

    patterns = [
        *FORMULA_PATTERNS,
        CITE_RE,
        REF_RE,
        LABEL_RE,
        re.compile(r"\\[A-Za-z]+(?:\[[^\]]*\])?(?:\{[^{}]*\})*"),
    ]
    out = text
    for pattern in patterns:
        out = pattern.sub(hold, out)
    return out, protected


def restore_protected(text: str, protected: Sequence[str]) -> str:
    out = text
    for i, value in enumerate(protected):
        out = out.replace(f"@@MMWF_PROTECTED_{i}@@", value)
    return out


def conservative_polish(text: str) -> str:
    staged, protected = hold_protected(text)
    for before, after in TEXT_REPLACEMENTS:
        staged = staged.replace(before, after)
    # Collapse excessive blank lines but preserve paragraph breaks.
    staged = re.sub(r"\n{3,}", "\n\n", staged)
    return restore_protected(staged, protected)


def bool_changed(value: int) -> str:
    return "是" if value else "否"


def append_or_replace_polish_contract(row: Mapping[str, Any]) -> None:
    existing = read_csv_dict(POLISH_CONTRACT) if POLISH_CONTRACT.exists() else []
    check_id = clean(row.get("check_id"))
    existing = [r for r in existing if clean(r.get("check_id")) != check_id]
    existing.append({k: row.get(k, "") for k in POLISH_FIELDS})
    write_csv_dicts(POLISH_CONTRACT, existing, POLISH_FIELDS)


def append_or_replace_freeze(row: Mapping[str, Any]) -> None:
    existing = read_csv_dict(FREEZE_REGISTRY) if FREEZE_REGISTRY.exists() else []
    artifact_id = clean(row.get("artifact_id"))
    existing = [r for r in existing if clean(r.get("artifact_id")) != artifact_id]
    existing.append({k: row.get(k, "") for k in FREEZE_FIELDS})
    write_csv_dicts(FREEZE_REGISTRY, existing, FREEZE_FIELDS)


def append_log(row: Mapping[str, Any]) -> None:
    rows = read_csv_dict(LOG_PATH) if LOG_PATH.exists() else []
    rows.append({k: row.get(k, "") for k in LOG_FIELDS})
    write_csv_dicts(LOG_PATH, rows, LOG_FIELDS)


def polish_section(section: str, apply: bool = False, force: bool = False) -> Tuple[Path, Dict[str, int], str]:
    src = SECTIONS_DIR / f"{section}.tex"
    if not src.exists():
        raise SystemExit(f"[FAIL] section file not found: {rel(src)}")

    original = src.read_text(encoding="utf-8")
    polished = conservative_polish(original)
    diffs = diff_atoms(original, polished)
    delta_total = sum(diffs.values())
    decision = "pass" if delta_total == 0 else "fail"

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    dst = OUT_DIR / f"{section}_polished.tex"
    dst.write_text(polished, encoding="utf-8")

    if apply and decision == "pass":
        if src.exists() and not force:
            backup = src.with_suffix(src.suffix + f".bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            backup.write_text(original, encoding="utf-8")
        src.write_text(polished, encoding="utf-8")
    elif apply and decision != "pass":
        raise SystemExit("[FAIL] protected atoms changed; refusing --apply")

    check_id = f"polish_{section}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    artifact_id = f"polished_{section}"
    review_note = "Rule-based conservative polish. No external AI used. Protected atoms unchanged." if decision == "pass" else "Protected atoms changed; human review required."

    append_or_replace_polish_contract({
        "check_id": check_id,
        "artifact_id": artifact_id,
        "section_id": section,
        "original_path": rel(src),
        "polished_path": rel(dst),
        "changed_numbers": bool_changed(diffs["numbers"]),
        "changed_units": bool_changed(diffs["units"]),
        "changed_formulas": bool_changed(diffs["formulas"]),
        "changed_labels": bool_changed(diffs["labels"]),
        "changed_refs": bool_changed(diffs["refs"]),
        "changed_citations": bool_changed(diffs["citations"]),
        "changed_model_names": bool_changed(diffs["model_names"]),
        "changed_result_meanings": "人工复核",
        "protected_atom_delta_count": str(delta_total),
        "decision": decision,
        "review_note": review_note,
        "owner": "workflow",
        "last_checked": now(),
    })

    append_or_replace_freeze({
        "artifact_id": artifact_id,
        "artifact_type": "polished_latex_section",
        "path": rel(dst),
        "hash_sha256": sha256_file(dst),
        "producing_stage": "polish",
        "freeze_reason": "fact-preserving polish output",
        "freeze_time": now(),
        "protected_atoms": "numbers;units;formulas;labels;refs;citations;model_names",
        "allowed_changes": "style;word_order;minor phrasing",
        "owner": "workflow",
        "status": "frozen" if decision == "pass" else "blocked",
        "notes": review_note,
    })

    append_log({
        "time": now(),
        "section": section,
        "source": rel(src),
        "output": rel(dst),
        "method": "v3.2_mvp_rule_based_fact_preserving",
        "decision": decision,
        "protected_atom_delta_count": str(delta_total),
        "risk_note": review_note,
    })

    return dst, diffs, decision


def main() -> None:
    parser = argparse.ArgumentParser(description="Fact-preserving conservative LaTeX polish for v3.2-MVP.")
    parser.add_argument("--section", default="current", help="Section id, current, or all. all requires --dev-debug.")
    parser.add_argument("--mode", default="deep")
    parser.add_argument("--apply", action="store_true", help="Overwrite source section only if protected atoms are unchanged.")
    parser.add_argument("--force", action="store_true", help="Do not create backup when --apply is used.")
    parser.add_argument("--dev-debug", action="store_true")
    args = parser.parse_args()

    assert_stage_allowed("polish", args.dev_debug)
    if args.section == "all" and not args.dev_debug:
        raise SystemExit("[FAIL] 单环节深度模式禁止 --section all。")

    if args.section == "current":
        sections = [choose_current()]
    elif args.section == "all":
        sections = [p.stem for p in sorted(SECTIONS_DIR.glob("*.tex"))]
    else:
        sections = [args.section]

    outputs: List[str] = []
    failed: List[str] = []
    for section in sections:
        dst, diffs, decision = polish_section(section, apply=args.apply, force=args.force)
        outputs.append(rel(dst))
        if decision != "pass":
            failed.append(section)
        print(f"[OK] {section}: {rel(dst)} decision={decision} protected_delta={sum(diffs.values())}")

    if failed and not args.dev_debug:
        print("[FAIL] Protected atoms changed in: " + ", ".join(failed))
        print(f"[INFO] See {rel(POLISH_CONTRACT)}")
        raise SystemExit(1)

    complete_stage("polish", f"Polished {len(outputs)} section(s) with fact-preserving diff checks. outputs={outputs}")
    print(f"[OK] updated {rel(POLISH_CONTRACT)}")


if __name__ == "__main__":
    main()
