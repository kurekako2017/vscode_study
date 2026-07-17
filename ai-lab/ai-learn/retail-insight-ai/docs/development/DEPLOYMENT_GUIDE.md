# ERIP V1.0 部署指南

最后更新：2026-07-17

本文档是 **Enterprise Retail Intelligence Platform (ERIP) V1.0** 的权威、可执行部署入口。  
服务名、端口、数据库用户、环境变量与命令均来自仓库当前配置（`docker-compose.yml`、Dockerfile、entrypoint、`.env.example`、`scripts/*`），禁止用记忆替代事实。

| 文档 | 职责 |
|---|---|
| **本文件** | 部署分层、Compose 操作、Secret、Backup/Restore 命令模板、生产差距 |
| `docs/learning/01_Foundation/RUNBOOK_LOCAL.md` | 学习向启动/排错、业务 Case、Appendix M/N |
| `VERIFY_CHECKLIST.md` | 启动完成勾选 |
| `.env.example` | 环境变量模板（无真实密钥） |

**V1.0 验收基线（文档编写时仓库事实）**

| 项 | 值 |
|---|---|
| 正式 Repository | **PostgreSQL** |
| InMemory | 仅辅助 unittest / 教学，不作业务验收 |
| Alembic head | **`20260717_08_ai_runtime`** |
| PostgreSQL Backend | **297 tests / 6 skipped** |
| InMemory Backend | **286 tests / 62 skipped** |
| Frontend | **116/116**；production build 通过 |
| Compose | services `postgres` / `backend` / `frontend` healthy |
| Volume | **`erip_postgres_data`** |
| 默认 LLM | `LLM_PROVIDER_MODE=stub`，`effective_mode=stub`，`RUN_REAL_LLM_SMOKE=0` |
| Runtime 持久化 | 表 `ai_runtime_settings` |
| Seed | `scripts/seed_scenario01.sh`（不自动随 Compose） |
| 默认验收 | **零真实 LLM 调用** |

---

## 1. 三种运行模式

| 模式 | Frontend | Backend | Database | 用途 |
|---|---|---|---|---|
| 本地开发 | `http://127.0.0.1:5173`（Vite） | `http://127.0.0.1:8000` | **宿主 PostgreSQL**（必须） | 页面开发 / API 调试 |
| Docker Compose | `http://127.0.0.1:8080`（nginx） | 宿主 `8000` 或经 8080 同源 `/api` | Compose PostgreSQL（volume） | 单机部署 / 企业验收 / 演示 |
| 正式生产 | HTTPS 域名 | 内网 Backend | 独立/托管 PostgreSQL | 企业运行（需额外硬化） |

**必须明确：**

1. **普通页面测试不需要 Docker**（本地 Backend + Vite 即可）。  
2. **本地开发仍必须使用 PostgreSQL** 做业务联调：`REPOSITORY_BACKEND=postgres`，且 `GET /health` 必须显示 `repository_backend=postgres`。  
3. **InMemory 仅**快速 unittest / 教学；**不是**正式业务验收。  
4. **本地宿主 PostgreSQL 与 Docker Volume `erip_postgres_data` 是不同数据源**。  
5. 要查看 **Docker 内已有业务数据**，请使用 **Frontend 8080**（Compose），不要假设 5173 连到同一库。  
6. Compose 下 Backend 环境写死 `REPOSITORY_BACKEND: postgres`。

---

## 2. 部署架构

### 2.1 请求路径（Compose）

```text
Browser
  │
  ▼
Frontend Nginx (service: frontend, 宿主 :8080 → 容器 :80)
  │  /api/*  ──proxy_pass──►  http://backend:8000
  │  /health ──proxy_pass──►  http://backend:8000/health
  │  SPA /*  → index.html
  ▼
FastAPI (service: backend, 宿主 :8000 → 容器 :8000)
  │  JWT / RBAC / Persistent Audit
  │  LLM Gateway + Usage Ledger
  │  ai_runtime_settings（运行 mode / kill_switch）
  ▼
PostgreSQL + pgvector (service: postgres, 宿主 :5432 默认)
  volume: erip_postgres_data
```

