#!/usr/bin/env bash
# export-and-upload.sh
# 在本地构建 Next.js 并导出静态文件，然后将 out/ 上传到 onamae（或其他远程主机）。
# 使用前请先检查并修改下面的变量。

set -euo pipefail

# 配置区：修改为你的项目路径与远程信息
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)/examples/headless-nextjs"
BUILD_CMD="npm run build"
EXPORT_CMD="npm run export"
# 远程信息
REMOTE_USER="youruser"
REMOTE_HOST="your-onamae-host.example.com"
REMOTE_PATH="/path/to/wwwroot"  # 目标站点根目录

# rsync 选项
RSYNC_OPTS="-avz --delete --omit-dir-times --no-perms"

# dry run 开关（1 = dry run, 0 = 执行）
DRY_RUN=1

usage(){
  echo "Usage: $0 [--run] [--user USER] [--host HOST] [--path PATH]"
  echo "  --run    : actually perform upload (default: dry-run)"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case $1 in
    --run) DRY_RUN=0; shift ;;
    --user) REMOTE_USER="$2"; shift 2 ;;
    --host) REMOTE_HOST="$2"; shift 2 ;;
    --path) REMOTE_PATH="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown arg: $1"; usage ;;
  esac
done

if [ -z "$REMOTE_USER" ] || [ -z "$REMOTE_HOST" ] || [ -z "$REMOTE_PATH" ]; then
  echo "请先在脚本顶部或通过参数设置 REMOTE_USER/REMOTE_HOST/REMOTE_PATH" >&2
  usage
fi

echo "[INFO] Project dir: ${PROJECT_DIR}"
cd "${PROJECT_DIR}"

echo "[INFO] Install dependencies (if needed)"
if [ ! -d node_modules ]; then
  npm install
fi

echo "[INFO] Run build: ${BUILD_CMD}"
${BUILD_CMD}

echo "[INFO] Run export: ${EXPORT_CMD}"
${EXPORT_CMD}

OUT_DIR="${PROJECT_DIR}/out"
if [ ! -d "${OUT_DIR}" ]; then
  echo "Export failed: ${OUT_DIR} not found" >&2
  exit 2
fi

SRC_DIR="${OUT_DIR}/"
DEST="${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/"

if [ "${DRY_RUN}" -eq 1 ]; then
  echo "[DRY RUN] rsync ${RSYNC_OPTS} --dry-run ${SRC_DIR} ${DEST}"
  rsync ${RSYNC_OPTS} --dry-run --exclude 'node_modules' "${SRC_DIR}" "${DEST}"
  echo "[INFO] Dry run complete. Rerun with --run to perform." 
else
  echo "[INFO] Executing rsync upload..."
  rsync ${RSYNC_OPTS} --exclude 'node_modules' "${SRC_DIR}" "${DEST}"
  echo "[INFO] Upload complete. Adjust permissions on remote if needed."
  echo "SSH to remote and run e.g.: chown -R www-data:www-data ${REMOTE_PATH}"
fi

echo "[DONE]"
