"""Local Qwen OpenAI-compatible LLM Provider。

文件职责：调用配置的本地 OpenAI-compatible endpoint（如 vLLM/Ollama 兼容层）。
谁调用它：仅 LLMGatewayService / ProviderChain。
禁止：自动下载模型、启动系统服务、向外部网络发送 Local 请求。
设计理由：Local 仍必须经过 Gateway、Evidence、Quota、Ledger、Audit。
"""

from __future__ import annotations

from pydantic import SecretStr

from app.llm.prompt_builder import PromptBuilder
from app.providers.openrouter_llm_provider import OpenRouterLLMProvider


class LocalQwenLLMProvider(OpenRouterLLMProvider):
    """本地 OpenAI-compatible endpoint；API Key 可选。"""

    def __init__(
        self,
        *,
        provider_name: str,
        model_name: str,
        base_url: str,
        api_key: SecretStr | None = None,
        timeout_seconds: float = 60.0,
        max_retries: int = 0,
        client=None,
        transport=None,
        prompt_builder: PromptBuilder | None = None,
    ) -> None:
        # 本地无 Key 时使用占位 Secret，不发送到外部网络（base_url 必须指向本地）。
        secret = api_key if api_key is not None else SecretStr("local-no-key")
        super().__init__(
            provider_name=provider_name,
            model_name=model_name,
            api_key=secret,
            base_url=base_url,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
            http_referer=None,
            app_title=None,
            client=client,
            transport=transport,
            prompt_builder=prompt_builder,
        )


__all__ = ["LocalQwenLLMProvider"]
