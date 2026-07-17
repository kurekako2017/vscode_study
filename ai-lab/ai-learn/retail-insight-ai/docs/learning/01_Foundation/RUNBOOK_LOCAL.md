# 启动与排错指南

这份文档用于本地启动 Retail Insight AI，并区分 Swagger、ReDoc、OpenAPI JSON、unittest、前后端联调各自的作用。

## ERIP 的三种运行与部署方式

| 方式 | 完整组成 | 日常启动命令 | 页面 | 用途 |
|---|---|---|---|---|
| **本地完整开发** | 宿主 PostgreSQL + Backend + Vite | **`./scripts/start_local.sh`** | **5173** | 页面开发与调试 |
| **Docker Compose** | 容器 PG + Backend + Nginx | **`./scripts/compose_up.sh`** | **8080** | 部署、验收、演示 |
| **正式生产** | HTTPS + 内网 Backend + 独立 PG | 由生产部署流程执行 | 正式域名 | 企业运行（非本地一条命令） |

**Docker / Compose 是什么：**

- **Docker**：镜像与容器运行技术。
- **Docker Compose**：多容器编排与统一启动（`docker-compose.yml`：`postgres` + `backend` + `frontend` + 网络/端口/Health Check/Volume `erip_postgres_data`/Alembic 启动顺序）。
- **不是**“只打包项目”；日常改页面**不必**开 Docker。
- Windows/WSL 下 Docker Desktop 有额外 CPU/内存开销；镜像占磁盘，运行容器占 CPU/Memory。

**必须记住：**

1. **Vite 不是第三套完整 Backend**，只是本地 Frontend 开发服务器；**只启动 Vite 无法完成业务测试**。
2. 本地 PostgreSQL 与 Docker Volume **默认是两个数据库**。
3. 本地 Frontend 若要使用 Docker 里的数据，应连正在运行的 **Docker Backend :8000**（Compose Frontend 则用 **8080**）；**不要**同时再起一个本地 Backend 争用 8000。
4. `/health` 必须显示 **`repository_backend=postgres`**。InMemory **不是**页面正式运行模式。
5. 方式三是生产架构，**不能**伪装成当前已完整自动化交付。

详细：[`docs/development/DEPLOYMENT_GUIDE.md`](../../development/DEPLOYMENT_GUIDE.md)。

### 首次配置 vs 日常启动（务必分开）

**首次配置（只做一次）：**

```bash
cp .env.example .env
# 编辑 .env：设置 DATABASE_URL 或 POSTGRES_HOST/PORT/DB/USER/PASSWORD
# .env 已被 gitignore，勿提交
# 确认宿主 PostgreSQL 已安装运行且账号可连
```

**日常本地启动 / 停止（不要再 export）：**

```bash
./scripts/start_local.sh
# 页面 http://127.0.0.1:5173/login
# Health http://127.0.0.1:8000/health

./scripts/stop_local.sh
```

`start_local.sh` 会自动：读根目录 `.env`、强制 postgres+stub、检查 PG、Alembic upgrade、起 Backend/Frontend、校验 health。
**禁止**把下面内容当日常命令：

```bash
# 不要日常这样做：
# export DATABASE_URL='...'
# export REPOSITORY_BACKEND=postgres
# export LLM_PROVIDER_MODE=stub
```

（底层脚本 `start_backend.sh` / `start_frontend.sh` 仍保留给进阶分终端调试。）

### Docker Compose 日常（一条命令）

```bash
./scripts/compose_up.sh
./scripts/compose_verify.sh
# 浏览器：http://127.0.0.1:8080/login

./scripts/compose_down.sh   # 禁止 down -v
```

---

## ERIP V1.0 当前权威启动入口

操作前先按场景选择章节，避免把历史阶段说明当成当前建议：

