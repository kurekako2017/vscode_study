"""
文件功能概述：`code/openai.py` 主要是 OpenAI，这个文件里有 3 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `_ChatCompletions`：功能概述：这个类是 `_ChatCompletions`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `create`：先接收输入参数 model, messages, tools, tool_choice, **kwargs，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 join、render_answer、any 等内部步骤完成主要工作，最后返回结果。
2. 类 `_Chat`：功能概述：这个类是 `_Chat`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先进入当前步骤，再调用 _ChatCompletions 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
3. 类 `OpenAI`：功能概述：这个类是 `OpenAI`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 api_key, base_url，再调用 _Chat 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
"""

from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any, Iterable, Optional

from _compat import render_answer


class _ChatCompletions:
    """
    功能概述：这个类是 `_ChatCompletions`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `create`：先接收输入参数 model, messages, tools, tool_choice, **kwargs，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 join、render_answer、any 等内部步骤完成主要工作，最后返回结果。
    """
    def create(self, model: str, messages: list[dict[str, Any]], tools: Any = None, tool_choice: Any = None, **kwargs: Any):  # 中文名称：创建
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
    def __init__(self):  # 中文名称：初始化
        self.completions = _ChatCompletions()


class OpenAI:
    """
    功能概述：这个类是 `OpenAI`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 api_key, base_url，再调用 _Chat 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    """
    def __init__(self, api_key: str | None = None, base_url: str | None = None):  # 中文名称：初始化
        self.api_key = api_key
        self.base_url = base_url
        self.chat = _Chat()
