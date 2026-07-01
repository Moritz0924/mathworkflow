from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "mcp_servers"))

from mcp_client import MCPClient  # noqa: E402
from vision_server import (  # noqa: E402
    DEFAULT_QWEN_VL_BASE_URL,
    DEFAULT_QWEN_VL_MODEL,
    chat_completions_endpoint,
    first_env,
    validate_image_path,
)


def test_mcp_vision_server_lists_and_calls_tool(tmp_path: Path) -> None:
    image = tmp_path / "scan.png"
    image.write_bytes(b"\x89PNG\r\n\x1a\n")
    env = os.environ.copy()
    env["VISION_OFFLINE"] = "1"
    with MCPClient(["python", str(ROOT / "mcp_servers" / "vision_server.py")], cwd=tmp_path, env=env, timeout_seconds=10) as client:
        client.initialize()
        tools = client.list_tools()
        assert any(tool.get("name") == "image_recognize" for tool in tools)
        result = client.call_tool("image_recognize", {"workspace": str(tmp_path), "image_path": str(image)})
    assert result["isError"] is False
    assert result["structuredContent"]["source"] == "offline_metadata"


def test_vision_server_rejects_paths_outside_workspace(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside.png"
    outside.write_bytes(b"\x89PNG\r\n\x1a\n")
    try:
        validate_image_path(str(tmp_path), str(outside), 1024)
        assert False, "expected path rejection"
    except ValueError as exc:
        assert "inside workspace" in str(exc)


def test_vision_server_rejects_missing_and_oversized_files(tmp_path: Path) -> None:
    missing = tmp_path / "missing.png"
    try:
        validate_image_path(str(tmp_path), str(missing), 1024)
        assert False, "expected missing file rejection"
    except ValueError as exc:
        assert "does not exist" in str(exc)

    image = tmp_path / "large.png"
    image.write_bytes(b"x" * 8)
    try:
        validate_image_path(str(tmp_path), str(image), 4)
        assert False, "expected size rejection"
    except ValueError as exc:
        assert "exceeds max bytes" in str(exc)


def test_qwen_vl_defaults_and_endpoint_normalization(monkeypatch) -> None:
    monkeypatch.delenv("QWEN_VL_BASE_URL", raising=False)
    monkeypatch.delenv("VISION_BASE_URL", raising=False)
    monkeypatch.delenv("QWEN_VL_MODEL", raising=False)
    monkeypatch.delenv("VISION_MODEL", raising=False)
    assert first_env(["QWEN_VL_BASE_URL", "VISION_BASE_URL"], DEFAULT_QWEN_VL_BASE_URL) == DEFAULT_QWEN_VL_BASE_URL
    assert first_env(["QWEN_VL_MODEL", "VISION_MODEL"], DEFAULT_QWEN_VL_MODEL) == DEFAULT_QWEN_VL_MODEL
    assert chat_completions_endpoint("https://dashscope.aliyuncs.com/compatible-mode/v1") == (
        "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    )
    assert chat_completions_endpoint("https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions") == (
        "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    )
