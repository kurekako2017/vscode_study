# DeepSearch Agents OpenRouter 运行手册

这份手册只保留一条可复制的主链路：

- 大模型：`OPENROUTER_API_KEY`
- 业务库：NAS 上的 MySQL
- 前端：Vite
- 后端：FastAPI

如果你想直接跑起来，就按下面顺序执行。

## 1. 进入项目

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main
```

这个仓库根目录下带了 `sitecustomize.py`，所以只要你在项目根目录启动 Python，它就会自动读取 `.env` 并把 `OPENROUTER_*` 映射成 OpenAI 兼容环境变量。

## 2. 准备 `.env`

```bash
cp .env.template .env
```

把 `.env` 改成下面这样：

```bash
# OpenRouter
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_API_KEY=你的_openrouter_api_key
LLM_QWEN_MAX=openai/gpt-4o-mini
LLM_MAX_COMPLETION_TOKENS=1024

# Tavily
TAVILY_API_KEY=你的_tavily_api_key

# RAGFlow
RAGFLOW_API_URL=http://your-ragflow-host
RAGFLOW_API_KEY=your_ragflow_api_key

# NAS MySQL
MYSQL_HOST=192.168.10.2
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=123456
MYSQL_DATABASE=ecommjava
MYSQL_CHARSET=utf8mb4
MYSQL_COLLATION=utf8mb4_unicode_ci
MYSQL_SQL_MODE=TRADITIONAL
```

## 3. 检查环境

```bash
python3 scripts/check_environment.py
```

你要重点看到：

- `OPENROUTER_BASE_URL`
- `OPENROUTER_API_KEY`
- `LLM_QWEN_MAX`
- `MYSQL_*`

## 4. 安装后端依赖

如果你想直接用当前系统 Python：

```bash
python3 -m pip install --target .deps -r requirements.txt
```

如果你已经装了 `uv`，也可以直接：

```bash
uv sync
```

## 5. 启动后端

```bash
PYTHONPATH=.deps python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000
```

## 6. 验证后端

另开一个终端，执行：

```bash
curl -s http://127.0.0.1:8000/api/health
```

健康检查里你应当能看到：

- `backend: alive`
- `llm.source: openrouter`
- `mysql.configured: true`

## 7. 启动前端

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/frontend
npm install
npm run dev
```

如果你只想先确认前端能构建成功：

```bash
npm run build
```

打开：

```text
http://localhost:5173
```

## 8. 跑一个最小任务

你可以直接在前端输入下面这句：

```text
请直接查询 drugs 表中 therapeutic_area 为 心血管 的药品，并用 Markdown 表格输出名称、品牌、规格、厂家和简介，直接给出结果，不要向我提问。
```

## 9. `examples/` 目录入口

这些示例都可以在项目根目录直接执行，`sitecustomize.py` 会自动读取 `.env` 并映射 OpenRouter 环境。

```bash
python3 examples/1-deep-agent-quickstart-search.py
python3 examples/2-deep-agent-streaming-chunks.py
python3 examples/3-dict-subagents-routing.py
python3 examples/4-async-subagents-streaming.py
python3 examples/5-subagent-nesting-limits.py
python3 examples/6-langgraph-subagent-wrapper.py
python3 examples/7-langchain-agent-subagent-wrapper.py
python3 examples/8-human-approval-interrupt-resume.py
python3 examples/9-human-edit-tool-args-resume.py
python3 examples/10-filesystem-backend-memory.py
python3 examples/11-store-backend-cross-session-memory.py
python3 examples/12-composite-backend-routing.py
python3 examples/13-model-call-limit-middleware.py
python3 examples/14-custom-tool-call-middleware.py
python3 examples/15-skills-from-filesystem.py
```

注意：

- `1` 和 `2` 需要 `TAVILY_API_KEY`
- 其余大多数示例主要依赖 `OPENROUTER_API_KEY` 和 `LLM_QWEN_MAX`
- `15` 只依赖本地 `skills/` 目录，不依赖联网搜索

## 10. 常用排错顺序

1. 先看 `python3 scripts/check_environment.py` 的输出。
2. 再看 `curl http://127.0.0.1:8000/api/health`。
3. 再看后端终端日志。
4. 再看前端控制台和 Network 面板。
5. 最后再查 MySQL 连接是否通。

## 11. 可选：本地 MySQL

如果你暂时不想连 NAS MySQL，也可以直接起仓库自带的教学库：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main
docker compose -f docker/docker-compose.yaml up -d
```

如果数据需要初始化，按 `docker/mysql/mysql.sql` 的说明导入即可。

## 12. 一次性复制版

如果你想最省事，可以按这个顺序直接粘贴执行：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main
cp .env.template .env
python3 scripts/check_environment.py
python3 -m pip install --target .deps -r requirements.txt
PYTHONPATH=.deps python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/frontend
npm install
npm run dev
```
