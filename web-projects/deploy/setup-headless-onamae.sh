#!/usr/bin/env bash
# setup-headless-onamae.sh
# 用于在 onamae RS 的 WordPress 实例上快速安装 WPGraphQL 与 JWT 插件的示例脚本（需在服务器上运行）

set -euo pipefail

WP_PATH="/var/www/html" # 修改为你的 WordPress 路径

echo "[INFO] 安装 WPGraphQL（wp-graphql）和 JWT 插件"
cd ${WP_PATH}

# 安装 WPGraphQL
wp plugin install graphql --activate --allow-root

# 安装 WPGraphQL JWT Auth（请替换为实际插件 slug）
wp plugin install wp-graphql-jwt-authentication --activate --allow-root || echo "JWT plugin may not exist with this slug; check plugin slug"

echo "[INFO] 完成。请在 WP 后台检查插件并配置 GraphQL 权限与身份验证设置。"

echo "建议：在 wp-config.php 中设置以下常量或通过服务器环境变量管理密钥："
echo "  define('WPGRAPHQL_JWT_SECRET_KEY', getenv('WPGRAPHQL_JWT_SECRET_KEY'));"

echo "若需在 content publish 时触发前端构建，请在 WordPress 中添加 webhook，或使用以下示例 curl 在发布后手动触发："
echo "  curl -X POST https://vercel.com/api/deploy?token=YOUR_TOKEN"
