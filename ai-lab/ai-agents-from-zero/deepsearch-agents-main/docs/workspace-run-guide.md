# 启动 / 验证 / 排错 最终版说明页

> 这份说明专门写给当前 `deepsearch-agents-main` 工作区。  
> 当前已验证的运行组合是：`OpenRouter + NAS MySQL + FastAPI + React`。  
> `Tavily` 和 `RAGFlow` 目前是可选项，不配置也能先把主链路跑起来。

## 1. 先看结论

如果你只是想快速把项目跑起来，顺序就是：

1. 配置 `.env`
2. 启动后端
3. 启动前端
4. 打开健康检查和前端页面确认状态
5. 再发起数据库查询任务

当前工作区里已经实测通过：

- 后端 `FastAPI` 可启动
- 前端 `Vite` 可启动
- `/api/health` 可返回正常状态
- 数据库查询子智能体可以连接 NAS MySQL
- 可以生成 Markdown 结果文件

如果你只想记住一句话，就记这个：

```text
先配 .env，再启动后端，再启动前端，再用健康检查和数据库任务验证，最后遇到问题就按排错清单逐项缩小范围。
```

### 推荐截图

- 这段结论区的页面截图
- 如果你想留存版本记录，也可以截一张 `.env` 配置文件关键片段截图

### 截图编号建议

- 截图 1：这段结论区
- 截图 2：`.env` 关键配置
- 截图 3：环境检查输出
- 截图 4：后端启动成功
- 截图 5：前端启动成功
- 截图 6：`/api/health` 返回
- 截图 7：数据库任务执行过程
- 截图 8：结果文件目录

## 2. 一键按顺序执行检查清单

如果你想最省心，就直接按下面顺序走。每一步完成后打勾再继续。

### 最短版 5 行命令

这组命令适合“依赖已经装好后”的日常快速起环境。第一次初始化时，还是建议先看上面的完整命令块。

```bash
cd ai-lab/ai-agents-from-zero/deepsearch-agents-main
python3 scripts/check_environment.py
PYTHONPATH=.deps python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000
cd frontend
npm run dev
```

### 推荐截图

- `check_environment.py` 的输出截图
- 后端 `uvicorn` 启动成功的终端截图
- 前端 `npm run dev` 启动成功的终端截图

如果你想给每个功能补“怎么用、怎么测”的统一写法，可以直接看：

- [`feature-usage-test-template.md`](feature-usage-test-template.md)

### 复制即可执行

下面这组命令按顺序一条条执行就行。你可以先复制到终端，再逐条回车。

```bash
cd ai-lab/ai-agents-from-zero/deepsearch-agents-main
python3 scripts/check_environment.py

python3 -m pip install --target .deps -r requirements.txt

PYTHONPATH=.deps python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000

cd frontend
npm install
npm run dev
```

如果你要验证数据库链路，再单独执行这条任务命令：

```bash
PYTHONPATH=.deps python3 - <<'PY'
import asyncio
from app.agent.main_agent import run_deep_agent
asyncio.run(run_deep_agent('请直接查询 drugs 表中 therapeutic_area 为 心血管 的药品，并用 Markdown 表格输出名称、品牌、规格、厂家和简介，直接给出结果，不要向我提问。', 'demo_db_003'))
PY
```

### 推荐截图

- 这条数据库任务命令本身的终端截图
- 前端里任务输入和执行中的事件流截图

说明：

- 上面第一段是启动顺序
- 第二段是数据库任务验证
- 如果你不想用 heredoc，就直接在前端里发同一句任务也可以
- 如果你当前环境里已经启动过后端或前端，重复执行对应命令时先 `Ctrl+C` 停掉旧进程再重启

- [ ] 进入项目目录：`cd ai-lab/ai-agents-from-zero/deepsearch-agents-main`
- [ ] 检查环境：`python3 scripts/check_environment.py`
- [ ] 确认 `.env` 里已经有：
  - [ ] `OPENROUTER_BASE_URL=https://openrouter.ai/api/v1`
  - [ ] `OPENROUTER_API_KEY=...`
  - [ ] `LLM_QWEN_MAX=openai/gpt-4o-mini`
  - [ ] `LLM_MAX_COMPLETION_TOKENS=1024`
  - [ ] `MYSQL_HOST=192.168.10.2`
  - [ ] `MYSQL_PORT=3306`
  - [ ] `MYSQL_USER=root`
  - [ ] `MYSQL_PASSWORD=123456`
  - [ ] `MYSQL_DATABASE=ecommjava`
- [ ] 安装后端依赖：
  - [ ] `python3 -m pip install --target .deps -r requirements.txt`
