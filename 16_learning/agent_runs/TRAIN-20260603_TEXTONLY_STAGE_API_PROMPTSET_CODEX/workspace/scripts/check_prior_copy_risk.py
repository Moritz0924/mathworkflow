from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Iterable, List

from learning_utils import (
    ROOT,
    ngrams,
    policy_path,
    read_csv_rows,
    read_learning_policy,
    utc_now,
    write_csv_rows,
)

FIELDS = [
    "target_path",
    "target_type",
    "max_overlap_ratio",
    "matched_source_id",
    "matched_source_path",
    "ngram_size",
    "threshold",
    "decision",
    "checked_at",
]


def default_targets() -> List[Path]:
    candidates: List[Path] = []
    for pattern in [
        "09_paper/*.md",
        "09_paper/*.tex",
        "02_latex_template/sections/*.tex",
        "08_figures/figure_caption_bank.md",
        "13_prior_db/cards/*.jsonl",
    ]:
        candidates.extend(ROOT.glob(pattern))
    return [path for path in candidates if path.is_file()]


def target_type(path: Path) -> str:
    text = path.as_posix()
    if "13_prior_db/cards" in text:
        return "prior_card"
    if "figure" in text or "caption" in text:
        return "caption_or_figure_note"
    if "09_paper" in text or "02_latex_template" in text:
        return "paper_text"
    return "other"


def source_texts(manifest_rows: Iterable[Dict[str, str]], text_dir: Path, max_chars: int) -> Iterable[tuple[str, str, str]]:
    for row in manifest_rows:
        source_id = row.get("source_id") or ""
        if not source_id:
            continue
        path = text_dir / f"{source_id}.txt"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        yield source_id, row.get("path") or "", text[:max_chars] if max_chars > 0 else text


def check_target(target: Path, manifest_rows: List[Dict[str, str]], text_dir: Path, n: int, threshold: float, max_source_chars: int) -> Dict[str, str]:
    text = target.read_text(encoding="utf-8", errors="ignore")
    target_ngrams = ngrams(text, n)
    if not target_ngrams:
        return {
            "target_path": target.relative_to(ROOT).as_posix(),
            "target_type": target_type(target),
            "max_overlap_ratio": "0.000000",
            "matched_source_id": "",
            "matched_source_path": "",
            "ngram_size": str(n),
            "threshold": f"{threshold:.6f}",
            "decision": "pass_no_target_ngrams",
            "checked_at": utc_now(),
        }
    best_ratio = 0.0
    best_source_id = ""
    best_source_path = ""
    for source_id, source_path, source_text in source_texts(manifest_rows, text_dir, max_source_chars):
        source_ngrams = ngrams(source_text, n)
        if not source_ngrams:
            continue
        ratio = len(target_ngrams & source_ngrams) / max(1, len(target_ngrams))
        if ratio > best_ratio:
            best_ratio = ratio
            best_source_id = source_id
            best_source_path = source_path
    return {
        "target_path": target.relative_to(ROOT).as_posix(),
        "target_type": target_type(target),
        "max_overlap_ratio": f"{best_ratio:.6f}",
        "matched_source_id": best_source_id,
        "matched_source_path": best_source_path,
        "ngram_size": str(n),
        "threshold": f"{threshold:.6f}",
        "decision": "fail" if best_ratio > threshold else "pass",
        "checked_at": utc_now(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check prior-text copy risk using n-gram overlap.")
    parser.add_argument("--target", action="append", default=[], help="Specific target file to check. Can be passed more than once.")
    parser.add_argument("--warn-only", action="store_true", help="Always exit 0 after writing reports.")
    args = parser.parse_args()

    policy = read_learning_policy()
    paths = policy.get("paths") or {}
    copy_cfg = policy.get("copy_risk") or {}
    manifest_path = policy_path(paths.get("manifest", ""), "13_prior_db/screening/pdf_manifest.csv")
    text_dir = policy_path(paths.get("source_text_dir", ""), "13_prior_db/fulltext_index/source_texts")
    report_csv = policy_path(paths.get("copy_risk_report", ""), "13_prior_db/screening/copy_risk_report.csv")
    report_md = ROOT / "11_review" / "prior_copy_risk_report.md"
    n = int(copy_cfg.get("ngram_size") or 8)
    threshold = float(copy_cfg.get("max_ngram_overlap_ratio") or 0.08)
    max_source_chars = int(copy_cfg.get("max_source_chars_per_doc") or 120000)

    manifest_rows = read_csv_rows(manifest_path)
    if not manifest_rows:
        raise SystemExit(f"[FAIL] missing or empty manifest: {manifest_path.relative_to(ROOT)}")

    targets = [Path(item) for item in args.target] if args.target else default_targets()
    targets = [(path if path.is_absolute() else ROOT / path).resolve() for path in targets]
    rows = [check_target(path, manifest_rows, text_dir, n, threshold, max_source_chars) for path in targets if path.exists()]
    write_csv_rows(report_csv, rows, FIELDS)

    fail_rows = [row for row in rows if row.get("decision") == "fail"]
    lines = [
        "# Prior Copy Risk Report",
        "",
        f"- generated_at: {utc_now()}",
        f"- checked_targets: {len(rows)}",
        f"- fail_count: {len(fail_rows)}",
        f"- threshold: {threshold}",
        f"- ngram_size: {n}",
        "",
    ]
    if fail_rows:
        lines += ["## Failures", ""]
        for row in fail_rows[:30]:
            lines.append(
                f"- {row['target_path']} overlaps {row['matched_source_id']} at {row['max_overlap_ratio']} ({row['matched_source_path']})"
            )
    else:
        lines.append("No target exceeded the configured prior-copy threshold.")
    report_md.parent.mkdir(parents=True, exist_ok=True)
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] wrote {report_csv.relative_to(ROOT)}")
    print(f"[OK] wrote {report_md.relative_to(ROOT)}")
    if fail_rows and not args.warn_only:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
