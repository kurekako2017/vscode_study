# 启动与排错指南

这份文档用于在本地从零启动 Retail Insight AI，并在出错时快速定位原因。每一步都说明为什么执行、怎么执行、怎么判断成功、失败通常是什么原因、怎么修。

## 启动顺序

| 步骤 | 为什么执行 | 命令 | 成功判断 | 失败原因 | 解决方法 |
| --- | --- | --- | --- | --- | --- |
| 1 | 先确认本机基础环境足够支撑后续启动 | `./scripts/check_env.sh` | 终端显示检查通过 | 命令不存在、版本不满足、依赖缺失 | 先修复 Python、Node、npm 等本地环境 |
| 2 | 启动后端，提供 Swagger、SSE 和业务 API | `./scripts/start_backend.sh` | 出现 `Uvicorn running on http://127.0.0.1:8000` | 端口占用、导入失败、语法错误 | 先看后端终端日志，再修复后重试 |
| 3 | 启动前端，确认页面能访问后端 | `./scripts/start_frontend.sh` | 出现 `Local: http://127.0.0.1:5173/` | 5173 被占用、npm 依赖未装、Vite 启动失败 | 先处理前端终端日志，再重启 |
| 4 | 用 Swagger 直接验证接口是否已经注册 | 打开 `http://127.0.0.1:8000/docs` | 页面能列出接口并支持执行 | 后端没启动、地址写错、404 | 回到第 2 步确认后端是否真的启动 |
| 5 | 用 ReDoc 阅读结构化文档 | 打开 `http://127.0.0.1:8000/redoc` | 页面正常展示接口说明 | 后端没启动或网络异常 | 回到后端终端和接口日志排错 |
| 6 | 用 OpenAPI JSON 确认合同实际注册情况 | 打开 `http://127.0.0.1:8000/openapi.json` | 能看到 JSON、paths 和 schemas | 路由没注册、后端没启动 | 回到 `docs/LEARNING_API_WALKTHROUGH.md` 核对接口 |
| 7 | 用完整测试收口，确认行为稳定 | `./scripts/run_tests.sh` | Backend tests、Frontend tests、Frontend build、Python compileall 都通过 | 任一阶段失败即停止 | 先修复最早失败的阶段，再重新执行 |

## 从项目根目录执行

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai
./scripts/check_env.sh
./scripts/start_backend.sh
./scripts/start_frontend.sh
```

## 从 backend 目录直接看 uvicorn

如果你想观察 `uvicorn` 的原始输出，可以进入 `backend` 后直接执行：

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai/backend
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

这样做的原因是：有些排错问题只看脚本日志不够，需要直接看 `FastAPI` 启动过程。

## 常见问题

### 后端启动失败

- 为什么会发生：`backend` 目录不对、虚拟环境没激活、依赖没装、8000 端口被占用，或者最近改动引入了 Python 语法错误。
- 怎么执行排查：

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -c "from app.main import app; print(app.title)"
ss -ltnp | grep ':8000'
```

- 成功判断：`app.title` 能打印，且 8000 没被别的进程占用。
- 解决方法：先结束旧进程，再重新执行 `./scripts/start_backend.sh`。

### 前端启动失败

- 为什么会发生：`frontend` 依赖未安装、5173 端口被占用，或者 Node.js 版本不满足要求。
- 怎么执行排查：

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai/frontend
npm install
npm run dev -- --host 127.0.0.1
```

- 成功判断：终端出现 `Local: http://127.0.0.1:5173/`。
- 解决方法：先查端口占用，再重启前端。

### Swagger 打不开

- 为什么会发生：后端其实没有启动成功，或者访问的不是 `127.0.0.1:8000`。
- 怎么执行排查：

```bash
curl -sS http://127.0.0.1:8000/health
```

- 成功判断：返回 JSON，且 `status=ok`。
- 解决方法：如果这里都返回不了 JSON，先回到“后端启动失败”排错。

### 任务创建成功但 SSE 没有事件

- 为什么会发生：任务还没真正开始、SSE 连接断开，或者 backend 进程重启后内存任务已丢失。
- 怎么执行排查：

```bash
curl -sS -X POST http://127.0.0.1:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"question":"売上と在庫の状況を分析してください","mode":"hybrid"}'
```

拿到 `task_id` 后再检查：

```bash
curl -sS -N "http://127.0.0.1:8000/api/tasks/<task_id>/events"
```

- 成功判断：至少出现一条 `event: status`。
- 解决方法：如果后端重启过，先重新创建任务再连 SSE。

### 报告取不到

- 为什么会发生：任务还没完成、事件流提前断开，或者报告仓库中没有对应 `task_id`。
- 怎么执行排查：

```bash
curl -sS "http://127.0.0.1:8000/api/tasks/<task_id>/report"
```

- 成功判断：返回 `status=generated` 且包含 Markdown。
- 解决方法：先确认 SSE 已经出现 `done`，再取报告。

### Security read model 为空

- 为什么会发生：当前实现使用 placeholder principal 和静态目录，若返回为空通常说明后端没加载成功。
- 怎么执行排查：

```bash
curl -sS http://127.0.0.1:8000/api/v1/users/me
curl -sS http://127.0.0.1:8000/api/v1/security/roles
curl -sS http://127.0.0.1:8000/api/v1/security/permissions
curl -sS http://127.0.0.1:8000/api/v1/audit-logs
```

- 成功判断：`users/me` 返回 `system` 占位主体，`roles` 和 `permissions` 返回冻结目录，`audit-logs` 返回列表。
- 解决方法：检查 `backend/app/main.py` 和后端终端日志。

### PostgreSQL 验证被跳过

- 为什么会发生：当前环境没有 `psycopg` 或没有 Docker CLI。
- 怎么执行排查：

```bash
./scripts/verify_postgres_phase2.sh
```

- 成功判断：脚本会明确说明是通过还是跳过。
- 解决方法：如果缺少 `docker` 或 `psycopg`，这是正常边界，不要把跳过写成成功。

## 本地验证建议

1. 先跑 `./scripts/check_env.sh`。
2. 再启动后端和前端。
3. 再用 `curl` 和 Swagger 验证 `health`、`task`、`document`、`approval`、`security` 接口。
4. 最后再跑 `./scripts/run_tests.sh` 做收口检查。

## 工具职责说明

- `Swagger` 是 `FastAPI` 自动生成的 API 调试与验证工具。
- `ReDoc` 是面向阅读的 API 文档展示工具。
- `OpenAPI JSON` 是机器可读的接口定义。
- 三者不是同一个用途，但都指向同一套后端合同。
- `UI` 完成以后，`Swagger` 仍然保留，因为它最适合接口学习、验证和排错。

## 推荐启动后验证顺序

```text
Swagger
↓
几个主链路 API
↓
后台日志
↓
unittest
↓
源码阅读
```