- [ ] 启动后端：
  - [ ] `PYTHONPATH=.deps python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000`
- [ ] 打开后端健康检查：
  - [ ] `http://127.0.0.1:8000/api/health`
- [ ] 启动前端：
  - [ ] `cd frontend`
  - [ ] `npm install`
  - [ ] `npm run dev`
- [ ] 打开前端页面：
  - [ ] `http://localhost:5173`
- [ ] 先跑一个数据库任务：
  - [ ] `请直接查询 drugs 表中 therapeutic_area 为 心血管 的药品，并用 Markdown 表格输出名称、品牌、规格、厂家和简介，直接给出结果，不要向我提问。`
- [ ] 确认结果文件生成在：
  - [ ] `app/output/session_{thread_id}/cardiovascular_drugs.md`

## 3. 当前前提

你这份环境里，最关键的前提是：

- 大模型走 `OpenRouter`
- 模型推荐使用 `openai/gpt-4o-mini`
- 模型输出上限建议设置为 `1024`
- MySQL 直接连 NAS 上的 `JtProject` 数据库
- `Tavily` 和 `RAGFlow` 可以先留空

推荐的 `.env` 关键值：

```bash
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

### 推荐截图

- `.env` 文件中 `OPENROUTER_*` 和 `MYSQL_*` 的配置片段截图

## 4. 环境检查

先进入项目目录：

```bash
cd ai-lab/ai-agents-from-zero/deepsearch-agents-main
```

然后检查当前环境：

```bash
python3 scripts/check_environment.py
```

你会重点看到这些项：

- `MYSQL_HOST` / `MYSQL_PORT` / `MYSQL_USER` / `MYSQL_PASSWORD` / `MYSQL_DATABASE`
- `LLM` 是否已配置
- `TAVILY_API_KEY` 和 `RAGFLOW_*` 是否为空

如果 `TAVILY` 和 `RAGFlow` 还是空的，不影响主链路启动，只是这两条能力先不可用。

### 推荐截图

- 环境检查命令的终端输出
- 重点保留 `mysql`、`llm`、`tavily`、`ragflow` 的状态行

### 预期结果

- Python 和 Node 可用
- MySQL 配置可读
- LLM 配置可读
- 可选服务未配置时能正常显示为空或未配置

### 排错点

- 如果 `mysql` 异常，先看 NAS 上 MySQL 是否在线
- 如果 `llm` 异常，先看 OpenRouter key 是否正确

## 5. 后端怎么启动

### 推荐方式

如果你的环境里已经有 `uv`，优先用：

```bash
uv sync
uv run uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload
```

### 当前工作区可用方式

如果 `uv` 还没有装，就用当前工作区实测可用的方式：

```bash
python3 -m pip install --target .deps -r requirements.txt
PYTHONPATH=.deps python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000
```

### 推荐截图

- `uvicorn` 成功启动的终端截图
- 最好截到监听地址和端口，比如 `0.0.0.0:8000`

后端启动后，可以访问：

```text
http://127.0.0.1:8000/api/health
```

健康检查正常时，你会看到类似：

- `backend: alive`
- `llm: configured`
- `mysql: configured`

### 推荐截图

- 浏览器打开 `http://127.0.0.1:8000/api/health` 的 JSON 页面
- 或终端 `curl` 的返回结果

### 预期结果

- 后端启动成功
- 健康检查返回 `ok`

### 排错点

- 如果启动就报错，先看依赖是否安装完整
- 如果健康检查失败，先看 `.env` 是否加载正确

## 6. 前端怎么启动

### 推荐方式

如果你已经有 `pnpm`：

```bash
cd frontend
pnpm install
pnpm dev
```

### 当前工作区可用方式

如果 `pnpm` 还没装，当前工作区里已经验证过可以直接用 `npm`：

```bash
cd frontend
npm install
npm run dev
```

前端默认会启动在：

```text
http://localhost:5173
```

### 推荐截图

- `npm run dev` 成功后的终端截图
- 浏览器中前端首页截图

## 7. 启动顺序

建议按这个顺序启动：

1. 先启动后端
2. 再启动前端
3. 再打开健康页和页面确认联通

这样如果有问题，会更容易判断是后端、前端还是数据库配置出了问题。

### 推荐截图

- 后端终端和前端终端并排截图
- 后端健康页和前端首页并排截图

## 8. 验证方法

### 验证后端

打开：

```text
http://127.0.0.1:8000/api/health
```

正常时，说明：

- 后端进程起来了
- OpenRouter 配置生效了
- NAS MySQL 配置生效了

#### 推荐截图

- 后端健康检查 JSON 截图

#### 预期结果

