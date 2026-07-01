from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple

from learning_utils import (
    ROOT,
    ensure_dir,
    infer_category_from_path,
    load_category_family_map,
    policy_path,
    read_csv_rows,
    read_learning_policy,
    sha256_file,
    sha256_text,
    stable_id,
    utc_now,
    write_csv_rows,
    write_jsonl,
)

MANIFEST_FIELDS = [
    "source_id",
    "path",
    "category",
    "family",
    "sha256",
    "page_count",
    "extract_status",
    "text_hash",
    "created_at",
]


def pdf_reader():
    try:
        from pypdf import PdfReader  # type: ignore

        return PdfReader
    except Exception:
        try:
            from PyPDF2 import PdfReader  # type: ignore

            return PdfReader
        except Exception as exc:
            raise SystemExit(f"[FAIL] pypdf or PyPDF2 is required for PDF extraction: {exc}")


def clean_pdf_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_text(path: Path, max_pages: int, min_ok_chars: int) -> Tuple[str, int, str]:
    reader_cls = pdf_reader()
    try:
        reader = reader_cls(str(path))
        pages = list(reader.pages)
        page_count = len(pages)
        chunks: List[str] = []
        for page in pages[:max_pages]:
            try:
                chunks.append(page.extract_text() or "")
            except Exception:
                chunks.append("")
        text = clean_pdf_text("\n".join(chunks))
        if len(text) >= min_ok_chars:
            status = "ok"
        elif text:
            status = "partial"
        else:
            status = "failed_empty_text"
        return text, page_count, status
    except Exception as exc:
        return f"[extract_failed] {exc}", 0, "failed_exception"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the local prior PDF corpus manifest and extracted text cache.")
    parser.add_argument("--limit", type=int, default=0, help="Optional development limit.")
    parser.add_argument("--force", action="store_true", help="Re-extract text even if cache files exist.")
    args = parser.parse_args()

    policy = read_learning_policy()
    paths = policy.get("paths") or {}
    corpus_cfg = policy.get("corpus") or {}
    corpus_root = policy_path(paths.get("corpus_root", ""), "论文数据集")
    manifest_path = policy_path(paths.get("manifest", ""), "13_prior_db/screening/pdf_manifest.csv")
    text_dir = policy_path(paths.get("source_text_dir", ""), "13_prior_db/fulltext_index/source_texts")
    source_meta_path = policy_path(paths.get("source_meta", ""), "13_prior_db/fulltext_index/source_meta.jsonl")
    feature_path = policy_path(paths.get("training_data", ""), "16_learning/training_data") / "corpus_features.csv"
    report_path = policy_path(paths.get("reports", ""), "16_learning/reports") / "corpus_build_report.md"
    max_pages = int(corpus_cfg.get("max_pages_per_pdf") or 80)
    min_ok_chars = int(corpus_cfg.get("min_ok_text_chars") or 300)
    expected_count = int(corpus_cfg.get("expected_pdf_count") or 0)
    pdf_glob = str(corpus_cfg.get("pdf_glob") or "**/*.pdf")

    ensure_dir(text_dir)
    family_map = load_category_family_map()
    pdfs = sorted(corpus_root.glob(pdf_glob), key=lambda p: p.as_posix().lower())
    if args.limit > 0:
        pdfs = pdfs[: args.limit]

    created_at = utc_now()
    rows: List[Dict[str, str]] = []
    meta_rows: List[Dict[str, object]] = []
    feature_rows: List[Dict[str, object]] = []
    failures: List[str] = []
    previous_rows = {row.get("source_id", ""): row for row in read_csv_rows(manifest_path)}

    for path in pdfs:
        rel_path = path.relative_to(corpus_root).as_posix()
        source_id = stable_id("SRC", rel_path)
        text_path = text_dir / f"{source_id}.txt"
        file_hash = sha256_file(path)
        if text_path.exists() and not args.force:
            text = text_path.read_text(encoding="utf-8", errors="ignore")
            previous = previous_rows.get(source_id, {})
            page_count = str(previous.get("page_count") or "")
            status = str(previous.get("extract_status") or "cached")
        else:
            text, page_count_value, status = extract_pdf_text(path, max_pages=max_pages, min_ok_chars=min_ok_chars)
            page_count = str(page_count_value)
            text_path.write_text(text, encoding="utf-8", errors="ignore")
        category = infer_category_from_path(path, corpus_root)
        family = family_map.get(category, "综合集成")
        text_hash = sha256_text(text)
        rows.append(
            {
                "source_id": source_id,
                "path": rel_path,
                "category": category,
                "family": family,
                "sha256": file_hash,
                "page_count": page_count,
                "extract_status": status,
                "text_hash": text_hash,
                "created_at": created_at,
            }
        )
        meta_rows.append(
            {
                "source_id": source_id,
                "path": rel_path,
                "category": category,
                "family": family,
                "text_cache": text_path.relative_to(ROOT).as_posix(),
                "text_hash": text_hash,
                "extract_status": status,
            }
        )
        feature_rows.append(
            {
                "source_id": source_id,
                "category": category,
                "family": family,
                "char_count": len(text),
                "line_count": text.count("\n") + 1 if text else 0,
                "figure_mentions": len(re.findall(r"图\s*\d+|figure", text, flags=re.I)),
                "table_mentions": len(re.findall(r"表\s*\d+|table", text, flags=re.I)),
                "formula_mentions": len(re.findall(r"公式|equation|\\\(", text, flags=re.I)),
                "extract_status": status,
            }
        )
        if status.startswith("failed"):
            failures.append(rel_path)

    write_csv_rows(manifest_path, rows, MANIFEST_FIELDS)
    write_jsonl(source_meta_path, meta_rows)
    write_csv_rows(
        feature_path,
        feature_rows,
        [
            "source_id",
            "category",
            "family",
            "char_count",
            "line_count",
            "figure_mentions",
            "table_mentions",
            "formula_mentions",
            "extract_status",
        ],
    )

    family_counts: Dict[str, int] = {}
    for row in rows:
        family_counts[row["family"]] = family_counts.get(row["family"], 0) + 1
    lines = [
        "# Prior Corpus Build Report",
        "",
        f"- generated_at: {created_at}",
        f"- corpus_root: {corpus_root.relative_to(ROOT).as_posix() if corpus_root.is_relative_to(ROOT) else corpus_root.as_posix()}",
        f"- pdf_count: {len(rows)}",
        f"- expected_pdf_count: {expected_count or 'not_configured'}",
        f"- extraction_failures: {len(failures)}",
        f"- manifest: {manifest_path.relative_to(ROOT).as_posix()}",
        f"- text_cache_dir: {text_dir.relative_to(ROOT).as_posix()}",
        "",
        "## Family Distribution",
        "",
    ]
    for family, count in sorted(family_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {family}: {count}")
    if expected_count and len(rows) != expected_count:
        lines += ["", "## Count Warning", "", f"- expected {expected_count}, found {len(rows)}"]
    if failures:
        lines += ["", "## Failed Examples", ""]
        lines.extend(f"- {item}" for item in failures[:20])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] wrote {manifest_path.relative_to(ROOT)}")
    print(f"[OK] wrote {source_meta_path.relative_to(ROOT)}")
    print(f"[OK] wrote {feature_path.relative_to(ROOT)}")
    print(f"[OK] wrote {report_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
