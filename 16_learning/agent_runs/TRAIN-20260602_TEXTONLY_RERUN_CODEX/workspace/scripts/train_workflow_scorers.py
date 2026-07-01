from __future__ import annotations

import argparse
import math
import random
from collections import Counter, defaultdict
from typing import Any, Dict, List, Tuple

from learning_utils import (
    DEFAULT_SEED,
    ROOT,
    family_scoring_risks,
    load_family_figure_hints,
    policy_path,
    read_csv_rows,
    read_learning_policy,
    tokenize,
    utc_now,
    write_json,
)


def load_docs(rows: List[Dict[str, str]], text_dir) -> List[Dict[str, Any]]:
    docs: List[Dict[str, Any]] = []
    for row in rows:
        source_id = row.get("source_id") or ""
        path = text_dir / f"{source_id}.txt"
        title = row.get("path") or ""
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        docs.append(
            {
                "source_id": source_id,
                "title": title,
                "text": title + "\n" + text[:20000],
                "family": row.get("family") or "综合集成",
                "category": row.get("category") or "unknown",
                "extract_status": row.get("extract_status") or "",
            }
        )
    return docs


def stratified_split(docs: List[Dict[str, Any]], label_key: str, test_ratio: float, seed: int) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    random.seed(seed)
    by_label: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for doc in docs:
        by_label[str(doc[label_key])].append(doc)
    train: List[Dict[str, Any]] = []
    test: List[Dict[str, Any]] = []
    for group in by_label.values():
        group = list(group)
        random.shuffle(group)
        if len(group) < 3:
            train.extend(group)
            continue
        test_n = max(1, int(round(len(group) * test_ratio)))
        test.extend(group[:test_n])
        train.extend(group[test_n:])
    return train, test


def train_nb(train_docs: List[Dict[str, Any]], label_key: str, max_tokens: int) -> Dict[str, Any]:
    label_counts: Counter[str] = Counter()
    token_counts: Dict[str, Counter[str]] = defaultdict(Counter)
    vocab: set[str] = set()
    for doc in train_docs:
        label = str(doc[label_key])
        label_counts[label] += 1
        counts = Counter(tokenize(str(doc.get("text") or ""), max_tokens=max_tokens))
        token_counts[label].update(counts)
        vocab.update(counts.keys())
    labels = sorted(label_counts)
    vocab_size = max(1, len(vocab))
    total_docs = max(1, sum(label_counts.values()))
    model = {
        "labels": labels,
        "label_counts": dict(label_counts),
        "log_priors": {label: math.log(label_counts[label] / total_docs) for label in labels},
        "token_log_probs": {},
        "unknown_log_prob": {},
        "vocab_size": vocab_size,
    }
    max_features = int(getattr(train_nb, "max_features_per_label", 2000))
    pruned_token_counts: Dict[str, Counter[str]] = {}
    for label in labels:
        if max_features > 0:
            pruned_token_counts[label] = Counter(dict(token_counts[label].most_common(max_features)))
        else:
            pruned_token_counts[label] = token_counts[label]

    for label in labels:
        total = sum(pruned_token_counts[label].values()) + vocab_size
        model["unknown_log_prob"][label] = math.log(1 / total)
        model["token_log_probs"][label] = {
            token: math.log((count + 1) / total) for token, count in pruned_token_counts[label].items()
        }
    return model


def predict(model: Dict[str, Any], text: str, max_tokens: int) -> Tuple[str, float]:
    counts = Counter(tokenize(text, max_tokens=max_tokens))
    scores: Dict[str, float] = {}
    for label in model.get("labels") or []:
        score = float((model.get("log_priors") or {}).get(label, -99.0))
        token_probs = (model.get("token_log_probs") or {}).get(label) or {}
        unk = float((model.get("unknown_log_prob") or {}).get(label, -99.0))
        for token, count in counts.items():
            score += count * float(token_probs.get(token, unk))
        scores[label] = score
    if not scores:
        return "", 0.0
    best = max(scores, key=scores.get)
    ordered = sorted(scores.values(), reverse=True)
    margin = ordered[0] - ordered[1] if len(ordered) > 1 else ordered[0]
    confidence = 1.0 / (1.0 + math.exp(-min(20.0, max(-20.0, margin / 20.0))))
    return best, confidence


def evaluate(model: Dict[str, Any], test_docs: List[Dict[str, Any]], label_key: str, max_tokens: int) -> Dict[str, Any]:
    if not test_docs:
        return {"test_count": 0, "accuracy": None, "examples": []}
    correct = 0
    examples = []
    for doc in test_docs:
        pred, confidence = predict(model, str(doc.get("text") or ""), max_tokens=max_tokens)
        truth = str(doc[label_key])
        if pred == truth:
            correct += 1
        elif len(examples) < 10:
            examples.append({"source_id": doc.get("source_id"), "truth": truth, "pred": pred, "confidence": round(confidence, 4)})
    return {"test_count": len(test_docs), "accuracy": correct / len(test_docs), "examples": examples}


