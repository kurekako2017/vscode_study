# RUNBOOK_LOCAL

这份手册用于在 VS Code + WSL Ubuntu 中，从零启动 Retail Insight AI，并亲自验证 Backend、Frontend、SSE 和 Report 全流程。所有命令默认在 WSL Ubuntu 终端执行。

## 1. 前提条件

需要以下工具：

- WSL Ubuntu。
- Python 3.11 以上，推荐 Python 3.12。
- Node.js 20.19 以上或 22.12 以上，推荐 Node.js 22。
- npm 10 以上。
- Docker 可选；不安装 Docker 也可以分别启动 Backend 和 Frontend。

确认版本：

```bash
python3 --version
python3 -m pip --version
node -v
npm -v
docker --version
```

如果最后一条显示 `docker: command not found`，只表示不能执行 Docker Compose，不影响本手册的普通本地启动方式。

也可以进入项目根目录后执行：

```bash
./scripts/check_env.sh
```

预期看到 Python、pip、Node、npm 的版本和“必需工具检查通过”。Docker 不存在时脚本只提示，不会失败。

## 2. 项目目录确认

从 `ai-learn` 工作区进入项目：

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai
pwd
```

预期 `pwd` 结尾是：

```text
/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai
```

如果你的仓库不在这个路径，先在 VS Code Explorer 中找到 `retail-insight-ai`，右键目录选择“Open in Integrated Terminal”，然后执行：

```bash
pwd
ls
```

`ls` 应能看到 `backend`、`frontend`、`scripts`、`README.md` 和 `RUNBOOK_LOCAL.md`。

## 3. Backend 启动步骤

在第一个 WSL 终端执行：

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

说明：

- `python3 -m venv .venv` 在 `backend/.venv` 创建隔离环境。
- `source .venv/bin/activate` 后，终端提示符通常会出现 `(.venv)`。
- `cp ../.env.example ../.env` 创建项目根目录配置；如果 `.env` 已存在，可以跳过，避免覆盖自己的配置。
- Backend 会读取项目根 `.env`，`RESEARCH_PROVIDER` 和 `DATA_PROVIDER` 默认都是 `static`。

出现以下信息表示启动成功：

```text
Uvicorn running on http://127.0.0.1:8000
Application startup complete
```

同时会看到 JSON 结构化日志，其中包含 `application_started` 事件。

另开终端确认：

```bash
curl -sS http://127.0.0.1:8000/health
```

返回包含 `"status":"ok"` 表示 Backend 可访问。

如果 8000 端口被占用，先查占用者：

```bash
ss -ltnp | grep ':8000'
```

确认 PID 后停止旧进程：

```bash
kill <PID>
```

再重新执行 Uvicorn 命令。Frontend 的 Vite 代理固定连接 8000，因此初学阶段建议释放 8000，而不是只把 Backend 改到其它端口。

停止 Backend：回到运行 Uvicorn 的终端，按 `Ctrl+C`。

## 4. Frontend 启动步骤

保持 Backend 终端运行，另开第二个 WSL 终端：

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai
cd frontend
npm install
npm run dev -- --host 127.0.0.1
```

Vite 默认端口是 5173。看到类似下面的信息表示成功：

```text
Local: http://127.0.0.1:5173/
```

在 Windows 浏览器打开：

```text
http://127.0.0.1:5173
```

也可以打开 `http://localhost:5173`。两种来源都在本地 CORS 白名单中。

如果 5173 被占用，Vite 可能显示 5174 等新端口。优先停止旧 Vite：

```bash
ss -ltnp | grep ':5173'
kill <PID>
```

然后重新启动，确认终端显示 5173。停止 Frontend：在 Vite 终端按 `Ctrl+C`。

## 5. Backend API 自测

以下命令在第三个终端执行。先确认 Backend 仍在 8000 端口运行。

### 5.1 Health check

命令：

```bash
curl -sS http://127.0.0.1:8000/health
```

