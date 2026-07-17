#!/usr/bin/env bash
# 一次性：在 WSL 宿主 PostgreSQL 上创建本地页面开发库 erip_local。
#
# 用途：管理员首次配置（非日常）。日常启动请用 ./scripts/start_local.sh
#
# 做什么：
#   - 确保宿主 PostgreSQL 16 main cluster 运行（可能需要 sudo 密码）
#   - 创建 OS peer 角色（当前用户）与库 erip_local（UTF8）
#   - 启用 pgvector
#   - 授予当前用户对该库的最小必要权限
#   - 不触碰 erip_integration_test 数据；不删除任何 Docker 容器/Volume
#
# 不做什么：
#   - 不修改 pg_hba.conf
#   - 不打印密码
#   - 不依赖 Docker / erip-local-pg
#   - 不把 erip_integration_test 当页面库
#
set -euo pipefail

OS_USER="${SUDO_USER:-${USER:-$(whoami)}}"
DB_NAME="erip_local"
CLUSTER_VER="16"
CLUSTER_NAME="main"

log() { echo "[setup_host_pg] $*"; }
err() { echo "[setup_host_pg] ERROR: $*" >&2; }

if [[ -z "$OS_USER" || "$OS_USER" == "root" ]]; then
  err "无法确定非 root OS 用户。"
  exit 1
fi

if ! command -v psql >/dev/null 2>&1; then
  err "未找到 psql。请安装 postgresql-client / postgresql-16。"
  exit 1
fi

if ! command -v sudo >/dev/null 2>&1; then
  err "需要 sudo 以使用 postgres 系统用户管理库。"
  exit 1
fi

log "目标：宿主库 ${DB_NAME}，peer 用户 ${OS_USER}（Unix socket）"
log "不会删除 Docker 容器/Volume，不会清空其他库。"

# 1) 端口冲突提示
if command -v ss >/dev/null 2>&1; then
  if ss -ltn 2>/dev/null | grep -qE ':5432[[:space:]]'; then
    if [[ ! -S /var/run/postgresql/.s.PGSQL.5432 ]]; then
      err "宿主 5432 已被占用，且 Unix socket 不存在——通常是 Docker 映射了 5432。"
      err "请先释放 5432（例如停止 Compose postgres 的宿主端口映射），再重试本脚本。"
      err "Compose 可改用：export POSTGRES_PORT=5433"
      err "不要 docker compose down -v；不要删除 Volume。"
      exit 2
    fi
  fi
fi

# 2) 启动 cluster
if ! pg_isready -h /var/run/postgresql -q 2>/dev/null \
  && [[ ! -S /var/run/postgresql/.s.PGSQL.5432 ]]; then
  log "启动宿主 PostgreSQL cluster ${CLUSTER_VER}/${CLUSTER_NAME}（可能需要 sudo 密码）…"
  if ! sudo pg_ctlcluster "$CLUSTER_VER" "$CLUSTER_NAME" start \
    && ! sudo service postgresql start; then
    err "无法启动宿主 PostgreSQL。若提示 Address already in use，请先释放 5432。"
    exit 3
  fi
  sleep 1
fi

if ! pg_isready -h /var/run/postgresql -q 2>/dev/null \
  && [[ ! -S /var/run/postgresql/.s.PGSQL.5432 ]]; then
  err "宿主 PostgreSQL 仍不可用。"
  exit 3
fi
log "宿主 PostgreSQL 可连接"

# 3) 创建角色 / 库 / extension（via postgres superuser + peer）
log "创建角色与数据库（若不存在）…"
sudo -u postgres psql -v ON_ERROR_STOP=1 -d postgres <<SQL
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '${OS_USER}') THEN
    CREATE ROLE ${OS_USER} LOGIN;
    RAISE NOTICE 'created role ${OS_USER}';
  ELSE
    RAISE NOTICE 'role ${OS_USER} already exists';
  END IF;
END
\$\$;

SELECT 'db_exists=' || EXISTS (SELECT 1 FROM pg_database WHERE datname = '${DB_NAME}');
SQL

DB_EXISTS="$(sudo -u postgres psql -d postgres -Atc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" || true)"
if [[ "$DB_EXISTS" != "1" ]]; then
  log "创建数据库 ${DB_NAME}（UTF8）…"
  sudo -u postgres psql -v ON_ERROR_STOP=1 -d postgres <<SQL
CREATE DATABASE ${DB_NAME}
  OWNER ${OS_USER}
  ENCODING 'UTF8'
  LC_COLLATE 'C.UTF-8'
  LC_CTYPE 'C.UTF-8'
  TEMPLATE template0;
SQL
else
  log "数据库 ${DB_NAME} 已存在，复用。"
  sudo -u postgres psql -v ON_ERROR_STOP=1 -d postgres \
    -c "ALTER DATABASE ${DB_NAME} OWNER TO ${OS_USER};" >/dev/null || true
fi

log "启用 pgvector 并授权…"
sudo -u postgres psql -v ON_ERROR_STOP=1 -d "$DB_NAME" <<SQL
CREATE EXTENSION IF NOT EXISTS vector;
GRANT CONNECT ON DATABASE ${DB_NAME} TO ${OS_USER};
GRANT USAGE, CREATE ON SCHEMA public TO ${OS_USER};
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${OS_USER};
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ${OS_USER};
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ${OS_USER};
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ${OS_USER};
SQL

# 4) 以 peer 验证
log "以 peer/socket 验证 ${OS_USER} → ${DB_NAME}…"
if ! psql -h /var/run/postgresql -d "$DB_NAME" -v ON_ERROR_STOP=1 -c "SELECT current_user, current_database(); SELECT extname FROM pg_extension WHERE extname='vector';" >/dev/null; then
  err "peer 登录失败。未修改 pg_hba.conf；请检查系统 peer 配置是否仍为 Ubuntu 默认。"
  exit 4
fi

# 5) 列出相关库状态（只读）
log "相关数据库状态："
sudo -u postgres psql -d postgres -c \
  "SELECT datname, pg_encoding_to_char(encoding) AS enc FROM pg_database WHERE datname IN ('erip_local','erip_integration_test','erip','postgres') ORDER BY 1;"

log "完成。建议 .env："
log "  DATABASE_URL=postgresql+psycopg:///erip_local?host=/var/run/postgresql"
log "  REPOSITORY_BACKEND=postgres"
log "  LLM_PROVIDER_MODE=stub"
log "然后执行：./scripts/start_local.sh"
log "注意：erip_integration_test 仅测试用，禁止当页面库。"
