# 功能一览与测试指南

> 这份文档的目标很直接：
> 1. 让你知道这个项目到底有哪些功能
> 2. 让你知道每个功能怎么测试
> 3. 让你知道输入什么、预期看到什么

## 1. 功能总览

这个项目的核心功能只有一条主线，但会拆成几个可测试的能力：

- 配置加载
- Mock 问数链路
- 真实问数链路
- 元数据知识库构建
- 后端 `/api/query` SSE 接口
- 前端问数页面联动
- NAS MySQL 连接
- Qdrant 向量库连接
- Elasticsearch 全文检索连接
- Embedding 服务连接

## 1.1 当前已经完成的功能

- `POST /api/query` 已完成，支持 SSE 流式返回
- Mock 问数链路已完成，可脱离外部基础设施运行
- 真实问数链路已完成主流程编排，可执行单轮问数
- LangGraph 执行步骤可在前端可视化展示
- 元数据知识库构建脚本已完成
- 前端单页问数界面已完成，支持样例问题、手工输入、停止查询、复制结果、清空会话
- LLM 已支持 `OpenRouter -> NVIDIA -> 本地 Ollama qwen2.5-coder:1.5b` 回退

## 1.2 当前不能使用或尚未实现的功能

- 没有除 `/api/query` 之外的业务 API
- 没有登录、鉴权、权限控制
- 没有会话持久化和历史记录存档
- 没有多轮上下文问答
- 没有页面化的知识库构建和管理入口
- 没有 CSV / Excel / JSON 导出入口
- 没有单独的 SQL 展示面板
- 没有写库、改库、删库这类数据操作能力
- 没有通用数据源适配层，当前默认围绕 MySQL + Qdrant + Elasticsearch

## 2. 配置加载

### 功能说明

项目启动时会读取 `.env` 和 `conf/app_config.yaml`，把 MySQL、Qdrant、ES、Embedding、LLM 和运行模式配置装配起来。

### 怎么测试

运行：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
python3 -m app.conf.app_config
```

### 输入

- 读取当前 `.env`
- 读取 `conf/app_config.yaml`

### 预期结果

- 能打印出配置里的 `es.host`
- 不报配置解析错误

## 3. Mock 问数链路

### 功能说明

Mock 模式下，后端不依赖 MySQL、Qdrant、Elasticsearch、Embedding 和大模型，直接返回一条模拟 SSE 流。

这个功能的价值是：

- Docker 没修好也能先联调前端
- 你可以先理解 SSE 的返回格式
- 你可以先看完整的问数过程展示

### 怎么测试

1. 启动后端：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
MOCK_MODE=true python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

2. 调接口：

```bash
curl -N -sS -X POST http://127.0.0.1:8000/api/query -H 'Content-Type: application/json' -d '{"query":"统计华北地区销售额"}'
```

### 输入

```text
统计华北地区销售额
```

### 预期结果

- 先返回一串 `progress`
- 进度步骤依次包括：
  - `抽取关键词`
  - `召回字段信息`
  - `召回指标信息`
  - `召回字段取值`
  - `生成 SQL`
  - `执行 SQL`
- 最后返回 `result`
- `result` 中会包含示例 SQL 和示例数据

## 4. 真实问数链路

### 功能说明

真实模式下，后端会：

- 读取用户问题
- 从 Qdrant 召回字段和指标
- 从 Elasticsearch 召回字段取值
- 结合 LLM 生成 SQL
- 去 NAS MySQL 的 `dw` 库执行 SQL
- 把结果以 SSE 形式返回给前端

### 怎么测试

1. 确认 `.env` 使用真实模式配置
2. 启动基础服务
3. 构建元数据知识库
4. 启动后端
5. 发起问数请求

### 输入

可以先用这些测试问题：

- `统计华北地区销售额`
- `统计 2025 年第一季度各大区的 GMV，并按 GMV 从高到低排序`
- `按会员等级统计 2025 年第一季度的订单数和销售额`

### 预期结果

- 页面或接口先返回进度流
- 最终返回查询结果
- 查询结果里的字段和问题语义匹配

补充说明：

- Mock 模式下，`result` 会带示例 SQL 和示例数据
- 真实模式下，当前 `run_sql` 节点返回的是结果行列表，不会单独把 SQL 再包装回前端

## 5. 元数据知识库构建

### 功能说明

这个功能会从 NAS MySQL 的教学数仓里抽取元数据，构建后续问数需要的检索知识库。

它会做三件事：

- 把表、字段、指标等元数据写入元数据库
- 把字段和指标向量写入 Qdrant
- 把字段值写入 Elasticsearch

### 怎么测试

运行：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
python3 -m app.scripts.build_meta_knowledge -c conf/meta_config.yaml
```

