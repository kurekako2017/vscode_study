#!/usr/bin/env bash
set -euo pipefail

# Helper script to run rag_api_demo in development.
# Tries to create a venv and install dependencies. If venv creation is not
# available, prints Docker instructions as a fallback.

PROJECT_DIR=$(cd "$(dirname "$0")" && pwd)
VENV_DIR="$PROJECT_DIR/.venv"

run_server() {
  export RAG_API_MOCK=1
  uvicorn main:app --reload --port 8000 --host 127.0.0.1
}

if python3 -m venv "$VENV_DIR" 2>/dev/null; then
  echo "Created venv at $VENV_DIR"
  # shellcheck source=/dev/null
  . "$VENV_DIR/bin/activate"
  pip install --upgrade pip setuptools wheel
  pip install -r "$PROJECT_DIR/requirements.txt"
  run_server
  exit 0
fi

if python3 -c "import fastapi, uvicorn, openai, pypdf" 2>/dev/null; then
  echo "python3 -m venv is unavailable, reusing current Python environment."
  run_server
  exit 0
fi

cat <<'EOF'
Could not create a virtual environment (python3 -m venv failed).
Two recommended alternatives:

1) Install system venv support and retry (Linux Debian/Ubuntu):
   sudo apt install python3-venv
   then run: ./run-dev.sh

2) Install dependencies into the current Python environment, then rerun:
   python3 -m pip install -r requirements.txt
   ./run-dev.sh

3) Use Docker (recommended when Python env is managed):
   # build image
   docker build -t rag_api_demo:dev .
   # run service in mock mode
   docker run -e RAG_API_MOCK=1 -p 8000:8000 rag_api_demo:dev

EOF
