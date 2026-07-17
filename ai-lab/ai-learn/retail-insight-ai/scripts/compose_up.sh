#!/usr/bin/env bash
# 一键启动 ERIP Compose（默认 Stub LLM）。
# 不删除 volume；不打印 Secret。

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker CLI 不可用（当前环境可能未启用 Docker Desktop WSL 集成）" >&2
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "ERROR: Docker daemon 未运行" >&2
  exit 1
fi

echo "[compose_up] validating compose config..."
docker compose config >/dev/null

echo "[compose_up] building images..."
docker compose build

echo "[compose_up] starting services..."
docker compose up -d

echo "[compose_up] waiting for health..."
for i in $(seq 1 60); do
  if docker compose ps --format json 2>/dev/null | grep -q '"Health":"healthy"' \
    || docker compose ps | grep -E 'healthy' >/dev/null 2>&1; then
    backend_ok=0
    frontend_ok=0
    curl -fsS "http://127.0.0.1:${BACKEND_PORT:-8000}/health" >/dev/null 2>&1 && backend_ok=1
    curl -fsS "http://127.0.0.1:${FRONTEND_PORT:-8080}/" >/dev/null 2>&1 && frontend_ok=1
    if [[ "$backend_ok" -eq 1 && "$frontend_ok" -eq 1 ]]; then
      echo "[compose_up] healthy: frontend + backend"
      docker compose ps
      exit 0
    fi
  fi
  sleep 2
done

echo "[compose_up] ERROR: services not healthy in time" >&2
docker compose ps >&2 || true
docker compose logs --tail=80 backend >&2 || true
exit 1
