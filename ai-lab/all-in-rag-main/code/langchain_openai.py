"""
文件功能概述：`code/langchain_openai.py` 主要是 LangChainOpenAI，这个文件里有 1 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `ChatOpenAI`：功能概述：这个类是 `ChatOpenAI`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 model, temperature, max_tokens, api_key, base_url, **kwargs，最后把结果交给下一步或直接结束。 2. `invoke`：先接收输入参数 input, config, **kwargs，再调用 AIMessage、render_answer、prompt_to_text 等内部步骤完成主要工作，最后返回结果。 3. `ainvoke`：先接收输入参数 input, config, **kwargs，再调用 self.invoke 等内部步骤完成主要工作，最后返回结果。 4. `stream`：先接收输入参数 input, config, **kwargs，再调用 self.invoke 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 5. `__call__`：先接收输入参数 input, *args, **kwargs，再调用 self.invoke 等内部步骤完成主要工作，最后返回结果。
"""

from __future__ import annotations

from typing import Any, Optional

from langchain_core.messages import AIMessage

from _compat import prompt_to_text, render_answer


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
        self.api_key = api_key
        self.base_url = base_url
        self.kwargs = kwargs

    def invoke(self, input: Any, config: Any | None = None, **kwargs: Any) -> AIMessage:  # 中文名称：invoke
        return AIMessage(content=render_answer(prompt_to_text(input)))

    async def ainvoke(self, input: Any, config: Any | None = None, **kwargs: Any) -> AIMessage:  # 中文名称：ainvoke
        return self.invoke(input, config=config, **kwargs)

    def stream(self, input: Any, config: Any | None = None, **kwargs: Any):  # 中文名称：stream
        yield self.invoke(input, config=config, **kwargs)

    def __call__(self, input: Any, *args: Any, **kwargs: Any) -> AIMessage:  # 中文名称：可调用执行
        return self.invoke(input, *args, **kwargs)