Mermaid（可选）：

```mermaid
flowchart LR
  B[Browser] --> N[frontend nginx :8080]
  N -->|/api reverse proxy| F[backend FastAPI :8000]
  F --> P[(postgres + pgvector)]
  F --> L[LLM Gateway stub by default]
```

### 2.2 组件说明（与代码一致）

| 组件 | 说明 |
|---|---|
| Alembic 启动链 | entrypoint：PG ready → `alembic upgrade head` → uvicorn；**migration 失败则不启动应用** |
| Volume | `erip_postgres_data` → `/var/lib/postgresql/data` |
| JWT / RBAC | Access Token + 冻结 Permission；401/403 fail-closed |
| Persistent Audit | PostgreSQL append-only 审计 |
| LLM Gateway | 唯一 Provider 外呼边界；Evidence Gate / 额度 / Ledger |
| Usage Ledger | PostgreSQL `llm_usage_ledger` 等 |
| `ai_runtime_settings` | 运行时 mode / kill_switch / version（**无 Key**） |
| Provider Secret | **仅 Backend 进程环境变量**读取；Frontend / DB 不保存 Key |

Compose project name（`docker-compose.yml`）：**`erip`**  
Services：**`postgres`**、**`backend`**、**`frontend`**

---

## 3. 环境要求

| 项 | 要求 | 说明 |
|---|---|---|
| Docker Engine / Desktop | Compose 场景必需 | `docker info` 必须成功 |
| Docker Compose | `docker compose` 插件 | 脚本使用 `docker compose` |
| WSL Integration | Windows 用户建议 | daemon 需在 WSL 可见 |
| Git | 克隆仓库 | — |
| curl | 健康检查 / verify / seed | 脚本依赖 |
| Node.js + npm | 本地 Frontend | `scripts/check_env.sh` |
| Python 3 + pip | 本地 Backend | 建议 3.12（镜像为 `python:3.12-slim`） |
| 端口 | 默认 5432 / 8000 / 8080 / 5173 | 可被占用则改环境变量 |
| CPU | **建议** ≥ 2 核 | 建议值，非硬门槛 |
| Memory | **建议** ≥ 4 GB 可用 | 建议值 |
| Disk | **建议** ≥ 10 GB 空闲 | 镜像 + volume |

检查工具（本地无 Docker 场景）：

```bash
./scripts/check_env.sh
```

---

## 4. 部署文件职责

| 文件 / 脚本 | 职责 |
|---|---|
| `docker-compose.yml` | 三服务编排、默认 stub、volume、端口、健康检查 |
| `backend/Dockerfile` | Backend 镜像：依赖、app、alembic、db、data、entrypoint；**不 COPY `.env`** |
| `frontend/Dockerfile` | multi-stage：`npm ci` + Vite build → nginx:1.29-alpine |
| `frontend/nginx.conf` | SPA + `/api`、`/health` 反代 `backend:8000` |
| `backend/scripts/docker-entrypoint.sh` | 等 PG → `alembic upgrade head` → `exec` uvicorn |
| `.dockerignore` / `backend/.dockerignore` / `frontend/.dockerignore` | 排除 `.env`、venv、tests 等 |
| `scripts/compose_up.sh` | build + up -d + 健康轮询 |
| `scripts/compose_verify.sh` | health / SPA 路径 / 镜像无 `.env` |
| `scripts/compose_down.sh` | `docker compose down`；**拒绝 `-v`** |
| `scripts/prove_dockerignore.sh` | 证明 dockerignore 排除 `.env`、compose 默认 stub |
| `scripts/run_api_e2e.sh` | Stub API E2E（`E2E_BASE_URL` 默认 `http://127.0.0.1:8000`） |
| `scripts/seed_scenario01.sh` | Scenario01 幂等种子（PG-only） |
| `scripts/start_backend.sh` / `start_frontend.sh` | 本地无 Docker 启动 |
| `.env.example` | 环境变量模板 |
| `backend/alembic/` + `alembic.ini` | Migration；URL 仅来自进程 `DATABASE_URL` |
| Volume `erip_postgres_data` | PostgreSQL 数据持久化 |

