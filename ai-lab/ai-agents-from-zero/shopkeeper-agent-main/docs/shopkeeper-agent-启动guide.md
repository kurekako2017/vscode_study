# 启动 / 验证 / 排错 最终版说明页

> 这份说明专门写给当前 `shopkeeper-agent-main` 工作区。  
> 当前推荐运行组合是：真实模式默认 `OpenRouter -> NVIDIA -> 本地 Ollama qwen2.5-coder:1.5b`，数据库接 `NAS MySQL`；`Mock` 只作为前后端联调兜底。

## 1. 先看结论

如果你只是想快速把项目跑起来，顺序就是：

1. 配置 `.env`
2. 启动后端
3. 启动前端
4. 打开问数页面确认状态
5. 再发起问数任务

如果你只想记住一句话，就记这个：

```text
先配 .env，再启动后端，再启动前端，再用问数接口和页面验证，最后遇到问题就按排错清单逐项缩小范围。
```

## 2. 两种运行模式

### 2.1 真实模式

适合：

- 你已经准备好 OpenRouter 或 NVIDIA API Key
- 你已经有本地 Ollama 的 `qwen2.5-coder:1.5b`
- 你想跑完整真实问数链路

特点：

- 后端优先接 OpenRouter
- OpenRouter 失败后尝试 NVIDIA
- 远端模型都不可用时回退本地 Ollama
- `meta` / `dw` 接 NAS MySQL
- Qdrant / Elasticsearch / Embedding 走本机基础服务
- 前端展示真实问数过程

### 2.2 Mock 模式

适合：

- Docker 或 NAS MySQL 暂时不可用
- 你想先把前后端联调跑起来
- 你想先看 SSE 流和页面展示效果

特点：

- 不依赖 MySQL、Qdrant、Elasticsearch、Embedding、OpenRouter、NVIDIA 或 Ollama
- `/api/query` 直接返回模拟结果
- 前端可以正常展示进度和结果

## 2.3 当前实现状态

### 已完成并可用

- 后端 FastAPI 服务可以启动，并按 `MOCK_MODE` 在 mock / 真实模式之间切换
- 后端已经提供 `POST /api/query` SSE 接口
- Mock 模式可直接返回完整的模拟进度流和示例结果
- 真实模式已经接好 LangGraph 主链路：
  `抽取关键词 -> 三路召回 -> 合并召回 -> 过滤表/指标 -> 补充上下文 -> 生成 SQL -> 校验 SQL -> 校正 SQL -> 执行 SQL`
- 真实模式已经接好依赖装配：
  Meta MySQL、DW MySQL、Qdrant、Elasticsearch、Embedding、LLM
- LLM 已支持回退顺序：
  `OpenRouter -> NVIDIA -> 本地 Ollama qwen2.5-coder:1.5b`
- 元数据知识库构建脚本已经可用：
  `python3 -m app.scripts.build_meta_knowledge -c conf/meta_config.yaml`
- 前端页面已经可用，支持：
  输入问题、点击样例问题、展示 SSE 进度、展示结构化结果表、复制结果、停止当前请求、清空当前会话

### 当前不能用或暂未实现

- 当前后端只有一个业务接口：
  `POST /api/query`
  没有健康检查、历史记录、会话管理、用户管理、配置管理等额外 API
- 前端没有多轮上下文能力：
  每次提问都会单独发起一次新查询，历史消息只保存在当前页面内存里
- 前端没有会话持久化：
  刷新页面后历史消息会丢失
- 前端没有结果导出能力：
  目前只能复制结果文本，没有导出 CSV / Excel / JSON 文件的入口
- 前端没有单独的 SQL 展示面板：
  Mock 结果里会带示例 SQL，但真实模式当前只返回查询结果行，不会额外返回 SQL 文本
- 当前没有数据写回类能力：
  不支持新增、修改、删除业务数据，也没有审批流
- 当前没有独立的知识库管理页面：
  元数据构建只能通过脚本触发，不是页面化操作
- 当前不是通用数据库 Agent：
  代码和配置是围绕当前电商教学数仓、MySQL、Qdrant、Elasticsearch 这套组合写的
