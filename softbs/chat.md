name: Local Continue Config
version: 1.0.0
schema: v1

models:
  # ===== 1. 本地模型 (Ollama) =====
  - name: "Local-Qwen-7B"
    provider: ollama
    model: qwen2.5-coder:7b

  # ===== 2. DeepSeek (通过 OpenRouter) =====
  - name: "DeepSeek"
    provider: openai
    model: deepseek/deepseek-chat
    apiBase: https://openrouter.ai/api/v1
    apiKey: sk-or-v1-bd97ab8835e52b9c21a9aeb7949ee3428b72def

    {
      "title": "Local-Qwen-7B",
      "provider": "ollama",
      "model": "qwen2.5-coder:7b"
    }


    
chatModels:
  - name: "Gemini 1.5 Flash"
    provider: google-generative-ai
    model: gemini-1.5-flash
    apiKey: ${AIzaSyDkSS59wKRnCsq9iprKwHlivUDJeXgLnCM}

 