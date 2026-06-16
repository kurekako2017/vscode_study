# DeepSearch Agents 工作区启动指南

这是一份合并后的主运行手册，覆盖原来的 `workspace-run-guide.md` 和 `RUNBOOK_OPENROUTER.md`。

只保留四类信息：

1. 从零启动到前端页面能打开
2. 怎么做最小验证
3. 哪些步骤适合截屏留证
4. 当前工作区里哪些功能和环境暂时不能用

## 快速链接

- [故障排查清单](#故障排查清单)
- [2.4 启动后端](#24-启动后端)
- [端口被占用时的排查顺序](#端口被占用时的排查顺序)
- [2.5 验证后端](#25-验证后端)
- [2.6 启动前端](#26-启动前端)
- [3. 建议截屏步骤](#3-建议截屏步骤)
- [4. 最小验证](#4-最小验证)

## 1. 先看结论

当前仓库的主链路是：

- 后端：`FastAPI`
- 前端：`Vite`
- 模型：`OpenRouter`，OpenRouter 402 时可按配置自动兜底到 `NVIDIA`
- 数据库：`NAS MySQL`
- 私有知识库：默认使用仓库内 `docs/knowledge_base/` 的本地向量检索

当前工作区已经具备的基础条件：

- `python3` 可用
- `node` 可用
- Python 依赖可导入
- 前端依赖可构建

当前工作区缺少的命令：

- `uv`
- `docker`
- `pnpm`

所以这份文档按“能直接跑起来”的方式写，不再依赖这些缺失命令。

仓库根目录里的 `sitecustomize.py` 会在你从项目根目录启动 Python 时自动读取 `.env`，并把 `OPENROUTER_*` 映射成 OpenAI 兼容变量。

### 建议截屏的位置

- 终端窗口：`python3 scripts/check_environment.py`
- 终端窗口：后端启动日志
- 浏览器窗口：`http://127.0.0.1:8000/api/health`
- 终端窗口：前端启动日志
- 浏览器窗口：终端里打印的 `Local:` 地址，常见是 `http://localhost:5173`，端口被占用时可能是 `http://localhost:5174`
- 文件管理器：`app/output/session_{thread_id}/`
- 浏览器前端：任务执行过程、事件流、结果区域

仓库里已经有可参考的现成示意图，放在 `docs/images/`：

- `docs/images/deepsearch-agent-home.jpg`
- `docs/images/deepsearch-database-report-result.jpg`
- `docs/images/deepsearch-network-search-result.jpg`
- `docs/images/deepsearch-system-architecture.svg`

### 建议编号

1. `.env` 关键配置
2. 环境检查输出
3. 后端启动成功
4. `/api/health` 返回
5. 前端启动成功
6. 前端首页
7. 数据库任务执行过程
8. 结果文件目录

## 2. 最短启动顺序

### 2.1 进入仓库根目录

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main
```

### 2.2 准备 `.env`

仓库根目录要有 `.env`。最直接的方式是复制示例文件：

```bash
cp .env.example .env
```

最少要确认这些值存在：

```env
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_API_KEY=你的_openrouter_api_key
LLM_QWEN_MAX=openai/gpt-4o-mini
LLM_MAX_COMPLETION_TOKENS=1024

MYSQL_HOST=192.168.10.2
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=123456
MYSQL_DATABASE=ecommjava
MYSQL_CHARSET=utf8mb4
MYSQL_COLLATION=utf8mb4_unicode_ci
MYSQL_SQL_MODE=TRADITIONAL
```

可选项，不影响页面打开，但相关功能会不可用：

```env
TAVILY_API_KEY=你的_tavily_api_key
```

本地知识库的推荐策略是：

1. 直接使用仓库内的 `docs/knowledge_base/` 目录作为默认知识库
2. 后续有新资料时，把 PDF、Word、Markdown 或文本文件放进去即可
3. 如果资料更新，重启后端即可重新构建本地检索结果

## 故障排查清单

后端启动失败时，优先按下面顺序处理：

1. 先看是不是刚刚那个终端还在跑后端，直接按 `Ctrl + C`
2. 查 `8000` 端口是否被占用：

```bash
lsof -iTCP:8000 -sTCP:LISTEN -n -P
```

3. 如果查到了 `PID`，先确认它是不是当前项目的后端：

```bash
ps -fp <PID>
```

4. 如果确认是后端进程，先正常结束：

```bash
kill <PID>
```

5. 如果还在监听，再强制结束：

```bash
kill -9 <PID>
```

6. 如果还有残留，按命令名批量结束：

```bash
pkill -f "python3 -m uvicorn app.api.server:app"
```

7. 如果还是不行，直接按端口杀掉：

```bash
fuser -k 8000/tcp
```

8. 最后确认端口空出来，再重新启动：

```bash
python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload
```

### 2.3 检查环境

```bash
python3 scripts/check_environment.py
```

这一步的截屏建议保留，因为它能直接说明当前机器能不能启动。

### 2.4 启动后端

当前工作区没有 `uv`，所以不要走 `uv sync` 那条标准路径。直接用现成 Python 环境启动：

```bash
python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload
```

#### 端口被占用时的排查顺序

如果你看到 `ERROR: [Errno 98] Address already in use`，直接去上面的 `故障排查清单`。

### 2.5 验证后端

新开一个终端执行：

```bash
curl -s http://127.0.0.1:8000/api/health
```

### 2.6 启动前端

当前工作区没有 `pnpm`，所以前端用 `npm`：

```bash
cd frontend
npm install
npm run dev
```

如果 `5173` 已被占用，Vite 会自动切换到下一个可用端口，例如 `5174`。
以终端里打印的 `Local:` 地址为准，不要只盯着默认端口。

### 2.7 打开页面

浏览器访问终端里打印的 `Local:` 地址。

```text
http://localhost:5173
```

前端已经配置好代理：

- `/api -> http://localhost:8000`
- `/ws -> ws://localhost:8000`

如果 `5173` 被占用，直接打开 `Local:` 后面的地址，比如 `http://localhost:5174`。

## 2.8 最短可执行版

如果你不想看前面的解释，按这个顺序执行：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main
python3 scripts/check_environment.py
python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload
```

另开一个终端：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/frontend
npm install
npm run dev
```

最后打开前端终端里打印的 `Local:` 地址。

## 3. 建议截屏步骤

### 建议截屏 1：`.env` 关键配置

建议截屏位置：

- 根目录 `.env` 文件
- 只截 `OPENROUTER_*` 和 `MYSQL_*` 关键片段

目的：

- 证明你已经把启动所需的核心变量配好

### 建议截屏 2：环境检查输出

建议截屏位置：

- 终端里 `python3 scripts/check_environment.py` 的输出

目的：

- 证明命令和变量状态已被检查

### 建议截屏 3：后端启动成功

建议截屏位置：

- 后端终端
- 出现 `Application startup complete.` 的位置

目的：

- 证明 FastAPI 已经起来

### 建议截屏 4：`/api/health` 返回

建议截屏位置：

- 浏览器打开 `http://127.0.0.1:8000/api/health`
- 或者终端 `curl` 输出

目的：

- 证明后端接口可访问

### 建议截屏 5：前端启动成功

建议截屏位置：

- `npm run dev` 的终端
- 出现 `Local: http://localhost:5173/` 或 `Local: http://localhost:5174/` 的位置

目的：

- 证明前端开发服务器已起来

### 建议截屏 6：前端首页

建议截屏位置：

- 浏览器打开终端里打印的 `Local:` 地址

目的：

- 证明前端页面能打开

### 建议截屏 7：数据库任务执行过程

建议截屏位置：

- 前端里的输入框和事件流
- 或终端里运行数据库任务的输出

目的：

- 证明主链路能调用数据库能力

### 建议截屏 8：结果文件目录

建议截屏位置：

- 文件管理器中的 `app/output/session_{thread_id}/`

目的：

- 证明任务产物已经写到输出目录

## 4. 最小验证

这部分按“先验证能连上，再验证能查到，再验证能产出结果”的顺序来。

### 4.1 只验证后端是否活着

先在终端执行：

```bash
curl -s http://127.0.0.1:8000/api/health
```

预期输出：

- 返回一段 JSON
- 里面有 `backend: alive`
- `llm`、`mysql`、`services` 会显示当前配置状态

如果这里报 `Couldn't connect to server`，说明不是“答案没回来”，而是后端进程根本没启动。
这时先别看 WebSocket，也别看任务接口，先把 `python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload` 跑起来。
在当前这个工作区里，如果你只是看到终端启动成功但浏览器或 curl 访问不到，优先检查是不是后端实际没在运行，或者端口被别的进程占用了。

### 4.2 验证前端能否打开并读取健康状态

输入：

- 浏览器打开 `http://localhost:5173`

预期输出：

- 页面可以正常加载
- 左侧健康区能显示 `Backend`
- `LLM` 能显示 provider / model 或“未配置”
- `MySQL` 能显示 host / port 或“未配置”

如果这里失败，通常是前端代理或前端构建问题。
如果这里能打开但显示 `OFF`，一般表示对应后端能力没有配置，不代表 WebSocket 单独可用。

### 4.3 验证 NAS MySQL 是否真的连通

输入：

```text
先列出当前数据库有哪些表，再挑一张表预览前 5 行数据。
```

预期输出：

- 能返回一个或多个表名
- 能看到某张表的字段或样例数据
- 如果返回“没有可用的表”，说明数据库连接成功，但当前库里可能没有业务表或你连到的是空库

这一步验证的是“数据库连接”，不是“业务数据一定存在”。

### 4.4 验证业务查询能不能查到数据

输入：

```text
请基于你刚才看到的真实表名，查询一条最容易命中的业务数据，并用 Markdown 表格输出。若没有数据，请明确告诉我当前表是空的还是表名不匹配。
```

预期输出：

- 如果表里有数据，返回表格或结构化结果
- 如果表里没数据，明确说明“表是空的”
- 如果表名不匹配，明确说明“没有找到匹配表”

你之前提到“NAS MySQL 正常但查不到”，通常就是这一层的问题，不代表数据库不可用，更多时候是：

- 任务问法和真实表名不一致
- 数据库里没有 `drugs` 这张表
- 连接到了正确的 NAS MySQL，但当前库没有你期望的业务数据

### 4.5 验证完整任务链路

输入：

```text
帮我简单介绍一下这个系统能做什么。
```

预期输出：

- 模型能回复一段完整说明
- 过程中不会报 OpenRouter 认证错误
- 任务不会在子智能体分派阶段直接失败

这一步只能验证“主链路能跑”，不能证明数据库一定有数据。

### 4.6 如果你要验证数据库功能，推荐的顺序

先做这三个输入：

1. `先列出当前数据库有哪些表`
2. `再挑一张表预览前 5 行数据`
3. `基于真实表名执行一个最容易命中的查询`

对应预期：

- 第 1 步看连接
- 第 2 步看结构
- 第 3 步看业务数据

如果第 1 步都没有表名输出，优先检查：

- `.env` 的 `MYSQL_*`
- 你是不是连到了正确的 NAS MySQL
- 这个库里到底有没有初始化业务表

## 5. 当前功能可用性

这里说的是当前工作区的真实情况，不是项目设计目标。

### 5.1 可用与不可用一览

| 功能 | 当前状态 | 依赖 | 不可用原因 |
|---|---|---|---|
| 后端进程启动 | 可用 | `python3 -m uvicorn ...` | 无 |
| `/api/health` | 可用 | 后端进程已启动 | 无 |
| 前端页面打开 | 可用 | `npm install` / `npm run dev` | 无 |
| 前后端基础联通 | 可用 | 前端代理到 `http://localhost:8000` | 无 |
| NAS MySQL | 可用 | `.env` 中 `MYSQL_*` | 无 |
| 业务数据一定能查到 | 不可保证 | NAS MySQL 连接成功不等于表里一定有数据 | 当前库可能没有业务表，或者表名与提示词不一致 |
| 本地 Docker MySQL 教学环境 | 不可用 | `docker` | 当前工作区没有 `docker` 命令 |
| `uv sync` | 不可用 | `uv` | 当前工作区没有 `uv` 命令 |
| `uv run uvicorn ...` | 不可用 | `uv` | 当前工作区没有 `uv` 命令 |
| `pnpm install` | 不可用 | `pnpm` | 当前工作区没有 `pnpm` 命令 |
| `pnpm dev` | 不可用 | `pnpm` | 当前工作区没有 `pnpm` 命令 |
| OpenRouter 模型调用 | 可用，前提是配置完整 | `OPENROUTER_API_KEY`、`OPENROUTER_BASE_URL`、`LLM_QWEN_MAX` | 没有可用的模型 API Key，或者模型地址配置不正确 |
| NVIDIA 模型调用 | 可选备用 | `NVIDIA_API_KEY`、`NVIDIA_BASE_URL`、`NVIDIA_MODEL` | 没有 NVIDIA 凭证或模型名 |
| 数据库查询助手 | 可用，前提是 NAS MySQL 可访问 | `MYSQL_*` | 数据库没连通，或者 `.env` 里的账号、地址、库名不对 |
| `Tavily` 网络搜索 | 可选 | `TAVILY_API_KEY` | 没有搜索服务的 API Key |
| 本地知识库问答 | 可用，默认启用 | `docs/knowledge_base/` 目录 | 没有可检索文档 |
| 完整的多智能体任务链路 | 条件可用 | 模型、数据库、搜索、知识库等下游能力都可用 | 任一关键依赖缺失时，整条链路就会中断或降级 |

### 5.2 读表结论

- 现在可以稳定用的是：后端、前端、健康检查、前后端联通、NAS MySQL
- 现在不能保证的是：你指定某张业务表后一定能查到结果
- 不能直接用的是：`uv`、`pnpm`、本地 Docker MySQL
- 本地知识库不需要单独服务；只要 `docs/knowledge_base/` 里有文档，就能参与检索
- 任务链路是否完整可用，取决于 OpenRouter、NAS MySQL，以及你是否补齐可选的 Tavily / NVIDIA 配置

## 6. 最短复现版

只想照着重跑的话，按这个顺序：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main
cp .env.example .env
python3 scripts/check_environment.py
python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload
```

另开终端：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main
curl -s http://127.0.0.1:8000/api/health
```

再另开终端：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/frontend
npm install
npm run dev
```

然后打开：

```text
http://localhost:5173
```

## 7. OpenRouter 备注

这部分是从原来的 `RUNBOOK_OPENROUTER.md` 合并过来的补充说明。

- `OpenRouter` 路径就是这份主指南里的默认路径
- 如果 OpenRouter 返回 `402` 且你已经配置了 `NVIDIA_API_KEY` 和 `NVIDIA_MODEL`，主智能体会自动切到 NVIDIA 再试一次
- 如果你想显式控制 provider，优先看 `LLM_PROVIDER=openrouter|nvidia|auto`
- 如果你已经在项目根目录启动 Python，`sitecustomize.py` 会自动处理环境变量映射
- 如果你要跑 `examples/` 里的脚本，优先在项目根目录执行
- `1` 和 `2` 号示例通常还需要 `TAVILY_API_KEY`
- 涉及数据库的示例还依赖 `MYSQL_*`

示例：

```bash
python3 examples/1-deep-agent-quickstart-search.py
python3 examples/2-deep-agent-streaming-chunks.py
python3 examples/3-dict-subagents-routing.py
```

## 8. 保留原则

以后再补内容，优先只加三类信息：

1. 还能不能启动
2. 哪一步建议截屏
3. 哪个功能现在不能用

不要把排错、教程、截屏说明混在一个段落里，后面会很难维护。
