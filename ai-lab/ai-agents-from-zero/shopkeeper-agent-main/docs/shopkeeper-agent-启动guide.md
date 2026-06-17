# shopkeeper-agent 当前机器启动指南

> 这份文档只写当前 `shopkeeper-agent-main` 工作区里真实可执行的命令。  
> 默认先走真实链路：`OpenRouter -> NVIDIA -> 本地 Ollama qwen2.5-coder:1.5b`。  
> 不一上来启动 Mock。Mock 只能在真实链路处理不了时最后兜底，并且必须明确标记为 Mock。

## 1. 当前结论

当前机器的实际情况：

- 后端不要用 `uv sync` / `uv run`：当前机器没有 `uv`
- 前端不要用 `pnpm`：当前机器没有 `pnpm`
- 后端可以直接复用仓库里的 `.venv`
- 前端可以直接用 `npm`
- 本机 `ollama` 已经有 `qwen2.5-coder:1.5b`
- Docker Desktop 已打开 WSL Integration，当前 WSL 里可以访问 Docker 容器服务
- 后端真实模式进程可以启动，并已验证能连接 `NAS MySQL + Qdrant + Elasticsearch + Embedding`
- 当前真实链路默认走 `.env`：`NAS MySQL 192.168.10.2 + 本机 Docker Qdrant/ES/Embedding + 本地 Ollama`
- 已验证真实查询 `统计华北地区销售额` 能返回 `销售额 = 41099.5`

## 2. 一条整体启动命令

在普通 WSL 终端里执行这一段。它启动的是真实模式，不是 Mock。

这条命令已经验证过：

- 后端返回 `backend_http=200`
- 前端返回 `frontend_http=200`
- 前端 `/api/query` 能通过 Vite 代理打到后端
- 当前真实查询 `统计华北地区销售额` 可以跑到 `执行SQL success` 并返回结果

这里故意使用 `8010` 和 `5188`，避免你机器上已有的 `8000` / `5173` 残留进程干扰验证。

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main

export MOCK_MODE=false
export LLM_PROVIDER_ORDER=openrouter,nvidia,ollama
export OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
export OLLAMA_MODEL_NAME=qwen2.5-coder:1.5b
export OLLAMA_API_KEY=ollama

export BACKEND_PORT=8010
export FRONTEND_PORT=5188

.venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port "$BACKEND_PORT" > /tmp/shopkeeper-backend-"$BACKEND_PORT".log 2>&1 &
BACKEND_PID=$!

sleep 5
echo "backend_http=$(curl -s --max-time 5 -o /dev/null -w '%{http_code}' http://127.0.0.1:${BACKEND_PORT}/docs)"

cd frontend
VITE_DEV_PROXY_TARGET=http://127.0.0.1:${BACKEND_PORT} npm run dev -- --host 127.0.0.1 --port "$FRONTEND_PORT" --strictPort > /tmp/shopkeeper-frontend-"$FRONTEND_PORT".log 2>&1 &
FRONTEND_PID=$!
trap 'kill "$FRONTEND_PID" "$BACKEND_PID" 2>/dev/null' EXIT

sleep 5
echo "frontend_http=$(curl -s --max-time 5 -o /dev/null -w '%{http_code}' http://127.0.0.1:${FRONTEND_PORT})"

echo "query_output:"
curl -N --max-time 25 -sS \
  -X POST http://127.0.0.1:${FRONTEND_PORT}/api/query \
  -H 'Content-Type: application/json' \
  -H 'Accept: text/event-stream' \
  -d '{"query":"统计华北地区销售额"}'

echo
echo "backend_log=/tmp/shopkeeper-backend-${BACKEND_PORT}.log"
echo "frontend_log=/tmp/shopkeeper-frontend-${FRONTEND_PORT}.log"
echo "frontend_url=http://127.0.0.1:${FRONTEND_PORT}"
echo "backend_url=http://127.0.0.1:${BACKEND_PORT}"

