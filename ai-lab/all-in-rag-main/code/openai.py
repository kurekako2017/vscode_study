"""
文件功能概述：`code/openai.py` 主要是 OpenAI，这个文件里有 3 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `_ChatCompletions`：功能概述：这个类是 `_ChatCompletions`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `create`：先接收输入参数 model, messages, tools, tool_choice, **kwargs，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 join、render_answer、any 等内部步骤完成主要工作，最后返回结果。
2. 类 `_Chat`：功能概述：这个类是 `_Chat`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先进入当前步骤，再调用 _ChatCompletions 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
3. 类 `OpenAI`：功能概述：这个类是 `OpenAI`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 api_key, base_url，再调用 _Chat 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from _compat import render_answer
from openrouter_env import load_real_openai_class, resolve_openrouter_api_key, resolve_openrouter_base_url

DEFAULT_COMPLETION_MAX_TOKENS = 800


class _ChatCompletions:
    """
    功能概述：这个类是 `_ChatCompletions`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `create`：先接收输入参数 model, messages, tools, tool_choice, **kwargs，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 join、render_answer、any 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, real_client: Any = None):  # 中文名称：初始化
        self._real_client = real_client

    def create(self, model: str, messages: list[dict[str, Any]], tools: Any = None, tool_choice: Any = None, **kwargs: Any):  # 中文名称：创建
        if self._real_client is not None:
            request_args = {
                "model": model,
                "messages": messages,
                **kwargs,
            }
            request_args.setdefault("max_tokens", DEFAULT_COMPLETION_MAX_TOKENS)
            if tools is not None:
                request_args["tools"] = tools
            if tool_choice is not None:
                request_args["tool_choice"] = tool_choice
            return self._real_client.chat.completions.create(**request_args)

        def _content(message: Any) -> str:  # 中文名称：content
            if isinstance(message, dict):
                return str(message.get("content", ""))
            return str(getattr(message, "content", ""))

        prompt = "\n".join(_content(message) for message in messages)
        content = render_answer(prompt)
        if any((isinstance(message, dict) and message.get("role") == "tool") or getattr(message, "role", None) == "tool" for message in messages):
            tool_result = ""
            for message in reversed(messages):
                if (isinstance(message, dict) and message.get("role") == "tool") or getattr(message, "role", None) == "tool":
                    tool_result = _content(message)
                    break
            message = SimpleNamespace(content=f"根据工具结果，答案是：{tool_result}", tool_calls=None)
            return SimpleNamespace(choices=[SimpleNamespace(message=message)])
        if tools:
            tool_call = SimpleNamespace(
                id="offline-tool-call",
                function=SimpleNamespace(name=tools[0]["function"]["name"], arguments='{"location":"杭州"}'),
            )
            message = SimpleNamespace(content=None, tool_calls=[tool_call])
            return SimpleNamespace(choices=[SimpleNamespace(message=message)])
        message = SimpleNamespace(content=content, tool_calls=None)
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


class _Chat:
    """
    功能概述：这个类是 `_Chat`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先进入当前步骤，再调用 _ChatCompletions 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    """
    def __init__(self, real_client: Any = None):  # 中文名称：初始化
        self.completions = _ChatCompletions(real_client=real_client)


class OpenAI:
    """
    功能概述：这个类是 `OpenAI`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 api_key, base_url，再调用 _Chat 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    """
    def __init__(self, api_key: str | None = None, base_url: str | None = None):  # 中文名称：初始化
        self.api_key = (api_key or resolve_openrouter_api_key() or "").strip() or None
        self.base_url = (base_url or resolve_openrouter_base_url()).strip()
        self._real_client = None

        real_openai = load_real_openai_class()
        if real_openai is not None and self.api_key:
            self._real_client = real_openai(api_key=self.api_key, base_url=self.base_url)

        self.chat = _Chat(real_client=self._real_client)
        self.models = getattr(self._real_client, "models", None)

    def __getattr__(self, name: str):
        if self._real_client is not None:
            return getattr(self._real_client, name)
        raise AttributeError(name)