### 输入

- `conf/meta_config.yaml`
- NAS MySQL 中的 `meta` 和 `dw`

### 预期结果

- 终端显示构建流程完成
- `meta` 库里出现表、字段、指标和关系数据
- Qdrant 里出现字段和指标 collection
- Elasticsearch 里出现字段值索引

## 6. 后端 `/api/query`

### 功能说明

这是前端真正调用的问数接口，返回 SSE 流。

### 怎么测试

```bash
curl -N -sS -X POST http://127.0.0.1:8000/api/query -H 'Content-Type: application/json' -d '{"query":"统计华北地区销售额"}'
```

### 输入

```json
{"query":"统计华北地区销售额"}
```

### 预期结果

- 返回 `text/event-stream`
- 先有 `progress`
- 后有 `result`
- 出错时返回 `error`

## 7. 前端问数页面

### 功能说明

前端负责：

- 展示问数输入框
- 展示样例问题
- 展示 SSE 过程
- 展示结构化结果表
- 复制结果
- 停止当前请求
- 清空当前页面会话

### 怎么测试

1. 启动前端
2. 打开页面
3. 点击样例问题或手工输入
4. 观察结果

### 输入

```text
统计华北地区销售额
```

### 预期结果

- 页面显示“正在连接问数智能体”
- 逐步更新执行步骤
- 最后显示结果内容

当前限制：

- 刷新页面后消息历史不会保留
- 当前没有多轮对话上下文
- 真实模式下没有单独 SQL 面板

## 8. NAS MySQL 连接

### 功能说明

项目把 MySQL 拆成两个库：

- `meta`：保存元数据
- `dw`：保存教学数仓

### 怎么测试

```bash
mysql -h 192.168.10.2 -P 3306 -u root -p
```

### 输入

- Host: `192.168.10.2`
- Port: `3306`
- User: `root`
- Password: `123456`

### 预期结果

- 能登录 MySQL
- 能看到 `meta` 和 `dw`

## 9. Qdrant 连接

### 功能说明

Qdrant 存字段和指标向量，给问数时的语义召回用。

### 怎么测试

```bash
curl -s http://127.0.0.1:6333
```

### 预期结果

- 返回 Qdrant 的版本信息

## 10. Elasticsearch 连接

### 功能说明

Elasticsearch 存字段真实取值，用来支持值域检索。

### 怎么测试

```bash
curl -s http://127.0.0.1:9200
```

### 预期结果

- 返回 Elasticsearch 节点和版本信息

## 11. Embedding 服务连接

### 功能说明

Embedding 服务负责把字段、指标、问题等文本转成向量。

### 怎么测试

```bash
curl -s http://127.0.0.1:8081
```

### 预期结果

- 服务能响应
- 第一次启动时可能比较慢，因为需要拉模型

## 12. 推荐测试顺序

如果你想按最稳的方式验证，建议这样测：

1. 先测 mock 问数
2. 再测前端页面
3. 再测 Qdrant / ES / Embedding
4. 再测 NAS MySQL
5. 再跑元数据知识库构建
6. 再测本地 Ollama 是否可用
7. 最后切真实问数

## 13. 一句话判断是否成功

- Mock 成功：前后端能联调，SSE 能看到进度和结果
- 真实成功：NAS MySQL、Qdrant、ES、Embedding、LLM 全都接通，`/api/query` 能返回真实结果
