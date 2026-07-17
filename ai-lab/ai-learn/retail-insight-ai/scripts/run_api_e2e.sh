#!/usr/bin/env bash
# 最小企业业务 API E2E（Stub LLM，零真实外呼）。
# 默认连 http://127.0.0.1:8000；可用 BASE_URL 覆盖。

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR/backend"

if [[ -x .venv/bin/python ]]; then
  PY=.venv/bin/python
else
  PY=python3
fi

export E2E_BASE_URL="${E2E_BASE_URL:-http://127.0.0.1:8000}"
export E2E_EXPECT_STUB="${E2E_EXPECT_STUB:-1}"

echo "[api_e2e] BASE_URL=$E2E_BASE_URL"
"$PY" -m tests.test_e2e_api_stub_flow
