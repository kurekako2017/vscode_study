#!/usr/bin/env bash
# 证明 .env 不会进入 Docker build context（不需要 daemon 也能做文件级检查）。

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail=0
for f in .dockerignore backend/.dockerignore frontend/.dockerignore; do
  if [[ ! -f "$f" ]]; then
    echo "MISSING $f" >&2
    fail=1
    continue
  fi
  if ! grep -qE '^\.env(\.\*)?$' "$f" && ! grep -q '\.env' "$f"; then
    echo "FAIL $f does not exclude .env" >&2
    fail=1
  else
    echo "OK $f excludes .env patterns"
  fi
done

# 确保 compose 默认 stub
if ! grep -q 'LLM_PROVIDER_MODE: stub' docker-compose.yml; then
  echo "FAIL compose not defaulting LLM_PROVIDER_MODE=stub" >&2
  fail=1
else
  echo "OK compose defaults LLM_PROVIDER_MODE=stub"
fi

# Dockerfile 不得 COPY .env（注释中的 “.env” 不算）
if grep -R --include='Dockerfile' -nE '^[[:space:]]*COPY[[:space:]].*\.env' backend frontend . 2>/dev/null \
  | grep -v example; then
  echo "FAIL Dockerfile copies .env" >&2
  fail=1
else
  echo "OK Dockerfiles do not COPY .env"
fi

exit "$fail"