---

## 5. 环境变量与 Secret

模板：项目根 `.env.example` → 复制为 `.env`（见第 6 节）。  
Compose：`backend` 的 `environment:` **钉死** `REPOSITORY_BACKEND=postgres`、`LLM_PROVIDER_MODE=stub` 及全部 `RUN_*_SMOKE=0`（见 `docker-compose.yml`）。

### 5.1 Repository / Database

| 变量 | 用途 | 必填 | 默认（.env.example / compose） | Secret | 安全示例 |
|---|---|---|---|---|---|
| `REPOSITORY_BACKEND` | 存储后端 | 业务验收必填 postgres | example: `postgres`；Compose 钉死 `postgres` | 否 | `postgres` |
| `POSTGRES_HOST` | DB 主机 | PG 时需要 | example `127.0.0.1`；Compose 容器内 `postgres` | 否 | Compose 内用服务名 `postgres` |
| `POSTGRES_PORT` | 宿主映射 / 连接端口 | 否 | `5432` | 否 | 冲突时 `export POSTGRES_PORT=5433` |
| `POSTGRES_DB` | 库名 | 是 | `erip` | 否 | `erip` |
| `POSTGRES_USER` | 用户 | 是 | `erip_app` | 否 | `erip_app` |
| `POSTGRES_PASSWORD` | 密码 | 是 | `erip_change_me_local_only`（占位） | **是** | 强随机；勿提交 |
| `DATABASE_URL` | SQLAlchemy/psycopg URL | Compose 由公式生成 | `postgresql+psycopg://erip_app:***@postgres:5432/erip` | **是** | 勿打印完整串 |

### 5.2 JWT / App

| 变量 | 用途 | 必填 | 默认 | Secret | 安全示例 |
|---|---|---|---|---|---|
| `JWT_SECRET_KEY` | 签发 Access Token | 是 | 本地占位长串 | **是** | 生产高熵随机 |
| `APP_ENV` | 环境名 | 否 | `local` | 否 | 生产用 `production` |
| `LOG_LEVEL` | 日志级别 | 否 | `INFO` | 否 | `INFO` |
| `SERVICE_NAME` | 结构化日志 | Compose 钉死 | `retail-insight-ai` | 否 | — |
| `CORS_ORIGINS` | CORS | 否 | 含 8080/5173 | 否 | 生产收紧为真实域名 |
| `LEARNING_TRACE` | 学习日志 | 否 | `false` | 否 | 默认关 |
| `TASK_EXECUTION_MODE` | 任务执行 | Compose `background` | `background` | 否 | — |

### 5.3 Port

| 变量 | 用途 | 默认 |
|---|---|---|
| `BACKEND_PORT` | 宿主映射 Backend | `8000` |
| `FRONTEND_PORT` | 宿主映射 Frontend | `8080` |
| `POSTGRES_PORT` | 宿主映射 PostgreSQL | `5432` |

### 5.4 LLM Mode（权威枚举）

| 值 | 含义 |
|---|---|
| `stub` | 默认；无网络；stub-low-cost / stub-high-quality |
| `openrouter` | 单 Provider（仍经 Gateway/Ledger） |
| `fallback_chain` | OpenRouter → NVIDIA → Gemini → Local Qwen（串行） |

| 变量 | 用途 | 必填 | 默认 | Secret |
|---|---|---|---|---|
| `LLM_PROVIDER_MODE` | **启动默认** mode | 否 | `stub`；Compose **钉死 stub** | 否 |
| `LLM_PROVIDER` | 兼容旧名 | 否 | `stub` | 否 |

**运行时授权**另存 PostgreSQL `ai_runtime_settings`（见第 12 节）。  
- `LLM_PROVIDER_MODE` = 进程启动默认 / 初始化 DB 行的默认值来源之一。  
- `ai_runtime_settings.mode` / `kill_switch` = 多实例共享的运行事实。  
- Key、模型名、价格 **仍只来自环境变量**，不进 `ai_runtime_settings`。