wait "$FRONTEND_PID"
kill "$BACKEND_PID"
```

打开：

```text
http://127.0.0.1:5188
```

说明：

- 后端地址：`http://127.0.0.1:8010`
- 前端地址：`http://127.0.0.1:5188`
- 前端通过 Vite 代理访问后端 `/api`
- 这条命令没有设置 `MOCK_MODE=true`
- 如果 `frontend_http` 不是 `200`，看 `/tmp/shopkeeper-frontend-5188.log`
- 如果 `backend_http` 不是 `200`，看 `/tmp/shopkeeper-backend-8010.log`
- 如果看到 `Cannot connect to host localhost:9200`，说明当前后端还没有连上 Elasticsearch，先检查 Docker 容器

如果你希望后端日志和前端日志分开看，用两个终端启动。

终端 1，后端：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main

export MOCK_MODE=false
export LLM_PROVIDER_ORDER=openrouter,nvidia,ollama
export OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
export OLLAMA_MODEL_NAME=qwen2.5-coder:1.5b
export OLLAMA_API_KEY=ollama

.venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8010
```

终端 2，前端：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main/frontend
VITE_DEV_PROXY_TARGET=http://127.0.0.1:8010 npm run dev -- --host 127.0.0.1 --port 5188 --strictPort
```

## 3. 启动后测试内容

启动后不要先盲等页面回答。按下面顺序测，每一步都写了输入和预想输出。

### 测试 1：后端进程是否真的在线

输入：

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8010/docs
```

预想输出：

```text
200
```

如果不是 `200`，说明后端没起来，先回到后端终端看 `uvicorn` 日志。

### 测试 2：前端进程是否真的在线

输入：

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:5188
```

预想输出：

```text
200
```

如果不是 `200`，说明前端没起来，先回到前端终端看 `npm run dev` 日志。

### 测试 3：本地 Ollama 回退模型是否存在

输入：

```bash
ollama list
```

预想输出里必须能看到：

```text
qwen2.5-coder:1.5b
```

如果看不到，先执行：

```bash
ollama pull qwen2.5-coder:1.5b
```

### 测试 4：真实链路基础服务是否在线

输入：

```bash
curl -s --max-time 5 http://127.0.0.1:6333
curl -s --max-time 5 http://127.0.0.1:9200
curl -s --max-time 5 http://127.0.0.1:8081
```

预想输出：

- `6333` 应该返回 Qdrant 的 JSON 信息
- `9200` 应该返回 Elasticsearch 的 JSON 信息
- `8081` 应该返回 Embedding 服务响应，至少不能连接失败

如果输出类似下面内容，表示真实问数链路还不能完成：

```text
Failed to connect
Connection refused
Operation timed out
```

当前机器 Docker 已经可用；如果这里仍然连接失败，优先检查 Docker Desktop 是否正在运行，以及 `docker ps` 里是否有 `qdrant`、`elasticsearch`、`embedding`。

### 测试 5：NAS MySQL 是否能连通

输入：

```bash
mysql -h 192.168.10.2 -P 3306 -u root -p
```

预想输出：

```text
能进入 mysql> 命令行
能看到 meta / dw 两个库
```

如果看到下面错误，表示真实问数链路还不能完成：

```text
Can't connect to MySQL server on '192.168.10.2' ([Errno 1] Operation not permitted)
```

这不是模型问题，是 NAS MySQL 网络访问没有打通，或后端仍在读取旧配置。

### 测试 6：真实问数接口测试

只有测试 3、4、5 都通过后，再测 `/api/query`。不要在基础服务没通时一直等页面回答。

这里先走前端代理地址 `5188/api/query`，因为这和浏览器页面的请求路径一致。

输入：

```bash
curl -N --max-time 180 -sS \
  -X POST http://127.0.0.1:5188/api/query \
  -H 'Content-Type: application/json' \
  -H 'Accept: text/event-stream' \
  -d '{"query":"统计华北地区销售额"}'
```

如果要绕过前端代理，直接测后端，把地址改成：

```text
http://127.0.0.1:8010/api/query
```

真实链路成功时，预想输出应该是 SSE 流，先出现多条 `progress`，最后出现 `result`：

```text
data: {"type":"progress","step":"抽取关键词","status":"running"}
data: {"type":"progress","step":"抽取关键词","status":"success"}
...
data: {"type":"result","data":[...]}
```

如果输出类似下面内容，表示后端捕获到了真实链路错误：

```text
data: {"type":"error","message":"..."}
```

当前这台机器已验证的实际输出是：

