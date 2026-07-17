#!/usr/bin/env bash
# 停止由 start_local.sh 启动并记录的本地 Backend / Frontend。
# 不停止 PostgreSQL；不影响 Docker Compose；禁止宽泛 pkill/killall。
#
# 用法：./scripts/stop_local.sh
#
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_DIR="$ROOT_DIR/.run"
BACKEND_PID_FILE="$RUN_DIR/local_backend.pid"
FRONTEND_PID_FILE="$RUN_DIR/local_frontend.pid"

log() { echo "[stop_local] $*"; }
err() { echo "[stop_local] ERROR: $*" >&2; }

pid_alive() {
  local pid="$1"
  [[ -n "${pid:-}" ]] && kill -0 "$pid" 2>/dev/null
}

read_cmdline() {
  local pid="$1"
  if [[ -r "/proc/${pid}/cmdline" ]]; then
    tr '\0' ' ' <"/proc/${pid}/cmdline" || true
  else
    ps -p "$pid" -o args= 2>/dev/null || true
  fi
}

# 仅当 cmdline 匹配允许模式之一，且（可选）像本仓库启动时才 kill
safe_kill_pidfile() {
  local name="$1"
  local pidfile="$2"
  shift 2
  # remaining: allowed substrings in cmdline (OR)

  if [[ ! -f "$pidfile" ]]; then
    log "${name}: 无 PID 文件（可能未由 start_local 启动）"
    return 0
  fi

  local pid
  pid="$(tr -d '[:space:]' <"$pidfile" || true)"
  if [[ -z "$pid" ]]; then
    log "${name}: PID 文件为空，清理"
    rm -f "$pidfile"
    return 0
  fi

  if ! pid_alive "$pid"; then
    log "${name}: PID ${pid} 已不存在，清理文件"
    rm -f "$pidfile"
    return 0
  fi

  local cmdline
  cmdline="$(read_cmdline "$pid")"
  if [[ -z "$cmdline" ]]; then
    err "${name}: 无法读取 PID ${pid} 命令行，为安全起见不杀进程；清理 PID 文件"
    rm -f "$pidfile"
    return 0
  fi

  local matched=0
  local pat
  for pat in "$@"; do
    if [[ "$cmdline" == *"$pat"* ]]; then
      matched=1
      break
    fi
  done

  # 额外要求：与本项目相关，或匹配 uvicorn/vite/npm 典型启动
  if [[ "$matched" -eq 0 ]]; then
    err "${name}: PID ${pid} 不像 start_local 启动的进程，跳过 kill"
    err "  cmdline 摘要：$(echo "$cmdline" | cut -c1-120)"
    rm -f "$pidfile"
    return 0
  fi

  log "${name}: 停止 PID ${pid}（优先进程组）"
  # setsid 启动时，负 PID 表示向整个进程组发信号（仍是精确 kill，非 pkill）
  kill -- "-${pid}" 2>/dev/null || kill "$pid" 2>/dev/null || true
  local i
  for i in $(seq 1 25); do
    pid_alive "$pid" || break
    sleep 0.2
  done
  if pid_alive "$pid"; then
    log "${name}: 再次 SIGTERM"
    kill -- "-${pid}" 2>/dev/null || kill "$pid" 2>/dev/null || true
    sleep 0.5
  fi
  if pid_alive "$pid"; then
    log "${name}: SIGKILL PID ${pid}"
    kill -9 -- "-${pid}" 2>/dev/null || kill -9 "$pid" 2>/dev/null || true
  fi
  rm -f "$pidfile"
  log "${name}: 已停止"
}

# 若 nohup 记录的是 npm 父进程，子进程 vite(node) 可能仍占用 5173。
# 仅当 cmdline 匹配本仓库 frontend 的 vite，且端口为本脚本固定 5173 时才停。
stop_orphan_vite_on_port() {
  local port="${1:-5173}"
  local root_marker="$ROOT_DIR/frontend"
  local pid cmdline cwd
  # 从 ss 解析 LISTEN 进程（不使用 pkill/killall）
  while read -r pid; do
    [[ -z "${pid:-}" ]] && continue
    if ! pid_alive "$pid"; then
      continue
    fi
    cmdline="$(read_cmdline "$pid")"
    cwd=""
    if [[ -r "/proc/${pid}/cwd" ]]; then
      cwd="$(readlink "/proc/${pid}/cwd" 2>/dev/null || true)"
    fi
    if [[ "$cmdline" != *"vite"* && "$cmdline" != *"npm run dev"* ]]; then
      continue
    fi
    if [[ "$cwd" != "$root_marker"* && "$cmdline" != *"$ROOT_DIR"* ]]; then
      log "Frontend orphan PID ${pid} 端口 ${port} 但不是本仓库路径，跳过"
      continue
    fi
    log "Frontend orphan: 停止残留 Vite/node PID ${pid}（端口 ${port}）"
    kill "$pid" 2>/dev/null || true
    local i
    for i in $(seq 1 20); do
      pid_alive "$pid" || break
      sleep 0.2
    done
    if pid_alive "$pid"; then
      kill -9 "$pid" 2>/dev/null || true
    fi
  done < <(
    ss -ltnp 2>/dev/null | grep -E ":${port}[[:space:]]" | grep -oE 'pid=[0-9]+' | cut -d= -f2 | sort -u || true
  )
}

log "停止本地 start_local 进程（不碰 PostgreSQL / Docker）…"
# Frontend：npm 包装或 vite；再清理可能残留的同仓库 vite 子进程
safe_kill_pidfile "Frontend" "$FRONTEND_PID_FILE" "vite" "npm run dev" "node"
stop_orphan_vite_on_port 5173
safe_kill_pidfile "Backend" "$BACKEND_PID_FILE" "uvicorn" "app.main:app"

rm -f "$BACKEND_PID_FILE" "$FRONTEND_PID_FILE" 2>/dev/null || true
log "完成。宿主 PostgreSQL 与 Docker 容器均未改动。"
log "可重复执行本脚本（幂等）。"
