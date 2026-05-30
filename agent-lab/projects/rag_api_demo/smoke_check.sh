#!/usr/bin/env bash
set -euo pipefail

# 简单的 /ask POST smoke test，用于 CI 或本地容器运行后的快速验证
HOST=${HOST:-http://localhost:8000}
PAYLOAD='{"question":"健康检查：请返回简短确认。"}'

echo "POST $HOST/ask -> payload: $PAYLOAD"
RESP=$(curl -sS -H "Content-Type: application/json" -d "$PAYLOAD" "$HOST/ask") || true

if [ -z "$RESP" ]; then
  echo "ERROR: empty response from /ask" >&2
  exit 1
fi

echo "OK: /ask responded"
echo "$RESP"