### 5.5 OpenRouter / NVIDIA / Gemini / Local Qwen

（字段以 `.env.example` 为准；价格单位 **USD / 百万 tokens**。）

| 类别 | 关键变量 | 必填时机 | Secret |
|---|---|---|---|
| OpenRouter | `OPENROUTER_API_KEY`, `OPENROUTER_*_MODEL`, `OPENROUTER_*_PRICE`, `OPENROUTER_BASE_URL`, `OPENROUTER_ENABLED` | mode=openrouter 或 chain 启用该 provider | Key **是** |
| NVIDIA | `NVIDIA_API_KEY`, `NVIDIA_*_MODEL`, prices, `NVIDIA_BASE_URL` | chain 启用时 | Key **是** |
| Gemini | `GEMINI_API_KEY`, `GEMINI_*_MODEL`, prices, `GEMINI_BASE_URL` | chain 启用时 | Key **是** |
| Local Qwen | `LOCAL_QWEN_ENABLED`, `LOCAL_QWEN_BASE_URL`, models, optional `LOCAL_QWEN_API_KEY` | chain 启用本地时 | 视配置 |

### 5.6 Timeout / Circuit / Smoke

| 变量 | 默认（.env.example） | Secret |
|---|---|---|
| `LLM_TOTAL_TIMEOUT_SECONDS` | `120` | 否 |
| `LLM_MAX_PROVIDER_ATTEMPTS` | `4` | 否 |
| `LLM_CIRCUIT_FAILURE_THRESHOLD` | `3` | 否 |
| `LLM_CIRCUIT_OPEN_DURATION_SECONDS` | `30` | 否 |
| `RUN_REAL_LLM_SMOKE` | `0` | 否 |
| `RUN_OPENROUTER_SMOKE` 等 | `0` | 否 |

**首次部署不得开启真实调用。** 默认保持 **stub**。

---

## 6. Secret 安全

```bash
cp .env.example .env
# 编辑 .env：更换 POSTGRES_PASSWORD、JWT_SECRET_KEY
# 勿提交 .env（已在 .gitignore）
```

**必须遵守：**

- `.env` **不**提交 Git  
- **不**把 Key 写进 `docker-compose.yml` 明文生产值、Frontend 源码、文档正文、Audit  
- 根/backend/frontend **`.dockerignore` 均排除 `.env`**；`prove_dockerignore.sh` 可验证  
- Dockerfile **不** `COPY .env`  
- 生产使用 Secret Manager / 编排 secrets  
- 更换 JWT Secret 与数据库密码  
- **AI管理** 页仅展示 configured / readiness **布尔值**与模型名等非 Secret 字段  

---

## 7. 首次 Docker 部署

在 **项目根** `retail-insight-ai/` 执行。

```bash
# 0) 进入仓库
cd /path/to/retail-insight-ai

# 1) 环境文件
cp .env.example .env
# 至少修改 POSTGRES_PASSWORD、JWT_SECRET_KEY（演示可暂用默认，生产禁止）

# 2) Docker 可用
docker info
docker compose version

# 3) 证明 .env 不进构建上下文 + compose 默认 stub
./scripts/prove_dockerignore.sh

# 4) 渲染配置（可读检查，勿把含密码的完整输出贴到公开场合）
docker compose config >/dev/null

# 5) 端口冲突时（示例：宿主 5432 被占用）
export POSTGRES_PORT=5433
# 可选：export BACKEND_PORT=8000 FRONTEND_PORT=8080

# 6) 构建并启动
./scripts/compose_up.sh

# 7) 健康与 SPA 检查
./scripts/compose_verify.sh
```

**访问入口**

| 用途 | URL |
|---|---|
| Frontend（正式） | http://127.0.0.1:8080 |
| Login | http://127.0.0.1:8080/login |
| Backend API | http://127.0.0.1:8000 |
| Swagger | http://127.0.0.1:8000/docs |
| Health | http://127.0.0.1:8000/health |

