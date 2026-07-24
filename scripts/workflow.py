from __future__ import annotations

import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mmwf.cli import main  # noqa: E402


if __name__ == "__main__":
    workspace = Path(os.environ.get("MMWF_WORKSPACE_ROOT") or ROOT).resolve()
    raise SystemExit(main(root=workspace))