```text
data: {"type": "progress", "step": "抽取关键词", "status": "running"}
data: {"type": "progress", "step": "抽取关键词", "status": "success"}
data: {"type": "progress", "step": "召回字段信息", "status": "running"}
data: {"type": "progress", "step": "召回指标信息", "status": "running"}
data: {"type": "progress", "step": "召回字段取值", "status": "running"}
data: {"type": "progress", "step": "召回字段取值", "status": "success"}
data: {"type": "progress", "step": "召回字段信息", "status": "success"}
data: {"type": "progress", "step": "召回指标信息", "status": "success"}
data: {"type": "progress", "step": "合并召回信息", "status": "success"}
...
data: {"type": "progress", "step": "执行SQL", "status": "success"}
data: {"type": "result", "data": [{"销售额": 41099.5}]}
```

结论：前端代理、后端接口、三路召回、合并召回、SQL 生成和真实查询都已打通。

如果 180 秒内一直没有 `result`，通常卡在这些位置之一：

- OpenRouter / NVIDIA 网络请求没有返回
- 本地 Ollama 生成太慢或模型服务没有响应
- Embedding 服务没有响应
- Qdrant / Elasticsearch 没有响应
- NAS MySQL 没有响应

这时先看后端终端日志里最后一个 `step`：

- 停在 `召回字段信息` / `召回指标信息`：优先查 Embedding 和 Qdrant
- 停在 `召回字段取值`：优先查 Elasticsearch
- 停在 `合并召回信息` / `添加额外上下文`：优先查 NAS MySQL
- 停在 `生成SQL` / `校正SQL`：优先查 OpenRouter、NVIDIA、Ollama
- 停在 `执行SQL`：优先查 NAS MySQL 的 `dw` 库

### 测试 7：前端页面输入测试

输入页面地址：

```text
http://127.0.0.1:5188
```

页面输入：

```text
统计华北地区销售额
```

真实链路成功时，预想输出：

- 页面出现执行进度节点
- 节点按顺序推进到 `执行SQL`
- 最后出现结果表
- 结果来自 NAS MySQL，不是 Mock

如果页面一直转，没有回答：

- 先不要切 Mock
- 先执行“测试 6：真实问数接口测试”
- 再根据后端日志最后一个 `step` 判断卡在哪个外部依赖

如果页面显示：

```text
接口请求失败：HTTP xxx
```

这说明浏览器请求 `/api/query` 得到的是非 2xx HTTP 状态码，优先按下面顺序查：

1. `curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8010/docs`
2. `curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:5188`
3. `curl -N --max-time 25 -sS -X POST http://127.0.0.1:5188/api/query -H 'Content-Type: application/json' -H 'Accept: text/event-stream' -d '{"query":"统计华北地区销售额"}'`

如果第 1 步不是 `200`，后端没起来。  
如果第 2 步不是 `200`，前端没起来。  
如果第 1、2 步都是 `200`，但第 3 步报 HTTP 错误，看 `/tmp/shopkeeper-frontend-5188.log` 里的 Vite proxy 错误。

## 4. 业务逻辑测试点

这一节用于验证“真实业务链路是否正确”，不是只看服务有没有启动。每个用例都建议同时观察前端节点、后端日志和最终结果。

通用成功路径应该依次出现这些节点：

```text
抽取关键词 -> 召回字段信息 / 召回指标信息 / 召回字段取值 -> 合并召回信息 -> 过滤指标信息 / 过滤表信息 -> 添加额外上下文 -> 生成SQL -> 校验SQL -> 执行SQL -> result
```

如果某一步变红，先按节点定位：

- `召回字段信息` / `召回指标信息`：查 `Embedding 8081` 和 `Qdrant 6333`
- `召回字段取值`：查 `Elasticsearch 9200`
- `合并召回信息`：查 `NAS MySQL meta`，尤其是 `DB_META_HOST` 是否仍误指向 `localhost`
- `添加额外上下文` / `执行SQL`：查 `NAS MySQL dw`
- `生成SQL` / `校正SQL`：查模型，当前本机默认是 `qwen2.5-coder:1.5b`

### 用例 1：华北地区销售额

输入：

```text
统计华北地区销售额
```

测试目的：

