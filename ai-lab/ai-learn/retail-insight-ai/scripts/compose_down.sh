#!/usr/bin/env bash
# 正常停止 Compose。禁止 -v，保留用户数据 volume。

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker CLI 不可用" >&2
  exit 1
fi

# 明确拒绝危险参数
for arg in "$@"; do
  if [[ "$arg" == "-v" || "$arg" == "--volumes" ]]; then
    echo "ERROR: 禁止 docker compose down -v（会删除数据 volume）" >&2
    exit 2
  fi
done

echo "[compose_down] stopping services (volumes preserved)..."
docker compose down
echo "[compose_down] done"
