#!/usr/bin/env bash
# 本地完整开发一键启动（WSL 宿主 PostgreSQL + Backend :8000 + Vite :5173）
#
# 日常只需：
#   ./scripts/start_local.sh
#
# 冻结边界：
#   - 本地完整开发：宿主 PostgreSQL（库 erip_local），不得依赖 Docker
#   - Docker Compose：才使用 Docker（compose_up.sh）
#   - 正式生产：独立部署流程
#
# 禁止：docker start / docker compose / 静默切 InMemory / 打印密码/Token/Key
# 禁止：把 erip_integration_test 当页面库
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

BACKEND_HOST="127.0.0.1"
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_HOST="127.0.0.1"
FRONTEND_PORT="5173"
EXPECTED_ALEMBIC_HEAD="20260717_08_ai_runtime"
FORBIDDEN_PAGE_DB="erip_integration_test"

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
  python3 - "$port" <<'PY'
import socket, sys
port = int(sys.argv[1])
s = socket.socket()
try:
    s.bind(("127.0.0.1", port))
except OSError:
    sys.exit(0)
finally:
    s.close()
sys.exit(1)
PY
}

pid_alive() {
  local pid="$1"
  [[ -n "${pid:-}" ]] && kill -0 "$pid" 2>/dev/null
}

safe_db_summary() {
  python3 - <<'PY'
import os
from urllib.parse import urlparse, parse_qs
url = os.environ.get("DATABASE_URL", "")
raw = url.replace("postgresql+psycopg://", "postgresql://", 1)
u = urlparse(raw)
qs = parse_qs(u.query)
host = u.hostname or (qs.get("host") or [""])[0] or "?"
port = u.port or (qs.get("port") or ["5432"])[0]
db = (u.path or "/").lstrip("/") or "?"
user = u.username or "?"
print(f"host={host} port={port} db={db} user={user}")
PY
}

db_name_from_url() {
  python3 - <<'PY'
import os
from urllib.parse import urlparse
url = os.environ.get("DATABASE_URL", "").replace("postgresql+psycopg://", "postgresql://", 1)
print((urlparse(url).path or "/").lstrip("/") or "")
PY
}

# 尝试在无交互 sudo 密码的前提下启动宿主 PostgreSQL cluster。
# 需要密码时不绕过；不回退 Docker / InMemory。
try_start_host_postgres() {
  if command -v pg_isready >/dev/null 2>&1; then
    if pg_isready -h /var/run/postgresql -q 2>/dev/null \
      || pg_isready -h 127.0.0.1 -p 5432 -q 2>/dev/null; then
      return 0
    fi
  fi

  # socket 已存在且可连
  if [[ -S /var/run/postgresql/.s.PGSQL.5432 ]]; then
    return 0
  fi

  log "宿主 PostgreSQL 未就绪，尝试非交互启动（不使用 Docker）…"

  if command -v pg_lsclusters >/dev/null 2>&1; then
    local status_line
    status_line="$(pg_lsclusters 2>/dev/null | awk 'NR>1 && $1=="16" && $2=="main" {print $4}' || true)"
    if [[ "${status_line}" == "online" ]]; then
      return 0
    fi
  fi

  # 端口被占用时，即使 sudo 成功也可能起不来；先报告冲突
  if port_in_use 5432; then
    # 若监听者不是本机 postgres socket 路径，多为 Docker 映射
    err "宿主端口 5432 已被占用，WSL 宿主 PostgreSQL cluster 无法绑定。"
    err "本地完整开发需要宿主 PG 使用 5432（或 Unix socket）。"
    err "请停止占用方后重试。常见原因：Docker Compose postgres 映射了宿主 5432。"
    err "Compose 验收请改用：export POSTGRES_PORT=5433 && ./scripts/compose_up.sh"
    err "本脚本不会 docker stop / compose down，也不会改用 erip-local-pg。"
    return 1
  fi

  local started=0
  if command -v sudo >/dev/null 2>&1; then
    if sudo -n true 2>/dev/null; then
      if sudo -n pg_ctlcluster 16 main start 2>/dev/null \
        || sudo -n service postgresql start 2>/dev/null \
        || sudo -n systemctl start postgresql 2>/dev/null; then
        started=1
      fi
    else
      err "启动宿主 PostgreSQL 需要 sudo 密码；当前会话无法非交互完成。"
      err "请在本机终端手动执行其一（需输入密码）："
      err "  sudo pg_ctlcluster 16 main start"
      err "  或: sudo service postgresql start"
      err "首次建库（仅一次）：./scripts/setup_host_postgres_local.sh"
      err "本脚本不会绕过 sudo，也不会静默切换 Docker 或 InMemory。"
      return 1
    fi
  else
    err "未找到 sudo，无法启动系统 PostgreSQL 服务。"
    return 1
  fi

  sleep 1
  if pg_isready -h /var/run/postgresql -q 2>/dev/null \
    || pg_isready -h 127.0.0.1 -p 5432 -q 2>/dev/null \
    || [[ -S /var/run/postgresql/.s.PGSQL.5432 ]]; then
    log "宿主 PostgreSQL 已启动"
    return 0
  fi

  if [[ "$started" -eq 1 ]]; then
    err "已尝试启动宿主 PostgreSQL，但仍不可连接（检查日志 /var/log/postgresql/）。"
  fi
  return 1
}

