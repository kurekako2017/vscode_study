# OpenClaw 本地模型与自动切换教程

> 适用场景：你本地已经能跑千问、Qwen、1.5B、3B 这类模型，想接入 OpenClaw，并考虑是否能自动切模型。

---

## 1. 能不能接本地模型

可以。

你这版 OpenClaw 本地文档已经支持：

- `Ollama` 本地模型
- `vLLM` 本地模型

如果你本地是直接跑 Ollama，优先用 Ollama。

如果你本地已经提供了 OpenAI 兼容接口，优先用 vLLM。

---

## 2. 两种最常见的接法

### 2.1 Ollama

适合：

- 本机直接跑轻量模型
- Qwen 1.5B / 3B
- 想快速接入

OpenClaw 官方文档明确说明：

- 用原生 Ollama API
- 地址写 `http://127.0.0.1:11434`
- 不要加 `/v1`

最小配置示例：

```json
{
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "http://127.0.0.1:11434",
        "apiKey": "ollama-local",
        "api": "ollama"
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/qwen2.5:3b"
      }
    }
  }
}
```

WSL 里环境变量也可以加：

```bash
export OLLAMA_API_KEY="ollama-local"
```

### 2.2 vLLM

适合：

- 你本地有 `/v1/models` 和 `/v1/chat/completions`
- 已经在跑 OpenAI 兼容模型服务

最小配置示例：

```json
{
  "models": {
    "providers": {
      "vllm": {
        "baseUrl": "http://127.0.0.1:8000/v1",
        "apiKey": "vllm-local",
        "api": "openai-completions"
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "vllm/your-model-id"
      }
    }
  }
}
```

---

## 3. 本地千问最推荐的组合

如果你本地有 Qwen 1.5B 和 3B，最实用的策略是：

- 1.5B：分类、改写、短回复、简单翻译
- 3B：总结、提炼、普通问答
- 云模型：复杂推理、长文本、工具调用

也就是说，小模型负责“快”，云模型负责“稳”和“强”。

---

## 4. OpenClaw 自己能不能自动切模型

能做一部分，但不是最智能的那种“按任务难度自动分流”。

OpenClaw 原生更像这样：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/qwen2.5:3b",
        "fallbacks": [
          "ollama/qwen2.5:1.5b"
        ]
      }
    }
  }
}
```

这个 `fallbacks` 更偏向：

- 主模型失败时切换
- 主模型不可用时兜底

不是严格意义上的“自动判断任务类型后选模型”。

---

## 5. 如果你想要真正的自动切模型

建议加一层路由：

- `LiteLLM`

这类方案更适合做：

- 简单任务走本地小模型
- 复杂任务走云模型
- 统一记录成本
- 统一做 fallback

也就是说：

- OpenClaw 负责聊天入口
- LiteLLM 负责模型路由

---

## 6. 一个实用的部署思路

### 方案 A：全部本地

- `primary = ollama/qwen2.5:3b`
- `fallbacks = ["ollama/qwen2.5:1.5b"]`

优点：

- 成本低
- 响应快

缺点：

- 复杂任务能力有限

### 方案 B：云模型主力，本地模型兜底

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "gemini/gemini-2.5-flash",
        "fallbacks": [
          "ollama/qwen2.5:3b",
          "ollama/qwen2.5:1.5b"
        ]
      }
    }
  }
}
```

优点：

- 质量更稳
- 本地模型还能做备用

缺点：

- 不是按任务自动分流

### 方案 C：LiteLLM 路由

适合后续进阶：

- 简单任务走本地
- 复杂任务走云端
- 统一网关和成本控制

---

## 7. 如果你现在就想接本地千问，推荐顺序

1. 先确认本地是 Ollama 还是 vLLM
2. 先让 OpenClaw 成功调用一个本地 Qwen 模型
3. 再补 `fallbacks`
4. 最后如果有需要，再加 LiteLLM 做真正的自动切换

这个顺序最稳，不容易一次改太多导致不好排错。
