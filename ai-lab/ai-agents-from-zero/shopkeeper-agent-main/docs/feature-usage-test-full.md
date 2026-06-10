# 功能使用与测试完整版

> 这份文档适合你真的要做功能验收、演示或排错时使用。  
> 每个功能都固定写成：功能说明、测试命令、推荐截图、预期结果、排错点。

## 0. 可直接复用的示例截图

你可以先把这几张现成图片当作参考：

- 前端首页示例图：[shopkeeper-agent-home.jpg](images/shopkeeper-agent-home.jpg)
- 查询结果示例图：[shopkeeper-agent-query-result.jpg](images/shopkeeper-agent-query-result.jpg)
- 系统架构图：[shopkeeper-agent-system-architecture.svg](images/shopkeeper-agent-system-architecture.svg)

如果你后面补自己的截图，建议命名成：

- `mock-query-result.png`
- `real-query-result.png`
- `meta-build-result.png`
- `frontend-home.png`
- `mysql-connect-result.png`

## 0.1 截图编号建议

如果你要把这份文档做成“验收版”，建议按下面编号补图：

- 截图 1：环境检查
- 截图 2：Mock 后端启动
- 截图 3：Mock 问数结果
- 截图 4：元数据构建结果
- 截图 5：真实后端启动
- 截图 6：前端问数页面
- 截图 7：NAS MySQL 连接
- 截图 8：完整联调流程

## 1. Mock 问数链路

### 1.1 功能说明

- 在没有 Docker 或真实基础设施还没准备好时，先把前后端链路跑起来。
- 直接返回模拟 SSE，不依赖 MySQL / Qdrant / ES / Embedding / LLM。

### 1.2 测试命令

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
MOCK_MODE=true python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

另开一个终端：

```bash
curl -N -sS -X POST http://127.0.0.1:8000/api/query -H 'Content-Type: application/json' -d '{"query":"统计华北地区销售额"}'
```

### 1.3 推荐截图

- 后端启动终端截图
- `curl` SSE 输出截图
- 前端问数页面截图

### 1.4 预期结果

- 先返回多段 `progress`
- 最后返回 `result`
- `result` 里有示例 SQL 和示例数据

### 1.5 排错点

- `MOCK_MODE=true` 是否真的生效
- `main.py` 是否挂载了 mock 路由
- 终端是否显示 Uvicorn 启动成功

## 2. 真实问数链路

### 2.1 功能说明

- 真正接到 OpenRouter + NAS MySQL + Qdrant + Elasticsearch + Embedding。
- 用户输入自然语言后，后端执行完整的召回、生成、查询、返回流程。

### 2.2 测试命令

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
cp .env.nas.example .env
bash scripts/up_local_stack.sh up
python3 -m app.scripts.build_meta_knowledge -c conf/meta_config.yaml
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

### 2.3 推荐截图

- 基础服务启动截图
- 元数据知识库构建完成截图
- 后端启动截图
- 前端问数结果截图

### 2.4 预期结果

- `meta` 和 `dw` 能连上 NAS MySQL
- Qdrant / Elasticsearch / Embedding 在线
- `/api/query` 能返回真实 SSE
- 前端能展示 SQL 和查询结果

### 2.5 排错点

- `OPENROUTER_API_KEY` 是否正确
- `DB_META_*` / `DB_DW_*` 是否指向 NAS
- `build_meta_knowledge` 是否成功
- 本机基础服务是否已经启动

## 3. 元数据知识库构建

### 3.1 功能说明

- 从 NAS MySQL 的教学数仓里抽取元数据，构建后续问数需要的检索知识库。

### 3.2 测试命令

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
python3 -m app.scripts.build_meta_knowledge -c conf/meta_config.yaml
```

### 3.3 推荐截图

- 构建过程终端截图
- `meta` 库表结构截图
- Qdrant collection 截图
- Elasticsearch 索引截图

### 3.4 预期结果

- 表、字段、指标、字段值索引都能写入成功

### 3.5 排错点

- NAS MySQL 是否连通
- Embedding 服务是否可用
- Qdrant / Elasticsearch 是否启动

## 4. 前端问数页面

### 4.1 功能说明

- 展示问数输入框、样例问题、SSE 过程和结果卡片。

### 4.2 测试命令

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main/frontend
pnpm install
pnpm dev
```

### 4.3 推荐截图

- 前端首页截图
- 输入问题后的执行流截图
- 结果卡片截图

### 4.4 预期结果

- 页面能打开
- 能看到样例问题
- 点击发送后可以展示进度和结果

### 4.5 排错点

- 前端是否连到正确后端地址
- `VITE_API_BASE_URL` 是否配置正确
- `VITE_DEV_PROXY_TARGET` 是否指向 `127.0.0.1:8000`

## 5. NAS MySQL 连接

### 5.1 功能说明

- 项目把 MySQL 拆成两个库：
  - `meta`：保存元数据
  - `dw`：保存教学数仓

### 5.2 测试命令

```bash
mysql -h 192.168.10.2 -P 3306 -u root -p
```

### 5.3 推荐截图

- MySQL 登录成功截图
- 数据库列表截图

### 5.4 预期结果

- 能登录
- 能看到 `meta` 和 `dw`

### 5.5 排错点

- NAS 上 MySQL 是否启动
- IP、端口、账号、密码是否正确

## 6. Qdrant / Elasticsearch / Embedding

### 6.1 功能说明

- Qdrant 存向量。
- Elasticsearch 存字段值。
- Embedding 把文本转成向量。

### 6.2 测试命令

```bash
curl -s http://127.0.0.1:6333
curl -s http://127.0.0.1:9200
curl -s http://127.0.0.1:8081
```

### 6.3 预期结果

- 三个服务都能返回响应

### 6.4 排错点

- Docker 基础服务是否启动
- 端口是否冲突
- Embedding 首次启动是否还在下载模型

## 7. 结果文件生成

### 7.1 功能说明

- 结果可以保存为可阅读的 Markdown 文档。

### 7.2 测试命令

```text
请整理一份心血管药品报告，并保存为 Markdown 文件。
```

### 7.3 预期结果

- 生成 Markdown 文件
- 文件内容和回答一致

## 8. 推荐测试顺序

如果你想按最稳的方式验证，建议这样测：

1. 先测 Mock 问数
2. 再测前端页面
3. 再测 Qdrant / ES / Embedding
4. 再测 NAS MySQL
5. 再跑元数据知识库构建
6. 最后切真实问数

## 9. 一句话判断是否成功

- Mock 成功：前后端能联调，SSE 能看到进度和结果
- 真实成功：NAS MySQL、Qdrant、ES、Embedding、OpenRouter 都接通，问数结果能回来
