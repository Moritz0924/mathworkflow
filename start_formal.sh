#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
python scripts/start_dashboard.py --host 127.0.0.1 --port 8765