预期结果：HTTP 200，并包含：

```json
{
  "status": "ok",
  "service": "retail-insight-ai",
  "provider": "static",
  "request_id": "每次请求生成的 ID"
}
```

失败时先看 Backend 终端是否仍有 Uvicorn 进程和异常日志。

### 5.2 创建任务

当前真实 Request Schema 是 `question` 和 `mode`。项目不接受 `store_id`、`period`、`analysis_type`。

命令：

```bash
curl -sS -X POST http://127.0.0.1:8000/api/tasks \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: local-manual-test" \
  -d '{"question":"売上と在庫の状況を分析してください","mode":"hybrid"}'
```

`mode` 可选：

- `hybrid`：KPI + Research。
- `kpi`：只执行 KPI。
- `research`：只执行 Research。

预期结果：HTTP 202 和成功 envelope：

```json
{
  "success": true,
  "request_id": "local-manual-test",
  "data": {
    "task_id": "这里是 UUID",
    "status": "queued"
  },
  "error": null
}
```

手工复制 `data.task_id` 中的 UUID，后面用 `<TASK_ID>` 表示。

也可以用命令自动提取：

```bash
CREATE_RESPONSE=$(curl -sS -X POST http://127.0.0.1:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"question":"売上と在庫の状況を分析してください","mode":"hybrid"}')

echo "$CREATE_RESPONSE"

TASK_ID=$(printf '%s' "$CREATE_RESPONSE" | python3 -c \
  'import json,sys; print(json.load(sys.stdin)["data"]["task_id"])')

echo "$TASK_ID"
```

失败时在 Backend 日志中查同一个 `request_id`。422 表示请求字段不符合 Schema。

### 5.3 查询任务状态

命令：

```bash
curl -sS "http://127.0.0.1:8000/api/tasks/${TASK_ID}"
```

预期 `data.status` 最终变成 `completed`。如果仍是 `queued` 或 `running`，等待一秒再执行一次。

失败时：

- `TASK_NOT_FOUND`：确认 task_id 是否复制完整，以及 Backend 是否刚刚重启。
- `failed`：查看 `data.error`，并按 task_id 检查 Backend 日志。

### 5.4 读取报告

任务 completed 后执行：

```bash
curl -sS "http://127.0.0.1:8000/api/tasks/${TASK_ID}/report"
```

预期 `success` 为 `true`，`data.markdown` 包含：

```text
# Retail Insight AI 経営分析レポート
## KPI サマリー
## Research サマリー
```

如果返回 `REPORT_NOT_FOUND`，通常是任务尚未完成；先重新查询状态。

### 5.5 SSE 测试

```bash
curl -N "http://127.0.0.1:8000/api/tasks/${TASK_ID}/events"
```

`-N` 禁止 curl 缓冲输出。预期看到多组 `id:`、`event:`、`data:`，最后是 `event: done`。

任何 API 命令失败时，都先看 Backend 终端最后一条带相同 `request_id` 或 `task_id` 的日志。

## 6. Frontend 自测

1. 确认 Backend 和 Frontend 两个终端都在运行。
2. 浏览器打开 `http://127.0.0.1:5173`。
3. 在“確認したい経営課題”输入：`売上と在庫の状況を分析してください`。
4. 选择 `KPI + Research`。
5. 点击“分析を開始”。
6. 在右侧观察 queued、running、Route、KPI、Research、Report 和 completed 进度。
7. 在下方确认出现 KPI 与 Research 报告。

故意验证错误显示：

- 清空问题时，提交按钮会禁用，这是前端第一层校验。
- 停止 Backend 后再提交，页面应显示 `[TASK_CREATE_ERROR]`。
- 要验证业务 error，停止 Backend，进入 `backend` 后用下面命令重新启动：

```bash
STATIC_RESEARCH_FAIL=true .venv/bin/python -m uvicorn app.main:app \
  --host 127.0.0.1 --port 8000
```

