#!/usr/bin/env bash
set -euo pipefail

# 集中执行本地提交前需要通过的 Backend、Frontend 和编译检查。
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

if [[ -x "$BACKEND_DIR/.venv/bin/python" ]]; then
  PYTHON_BIN="$BACKEND_DIR/.venv/bin/python"
  echo "使用 backend/.venv/bin/python"
else
  PYTHON_BIN="python3"
  echo "未找到 backend/.venv，使用系统 python3"
fi

echo "[1/4] 执行 Backend tests"
cd "$BACKEND_DIR"
"$PYTHON_BIN" -m unittest discover -s tests -v

echo "[2/4] 执行 Frontend tests"
cd "$FRONTEND_DIR"
if [[ ! -d node_modules ]]; then
  echo "未找到 node_modules，正在执行 npm install"
  npm install
fi
npm test

echo "[3/4] 执行 Frontend production build"
npm run build

echo "[4/4] 执行 Python compileall"
cd "$BACKEND_DIR"
"$PYTHON_BIN" -m compileall app

echo "全部本地测试与编译检查通过"
