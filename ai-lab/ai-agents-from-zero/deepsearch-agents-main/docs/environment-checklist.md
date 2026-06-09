# DeepSearch Agents 环境清单

> 目标：把 `deepsearch-agents-main` 在当前工作区里真正跑起来，而不是只停留在“知道要配什么”的层面。

## 1. 这套项目里各组件的职责

- `OpenRouter / OpenAI Compatible API`
  - 负责提供大模型推理能力。
  - 主智能体和子智能体最终都依赖它来做理解、规划、总结和工具编排。
  - 这个项目现在同时支持 `OPENAI_*` 和 `OPENROUTER_*` 两套变量名。
- `MySQL`
  - 负责承载结构化业务数据。
  - 在这个项目里，它相当于“原本系统里的业务数据库”，但不是系统全量数据库，而是给数据库查询子智能体用的教学型业务库。
- `Tavily`
  - 负责互联网公开资料检索。
  - 适合新闻、行业信息、政策、网页资料等外部信息源。
- `RAGFlow`
  - 负责内部非结构化知识库问答。
  - 适合 PDF、文档、企业资料库等内部知识场景。
- `FastAPI + WebSocket`
  - 负责后端任务接口、事件流、文件上传下载和前后端实时联动。
- `React + Vite`
  - 负责前端对话界面、任务状态展示和结果查看。

## 2. MySQL 在这里到底干什么

是的，你的理解基本正确。

这个项目里的 MySQL 可以理解成“原系统里的业务数据库”，智能体不是直接接管整个原系统，而是通过数据库查询子智能体去检索这个业务数据库里的结果，再结合其他来源回答问题。

它解决的核心问题是：

- 让智能体能够查到真实、结构化、可聚合的数据；
- 避免把库存、销量、批次、产品信息这类信息全都交给模型“猜”；
- 让回答从“语言模型推测”变成“能落到 SQL 查询结果”的业务回答。

如果不用这种方式，常见结果是：

- 模型会把库存、销量、客户这些结构化信息说得很像真的，但实际上并没有查数据库；
- 回答无法追溯来源，业务场景里很容易出错；
- 当用户问“某个药当前库存多少”“某个区域销售额多少”时，答案会漂；
- 无法形成可验证、可审计的业务闭环。

## 3. 当前环境清单

以下是当前工作区里已经确认过的环境状态：

- `Python 3.12.3`，可用
- `Node v22.22.1`，可用
- `uv`，当前不可用
- `docker`，当前不作为这条链路的必需项
- `pnpm`，当前不可用

说明：

- 这意味着后端 Python 代码可以继续推进，而且 MySQL 已经切到 NAS 远端数据库，不再依赖本机容器。
- 如果后续你想切回 Docker MySQL，再回到 Docker Desktop 的 WSL 集成设置即可。
- 如果暂时不想动 Docker，也可以继续使用这个 NAS MySQL 方案。

## 4. 必备环境变量

项目当前至少需要这些变量：

```bash
# 大模型
OPENAI_BASE_URL=
OPENAI_API_KEY=
OPENROUTER_BASE_URL=
OPENROUTER_API_KEY=
LLM_QWEN_MAX=
LLM_MAX_COMPLETION_TOKENS=

# 互联网搜索
TAVILY_API_KEY=

# RAGFlow
RAGFLOW_API_URL=
RAGFLOW_API_KEY=

# MySQL
MYSQL_HOST=
MYSQL_PORT=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_DATABASE=
MYSQL_CHARSET=
MYSQL_COLLATION=
MYSQL_SQL_MODE=
```

建议优先策略：

1. 先确认大模型 API 可用，`OPENAI_*` 和 `OPENROUTER_*` 任意一套都可以，推荐 `openai/gpt-4o-mini` 这类文本模型，并把 `LLM_MAX_COMPLETION_TOKENS` 控制在一个合理范围内。
2. 再确认 MySQL 连接可用。
3. 然后补 Tavily。
4. 最后补 RAGFlow。

