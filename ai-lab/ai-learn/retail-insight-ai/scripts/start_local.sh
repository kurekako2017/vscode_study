#!/usr/bin/env bash
# 本地完整开发一键启动（宿主 PostgreSQL + Backend :8000 + Vite :5173）
#
# 日常只需：
#   ./scripts/start_local.sh
#
# 配置来源：项目根 .env（Git 忽略；Settings 也读 ../.env / .env）
# 禁止：在日常命令中 export DATABASE_URL；禁止打印密码/Token/Key。
#
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"
VENV_DIR="$BACKEND_DIR/.venv"
RUN_DIR="$ROOT_DIR/.run"
BACKEND_PID_FILE="$RUN_DIR/local_backend.pid"
FRONTEND_PID_FILE="$RUN_DIR/local_frontend.pid"
BACKEND_LOG="$RUN_DIR/local_backend.log"
FRONTEND_LOG="$RUN_DIR/local_frontend.log"
ENV_FILE="$ROOT_DIR/.env"
ENV_EXAMPLE="$ROOT_DIR/.env.example"

BACKEND_HOST="127.0.0.1"
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_HOST="127.0.0.1"
FRONTEND_PORT="5173"

log() { echo "[start_local] $*"; }
err() { echo "[start_local] ERROR: $*" >&2; }

