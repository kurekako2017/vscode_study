#!/usr/bin/env bash
set -euo pipefail

MODEL="${AIDER_MODEL:-ollama_chat/qwen2.5-coder:7b}"
OLLAMA_HOST="${OLLAMA_API_BASE:-http://127.0.0.1:11434}"
CHAT_LANGUAGE="${AIDER_CHAT_LANGUAGE:-zh}"
EDIT_FORMAT="${AIDER_EDIT_FORMAT:-diff}"
SHOW_DIFFS="${AIDER_SHOW_DIFFS:-true}"
AUTO_COMMITS="${AIDER_AUTO_COMMITS:-false}"
STREAMING="${AIDER_STREAMING:-true}"
MAP_TOKENS="${AIDER_MAP_TOKENS:-}"
SUBTREE_ONLY="${AIDER_SUBTREE_ONLY:-false}"
KEEP_SUBDIR="${AIDER_KEEP_SUBDIR:-false}"
PREWARM=0
PROJECT_PATH=""
AIDER_ARGS=()
AIDER_DEFAULT_ARGS=()
SCRIPT_NAME="$(basename "$0")"

apply_profile() {
  case "$1" in
    aiderwsl-fast)
      MODEL="${AIDER_MODEL_FAST:-ollama_chat/qwen2.5-coder:3b}"
      STREAMING=false
      PREWARM=0
      ;;
    aiderwsl-arch)
      MODEL="${AIDER_MODEL_ARCH:-ollama_chat/qwen2.5-coder:7b}"
      AIDER_ARGS+=(--architect)
      ;;
    aiderwsl-no-stream)
      STREAMING=false
      ;;
    aiderwsl-prewarm)
      PREWARM=1
      ;;
    aiderwsl-3b)
      MODEL="${AIDER_MODEL_3B:-ollama_chat/qwen2.5-coder:3b}"
      ;;
    aiderwsl-big)
      MAP_TOKENS="${AIDER_MAP_TOKENS_BIG:-0}"
      SUBTREE_ONLY=true
      KEEP_SUBDIR=true
      ;;
  esac
}

apply_profile "$SCRIPT_NAME"

usage() {
  cat <<'EOF'
Usage:
  aiderwsl [project_dir] [aider options]
  aiderwsl --project-dir <dir> [aider options]

Defaults:
  model: ollama_chat/qwen2.5-coder:7b
  chat-language: zh
  edit-format: diff
  auto-commits: false
  profile: default

Useful flags:
  --architect
  --no-stream
  --prewarm
  --map-tokens 0
  --subtree-only
  --model <model>
  --chat-language <lang>
  --edit-format <format>
  --auto-commits
  --no-auto-commits

Shortcut commands:
  aiderwsl-fast
  aiderwsl-arch
  aiderwsl-no-stream
  aiderwsl-prewarm
  aiderwsl-3b
  aiderwsl-big

Interactive commands inside Aider:
  /add <file>
  /drop <file>
  /ls
  /model <name>
  /help
  /exit
EOF
}

while (($#)); do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --model)
      MODEL="${2:-}"
      shift 2
      ;;
    --model=*)
      MODEL="${1#*=}"
      shift
      ;;
    --project-dir|--project-path)
      PROJECT_PATH="${2:-}"
      shift 2
      ;;
    --project-dir=*|--project-path=*)
      PROJECT_PATH="${1#*=}"
      shift
      ;;
    --chat-language)
      CHAT_LANGUAGE="${2:-}"
      shift 2
      ;;
    --chat-language=*)
      CHAT_LANGUAGE="${1#*=}"
      shift
      ;;
    --edit-format)
      EDIT_FORMAT="${2:-}"
      shift 2
      ;;
    --edit-format=*)
      EDIT_FORMAT="${1#*=}"
      shift
      ;;
    --auto-commits)
      AUTO_COMMITS=true
      shift
      ;;
    --no-auto-commits)
      AUTO_COMMITS=false
      shift
      ;;
    --stream)
      STREAMING=true
      shift
      ;;
    --no-stream)
      STREAMING=false
      shift
      ;;
    --architect|--no-auto-accept-architect|--auto-accept-architect|--pretty|--no-pretty|--show-diffs|--no-show-model-warnings)
      AIDER_ARGS+=("$1")
      shift
      ;;
    --prewarm)
      PREWARM=1
      shift
      ;;
    --map-tokens)
      MAP_TOKENS="${2:-}"
      shift 2
      ;;
    --map-tokens=*)
      MAP_TOKENS="${1#*=}"
      shift
      ;;
    --subtree-only)
      SUBTREE_ONLY=true
      KEEP_SUBDIR=true
      shift
      ;;
    --no-subtree-only)
      SUBTREE_ONLY=false
      shift
      ;;
    --keep-subdir)
      KEEP_SUBDIR=true
      shift
      ;;
    big)
      apply_profile "aiderwsl-big"
      shift
      ;;
    fast|arch|no-stream|prewarm|3b)
      apply_profile "aiderwsl-$1"
      shift
      ;;
    --)
      shift
      AIDER_ARGS+=("$@")
      break
      ;;
    *)
      if [ -z "$PROJECT_PATH" ] && [ -d "$1" ]; then
        PROJECT_PATH="$1"
      else
        AIDER_ARGS+=("$1")
      fi
      shift
      ;;
  esac
