#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# 允许外部通过环境变量覆盖 Python 和虚拟环境目录，方便不同机器复用同一脚本。
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VENV_DIR:-.venv}"

echo "[1/5] Create virtualenv: ${VENV_DIR}"
if "$PYTHON_BIN" -m virtualenv --version >/dev/null 2>&1; then
  # 优先使用 virtualenv，若环境里没有再退回到标准库 venv。
  "$PYTHON_BIN" -m virtualenv "$VENV_DIR"
else
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

echo "[2/5] Activate virtualenv"
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

echo "[3/5] Upgrade pip"
# 先升级打包工具，减少旧版本 pip/setuptools 导致的安装问题。
python -m pip install --upgrade pip setuptools wheel

echo "[4/5] Install backend dependencies"
# `pip install -e .` 会把当前项目以可编辑模式安装，方便边改代码边运行。
python -m pip install -e .

echo "[5/5] Install frontend dependencies"
# 前端依赖单独放在 frontend 目录下，进入目录后再执行安装。
cd frontend
npm install

echo
echo "Bootstrap finished."
echo "Next:"
echo "  1. Copy .env.nas.example to .env and fill OPENROUTER_API_KEY"
echo "  2. Prepare NAS MySQL meta/dw databases"
echo "  3. Run backend with: source .venv/bin/activate && uvicorn main:app --reload"
echo "  4. Run frontend with: cd frontend && npm run dev"
