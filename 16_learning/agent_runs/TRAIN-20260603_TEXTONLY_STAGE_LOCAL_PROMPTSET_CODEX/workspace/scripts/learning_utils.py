from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

from workflow_utils import ROOT, load_yaml

LEARNING_POLICY = ROOT / "config" / "learning_policy.yaml"
PRIOR_POLICY = ROOT / "config" / "prior_db_policy.yaml"
DEFAULT_SEED = 20260524


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_learning_policy() -> Dict[str, Any]:
    policy = load_yaml(LEARNING_POLICY)
    return policy or {}


def policy_path(raw: str, default: str) -> Path:
    value = str(raw or default)
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(row) for row in csv.DictReader(f)]


def write_csv_rows(path: Path, rows: Sequence[Mapping[str, Any]], fieldnames: Sequence[str]) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(fieldnames))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_jsonl(path: Path, records: Iterable[Mapping[str, Any]]) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(dict(record), ensure_ascii=False, sort_keys=True) + "\n")


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            text = line.strip()
            if text:
                rows.append(json.loads(text))
    return rows


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def stable_id(prefix: str, value: str, length: int = 12) -> str:
    digest = hashlib.sha256(value.encode("utf-8", errors="ignore")).hexdigest()[:length]
    return f"{prefix}{digest}"


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[^\w\u4e00-\u9fff]+", "", text)
    return text


def tokenize(text: str, max_tokens: int = 6000) -> List[str]:
    text = text.lower()
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9_+-]{1,}|[\u4e00-\u9fff]", text)
    tokens: List[str] = []
    chinese_run: List[str] = []

    def flush_chinese() -> None:
        if not chinese_run:
            return
        joined = "".join(chinese_run)
        for n in (2, 3, 4):
            for i in range(max(0, len(joined) - n + 1)):
                tokens.append(joined[i : i + n])
        chinese_run.clear()

    for word in words:
        if re.fullmatch(r"[\u4e00-\u9fff]", word):
            chinese_run.append(word)
        else:
            flush_chinese()
            tokens.append(word)
    flush_chinese()
    if max_tokens > 0:
        return tokens[:max_tokens]
    return tokens


def tfidf_vector(text: str, idf: Mapping[str, float], max_tokens: int = 6000) -> Dict[str, float]:
    counts: Dict[str, int] = {}
    for token in tokenize(text, max_tokens=max_tokens):
        if token in idf:
            counts[token] = counts.get(token, 0) + 1
    if not counts:
        return {}
    weights = {token: (1.0 + math.log(count)) * float(idf[token]) for token, count in counts.items()}
    norm = math.sqrt(sum(value * value for value in weights.values())) or 1.0
    return {token: value / norm for token, value in weights.items()}


def cosine_sparse(left: Mapping[str, float], right: Mapping[str, float]) -> float:
    if not left or not right:
        return 0.0
    if len(left) > len(right):
        left, right = right, left
    return sum(value * float(right.get(token, 0.0)) for token, value in left.items())


def ngrams(text: str, n: int) -> set[str]:
    norm = normalize_text(text)
    if len(norm) < n:
        return set()
    return {norm[i : i + n] for i in range(len(norm) - n + 1)}


def split_semicolon(value: Any) -> List[str]:
    parts = re.split(r"[;；,，|]+", str(value or ""))
    return [part.strip() for part in parts if part.strip()]


def compact_list(values: Iterable[Any], max_items: int = 8) -> List[str]:
    seen: List[str] = []
    for value in values:
        text = str(value or "").strip()
        if text and text not in seen:
            seen.append(text)
        if len(seen) >= max_items:
            break
    return seen


def load_category_family_map() -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for row in read_csv_rows(ROOT / "13_sample_prior" / "sample_manifest.csv"):
        category = str(row.get("category") or "").strip()
        family = str(row.get("family") or "").strip()
        if category and family:
            mapping.setdefault(category, family)
    fallback = {
        "线性规划": "优化决策",
        "遗传算法": "优化决策",
        "模拟退火": "优化决策",
        "蚁群算法": "优化决策",
        "动态规划": "优化决策",
        "排队论": "优化决策",
        "层次分析法": "统计评价",
        "主成分分析": "统计评价",
        "因子分析": "统计评价",
        "模糊综合评价": "统计评价",
        "相关系数": "统计评价",
        "多元回归": "预测回归",
        "拟合模型": "预测回归",
        "灰色预测": "预测回归",
        "微分方程": "机理仿真",
        "元胞自动机": "机理仿真",
        "神经网络": "机器学习",
        "支持向量机": "机器学习",
        "决策树": "机器学习",
    }
    for key, value in fallback.items():
        mapping.setdefault(key, value)
    return mapping


def infer_category_from_path(path: Path, corpus_root: Path) -> str:
    try:
        rel_parts = path.relative_to(corpus_root).parts
    except ValueError:
        rel_parts = path.parts
    for part in rel_parts[:-1]:
        lowered = part.lower()
        if part.isdigit() or lowered.endswith(".zip"):
            continue
        return part
    if len(rel_parts) >= 2:
        return rel_parts[-2]
    return "unknown"


def family_problem_type(family: str) -> str:
    return {
        "优化决策": "优化决策型",
        "统计评价": "数据评价型",
        "预测回归": "预测分析型",
        "机理仿真": "机理仿真型",
        "机器学习": "分类识别型",
        "空间网络": "网络空间型",
        "综合集成": "综合开放型",
    }.get(family, "综合开放型")


def load_family_figure_hints() -> Dict[str, List[str]]:
    rows = read_csv_rows(ROOT / "08_figures" / "model_chart_priority_matrix.csv")
    out: Dict[str, List[str]] = {}
    for row in rows:
        family = str(row.get("model_family") or "").strip()
        if not family:
            continue
        out[family] = compact_list(row.get(f"priority_{i}") for i in range(1, 6))
    return out


def family_scoring_risks(family: str) -> List[str]:
    return {
        "优化决策": ["constraints not traceable", "objective and result table disconnected", "sensitivity analysis missing"],
        "统计评价": ["indicator meaning unclear", "weight source weak", "ranking interpretation unsupported"],
        "预测回归": ["residual diagnostics missing", "prediction interval missing", "extrapolation boundary unclear"],
        "机理仿真": ["assumptions not linked to mechanism", "parameters lack source", "scenario validation weak"],
        "机器学习": ["train/test split unclear", "only accuracy reported", "interpretability or ablation missing"],
        "空间网络": ["spatial scale unclear", "node or coordinate meaning missing", "overdense network visualization"],
    }.get(family, ["evidence chain weak", "validation section underdeveloped"])


def family_model_hints(category: str, family: str) -> List[str]:
    hints = {
        "优化决策": ["define decision variables first", "bind objective and constraints to data fields", "compare baseline and optimized plans"],
        "统计评价": ["build indicator hierarchy", "record weight source", "explain score, rank and robustness together"],
        "预测回归": ["separate cleaning, feature selection and validation", "report error distribution", "state extrapolation boundary"],
        "机理仿真": ["state assumptions before equations", "calibrate key parameters", "compare scenarios and sensitivity"],
        "机器学习": ["define data split", "compare baseline models", "add interpretability and error analysis"],
    }.get(family, ["state problem decomposition", "bind each claim to a source artifact", "keep validation visible"])
    return [category, *hints]
