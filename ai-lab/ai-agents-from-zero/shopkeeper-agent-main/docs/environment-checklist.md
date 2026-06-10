# shopkeeper-agent-main 环境清单

> 目标：把 `shopkeeper-agent-main` 在当前工作区里真正跑起来，而不是只停留在“知道要配什么”的层面。

## 1. 这套项目里各组件的职责

- `OpenRouter / OpenAI Compatible API`
  - 负责提供大模型推理能力。
  - 主问数链路最终都依赖它来做理解、规划、总结和结果组织。
- `NAS MySQL`
  - 负责承载结构化业务数据。
  - 在这个项目里，它相当于“原系统里的业务数据库”。
- `Qdrant`
  - 负责存字段和指标向量。
  - 给问数时的语义召回用。
- `Elasticsearch`
  - 负责存字段真实取值。
  - 给问数时的值域检索用。
- `Embedding`
  - 负责把字段、指标和问题文本转成向量。
- `FastAPI`
  - 负责后端接口、SSE 流和依赖装配。
- `React + Vite`
  - 负责前端问数页面、进度展示和结果展示。

## 2. MySQL 在这里到底干什么

是的，你的理解基本正确。

这个项目里的 MySQL 可以理解成“原系统里的业务数据库”，智能体不是直接接管整个原系统，而是通过问数链路去检索这个数据库里的结果，再结合检索结果和模型回答问题。

它解决的核心问题是：

- 让智能体能查到真实、结构化、可聚合的数据；
- 避免把库存、销量、订单、区域这些信息全都交给模型“猜”；
- 让回答从“语言模型推测”变成“能落到查询结果”的业务回答。

如果不用这种方式，常见结果是：

- 模型会把业务数据说得很像真的，但实际上并没有查数据库；
- 回答无法追溯来源，业务场景里很容易出错；
- 用户一问“某个区域销售额多少”，答案会漂；
- 无法形成可验证、可审计的闭环。

## 3. 当前环境清单

以下是当前工作区里已经确认过的环境状态：

- `Python 3.12.3`，可用
- `Node.js`，可用
- `docker`，当前优先作为可选项，不作为这条链路的必需项
- `pnpm`，如果没有也可以先用 `npm`

说明：

- 这意味着后端 Python 代码可以继续推进，而且 MySQL 可以继续走 NAS 远端数据库。
- 如果后续你想切回 Docker MySQL，再回到 Docker Desktop 的 WSL 集成设置即可。
- 如果暂时不想动 Docker，也可以继续使用 `Mock` 或 `NAS MySQL` 方案。

## 4. 必备环境变量

项目当前至少需要这些变量：

```bash
# 大模型
OPENROUTER_API_KEY=
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_API_KEY=
LLM_MODEL_NAME=openai/gpt-4o-mini
LLM_BASE_URL=https://openrouter.ai/api/v1

# 运行模式
MOCK_MODE=false

# NAS MySQL
DB_META_HOST=192.168.10.2
DB_META_PORT=3306
DB_META_USER=root
DB_META_PASSWORD=123456
DB_META_DATABASE=meta
DB_DW_HOST=192.168.10.2
DB_DW_PORT=3306
DB_DW_USER=root
DB_DW_PASSWORD=123456
DB_DW_DATABASE=dw

# 向量库
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_EMBEDDING_SIZE=1024

# Embedding
EMBEDDING_HOST=localhost
EMBEDDING_PORT=8081
EMBEDDING_MODEL=BAAI/bge-large-zh-v1.5

# 全文检索
ES_HOST=localhost
ES_PORT=9200
ES_INDEX_NAME=data_agent

# 前端
VITE_DEV_PROXY_TARGET=http://127.0.0.1:8000
VITE_API_BASE_URL=
```

建议优先策略：

1. 先确认大模型 API 可用，推荐 `OpenRouter`
2. 再确认 NAS MySQL 连接可用
3. 然后补 Qdrant / Elasticsearch / Embedding
4. 最后决定是先跑 `Mock` 还是直接进真实模式

## 5. 依赖与服务清单

### 后端

- Python 3.12
- 依赖安装方式（`pip` / `uv` 均可）

### 前端

- Node.js
- `pnpm` 或 `npm`
- `frontend/package.json`

### 外部服务

- OpenRouter 或其他 OpenAI-Compatible 模型服务
- NAS MySQL
- Qdrant
- Elasticsearch
- Embedding 服务

## 6. 适合当前工作区的落地顺序

### 第一步：先把环境边界定清楚

- 确认哪些服务要本机跑，哪些可以走远端服务。
- 当前这台环境里，Docker 不是第一优先级，所以可以先走 Mock 或 NAS MySQL。

### 第二步：先让后端“能起来”

- 配好 `.env`
- 启动 FastAPI
- 先验证配置能读、`/api/query` 能挂载

### 第三步：再接 NAS MySQL

- 先验证连通性
- 再验证 `meta` / `dw`
- 最后验证问数链路

### 第四步：再接 Qdrant / Elasticsearch / Embedding

- 先让向量检索和全文检索能工作
- 再让元数据构建跑通

### 第五步：最后再接前端

- 先看后端 SSE 是否正常
- 再看前端是否能展示进度和结果

## 7. 当前建议先做的实际落地

如果我们要“先实施一部分”，建议先落下面 3 件事：

1. 把 `.env.example` 或 `.env.nas.example` 复制成可本地使用的 `.env`，并补齐真实值或临时值。
2. 先尝试只启动后端，确认代码层面没有依赖或配置缺口。
3. 把数据库运行方案定下来：
   - 方案 A：先走 `Mock`
   - 方案 B：连接 NAS MySQL
   - 方案 C：如果 Docker 后面修好了，再切回本机容器

## 8. 当前落地进度

### 已完成

- 已补充环境清单文档。
- 已增加后端配置加载与 `.env` 覆盖。
- 已增加 `MOCK_MODE`，可在没有 Docker 的情况下先跑 mock SSE 链路。
- 已把 `OpenRouter` 适配进 `.env` 体系。
- 已把基础服务启动、功能测试和排错文档分层整理。

### 待完成

- 真实模式下的 `OpenRouter API Key` 需要你填真实值。
- NAS MySQL 的 `meta` / `dw` 还要按当前实际状态再确认一次。
- 如果要启用 Qdrant / Elasticsearch / Embedding 的真实联调，还要继续准备基础服务。

## 9. 结论

这套项目里的 MySQL，不是“额外随便挂一个数据库”，而是问数业务里的结构化数据源。

智能体的作用也不是替代数据库，而是：

- 先识别问题需要哪类数据；
- 再去对应数据源检索；
- 最后把检索结果组织成可读、可追溯、可交付的答案。
