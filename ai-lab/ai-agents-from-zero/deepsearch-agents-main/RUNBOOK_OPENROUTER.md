# DeepSearch Agents OpenRouter 运行手册

这份手册只讲一条最容易跑起来的路径：

- 大模型：`OpenRouter`
- 后端：`FastAPI`
- 前端：`Vite`
- 数据库：当前工作区默认复用 `NAS MySQL`

如果你刚才没跑起来，不要一下子前后端一起开。正确顺序是：

1. 先准备 `.env`
2. 先检查环境变量
3. 先启动后端
4. 先用 `health` 接口确认后端真的活了
5. 最后再启动前端

## 0. 你现在要用哪个目录

先进入项目根目录：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main
pwd
```

你应该看到：

```text
/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main
```

后面所有 Python 命令都默认在这个目录执行。

这个仓库根目录有 `sitecustomize.py`，所以只要你在项目根目录启动 Python，它就会自动读取 `.env`，并把 `OPENROUTER_*` 映射成 OpenAI 兼容变量。

## 1. 先确认基础命令在不在

执行：

```bash
python3 --version
node --version
uv --version
pnpm --version
```

目标：

- `python3` 要是 `3.12.x`
- `node` 要能输出版本号
- `uv` 要能输出版本号
- `pnpm` 要能输出版本号

如果 `pnpm` 没装，而你只想先跑前端，也可以暂时用 `npm`，但这份项目的标准方式还是 `pnpm`。

## 2. 准备 `.env`

先复制模板：

```bash
cp .env.template .env
```

然后编辑 `.env`。至少要填这些：

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

### 你现在最少必须保证哪些值正确

如果你只是想把项目先启动起来，最低要求是：

- `OPENROUTER_BASE_URL`
- `OPENROUTER_API_KEY`
- `LLM_QWEN_MAX`
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DATABASE`

如果下面这些没填，项目也可能能启动，但部分能力会不可用：

- `TAVILY_API_KEY`
- `RAGFLOW_API_URL`
- `RAGFLOW_API_KEY`

## 3. 运行环境检查脚本

这一步一定要做。执行：

```bash
python3 scripts/check_environment.py
```

### 正常时你应该看到什么

重点看这几行是不是 `OK`：

- `OPENROUTER_BASE_URL`
- `OPENROUTER_API_KEY`
- `LLM_QWEN_MAX`
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DATABASE`
- `LLM (OpenAI/OpenRouter)`

最后一段要尽量看到：

```text
Environment variables look ready.
```

### 如果这里失败，先不要继续

最常见原因是：

1. `.env` 根本没创建
2. `.env` 不在项目根目录
3. `OPENROUTER_API_KEY` 没填
4. MySQL 配置没填完整

## 4. 安装后端依赖

推荐方式是 `uv`：

```bash
uv sync
```

如果你不用 `uv`，可以退一步用：

```bash
python3 -m pip install --target .deps -r requirements.txt
```

两种方式二选一就行，不需要都装。

### 推荐你怎么选

- 如果你已经有 `uv`：用 `uv sync`
- 如果你只是想最快验证：用 `pip install --target .deps`

## 5. 启动后端

### 方案 A：你用了 `uv sync`

执行：

```bash
uv run uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload
```

### 方案 B：你用了 `.deps`

执行：

```bash
PYTHONPATH=.deps python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000
```

### 后端启动成功时你应该看到

终端里通常会出现类似：

```text
Uvicorn running on http://0.0.0.0:8000
Application startup complete.
```

这一步终端不要关，保持它一直运行。

## 6. 单独验证后端是不是活着

新开一个终端，再次进入项目目录：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main
```

然后执行：

```bash
curl -s http://127.0.0.1:8000/api/health
```

### 你重点看什么

返回 JSON 里重点看：

- `backend` 应该是 `alive`
- `llm.configured` 应该是 `true`
- `llm.source` 应该是 `openrouter`
- `llm.model` 应该有值
- `mysql.configured` 应该是 `true`

如果你看到了这些，说明后端已经真的能给前端用了。

