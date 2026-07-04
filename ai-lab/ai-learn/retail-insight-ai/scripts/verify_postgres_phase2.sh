#!/usr/bin/env bash
set -euo pipefail

# Phase 2 的 PostgreSQL 验证入口：
# 1. 先检查当前环境是否具备 psycopg 与 Docker
# 2. 条件满足时自动拉起 postgres 并执行最小 Repository 集成测试
# 3. 条件不满足时明确输出跳过原因和后续手动命令

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
STRICT_MODE="${VERIFY_POSTGRES_STRICT:-false}"

if [[ -x "$BACKEND_DIR/.venv/bin/python" ]]; then
  PYTHON_BIN="$BACKEND_DIR/.venv/bin/python"
  echo "使用 backend/.venv/bin/python"
else
  PYTHON_BIN="python3"
  echo "未找到 backend/.venv，使用系统 python3"
fi

skip_verify() {
  local reason="$1"
  echo "PostgreSQL Phase 2 验证跳过: $reason"
  echo "建议先满足以下条件后重试："
  echo "1. 在 backend Python 环境中安装 requirements.txt（需要 psycopg[binary]）"
  echo "2. 安装并启动 Docker CLI / Docker Engine"
  echo "3. 在项目根目录重新执行 ./scripts/verify_postgres_phase2.sh"
  echo
  echo "手动验证命令："
  echo "  docker compose up -d postgres"
  echo "  cd backend"
  echo "  source .venv/bin/activate"
  echo "  REPOSITORY_BACKEND=postgres python -m unittest tests.test_postgres_repositories -v"
  if [[ "$STRICT_MODE" == "true" ]]; then
    exit 1
  fi
  exit 0
}

if ! "$PYTHON_BIN" -c "import psycopg" >/dev/null 2>&1; then
  skip_verify "当前 Python 环境缺少 psycopg"
fi

if ! command -v docker >/dev/null 2>&1; then
  skip_verify "当前环境缺少 docker CLI"
fi

cleanup() {
  cd "$ROOT_DIR"
  docker compose stop postgres >/dev/null 2>&1 || true
}

trap cleanup EXIT

cd "$ROOT_DIR"
echo "[1/2] 启动 PostgreSQL 容器"
docker compose up -d postgres

echo "[2/2] 执行 PostgreSQL Repository 集成测试"
cd "$BACKEND_DIR"
REPOSITORY_BACKEND=postgres "$PYTHON_BIN" -m unittest tests.test_postgres_repositories -v

echo "PostgreSQL Phase 2 验证通过"
