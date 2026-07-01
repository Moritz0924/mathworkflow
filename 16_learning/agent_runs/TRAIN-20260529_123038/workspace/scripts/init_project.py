"""Copy this template to a new project directory.

Usage:
    python scripts/init_project.py ../my_contest_project
"""
from pathlib import Path
import shutil
import sys

SRC = Path(__file__).resolve().parents[1]


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/init_project.py <target_dir>")
    target = Path(sys.argv[1]).resolve()
    if target.exists():
        raise SystemExit(f"Target already exists: {target}")
    ignore = shutil.ignore_patterns("*.zip", "__pycache__", ".DS_Store")
    shutil.copytree(SRC, target, ignore=ignore)
    print(f"[OK] initialized project at {target}")


if __name__ == "__main__":
    main()