然后在页面选择 Research 或 Hybrid 并提交，应显示：

```text
[RESEARCH_PROVIDER_ERROR] Research provider failed
```

验证后按 `Ctrl+C`，再用普通启动命令恢复。

## 7. SSE 自测

SSE（Server-Sent Events）是服务器通过一个持续 HTTP 连接，按发生顺序向浏览器推送事件的协议。本项目用它展示 Workflow 进度，客户端不需要反复轮询每个 Node。

创建任务并取得 task_id 后执行：

```bash
curl -N "http://127.0.0.1:8000/api/tasks/${TASK_ID}/events"
```

正常任务会看到：

```text
event: status
data: {..."status":"running"...}

event: done
data: {..."status":"completed"...}
```

- `status`：queued、running 或 Node 进度。
- `done`：任务成功完成，可以读取 Report。
- `error`：任务失败，data 中包含 `error_code`、`message`、`request_id` 和 `task_id`。
- error 是终态；发送 error 后不会再发送 done。

即使任务已经快速完成，当前 InMemoryEventRepository 也会从 sequence 1 重放本进程中保存的事件。Backend 重启后事件会丢失。

## 8. 日志查看方法

Backend 日志直接输出在运行 Uvicorn 的终端，每一行是 JSON。关键字段：

| 字段 | 含义 |
| --- | --- |
| `request_id` | 一次 HTTP 请求的关联 ID，也会返回在响应中 |
| `task_id` | 一次分析任务的 ID |
| `event` | `task_queued`、`kpi_completed`、`task_failed` 等事件名 |
| `error_code` | 失败分类；成功时通常为 null |
| `duration_ms` | 当前步骤耗时 |

需要保存日志时可以这样启动：

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000 2>&1 \
  | tee /tmp/retail-insight-ai.log
```

根据 task_id 查问题：

```bash
grep '"task_id":"<TASK_ID>"' /tmp/retail-insight-ai.log
```

排查顺序：先找 `task_failed` 的 `error_code`，再向上找同一 task_id 最后一个 completed Node。日志不会记录完整问题正文、API Key、会员资料或内部资料正文。

## 9. 测试命令

Backend：

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai/backend
source .venv/bin/activate
python -m unittest discover tests
```

Frontend：

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai/frontend
npm test
npm run build
```

Python compile：

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai/backend
python -m compileall app
```

也可以从项目根目录一次执行全部检查：

```bash
./scripts/run_tests.sh
```

预期最后看到“全部本地测试与编译检查通过”。

## 10. 常见错误排查

### 10.1 ModuleNotFoundError

原因：不在 `backend` 目录启动、虚拟环境未激活，或依赖未安装。

解决：

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai/backend
source .venv/bin/activate
python -m pip install -r requirements.txt
python -c "import fastapi, langgraph, pydantic_settings; print('imports ok')"
```

确认修复：最后输出 `imports ok`，再启动 Uvicorn。

### 10.2 pip install 失败

原因：WSL 网络、代理、证书或 PyPI 暂时不可用。

解决：

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

如果仍失败，先确认网络：

```bash
curl -I https://pypi.org
```

确认修复：`python -m pip check` 输出 `No broken requirements found`。

### 10.3 uvicorn command not found

原因：没有激活虚拟环境，或直接调用了不存在于 PATH 的命令。

解决：

```bash
cd backend
source .venv/bin/activate
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

确认修复：终端显示 `Uvicorn running on http://127.0.0.1:8000`。

### 10.4 port 8000 already in use

原因：旧 Backend 或其它程序仍占用端口。

解决：

```bash
ss -ltnp | grep ':8000'
kill <PID>
```

确认修复：

```bash
curl -sS http://127.0.0.1:8000/health
```

返回当前服务的 `status: ok`。

### 10.5 Frontend npm install 失败

原因：Node 版本过旧、npm Registry 网络问题或本地缓存异常。

