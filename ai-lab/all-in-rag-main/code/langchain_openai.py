"""
文件功能概述：`code/langchain_openai.py` 主要是 LangChainOpenAI，这个文件里有 1 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `ChatOpenAI`：功能概述：这个类是 `ChatOpenAI`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 model, temperature, max_tokens, api_key, base_url, **kwargs，最后把结果交给下一步或直接结束。 2. `invoke`：先接收输入参数 input, config, **kwargs，再调用 AIMessage、render_answer、prompt_to_text 等内部步骤完成主要工作，最后返回结果。 3. `ainvoke`：先接收输入参数 input, config, **kwargs，再调用 self.invoke 等内部步骤完成主要工作，最后返回结果。 4. `stream`：先接收输入参数 input, config, **kwargs，再调用 self.invoke 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 5. `__call__`：先接收输入参数 input, *args, **kwargs，再调用 self.invoke 等内部步骤完成主要工作，最后返回结果。
"""

from __future__ import annotations

from typing import Any, Optional

from langchain_core.messages import AIMessage

from _compat import prompt_to_text, render_answer
from openrouter_env import load_real_openai_class, resolve_openrouter_api_key, resolve_openrouter_base_url

DEFAULT_COMPLETION_MAX_TOKENS = 800


class ChatOpenAI:
    """
    功能概述：这个类是 `ChatOpenAI`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 model, temperature, max_tokens, api_key, base_url, **kwargs，最后把结果交给下一步或直接结束。
    2. `invoke`：先接收输入参数 input, config, **kwargs，再调用 AIMessage、render_answer、prompt_to_text 等内部步骤完成主要工作，最后返回结果。
    3. `ainvoke`：先接收输入参数 input, config, **kwargs，再调用 self.invoke 等内部步骤完成主要工作，最后返回结果。
    4. `stream`：先接收输入参数 input, config, **kwargs，再调用 self.invoke 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    5. `__call__`：先接收输入参数 input, *args, **kwargs，再调用 self.invoke 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(
        self,
        model: str = "offline/mock",
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any,
    ):  # 中文名称：初始化
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = (api_key or resolve_openrouter_api_key() or "").strip() or None
        self.base_url = (base_url or resolve_openrouter_base_url()).strip()
        self.kwargs = kwargs
        self._real_client = None

        real_openai = load_real_openai_class()
        if real_openai is not None and self.api_key:
            self._real_client = real_openai(api_key=self.api_key, base_url=self.base_url)

    def invoke(self, input: Any, config: Any | None = None, **kwargs: Any) -> AIMessage:  # 中文名称：invoke
        prompt_text = prompt_to_text(input)
        if self._real_client is not None:
            request_args: dict[str, Any] = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt_text}],
                "temperature": self.temperature,
            }
            request_args["max_tokens"] = self.max_tokens if self.max_tokens is not None else DEFAULT_COMPLETION_MAX_TOKENS
            response = self._real_client.chat.completions.create(**request_args)
            content = response.choices[0].message.content or ""
            return AIMessage(content=content)
        return AIMessage(content=render_answer(prompt_to_text(input)))

    async def ainvoke(self, input: Any, config: Any | None = None, **kwargs: Any) -> AIMessage:  # 中文名称：ainvoke
        return self.invoke(input, config=config, **kwargs)

    def stream(self, input: Any, config: Any | None = None, **kwargs: Any):  # 中文名称：stream
        yield self.invoke(input, config=config, **kwargs)

    def __call__(self, input: Any, *args: Any, **kwargs: Any) -> AIMessage:  # 中文名称：可调用执行
        return self.invoke(input, *args, **kwargs)
