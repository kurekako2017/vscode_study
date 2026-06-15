"""
大模型初始化模块

负责从 .env 中读取模型配置，并创建项目统一复用的模型对象
后续主智能体和子智能体都从这里导入 model，避免在多个文件里重复加载环境变量
"""

import os

from dotenv import find_dotenv, load_dotenv
from langchain.chat_models import init_chat_model

from app.runtime_config import apply_openai_compatible_env, resolve_llm_config

# find_dotenv 会从当前目录向上查找 .env，适合脚本和 Web 服务从不同入口启动的场景
load_dotenv(find_dotenv())

def build_llm_model(provider: str | None = None):
    """Build an OpenAI-compatible chat model for the requested provider."""
    llm_config = resolve_llm_config(provider)
    apply_openai_compatible_env(llm_config, override=True)

    if provider is not None and not llm_config.get("configured"):
        missing = ", ".join(llm_config.get("missing", [])) or "unknown"
        raise ValueError(f"LLM provider {provider} config incomplete: {missing}")

    resolved_model_name = str(
        llm_config.get("model") or os.getenv("LLM_QWEN_MAX") or "openai/gpt-4o-mini"
    )
    max_completion_tokens = int(os.getenv("LLM_MAX_COMPLETION_TOKENS", "1024"))

    return init_chat_model(
        model=resolved_model_name,
        model_provider="openai",
        max_completion_tokens=max_completion_tokens,
    )


# 默认使用当前环境解析出的 provider 构建模型
model = build_llm_model()