# 仅加载 KEY=VALUE，不 source 可执行内容；不 echo 值。
load_env_file() {
  local file="$1"
  local line key val
  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%$'\r'}"
    [[ -z "${line//[[:space:]]/}" ]] && continue
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    if [[ "$line" =~ ^([A-Za-z_][A-Za-z0-9_]*)=(.*)$ ]]; then
      key="${BASH_REMATCH[1]}"
      val="${BASH_REMATCH[2]}"
      # 去掉成对引号
      if [[ "$val" =~ ^\"(.*)\"$ ]]; then val="${BASH_REMATCH[1]}"; fi
      if [[ "$val" =~ ^\'(.*)\'$ ]]; then val="${BASH_REMATCH[1]}"; fi
      export "${key}=${val}"
    fi
  done < "$file"
}

port_in_use() {
  local port="$1"
  if command -v ss >/dev/null 2>&1; then
    ss -ltn 2>/dev/null | grep -qE ":${port}[[:space:]]"
    return $?
  fi
  if command -v lsof >/dev/null 2>&1; then
    lsof -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1
    return $?
  fi
  # 回退：尝试绑定探测
  python3 - "$port" <<'PY'
import socket, sys
port = int(sys.argv[1])
s = socket.socket()
try:
    s.bind(("127.0.0.1", port))
except OSError:
    sys.exit(0)  # in use
finally:
    s.close()
sys.exit(1)
PY
}

pid_alive() {
  local pid="$1"
  [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}

# ---------- 0) 前置 ----------
cd "$ROOT_DIR"
mkdir -p "$RUN_DIR"

if [[ ! -f "$ENV_FILE" ]]; then
  err "未找到项目根 .env（本地配置只做一次）。"
  err "请执行："
  err "  cp .env.example .env"
  err "然后编辑 .env，设置 DATABASE_URL 或 POSTGRES_HOST/PORT/DB/USER/PASSWORD。"
  err "该文件已被 .gitignore 忽略，勿提交。"
  exit 2
fi

# 配置必须来自项目根 .env（首次填写一次），不依赖会话里偶然残留的 export。
env_file_has_database_url=0
env_file_has_postgres_parts=0
if grep -qE '^[[:space:]]*DATABASE_URL=.+' "$ENV_FILE"; then
  env_file_has_database_url=1
fi
if grep -qE '^[[:space:]]*POSTGRES_USER=.+' "$ENV_FILE" \
  && grep -qE '^[[:space:]]*POSTGRES_PASSWORD=.+' "$ENV_FILE" \
  && grep -qE '^[[:space:]]*POSTGRES_DB=.+' "$ENV_FILE"; then
  env_file_has_postgres_parts=1
fi

if [[ "$env_file_has_database_url" -eq 0 && "$env_file_has_postgres_parts" -eq 0 ]]; then
  err "项目根 .env 中尚未配置数据库连接（首次只需设置一次）。"
  err "请编辑 .env，二选一："
  err "  1) DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DB"
  err "  2) POSTGRES_HOST / POSTGRES_PORT / POSTGRES_DB / POSTGRES_USER / POSTGRES_PASSWORD"
  err "示例模板：.env.example。日常启动不要再 export。"
  exit 2
fi

# 清除会话残留，避免误用 Docker/其他 shell 留下的 DATABASE_URL
unset DATABASE_URL || true

log "加载配置：.env（不打印内容）"
load_env_file "$ENV_FILE"

# 强制本地安全默认（覆盖 .env 中的危险组合；用户日常无需 export）
export REPOSITORY_BACKEND=postgres
export LLM_PROVIDER_MODE=stub
export LLM_PROVIDER=stub
export RUN_REAL_LLM_SMOKE=0
export RUN_OPENROUTER_SMOKE=0
export RUN_NVIDIA_SMOKE=0
export RUN_GEMINI_SMOKE=0
export RUN_LOCAL_QWEN_SMOKE=0

# 组装 DATABASE_URL：优先 .env 中的 DATABASE_URL；否则由 POSTGRES_* 生成
if [[ -z "${DATABASE_URL:-}" ]]; then
  if [[ -n "${POSTGRES_USER:-}" && -n "${POSTGRES_PASSWORD:-}" && -n "${POSTGRES_DB:-}" ]]; then
    DATABASE_URL="$(
      POSTGRES_HOST="${POSTGRES_HOST:-127.0.0.1}" \
      POSTGRES_PORT="${POSTGRES_PORT:-5432}" \
      POSTGRES_DB="$POSTGRES_DB" \
      POSTGRES_USER="$POSTGRES_USER" \
      POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
      python3 - <<'PY'
import os
from urllib.parse import quote_plus
host = os.environ.get("POSTGRES_HOST", "127.0.0.1")
port = os.environ.get("POSTGRES_PORT", "5432")
db = os.environ["POSTGRES_DB"]
user = quote_plus(os.environ["POSTGRES_USER"])
password = quote_plus(os.environ["POSTGRES_PASSWORD"])
print(f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}")
PY
    )"
    export DATABASE_URL
    log "已从 .env 的 POSTGRES_* 组装 DATABASE_URL（不打印）"
  else
    err "加载 .env 后仍无法得到 DATABASE_URL。"
    exit 2
  fi
else
  export DATABASE_URL
  log "已使用 .env 中的 DATABASE_URL（不打印）"
fi

# 安全摘要（不含密码）
SAFE_DB_SUMMARY="$(
  python3 - <<'PY'
import os
from urllib.parse import urlparse
url = os.environ.get("DATABASE_URL", "")
u = urlparse(url.replace("postgresql+psycopg://", "postgresql://", 1))
print(f"host={u.hostname or '?'} port={u.port or 5432} db={(u.path or '/').lstrip('/') or '?'} user={u.username or '?'}")
PY
)"
log "数据库目标：${SAFE_DB_SUMMARY} repository_backend=postgres llm=stub"

# ---------- 1) 工具 ----------
if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  log "创建 backend/.venv"
  python3 -m venv "$VENV_DIR"
fi
log "确认 Backend 依赖"
"$VENV_DIR/bin/python" -m pip install -q -r "$BACKEND_DIR/requirements.txt"

if ! command -v node >/dev/null 2>&1 || ! command -v npm >/dev/null 2>&1; then
  err "需要 node 与 npm（Frontend）。请先 ./scripts/check_env.sh"
  exit 1
fi

# ---------- 2) 端口 / 已有进程 ----------
if pid_alive "$(cat "$BACKEND_PID_FILE" 2>/dev/null || true)"; then
  err "Backend 已由 start_local 启动（PID 文件存在）。先 ./scripts/stop_local.sh"
  exit 3
fi
if pid_alive "$(cat "$FRONTEND_PID_FILE" 2>/dev/null || true)"; then
  err "Frontend 已由 start_local 启动。先 ./scripts/stop_local.sh"
  exit 3
fi

if port_in_use "$BACKEND_PORT"; then
  err "端口 ${BACKEND_PORT} 已被占用（可能是 Docker Backend 或其他进程）。"
  err "不要同时启动两个 Backend。若要用 Docker 数据，请只使用 Compose :8080，或 stop 占用方后再启动本地。"
  exit 4
fi
if port_in_use "$FRONTEND_PORT"; then
  err "端口 ${FRONTEND_PORT} 已被占用。请释放后再启动，或停止其他 Vite 进程。"
  exit 4
fi

# ---------- 3) PostgreSQL 可连接 ----------
log "检查 PostgreSQL 可连接…"
# 若本机约定的 erip-local-pg 容器存在但未启动，尝试拉起（不打印 Secret）
if command -v docker >/dev/null 2>&1; then
  if docker ps -a --format '{{.Names}}' 2>/dev/null | grep -qx 'erip-local-pg'; then
    if ! docker ps --format '{{.Names}}' 2>/dev/null | grep -qx 'erip-local-pg'; then
      log "检测到 erip-local-pg 容器未运行，正在 docker start…"
      docker start erip-local-pg >/dev/null 2>&1 || true
      sleep 2
    fi
  fi
fi
if ! "$VENV_DIR/bin/python" - <<'PY'
import os, sys
try:
    import psycopg
except ImportError:
    print("psycopg not installed in venv", file=sys.stderr)
    sys.exit(1)
url = os.environ["DATABASE_URL"].replace("postgresql+psycopg://", "postgresql://", 1)
try:
    with psycopg.connect(url, connect_timeout=5) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            cur.fetchone()
except Exception as exc:
    print(type(exc).__name__, file=sys.stderr)
    sys.exit(1)
sys.exit(0)
PY
then
  err "无法连接 PostgreSQL（${SAFE_DB_SUMMARY}）。"
  err "请确认：1) 本地开发库服务已运行（本机 erip-local-pg 或等价实例） 2) .env 中库名/用户正确 3) 用户有权限。"
  err "密码错误时只报连接失败，不会打印密码。勿连接 erip_integration_test 当页面库。"
  exit 5
fi
log "PostgreSQL OK"

# ---------- 4) Alembic ----------
log "Alembic upgrade head…"
(
  cd "$BACKEND_DIR"
  export DATABASE_URL
  export REPOSITORY_BACKEND=postgres
  "$VENV_DIR/bin/python" -m alembic upgrade head
  "$VENV_DIR/bin/python" -m alembic current 2>/dev/null | tail -n 3 || true
)
log "Alembic OK"

# ---------- 5) 启动 Backend ----------
log "启动 Backend ${BACKEND_HOST}:${BACKEND_PORT}…"
(
  cd "$BACKEND_DIR"
  export DATABASE_URL
  export REPOSITORY_BACKEND=postgres
  export LLM_PROVIDER_MODE=stub
  export LLM_PROVIDER=stub
  export RUN_REAL_LLM_SMOKE=0
  export RUN_OPENROUTER_SMOKE=0
  export RUN_NVIDIA_SMOKE=0
  export RUN_GEMINI_SMOKE=0
  export RUN_LOCAL_QWEN_SMOKE=0
  nohup "$VENV_DIR/bin/python" -m uvicorn app.main:app \
    --host "$BACKEND_HOST" --port "$BACKEND_PORT" \
    >"$BACKEND_LOG" 2>&1 &
  echo $! >"$BACKEND_PID_FILE"
)
BACKEND_PID="$(cat "$BACKEND_PID_FILE")"
log "Backend PID=${BACKEND_PID} log=${BACKEND_LOG}"

# ---------- 6) 等待 health ----------
HEALTH_URL="http://${BACKEND_HOST}:${BACKEND_PORT}/health"
ok=0
for i in $(seq 1 40); do
  if body="$(curl -fsS "$HEALTH_URL" 2>/dev/null)"; then
    if echo "$body" | grep -q '"repository_backend"[[:space:]]*:[[:space:]]*"postgres"'; then
      ok=1
      break
    fi
    err "Health 返回但 repository_backend 不是 postgres：请检查 .env / 启动环境"
    err "（不打印完整 body 中的敏感字段；仅检查字段名）"
    # still fail closed
    break
  fi
  sleep 0.5
done

if [[ "$ok" -ne 1 ]]; then
  err "Backend 未在超时内变为 healthy postgres。"
  err "请查看日志：${BACKEND_LOG}"
  # 失败时尽量停掉刚起的 backend
  if pid_alive "$BACKEND_PID"; then kill "$BACKEND_PID" 2>/dev/null || true; fi
  rm -f "$BACKEND_PID_FILE"
  exit 6
fi
log "Health OK repository_backend=postgres"

# ---------- 7) Frontend ----------
if [[ ! -d "$FRONTEND_DIR/node_modules" ]]; then
  log "npm install（首次）…"
  (cd "$FRONTEND_DIR" && npm install)
fi

log "启动 Frontend ${FRONTEND_HOST}:${FRONTEND_PORT}…"
(
  cd "$FRONTEND_DIR"
  nohup npm run dev -- --host "$FRONTEND_HOST" --port "$FRONTEND_PORT" \
    >"$FRONTEND_LOG" 2>&1 &
  echo $! >"$FRONTEND_PID_FILE"
)
FRONTEND_PID="$(cat "$FRONTEND_PID_FILE")"
log "Frontend PID=${FRONTEND_PID} log=${FRONTEND_LOG}"

# 等待 Vite 端口
fe_ok=0
for i in $(seq 1 40); do
  if curl -fsS -o /dev/null "http://${FRONTEND_HOST}:${FRONTEND_PORT}/" 2>/dev/null \
    || curl -fsS -o /dev/null "http://${FRONTEND_HOST}:${FRONTEND_PORT}/login" 2>/dev/null; then
    fe_ok=1
    break
  fi
  sleep 0.5
done
if [[ "$fe_ok" -ne 1 ]]; then
  err "Frontend 未在超时内响应。日志：${FRONTEND_LOG}"
  err "Backend 仍在运行（PID ${BACKEND_PID}）。可 ./scripts/stop_local.sh 后重试。"
  exit 7
fi

# ---------- 8) 成功摘要 ----------
cat <<EOF

[start_local] 本地完整开发已启动（方式一）

  Frontend:  http://${FRONTEND_HOST}:${FRONTEND_PORT}
  Login:     http://${FRONTEND_HOST}:${FRONTEND_PORT}/login
  Backend:   http://${BACKEND_HOST}:${BACKEND_PORT}
  Health:    ${HEALTH_URL}
  Swagger:   http://${BACKEND_HOST}:${BACKEND_PORT}/docs

  repository_backend=postgres  LLM=stub  零真实 smoke
  DB: ${SAFE_DB_SUMMARY}

  停止：./scripts/stop_local.sh
  日志：${BACKEND_LOG}  ${FRONTEND_LOG}

EOF
