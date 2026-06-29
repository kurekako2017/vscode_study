#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$ROOT_DIR/backend/.venv/bin/python"

if [[ ! -x "$PYTHON" ]]; then
  python3 -m venv --system-site-packages "$ROOT_DIR/backend/.venv"
  "$ROOT_DIR/backend/.venv/bin/python" -m pip install -r "$ROOT_DIR/backend/requirements.txt"
fi

cd "$ROOT_DIR/backend"
"$PYTHON" -m unittest discover -s tests -v
"$PYTHON" -m compileall app

cd "$ROOT_DIR/frontend"
if [[ ! -d node_modules ]]; then
  npm install
fi
npm test
npm run build