def main() -> None:
    parser = argparse.ArgumentParser(description="Train lightweight workflow scorers from the local prior corpus.")
    parser.parse_args()

    policy = read_learning_policy()
    paths = policy.get("paths") or {}
    training = policy.get("training") or {}
    seed = int(training.get("seed") or DEFAULT_SEED)
    test_ratio = float(training.get("test_ratio") or 0.2)
    min_class = int(training.get("min_class_count_for_confident_metric") or 3)
    max_tokens = int(training.get("max_tokens_per_document") or 6000)
    max_features = int(training.get("max_features_per_label") or 2000)
    manifest_path = policy_path(paths.get("manifest", ""), "13_prior_db/screening/pdf_manifest.csv")
    text_dir = policy_path(paths.get("source_text_dir", ""), "13_prior_db/fulltext_index/source_texts")
    models_dir = policy_path(paths.get("models", ""), "16_learning/models")
    report_path = policy_path(paths.get("reports", ""), "16_learning/reports") / "training_report.md"
    rows = read_csv_rows(manifest_path)
    if not rows:
        raise SystemExit(f"[FAIL] missing or empty manifest: {manifest_path.relative_to(ROOT)}")

    docs = load_docs(rows, text_dir)
    ok_docs = [doc for doc in docs if not str(doc.get("extract_status") or "").startswith("failed")]
    family_dist = Counter(str(doc["family"]) for doc in docs)
    category_dist = Counter(str(doc["category"]) for doc in docs)
    low_sample = [f"{label}:{count}" for label, count in sorted(category_dist.items()) if count < min_class]
    train_docs, test_docs = stratified_split(ok_docs, "family", test_ratio=test_ratio, seed=seed)
    train_nb.max_features_per_label = max_features  # type: ignore[attr-defined]
    family_model = train_nb(train_docs, "family", max_tokens=max_tokens)
    family_eval = evaluate(family_model, test_docs, "family", max_tokens=max_tokens)

    scorer = {
        "version": "workflow-scorers-v1",
        "trained_at": utc_now(),
        "seed": seed,
        "sample_count": len(docs),
        "usable_sample_count": len(ok_docs),
        "family_classifier": family_model,
        "family_eval": family_eval,
        "figure_prior_by_family": load_family_figure_hints(),
        "risk_prior_by_family": {family: family_scoring_risks(family) for family in family_dist},
        "auto_apply": False,
    }
    write_json(models_dir / "workflow_scorers.json", scorer)

    failed_examples = [doc for doc in docs if str(doc.get("extract_status") or "").startswith("failed")][:12]
    lines = [
        "# Workflow Scorer Training Report",
        "",
        f"- generated_at: {utc_now()}",
        f"- seed: {seed}",
        f"- sample_count: {len(docs)}",
        f"- usable_sample_count: {len(ok_docs)}",
        f"- train_count: {len(train_docs)}",
        f"- test_count: {len(test_docs)}",
        f"- family_accuracy: {family_eval['accuracy'] if family_eval['accuracy'] is not None else 'not_available'}",
        f"- max_features_per_label: {max_features}",
        f"- unavailable_reason: {'none' if ok_docs else 'no extracted text'}",
        "",
        "## Family Distribution",
        "",
    ]
    for label, count in family_dist.most_common():
        lines.append(f"- {label}: {count}")
    lines += ["", "## Category Distribution", ""]
    for label, count in category_dist.most_common():
        lines.append(f"- {label}: {count}")
    lines += ["", "## Low Sample Warnings", ""]
    if low_sample:
        lines.extend(f"- {item}" for item in low_sample)
    else:
        lines.append("- none")
    lines += ["", "## Failed Extraction Examples", ""]
    if failed_examples:
        for doc in failed_examples:
            lines.append(f"- {doc['source_id']}: {doc['title']}")
    else:
        lines.append("- none")
    lines += ["", "## Misclassified Evaluation Examples", ""]
    if family_eval.get("examples"):
        for item in family_eval["examples"]:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines += [
        "",
        "## Safety Notes",
        "",
        "- This scorer only suggests routing, figure, and review risks.",
        "- It must not auto-apply changes to workflow policy, contracts, paper text, or results.",
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] wrote {(models_dir / 'workflow_scorers.json').relative_to(ROOT)}")
    print(f"[OK] wrote {report_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
