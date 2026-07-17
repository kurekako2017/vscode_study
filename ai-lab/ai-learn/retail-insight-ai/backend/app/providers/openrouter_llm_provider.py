"""OpenRouter LLM Provider：第一个真实 Provider 实现。

文件职责：通过 OpenRouter Chat Completions 实现 analyze / generate_report。
谁调用它：仅 LLMGatewayService（经 ModelRouter）。
它调用谁：httpx Client（可注入 MockTransport）、PromptBuilder、response_parser。
设计理由：API Key 只在 Authorization Header；不记 Prompt/正文/Key；有限重试。
日本现场面试：真实调用仍必须经过 Gateway、Evidence、Quota、幂等、Ledger、Audit。
"""

from __future__ import annotations

import logging
from time import monotonic, sleep
from typing import Any
from uuid import uuid4

import httpx
from pydantic import SecretStr

from app.llm.prompt_builder import BuiltPrompt, PromptBuilder
from app.llm.response_parser import (
    extract_json_object,
    parse_analysis_payload,
    parse_report_payload,
)
from app.models.ai_analysis import (
    LLMAnalysisInput,
    LLMProviderAuthenticationError,
    LLMProviderCitationInvalidError,
    LLMProviderModelUnavailableError,
    LLMProviderPartialFailureError,
    LLMProviderRateLimitError,
    LLMProviderResponseInvalidError,
    LLMProviderResult,
    LLMProviderTimeoutError,
    LLMProviderUnavailableError,
    LLMReportInput,
    LLMReportResult,
)
from app.models.internal_rag import LLMUsageMetrics, RAGPromptContext
from app.providers.llm_provider import LLMProviderOutput

logger = logging.getLogger(__name__)

