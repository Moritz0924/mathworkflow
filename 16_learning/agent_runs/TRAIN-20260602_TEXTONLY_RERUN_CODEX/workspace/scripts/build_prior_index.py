from __future__ import annotations

import argparse
import math
from collections import Counter
from typing import Dict, List

from learning_utils import (
    ROOT,
    policy_path,
    read_jsonl,
    read_learning_policy,
    tokenize,
    utc_now,
    write_json,
)


def card_text(card: Dict[str, object]) -> str:
    parts = [
        str(card.get("category") or ""),
        str(card.get("family") or ""),
        str(card.get("problem_type") or ""),
        " ".join(str(x) for x in (card.get("model_hints") or [])),
        " ".join(str(x) for x in (card.get("figure_hints") or [])),
        " ".join(str(x) for x in (card.get("scoring_risks") or [])),
    ]
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a CPU-local TF-IDF prior-card index.")
    parser.parse_args()

    policy = read_learning_policy()
    paths = policy.get("paths") or {}
    retrieval = policy.get("retrieval") or {}
    cards_path = policy_path(paths.get("prior_cards", ""), "13_prior_db/cards/prior_cards.jsonl")
    index_path = policy_path(paths.get("prior_index", ""), "13_prior_db/fulltext_index/prior_card_tfidf.json")
    max_tokens = int(retrieval.get("ngram_max_tokens") or 6000)
    cards = read_jsonl(cards_path)
    if not cards:
        raise SystemExit(f"[FAIL] missing or empty prior cards: {cards_path.relative_to(ROOT)}")

    doc_tokens: List[List[str]] = []
    df: Counter[str] = Counter()
    for card in cards:
        tokens = tokenize(card_text(card), max_tokens=max_tokens)
        doc_tokens.append(tokens)
        df.update(set(tokens))

    doc_count = len(cards)
    idf = {token: math.log((1 + doc_count) / (1 + count)) + 1.0 for token, count in df.items()}
    docs = []
    for card, tokens in zip(cards, doc_tokens):
        counts = Counter(tokens)
        weights = {token: (1.0 + math.log(count)) * idf[token] for token, count in counts.items()}
        norm = math.sqrt(sum(value * value for value in weights.values())) or 1.0
        vector = {token: round(value / norm, 8) for token, value in weights.items() if value > 0}
        top_terms = sorted(vector.items(), key=lambda item: item[1], reverse=True)[:20]
        docs.append(
            {
                "card_id": card.get("card_id"),
                "category": card.get("category"),
                "family": card.get("family"),
                "problem_type": card.get("problem_type"),
                "source_ids": card.get("source_ids") or [],
                "copy_risk_status": card.get("copy_risk_status"),
                "search_text": card_text(card),
                "vector": vector,
                "top_terms": [term for term, _ in top_terms],
            }
        )

    payload = {
        "version": "prior-card-tfidf-v1",
        "built_at": utc_now(),
        "doc_count": doc_count,
        "tokenizer": "ascii_words_plus_chinese_char_ngrams_2_4",
        "idf": idf,
        "docs": docs,
    }
    write_json(index_path, payload)
    print(f"[OK] wrote {index_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
