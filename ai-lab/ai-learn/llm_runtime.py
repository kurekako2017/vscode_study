"""Shared OpenAI-compatible provider fallback for the ai-learn examples."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any, get_args, get_origin, Literal

from openai import OpenAI


@dataclass(frozen=True)
class Provider:
    name: str
    api_key: str
    base_url: str
    model: str


class ProvidersExhausted(RuntimeError):
    """Raised after every configured real provider failed."""


def providers() -> list[Provider]:
    """Return providers in the required OpenRouter -> NVIDIA -> Ollama order."""
    result: list[Provider] = []
    openrouter_key = (os.getenv("OPENROUTER_API_KEY") or os.getenv("openRouter") or "").strip()
    if openrouter_key:
        result.append(Provider(
            "openrouter",
            openrouter_key,
            os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            os.getenv("OPENROUTER_MODEL", "openrouter/free"),
        ))

    nvidia_key = (
        os.getenv("NVIDIA_API_KEY")
        or os.getenv("NVIDIA_NIM_API_KEY")
        or os.getenv("NGC_API_KEY")
        or ""
    ).strip()
    if nvidia_key:
        result.append(Provider(
            "nvidia",
            nvidia_key,
            os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1"),
            os.getenv("NVIDIA_MODEL", "qwen/qwen2.5-coder-32b-instruct"),
        ))

    ollama_base_url = (
        os.getenv("OLLAMA_BASE_URL")
        or os.getenv("OLLAMA_API_BASE")
        or "http://127.0.0.1:11434"
    ).rstrip("/")
    if not ollama_base_url.endswith("/v1"):
        ollama_base_url += "/v1"
    result.append(Provider(
        "ollama",
        os.getenv("OLLAMA_API_KEY", "ollama"),
        ollama_base_url,
        os.getenv("OLLAMA_MODEL", "qwen2.5-coder:1.5b"),
    ))
    return result


def has_real_provider() -> bool:
    """Ollama is always a real-provider candidate, even when cloud keys are absent."""
    return True


def provider_summary() -> str:
    return " -> ".join(provider.name for provider in providers()) + " -> mock"


def _chat_tools(tools: list[dict[str, Any]] | None) -> list[dict[str, Any]] | None:
    if not tools:
        return None
    converted = []
    for tool in tools:
        if tool.get("type") == "function" and "function" not in tool:
            function = {key: value for key, value in tool.items() if key not in {"type", "strict"}}
            if "strict" in tool:
                function["strict"] = tool["strict"]
            converted.append({"type": "function", "function": function})
        else:
            converted.append(tool)
    return converted


def _messages(instructions: str | None, input_value: Any) -> list[dict[str, Any]]:
    messages: list[dict[str, Any]] = []
    if instructions:
        messages.append({"role": "system", "content": instructions})
    if isinstance(input_value, str):
        messages.append({"role": "user", "content": input_value})
        return messages
    for item in input_value:
        if item.get("type") == "function_call_output":
            messages.append({
                "role": "tool",
                "tool_call_id": item["call_id"],
                "content": item["output"],
            })
        elif item.get("role"):
            messages.append({"role": item["role"], "content": item.get("content", "")})
    return messages


def _extract_json(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    start, end = stripped.find("{"), stripped.rfind("}")
    return stripped[start:end + 1] if start >= 0 and end > start else stripped


class _ResponsesAdapter:
    def __init__(self, owner: "FallbackOpenAI") -> None:
        self.owner = owner

    def create(self, *, model: str | None = None, instructions: str | None = None,
               input: Any, tools: list[dict[str, Any]] | None = None, **_: Any) -> Any:
        return self.owner._create(model, instructions, input, tools)

    def parse(self, *, model: str | None = None, instructions: str | None = None,
              input: Any, text_format: Any, **_: Any) -> Any:
        schema = json.dumps(text_format.model_json_schema(), ensure_ascii=False)
        extra = (
            "\nReturn only valid JSON matching this JSON Schema; no markdown fences:\n" + schema
        )
        response = self.owner._create(model, (instructions or "") + extra, input, None)
        try:
            parsed = text_format.model_validate_json(_extract_json(response.output_text))
        except Exception:
            parsed = text_format(**{
                name: _mock_value(field.annotation, name)
                for name, field in text_format.model_fields.items()
            })
        response.output_parsed = parsed
        return response


class FallbackOpenAI:
    """Small Responses-like facade backed by portable chat completions."""

    def __init__(self) -> None:
        self.responses = _ResponsesAdapter(self)
        self._pending_assistant_message: dict[str, Any] | None = None

    def _create(self, requested_model: str | None, instructions: str | None,
                input_value: Any, tools: list[dict[str, Any]] | None) -> Any:
        errors: list[str] = []
        for provider in providers():
            try:
                client = OpenAI(
                    api_key=provider.api_key,
                    base_url=provider.base_url,
                    timeout=float(os.getenv("LLM_TIMEOUT_SECONDS", "45")),
                    max_retries=0,
                )
                messages = _messages(instructions, input_value)
                if self._pending_assistant_message and any(m["role"] == "tool" for m in messages):
                    tool_index = next(i for i, message in enumerate(messages) if message["role"] == "tool")
                    messages.insert(tool_index, self._pending_assistant_message)
                kwargs: dict[str, Any] = {
                    "model": provider.model,
                    "messages": messages,
                }
                converted_tools = _chat_tools(tools)
                if converted_tools:
                    kwargs["tools"] = converted_tools
                print(f"INFO: trying provider={provider.name} model={provider.model}", file=sys.stderr)
                completion = client.chat.completions.create(**kwargs)
                message = completion.choices[0].message
                output = []
                for call in message.tool_calls or []:
                    output.append(SimpleNamespace(
                        type="function_call",
                        name=call.function.name,
                        arguments=call.function.arguments,
                        call_id=call.id,
                    ))
                if message.tool_calls:
                    self._pending_assistant_message = message.model_dump(exclude_none=True)
                else:
                    self._pending_assistant_message = None
                return SimpleNamespace(output_text=message.content or "", output=output)
            except Exception as exc:
                errors.append(f"{provider.name}: {type(exc).__name__}: {exc}")
                detail = " ".join(str(exc).split())[:300]
                print(
                    f"WARNING: provider {provider.name} failed ({type(exc).__name__}: {detail}); "
                    "trying next provider",
                    file=sys.stderr,
                )
        print("WARNING: all real providers failed; using final mock fallback", file=sys.stderr)
        return SimpleNamespace(
            output_text="[MOCK MODE] All cloud and local model providers were unavailable.",
            output=[],
            provider_errors=errors,
        )


def build_fallback_client() -> FallbackOpenAI:
    return FallbackOpenAI()


def _mock_value(annotation: Any, field_name: str) -> Any:
    origin = get_origin(annotation)
    args = get_args(annotation)
    if origin is Literal:
        return args[0]
    if origin is list:
        return [f"mock {field_name}"]
    if annotation is bool:
        return False
    if annotation is int:
        return 0
    if annotation is float:
        return 0.0
    return f"[MOCK MODE] {field_name}"
