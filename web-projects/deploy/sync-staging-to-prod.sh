#!/usr/bin/env bash
# sync-staging-to-prod.sh
# 示例：从 staging 同步指定目录到 production，包含备份、路径替换与权限调整。

set -euo pipefail

# 配置区域 —— 请根据你的环境修改
STAGING_USER="user"
STAGING_HOST="staging.example.com"
STAGING_PATH="/var/www/staging"

PROD_PATH="/var/www/html"
PROD_USER="root"

# 要同步的相对目录（相对于 WordPress 根）
SYNC_DIRS=("wp-content/uploads" "wp-content/plugins/your-custom-plugin" "wp-content/themes/your-theme/dist")

# rsync 选项
RSYNC_OPTS="-avz --delete --omit-dir-times --no-perms"

# 备份目录（在生产服务器上保存当前状态以便回滚）
BACKUP_DIR="/backup/wordpress_$(date +%F-%T)"

DRY_RUN=1 # 1 = dry run, 0 = execute

echo "[INFO] 启动同步脚本（DRY_RUN=${DRY_RUN}）"

echo "[INFO] 在生产创建备份目录 ${BACKUP_DIR}"
ssh ${PROD_USER}@${STAGING_HOST} "mkdir -p ${BACKUP_DIR} || true"

echo "[INFO] 导出生产 DB（请确认在 production 上运行或改为调用远程命令）"
ssh ${PROD_USER}@${STAGING_HOST} "wp db export ${BACKUP_DIR}/prod-backup.sql --path=${PROD_PATH}"

for dir in "${SYNC_DIRS[@]}"; do
  SRC="${STAGING_USER}@${STAGING_HOST}:${STAGING_PATH}/${dir}/"
  DEST="${PROD_PATH}/${dir}/"
  echo "[INFO] 同步 ${SRC} -> ${DEST}"
  if [ "${DRY_RUN}" -eq 1 ]; then
    rsync ${RSYNC_OPTS} --dry-run --exclude 'cache/' "${SRC}" "${DEST}"
  else
    # 先备份被覆盖的文件（可选）
    rsync ${RSYNC_OPTS} --backup --backup-dir=${BACKUP_DIR} --exclude 'cache/' "${SRC}" "${DEST}"
  fi
done

echo "[INFO] 如果需要替换 URL，请在 production 上运行 WP-CLI 的 search-replace："
echo "wp search-replace 'https://staging.example.com' 'https://example.com' --path=${PROD_PATH} --skip-columns=guid"

echo "[INFO] 同步完成（DRY_RUN=${DRY_RUN}）。请在 production 上手动调整权限并清理缓存："
echo "chown -R www-data:www-data ${PROD_PATH}/wp-content"
echo "wp cache flush --path=${PROD_PATH}"

echo "[DONE] 完成。"
