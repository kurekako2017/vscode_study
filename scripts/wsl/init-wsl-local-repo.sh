#!/usr/bin/env bash

set -euo pipefail

# 脚本: init-wsl-local-repo.sh
# 说明: 将当前仓库复制到 WSL Home 工作区，便于长期高性能开发。
# 用法:
#   bash ./scripts/wsl/init-wsl-local-repo.sh
#   bash ./scripts/wsl/init-wsl-local-repo.sh /mnt/d/dev/source_code/vscode_study ~/workspace/vscode_study

SOURCE_REPO="${1:-/mnt/d/dev/source_code/vscode_study}"
TARGET_REPO="${2:-$HOME/workspace/vscode_study}"

if [[ ! -d "$SOURCE_REPO" ]]; then
  echo "[ERROR] Source repo not found: $SOURCE_REPO"
  exit 1
fi

if [[ ! -d "$SOURCE_REPO/.git" ]]; then
  echo "[ERROR] Source path is not a git repository: $SOURCE_REPO"
  exit 1
fi

if [[ -e "$TARGET_REPO" ]]; then
  if [[ -d "$TARGET_REPO/.git" ]]; then
    echo "[INFO] Target repo already exists: $TARGET_REPO"
    echo "[INFO] No action taken. Open it with:"
    echo "       cd \"$TARGET_REPO\" && code ."
    exit 0
  fi

  echo "[ERROR] Target path exists but is not a git repository: $TARGET_REPO"
  echo "[INFO] Remove or rename it, then run the script again."
  exit 1
fi

mkdir -p "$(dirname "$TARGET_REPO")"

echo "[INFO] Copying repository into WSL local workspace..."
echo "[INFO] Source: $SOURCE_REPO"
echo "[INFO] Target: $TARGET_REPO"

cp -a "$SOURCE_REPO" "$TARGET_REPO"

echo "[INFO] Done. Next steps:"
echo "       cd \"$TARGET_REPO\""
echo "       code ."
echo "       bash ./scripts/wsl/dev-check-gitbash.sh"