解决：

```bash
node -v
npm -v
npm cache verify
npm install
```

Node 应满足本手册第一节版本要求。确认修复：`npm test` 可以启动 Vitest。

### 10.6 Vite 页面打不开

原因：Vite 未运行、打开了错误端口，或进程已经退出。

解决：

```bash
cd frontend
npm run dev -- --host 127.0.0.1
```

确认终端实际显示的 Local URL，并执行：

```bash
curl -I http://127.0.0.1:5173
```

返回 HTTP 200 后再刷新浏览器。

### 10.7 CORS error

原因：直接从未加入白名单的浏览器 Origin 调用 Backend，或修改 `.env` 后没有重启 Backend。

解决：确认项目根 `.env` 包含：

```text
CORS_ORIGINS=["http://127.0.0.1:5173","http://localhost:5173"]
```

保存后重启 Backend。确认修复：从 `http://127.0.0.1:5173` 或 `http://localhost:5173` 提交任务，浏览器 Console 不再出现 CORS 错误。不要把生产配置改成允许 `*`。

### 10.8 task_id 查不到

原因：复制错误、请求到了另一个 Backend，或 Backend 重启导致 InMemory 数据丢失。

解决：重新创建任务并复制最新 `data.task_id`。

确认修复：

```bash
curl -sS "http://127.0.0.1:8000/api/tasks/${TASK_ID}"
```

返回 `success: true`。

### 10.9 report not found

原因：任务尚未 completed，或 Backend 重启后内存报告丢失。

解决：先查询任务状态；如果任务不存在则重新创建。如果状态仍在运行，等待后重试。

确认修复：Report API 返回 `success: true`，并包含 `data.markdown`。

### 10.10 SSE 没有输出

原因：curl 没有使用 `-N`、task_id 错误、Backend 不在 8000，或任务属于重启前的进程。

解决：

```bash
curl -sS http://127.0.0.1:8000/health
curl -N "http://127.0.0.1:8000/api/tasks/${TASK_ID}/events"
```

确认修复：至少看到 `event: status`，最终看到 done 或 error。

### 10.11 Docker CLI not found

原因：WSL 中没有 Docker CLI，或 Docker Desktop 未启用 WSL Integration。

解决选择：

- 本项目不要求 Docker，直接使用本手册第 3、4 节启动。
- 如果需要 Docker，在 Windows Docker Desktop 中启用当前 Ubuntu 的 WSL Integration，然后重新打开 WSL 终端。

确认修复：

```bash
docker --version
docker compose version
```

## 11. 当前实现边界

- API、TaskService、LangGraph Workflow、SSE、Report Generator 和 Frontend 是真实实现。
- Research Provider 当前是 `StaticResearchProvider`，不会调用真实 LLM 或搜索服务。
- Repository 当前是 `InMemoryRepository` 系列，只在当前 Backend 进程中保存数据。
- 不需要 OpenAI Key，也不需要任何真实模型 Key。
- 不需要 Docker，也能分别启动 Backend 和 Frontend。
- Backend 重启后，已有 task_id、SSE 事件和 Report 会丢失。

## 12. 一键启动脚本说明