done

PROJECT_PATH="${PROJECT_PATH:-$PWD}"

if [ ! -d "$PROJECT_PATH" ]; then
  echo "Project path not found: $PROJECT_PATH" >&2
  exit 1
fi

if ! command -v ollama >/dev/null 2>&1; then
  echo "ollama command not found" >&2
  exit 1
fi

if ! command -v aider >/dev/null 2>&1; then
  echo "aider command not found" >&2
  exit 1
fi

export OLLAMA_API_BASE="$OLLAMA_HOST"
export OPENAI_API_KEY="${OPENAI_API_KEY:-na}"

if ! curl -fsS "$OLLAMA_HOST/api/tags" >/dev/null 2>&1; then
  nohup ollama serve >/tmp/ollama-serve.log 2>&1 &
  for _ in $(seq 1 20); do
    if curl -fsS "$OLLAMA_HOST/api/tags" >/dev/null 2>&1; then
      break
    fi
    sleep 1
  done
fi

if ! curl -fsS "$OLLAMA_HOST/api/tags" >/dev/null 2>&1; then
  echo "Ollama is not reachable at $OLLAMA_HOST" >&2
  echo "Check /tmp/ollama-serve.log for startup output." >&2
  exit 1
fi

if git -C "$PROJECT_PATH" rev-parse --show-toplevel >/dev/null 2>&1; then
  if [ "$KEEP_SUBDIR" != true ]; then
    PROJECT_PATH="$(git -C "$PROJECT_PATH" rev-parse --show-toplevel)"
  fi
else
  echo "Warning: $PROJECT_PATH is not a git repo. Aider works best inside git." >&2
fi

if [ "$PREWARM" -eq 1 ]; then
  OLLAMA_MODEL="${MODEL#ollama_chat/}"
  OLLAMA_MODEL="${OLLAMA_MODEL#ollama/}"
  echo "Prewarming Ollama model: $OLLAMA_MODEL"
  ollama run "$OLLAMA_MODEL" "warmup" >/dev/null
fi

if [ "$SHOW_DIFFS" = true ]; then
  AIDER_DEFAULT_ARGS+=(--show-diffs)
fi

if [ "$STREAMING" = true ]; then
  AIDER_DEFAULT_ARGS+=(--stream)
else
  AIDER_DEFAULT_ARGS+=(--no-stream)
fi

if [ "$AUTO_COMMITS" = true ]; then
  AIDER_DEFAULT_ARGS+=(--auto-commits)
else
  AIDER_DEFAULT_ARGS+=(--no-auto-commits)
fi

if [ -n "$MAP_TOKENS" ]; then
  AIDER_DEFAULT_ARGS+=(--map-tokens "$MAP_TOKENS")
fi

if [ "$SUBTREE_ONLY" = true ]; then
  AIDER_DEFAULT_ARGS+=(--subtree-only)
fi

cd "$PROJECT_PATH"
exec aider \
  --model "$MODEL" \
  --chat-language "$CHAT_LANGUAGE" \
  --edit-format "$EDIT_FORMAT" \
  "${AIDER_DEFAULT_ARGS[@]}" \
  "${AIDER_ARGS[@]}"
