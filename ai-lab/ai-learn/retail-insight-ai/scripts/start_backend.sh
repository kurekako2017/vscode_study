#!/usr/bin/env bash
set -euo pipefail

# 无论从哪个目录调用，都先定位到 retail-insight-ai 项目根目录。
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
VENV_DIR="$BACKEND_DIR/.venv"

echo "[1/4] 检查 Backend 虚拟环境"
if [[ ! -d "$VENV_DIR" ]]; then
  echo "未找到 backend/.venv，正在创建"
  python3 -m venv "$VENV_DIR"
else
  echo "已找到 backend/.venv"
fi

echo "[2/4] 安装或确认 Python 依赖"
"$VENV_DIR/bin/python" -m pip install -r "$BACKEND_DIR/requirements.txt"

echo "[3/4] 检查本地配置"
if [[ ! -f "$ROOT_DIR/.env" ]]; then
  cp "$ROOT_DIR/.env.example" "$ROOT_DIR/.env"
  echo "已从 .env.example 创建项目根目录 .env"
else
  echo "已找到项目根目录 .env"
fi

echo "[4/4] 启动 Backend：http://127.0.0.1:8000"
echo "按 Ctrl+C 停止服务"
cd "$BACKEND_DIR"
exec "$VENV_DIR/bin/python" -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
