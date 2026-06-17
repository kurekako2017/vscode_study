# Shopkeeper Agent 新手总指南

> 这是一份合并后的总入口文档。  
> 目标很简单：少翻文件，先跑起来，再验证，再排错。

## 先看什么

推荐顺序：

1. 先看本页，确认这套项目是做什么的、怎么启动、怎么验证。
2. 再看 [目录结构调用流程图](shopkeeper-agent-目录结构调用流程图.md)，把代码入口和调用链路对应起来。
3. 如果你想看更细的功能说明，再回到源码和提示词。

## 项目在做什么

这是一个“电商问数”智能体项目，主链路是：

1. 用户输入自然语言问题
2. 后端把问题转成 SSE 流
3. 智能体召回字段、指标和值域
4. 生成 SQL
5. 校验并执行 SQL
6. 前端实时展示进度和结果

## 你需要准备什么

最少需要这些东西：

- Python 3.12+
- Node.js
- 一个可用的 `.env`
- 真实模式下还需要：
  - OpenRouter API Key
  - NAS MySQL 的 `meta` 和 `dw`
  - Qdrant
  - Elasticsearch
  - Embedding 服务

常用环境变量：

- `MOCK_MODE=true` 时走 mock SSE，不依赖外部基础设施
- `LLM_PROVIDER_ORDER=openrouter,nvidia,ollama`
- `VITE_DEV_PROXY_TARGET=http://127.0.0.1:8000`
- `VITE_API_BASE_URL=` 为空时走本地代理

## 两种启动模式

### 1. 先跑起来的 mock 模式

适合下面情况：

- Docker 还没完全准备好
- 你想先看前后端联调
- 你只关心 SSE 流和页面展示

启动后端：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
MOCK_MODE=true python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

启动前端：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main/frontend
npm install
npm run dev
```

### 2. 真实模式

适合下面情况：

- 你已经准备好真实模型和数据库
- 你要跑完整问数链路
- 你要验证 SQL 生成和执行

推荐顺序：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
bash scripts/up_local_stack.sh up
python3 -m app.scripts.build_meta_knowledge -c conf/meta_config.yaml
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

前端：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main/frontend
npm install
npm run dev
```

## 怎么验证

### 1. 后端是否在线

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/docs
```

预期：

- 返回 `200`

### 2. 前端是否在线

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:5173
```

预期：

- 返回 `200`

### 3. mock 接口是否有 SSE

```bash
curl -N -sS -X POST http://127.0.0.1:8000/api/query -H 'Content-Type: application/json' -d '{"query":"统计华北地区销售额"}'
```

预期：

- 先有多段 `progress`
- 最后有 `result`

### 4. 真实模式基础服务是否在线

```bash
curl -s http://127.0.0.1:6333
curl -s http://127.0.0.1:9200
curl -s http://127.0.0.1:8081
```

预期：

- Qdrant、Elasticsearch、Embedding 都能响应

### 5. NAS MySQL 是否可达

```bash
mysql -h 192.168.10.2 -P 3306 -u root -p
```

预期：

- 能登录
- 能看到 `meta` 和 `dw`

### 6. 元数据知识库是否构建成功

```bash
python3 -m app.scripts.build_meta_knowledge -c conf/meta_config.yaml
```

预期：

- 元数据库里有表、字段、指标
- Qdrant 里有字段和指标 collection
- Elasticsearch 里有字段值索引

## 功能一览

- 配置加载
- mock 问数链路
- 真实问数链路
- 元数据知识库构建
- `/api/query` SSE 接口
- 前端问数页面联动
- NAS MySQL 连接
- Qdrant 向量库连接
- Elasticsearch 全文检索连接
- Embedding 服务连接

## 排错顺序

### 1. 后端起不来

先看：

1. `.env` 是否放在项目根目录
2. `MOCK_MODE` 是否写对
3. 配置文件是否能读取
4. 当前 Python 环境是否缺包

### 2. mock 没有 SSE

先看：

1. `main.py` 是否挂了 `mock_query_router`
2. `app/api/lifespan.py` 是否在 mock 模式下跳过外部依赖
3. 终端里是否有启动成功日志

### 3. 真实模式不通

先看：

1. NAS MySQL 是否连得上
2. `meta` / `dw` 是否已导入
3. Qdrant / Elasticsearch / Embedding 是否启动
4. `build_meta_knowledge` 是否成功
5. OpenRouter Key 是否配置

### 4. Docker CLI 在 WSL 里不可用

先别卡住，直接走 mock 模式继续做前端联调和代码理解。

## 现在最实用的建议

如果你只想尽快推进，按这个顺序做：

1. 复制 `.env.example` 或 `.env.nas.example` 成 `.env`
2. 先用 `MOCK_MODE=true` 跑通后端和前端
3. 再切真实模式
4. 再补 NAS MySQL、Qdrant、Elasticsearch 和 Embedding
5. 最后做完整问数验证

## 旧文档说明

原来的以下文档内容已经合并到本页：

- `shopkeeper-agent-启动guide.md`
- `start-verify-troubleshoot-final.md`
- `feature-overview-and-test-guide.md`
- `environment-checklist.md`
- `local-environment-progress.md`

以后优先只看这一页，再按需要跳到源码或目录图。
