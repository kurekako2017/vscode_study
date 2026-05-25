#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="${SCRIPT_DIR}/.."
cd "${LAB_ROOT}"

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip

REQ_FILE="${LAB_ROOT}/projects/hello-localstack/requirements.txt"
if [ -f "${REQ_FILE}" ]; then
  pip install -r "${REQ_FILE}"
fi

echo "LocalStack lab environment ready. Activate with: source ${LAB_ROOT}/.venv/bin/activate"
