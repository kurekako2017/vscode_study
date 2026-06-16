# LLM Provider 回退运行模式

当前真实问数链路默认不走 mock，而是按下面顺序调用模型：

```text
OpenRouter -> NVIDIA NIM -> 本地 Ollama qwen2.5-coder:1.5b
```

## 1. 必填与可选变量

```bash
LLM_PROVIDER_ORDER=openrouter,nvidia,ollama

OPENROUTER_API_KEY=你的_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL_NAME=openai/gpt-4o-mini

NVIDIA_API_KEY=你的_nvidia_api_key
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
NVIDIA_MODEL_NAME=nvidia/llama-3.3-nemotron-super-49b-v1

OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
OLLAMA_MODEL_NAME=qwen2.5-coder:1.5b
OLLAMA_API_KEY=ollama
```

说明：

- `OPENROUTER_API_KEY` 已填时，优先走 OpenRouter。
- `NVIDIA_API_KEY` 已填时，OpenRouter 失败后会尝试 NVIDIA。
- 本地 Ollama 不需要真实 key，但 OpenAI 兼容客户端要求传一个值，所以保留 `OLLAMA_API_KEY=ollama`。
- 旧的 `LLM_API_KEY`、`LLM_MODEL_NAME`、`LLM_BASE_URL` 仍兼容，会在没有单独 OpenRouter 配置时映射到 OpenRouter。
- 如果你的 NVIDIA 环境变量叫 `NGC_API_KEY`，后端会自动兼容为 `NVIDIA_API_KEY`。

## 2. 本地 Ollama 准备

```bash
ollama list
ollama pull qwen2.5-coder:1.5b
```

当前项目已经按 OpenAI-Compatible `/v1` 形式访问 Ollama：

```bash
OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
```

## 3. 验证配置

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
.venv/bin/python -m app.conf.app_config
.venv/bin/python - <<'PY'
from app.agent.llm import _models
for model in _models:
    print(getattr(model, "model_name", None), getattr(model, "openai_api_base", None))
PY
```

预期：

- 能看到 OpenRouter 模型。
- 填了 `NVIDIA_API_KEY` 后能看到 NVIDIA 模型。
- 总能看到 `qwen2.5-coder:1.5b` 作为最后回退。

## 4. Mock 的位置

`MOCK_MODE=true` 仍然保留，只用于前后端联调或外部服务不可用时的演示。真实运行请使用：

```bash
MOCK_MODE=false
```
