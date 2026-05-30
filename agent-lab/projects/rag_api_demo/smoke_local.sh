#!/usr/bin/env bash
set -euo pipefail

# 简易本地 smoke test：启动服务（mock）、等待 /health、调用 /ask、验证返回并清理。
# 用法：在仓库根或任意地方运行此脚本（会自动 cd 到脚本目录）

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

PORT=8000
HOST=127.0.0.1
UVICORN_CMD=(uvicorn main:app --reload --port "$PORT" --host "$HOST")

export RAG_API_MOCK=1

echo "Starting rag_api_demo (mock) with: ${UVICORN_CMD[*]}"
"${UVICORN_CMD[@]}" > server.log 2>&1 &
PID=$!
echo "Server PID: $PID"

cleanup() {
  echo "Stopping server PID $PID..."
  kill "$PID" 2>/dev/null || true
  wait "$PID" 2>/dev/null || true
}
trap cleanup EXIT

echo -n "Waiting for /health"
for i in $(seq 1 30); do
  sleep 1
  HEALTH=$(curl -s "http://$HOST:$PORT/health" || true)
  if echo "$HEALTH" | python3 - <<'PY'
import sys, json
s=sys.stdin.read()
try:
    j=json.loads(s)
except Exception:
    sys.exit(1)
if j.get('status')=='ok':
    sys.exit(0)
sys.exit(1)
PY
  then
    echo " -> OK"
    break
  fi
  echo -n "."
  if [ "$i" -eq 30 ]; then
    echo ""
    echo "ERROR: service did not become healthy within timeout. Check server.log for details." >&2
    exit 2
  fi
done

echo "Posting /ask..."
RESP=$(curl -s -X POST "http://$HOST:$PORT/ask" -H "Content-Type: application/json" -d '{"question":"smoke test"}' || true)
echo "Response: $RESP"

echo "$RESP" | python3 - <<'PY'
import sys, json
try:
    j=json.loads(sys.stdin.read())
except Exception as e:
    print('FAILED: response not valid JSON', e)
    sys.exit(2)
if not ('answer' in j and 'source_count' in j):
    print('FAILED: missing keys in response:', list(j.keys()))
    sys.exit(3)
print('SMOKE TEST PASSED')
sys.exit(0)
PY

# cleanup via trap