# ---------- 0) 前置 ----------
cd "$ROOT_DIR"
mkdir -p "$RUN_DIR"

if [[ ! -f "$ENV_FILE" ]]; then
  err "未找到项目根 .env（本地配置只做一次）。"
  err "请执行：cp .env.example .env"
  err "然后按 docs/database/DATABASE.md 配置 WSL 宿主库 erip_local。"
  err "该文件已被 .gitignore 忽略，勿提交。"
  exit 2
fi

env_file_has_database_url=0
env_file_has_postgres_parts=0
if grep -qE '^[[:space:]]*DATABASE_URL=.+' "$ENV_FILE"; then
  env_file_has_database_url=1
fi
if grep -qE '^[[:space:]]*POSTGRES_USER=.+' "$ENV_FILE" \
  && grep -qE '^[[:space:]]*POSTGRES_DB=.+' "$ENV_FILE"; then
  env_file_has_postgres_parts=1
fi

if [[ "$env_file_has_database_url" -eq 0 && "$env_file_has_postgres_parts" -eq 0 ]]; then
  err "项目根 .env 中尚未配置数据库连接。"
  err "推荐（Unix socket / peer，无需密码）："
  err "  DATABASE_URL=postgresql+psycopg:///erip_local?host=/var/run/postgresql"
  err "勿使用 erip_integration_test 作为页面库；勿依赖 erip-local-pg Docker 容器。"
  exit 2
fi

# 清除会话残留，避免误用 Docker/其他 shell 留下的 DATABASE_URL
unset DATABASE_URL || true

log "加载配置：.env（不打印内容）"
load_env_file "$ENV_FILE"

# 强制本地安全默认（覆盖 .env 中的危险组合）
export REPOSITORY_BACKEND=postgres
export LLM_PROVIDER_MODE=stub
export LLM_PROVIDER=stub
export RUN_REAL_LLM_SMOKE=false
export RUN_OPENROUTER_SMOKE=0
export RUN_NVIDIA_SMOKE=0
export RUN_GEMINI_SMOKE=0
export RUN_LOCAL_QWEN_SMOKE=0