`compose_up.sh` 行为摘要：`docker compose config` → `build` → `up -d` → 轮询至 Backend `/health` 与 Frontend `/` 可用。

---

## 8. Alembic

### 8.1 启动链（`backend/scripts/docker-entrypoint.sh`）

```text
PostgreSQL ready（psycopg SELECT 1，默认最长 ~60s）
    →
alembic upgrade head
    →
alembic current（日志）
    →
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers
```

- **Migration 失败时不会启动 uvicorn**，Backend **不应**伪装 healthy。  
- 当前 head：**`20260717_08_ai_runtime`**  
  （文件：`backend/alembic/versions/20260717_08_ai_runtime_settings.py`，含表 `ai_runtime_settings`）

### 8.2 查看当前 revision

```bash
docker compose exec backend alembic current
docker compose exec backend alembic history
```

---

## 9. 部署后验证

```bash
# 服务状态
docker compose ps
# 期望：postgres / backend / frontend 均为 healthy（或 Up + healthy）

# Backend health（必须 postgres）
curl -fsS http://127.0.0.1:8000/health
# 成功标准：JSON 中 "repository_backend":"postgres"（顶层字段，与当前 Health 响应一致）

# Frontend
curl -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8080/
# 成功标准：200

# History API 路由（与 App.tsx / compose_verify 一致；应返回 SPA 200 而非裸 404）
for path in / /login /dashboard /documents /rag /analysis /approval /ai-admin; do
  code=$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:8080$path")
  echo "$path -> $code"
done

# Alembic
docker compose exec backend alembic current
# 成功标准：20260717_08_ai_runtime

# LLM / Runtime（admin JWT；勿打印 Token）
# 1) POST /api/v1/auth/login 取得 access_token
# 2) GET /api/v1/admin/ai-runtime
# 成功标准：effective_mode=stub，kill_switch 布尔可读，无 api_key / sk- 字段

# Volume
docker volume ls | grep erip_postgres_data
```

一键：

```bash
./scripts/compose_verify.sh
```

（脚本已覆盖 health、`/login` `/dashboard` `/documents` `/rag` `/analysis` `/approval`；`/ai-admin` 建议按上表手测。）

---

## 10. 测试账号

**仅本地 Stub / 演示。禁止生产使用。生产必须替换为企业 IdP，禁止复用测试密码。**

| 角色 | 用户名 | 密码 |
|---|---|---|
| admin | `admin` | `Admin#2026!` |
| manager | `manager` | `Manager#2026!` |
| employee | `employee` | `Employee#2026!` |

来源：RUNBOOK + deterministic test users（bcrypt，应用不存明文密码文件）。

- admin：含 **AI管理**（`security.manage`）、Audit 等  
- manager：审批 review / approve / reject  
- employee：文档 / RAG / 提交审批；**approve → 403**

---

## 11. Scenario01 Seed

```bash
./scripts/seed_scenario01.sh
# BASE_URL=http://127.0.0.1:8000 ./scripts/seed_scenario01.sh
```

| 规则 | 说明 |
|---|---|
| 只允许 PostgreSQL | `/health` 的 `repository_backend` 必须为 `postgres`，否则 exit |
| 幂等 | 按 title / Idempotency-Key / checksum 复用；不删除现有数据 |
| 调用范围 | login → documents upload → import → chunk |
| 禁止 | Retrieval、AI 分析、报告、审批、真实 LLM |
| Provider | `provider_calls=0` / `provider_call_target=0` |
| 输出 | `document_id`、status、chunk_count、recommended_question |
| 不输出 | Token、密码、文档正文、API Key |
| 自动启动 | **不**随 Compose 启动 |

样例路径：`docs/learning/sample-data/Scenario01_Sales_Decline/`（`01`–`06` 业务 md）。

**部署后推荐操作链（人工）：**

```text
文書管理
  → 「使用此文档检索」
  → RAG/AI分析
  →（证据后）AI分析
  → 生成取締役会報告
  → 提交审批
  → manager 在承認管理 approve/reject
```

---

## 12. AI Runtime 管理

