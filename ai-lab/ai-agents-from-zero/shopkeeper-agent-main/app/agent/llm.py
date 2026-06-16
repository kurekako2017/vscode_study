"""
电商问数 Agent 使用的大模型实例

集中初始化 OpenAI 兼容的 Chat Model，供节点或本地测试直接复用。
默认按 OpenRouter -> NVIDIA -> 本地 Ollama 的顺序回退。
"""

from langchain.chat_models import init_chat_model

from app.conf.app_config import app_config


def _build_openai_compatible_model(model: str, base_url: str, api_key: str):
    return init_chat_model(
        model=model,
        model_provider="openai",
        base_url=base_url,
        api_key=api_key,
        # 字段扩展、SQL 生成更看重稳定性，所以这里关闭随机发散
        temperature=0,
    )


def _configured_models():
    provider_map = {
        "openrouter": {
            "model": app_config.llm.openrouter_model_name or app_config.llm.model_name,
            "base_url": app_config.llm.openrouter_base_url or app_config.llm.base_url,
            "api_key": app_config.llm.openrouter_api_key or app_config.llm.api_key,
            "requires_key": True,
        },
        "nvidia": {
            "model": app_config.llm.nvidia_model_name,
            "base_url": app_config.llm.nvidia_base_url,
            "api_key": app_config.llm.nvidia_api_key,
            "requires_key": True,
        },
        "ollama": {
            "model": app_config.llm.ollama_model_name,
            "base_url": app_config.llm.ollama_base_url,
            "api_key": app_config.llm.ollama_api_key or "ollama",
            "requires_key": False,
        },
    }

    providers = [
        provider.strip().lower()
        for provider in app_config.llm.provider_order.split(",")
        if provider.strip()
    ]

    models = []
    for provider in providers:
        config = provider_map.get(provider)
        if not config:
            continue
        if config["requires_key"] and not config["api_key"]:
            continue
        models.append(
            _build_openai_compatible_model(
                model=config["model"],
                base_url=config["base_url"],
                api_key=config["api_key"],
            )
        )

    if not models:
        models.append(
            _build_openai_compatible_model(
                model=app_config.llm.ollama_model_name,
                base_url=app_config.llm.ollama_base_url,
                api_key=app_config.llm.ollama_api_key or "ollama",
            )
        )
    return models


_models = _configured_models()

# 节点只复用 llm，不重复初始化模型连接；主模型失败时自动尝试后续模型。
llm = _models[0].with_fallbacks(_models[1:]) if len(_models) > 1 else _models[0]

if __name__ == "__main__":
    # 本地快速验证 LLM 配置是否能正常调用
    print(llm.invoke("你好").content)