| 场景 | 权威入口 |
|---|---|
| **部署分层（本地 / Compose / 生产差距）** | **[`docs/development/DEPLOYMENT_GUIDE.md`](../../development/DEPLOYMENT_GUIDE.md)**（独立部署权威；本 RUNBOOK 不重复生产清单） |
| ERIP V1.0 正式启动 | [Appendix M](#appendix-m-docker-compose-启动与本地验收v10)：**Docker Compose + PostgreSQL**（默认且必须） |
| 本地 PostgreSQL 联调 | PostgreSQL 环境变量 + Backend/Frontend（见下文「本地 PostgreSQL 联调」；脚本步骤可参考 [Appendix L](#appendix-l-frontend-启动验证测试与停止)） |
| 快速单元测试 / 教学 | **InMemory，仅辅助用途**（unittest 加速 / 故障隔离；**不是**正式业务验收） |
| 最终业务验收 | **PostgreSQL + Stub E2E**（Appendix M + [Appendix N](#appendix-n-v10-启动验收基线最终状态)） |

### Repository 最终定位（V1.0）

- **PostgreSQL** 是 ERIP V1.0 **正式运行、企业验收与数据持久化**的权威 Repository。
- **Docker Compose 默认并必须使用 PostgreSQL**（`REPOSITORY_BACKEND=postgres`）。
- 最终业务链、人工验收、Stub E2E、Audit、Approval、Ledger、ReportVersion **均以 PostgreSQL 为准**。
- **InMemory 仅保留**为快速单元测试、教学适配器和故障隔离工具；**不作为正式业务验收结果**。
- **不**继续补齐 InMemory 的 PostgreSQL 企业能力；**不**删除 InMemory 代码（避免破坏快速测试）；**不**把 InMemory 写成推荐生产配置。
- 不得把「InMemory 已从代码删除」写成现状（代码仍存在）。

```text
本地脚本的 InMemory 默认值只为兼容快速学习；
正式运行请显式设置 REPOSITORY_BACKEND=postgres，或直接使用 Docker Compose。
```

### 本地测试账号（仅限本地 Stub/测试，非生产）

来源：`backend/tests/auth_test_utils.py` + `backend/app/security/user_provider.py`（bcrypt，应用不存明文）。

| 角色     | 用户名       | 密码（仅本地测试） | 用途                                 |
| -------- | ------------ | ------------------ | ------------------------------------ |
| admin    | `admin`    | `Admin#2026!`    | 全权限；**AI管理**；Audit      |
| manager  | `manager`  | `Manager#2026!`  | 审批 review/approve/reject           |
| employee | `employee` | `Employee#2026!` | 文档/RAG/AI分析/submit；approve→403 |

登录 API：`POST /api/v1/auth/login`。页面：`http://127.0.0.1:8080/login`（Compose 正式）或 `http://127.0.0.1:5173/login`（Vite 开发）。

### 8080 与 5173

| 端口           | 用途                                                                                           |
| -------------- | ---------------------------------------------------------------------------------------------- |
| **8080** | **正式 Docker Frontend**（连 Compose Backend + PostgreSQL）— 日常手动使用优先           |
| **5173** | **Vite 本地开发** Frontend（需自行 `start_frontend.sh`，并保证 Backend 指向 postgres） |
| 8000           | Backend API / Swagger`/docs`                                                                 |

### KPI任务分析 vs RAG/AI分析

| 入口        | 路径          | 含义                                                                                                   |
| ----------- | ------------- | ------------------------------------------------------------------------------------------------------ |
| KPI任务分析 | `/analysis` | 旧 Task API + SSE（hybrid/kpi/research），**不是** low_cost AI 成本入口                          |
| RAG/AI分析  | `/rag`      | 检索 +**显式** AI分析(low_cost) + 董事会报告(high_quality)；展示 Provider/Model/Route/Token/Cost |
| AI管理      | `/ai-admin` | 仅`security.manage`：查看/切换 `LLM_PROVIDER_MODE`（stub/openrouter/fallback_chain）               |

### Scenario01 导入 PostgreSQL

仓库路径：`docs/learning/sample-data/Scenario01_Sales_Decline/`（磁盘文件 **不会**自动入库）。

页面步骤：

1. 登录 employee/admin → **文書管理**
2. 上传 `01_…md`～`06_…md`（标题建议前缀 `SCENARIO01_ACCEPTANCE_<date>`）
3. 对每份文档 **Import** → **Chunk**
4. 在列表确认状态为 validated 且 Chunk 数 > 0 后再做 RAG

### 上传数据写在哪里

- **PostgreSQL `documents` 表**：元数据 + **正文 `content`**（解码后的文本，非独立对象存储桶）
- **chunks / imports / sessions** 等表：Import/Chunk 流水与切片
- 原始 multipart 文件：请求处理时读入内存/字节流并写入 DB 文本字段；**不**默认落到宿主机独立 uploads 目录（以当前 `DocumentUploadService` 为准）

### LLM 模式与成本

枚举（代码权威）：`stub` | `openrouter` | `fallback_chain`。

- **验收/日常：必须 stub**（零外呼费用）
- `fallback_chain`：OpenRouter→NVIDIA→Gemini→Local Qwen（可能付费；需服务端密钥）
- `openrouter`：单 Provider 兼容模式（需 Key）
- 管理页切换：`GET/PUT /api/v1/admin/llm/runtime`（不接收 Key；禁止打开 real smoke）
- 真实 smoke 仅 opt-in 环境变量，默认测试 suite 永不执行

### V1.0 正式前端导航

（与 `frontend/src/App.tsx` 一致，登录后可见项受 RBAC 过滤）

```text
学习总览
→ 文書管理
→ RAG/AI分析          （/rag：检索 + 显式 AI分析 + 董事会报告）
→ KPI任务分析         （/analysis：旧 Task API + SSE，不是 AI 成本入口）
→ 承認管理            （报告下拉选 task_id，无需手抄）
→ AI管理              （仅 admin / security.manage；LLM 模式开关）
```

**正式页面入口：**

| 环境                          | URL                       |
| ----------------------------- | ------------------------- |
| Docker/PostgreSQL（推荐日常） | `http://127.0.0.1:8080` |
| Vite 本地开发                 | `http://127.0.0.1:5173` |

说明：下文若仍出现 `Dashboard / Analysis / Tasks` / `RAG検索` / `分析依頼` 等旧标签，视为**历史阶段记录**；当前操作与验收以本节导航与上表端口为准。

## 目录

- [ERIP V1.0 当前权威启动入口](#erip-v10-当前权威启动入口)
- [三个文档入口不是同一个用途](#三个文档入口不是同一个用途)
- [企业项目验证体系](#企业项目验证体系)
- [推荐启动顺序](#推荐启动顺序)
- [如果要直接看后端原始输出](#如果要直接看后端原始输出)
- [Swagger / ReDoc / OpenAPI JSON 的使用方式](#swagger--redoc--openapi-json-的使用方式)
- [unittest 执行规则](#unittest-执行规则)
- [常见问题](#常见问题)
- [推荐验证顺序](#推荐验证顺序)
- [Appendix A: 初学者本地启动顺序](#appendix-a-初学者本地启动顺序)
- [Appendix B: 常见启动错误与修复](#appendix-b-常见启动错误与修复)
- [Appendix C: Quick Start（1 Minute Quick Start）](#appendix-c-quick-start1-minute-quick-start)
- [Appendix D: Startup Flow](#appendix-d-startup-flow)
- [Appendix E: Startup Checklist](#appendix-e-startup-checklist)
- [Appendix F: WSL + VSCode 使用建议](#appendix-f-wsl--vscode-使用建议)
- [Appendix G: VSCode Debug &amp; Run](#appendix-g-vscode-debug--run)
- [Appendix H: Interview Demo Startup](#appendix-h-interview-demo-startup)
- [Appendix I: Startup Decision Tree](#appendix-i-startup-decision-tree)
- [Appendix J: FAQ](#appendix-j-faq)
- [Appendix K: Frontend 页面学习路线](#appendix-k-frontend-页面学习路线)
- [Appendix L: Frontend 启动、验证、测试与停止](#appendix-l-frontend-启动验证测试与停止)
- [Appendix M: Docker Compose 启动与本地验收（V1.0）](#appendix-m-docker-compose-启动与本地验收v10)
- [Appendix N: V1.0 启动验收基线（最终状态）](#appendix-n-v10-启动验收基线最终状态)

## 推荐启动顺序

**正式推荐（PostgreSQL / Compose）：** 直接按 [Appendix M](#appendix-m-docker-compose-启动与本地验收v10) 执行 `compose_up` → `compose_verify` → Stub E2E → `compose_down`（禁止 `-v`）。

**本地脚本联调（若不用 Compose）：**

1. Terminal 1 在 `<project_root>` 执行 `./scripts/check_env.sh`。
2. **正式数据路径**：先 `export REPOSITORY_BACKEND=postgres` 与合法 `DATABASE_URL`，再 `./scripts/start_backend.sh`。
   （若省略，脚本可能落在 InMemory——**仅兼容快速学习，不作业务验收**。）
3. 保持 Terminal 1 中的 Backend 持续运行，不关闭，不按 `Ctrl+C`。
4. 验证：
   - `http://127.0.0.1:8000/health`（正式路径期望 `repository_backend=postgres`）
   - `http://127.0.0.1:8000/docs`
   - `http://127.0.0.1:8000/redoc`
   - `http://127.0.0.1:8000/openapi.json`
5. 另开 Terminal 2，在 `<project_root>` 执行 `./scripts/start_frontend.sh`。
6. 保持 Terminal 2 中的 Frontend 持续运行。
7. 浏览器打开 `http://127.0.0.1:5173`。

## 如果要直接看后端原始输出

这样做适合观察最原始的 FastAPI 启动日志和异常堆栈，命令与 Appendix C 保持一致，参见 [Appendix C](#appendix-c-quick-start1-minute-quick-start)。

## Swagger / ReDoc / OpenAPI JSON 的使用方式

### Swagger

用途：手工执行接口，验证请求、响应和业务流程。

推荐先点：

1. `GET /health`
2. `POST /api/tasks`
3. `GET /api/tasks/{task_id}`
4. `GET /api/tasks/{task_id}/report`

执行 `POST /api/tasks` 后，先看启动后端的终端日志，应该能直接看到 `[LEARNING REQUEST BODY]`，其中包含 `task_id`、`question` 和 `mode`，方便确认请求体是否按预期进入 `TaskService`。

### ReDoc

用途：阅读字段结构和响应模型，不适合高频点击调试。

### OpenAPI JSON

用途：确认接口定义是否真的注册，适合做合同检查和工具接入。

## unittest 执行规则

测试命令必须在 `<project_root>/backend` 目录执行，完整命令与单文件执行方式参见 Appendix E 和 Appendix C。

如果出现 `ModuleNotFoundError: No module named tests`，说明执行目录错了，不要先怀疑测试代码本身。

## 常见问题

### Swagger 打不开

先确认后端是否真的启动，再确认访问的是 `127.0.0.1:8000/docs`。

### ReDoc 打不开

说明后端可能没起来，或者路由未正常注册。先回头验证 `/health`。

### openapi.json 打不开

优先怀疑后端启动失败、接口注册失败或访问地址错误。

### unittest 找不到 tests

大概率是因为你不在 `backend/` 目录里执行。

### 审批或安全接口是空的

先确认你不是在空白进程里刚启动后立即读取；再看 `docs/LEARNING_API_WALKTHROUGH.md` 的推荐执行顺序。

## 推荐验证顺序

```text
Swagger
→ 主链路 API
→ 文档链路 API
→ 审批 / 安全 / 审计 API
→ backend unittest
→ React + FastAPI 联调
```

# Appendix A: 初学者本地启动顺序

这一章专门给第一次跑 `retail-insight-ai` 的同学看，目标是先把后端稳定启动起来，再逐步检查文档、前端和测试。

## 1. 进入项目根目录

命令参见 [Appendix C](#appendix-c-quick-start1-minute-quick-start)。

为什么这样做：

- 所有相对路径命令都以项目根目录为基准。
- `backend/requirements.txt`、`docs/learning/01_Foundation/RUNBOOK_LOCAL.md`、`scripts/` 都是在 `<project_root>` 下组织的。

## 2. 创建 `.venv`

命令参见 [Appendix C](#appendix-c-quick-start1-minute-quick-start)。

为什么这样做：

- 把项目依赖和系统 Python 隔离开。
- 新手最常见的问题就是“装过依赖，但不是装到当前解释器里”。

## 3. 激活 `.venv`

命令参见 [Appendix C](#appendix-c-quick-start1-minute-quick-start)。

激活成功后，命令行一般会出现 `(.venv)` 前缀。

## 4. 升级 `pip`

命令参见 [Appendix C](#appendix-c-quick-start1-minute-quick-start)。

为什么这样做：

- 新版 `pip` 更容易正确安装 `fastapi`、`uvicorn`、`python-multipart` 这类依赖。
- 遇到奇怪安装失败时，先升级 `pip` 往往最省时间。

## 5. 安装依赖

命令参见 [Appendix C](#appendix-c-quick-start1-minute-quick-start)。

为什么这样做：

- 后端依赖集中写在 `backend/requirements.txt`。
- 这一步会把 `python-multipart`、`fastapi`、`uvicorn` 等后端启动所需包装进当前 `.venv`。

## 6. 检查关键依赖

```bash
python -m pip show fastapi uvicorn python-multipart
python -c "import fastapi, uvicorn, multipart; print('dependency check ok')"
```

为什么这样做：

- `pip show` 可以确认包是否真的装进当前环境。
- `import multipart` 可以直接验证 `python-multipart` 是否可被当前 Python 解释器找到。

## 7. 检查 `.env`

```bash
cd <project_root>
test -f .env && echo ".env exists" || echo ".env missing, copy from .env.example if needed"
```

如果需要初始化：

```bash
cp <project_root>/.env.example <project_root>/.env
```

为什么这样做：

- 后端启动时会读取环境配置。
- 正式运行使用 PostgreSQL + stub/LLM 配置；保留 `.env` 习惯避免切换 Repository / Provider 时踩坑。

## 8. 启动 Backend

命令参见 [Appendix C](#appendix-c-quick-start1-minute-quick-start)。

为什么这样做：

- 这是当前项目约定的本地启动方式。
- 从 `backend/` 目录执行，可以确保 `app.main:app` 的导入路径正确。

## 9. 验证 `/health`

验证命令与 Appendix C 一致，直接访问 `http://127.0.0.1:8000/health`。

预期：

- 返回 200。
- 返回体里能看到健康状态信息。

## 10. 打开 Swagger / ReDoc / OpenAPI

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
http://127.0.0.1:8000/openapi.json
```

为什么这样做：

- Swagger 用于交互调试。
- ReDoc 用于阅读接口结构。
- OpenAPI JSON 用于检查接口合同是否正确注册。

## 11. 启动 Frontend（V1.0 正式联调步骤）

> **历史阶段记录**：早期骨架期曾把 Frontend 写成「可选」。
> **V1.0 当前**：Frontend 已交付（Login/JWT/RBAC/Learning Dashboard 等）；完整学习与 UI 验收应启动 Frontend。
> 若**仅**调试 Backend API，可先只完成 Appendix C，但不得再把「Frontend 可选」当作当前产品状态。

命令（权威步骤见 [Appendix L](#appendix-l-frontend-启动验证测试与停止)）：

```bash
# 项目根目录，Backend 已在 8000 运行后
./scripts/start_frontend.sh
# 浏览器：http://127.0.0.1:5173
```

为什么这样做：

- 先验证 Backend Health/Swagger，再联调 Frontend，更容易分层排错。
- 正式导航与业务链（文書管理 → … → 承認管理）需要在 UI 上走通。

## 12. 运行 `unittest`（推荐，非可选项）

命令参见 Appendix E；全量基线见 Appendix N。

为什么这样做：

- 单元测试是后端最稳定的回归保护。
- 如果启动成功但测试失败，就说明是业务逻辑或接口行为问题，不是纯启动问题。

# Appendix B: 常见启动错误与修复

## 1. `python-multipart` 未安装

现象：

- 启动时出现 `RuntimeError: Form data requires "python-multipart" to be installed.`
- 访问上传接口相关路由时直接报错。

原因：

- `FastAPI` 处理 `UploadFile`、`Form(...)` 时需要 `python-multipart`。
- 依赖没有装进当前 `.venv`，或者 `requirements.txt` 没有声明这个包。

检查命令：

```bash
python -m pip show python-multipart
python -c "import multipart; print('ok')"
```

修复命令：

参见 Appendix C 的完整安装流程；这里的关键是确保当前解释器里能找到 `python-multipart`。

## 2. `ModuleNotFoundError`

现象：

- 启动时提示 `ModuleNotFoundError: No module named 'app'`。
- 或者提示找不到某个后端模块。

原因：

- 你可能在错误目录执行命令。
- 也可能没有激活 `.venv`，导致解释器环境不对。

检查命令：

```bash
pwd
python -c "import sys; print(sys.executable)"
```

修复命令：

先回到 `<project_root>/backend`，再按 Appendix C 启动后端。

## 3. `uvicorn` 找不到

现象：

- 执行 `uvicorn ...` 时提示 `command not found`。

原因：

- `uvicorn` 没装进当前环境。
- 或者 `.venv` 没激活，系统 PATH 里没有这个命令。

检查命令：

```bash
which uvicorn
python -m pip show uvicorn
```

修复命令：

参见 Appendix C；如果 `uvicorn` 找不到，通常是 `.venv` 未激活或依赖未安装。

## 4. `8000` 端口被占用

现象：

- 启动时报 `Address already in use`。
- 或者 `port 8000 is already in use`。

原因：

- 另一个后端进程已经在监听 8000。

检查命令：

```bash
ss -ltnp | grep 8000
```

修复命令：

先结束占用 8000 的进程，再按 Appendix C 重新启动后端。

## 5. `.venv` 没有激活

现象：

- `python -V` 不是项目里的解释器。
- `pip install` 后依赖还是找不到。

原因：

- 你执行命令时使用了系统 Python，而不是项目虚拟环境。

检查命令：

```bash
which python
python -m pip -V
```

修复命令：

参见 Appendix F 的 WSL + VSCode 检查方法。

## 6. `requirements` 没装完整

现象：

- 后端部分模块能导入，部分模块导入失败。
- 上传、文档解析、Swagger 相关页面启动不完整。

原因：

- 依赖只装了一部分。
- 或者中途安装失败，但你没有注意到报错。

检查命令：

```bash
python -m pip check
python -m pip freeze | sed -n '1,120p'
```

修复命令：

回到 Appendix C 的安装步骤，重新安装依赖后再执行 `python -m pip check`。

## 7. 在错误目录执行命令

现象：

- `python -m unittest discover -s tests -v` 找不到测试。
- `python -m uvicorn app.main:app` 报导入错误。

原因：

- `backend/` 下的命令被放到了项目根目录执行。
- 或者根目录命令被放到了 `backend/` 里执行。

检查命令：

```bash
pwd
```

修复命令：

先切换到 `<project_root>/backend`，再按 Appendix C 启动后端。

# Appendix C: Quick Start（1 Minute Quick Start）

第一次 Clone 项目后，先直接照着执行下面这组命令。

```bash
cd <project_root>
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
cd <project_root>/backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

启动后立刻做最小健康检查：

```bash
curl http://127.0.0.1:8000/health
```

再打开 Swagger：

```text
http://127.0.0.1:8000/docs
```

# Appendix D: Startup Flow

V1.0 **正式启动主路径**（PostgreSQL；权威步骤见 Appendix M）：

```text
Project Root
↓
Docker Compose up（postgres + backend + frontend）
↓
compose_verify + Stub E2E
↓
浏览器 http://127.0.0.1:8080
  学习总览 → 文書管理 → RAG/AI分析 → KPI任务分析 → 承認管理 → AI管理
↓
compose_down（禁止 -v）
```

V1.0 **本地脚本路径**（兼容；见 Appendix L）：

```text
Project Root → .venv → （正式）REPOSITORY_BACKEND=postgres
  或（仅快速教学）省略后可能 InMemory（不作业务验收）
→ start_backend + start_frontend → http://127.0.0.1:5173
```

> **历史阶段记录**：旧流程图曾以 InMemory 为主、Frontend Optional。
> **V1.0 当前**：Frontend 正式；**Repository 权威为 PostgreSQL**；InMemory 仅辅助。

最终数字见 Appendix N。

# Appendix E: Startup Checklist

第一次运行时，可以逐项勾选。

- [ ] Python 已安装
- [ ] 项目根目录已进入
- [ ] `.venv` 已创建
- [ ] `.venv` 已激活
- [ ] `requirements.txt` 已安装
- [ ] `.env` 已存在
- [ ] **正式路径**：Compose 已 up（Appendix M）或已 `REPOSITORY_BACKEND=postgres`
- [ ] Backend 已启动；`GET /health` 返回 200 且正式路径为 `repository_backend=postgres`
- [ ] Swagger / ReDoc / openapi 可打开
- [ ] Frontend 已启动（Compose `:8080` 或本地 `:5173`）
- [ ] 正式导航可见：学习总览 → 文書管理 → RAG/AI分析 → KPI任务分析 → 承認管理 → AI管理
- [ ] **业务验收**：Stub E2E / 人工链以 PostgreSQL 为准（Appendix M/N）
- [ ] **辅助**：InMemory unittest 可选；不作业务结论

# Appendix F: WSL + VSCode 使用建议

- 本项目建议优先使用 WSL Ubuntu 里的 Python，而不是 Windows 系统 Python。
- 不要混用 Windows Python 和 WSL Python，否则 `.venv`、`pip`、`uvicorn`、`python -m unittest` 可能指向不同环境。
- 检查当前 Python：

```bash
which python
python -V
python -c "import sys; print(sys.executable)"
```

- 检查当前 pip：

```bash
which pip
python -m pip -V
```

- 确认 VSCode 使用的是 `.venv`：

```bash
which python
python -m pip -V
```

如果输出路径在项目 `.venv` 下，通常就是对的。

- VSCode Terminal 建议从 `<project_root>` 打开，再执行 `source .venv/bin/activate`。
- 如果 Terminal 里看到的 Python 路径不是项目 `.venv`，先切换解释器，再重新打开 Terminal。

# Appendix G: VSCode Debug & Run

第一次接触 VSCode 时，可以按下面顺序做。

1. 打开 VSCode。
2. 打开项目根目录。
3. 打开 Terminal。
4. 选择 Python Interpreter，指向项目 `.venv`。
5. 在 Terminal 里执行 Appendix C 的启动命令。
6. 看 Terminal Log 是否出现 `Application startup complete`。
7. 如果要调试，把运行方式换成 VSCode 的 Python Debugger，再启动 `app.main:app`。
8. 调试时优先看 Terminal 输出，不要只看浏览器页面。

# Appendix H: Interview Demo Startup

面试演示建议按这个顺序。

路径 A：Backend API 闭环（适合先讲后端主链）

```text
Backend
↓
Health
↓
Swagger
↓
Create Task
↓
Task Status
↓
SSE
↓
Report
↓
结束
```

路径 B：V1.0 正式 UI 闭环（适合讲前后端联调与 RBAC）

```text
Backend + Frontend
↓
登录
↓
学习总览
↓
文書管理 → RAG/AI分析 → KPI任务分析 → 承認管理 → AI管理
↓
（需要时）Compose / PostgreSQL 验收见 Appendix M
```

为什么按这个顺序演示：

- 先证明服务活着，再证明接口可读。
- 再证明能创建任务、能观察任务状态、能看到实时进度。
- 最后展示报告或 UI 业务链，说明这是一个完整闭环，不是单点接口。
- 不要用「Frontend 可选 / 当前阶段只有 Backend」当作 V1.0 交付结论。

# Appendix I: Startup Decision Tree

```text
Backend 启动失败？
↓
ImportError？
↓
YES → 安装 requirements → 再启动
↓
NO
↓
Port 被占用？
↓
YES → kill 进程 → 再启动
↓
NO
↓
检查 .env
↓
检查 .venv
↓
检查 Python
↓
仍然失败 → 回看 Appendix B
```

如果更细一点，也可以按下面思路排：

- 先看是不是导入错误。
- 再看是不是端口占用。
- 再看是不是环境变量缺失。
- 再看是不是 `.venv` 没激活。
- 再看是不是 Python / pip 指到了别的环境。

# Appendix J: FAQ

## Q1. 为什么必须进入 backend 再启动？

因为 `app.main:app` 是后端入口，很多相对路径和依赖默认都以 `<project_root>/backend` 为基准。如果在项目根目录直接启动，容易出现导入路径或测试发现路径不一致的问题。新手最稳妥的做法就是先进入 `<project_root>/backend`，再运行后端命令。

## Q2. 为什么使用 `python -m uvicorn`？

这样会让 `python` 和 `uvicorn` 来自同一个解释器环境，减少“命令找得到，但依赖找不到”的问题。对新手来说，这比直接敲 `uvicorn` 更稳，也更容易排查问题。这个写法同样适合调试和文档复制执行。

## Q3. 为什么使用 `python -m pip`？

因为它明确表示“用当前 Python 对应的 pip”。如果直接用 `pip`，很容易装到系统环境或别的虚拟环境里。新手第一优先级是让安装和运行使用同一个解释器。

## Q4. 为什么不要 `sudo pip install`？

`sudo pip install` 很容易把依赖装到系统环境，后面会污染别的项目。它也会掩盖 `.venv` 没激活的问题。这个项目更推荐把所有安装都放进 `.venv`。

## Q5. 为什么使用 `.venv`？

`.venv` 可以把项目依赖和系统环境隔离开。这样你升级、删除或重装依赖时，不会影响别的项目。对初学者来说，这也是最容易复现和排错的方式。

## Q6. 为什么先跑 Health，再看 Swagger？

`/health` 是最轻量的启动验证点，能最快确认服务已经活着。只有服务真正启动后，再打开 Swagger 才有意义。这个顺序可以帮助你快速判断问题是在“服务没起来”还是“接口文档没注册”。

# Appendix K: Frontend 页面学习路线

这一章是新增的 Frontend 学习入口。

注意：

- 这一章是追加内容
- 不替换原来的 Backend API 学习入口
- 原来的 `Health → Swagger → Task API` 路线继续保留

也就是说，当前项目有两条长期并存的学习路线：

第一条：

```text
Backend
→ Health
→ Swagger
→ Task API
→ API 调试
```

第二条（**V1.0 正式导航**）：

```text
Backend
→ 确认 Health
→ 确认 Swagger
→ Frontend（登录后）
→ 学习总览
→ 文書管理
→ RAG/AI分析
→ KPI任务分析
→ 承認管理
→ AI管理
```

> **历史阶段记录**：旧文曾写 `Dashboard → Analysis / Tasks → Documents → RAG → Approval` 英文标签。
> 代码与 UI 现已统一为上方中文正式导航；学习时以正式导航为准。

## K-1. Frontend 页面学习总顺序

```text
Backend 启动
↓
确认 Health
↓
确认 Swagger
↓
启动 Frontend
↓
打开浏览器 http://127.0.0.1:5173
↓
登录（如需）
↓
学习总览
↓
文書管理
↓
RAG/AI分析
↓
KPI任务分析
↓
承認管理
↓
AI管理
```

## K-2. 学习总览（Dashboard 路由）

页面操作：

- 打开首页 / 学习总览
- 点击快捷入口进入 `文書管理` / `RAG/AI分析` / `KPI任务分析` / `承認管理` / `AI管理`（文案以页面按钮为准）

对应 API：

- 无（总览页本身；子页另有 API）

预期结果：

- 默认先显示 **学习总览**
- 点击快捷按钮后切换到对应页面

如何确认成功：

- 顶部导航高亮变化
- Network 中没有新的 API 请求（仅切换路由时）
- 页面内容已经切换
- 导航顺序符合：学习总览 → 文書管理 → RAG/AI分析 → KPI任务分析 → 承認管理 → AI管理

## K-3. KPI任务分析（历史标题曾写作 Analysis / Tasks）

页面操作：

- 输入问题
- 选择 `hybrid` / `kpi` / `research`
- 点击 `分析を開始`

对应 API：

- `POST /api/tasks`
- `GET /api/tasks/{task_id}/events`
- `GET /api/tasks/{task_id}/report`

预期结果：

- 成功创建任务
- 页面显示状态流转
- 最终显示报告

如何确认成功：

- Network 中先看到 `POST /api/tasks`
- 再看到 SSE `GET /api/tasks/{task_id}/events`
- 最后看到 `GET /api/tasks/{task_id}/report`
- 页面出现报告内容

## K-4. 文書管理（Documents 路由）

页面操作：

- 查看列表
- 上传文件
- 查看详情
- 点击 `Archive`
- 点击 `Import`
- 点击 `Chunk`

对应 API：

- `GET /api/v1/documents`
- `POST /api/v1/documents`
- `GET /api/v1/documents/{document_id}`
- `DELETE /api/v1/documents/{document_id}`
- `POST /api/v1/documents/{document_id}/import`
- `POST /api/v1/documents/{document_id}/chunks`
- `GET /api/v1/documents/{document_id}/chunks`

预期结果：

- 列表能显示真实文档
- 上传后能刷新列表
- 详情与 chunk 预览能刷新

如何确认成功：

- 上传后看到成功 Banner
- Network 中看到上传成功后再次请求文档列表
- 点击单条文档后能看到详情和 chunks 请求

补充学习文档：

- `docs/learning/02_Frontend/FRONTEND_SOURCE_LEARNING_GUIDE.md`
- `docs/learning/02_Frontend/TEST_LEARNING_DOCUMENTS_PAGE.md`

## K-5. RAG/AI分析

页面操作：

- 输入 Query，点击 `Search Retrieval`
- 输入 Question，点击 `Generate Answer`

对应 API：

- `POST /api/v1/document-retrieval/search`
- `POST /api/v1/internal-rag/answer`

预期结果：

- Retrieval 返回结果列表
- Internal RAG 返回 grounded answer、citations、confidence、warnings

如何确认成功：

- Network 中看到两个真实 POST 请求
- 页面显示 `retrieval_mode`
- 页面显示 citations 和 warnings

## K-6. 承認管理（Approval 路由）

页面操作：

- 查看审批列表
- 查看详情
- 提交审批
- Approve
- Reject
- Request Revision

对应 API：

- `GET /api/v1/approvals`
- `GET /api/v1/approvals/{approval_id}`
- `POST /api/v1/reports/{task_id}/submit-approval`
- `POST /api/v1/approvals/{approval_id}/approve`
- `POST /api/v1/approvals/{approval_id}/reject`
- `POST /api/v1/reports/{task_id}/revise`

预期结果：

- 列表与详情可读
- 提交与审批后页面会刷新
- 403 / 409 错误能显示在页面

如何确认成功：

- 页面出现成功或错误 Banner
- Network 中看到刷新后的列表和详情请求
- 页面状态 badge 变化

# Appendix L: Frontend 启动、验证、测试与停止

## L-0. 先区分两种操作

这一章最容易混的，是下面两件事其实不是同一回事：

第一种：

```text
页面学习启动
=
启动 Backend + 启动 Frontend + 打开浏览器
```

第二种：

```text
自动化测试启动
=
运行 unittest / vitest / build / compileall
```

请先分清：

- 想手动点页面，就走“页面学习启动”
- 想验证回归结果，就走“自动化测试启动”

**V1.0 当前**双终端联调权威入口（不再使用「Frontend Phase 3」阶段称呼作为当前状态）：

页面学习：

```bash
./scripts/start_backend.sh
./scripts/start_frontend.sh
```

自动化测试：

```bash
./scripts/run_tests.sh
```

> **历史阶段记录**：旧文曾写「Frontend Phase 3 权威入口」。Phase 3 是开发过程标签；**交付状态以本文顶部「ERIP V1.0 当前权威启动入口」与 Appendix N 为准**。

前面 Appendix A ~ J 保留的是原有学习路径和手动命令说明。
这一章是 **本地脚本双终端联调**入口：正式数据请 `REPOSITORY_BACKEND=postgres`；**业务验收权威路径仍是 Appendix M（Compose + PostgreSQL）**。InMemory 仅辅助，不作业务结论。

## L-1. 环境准备

当前项目 Frontend 本地运行至少需要：

- `python3`
- `pip`
- `node`
- `npm`

真实检查脚本：

```bash
./scripts/check_env.sh
```

## L-2. Python 环境

Backend 启动脚本会使用：

- `backend/.venv`

真实脚本：

- `scripts/start_backend.sh`

## L-3. Node 环境

Frontend 启动依赖：

- `node`
- `npm`

真实脚本：

- `scripts/start_frontend.sh`

## L-4. 安装依赖

Backend 依赖：

```bash
./scripts/start_backend.sh
```

这个脚本会自动执行：

- 创建 `backend/.venv`
- 安装 `backend/requirements.txt`

Frontend 依赖：

```bash
./scripts/start_frontend.sh
```

这个脚本会自动检查 `frontend/node_modules`，不存在时执行 `npm install`。

## L-5. Backend 启动

推荐：

```bash
./scripts/start_backend.sh
```

手动方式：

```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## L-6. Backend 验证

Health：

```bash
curl http://127.0.0.1:8000/health
```

Swagger：

```bash
curl -I http://127.0.0.1:8000/docs
```

OpenAPI：

```bash
curl -sS http://127.0.0.1:8000/openapi.json | head
```

## L-7. Frontend 启动

推荐：

```bash
./scripts/start_frontend.sh
```

手动方式：

```bash
cd frontend
npm run dev -- --host 127.0.0.1
```

双终端学习时建议这样开：

终端 1：

```bash
./scripts/start_backend.sh
```

终端 2：

```bash
./scripts/start_frontend.sh
```

## L-8. Frontend 验证

浏览器地址：

- `http://127.0.0.1:5173`

成功标志：

- 能看到 **学习总览**（路由可为 `/` 或 `/dashboard`）
- 顶部导航包含正式标签：

```text
学习总览
→ 文書管理
→ RAG/AI分析
→ KPI任务分析
→ 承認管理
→ AI管理
```

- （历史对照）旧文档英文标签 `Dashboard / Analysis / Tasks / Documents / RAG / Approval` 不再作为当前 UI 验收标准

## L-9. 浏览器地址总表

- Backend Health: `http://127.0.0.1:8000/health`
- Backend Swagger: `http://127.0.0.1:8000/docs`
- Backend ReDoc: `http://127.0.0.1:8000/redoc`
- Backend OpenAPI: `http://127.0.0.1:8000/openapi.json`
- Frontend: `http://127.0.0.1:5173`

## L-10. 自动化测试

这一节不是“启动页面”，而是“跑自动化验证”。

也就是说：

- 页面学习时，不需要先跑这一节
- 收尾验证、提交前检查时，再跑这一节

全部检查：

```bash
./scripts/run_tests.sh
```

Backend tests：

```bash
cd backend
python3 -m unittest discover -s tests -v
```

Frontend 全部测试：

```bash
cd frontend
npm test
```

Frontend build：

```bash
cd frontend
npm run build
```

Python compileall：

```bash
cd backend
python3 -m compileall app
```

单页面测试命令：

```bash
cd frontend
npm test -- --run src/pages/DashboardPage.test.tsx
npm test -- --run src/pages/TasksPage.test.tsx
npm test -- --run src/pages/DocumentsPage.test.tsx
npm test -- --run src/pages/RagPage.test.tsx
npm test -- --run src/pages/ApprovalPage.test.tsx
```

API Client 测试：

```bash
cd frontend
npm test -- --run src/api.test.ts
```

V1.0 补充：PostgreSQL 全量 Backend suite（需要本机或专用测试库 `erip_integration_test`）：

```bash
cd backend
export REPOSITORY_BACKEND=postgres
export DATABASE_URL="postgresql+psycopg:///erip_integration_test?host=/var/run/postgresql"
export LLM_PROVIDER_MODE=stub
# 可选：固定哈希种子，便于对比偶发问题
export PYTHONHASHSEED=0
python3 -m unittest discover -s tests -v
```

V1.0 补充：Compose Stub API E2E（先 `compose_up` 且 Backend 在 8000）：

```bash
# 在项目根目录
export E2E_BASE_URL=http://127.0.0.1:8000
export E2E_EXPECT_STUB=1
./scripts/run_api_e2e.sh
```

当前 V1.0 自动化基线数字见 [Appendix N](#appendix-n-v10-启动验收基线最终状态)。

## L-11. 停止项目

如果你是直接运行：

- `./scripts/start_backend.sh`
- `./scripts/start_frontend.sh`

最直接的停止方法就是在对应终端按：

```text
Ctrl+C
```

如果你在 WSL / VSCode 终端中关闭了窗口，开发服务也会一起退出。

## L-12. 常见错误

### Backend 无法启动

优先检查：

- `python3` 是否存在
- `backend/.venv` 是否创建成功
- `backend/requirements.txt` 是否安装成功
- `8000` 端口是否被占用

### Frontend 无法启动

优先检查：

- `node` / `npm` 是否存在
- `frontend/node_modules` 是否安装成功
- `5173` 端口是否被占用

### Health 失败

说明 Backend 还没有正常启动，先不要继续查 Frontend。

### Swagger 打不开

先确认：

- `http://127.0.0.1:8000/health` 是否已经成功

### Task Pending 很久

先检查：

- Backend 终端是否仍在运行
- SSE 请求是否建立
- 是否收到了 `done` 事件

### Documents 上传失败

先检查：

- 上传的是不是当前支持的文件类型
- metadata 是否填写完整
- 页面错误 Banner 里的错误码

### RAG `insufficient_context`

这通常表示：

- 当前检索没有找到足够证据

这不是 Frontend 启动失败，而是业务返回结果为空或证据不足。

### Approval 403

这表示：

- 当前审批动作被权限边界拒绝

页面应显示错误 Banner。

### Approval 409

这表示：

- 当前审批状态冲突
- 比如重复提交、重复决策或状态不允许

### PostgreSQL 验收说明（V1.0 权威 Repository）

历史笔记中曾出现「PostgreSQL 仅 skipped / 未完成」的表述。
**V1.0 最终定位**：**PostgreSQL 是正式运行与业务验收的权威 Repository**；InMemory **仅**保留为快速单元测试/教学适配器，**不是**正式业务验收结果，也**不会**继续补齐 PostgreSQL 企业能力。

当前 Backend 基线（以本机最近稳定验收为准）：

| 模式                  | 结果                                                                                           | 用途                                      |
| --------------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------- |
| PostgreSQL 全量 suite | **281 tests**，**2** 个 real smoke 默认 **skipped**；发布基线曾连续 3 次稳定 | **正式回归**                        |
| InMemory 全量 suite   | **270 tests**，**52 skipped**                                                      | **辅助**（加速/隔离；不作业务结论） |

PostgreSQL 需要：

- 专用测试库名必须是 `erip_integration_test`（防止误清业务库）
- 环境变量 `REPOSITORY_BACKEND=postgres` 与合法 `DATABASE_URL`
- 默认 `LLM_PROVIDER_MODE=stub`（验收零真实 LLM 费用）

命令与注意点见 L-10 补充段与 Appendix N。

### Docker / Compose 验收说明（V1.0 已落地）

历史笔记中曾写「Docker 未验证」。
**V1.0 最终状态**：在 Docker Desktop Engine 与 WSL Integration 可用时，下列项已通过：

- image build
- `docker compose config`
- postgres / backend / frontend healthy
- Alembic 自动迁移到 `20260717_07_fallback_chain`
- Frontend History API 路由刷新 200
- Stub E2E
- `compose_down` **不带 `-v`**，Volume 保留后重启数据仍在

如果本地 **没有** Docker CLI 或 daemon 未启动，仍然不要假装通过；应明确记录「本机 Docker 不可用，未执行 Compose 验收」。
完整步骤见 [Appendix M](#appendix-m-docker-compose-启动与本地验收v10)。

### WSL 关闭导致服务退出

如果你关闭了 WSL 终端或 VSCode 远程会话，正在运行的本地开发服务通常也会结束。

# Appendix M: Docker Compose 启动与本地验收（V1.0）

本附录是 **ERIP V1.0 正式启动与业务验收的权威路径**（Docker Compose + PostgreSQL）。
本地脚本（Appendix A / C / L）仍保留作兼容与快速教学，**不替代**本附录的正式地位。

## M-1. 何时用 Compose

| 场景                      | 推荐                                                       |
| ------------------------- | ---------------------------------------------------------- |
| 正式启动 / 企业业务验收   | **Compose + PostgreSQL**（本附录，权威）             |
| 本地 PostgreSQL 联调      | 显式`REPOSITORY_BACKEND=postgres` + 本地脚本             |
| 快速改代码 / 单元测试加速 | 本地脚本可能默认 InMemory（**辅助**；不作业务验收）  |
| 默认费用安全验收          | Compose 默认`LLM_PROVIDER_MODE=stub`，不要默认开真实 LLM |

## M-2. 前置条件

1. Docker CLI 可用：`docker version` 能看到 Client **与** Server。
2. Compose v2 可用：`docker compose version`（示例：`v2.40.3-desktop.1`）。
3. 不在启动前 `kill` 用户进程。
4. 检查端口占用（只观察，不杀进程）：

```bash
ss -ltn | grep -E ':8000|:8080|:5432|:5433' || true
```

若宿主 **5432 已被本机 PostgreSQL 占用**，Compose 发布 Postgres 时改用：

```bash
export POSTGRES_PORT=5433
```

Backend / Frontend 默认：

```bash
export BACKEND_PORT=8000
export FRONTEND_PORT=8080
```

## M-3. 推荐命令顺序（项目根目录）

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai

# 可选：端口映射（宿主 5432 被占用时）
export POSTGRES_PORT=5433
export BACKEND_PORT=8000
export FRONTEND_PORT=8080

# 1) 证明 .env 不会进镜像；Compose 默认 stub
./scripts/prove_dockerignore.sh

# 2) 渲染后的配置（可人工确认 LLM_PROVIDER_MODE: stub 与 published 端口）
docker compose config

# 3) 构建并启动（Postgres healthy → Alembic upgrade → uvicorn → frontend）
./scripts/compose_up.sh

# 4) 健康、SPA 路由、镜像无 .env
./scripts/compose_verify.sh

# 5) Stub 企业业务链 API E2E（零真实 LLM）
export E2E_BASE_URL=http://127.0.0.1:8000
export E2E_EXPECT_STUB=1
./scripts/run_api_e2e.sh
```

## M-4. 必须看到的健康结果

| 检查项                                                         | 期望                                                                                                             |
| -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `docker compose ps`                                          | postgres / backend / frontend 均为 running 且 healthy（或 frontend healthy）                                     |
| `curl http://127.0.0.1:8000/health`                          | `status=ok`，`repository_backend=postgres`（Compose 路径）                                                   |
| `curl -o /dev/null -w '%{http_code}' http://127.0.0.1:8080/` | `200`                                                                                                          |
| SPA 路由（History API 刷新）                                   | `/` `/login` `/dashboard` `/documents` `/rag` `/analysis` `/approval` 均为 **200**，不是 404 |
| Alembic                                                        | `docker compose exec backend alembic current` → `20260717_07_fallback_chain (head)`                         |
| LLM                                                            | 容器内`LLM_PROVIDER_MODE=stub`；默认验收 **零真实 LLM 调用**                                             |

`compose_verify.sh` 已覆盖 Frontend 多路由 200 与 Backend health。

## M-5. Stub E2E 覆盖什么

`./scripts/run_api_e2e.sh` → `backend/tests/test_e2e_api_stub_flow.py`（对 `E2E_BASE_URL` 发 HTTP）：

```text
三角色登录（admin / manager / employee）
→ 文档 Upload / Import / Chunk
→ Retrieval
→ AI 分析（stub-low-cost）
→ 董事会报告（stub-high-quality）
→ submit Approval
→ employee approve → 403
→ manager approve → 成功
→ Audit 可读
→ Usage Ledger 有 stub 成功记录
→ 普通 Retrieval / extractive RAG 不强制真实 Provider 外呼
```

成功标志：终端出现 `OK`，且过程中 **不要** 打印 Token / API Key。

## M-6. 数据持久化验收（禁止 `down -v`）

```bash
# 1) 在运行中的系统创建一条可识别的专用数据（例如带 PERSIST_PROBE_ 前缀的文档标题）
# 2) 记录安全 ID（document_id），不要记录密码/Token
# 3) 停止容器（脚本拒绝 -v）
./scripts/compose_down.sh

# 4) 确认 volume 仍在
docker volume ls | grep erip_postgres_data

# 5) 再启动并 verify
./scripts/compose_up.sh
./scripts/compose_verify.sh

# 6) 用同一 document_id / 标题确认数据仍在
# 7) 再 down，仍然不要 -v
./scripts/compose_down.sh
```

`scripts/compose_down.sh` 会拒绝 `-v` / `--volumes`，避免误删学习数据。

## M-7. Compose 常见错误

| 现象                                                    | 可能原因                              | 处理                                                                               |
| ------------------------------------------------------- | ------------------------------------- | ---------------------------------------------------------------------------------- |
| `Docker daemon 未运行`                                | Docker Desktop / WSL Integration 未开 | 先恢复 Desktop，再`docker info`                                                  |
| backend unhealthy，`No such file: /app/db/schema.sql` | 旧镜像未 COPY`db/`                  | 确认`backend/Dockerfile` 含 `COPY db ./db` 后 `docker compose build backend` |
| 5432 bind 失败                                          | 宿主 PostgreSQL 占用                  | `POSTGRES_PORT=5433`                                                             |
| E2E 401                                                 | 测了错误账号或服务未 ready            | 使用`admin` / `manager` / `employee` 与文档中的测试密码约定；先 `/health`  |
| 想「彻底清空」                                          | 误用`docker compose down -v`        | **禁止**；验收路径只允许保留 volume 的 down                                  |

## M-8. 与本地脚本路径的关系

```text
Compose 路径（本附录，权威）
  compose_up / verify / e2e / down
  → V1.0 正式运行与业务验收；PostgreSQL + 迁移 + SPA

本地脚本路径（兼容）
  start_backend.sh + start_frontend.sh
  → 正式联调须 REPOSITORY_BACKEND=postgres
  → 省略时可能 InMemory，仅快速学习/单元测试，不作业务验收
```

两条路径都要会；**不要**删除本地脚本章节，也**不要**把 InMemory 默认当成正式运行。

# Appendix N: V1.0 启动验收基线（最终状态）

本附录固定 **文档编写时点** 的最终验收数字与禁止项，供启动手册与测试手册共用。
数字以本仓库已完成回归为准；若你本机结果不同，先查环境，再改文档。

## N-1. Backend

| 项                                    | 基线                                                                        |
| ------------------------------------- | --------------------------------------------------------------------------- |
| PostgreSQL 全量（**正式回归**） | **281 tests**，**2 skipped**（real LLM smoke 默认 skip）        |
| PostgreSQL 稳定性                     | 完整 suite**连续 3 次** 通过（修复 JWT 时钟回拨后）                   |
| InMemory 全量（**仅辅助**）     | **270 tests**，**52 skipped**；不作业务验收结论                 |
| Alembic head                          | `20260717_07_fallback_chain`                                              |
| Repository 权威                       | **PostgreSQL**（Compose 默认且必须）；InMemory 代码保留但不补企业能力 |
| `python -m compileall app`          | 通过                                                                        |
| `git diff --check`                  | 通过                                                                        |
| 默认 LLM                              | `LLM_PROVIDER_MODE=stub`；默认验收 **零真实 LLM 费用**              |

## N-2. Frontend

| 项                                                | 基线                                                   |
| ------------------------------------------------- | ------------------------------------------------------ |
| 测试                                              | **113 / 113**                                    |
| Production build                                  | 通过                                                   |
| Login / JWT / ProtectedRoute / RBAC Permission UI | 已完成                                                 |
| React Lifecycle Live Status                       | 已完成                                                 |
| Frontend Learning Dashboard                       | 已完成                                                 |
| 开发服务器                                        | `http://127.0.0.1:5173`（`start_frontend.sh`）     |
| Compose 前端                                      | `http://127.0.0.1:8080`（nginx SPA + `/api` 代理） |

## N-3. Docker / Compose

| 项                            | 基线                                        |
| ----------------------------- | ------------------------------------------- |
| image build                   | 通过                                        |
| compose config                | 通过                                        |
| postgres / backend / frontend | healthy                                     |
| Alembic 自动迁移              | 通过（entrypoint）                          |
| History API 路由刷新          | `/login` 等 200                           |
| Stub E2E                      | 通过                                        |
| down 后 volume 保留与数据恢复 | 通过                                        |
| 禁止                          | `docker compose down -v` 作为日常验收步骤 |

## N-4. 业务链（人工 + Stub E2E 共同指向）

```text
文書管理
→ RAG/AI分析
→ KPI任务分析
→ 承認管理
→ AI管理
→ 最终审计报告
```

样例业务数据目录（人工走 UI 时使用，不替代自动化）：

```text
docs/learning/sample-data/Scenario01_Sales_Decline/
```

详细业务步骤与检查表见：

- `docs/learning/sample-data/Scenario01_Sales_Decline/10_業務テストシナリオ.md`
- `docs/learning/01_Foundation/TEST_CASES.md` 文末「V1.0 业务数据验证与验收」

## N-5. 启动路径对照（保留原路径）

| 路径                    | 命令入口                                     | 典型用途                                  |
| ----------------------- | -------------------------------------------- | ----------------------------------------- |
| A. Compose + PostgreSQL | `compose_up.sh` 等                         | **V1.0 正式启动与业务验收（权威）** |
| B. 本地脚本 + postgres  | `REPOSITORY_BACKEND=postgres` + start_*    | 本地 PostgreSQL 联调                      |
| C. 本地脚本 / InMemory  | start_* 未设 postgres                        | **仅**快速学习/单元测试辅助         |
| D. 自动化               | PG suite（正式）/ InMemory（辅助）/ npm test | 业务结论只看 PostgreSQL                   |

原 Appendix A～L 的命令 **全部仍然有效**；N 固定基线与 Repository 定位，不删除旧步骤。
