# 启动与排错指南

这份文档用于在 VS Code + WSL Ubuntu 中从零启动 Retail Insight AI，并在遇到问题时快速定位原因。

## 启动顺序

### 从项目根目录执行

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai
./scripts/check_env.sh
./scripts/start_backend.sh
```

如果只想检查环境，也可以只执行 `./scripts/check_env.sh`。

### 从 backend 目录执行

如果你不想用脚本，而是想直接看 uvicorn 启动过程，可以进入 `backend` 后执行：

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai/backend
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 从项目根目录执行前端

另开一个终端，回到项目根目录：

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai
./scripts/start_frontend.sh
```

浏览器打开：

```text
http://127.0.0.1:5173
```

### 三个文档入口

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

三者作用：

- Swagger 适合点接口、填输入、直接执行。
- ReDoc 适合长时间阅读接口说明。
- OpenAPI JSON 适合确认接口和 schema 真实注册情况。

## 常见问题

### 问题：后端启动失败

- 原因：`backend` 目录不对、虚拟环境没激活、依赖没装、8000 端口被占用，或者最近改动引入了 Python 语法错误。
- 解决方法：

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -c "from app.main import app; print(app.title)"
ss -ltnp | grep ':8000'
```

如果 8000 已被占用，先结束旧进程，再重新执行：

```bash
./scripts/start_backend.sh
```

### 问题：前端启动失败

- 原因：`frontend` 依赖未安装、5173 端口被占用，或者 Node.js 版本不满足要求。
- 解决方法：

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai/frontend
npm install
npm run dev -- --host 127.0.0.1
```

如果 5173 被占用，先查占用者：

```bash
ss -ltnp | grep ':5173'
```

然后结束旧进程，再重新启动。

### 问题：Swagger 打不开

- 原因：后端其实没有启动成功，或者你访问的不是 `127.0.0.1:8000`。
- 解决方法：

```bash
curl -sS http://127.0.0.1:8000/health
```

如果这里都返回不了 JSON，先回到“后端启动失败”排错。

### 问题：任务创建成功但 SSE 没有事件

- 原因：任务还没真正开始、SSE 连接断开、或者 backend 进程重启后内存任务已丢失。
- 解决方法：

```bash
curl -sS -X POST http://127.0.0.1:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"question":"売上と在庫の状況を分析してください","mode":"hybrid"}'
```

拿到 `task_id` 后再检查：

```bash
curl -sS -N "http://127.0.0.1:8000/api/tasks/<task_id>/events"
```

如果后端重启过，先重新创建任务再连 SSE。

### 问题：报告取不到

- 原因：任务还没完成、事件流提前断开、或者报告仓库中没有对应 `task_id`。
- 解决方法：

```bash
curl -sS "http://127.0.0.1:8000/api/tasks/<task_id>/report"
```

如果返回 `REPORT_NOT_FOUND`，先确认：

```bash
curl -sS -N "http://127.0.0.1:8000/api/tasks/<task_id>/events"
```

等到 `done` 事件出现后再取报告。

### 问题：Security read model 为空

- 原因：当前实现使用 placeholder principal 和静态目录，若返回为空通常说明后端没加载成功。
- 解决方法：

```bash
curl -sS http://127.0.0.1:8000/api/v1/users/me
curl -sS http://127.0.0.1:8000/api/v1/security/roles
curl -sS http://127.0.0.1:8000/api/v1/security/permissions
curl -sS http://127.0.0.1:8000/api/v1/audit-logs
```

如果这些接口报错，优先检查 `backend/app/main.py` 和后端终端日志。

### 问题：测试脚本失败

- 原因：通常是最前面的一个测试阶段失败，后续阶段不会继续跑。
- 解决方法：

```bash
./scripts/run_tests.sh
```

先看第一个失败阶段，再去对应 `backend/tests/` 或 `frontend/src/*.test.tsx` 排错，不要先猜后面的结果。

### 问题：PostgreSQL 验证被跳过

- 原因：当前环境没有 `psycopg` 或没有 Docker CLI。
- 解决方法：

```bash
./scripts/verify_postgres_phase2.sh
```

如果脚本明确提示缺少 `docker` 或 `psycopg`，这表示跳过原因是正常且可接受的，不要把它当成失败。

## 本地验证建议

1. 先跑 `./scripts/check_env.sh`。
2. 再启动后端和前端。
3. 再用 `curl` 和 Swagger 验证 `health`、`task`、`document`、`approval`、`security` 接口。
4. 最后再跑 `./scripts/run_tests.sh` 做收口检查。
