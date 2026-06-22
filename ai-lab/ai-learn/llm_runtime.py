"""所有真实 LLM 示例共用的模型回退运行时。

初学者可以把本文件理解成一个“模型插座”：上层示例只调用 Responses 风格接口，
这里负责按 OpenRouter -> NVIDIA -> Ollama -> Mock 的顺序寻找可用实现。
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any, Literal, get_args, get_origin

from openai import OpenAI


@dataclass(frozen=True)
class Provider:
    """一次模型连接所需的提供商名称、凭据、地址和实际模型名。"""

    name: str
    api_key: str
    base_url: str
    model: str


class ProvidersExhausted(RuntimeError):
    """Raised after every configured real provider failed."""


def providers() -> list[Provider]:
    """读取环境变量，并按固定回退顺序返回可尝试的提供商。"""
    result: list[Provider] = []
    # 云端 provider 只有配置 Key 后才加入列表，避免发送必然失败的请求。
    openrouter_key = (
        os.getenv("OPENROUTER_API_KEY") or os.getenv("openRouter") or ""
    ).strip()
    if openrouter_key:
        result.append(
            Provider(
                "openrouter",
                openrouter_key,
                os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
                os.getenv("OPENROUTER_MODEL", "openrouter/free"),
            )
        )

    nvidia_key = (
        os.getenv("NVIDIA_API_KEY")
        or os.getenv("NVIDIA_NIM_API_KEY")
        or os.getenv("NGC_API_KEY")
        or ""
    ).strip()
    if nvidia_key:
        result.append(
            Provider(
                "nvidia",
                nvidia_key,
                os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1"),
                os.getenv("NVIDIA_MODEL", "qwen/qwen2.5-coder-32b-instruct"),
            )
        )

    ollama_base_url = (
        os.getenv("OLLAMA_BASE_URL")
        or os.getenv("OLLAMA_API_BASE")
        or "http://127.0.0.1:11434"
    ).rstrip("/")
    if not ollama_base_url.endswith("/v1"):
        # OpenAI SDK 需要兼容接口的 /v1 路径。
        ollama_base_url += "/v1"
    result.append(
        Provider(
            "ollama",
            os.getenv("OLLAMA_API_KEY", "ollama"),
            ollama_base_url,
            os.getenv("OLLAMA_MODEL", "qwen2.5-coder:1.5b"),
        )
    )
    return result


def has_real_provider() -> bool:
    """返回是否存在真实候选；本项目始终把本地 Ollama 视为候选。"""
    return True


def provider_summary() -> str:
    """生成用于文档或日志展示的回退顺序。"""
    return " -> ".join(provider.name for provider in providers()) + " -> mock"


def _chat_tools(tools: list[dict[str, Any]] | None) -> list[dict[str, Any]] | None:
    """把 Responses 风格工具定义转换为 Chat Completions 的 function 包装格式。"""
    if not tools:
        return None
    converted = []
    for tool in tools:
        # 已经包含 function 的工具无需再次包装。
        if tool.get("type") == "function" and "function" not in tool:
            function = {
                key: value
                for key, value in tool.items()
                if key not in {"type", "strict"}
            }
            if "strict" in tool:
                function["strict"] = tool["strict"]
            converted.append({"type": "function", "function": function})
        else:
            converted.append(tool)
    return converted


def _messages(instructions: str | None, input_value: Any) -> list[dict[str, Any]]:
    """把上层输入转换为 Chat Completions 接受的 messages 列表。"""
    messages: list[dict[str, Any]] = []
    if instructions:
        messages.append({"role": "system", "content": instructions})
    if isinstance(input_value, str):
        # 最常见的一次性问答：system + user 两条消息。
        messages.append({"role": "user", "content": input_value})
        return messages
    for item in input_value:
        if item.get("type") == "function_call_output":
            # 工具执行结果必须带原 call_id，模型才能对应到之前的工具请求。
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": item["call_id"],
                    "content": item["output"],
                }
            )
        elif item.get("role"):
            messages.append({"role": item["role"], "content": item.get("content", "")})
    return messages


def _extract_json(text: str) -> str:
    """去除 Markdown 代码围栏，并截取最外层 JSON 对象。"""
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    start, end = stripped.find("{"), stripped.rfind("}")
    return stripped[start : end + 1] if start >= 0 and end > start else stripped


class _ResponsesAdapter:
    """提供 create/parse 两个教学示例需要的 Responses 风格方法。"""

    def __init__(self, owner: "FallbackOpenAI") -> None:
        self.owner = owner

    def create(
        self,
        *,
        model: str | None = None,
        instructions: str | None = None,
        input: Any,
        tools: list[dict[str, Any]] | None = None,
        **_: Any,
    ) -> Any:
        """把普通文本请求交给统一的 provider 回退逻辑。"""
        return self.owner._create(model, instructions, input, tools)

    def parse(
        self,
        *,
        model: str | None = None,
        instructions: str | None = None,
        input: Any,
        text_format: Any,
        **_: Any,
    ) -> Any:
        """要求模型返回指定 Pydantic schema，并把 JSON 校验为对象。"""
        schema = json.dumps(text_format.model_json_schema(), ensure_ascii=False)
        extra = (
            "\nReturn only valid JSON matching this JSON Schema; no markdown fences:\n"
            + schema
        )
        response = self.owner._create(model, (instructions or "") + extra, input, None)
        try:
            parsed = text_format.model_validate_json(
                _extract_json(response.output_text)
            )
        except Exception:
            # 教学环境中的最终 Mock 可能没有合法 JSON，因此构造类型正确的占位值。
            parsed = text_format(
                **{
                    name: _mock_value(field.annotation, name)
                    for name, field in text_format.model_fields.items()
                }
            )
        response.output_parsed = parsed
        return response


class FallbackOpenAI:
    """Small Responses-like facade backed by portable chat completions."""

    def __init__(self) -> None:
        # responses 让上层代码保持接近 OpenAI Responses API 的调用形式。
        self.responses = _ResponsesAdapter(self)
        self._pending_assistant_message: dict[str, Any] | None = None

    def _create(
        self,
        requested_model: str | None,
        instructions: str | None,
        input_value: Any,
        tools: list[dict[str, Any]] | None,
    ) -> Any:
        """逐个尝试 provider；成功立即返回，全部失败才生成 Mock 响应。"""
        # requested_model 是上层展示的逻辑模型名；实际模型由每个 provider 的环境变量决定。
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
                if self._pending_assistant_message and any(
                    m["role"] == "tool" for m in messages
                ):
                    # 第二轮工具调用必须补回模型上一轮发出的 assistant tool_call 消息。
                    tool_index = next(
                        i
                        for i, message in enumerate(messages)
                        if message["role"] == "tool"
                    )
                    messages.insert(tool_index, self._pending_assistant_message)
                kwargs: dict[str, Any] = {
                    "model": provider.model,
                    "messages": messages,
                }
                converted_tools = _chat_tools(tools)
                if converted_tools:
                    kwargs["tools"] = converted_tools
                print(
                    f"INFO: trying provider={provider.name} model={provider.model}",
                    file=sys.stderr,
                )
                completion = client.chat.completions.create(**kwargs)
                message = completion.choices[0].message
                output = []
                for call in message.tool_calls or []:
                    # SimpleNamespace 模拟上层示例读取的 Responses function_call 属性。
                    output.append(
                        SimpleNamespace(
                            type="function_call",
                            name=call.function.name,
                            arguments=call.function.arguments,
                            call_id=call.id,
                        )
                    )
                if message.tool_calls:
                    self._pending_assistant_message = message.model_dump(
                        exclude_none=True
                    )
                else:
                    self._pending_assistant_message = None
                # “trying” 只表示尝试过；这一行明确告诉学习者最终真正使用了哪个模型。
                print(
                    f"MODEL: provider={provider.name} model={provider.model} mode=real",
                    file=sys.stderr,
                )
                return SimpleNamespace(output_text=message.content or "", output=output)
            except Exception as exc:
                # 单个 provider 失败不终止程序，记录原因后继续尝试下一个。
                errors.append(f"{provider.name}: {type(exc).__name__}: {exc}")
                detail = " ".join(str(exc).split())[:300]
                print(
                    f"WARNING: provider {provider.name} failed ({type(exc).__name__}: {detail}); "
                    "trying next provider",
                    file=sys.stderr,
                )
        print(
            "WARNING: all real providers failed; using final mock fallback",
            file=sys.stderr,
        )
        print("MODEL: provider=local model=mock mode=mock", file=sys.stderr)
        return SimpleNamespace(
            output_text="[MOCK MODE] All cloud and local model providers were unavailable.",
            output=[],
            provider_errors=errors,
        )


# 通用函数：获取指定类型的值，如果不存在则返回默认值
def build_fallback_client() -> FallbackOpenAI:
    """创建供各示例复用的轻量客户端。"""
    return FallbackOpenAI()


def _mock_value(annotation: Any, field_name: str) -> Any:
    """根据 Pydantic 字段类型构造最小 Mock 值，保证结构化示例仍可运行。"""
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
