from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any, Iterable, Optional

from _compat import render_answer


class _ChatCompletions:
    def create(self, model: str, messages: list[dict[str, Any]], tools: Any = None, tool_choice: Any = None, **kwargs: Any):
        def _content(message: Any) -> str:
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
    def __init__(self):
        self.completions = _ChatCompletions()


class OpenAI:
    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        self.api_key = api_key
        self.base_url = base_url
        self.chat = _Chat()
