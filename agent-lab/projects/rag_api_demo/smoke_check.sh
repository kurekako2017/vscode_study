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

echo "Response: $RESP"

# Basic JSON validation: ensure 'answer' and 'source_count' keys exist
python3 - <<'PY'
import sys, json
try:
    obj = json.loads(sys.stdin.read())
except Exception as e:
    print('ERROR: response is not valid JSON:', e, file=sys.stderr)
    sys.exit(1)

if 'answer' not in obj or 'source_count' not in obj:
    print('ERROR: required fields missing in response. Keys:', list(obj.keys()), file=sys.stderr)
    sys.exit(1)

print('OK: /ask returned required fields (answer, source_count)')
PY <<EOF
$RESP
EOF