- 验证字段取值召回能命中 `dim_region.region_name = 华北`
- 验证指标召回能命中 `GMV` 或销售额相关指标
- 验证合并节点能补齐 `fact_order.region_id` 与 `dim_region.region_id`
- 验证 SQL 生成能正确 JOIN 地区维表

预想中间结果：

```text
抽取关键词：包含 华北地区 / 销售额
召回字段取值：dim_region.region_name.华北
召回指标信息：GMV
合并召回信息：包含 fact_order、dim_region
过滤表信息：保留 fact_order、dim_region
```

预想 SQL 形态：

```sql
SELECT SUM(fact_order.order_amount) AS 销售额
FROM fact_order
JOIN dim_region ON fact_order.region_id = dim_region.region_id
WHERE dim_region.region_name = '华北'
```

预想出力：

```text
销售额 = 41099.5
```

### 用例 2：各大区 GMV 排序

输入：

```text
统计 2025 年第一季度各大区的 GMV，并按 GMV 从高到低排序
```

测试目的：

- 验证时间语义能使用 `dim_date.year = 2025` 和 `dim_date.quarter = Q1`
- 验证大区维度能使用 `dim_region.region_name`
- 验证 GMV 指标能聚合 `fact_order.order_amount`
- 验证排序逻辑 `ORDER BY GMV DESC`

预想 SQL 形态：

```sql
SELECT dim_region.region_name, SUM(fact_order.order_amount) AS GMV
FROM fact_order
JOIN dim_region ON fact_order.region_id = dim_region.region_id
JOIN dim_date ON fact_order.date_id = dim_date.date_id
WHERE dim_date.year = 2025 AND dim_date.quarter = 'Q1'
GROUP BY dim_region.region_name
ORDER BY GMV DESC
```

预想出力：

```text
华东 107373.0
华南 70202.0
华北 41099.5
西南 31528.0
华中 28957.0
```

### 用例 3：2025 年 3 月各商品品类销量和销售额

输入：

```text
统计 2025 年 3 月各商品品类的销量和销售额
```

测试目的：

- 验证商品品类召回与 `dim_product.category`
- 验证销量使用 `SUM(fact_order.order_quantity)`
- 验证销售额使用 `SUM(fact_order.order_amount)`
- 验证月份过滤使用 `dim_date.year = 2025` 和 `dim_date.month = 3`

预想出力：

```text
手机数码 销量 10 销售额 62190.0
家用电器 销量 6 销售额 19196.0
鞋靴 销量 4 销售额 4396.0
服饰 销量 7 销售额 2593.0
食品饮料 销量 139 销售额 1115.0
休闲零食 销量 156 销售额 630.0
```

说明：

如果排序字段没有在问题中明确指定，返回顺序可以不同；重点看每个品类的数值是否一致。

### 用例 4：会员等级订单数和销售额

输入：

```text
按会员等级统计 2025 年第一季度的订单数和销售额
```

测试目的：

- 验证客户维表 `dim_customer.member_level`
- 验证订单数使用 `COUNT(fact_order.order_id)`
- 验证销售额使用 `SUM(fact_order.order_amount)`
- 验证 `fact_order.customer_id = dim_customer.customer_id`

预想出力：

```text
黄金 订单数 34 销售额 100178.5
白银 订单数 30 销售额 71094.0
铂金 订单数 25 销售额 57679.0
青铜 订单数 26 销售额 50208.0
```

### 用例 5：华东地区销售额最高的前 5 个商品

输入：

```text
查询华东地区 2025 年第一季度销售额最高的前 5 个商品
```

测试目的：

- 验证地区取值召回 `dim_region.region_name = 华东`
- 验证商品名称维度 `dim_product.product_name`
- 验证多表 JOIN：`fact_order + dim_region + dim_product + dim_date`
- 验证 Top N 排序和 `LIMIT 5`

预想出力：

```text
Galaxy S24 Ultra 28497.0
Mate 60 Pro 27996.0
iPhone 15 Pro 17998.0
戴森 V15 吸尘器 10998.0
美的空调 KFR-35GW 6400.0
```

### 用例 6：合并召回信息专项检查

输入：

```text
统计华北地区销售额
```

如果页面红在：

```text
合并召回信息
```

