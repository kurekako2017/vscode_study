# OpenRouter + NAS MySQL 最终可运行配置

这份配置是给当前 `deepsearch-agents-main` workspace 用的。

目标很明确：

- 默认模型走 `OpenRouter`
- OpenRouter 返回 `402` 时，如果已经配置了 `NVIDIA`，自动兜底
- 数据库固定走 `NAS MySQL`
- 前端只连后端，不直接配置模型或数据库

## 1. 最小必需项

只要先把下面这些配好，就能启动主链路：

```env
LLM_PROVIDER=openrouter
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_API_KEY=你的_openrouter_api_key
LLM_QWEN_MAX=openai/gpt-4o-mini
LLM_MAX_COMPLETION_TOKENS=1024

MYSQL_HOST=192.168.10.2
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=123456
MYSQL_DATABASE=ecommjava
MYSQL_CHARSET=utf8mb4
MYSQL_COLLATION=utf8mb4_unicode_ci
MYSQL_SQL_MODE=TRADITIONAL
```

## 2. 可选 NVIDIA 兜底

如果你希望 OpenRouter 402 时继续跑，就再补这些：

```env
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
NVIDIA_API_KEY=你的_nvidia_api_key
NVIDIA_MODEL=你实际可用的_nvidia_model
LLM_PROVIDER=auto
```

说明：

- `LLM_PROVIDER=openrouter`：默认优先 OpenRouter
- `LLM_PROVIDER=nvidia`：强制使用 NVIDIA
- `LLM_PROVIDER=auto`：OpenRouter 优先，失败后再看 NVIDIA 是否可用

## 3. 前端只需要什么

前端目录里只需要这两个变量：

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_BASE_URL=ws://localhost:8000
```

模型和数据库都不要写在前端 `.env.local` 里，它们属于仓库根目录 `.env`。

## 4. 当前 workspace 的启动顺序

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main
python3 scripts/check_environment.py
python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload
```

另开一个终端：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/frontend
npm install
npm run dev
```

浏览器打开：

```text
http://localhost:5173
```

## 5. 你应该看到什么

`/api/health` 里：

- `backend = alive`
- `llm.configured = true`
- `llm.provider = openrouter` 或 `nvidia`
- `llm.source = openrouter` 或 `nvidia`
- `mysql.configured = true`
- `mysql.host = 192.168.10.2`
- `mysql.port = 3306`

前端健康面板里：

- `LLM` 显示 `provider · source / model`
- `MySQL` 显示 `192.168.10.2:3306`

## 6. 常见误区

- `NAS MySQL` 可用，不等于每个业务表都有数据
- `OpenRouter` 返回 `402`，不是问法错了，是额度、账单或模型可用性问题
- 前端不负责配置模型和数据库，根配置都在仓库根目录 `.env`
- `uv`、`pnpm` 在当前 workspace 里不可直接依赖，主指南里已经给了替代命令

## 7. 验证建议

先按这个顺序看：

1. `python3 scripts/check_environment.py`
2. 后端启动日志
3. `GET /api/health`
4. 前端首页
5. 数据库查询任务

如果数据库查询返回空，不要先怀疑 NAS MySQL，先确认：

- 你是不是连到了正确的库
- 这张表是不是存在
- 这个库里是不是本来就没有你想要的数据
