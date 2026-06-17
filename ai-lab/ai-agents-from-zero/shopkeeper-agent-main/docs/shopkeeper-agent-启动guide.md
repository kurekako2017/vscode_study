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
- 后端真实模式进程可以启动
- 完整真实问数链路还依赖 `NAS MySQL + Qdrant + Elasticsearch + Embedding`

## 2. 一条整体启动命令

在普通 WSL 终端里执行这一段。它启动的是真实模式，不是 Mock。

这条命令已经验证过：

- 后端返回 `backend_http=200`
- 前端返回 `frontend_http=200`
- 前端 `/api/query` 能通过 Vite 代理打到后端
- 当前真实查询返回的错误是 Elasticsearch `localhost:9200` 没启动，不是前后端没连上

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
- 如果看到 `Cannot connect to host localhost:9200`，说明 Elasticsearch 没启动

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

当前机器如果输出类似下面内容，表示真实问数链路还不能完成：

```text
Failed to connect
Connection refused
Operation timed out
```

原因是当前机器没有 `docker`，所以不能通过 `bash scripts/up_local_stack.sh up` 拉起 `Qdrant + Elasticsearch + Embedding`。

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

当前机器如果看到下面错误，表示真实问数链路还不能完成：

```text
Can't connect to MySQL server on '192.168.10.2' ([Errno 1] Operation not permitted)
```

这不是模型问题，是 NAS MySQL 网络访问没有打通。

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
data: {"type": "progress", "step": "召回字段取值", "status": "error"}
data: {"type": "error","message":"Cannot connect to host localhost:9200 ..."}
```

结论：前端代理和后端接口是通的；当前等不到真实答案，是因为 Elasticsearch `9200` 没启动。

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

## 4. 模型优先顺序

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

## 5. 当前已验证的命令状态

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

## 6. 当前不要用的错误命令

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

## 7. 真实链路还需要哪些外部服务

后端真实模式进程能启动，不等于完整问数链路已经成功。

完整真实问数还需要：

- `NAS MySQL`：`meta` / `dw`
- `Qdrant`：字段和指标向量召回
- `Elasticsearch`：字段取值检索
- `Embedding(TEI)`：文本向量
- `OpenRouter`、`NVIDIA` 或本地 `Ollama` 至少一个模型可用

当前已知阻塞：

```text
docker: command not found
```

所以当前机器不能用 `bash scripts/up_local_stack.sh up` 拉起 `Qdrant + Elasticsearch + Embedding`。

当前访问 NAS MySQL 的报错是：

```text
Can't connect to MySQL server on '192.168.10.2' ([Errno 1] Operation not permitted)
```

所以当前只能确认：

- 后端真实模式进程可以启动
- 前端启动命令是 `npm run dev`
- 本地 Ollama 回退模型存在
- 完整真实问数链路还没有打通

## 8. 真实链路验证命令

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

## 9. 最后兜底：Mock 模式

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
