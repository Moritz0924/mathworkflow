from __future__ import annotations

import json
import re
from typing import Any, List, Optional, Tuple


class SimpleYAMLError(ValueError):
    pass


Line = Tuple[int, str]


def loads(text: str) -> Any:
    stripped = text.strip()
    if not stripped:
        return {}
    if stripped[0] in "{[":
        return json.loads(stripped)
    lines = _logical_lines(text)
    value, index = _parse_block(lines, 0, 0)
    while index < len(lines) and not lines[index][1].strip():
        index += 1
    return value


def _logical_lines(text: str) -> List[Line]:
    out: List[Line] = []
    for raw in text.splitlines():
        if not raw.strip():
            continue
        stripped = raw.lstrip(" ")
        if stripped.startswith("#"):
            continue
        indent = len(raw) - len(stripped)
        out.append((indent, _strip_inline_comment(stripped.rstrip())))
    return out


def _strip_inline_comment(text: str) -> str:
    in_single = False
    in_double = False
    for idx, ch in enumerate(text):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            if idx == 0 or text[idx - 1].isspace():
                return text[:idx].rstrip()
    return text


def _parse_block(lines: List[Line], index: int, indent: int) -> Tuple[Any, int]:
    index = _skip_deeper_or_blank(lines, index)
    if index >= len(lines):
        return {}, index
    actual_indent, content = lines[index]
    if actual_indent < indent:
        return {}, index
    if content.startswith("- ") and actual_indent == indent:
        return _parse_list(lines, index, indent)
    return _parse_map(lines, index, indent)


def _skip_deeper_or_blank(lines: List[Line], index: int) -> int:
    return index


def _parse_list(lines: List[Line], index: int, indent: int) -> Tuple[List[Any], int]:
    items: List[Any] = []
    while index < len(lines):
        line_indent, content = lines[index]
        if line_indent < indent:
            break
        if line_indent > indent:
            break
        if not content.startswith("- "):
            break
        rest = content[2:].strip()
        if not rest:
            item, index = _parse_block(lines, index + 1, indent + 2)
            items.append(item)
            continue
        key, value = _split_key_value(rest)
        if key is not None:
            item = {}
            if value in {None, ""}:
                nested, next_index = _parse_block(lines, index + 1, indent + 2)
                item[key] = nested
                index = next_index
            elif value in {">", "|"}:
                block, next_index = _collect_block_scalar(lines, index + 1, indent + 2, folded=value == ">")
                item[key] = block
                index = next_index
            else:
                item[key] = _parse_scalar(value)
                index += 1
            if index < len(lines) and lines[index][0] > indent:
                extra, next_index = _parse_block(lines, index, indent + 2)
                if isinstance(extra, dict):
                    item.update(extra)
                    index = next_index
            items.append(item)
        else:
            items.append(_parse_scalar(rest))
            index += 1
    return items, index


def _parse_map(lines: List[Line], index: int, indent: int) -> Tuple[dict, int]:
    obj: dict = {}
    while index < len(lines):
        line_indent, content = lines[index]
        if line_indent < indent:
            break
        if line_indent > indent:
            break
        if content.startswith("- "):
            break
        key, value = _split_key_value(content)
        if key is None:
            raise SimpleYAMLError(f"cannot parse line: {content}")
        if value in {None, ""}:
            nested, index = _parse_block(lines, index + 1, indent + 2)
            obj[key] = nested
        elif value in {">", "|"}:
            block, index = _collect_block_scalar(lines, index + 1, indent + 2, folded=value == ">")
            obj[key] = block
        else:
            obj[key] = _parse_scalar(value)
            index += 1
    return obj, index


def _split_key_value(text: str) -> Tuple[Optional[str], Optional[str]]:
    if ":" not in text:
        return None, None
    key, value = text.split(":", 1)
    key = key.strip()
    if not key:
        return None, None
    return key, value.strip()


def _collect_block_scalar(lines: List[Line], index: int, indent: int, folded: bool) -> Tuple[str, int]:
    parts: List[str] = []
    while index < len(lines):
        line_indent, content = lines[index]
        if line_indent < indent:
            break
        parts.append(content.strip())
        index += 1
    return (" ".join(parts) if folded else "\n".join(parts)), index


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"", "null", "Null", "NULL", "~"}:
        return None
    if value in {"true", "True", "TRUE"}:
        return True
    if value in {"false", "False", "FALSE"}:
        return False
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(part.strip()) for part in inner.split(",")]
    if re.fullmatch(r"-?\d+", value):
        try:
            return int(value)
        except Exception:
            pass
    if re.fullmatch(r"-?\d+\.\d+", value):
        try:
            return float(value)
        except Exception:
            pass
    return value
