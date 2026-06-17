#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# 允许通过环境变量切换 compose 文件，默认使用 NAS 场景的编排配置。
COMPOSE_FILE="${COMPOSE_FILE:-docker/docker-compose.nas.yaml}"
MODE="${1:-up}"

case "$MODE" in
  up)
    # 启动本地依赖栈，默认后台运行。
    echo "Starting local stack with ${COMPOSE_FILE}"
    docker compose -f "$COMPOSE_FILE" up -d
    ;;
  down)
    # 关闭整个本地依赖栈。
    echo "Stopping local stack with ${COMPOSE_FILE}"
    docker compose -f "$COMPOSE_FILE" down
    ;;
  ps)
    # 查看当前 compose 服务状态。
    docker compose -f "$COMPOSE_FILE" ps
    ;;
  logs)
    # 跟踪日志，后面可以继续追加服务名参数。
    shift || true
    docker compose -f "$COMPOSE_FILE" logs -f "$@"
    ;;
  *)
    echo "Usage: $0 {up|down|ps|logs}"
    exit 1
    ;;
esac
