from __future__ import annotations

from typing import Any, Optional

from langchain_core.messages import AIMessage

from _compat import prompt_to_text, render_answer


class ChatOpenAI:
    def __init__(
        self,
        model: str = "offline/mock",
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any,
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = api_key
        self.base_url = base_url
        self.kwargs = kwargs

    def invoke(self, input: Any, config: Any | None = None, **kwargs: Any) -> AIMessage:
        return AIMessage(content=render_answer(prompt_to_text(input)))

    async def ainvoke(self, input: Any, config: Any | None = None, **kwargs: Any) -> AIMessage:
        return self.invoke(input, config=config, **kwargs)

    def stream(self, input: Any, config: Any | None = None, **kwargs: Any):
        yield self.invoke(input, config=config, **kwargs)

    def __call__(self, input: Any, *args: Any, **kwargs: Any) -> AIMessage:
        return self.invoke(input, *args, **kwargs)

