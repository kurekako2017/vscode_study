#!/usr/bin/env bash
set -euo pipefail

# Docker 是可选项；Python、pip、Node 和 npm 是本地双服务运行的必需项。
missing_required=0

echo "检查本地开发环境"

if command -v python3 >/dev/null 2>&1; then
  echo -n "python3: "
  python3 --version
else
  echo "python3: 未安装"
  missing_required=1
fi

if command -v python3 >/dev/null 2>&1 && python3 -m pip --version >/dev/null 2>&1; then
  echo -n "pip: "
  python3 -m pip --version
else
  echo "pip: 未安装（可安装 python3-pip）"
  missing_required=1
fi

if command -v node >/dev/null 2>&1; then
  echo -n "node: "
  node -v
else
  echo "node: 未安装"
  missing_required=1
fi

if command -v npm >/dev/null 2>&1; then
  echo -n "npm: "
  npm -v
else
  echo "npm: 未安装"
  missing_required=1
fi

if command -v docker >/dev/null 2>&1; then
  echo -n "docker（可选）: "
  docker --version
else
  echo "docker（可选）: 未安装；不影响 Backend + Frontend 本地运行"
fi

if [[ "$missing_required" -ne 0 ]]; then
  echo "缺少必需工具，请根据上面的提示安装后重新执行。"
  exit 1
fi

echo "必需工具检查通过"
