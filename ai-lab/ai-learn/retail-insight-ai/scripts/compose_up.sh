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

# 默认端口来自环境或 compose 默认（不要求用户每次 export）
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-8080}"
POSTGRES_PORT="${POSTGRES_PORT:-5432}"

port_busy() {
  local port="$1"
  if command -v ss >/dev/null 2>&1; then
    ss -ltn 2>/dev/null | grep -qE ":${port}[[:space:]]"
    return $?
  fi
  return 1
}

echo "[compose_up] validating compose config..."
docker compose config >/dev/null

for p in "$POSTGRES_PORT" "$BACKEND_PORT" "$FRONTEND_PORT"; do
  if port_busy "$p"; then
    echo "[compose_up] WARNING: 宿主端口 ${p} 似乎已被占用。" >&2
    echo "[compose_up] 若 compose 启动失败，请先释放端口，或一次性覆盖例如：" >&2
    echo "[compose_up]   export POSTGRES_PORT=5433   # 仅冲突时需要" >&2
    echo "[compose_up] 不会自动杀死占用进程。" >&2
  fi
done

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
