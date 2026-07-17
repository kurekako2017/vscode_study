"""NVIDIA NIM OpenAI-compatible LLM Provider。

文件职责：复用 OpenAI-compatible transport，对接 NVIDIA 官方 Chat Completions。
谁调用它：仅 LLMGatewayService / ProviderChain。
设计理由：Key 只在 Authorization Header；解析 usage/model/request id。
"""

from __future__ import annotations

from pydantic import SecretStr

from app.llm.prompt_builder import PromptBuilder
from app.providers.openrouter_llm_provider import OpenRouterLLMProvider


class NVIDIALLMProvider(OpenRouterLLMProvider):
    """NVIDIA integrate.api 使用 OpenAI-compatible /chat/completions。"""

    def __init__(
        self,
        *,
        provider_name: str,
        model_name: str,
        api_key: SecretStr,
        base_url: str = "https://integrate.api.nvidia.com/v1",
        timeout_seconds: float = 20.0,
        max_retries: int = 0,
        client=None,
        transport=None,
        prompt_builder: PromptBuilder | None = None,
    ) -> None:
        super().__init__(
            provider_name=provider_name,
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
            http_referer=None,
            app_title=None,
            client=client,
            transport=transport,
            prompt_builder=prompt_builder,
        )


__all__ = ["NVIDIALLMProvider"]