# 组装 DATABASE_URL：优先 .env；否则由 POSTGRES_* 生成（支持 socket host）
if [[ -z "${DATABASE_URL:-}" ]]; then
  if [[ -n "${POSTGRES_USER:-}" && -n "${POSTGRES_DB:-}" ]]; then
    DATABASE_URL="$(
      POSTGRES_HOST="${POSTGRES_HOST:-/var/run/postgresql}" \
      POSTGRES_PORT="${POSTGRES_PORT:-5432}" \
      POSTGRES_DB="$POSTGRES_DB" \
      POSTGRES_USER="$POSTGRES_USER" \
      POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-}" \
      python3 - <<'PY'
import os
from urllib.parse import quote_plus
host = os.environ.get("POSTGRES_HOST", "/var/run/postgresql")
port = os.environ.get("POSTGRES_PORT", "5432")
db = os.environ["POSTGRES_DB"]
user = quote_plus(os.environ["POSTGRES_USER"])
password = os.environ.get("POSTGRES_PASSWORD", "")
# Unix socket 目录：postgresql+psycopg://user@/db?host=/var/run/postgresql
if host.startswith("/"):
    if password:
        print(f"postgresql+psycopg://{user}:{quote_plus(password)}@/{db}?host={host}")
    else:
        print(f"postgresql+psycopg://{user}@/{db}?host={host}")
else:
    if password:
        print(f"postgresql+psycopg://{user}:{quote_plus(password)}@{host}:{port}/{db}")
    else:
        print(f"postgresql+psycopg://{user}@{host}:{port}/{db}")
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

SAFE_DB_SUMMARY="$(safe_db_summary)"
PAGE_DB="$(db_name_from_url)"
log "数据库目标：${SAFE_DB_SUMMARY} repository_backend=postgres llm=stub"

if [[ "$PAGE_DB" == "$FORBIDDEN_PAGE_DB" ]]; then
  err "拒绝：.env 指向 ${FORBIDDEN_PAGE_DB}。该库仅用于自动化测试，严禁作为页面开发库。"
  err "请改为 erip_local（WSL 宿主 PostgreSQL）。"
  exit 2
fi

# 拒绝明显指向误建 Docker 本地容器端口的配置（5433 + erip-local-pg 时代）
if echo "$SAFE_DB_SUMMARY" | grep -q 'port=5433'; then
  err "拒绝：DATABASE_URL 指向端口 5433（多为误建 erip-local-pg Docker 映射）。"
  err "本地完整开发应使用 WSL 宿主 PostgreSQL（默认 5432 / Unix socket）上的 erip_local。"
  err "请修正 .env 后重试。容器 erip-local-pg 保留不删，但不再作为本地权威方案。"
  exit 2
fi

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
  err "端口 ${BACKEND_PORT} 已被占用（可能是其他 Backend）。"
  err "不要同时启动两个 Backend。Compose 演示请用 :8080；本地开发用本脚本 :8000。"
  exit 4
fi
if port_in_use "$FRONTEND_PORT"; then
  err "端口 ${FRONTEND_PORT} 已被占用。请释放后再启动，或停止其他 Vite 进程。"
  exit 4
fi

# ---------- 3) 宿主 PostgreSQL（无 Docker）----------
log "检查 WSL 宿主 PostgreSQL…"
if ! try_start_host_postgres; then
  err "无法使用 WSL 宿主 PostgreSQL（${SAFE_DB_SUMMARY}）。"
  err "不会回退 Docker（erip-local-pg / Compose）或 InMemory。"
  exit 5
fi

log "验证数据库可连接…"
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
            cur.execute("SELECT extname FROM pg_extension WHERE extname = 'vector'")
            row = cur.fetchone()
            if not row:
                print("pgvector_missing", file=sys.stderr)
                sys.exit(2)
except Exception as exc:
    print(type(exc).__name__, file=sys.stderr)
    sys.exit(1)