| 项 | 事实 |
|---|---|
| 权限 | JWT + `security.manage`（admin） |
| API | `GET/PATCH /api/v1/admin/ai-runtime` |
| 模式 | `stub` / `openrouter` / `fallback_chain` |
| PATCH 要求 | `confirmed=true`、`expected_version`；Stub→Real 需 `confirmation_text`（`ENABLE_REAL_LLM`） |
| readiness | 目标 mode 未 ready → 422 |
| version 冲突 | 409 |
| Kill Switch | 强制 `effective_mode=stub` |
| 持久化 | PostgreSQL `ai_runtime_settings`；**Backend 重启后保持** |
| Key | **不**存 DB、**不**回响应、**不**进 Frontend |
| 费用 | 开启 Real **可能产生外部 API 费用** |
| 普通 RAG | 默认可零 Provider；**不**自动调用 LLM |
| 真实 smoke | 仅 opt-in 环境变量；默认验收关闭 |
| InMemory | 管理 API **503** fail-closed |

前端入口：`http://127.0.0.1:8080/ai-admin`（Compose）。

---

## 13. 日常启动 / 停止 / 重启

```bash
# 启动（build + up + 健康等待）
./scripts/compose_up.sh

# 验证
./scripts/compose_verify.sh

# 停止服务（保留 Volume）
./scripts/compose_down.sh
# 等价：docker compose down
```

### 禁止删除数据卷

```text
╔══════════════════════════════════════════════════════════╗
║  禁止：docker compose down -v                            ║
║  禁止：./scripts/compose_down.sh -v                      ║
║  脚本收到 -v / --volumes 会拒绝并 exit 2                 ║
║  -v 会删除 erip_postgres_data，业务数据不可恢复（无备份时）║
╚══════════════════════════════════════════════════════════╝
```

| 操作 | 数据 |
|---|---|
| `compose_down` / `docker compose down` | 停容器；**Volume 保留** |
| `docker compose restart backend` | 进程重启；DB 与 Runtime 配置保留 |
| `docker compose down -v` | **删除 Volume** → 数据丢失 |

---

## 14. 日志与排错

```bash
# 全部服务
docker compose logs

# 单服务
docker compose logs backend
docker compose logs frontend
docker compose logs postgres

# 最近 N 行 / 跟随
docker compose logs --tail=100 backend
docker compose logs -f backend

# Migration 相关：看 backend 启动日志中的 [backend-entrypoint]
docker compose logs backend 2>&1 | grep -E 'alembic|entrypoint|ERROR' | tail -50
```

**日志中不得回显** API Key、密码、完整 JWT、完整 Prompt。

| 现象 | 可能原因 | 处理方向 |
|---|---|---|
| Docker daemon 不可用 | Desktop/服务未起 | `docker info`；启动 daemon |
| WSL Integration | Windows 未集成 | Docker Desktop → WSL 集成 |
| 端口冲突 | 5432/8000/8080 占用 | `export POSTGRES_PORT=5433` 等；`ss -ltn` |
| Backend unhealthy | Migration 失败 / PG 未 ready | `logs backend`；确认密码与 volume |
| Migration failure | SQL/权限/扩展 | 修库后重启 backend；勿伪装 healthy |
| PostgreSQL unavailable | 依赖未 healthy | `docker compose ps postgres` |
| health 显示 InMemory | 连错实例或本地未设 postgres | 检查 `REPOSITORY_BACKEND`；Compose 应恒为 postgres |
| Frontend 404 | 旧镜像 / 路径错误 | 重建 frontend；确认 History 路由 |
| 401 | 未登录 / Token 过期 | 重新 login |
| 403 | 权限不足 | 换角色；employee 不可 approve / AI管理 |
| 文档不可检索 | 未 Chunk / archived | Import→Chunk；searchable=yes |
| AI 按钮禁用 | 无证据 / 无权限 | 先 Retrieval；`analysis.execute` |
| Provider not ready | 无 Key/模型 | 配环境变量；保持 stub |
| Runtime 409 | expected_version 过期 | 重新 GET 再 PATCH |
| Kill Switch ON | 故意阻断真实调用 | Admin 关闭（需确认） |
| Volume 不可见 | 未 up 过 / 名称不同 | `docker volume ls \| grep erip` |