## 5. 依赖与服务清单

### 后端

- Python 3.12
- `uv` 或等价的 Python 依赖安装方式
- `requirements.txt` / `pyproject.toml`

### 前端

- Node.js
- `pnpm`
- `frontend/package.json`

### 外部服务

- OpenRouter 或其他 OpenAI-Compatible 模型服务
- MySQL 8.x
- Tavily API
- RAGFlow 服务

## 6. 适合当前工作区的落地顺序

### 第一步：先把环境边界定清楚

- 确认哪些服务要本机跑，哪些可以走外部服务。
- 当前这台环境里，Docker 不可用，所以 MySQL 容器要么换到远端，要么等 Docker Desktop WSL 集成可用。

### 第二步：先让后端“能起来”

- 配好 `.env`
- 安装后端依赖
- 启动 FastAPI
- 先验证健康检查和最小对话链路

### 第三步：再接 MySQL

- 先验证连通性
- 再验证表名、样例数据、SQL 查询
- 最后验证数据库查询子智能体的回答链路

### 第四步：再接 Tavily 和 RAGFlow

- 先让网络搜索能返回结果
- 再让知识库问答能查到内部文档

### 第五步：最后再接前端

- 先看后端事件流是否正常
- 再看前端是否能展示任务过程、结果和文件列表

## 7. 这次建议先做的实际落地

如果我们要“先实施一部分”，建议先落下面 3 件事：

1. 把 `.env.example` 复制成可本地使用的 `.env`，并补齐真实值或临时值。
2. 先尝试只启动后端，确认代码层面没有依赖或配置缺口。
3. 把 MySQL 的运行方案定下来：
   - 方案 A：本机 Docker 起 MySQL
   - 方案 B：连接一个已有的远端 MySQL
   - 方案 C：先不跑数据库，只验证非数据库链路
4. 如果想直接填值，可以先参考项目根目录的 `.env.template`。
5. 如果你决定采用本机 Docker MySQL，建议直接看这份说明：[`local-setup-openrouter-docker-mysql.md`](local-setup-openrouter-docker-mysql.md)
6. 如果你想直接按“当前工作区能跑起来”的顺序执行，建议直接看：[`workspace-run-guide.md`](workspace-run-guide.md)
7. 如果你想先看整套文档入口，建议直接看：[`docs-index.md`](docs-index.md)

## 8. 当前落地进度

### 已完成

- 已补充环境清单文档。
- 已增加环境校验脚本 `scripts/check_environment.py`。
- 已兼容 `OPENAI_*` 与 `OPENROUTER_*` 两套模型环境变量。
- 已把 Tavily 和 RAGFlow 改成按需初始化，避免没有 key 时后端导入失败。
- 已增加后端健康检查接口，前端可以直接读取后端、模型、MySQL 和外部服务状态。
- 已安装后端 Python 依赖。
- 已启动后端 `FastAPI` 服务。
- 已安装前端依赖并通过 `npm run build`。
- 已启动前端 `Vite` 开发服务器。
- 已确认 NAS MySQL 可用，并把深度研搜的教学库导入到 `deepsearch_db`。

### 待完成

- `uv` 依赖管理工具未安装。
- `pnpm` 未安装，当前前端用 `npm` 作为临时替代。
- `TAVILY_API_KEY`、`RAGFLOW_*` 和部分外部服务信息还没有补齐。
- 如果后续要启用 Tavily 和 RAGFlow，还需要继续补真实的外部服务地址和 key。

## 9. 结论

这套项目的 MySQL，不是“额外随便挂一个数据库”，而是多智能体研究流程里的结构化数据源。

智能体的作用也不是替代数据库，而是：

- 先识别问题需要哪类数据；
- 再去对应数据源检索；
- 最后把检索结果组织成可读、可追溯、可交付的答案。
