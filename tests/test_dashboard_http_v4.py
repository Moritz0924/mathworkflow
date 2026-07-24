from __future__ import annotations

import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

from mmwf.state import default_state, write_state
from scripts.start_dashboard import create_server
from tests.test_formal_workflow import write_policy, write_prompt_templates


class DashboardHttpTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        write_policy(self.root)
        write_prompt_templates(self.root)
        (self.root / "00_problem").mkdir()
        (self.root / "00_problem" / "problem_statement.md").write_text("demo", encoding="utf-8")
        write_state(self.root, default_state("demo"))
        web = self.root / "web"
        web.mkdir()
        (web / "index.html").write_text("<h1>dashboard</h1>", encoding="utf-8")
        self.server = create_server(self.root, web_root=web, host="127.0.0.1", port=0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temp.cleanup()

    def get_json(self, path: str) -> dict:
        with urllib.request.urlopen(self.base + path, timeout=3) as response:
            return json.loads(response.read().decode("utf-8"))

    def post_json(self, path: str, payload: dict) -> dict:
        request = urllib.request.Request(
            self.base + path,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=3) as response:
            return json.loads(response.read().decode("utf-8"))

    def test_state_prepare_and_handoff_routes(self) -> None:
        state = self.get_json("/api/state")
        self.assertEqual("pending_chatgpt", state["status"])
        handoff = self.post_json("/api/actions/prepare", {"target": "chatgpt", "handoff_id": "H-HTTP"})
        self.assertEqual("H-HTTP", handoff["handoff_id"])
        rows = self.get_json("/api/handoffs")
        self.assertEqual("H-HTTP", rows[0]["handoff_id"])

    def test_old_sandbox_route_is_removed(self) -> None:
        request = urllib.request.Request(
            self.base + "/api/sandbox/start",
            data=b"{}",
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.assertRaises(urllib.error.HTTPError) as captured:
            urllib.request.urlopen(request, timeout=3)
        self.assertEqual(404, captured.exception.code)


if __name__ == "__main__":
    unittest.main()