---

## 15. PostgreSQL 持久化

实际落库（企业路径）包括但不限于：

| 数据 | 说明 |
|---|---|
| `documents`（含 **content 正文**） | 元数据 + 解码后文本；**非**独立 Object Storage 桶 |
| imports / chunks / sessions | Import/Chunk 流水与切片 |
| tasks / events | 任务与事件 |
| reports / report_versions | 报告与不可变版本 |
| approvals / approval_events | 审批与 History |
| audit_logs | Persistent Audit |
| llm_usage_ledger 等 | 成本与额度 |
| **ai_runtime_settings** | Runtime mode / kill_switch / version |

- Volume 名：**`erip_postgres_data`**  
- 容器重启、`compose_down`（无 `-v`）后数据保留  
- **`down -v` 删除 Volume = 数据丢失风险**

---

## 16. Backup（命令模板；本轮不实际执行）

> **本轮文档任务不实际执行备份。** 以下按当前 Compose 默认 Service/DB/User 编写。

```bash
# 在项目根；目录与时间戳
mkdir -p backups
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
OUT="backups/erip_${STAMP}.sql"

# 使用容器内 pg_dump；密码经环境注入，避免命令行历史
# 默认用户/库：erip_app / erip（与 docker-compose.yml 一致）
docker compose exec -T \
  -e PGPASSWORD \
  postgres \
  pg_dump -U erip_app -d erip --no-password > "$OUT"

# 若未 export PGPASSWORD，可在交互环境使用：
# docker compose exec -T postgres \
#   env PGPASSWORD='***不要写进脚本仓库***' \
#   pg_dump -U erip_app -d erip --no-password > "$OUT"

# 核对
test -s "$OUT" && echo "backup_ok bytes=$(wc -c < "$OUT")"
# 确认连的是预期库：docker compose exec postgres psql -U erip_app -d erip -c 'SELECT current_database();'
```

**建议（建议值）：** 每日逻辑备份 + 定期恢复演练；备份文件权限收紧；勿把密码写进 Git。

---

## 17. Restore（命令模板；默认不执行）

```text
╔════════════════════════════════════════════════════════════╗
║  恢复可能覆盖目标库数据                                     ║
║  1) 停止写入（停 backend 或维护窗口）                        ║
║  2) 先再做一份当前库 backup                                 ║
║  3) 确认目标库名 / 用户 / 主机无误                          ║
║  4) 仅管理员在明确授权后执行                                ║
║  本轮部署文档任务：不实际执行 restore                       ║
╚════════════════════════════════════════════════════════════╝
```

示例（**仅作模板**）：

```bash
# 危险：覆盖 erip 库内容
# docker compose stop backend
# cat backups/erip_YYYYMMDDTHHMMSSZ.sql | \
#   docker compose exec -T -e PGPASSWORD postgres \
#   psql -U erip_app -d erip --no-password
# docker compose start backend
# curl -fsS http://127.0.0.1:8000/health
```

---

## 18. Upgrade

```text
确认版本 / 变更说明
  → Backup（第 16 节）
  → git pull（或发布包）
  → docker compose build
  → docker compose up -d
  → entrypoint 自动 alembic upgrade head
  → Health + compose_verify
  → Stub 冒烟（默认 stub，不开真实 LLM）
  → 页面验证（登录 / 文档 / RAG / 审批）
```

- **保留旧镜像 tag** 便于回滚  
- **不修改** 已发布旧 Migration 文件  
- 升级窗口保持 **`LLM_PROVIDER_MODE=stub`** / Runtime stub  
- **Seed 不随升级自动执行**

---

## 19. Rollback

| 类型 | 做法 | 注意 |
|---|---|---|
| 应用镜像回滚 | 部署上一镜像 tag；`up -d` | 先确认与 DB schema 兼容 |
| Migration downgrade | `alembic downgrade <rev>`（受控） | 可能丢列/表；需 DBA；**不是** `compose_down` |
| 数据恢复 | 第 17 节 restore | 覆盖风险 |

