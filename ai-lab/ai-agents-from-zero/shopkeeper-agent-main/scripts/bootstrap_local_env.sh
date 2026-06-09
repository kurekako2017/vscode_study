#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VENV_DIR:-.venv}"

echo "[1/5] Create virtualenv: ${VENV_DIR}"
if "$PYTHON_BIN" -m virtualenv --version >/dev/null 2>&1; then
  "$PYTHON_BIN" -m virtualenv "$VENV_DIR"
else
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

echo "[2/5] Activate virtualenv"
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

echo "[3/5] Upgrade pip"
python -m pip install --upgrade pip setuptools wheel

echo "[4/5] Install backend dependencies"
python -m pip install -e .

echo "[5/5] Install frontend dependencies"
cd frontend
npm install

echo
echo "Bootstrap finished."
echo "Next:"
echo "  1. Copy .env.nas.example to .env and fill OPENROUTER_API_KEY"
echo "  2. Prepare NAS MySQL meta/dw databases"
echo "  3. Run backend with: source .venv/bin/activate && uvicorn main:app --reload"
echo "  4. Run frontend with: cd frontend && npm run dev"