_MAX_RESPONSE_BYTES = 512_000
_RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class OpenRouterLLMProvider:
    """OpenRouter 兼容 Chat Completions 的可替换 Provider。"""

    def __init__(
        self,
        *,
        provider_name: str,
        model_name: str,
        api_key: SecretStr,
        base_url: str = "https://openrouter.ai/api/v1",
        timeout_seconds: float = 30.0,
        max_retries: int = 1,
        http_referer: str | None = None,
        app_title: str | None = None,
        client: httpx.Client | None = None,
        transport: httpx.BaseTransport | None = None,
        prompt_builder: PromptBuilder | None = None,
    ) -> None:
        if not model_name.strip():
            raise ValueError("OpenRouter model_name is required")
        self.provider_name = provider_name
        self.model_name = model_name
        self.name = provider_name
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._max_retries = max(0, min(max_retries, 2))
        self._http_referer = http_referer
        self._app_title = app_title
        self._prompt_builder = prompt_builder or PromptBuilder()
        self._owns_client = client is None
        if client is not None:
            self._client = client
        else:
            timeout = httpx.Timeout(
                timeout_seconds,
                connect=min(10.0, timeout_seconds),
                read=timeout_seconds,
                write=min(10.0, timeout_seconds),
            )
            self._client = httpx.Client(
                base_url=self._base_url,
                timeout=timeout,
                transport=transport,
                headers=self._static_headers(),
            )
        self.call_count = 0
        self.analyze_call_count = 0
        self.generate_report_call_count = 0
        self.http_call_count = 0

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def analyze(self, request: LLMAnalysisInput) -> LLMProviderResult:
        self.call_count += 1
        self.analyze_call_count += 1
        prompt = self._prompt_builder.build_analysis(request)
        started = monotonic()
        raw = self._chat_completion(
            prompt=prompt,
            max_output_tokens=request.max_output_tokens,
            request_id=request.request_id,
            timeout_seconds=request.timeout_seconds,
        )
        latency_ms = max(1, int((monotonic() - started) * 1000))
        content = raw["content"]
        try:
            payload = extract_json_object(content)
            answer, insufficient, warnings = parse_analysis_payload(payload, evidence=request.evidence)
        except (LLMProviderResponseInvalidError, LLMProviderCitationInvalidError):
            raise
        except Exception as exc:
            raise LLMProviderResponseInvalidError("analysis payload invalid") from exc

        input_tokens, output_tokens, usage_source = self._resolve_usage(
            raw.get("usage"),
            prompt_chars=prompt.char_count,
            completion_text=content,
        )
        actual_model = raw.get("model")
        self._assert_model_match(actual_model)
        return LLMProviderResult(
            answer=answer,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            provider_request_id=raw.get("provider_request_id") or f"or-{uuid4().hex}",
            finish_reason=raw.get("finish_reason") or "stop",
            usage_source=usage_source,
            actual_model=actual_model if isinstance(actual_model, str) else None,
            warnings=warnings,
            insufficient_context=insufficient,
        )

    def generate_report(self, request: LLMReportInput) -> LLMReportResult:
        self.call_count += 1
        self.generate_report_call_count += 1
        prompt = self._prompt_builder.build_report(request)
        started = monotonic()
        raw = self._chat_completion(
            prompt=prompt,
            max_output_tokens=request.max_output_tokens,
            request_id=request.request_id,
            timeout_seconds=request.timeout_seconds,
        )
        latency_ms = max(1, int((monotonic() - started) * 1000))
        content = raw["content"]
        try:
            payload = extract_json_object(content)
            _title, summary, kpi, risks, recommendations, markdown = parse_report_payload(
                payload, evidence=request.evidence
            )
        except (LLMProviderResponseInvalidError, LLMProviderCitationInvalidError):
            raise
        except Exception as exc:
            raise LLMProviderResponseInvalidError("report payload invalid") from exc

        input_tokens, output_tokens, usage_source = self._resolve_usage(
            raw.get("usage"),
            prompt_chars=prompt.char_count,
            completion_text=content,
        )
        actual_model = raw.get("model")
        self._assert_model_match(actual_model)
        return LLMReportResult(
            executive_summary=summary,
            kpi_findings=kpi,
            risks=risks,
            recommendations=recommendations,
            markdown=markdown,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            provider_request_id=raw.get("provider_request_id") or f"or-report-{uuid4().hex}",
            finish_reason=raw.get("finish_reason") or "stop",
            usage_source=usage_source,
            actual_model=actual_model if isinstance(actual_model, str) else None,
        )

    def generate(self, context: RAGPromptContext) -> LLMProviderOutput:
        """普通 RAG 不得进入 Gateway；此方法保留协议形状并拒绝隐式调用。"""

        raise RuntimeError("OpenRouter generate() is disabled for ordinary RAG paths")

    def _chat_completion(
        self,
        *,
        prompt: BuiltPrompt,
        max_output_tokens: int,
        request_id: str,
        timeout_seconds: float,
    ) -> dict[str, Any]:
        body = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": prompt.system},
                {"role": "user", "content": prompt.user},
            ],
            "max_tokens": max_output_tokens,
            "temperature": 0,
            "response_format": {"type": "json_object"},
        }
        headers = {
            "Authorization": f"Bearer {self._api_key.get_secret_value()}",
            "Content-Type": "application/json",
            "X-Request-ID": request_id,
        }
        if self._http_referer:
            headers["HTTP-Referer"] = self._http_referer
        if self._app_title:
            headers["X-Title"] = self._app_title

        attempts = self._max_retries + 1
        last_error: Exception | None = None
        for attempt in range(attempts):
            try:
                self.http_call_count += 1
                response = self._client.post(
                    "/chat/completions",
                    json=body,
                    headers=headers,
                    timeout=timeout_seconds,
                )
                return self._parse_http_response(response)
            except (
                LLMProviderAuthenticationError,
                LLMProviderModelUnavailableError,
                LLMProviderResponseInvalidError,
            ):
                raise
            except LLMProviderRateLimitError as exc:
                last_error = exc
                if attempt + 1 >= attempts:
                    raise
                sleep(0.05 * (attempt + 1))
            except LLMProviderTimeoutError as exc:
                last_error = exc
                if attempt + 1 >= attempts:
                    raise
                sleep(0.05 * (attempt + 1))
            except LLMProviderUnavailableError as exc:
                last_error = exc
                if attempt + 1 >= attempts:
                    raise
                sleep(0.05 * (attempt + 1))
            except httpx.TimeoutException as exc:
                last_error = LLMProviderTimeoutError("openrouter timeout")
                if attempt + 1 >= attempts:
                    raise last_error from exc
                sleep(0.05 * (attempt + 1))
            except httpx.TransportError as exc:
                last_error = LLMProviderUnavailableError("openrouter transport error")
                if attempt + 1 >= attempts:
                    raise last_error from exc
                sleep(0.05 * (attempt + 1))
        assert last_error is not None
        raise last_error

    def _parse_http_response(self, response: httpx.Response) -> dict[str, Any]:
        status = response.status_code
        # 绝不把 Authorization 或响应全文写入日志。
        logger.info(
            "openrouter_http_response",
            extra={
                "event": "openrouter_http_response",
                "status": status,
                "provider": self.provider_name,
                "model": self.model_name,
                "content_length": len(response.content or b""),
            },
        )
        if status in {401, 403}:
            raise LLMProviderAuthenticationError("openrouter authentication failed")
        if status == 404:
            raise LLMProviderModelUnavailableError("openrouter model unavailable")
        if status == 429:
            raise LLMProviderRateLimitError("openrouter rate limited")
        if status == 400:
            # 参数/模型/token 类错误：不可重试。
            detail = self._safe_error_category(response)
            if "model" in detail:
                raise LLMProviderModelUnavailableError("openrouter model error")
            raise LLMProviderResponseInvalidError("openrouter bad request")
        if status >= 500:
            raise LLMProviderUnavailableError("openrouter server error")
        if status >= 400:
            raise LLMProviderUnavailableError("openrouter request failed")

        content_type = (response.headers.get("content-type") or "").lower()
        if "application/json" not in content_type:
            raise LLMProviderResponseInvalidError("unexpected content-type")
        if len(response.content or b"") > _MAX_RESPONSE_BYTES:
            raise LLMProviderResponseInvalidError("provider response too large")

        try:
            payload = response.json()
        except ValueError as exc:
            raise LLMProviderResponseInvalidError("provider body is not JSON") from exc
        if not isinstance(payload, dict):
            raise LLMProviderResponseInvalidError("provider body root invalid")

        # OpenRouter 错误体可能仍是 200 外的结构；严格解析 choices。
        if payload.get("error"):
            message = str(payload["error"].get("message", "")) if isinstance(payload["error"], dict) else ""
            lowered = message.lower()
            if "rate" in lowered:
                raise LLMProviderRateLimitError("openrouter rate limited")
            if "model" in lowered:
                raise LLMProviderModelUnavailableError("openrouter model error")
            raise LLMProviderUnavailableError("openrouter error payload")

        choices = payload.get("choices")
        if not isinstance(choices, list) or not choices:
            raise LLMProviderResponseInvalidError("missing choices")
        first = choices[0]
        if not isinstance(first, dict):
            raise LLMProviderResponseInvalidError("invalid choice")
        message = first.get("message") or {}
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, str) or not content.strip():
            # 部分失败：若有 usage 仍要记账。
            usage = payload.get("usage") if isinstance(payload.get("usage"), dict) else {}
            prompt_tokens = int(usage.get("prompt_tokens") or 0)
            completion_tokens = int(usage.get("completion_tokens") or 0)
            if prompt_tokens or completion_tokens:
                raise LLMProviderPartialFailureError(
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    latency_ms=1,
                )
            raise LLMProviderResponseInvalidError("empty completion content")

        return {
            "content": content,
            "model": payload.get("model"),
            "usage": payload.get("usage") if isinstance(payload.get("usage"), dict) else None,
            "provider_request_id": str(payload.get("id") or uuid4().hex),
            "finish_reason": str(first.get("finish_reason") or "stop"),
        }

    def _resolve_usage(
        self, usage: dict[str, Any] | None, *, prompt_chars: int, completion_text: str
    ) -> tuple[int, int, str]:
        if isinstance(usage, dict):
            prompt_tokens = usage.get("prompt_tokens")
            completion_tokens = usage.get("completion_tokens")
            if prompt_tokens is not None and completion_tokens is not None:
                return max(0, int(prompt_tokens)), max(0, int(completion_tokens)), "provider_reported"
        # 缺失 usage 时不得伪造精确值：用本地估算并标记 estimated。
        input_tokens = max(1, (prompt_chars + 3) // 4)
        output_tokens = max(1, (len(completion_text) + 3) // 4)
        return input_tokens, output_tokens, "estimated"

    def _assert_model_match(self, actual_model: Any) -> None:
        if actual_model is None or actual_model == "":
            return
        if not isinstance(actual_model, str):
            raise LLMProviderModelUnavailableError("provider returned non-string model")
        if actual_model.strip() != self.model_name.strip():
            # 不允许静默换模型后仍按原模型记账。
            raise LLMProviderModelUnavailableError("provider returned unexpected model")

    def _static_headers(self) -> dict[str, str]:
        headers = {"Accept": "application/json"}
        if self._http_referer:
            headers["HTTP-Referer"] = self._http_referer
        if self._app_title:
            headers["X-Title"] = self._app_title
        return headers

    def _safe_error_category(self, response: httpx.Response) -> str:
        try:
            payload = response.json()
            if isinstance(payload, dict) and isinstance(payload.get("error"), dict):
                return str(payload["error"].get("message") or "").lower()
        except Exception:
            return ""
        return ""


__all__ = ["OpenRouterLLMProvider"]
