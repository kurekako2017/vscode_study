# DeepSearch Agents Frontend

React + Vite + Tailwind CSS + Ant Design frontend for the DeepSearch Agents FastAPI backend.

## Run

```bash
npm install
npm run dev
```

By default the app talks to `http://localhost:8000` and `ws://localhost:8000`.
Override with `.env.local`:

```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_BASE_URL=ws://localhost:8000
```

Frontend runtime does not configure the LLM, MySQL, or local knowledge base directly.
Those settings belong in the repository root `.env`:

- `OPENROUTER_*` for the default model provider
- `NVIDIA_*` for optional fallback
- `MYSQL_*` for the NAS database
- The local knowledge base is read from `docs/knowledge_base/`

## Backend Contract

- `GET /api/health`
- `POST /api/task`
- `POST /api/upload`
- `GET /api/files`
- `GET /api/download`
- `WebSocket /ws/{thread_id}`

The sidebar reads `GET /api/health` to show whether the backend, model, MySQL, Tavily,
and local knowledge base are present.