**不得**将 `docker compose down` 表述为数据库回滚。  
`compose_down` 只停容器；只有 `-v` 或 restore/downgrade 才改变数据面。

---

## 20. 本地开发（无需 Docker）

**仍必须连接宿主 PostgreSQL**（业务联调），不要用 InMemory 充当验收。

```bash
# 项目根
cp -n .env.example .env   # 若尚无 .env

export REPOSITORY_BACKEND=postgres
export DATABASE_URL='postgresql+psycopg://<user>:<password>@127.0.0.1:5432/<db>'
export LLM_PROVIDER_MODE=stub
# 首次需对目标库执行：cd backend && alembic upgrade head

./scripts/start_backend.sh
# → http://127.0.0.1:8000  （uvicorn --reload）

# 另开终端
./scripts/start_frontend.sh
# → http://127.0.0.1:5173  （Vite；代理 /api 与 /health → 8000）
```

| 地址 | 说明 |
|---|---|
| http://127.0.0.1:8000/health | 必须 `repository_backend=postgres` |
| http://127.0.0.1:8000/docs | Swagger |
| http://127.0.0.1:5173/login | Vite 开发登录页 |

**再次强调：**

- **5173** = Vite 开发；**8000** = Backend；**8080** = Compose 正式 Frontend  
- 本地 DB ≠ Docker Volume  
- 要看 Compose 里已有数据 → 使用 **8080**

---

## 21. Production 安全清单

- [ ] 移除 / 禁用 deterministic 测试账号  
- [ ] 企业 IdP / SSO（本仓库未交付完整产品化 IdP）  
- [ ] 强 `JWT_SECRET_KEY`  
- [ ] 强数据库密码；定期轮换  
- [ ] TLS / HTTPS 边缘终止  
- [ ] 正式域名 + Reverse Proxy  
- [ ] **不**对公网暴露 PostgreSQL 端口  
- [ ] 收紧 `CORS_ORIGINS`  
- [ ] Secret Manager 注入 Key  
- [ ] 日志脱敏（无 Token/Key/全文 Prompt）  
- [ ] Audit 保留策略  
- [ ] Backup + Restore 演练  
- [ ] Monitoring / Alert  
- [ ] 容器 Resource Limit  
- [ ] API Rate Limit  
- [ ] LLM Budget + Kill Switch 流程  
- [ ] 最小权限 RBAC  
- [ ] Volume 权限与备份加密  
- [ ] 非 root 运行（Backend 镜像已 `USER appuser`）  
- [ ] 镜像漏洞扫描  

---

## 22. 当前边界（未交付，禁止写成已完成）

| 项 | 状态 |
|---|---|
| 多租户 | 未交付 |
| Billing UI | 未交付 |
| SIEM 产品化 | 未交付 |
| WORM / Tamper Evidence | 未交付 |
| Streaming 平台化 | 未交付 |
| Kubernetes / HA 拓扑 | 未交付 |
| 自动 CI/CD 全流水线 | 未作为本仓库默认可运行完成项 |
| 完整监控告警台 | 未交付 |
| 企业 IdP | 未交付 |
| 真实付费 LLM smoke | 仅 opt-in；**默认验收禁止** |

默认验收：**stub / 零真实 LLM 调用**。

---

## 变更记录

| 日期 | 说明 |
|---|---|
| 2026-07-17 | 按 22 节结构重写：对齐 compose/entrypoint/scripts/Alembic head `20260717_08_ai_runtime`；明确本地开发也必须 PostgreSQL |

---

**原则**

1. 普通页面开发不需要 Docker。  
2. 业务联调与验收必须 PostgreSQL。  
3. Compose 默认 stub + `erip_postgres_data` 持久化。  
4. 禁止日常 `down -v`。  
5. Key 永不进库、不进镜像、不进前端。  
6. 生产 = Compose 基线 + 第 21 节硬化，不是默认 `.env` 原样上线。
