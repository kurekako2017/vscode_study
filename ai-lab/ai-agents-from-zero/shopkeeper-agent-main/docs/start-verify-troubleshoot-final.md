# shopkeeper-agent-main 启动 / 验证 / 排错最终说明

> 这一页是给你后面反复回看的最终版。
> 目标只有一个：不管 Docker 正不正常，你都能先把项目搭起来，知道怎么验证，遇到问题知道先查哪里。

## 1. 这个项目的核心链路

这个项目本质上是一个“电商问数”智能体：

- 用户输入自然语言问题
- 后端把问题转成 SSE 流
- 智能体先召回字段、指标、值域
- 再生成 SQL
- 再查询数仓
- 最后把结果返回给前端

## 2. 两种运行模式

### 2.1 Mock 模式

适合：

- Docker Desktop / WSL 还没修好
- 你想先把前后端联调跑起来
- 你想先看 SSE 流和页面展示效果

特点：

- 不依赖 MySQL、Qdrant、Elasticsearch、Embedding、LLM
- `/api/query` 直接返回模拟结果
- 前端可以正常展示进度和结果

### 2.2 真实模式

适合：

- 你已经准备好 OpenRouter API Key
- 你想复用 NAS 上的 MySQL
- 你要跑完整真实链路

特点：

- 后端接 OpenRouter
- `meta` / `dw` 接 NAS MySQL
- Qdrant / Elasticsearch / Embedding 走本机基础服务
- 前端展示真实问数过程

## 3. 先选模式

### 先跑起来，推荐 mock

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
cp .env.mock.example .env
MOCK_MODE=true python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

另开一个终端启动前端：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main/frontend
pnpm install
pnpm dev
```

### 切回真实链路，推荐 OpenRouter + NAS MySQL

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
cp .env.nas.example .env
bash scripts/up_local_stack.sh up
python3 -m app.scripts.build_meta_knowledge -c conf/meta_config.yaml
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

另开一个终端启动前端：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main/frontend
pnpm install
pnpm dev
```

## 4. 启动前先准备什么

### 4.1 通用准备

- Python 3.12+
- `pnpm`
- 项目根目录 `.env`
- 前端 `.env` 如需自定义代理可再补

### 4.2 Mock 模式需要什么

- `MOCK_MODE=true`
- `VITE_API_BASE_URL=`
- `VITE_DEV_PROXY_TARGET=http://127.0.0.1:8000`

### 4.3 真实模式需要什么

- `OPENROUTER_API_KEY`
- NAS MySQL 的 `meta` / `dw`
- 本机 Qdrant / Elasticsearch / Embedding

## 5. 怎么验证是否启动成功

### 5.1 配置是否能读

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
python3 -m app.conf.app_config
```

预期：

- 不报配置错误
- 能输出配置内容

### 5.2 Mock 接口是否通

```bash
curl -N -sS -X POST http://127.0.0.1:8000/api/query -H 'Content-Type: application/json' -d '{"query":"统计华北地区销售额"}'
```

预期：

- 先看到多段 `progress`
- 最后看到 `result`

### 5.3 前端页面是否通

输入：

```text
统计华北地区销售额
```

预期：

- 页面显示问数过程
- 页面显示 SQL 摘要
- 页面显示结果卡片

### 5.4 真实模式基础服务是否通

```bash
curl -s http://127.0.0.1:6333
curl -s http://127.0.0.1:9200
curl -s http://127.0.0.1:8081
```

预期：

- Qdrant 返回版本信息
- Elasticsearch 返回节点信息
- Embedding 返回响应

### 5.5 NAS MySQL 是否通

```bash
mysql -h 192.168.10.2 -P 3306 -u root -p
```

预期：

- 能登录
- 能看到 `meta` 和 `dw`

### 5.6 元数据知识库是否构建成功

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
python3 -m app.scripts.build_meta_knowledge -c conf/meta_config.yaml
```

预期：

- 构建过程结束
- `meta` 库里有表、字段、指标
- Qdrant 里有字段和指标集合
- Elasticsearch 里有字段值索引

## 6. 功能测试怎么做

### 6.1 Mock 问数

输入：

```text
统计华北地区销售额
```

预期：

- `progress` 逐步推进
- 最后返回示例 SQL 和示例数据

### 6.2 真实问数

输入：

- `统计华北地区销售额`
- `统计 2025 年第一季度各大区的 GMV，并按 GMV 从高到低排序`
- `按会员等级统计 2025 年第一季度的订单数和销售额`

预期：

- 返回真实 SSE
- 结果和问题语义匹配

### 6.3 前端联动

输入任意问题后，预期看到：

- 执行进度
- SQL 摘要
- 结果内容

## 7. 排错顺序

### 7.1 如果后端起不来

先看：

1. `.env` 有没有放到项目根目录
2. `MOCK_MODE` 有没有写对
3. 配置文件是否能读
4. 当前 Python 环境是否缺包

### 7.2 如果 mock 接口没有 SSE

先看：

1. `main.py` 是否真的挂了 `mock_query_router`
2. `app/api/lifespan.py` 是否在 mock 模式下跳过了外部依赖
3. 终端里有没有启动成功日志

### 7.3 如果真实模式不通

先看：

1. NAS MySQL 是否连得上
2. `meta` / `dw` 是否已创建并导入
3. Qdrant / Elasticsearch / Embedding 是否已启动
4. `build_meta_knowledge` 是否成功
5. OpenRouter Key 是否已设置

### 7.4 如果 Docker CLI 在 WSL 不可用

先别卡住项目本身，直接走 mock 模式继续开发和联调。

这不是项目逻辑坏了，而是本机 Docker Desktop / WSL 互通链路的问题。

## 8. 最短判断法

### Mock 成功

满足下面两条就算成功：

- 后端 `/api/query` 返回 SSE
- 前端能看到进度和结果

### 真实成功

满足下面这几条就算成功：

- NAS MySQL 可连通
- `meta` / `dw` 已导入
- Qdrant / Elasticsearch / Embedding 在线
- `build_meta_knowledge` 跑完
- `/api/query` 返回真实结果
- 前端页面显示真实问数链路

## 9. 推荐使用顺序

1. 先跑 mock
2. 再确认前端
3. 再确认基础服务
4. 再确认 NAS MySQL
5. 再跑真实模式

## 10. 常用入口

- [Mock 优先启动说明](mock-first-quickstart.md)
- [Mock 启动命令块](mock-first-copy-paste.md)
- [Mock 最短 5 行命令](mock-first-5lines.md)
- [OpenRouter + NAS MySQL 启动说明](openrouter-nas-mysql-quickstart.md)
- [功能一览与测试指南](feature-overview-and-test-guide.md)
- [功能检查清单](feature-checklist.md)
