from __future__ import annotations

import argparse
import json
import mimetypes
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Type
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mmwf.dashboard import DashboardService  # noqa: E402
from mmwf.errors import WorkflowError  # noqa: E402


MAX_BODY_BYTES = 5 * 1024 * 1024


def handler_class(workspace: Path, web_root: Path) -> Type[BaseHTTPRequestHandler]:
    service = DashboardService(workspace, ROOT / "scripts" / "workflow.py")
    static_root = web_root.resolve()

    class DashboardHandler(BaseHTTPRequestHandler):
        server_version = "MMWF/4"

        def log_message(self, fmt: str, *args: Any) -> None:
            sys.stderr.write(f"[dashboard] {self.address_string()} {fmt % args}\n")

        def send_json(self, payload: Any, status: int = 200) -> None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def read_json(self) -> Dict[str, Any]:
            raw_length = self.headers.get("Content-Length") or "0"
            try:
                length = int(raw_length)
            except ValueError as exc:
                raise WorkflowError("invalid Content-Length") from exc
            if length < 0 or length > MAX_BODY_BYTES:
                raise WorkflowError("request body is too large")
            if length == 0:
                return {}
            try:
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise WorkflowError("request body must be UTF-8 JSON") from exc
            if not isinstance(payload, dict):
                raise WorkflowError("request JSON must be an object")
            return payload

        def do_GET(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            try:
                if path == "/api/health":
                    self.send_json({"status": "ok", "version": "v4"})
                elif path == "/api/state":
                    self.send_json(service.state())
                elif path == "/api/handoffs":
                    self.send_json(service.list_handoffs())
                elif path.startswith("/api/handoffs/"):
                    self.send_json(service.handoff_detail(unquote(path.rsplit("/", 1)[-1])))
                elif path.startswith("/api/"):
                    self.send_json({"error": "unknown API route"}, status=404)
                else:
                    self.serve_static(path)
            except WorkflowError as exc:
                self.send_json({"error": str(exc)}, status=400)
            except OSError as exc:
                self.send_json({"error": str(exc)}, status=500)

        def do_POST(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            routes = {
                "/api/actions/prepare": "prepare",
                "/api/actions/import": "import",
                "/api/actions/verify": "verify",
                "/api/actions/confirm": "confirm",
                "/api/actions/check-gates": "check_gates",
                "/api/actions/check-contracts": "check_contracts",
            }
            action = routes.get(path)
            if not action:
                self.send_json({"error": "unknown API route"}, status=404)
                return
            try:
                self.send_json(service.dispatch(action, self.read_json()))
            except WorkflowError as exc:
                self.send_json({"error": str(exc)}, status=400)
            except OSError as exc:
                self.send_json({"error": str(exc)}, status=500)

        def serve_static(self, requested: str) -> None:
            relative = "index.html" if requested in {"", "/"} else unquote(requested.lstrip("/"))
            target = (static_root / relative).resolve()
            try:
                target.relative_to(static_root)
            except ValueError:
                self.send_error(404)
                return
            if not target.exists() and "." not in Path(relative).name:
                target = static_root / "index.html"
            if not target.exists() or not target.is_file():
                self.send_error(404)
                return
            data = target.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(str(target))[0] or "application/octet-stream")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    return DashboardHandler


def create_server(
    workspace: Path,
    *,
    web_root: Path | None = None,
    host: str = "127.0.0.1",
    port: int = 8765,
) -> ThreadingHTTPServer:
    resolved_workspace = workspace.resolve()
    resolved_web_root = (web_root or (resolved_workspace / "11_dashboard" / "web" / "dist")).resolve()
    return ThreadingHTTPServer((host, port), handler_class(resolved_workspace, resolved_web_root))


def main() -> None:
    parser = argparse.ArgumentParser(description="Start the ChatGPT + Codex formal workflow dashboard")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--open", action="store_true")
    args = parser.parse_args()
    server = create_server(Path(args.root), host=args.host, port=args.port)
    url = f"http://{args.host}:{server.server_port}"
    print(f"[OK] dashboard listening at {url}")
    if args.open:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