### 如果这里失败

按这个顺序排：

1. 后端终端是不是已经退出了
2. 端口 `8000` 是不是没起来
3. 你是不是用了错误的启动命令
4. 你是不是没在项目根目录启动 Python

## 7. 启动前端

前端目录在这里：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/frontend
```

推荐：

```bash
pnpm install
pnpm dev
```

如果你暂时没有 `pnpm`，可以用：

```bash
npm install
npm run dev
```

### 前端启动成功时你应该看到

类似：

```text
Local:   http://localhost:5173/
```

浏览器打开：

```text
http://localhost:5173
```

这个前端默认会把 `/api` 和 `/ws` 代理到 `http://localhost:8000`，配置在 `frontend/vite.config.ts`，所以通常不需要额外改前端环境变量。

## 8. 先跑一个最小联通测试

打开前端后，先不要上来就测最复杂的多来源任务。先测一个简单问题，比如：

```text
帮我简单介绍一下这个系统能做什么。
```

如果只是想测数据库链路，可以试：

```text
请直接查询 drugs 表中 therapeutic_area 为 心血管 的药品，并用 Markdown 表格输出名称、品牌、规格、厂家和简介，直接给出结果，不要向我提问。
```

## 9. 最短可复制版

如果你想按最短顺序重跑一遍，直接照抄：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main
cp .env.template .env
python3 scripts/check_environment.py
uv sync
uv run uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload
```

新开第二个终端：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main
curl -s http://127.0.0.1:8000/api/health
```

新开第三个终端：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/frontend
pnpm install
pnpm dev
```

## 10. 如果你刚才“没跑起来”，最可能卡在哪

### 情况 1：`check_environment.py` 就失败

说明 `.env` 没配好。

先检查：

```bash
ls -la .env
python3 scripts/check_environment.py
```

### 情况 2：后端启动命令直接报错

说明多半是依赖没装好。

重做：

```bash
uv sync
```

如果你不用 `uv`：

```bash
python3 -m pip install --target .deps -r requirements.txt
PYTHONPATH=.deps python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000
```

### 情况 3：后端能启动，但 `health` 里 `llm` 或 `mysql` 不对

重点检查 `.env`：

- `OPENROUTER_API_KEY`
- `OPENROUTER_BASE_URL`
- `LLM_QWEN_MAX`
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DATABASE`

### 情况 4：前端能开，但页面调用后端失败

先别看前端代码，先看后端接口：

```bash
curl -s http://127.0.0.1:8000/api/health
```

只有 `health` 正常了，前端代理才有意义。

## 11. 示例脚本怎么跑

这些示例都要在项目根目录执行：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main
```

然后例如：

```bash
uv run python examples/1-deep-agent-quickstart-search.py
uv run python examples/2-deep-agent-streaming-chunks.py
uv run python examples/3-dict-subagents-routing.py
```

如果你没有 `uv`，也可以：

```bash
PYTHONPATH=.deps python3 examples/1-deep-agent-quickstart-search.py
```

注意：

- `1` 和 `2` 需要 `TAVILY_API_KEY`
- 大多数示例依赖 `OPENROUTER_API_KEY`
- 涉及数据库的示例还依赖 `MYSQL_*`

## 12. 你现在最推荐的实际运行顺序

按这个顺序最稳：

1. `cd deepsearch-agents-main`
2. `cp .env.template .env`
3. 把 `OPENROUTER_API_KEY` 和 `MYSQL_*` 填好
4. `python3 scripts/check_environment.py`
5. `uv sync`
6. `uv run uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload`
7. 新终端执行 `curl -s http://127.0.0.1:8000/api/health`
8. 确认 `backend=alive`、`llm.source=openrouter`、`mysql.configured=true`
9. `cd frontend`
10. `pnpm install`
11. `pnpm dev`
12. 浏览器打开 `http://localhost:5173`

如果你愿意，我下一步可以继续把这份手册再补成“带实际截图检查点”的版本，或者我直接帮你按这份顺序把这个项目在当前工作区跑起来并定位卡住点。