- 返回 `status=ok`
- 关键依赖状态正常

#### 排错点

- 如果 `llm` 异常，先检查 OpenRouter 配置
- 如果 `mysql` 异常，先检查 NAS MySQL 连通性

### 验证前端

打开：

```text
http://localhost:5173
```

页面里能看到健康状态面板，就说明前后端已经联通。

#### 推荐截图

- 前端首页截图
- 健康状态面板截图

#### 预期结果

- 页面可打开
- 健康面板可见

#### 排错点

- 如果页面打不开，先看前端进程
- 如果健康面板异常，先看后端健康接口

### 验证数据库链路

在前端任务输入框里直接试这个任务：

```text
请直接查询 drugs 表中 therapeutic_area 为 心血管 的药品，并用 Markdown 表格输出名称、品牌、规格、厂家和简介，直接给出结果，不要向我提问。
```

这个任务在当前工作区已经验证过，可以生成结果文件。

#### 推荐截图

- 前端输入框里填写任务的截图
- 执行过程中的事件流截图
- 最终回答中的表格截图
- 输出文件目录截图

#### 预期结果

- 能看到数据库查询结果
- 能看到 Markdown 表格
- 能在输出目录找到 `cardiovascular_drugs.md`

#### 排错点

- 如果没有结果文件，先看任务是否真的完成
- 如果结果不对，先看 MySQL 表和字段名是否写对

## 9. 结果文件在哪里

每次任务都会在下面这个目录创建会话产物：

```text
app/output/session_{thread_id}
```

比如数据库任务成功后，会生成类似：

```text
app/output/session_demo_db_003/cardiovascular_drugs.md
```

### 推荐截图

- 文件管理器里 `app/output/session_demo_db_003/` 的目录截图
- Markdown 文件内容预览截图

### 预期结果

- 文件存在
- 文件内容和任务一致

## 10. 这套环境里哪些东西可以先不配

可以先不配：

- `TAVILY_API_KEY`
- `RAGFLOW_API_URL`
- `RAGFLOW_API_KEY`

不影响：

- 后端启动
- 前端启动
- 健康检查
- 数据库查询
- Markdown 文件生成

### 推荐截图

- `.env` 里留空的可选项截图
- 健康检查里可选服务显示未配置的截图

### 预期结果

- 主链路仍然能跑
- 可选服务不影响后端和前端启动

## 11. 排错清单

### 1) 后端启动了，但数据库查不通

优先检查：

- `MYSQL_HOST=192.168.10.2`
- `MYSQL_PORT=3306`
- `MYSQL_USER=root`
- `MYSQL_PASSWORD=123456`
- `MYSQL_DATABASE=ecommjava`

#### 推荐截图

- `.env` 的 MySQL 配置截图
- NAS 上 MySQL 容器状态截图

#### 预期结果

- NAS MySQL 处于运行状态
- 项目能查到 `drugs` 表

### 2) 健康检查显示 OpenRouter 配置正常，但任务还是报额度错误

优先把：

```bash
LLM_QWEN_MAX=openai/gpt-4o-mini
LLM_MAX_COMPLETION_TOKENS=1024
```

写进 `.env`。

#### 推荐截图

- `.env` 里模型配置截图
- 健康检查里 `llm` 的状态截图

### 3) 前端打不开

先确认前端进程在跑：

```bash
npm run dev
```

如果你改了前端配置，通常重启一次前端就能生效。

#### 推荐截图

- 前端启动终端截图
- 浏览器空白页或报错页截图

### 4) 健康检查里 llm、mysql、services 显示不全

优先排查：

1. `.env` 是否真的在项目根目录
2. 后端启动前是否重新加载了环境变量
3. `app/api/server.py` 是否已经被当前进程加载
4. 是否还在使用旧的后端进程

#### 推荐截图

- 后端进程列表截图
- 重新启动后的日志截图

### 5) 数据库任务能跑，但结果不对

优先检查：

1. 任务里有没有明确表名
2. 任务里有没有明确字段名
3. NAS MySQL 里是否真的有对应数据
4. 结果文件是否生成在当前 `thread_id` 的目录中

#### 推荐截图

- 任务输入截图
- 执行结果截图
- 输出文件截图

## 12. 最终建议

如果你在当前工作区只想先验证主链路，建议按这个顺序：

1. 先跑后端健康检查
2. 再跑前端页面
3. 再跑数据库查询任务
4. 最后再决定要不要补 Tavily 和 RAGFlow

这条路最稳，也最适合先把项目跑通。

### 推荐截图

- 一次完整联调流程的截图合集
- 建议至少包含：健康检查、前端首页、数据库结果、输出文件