先看后端日志，常见错误和含义如下：

```text
Can't connect to MySQL server on 'localhost'
```

含义：

```text
后端仍在连接本机 MySQL，不是在连接 NAS MySQL。
通常是旧后端进程没停，或 .env 没被当前进程读取。
```

处理：

```bash
ps -ef | grep 'uvicorn main:app'
kill 旧后端PID
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
.venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

预想修复后：

```text
合并召回信息 success
后续进入 过滤指标信息 / 过滤表信息
```

## 5. 模型优先顺序

真实链路的模型优先顺序是：

```text
OpenRouter -> NVIDIA -> 本地 Ollama qwen2.5-coder:1.5b
```

对应环境变量：

```bash
LLM_PROVIDER_ORDER=openrouter,nvidia,ollama
OPENROUTER_API_KEY=你的_openrouter_api_key
NVIDIA_API_KEY=你的_nvidia_api_key
OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
OLLAMA_MODEL_NAME=qwen2.5-coder:1.5b
OLLAMA_API_KEY=ollama
```

如果 `OPENROUTER_API_KEY` 为空，代码会跳过 OpenRouter。  
如果 `NVIDIA_API_KEY` 为空，代码会跳过 NVIDIA。  
如果前两个都不可用，代码会回退到本地 Ollama。

## 6. 当前已验证的命令状态

后端依赖：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
.venv/bin/python -c "import uvicorn, fastapi; print('backend_venv_ok')"
```

已验证：可用。

后端启动：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
.venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8010
```

已验证：后端进程可以启动。

前端启动命令：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main/frontend
VITE_DEV_PROXY_TARGET=http://127.0.0.1:8010 npm run dev -- --host 127.0.0.1 --port 5188 --strictPort
```

已验证：可启动，Vite 返回 `http://127.0.0.1:5188/`。

Ollama：

```bash
ollama list
```

已验证：本机有 `qwen2.5-coder:1.5b`。

## 7. 当前不要用的错误命令

不要用：

```bash
uv sync
uv run fastapi dev main.py
uv run python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

原因：

```text
uv: command not found
```

不要用：

```bash
pnpm install
pnpm dev
```

原因：

```text
pnpm: command not found
```

不要把下面这段作为真实模式启动命令：

```bash
MOCK_MODE=true .venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

原因：

```text
这是 Mock 模式，不是真实链路。
```

## 8. 真实链路还需要哪些外部服务

后端真实模式进程能启动，不等于完整问数链路已经成功。

完整真实问数还需要：

- `NAS MySQL`：`meta` / `dw`
- `Qdrant`：字段和指标向量召回
- `Elasticsearch`：字段取值检索
- `Embedding(TEI)`：文本向量
- `OpenRouter`、`NVIDIA` 或本地 `Ollama` 至少一个模型可用

当前已验证：

- Docker Desktop WSL Integration 已可用
- `Qdrant 6333` 可访问
- `Elasticsearch 9200` 可访问
- `Embedding 8081` 容器已启动
- `NAS MySQL 192.168.10.2:3306` 可访问
- 真实链路已跑通 `统计华北地区销售额`

## 9. 真实链路验证命令

后端和前端启动后，先验证基础服务。

Qdrant：

```bash
curl -s http://127.0.0.1:6333
```

Elasticsearch：

```bash
curl -s http://127.0.0.1:9200
```

Embedding：

```bash
curl -s http://127.0.0.1:8081
```

NAS MySQL：

```bash
mysql -h 192.168.10.2 -P 3306 -u root -p
```

Ollama：

```bash
ollama list
```

只有这些都通了，再构建元数据知识库：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
.venv/bin/python -m app.scripts.build_meta_knowledge -c conf/meta_config.yaml
```

然后再通过页面发起真实问数。

## 10. 最后兜底：Mock 模式

只有在真实链路确认处理不了时，才用 Mock。

Mock 后端命令：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
MOCK_MODE=true .venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Mock 前端命令：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main/frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

必须明确标记：

- 这是 Mock 模式
- `/api/query` 返回的是 Mock 数据
- 页面上看到的进度、SQL、结果表都不是 NAS MySQL 的真实查询结果
- 测试记录里不能把 Mock 写成真实链路成功