- 当前没有鉴权和权限隔离：
  这是本地开发 / 演示形态，不是可直接上线的多租户系统

## 3. 先选模式

### 推荐：真实链路，OpenRouter / NVIDIA / Ollama + NAS MySQL

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

### 兜底：Mock 联调

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

## 4. 怎么验证是否启动成功

### 4.1 配置是否能读

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
python3 -m app.conf.app_config
```

预期：

- 不报配置错误
- 能输出配置内容

### 4.2 Mock 接口是否通

```bash
curl -N -sS -X POST http://127.0.0.1:8000/api/query -H 'Content-Type: application/json' -d '{"query":"统计华北地区销售额"}'
```

预期：

- 先看到多段 `progress`
- 最后看到 `result`

### 4.3 前端页面是否通

输入：

```text
统计华北地区销售额
```

预期：

- 页面显示问数过程
- 页面显示结构化结果表
- Mock 模式下结果对象里会带示例 SQL
- 真实模式下当前主要展示查询结果，不单独展示 SQL

### 4.4 真实模式基础服务是否通

```bash
curl -s http://127.0.0.1:6333
curl -s http://127.0.0.1:9200
curl -s http://127.0.0.1:8081
```

预期：

- Qdrant 返回版本信息
- Elasticsearch 返回节点信息
- Embedding 返回响应

### 4.5 NAS MySQL 是否通

```bash
mysql -h 192.168.10.2 -P 3306 -u root -p
```

预期：

- 能登录
- 能看到 `meta` 和 `dw`

### 4.6 元数据知识库是否构建成功

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
python3 -m app.scripts.build_meta_knowledge -c conf/meta_config.yaml
```

预期：

- 构建过程结束
- `meta` 库里有表、字段、指标
- Qdrant 里有字段和指标集合
- Elasticsearch 里有字段值索引

## 5. 排错顺序

### 5.1 如果后端起不来

先看：

1. `.env` 有没有放到项目根目录
2. `MOCK_MODE` 有没有写对
3. 配置文件是否能读
4. 当前 Python 环境是否缺包

### 5.2 如果 mock 接口没有 SSE

先看：

1. `main.py` 是否真的挂了 `mock_query_router`
2. `app/api/lifespan.py` 是否在 mock 模式下跳过了外部依赖
3. 终端里有没有启动成功日志

### 5.3 如果真实模式不通

先看：

1. NAS MySQL 是否连得上
2. `meta` / `dw` 是否已创建并导入
3. Qdrant / Elasticsearch / Embedding 是否已启动
4. `build_meta_knowledge` 是否成功
5. OpenRouter 或 NVIDIA Key 是否已设置
6. `ollama list` 是否能看到 `qwen2.5-coder:1.5b`

### 5.4 如果 Docker CLI 在 WSL 不可用

先确认是否能走 NAS MySQL + 本地 Ollama；如果基础服务也不可用，再走 Mock 模式继续开发和联调。

这不是项目逻辑坏了，而是本机 Docker Desktop / WSL 互通链路的问题。

## 6. 最短判断法

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
- 模型链路至少有 OpenRouter、NVIDIA 或本地 Ollama 一个可用
- `/api/query` 返回真实结果
- 前端页面显示真实问数链路

## 7. 当前最值得记住的边界

- 这套代码已经能跑“单轮电商问数”主链路
- 这套代码还不是“带后台、带权限、带历史会话”的完整产品
- Mock 适合联调
- 真实模式适合验证当前教学数仓上的问数闭环

## 8. 常用入口

- [Mock 优先启动说明](mock-first-quickstart.md)
- [Mock 启动命令块](mock-first-copy-paste.md)
- [Mock 最短 5 行命令](mock-first-5lines.md)
- [OpenRouter + NAS MySQL 说明](local-setup-openrouter-docker-mysql.md)
- [LLM Provider 回退运行模式](llm-provider-fallback.md)
- [功能一览与测试指南](feature-overview-and-test-guide.md)
- [功能检查清单](feature-checklist.md)
