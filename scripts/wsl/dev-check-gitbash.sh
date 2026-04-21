#!/usr/bin/env bash

# 用于 Windows Git Bash 开发流程的快速环境检查。
# 可重复执行且不会破坏现有环境。

set -u

PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

ok() {
  PASS_COUNT=$((PASS_COUNT + 1))
  echo "[PASS] $1"
}

warn() {
  WARN_COUNT=$((WARN_COUNT + 1))
  echo "[WARN] $1"
}

fail() {
  FAIL_COUNT=$((FAIL_COUNT + 1))
  echo "[FAIL] $1"
}

has_cmd() {
  command -v "$1" >/dev/null 2>&1
}

print_header() {
  echo
  echo "=== $1 ==="
}

check_cmd_version() {
  local cmd="$1"
  local version_cmd="$2"
  local label="$3"

  if has_cmd "$cmd"; then
    local v
    v=$(eval "$version_cmd" 2>/dev/null | head -n 1)
    ok "$label: ${v:-installed}"
  else
    fail "$label not found"
  fi
}

check_optional_cmd_version() {
  local cmd="$1"
  local version_cmd="$2"
  local label="$3"

  if has_cmd "$cmd"; then
    local v
    v=$(eval "$version_cmd" 2>/dev/null | head -n 1)
    ok "$label: ${v:-installed}"
  else
    warn "$label not found (optional)"
  fi
}

check_env_var() {
  local name="$1"
  local value="${!name:-}"

  if [ -n "$value" ]; then
    ok "$name is set"
  else
    warn "$name is not set"
  fi
}

print_header "Shell"
if [ -n "${MSYSTEM:-}" ]; then
  ok "Running in Git Bash/MSYS2 (${MSYSTEM})"
else
  warn "Not in Git Bash/MSYS2 (MSYSTEM is empty)"
fi

check_cmd_version git "git --version" "Git"
check_optional_cmd_version ssh "ssh -V" "OpenSSH"
check_optional_cmd_version code "code --version" "VS Code CLI"

print_header "Java"
check_optional_cmd_version java "java -version" "Java runtime"
check_optional_cmd_version javac "javac -version" "Java compiler"
check_optional_cmd_version mvn "mvn -v" "Maven"

if [ -x "./mvnw" ]; then
  if ./mvnw -v >/dev/null 2>&1; then
    ok "Maven Wrapper (./mvnw) is executable"
  else
    warn "Maven Wrapper exists but failed to run"
  fi
elif [ -f "./mvnw" ]; then
  warn "Maven Wrapper found but not executable (run: chmod +x ./mvnw)"
else
  warn "No Maven Wrapper in current directory"
fi

print_header "Python"
check_optional_cmd_version python "python --version" "Python"
check_optional_cmd_version pip "pip --version" "pip"
check_optional_cmd_version uv "uv --version" "uv"

if [ -d ".venv" ]; then
  ok ".venv directory found"
else
  warn ".venv directory not found in current directory"
fi

if [ -f ".venv/Scripts/activate" ]; then
  ok "Virtualenv activation script exists (.venv/Scripts/activate)"
else
  warn "No .venv/Scripts/activate in current directory"
fi

print_header "LLM / Local AI"
check_env_var OPENAI_API_KEY
check_env_var ANTHROPIC_API_KEY
check_env_var GEMINI_API_KEY
check_optional_cmd_version ollama "ollama --version" "Ollama"

print_header "Workspace hint"
printf 'Current directory: %s\n' "$(pwd)"
printf 'Tip: cd /d/dev/source_code/vscode_study\n'

echo
printf 'Summary: PASS=%s WARN=%s FAIL=%s\n' "$PASS_COUNT" "$WARN_COUNT" "$FAIL_COUNT"

if [ "$FAIL_COUNT" -gt 0 ]; then
  exit 1
fi

exit 0