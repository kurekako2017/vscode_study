#!/usr/bin/env bash
set -euo pipefail

# 脚本自行定位项目目录，调用者不必手工 cd 到 frontend。
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"

echo "[1/2] 检查 Frontend 依赖"
cd "$FRONTEND_DIR"
if [[ ! -d node_modules ]]; then
  echo "未找到 node_modules，正在执行 npm install"
  npm install
else
  echo "已找到 node_modules，跳过 npm install"
fi

echo "[2/2] 启动 Frontend：http://127.0.0.1:5173"
echo "按 Ctrl+C 停止服务"
exec npm run dev -- --host 127.0.0.1
