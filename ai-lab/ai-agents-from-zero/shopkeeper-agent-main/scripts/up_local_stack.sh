#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

COMPOSE_FILE="${COMPOSE_FILE:-docker/docker-compose.nas.yaml}"
MODE="${1:-up}"

case "$MODE" in
  up)
    echo "Starting local stack with ${COMPOSE_FILE}"
    docker compose -f "$COMPOSE_FILE" up -d
    ;;
  down)
    echo "Stopping local stack with ${COMPOSE_FILE}"
    docker compose -f "$COMPOSE_FILE" down
    ;;
  ps)
    docker compose -f "$COMPOSE_FILE" ps
    ;;
  logs)
    shift || true
    docker compose -f "$COMPOSE_FILE" logs -f "$@"
    ;;
  *)
    echo "Usage: $0 {up|down|ps|logs}"
    exit 1
    ;;
esac
