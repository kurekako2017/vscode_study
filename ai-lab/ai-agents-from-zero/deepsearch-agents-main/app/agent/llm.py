"""
大模型初始化模块

负责从 .env 中读取模型配置，并创建项目统一复用的模型对象
后续主智能体和子智能体都从这里导入 model，避免在多个文件里重复加载环境变量
"""

import os

from dotenv import find_dotenv, load_dotenv
from langchain.chat_models import init_chat_model

# find_dotenv 会从当前目录向上查找 .env，适合脚本和 Web 服务从不同入口启动的场景
load_dotenv(find_dotenv())

# 兼容 OpenAI / OpenRouter 两种环境变量命名：
# 1. 优先使用标准 OpenAI 变量
# 2. 如果只有 OpenRouter 变量，则自动映射到 OpenAI 兼容变量
if not os.getenv("OPENAI_API_KEY") and os.getenv("OPENROUTER_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY", "")

if not os.getenv("OPENAI_BASE_URL") and os.getenv("OPENROUTER_BASE_URL"):
    os.environ["OPENAI_BASE_URL"] = os.getenv("OPENROUTER_BASE_URL", "")

# 具体模型名优先读取环境变量；如果没有配置，先用一个默认值保证服务可以启动
resolved_model_name = (
    os.getenv("LLM_QWEN_MAX")
    or os.getenv("OPENAI_MODEL")
    or os.getenv("OPENROUTER_MODEL")
    or "gpt-4o-mini"
)

# 使用 OpenAI 兼容协议接入模型；具体模型名由上面的 resolved_model_name 控制
model = init_chat_model(
    model=resolved_model_name,
    model_provider="openai",
)
