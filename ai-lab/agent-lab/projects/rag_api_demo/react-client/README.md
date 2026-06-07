# rag_api_demo React 客户端

这是一个最小但可用的 React Web 客户端，用来调用 `rag_api_demo` 的 FastAPI 接口。

它适合当作这个 demo 的“最流行客户端形态”:

- 浏览器访问
- React 界面
- 通过 `fetch` 调用后端
- 保留对话历史和操作记录

## 1. 它会调哪些接口

- `GET /`
- `GET /health`
- `POST /ask`
- `POST /reload`

## 2. 本地运行

先确保后端在运行:

```bash
cd ai-lab/agent-lab/projects/rag_api_demo
./run-dev.sh
```

然后启动前端:

```bash
cd ai-lab/agent-lab/projects/rag_api_demo/react-client
npm install
npm run dev
```

默认会访问:

```text
http://127.0.0.1:8000
```

如果你的后端不在这个地址，可以在页面里修改 Base URL，或者创建 `.env` 文件并设置 `VITE_RAG_API_BASE_URL`。

## 3. 常见环境变量

- `VITE_RAG_API_BASE_URL`：如果你想在构建时指定默认后端地址，可以自行扩展到 `App.jsx`
- `react-client/.env.example`：可以复制成 `.env` 后修改默认后端地址
- `RAG_API_CORS_ORIGINS`：后端允许的浏览器来源，默认已经包含 `localhost:5173`

## 4. 这个客户端的定位

它不是生产级产品，而是一个最小的“人类用户客户端”示例，用来说明：

- 客户端如何调用 agent
- React 如何当作 API 客户端
- 前后端如何分离
