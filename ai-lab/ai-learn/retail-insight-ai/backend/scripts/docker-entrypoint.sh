#!/usr/bin/env sh
# Backend 容器启动：PostgreSQL ready → Alembic upgrade head → 启动应用。
# Migration 失败时不启动 uvicorn。日志不含 Secret。

set -eu

log() {
  echo "[backend-entrypoint] $*"
}

# 规范化 DATABASE_URL（支持 postgresql:// 与 postgresql+psycopg://）
if [ -z "${DATABASE_URL:-}" ]; then
  PGHOST="${POSTGRES_HOST:-postgres}"
  PGPORT="${POSTGRES_PORT:-5432}"
  PGUSER="${POSTGRES_USER:-erip_app}"
  PGPASS="${POSTGRES_PASSWORD:-}"
  PGDB="${POSTGRES_DB:-erip}"
  if [ -z "$PGPASS" ]; then
    log "ERROR: DATABASE_URL or POSTGRES_PASSWORD required"
    exit 1
  fi
  export DATABASE_URL="postgresql+psycopg://${PGUSER}:${PGPASS}@${PGHOST}:${PGPORT}/${PGDB}"
fi

# Alembic 需要可连接 URL；env.py 会规范化驱动前缀。
export REPOSITORY_BACKEND="${REPOSITORY_BACKEND:-postgres}"
export LLM_PROVIDER_MODE="${LLM_PROVIDER_MODE:-stub}"
export RUN_REAL_LLM_SMOKE="${RUN_REAL_LLM_SMOKE:-0}"

log "waiting for PostgreSQL..."
python - <<'PY'
import os, sys, time
import psycopg

url = os.environ["DATABASE_URL"].replace("postgresql+psycopg://", "postgresql://", 1)
deadline = time.time() + float(os.environ.get("POSTGRES_WAIT_SECONDS", "60"))
last = None
while time.time() < deadline:
    try:
        with psycopg.connect(url, connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        print("[backend-entrypoint] PostgreSQL is ready", flush=True)
        sys.exit(0)
    except Exception as exc:  # noqa: BLE001
        last = type(exc).__name__
        time.sleep(1.5)
print(f"[backend-entrypoint] ERROR: PostgreSQL not ready ({last})", flush=True)
sys.exit(1)
PY

log "running alembic upgrade head..."
alembic upgrade head
log "alembic current:"
alembic current || true

log "starting application: $*"
exec "$@"
