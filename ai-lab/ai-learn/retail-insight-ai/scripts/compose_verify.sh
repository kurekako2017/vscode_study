#!/usr/bin/env bash
# Compose 健康与安全检查（不打印 Secret）。

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

BACKEND_URL="${BACKEND_URL:-http://127.0.0.1:${BACKEND_PORT:-8000}}"
FRONTEND_URL="${FRONTEND_URL:-http://127.0.0.1:${FRONTEND_PORT:-8080}}"

echo "[compose_verify] compose config"
docker compose config >/dev/null

echo "[compose_verify] backend health"
curl -fsS "$BACKEND_URL/health" | head -c 400
echo

echo "[compose_verify] frontend root"
code=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL/")
echo "frontend_http=$code"
[[ "$code" == "200" ]]

echo "[compose_verify] SPA routes return index (not 404)"
for path in /login /dashboard /documents /rag /analysis /approval; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL$path")
  echo "  $path -> $code"
  [[ "$code" == "200" ]]
done

echo "[compose_verify] .env not in backend image (if image exists)"
if docker image inspect erip-backend >/dev/null 2>&1 || docker compose images backend >/dev/null 2>&1; then
  img=$(docker compose images -q backend 2>/dev/null | head -1 || true)
  if [[ -n "$img" ]]; then
    if docker run --rm --entrypoint sh "$img" -c 'ls -la /app/.env 2>/dev/null' 2>/dev/null; then
      echo "ERROR: .env found inside backend image" >&2
      exit 1
    fi
    echo "  backend image has no /app/.env (expected)"
  fi
fi

echo "[compose_verify] ok"