首次执行：

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai
chmod +x scripts/*.sh
./scripts/check_env.sh
```

第一个终端启动 Backend：

```bash
./scripts/start_backend.sh
```

第二个终端启动 Frontend：

```bash
./scripts/start_frontend.sh
```

浏览器打开 `http://127.0.0.1:5173`。

执行全部测试：

```bash
./scripts/run_tests.sh
```

脚本可以从项目根目录直接执行，也可以从其它目录用绝对路径执行；脚本会自行定位 `retail-insight-ai` 根目录。

<!-- DOC-SYNC:START group=study-and-runbook -->
## 文档同步块

- group: `study-and-runbook`
- file: `retail-insight-ai/RUNBOOK_LOCAL.md`
- self_sha256: `82e649ea6d4a1124aef7bac0e5296b5bbd4077586f02199892583fefaf930f1a`
- peers:
- `retail-insight-ai/CODE_STUDY_GUIDE.md` | sha256=7835d7b286bdaad961b008b3623bf07ff31edf644e60239270d09e108eded449 | # CODE STUDY GUIDE / 这份指南面向第一次阅读 React、FastAPI 和 LangGraph 项目的学习者。建议先把 Backend 和 Frontend 都运行起来，再按本文顺序阅读；每读到一个步骤，就在页面或日志中观察它的实际效果。 / > 路径说明：下文路径都相对于 `retail-insight-ai/`。需求中提到的 `api/routes/tasks.py` 在本项目中的实际路径是 `backend/
- `retail-insight-ai/VERIFY_CHECKLIST.md` | sha256=a102715dbf95744db73011bb1df9cd7999da3fc9d576d4677eb230a34d77b925 | # VERIFY CHECKLIST / 所有命令默认先进入项目根目录： / ```bash / cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai
- `retail-insight-ai/STUDY_PLAN_DAY1_DAY3.md` | sha256=23659aa081e315f7a7cf87c0e3266ad81620d0b0577954f4138c7a1280b6f7c5 | # Retail Insight AI 学习计划（Day1～Day3） / 这是一份面向初学者的“边运行、边阅读、边验证”学习计划。所有路径都相对于 `retail-insight-ai/` 项目根目录；命令均可直接复制到 WSL Ubuntu 的 Bash 终端执行。 / ## 三天学习目标 / 通过三天时间，完成以下目标：
- `ai-agent-retail-handbook-v3/01_日本AI项目实战.md` | sha256=aa0cf1068c64dbdeedf2f1f5e38d235fab7d19a23aa2ad23ceee7645ac7ebac1 | # 01_日本AI项目实战 / ## 目录 / - [第一章 项目概述](#第一章-项目概述) / - [第二章 行业背景](#第二章-行业背景)
- `ai-agent-retail-handbook-v3/04_日本现场开发.md` | sha256=bca69b09dcf09db6f0869f4af8121a3d7f4e280757c8e377cd761370c68295e5 | # 04_日本现场开发 / ## 第一章 日本现场开发总流程 / Retail Insight AI 按日本现场流程推进：需求整理、基本設計、詳細設計、API 設計、開発、単体試験、結合試験、レビュー、部署、保守改修。 / 【TL Review】
- `ai-agent-retail-handbook-v3/05_TL代码审查.md` | sha256=797c312f4566abe80afb5f87dbbf97b22d983195cb9610de8de81f47af01c9c3 | # 05_TL代码审查 / ## 第一章 Review 总原则 / TL Review 的目标是确认 Retail Insight AI 能支撑日本小売業客户的经营分析、运用监视、障害対応和保守改修。 / 【TL Review】
- `ai-agent-retail-handbook-v3/06_学习路线.md` | sha256=1b39176bff4feb5bcde639affcec4036334622aca73dac53c321b649d8c11e3f | # 06_学习路线 / ## 第一章 成长目标 / 目标是能够在日本 AI Agent 现场说明 Retail Insight AI 的业务背景、系统架构、担当范围、设计决策、Review 观点和运用扩展。 / 【TL Review】
- `ai-agent-retail-handbook-v3/11_Project_Structure.md` | sha256=a40c03fd0eadeb68466c3a44a53ddf58769d104af40d37f6b658135157ef09bb | # 11_Project_Structure / # 目录 / - [1. 设计目标](#1-设计目标) / - [2. 顶层目录](#2-顶层目录)

说明：
- 这个块由 `scripts/sync_retail_handbook_docs.py` 自动维护。
- 只同步这个块，不覆盖各自正文。
- 任一组内文档正文变化时，整组文档的同步块都会一起刷新。
<!-- DOC-SYNC:END group=study-and-runbook -->
