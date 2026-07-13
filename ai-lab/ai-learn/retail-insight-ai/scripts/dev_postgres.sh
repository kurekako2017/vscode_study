#!/usr/bin/env bash
set -euo pipefail

# 文件职责：统一本机 PostgreSQL Enterprise Mode 的临时环境与 Repository 测试入口。
# 谁调用它：开发者从项目根目录执行；它调用 pg_isready 与 backend unittest。
# 输入：可覆盖的 PGPASSFILE、DATABASE_URL；输出：连通性与 PostgreSQL 测试结果。
# 设计边界：不保存密码、不创建数据库/Role、不执行 schema.sql，也不运行 Alembic upgrade。
# 日本现场面试：开发脚本只做可重复验证，数据库变更必须走独立、可审查的 migration 流程。

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"

export PGPASSFILE="${PGPASSFILE:-/tmp/erip_pgpass}"
export DATABASE_URL="${DATABASE_URL:-postgresql://erip_test_user@127.0.0.1:5432/erip_integration_test}"
export REPOSITORY_BACKEND="postgres"

if [[ ! -f "$PGPASSFILE" ]]; then
  echo "PostgreSQL 验证失败：PGPASSFILE 不存在：$PGPASSFILE" >&2
  exit 1
fi

if [[ ! -r "$PGPASSFILE" ]]; then
  echo "PostgreSQL 验证失败：PGPASSFILE 不可读：$PGPASSFILE" >&2
  exit 1
fi

if ! command -v pg_isready >/dev/null 2>&1; then
  echo "PostgreSQL 验证失败：未找到 pg_isready" >&2
  exit 1
fi

if ! pg_isready -d "$DATABASE_URL" >/dev/null; then
  echo "PostgreSQL 验证失败：数据库未就绪或 DATABASE_URL 不可达" >&2
  exit 1
fi

if [[ -x "$BACKEND_DIR/.venv/bin/python" ]]; then
  PYTHON_BIN="$BACKEND_DIR/.venv/bin/python"
else
  PYTHON_BIN="python3"
fi

echo "PostgreSQL 已就绪，开始执行 Repository Integration Tests"
cd "$BACKEND_DIR"
"$PYTHON_BIN" -m unittest tests.test_postgres_repositories -v

echo "PostgreSQL Enterprise Mode 验证通过"
