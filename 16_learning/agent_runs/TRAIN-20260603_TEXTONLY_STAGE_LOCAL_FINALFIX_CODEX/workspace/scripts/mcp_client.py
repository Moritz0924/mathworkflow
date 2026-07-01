from __future__ import annotations

import argparse
import json
import os
import queue
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence


class MCPError(RuntimeError):
    pass


class MCPClient:
    """Minimal stdio JSON-RPC client for the local MCP-compatible servers."""

    def __init__(
        self,
        command: Sequence[str],
        cwd: Optional[Path] = None,
        env: Optional[Mapping[str, str]] = None,
        timeout_seconds: float = 30.0,
    ) -> None:
        if not command:
            raise ValueError("MCP command cannot be empty")
        self.command = [str(part) for part in command]
        self.cwd = cwd
        self.env = dict(env or {})
        self.timeout_seconds = timeout_seconds
        self._next_id = 1
        self._proc: Optional[subprocess.Popen[str]] = None
        self._stdout_queue: "queue.Queue[str]" = queue.Queue()
        self._stderr_queue: "queue.Queue[str]" = queue.Queue()
        self._threads: List[threading.Thread] = []

    def __enter__(self) -> "MCPClient":
        self.start()
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        self.close()

    def start(self) -> None:
        if self._proc is not None:
            return
        env = os.environ.copy()
        env.update(self.env)
        self._proc = subprocess.Popen(
            self.command,
            cwd=str(self.cwd) if self.cwd else None,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._threads = [
            threading.Thread(target=self._read_lines, args=(self._proc.stdout, self._stdout_queue), daemon=True),
            threading.Thread(target=self._read_lines, args=(self._proc.stderr, self._stderr_queue), daemon=True),
        ]
        for thread in self._threads:
            thread.start()

    def close(self) -> None:
        proc = self._proc
        if proc is None:
            return
        if proc.poll() is None:
            try:
                proc.terminate()
                proc.wait(timeout=2)
            except Exception:
                proc.kill()
        self._proc = None

    @staticmethod
    def _read_lines(stream: Optional[Any], out: "queue.Queue[str]") -> None:
        if stream is None:
            return
        for line in stream:
            out.put(line.rstrip("\n"))

    def request(self, method: str, params: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        if self._proc is None:
            self.start()
        assert self._proc is not None
        if self._proc.stdin is None:
            raise MCPError("MCP process has no stdin")
        if self._proc.poll() is not None:
            stderr = self._drain(self._stderr_queue)
            raise MCPError(f"MCP process exited before request: {self._proc.returncode}; {stderr}")

        request_id = self._next_id
        self._next_id += 1
        payload = {"jsonrpc": "2.0", "id": request_id, "method": method, "params": dict(params or {})}
        self._proc.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
        self._proc.stdin.flush()

        while True:
            try:
                raw = self._stdout_queue.get(timeout=self.timeout_seconds)
            except queue.Empty as exc:
                stderr = self._drain(self._stderr_queue)
                raise MCPError(f"timed out waiting for MCP response to {method}; {stderr}") from exc
            if not raw.strip():
                continue
            try:
                response = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if response.get("id") != request_id:
                continue
            if response.get("error"):
                raise MCPError(str(response["error"]))
            return dict(response.get("result") or {})

    @staticmethod
    def _drain(q: "queue.Queue[str]") -> str:
        items: List[str] = []
        while True:
            try:
                items.append(q.get_nowait())
            except queue.Empty:
                break
        return "\n".join(items)[-2000:]

    def initialize(self) -> Dict[str, Any]:
        return self.request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "math-workflow-mcp-client", "version": "v1"},
            },
        )

    def list_tools(self) -> List[Dict[str, Any]]:
        result = self.request("tools/list")
        return list(result.get("tools") or [])

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> Dict[str, Any]:
        return self.request("tools/call", {"name": name, "arguments": dict(arguments)})


def main() -> None:
    parser = argparse.ArgumentParser(description="Minimal stdio MCP client.")
    parser.add_argument("--command", nargs="+", required=True, help="MCP server command.")
    parser.add_argument("--list-tools", action="store_true")
    parser.add_argument("--call-tool", default="")
    parser.add_argument("--arguments-json", default="{}")
    parser.add_argument("--cwd", default="")
    args = parser.parse_args()

    cwd = Path(args.cwd).resolve() if args.cwd else None
    with MCPClient(args.command, cwd=cwd) as client:
        init = client.initialize()
        if args.list_tools:
            print(json.dumps({"initialize": init, "tools": client.list_tools()}, ensure_ascii=False, indent=2))
            return
        if args.call_tool:
            arguments = json.loads(args.arguments_json)
            print(json.dumps(client.call_tool(args.call_tool, arguments), ensure_ascii=False, indent=2))
            return
        print(json.dumps(init, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