sys.exit(0)
PY
then
  rc=$?
  err "无法连接或使用宿主库（${SAFE_DB_SUMMARY}）。"
  if [[ "${rc:-1}" -eq 2 ]]; then
    err "数据库可连但未启用 pgvector。请在该库执行：CREATE EXTENSION IF NOT EXISTS vector;"
  else
    err "请确认：1) 宿主 PostgreSQL 已运行 2) 库 erip_local 已创建 3) 当前用户有 peer/权限。"
    err "首次建库：./scripts/setup_host_postgres_local.sh（可能需要 sudo 密码）"
  fi
  err "勿连接 erip_integration_test 当页面库；勿依赖 Docker 容器。"
  exit 5
fi
log "PostgreSQL OK（宿主 erip_local + pgvector）"

# ---------- 4) Alembic ----------
log "Alembic upgrade head…"
(
  cd "$BACKEND_DIR"
  export DATABASE_URL
  export REPOSITORY_BACKEND=postgres
  "$VENV_DIR/bin/python" -m alembic upgrade head
)
current_out="$(
  cd "$BACKEND_DIR"
  export DATABASE_URL
  export REPOSITORY_BACKEND=postgres
  "$VENV_DIR/bin/python" -m alembic current 2>/dev/null || true
)"
if ! echo "$current_out" | grep -q "$EXPECTED_ALEMBIC_HEAD"; then
  err "Alembic current 未处于期望 head：${EXPECTED_ALEMBIC_HEAD}"
  err "实际输出："
  echo "$current_out" >&2
  exit 6
fi
log "Alembic OK head=${EXPECTED_ALEMBIC_HEAD}"

# ---------- 5) 启动 Backend ----------
log "启动 Backend ${BACKEND_HOST}:${BACKEND_PORT}…"
(
  cd "$BACKEND_DIR"
  export DATABASE_URL
  export REPOSITORY_BACKEND=postgres
  export LLM_PROVIDER_MODE=stub
  export LLM_PROVIDER=stub
  export RUN_REAL_LLM_SMOKE=false
  export RUN_OPENROUTER_SMOKE=0
  export RUN_NVIDIA_SMOKE=0
  export RUN_GEMINI_SMOKE=0
  export RUN_LOCAL_QWEN_SMOKE=0
  # setsid：独立进程组，stop_local 可干净结束子进程
  setsid nohup "$VENV_DIR/bin/python" -m uvicorn app.main:app \
    --host "$BACKEND_HOST" --port "$BACKEND_PORT" \
    >"$BACKEND_LOG" 2>&1 < /dev/null &
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
    err "Health 返回但 repository_backend 不是 postgres"
    break
  fi
  sleep 0.5
done

if [[ "$ok" -ne 1 ]]; then
  err "Backend 未在超时内变为 healthy postgres。"
  err "请查看日志：${BACKEND_LOG}"
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
  setsid nohup npm run dev -- --host "$FRONTEND_HOST" --port "$FRONTEND_PORT" \
    >"$FRONTEND_LOG" 2>&1 < /dev/null &
  echo $! >"$FRONTEND_PID_FILE"
)
FRONTEND_PID="$(cat "$FRONTEND_PID_FILE")"
log "Frontend PID=${FRONTEND_PID} log=${FRONTEND_LOG}"

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

[start_local] 本地完整开发已启动（方式一 · 无 Docker）

  Frontend:  http://${FRONTEND_HOST}:${FRONTEND_PORT}
  Login:     http://${FRONTEND_HOST}:${FRONTEND_PORT}/login
  Backend:   http://${BACKEND_HOST}:${BACKEND_PORT}
  Health:    ${HEALTH_URL}
  Swagger:   http://${BACKEND_HOST}:${BACKEND_PORT}/docs

  repository_backend=postgres  LLM=stub  零真实 smoke
  DB: ${SAFE_DB_SUMMARY}
  Alembic head: ${EXPECTED_ALEMBIC_HEAD}

  停止：./scripts/stop_local.sh  （只停 Backend/Frontend；不停宿主 PostgreSQL；不碰 Docker）
  日志：${BACKEND_LOG}  ${FRONTEND_LOG}

EOF
