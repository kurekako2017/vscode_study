"""Google Gemini LLM Provider。

文件职责：通过 Gemini generateContent API 实现 analyze / generate_report。
谁调用它：仅 LLMGatewayService / ProviderChain。
它调用谁：httpx、PromptBuilder、response_parser。
设计理由：API Key 仅后端 Header/query 使用；不泄露到日志、Frontend 或 URL 审计。
日本现场面试：Gemini 也必须走 Gateway、Evidence、Quota、Ledger、Audit。
"""

from __future__ import annotations

import logging
from time import monotonic
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


class GeminiLLMProvider:
    """Gemini generateContent 合同的可替换 Provider。"""

    def __init__(
        self,
        *,
        provider_name: str,
        model_name: str,
        api_key: SecretStr,
        base_url: str = "https://generativelanguage.googleapis.com/v1beta",
        timeout_seconds: float = 20.0,
        client: httpx.Client | None = None,
        transport: httpx.BaseTransport | None = None,
        prompt_builder: PromptBuilder | None = None,
    ) -> None:
        if not model_name.strip():
            raise ValueError("Gemini model_name is required")
        self.provider_name = provider_name
        self.model_name = model_name
        self.name = provider_name
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
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
                headers={"Accept": "application/json"},
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
        raw = self._generate_content(
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
        return LLMProviderResult(
            answer=answer,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            provider_request_id=raw.get("provider_request_id") or f"gem-{uuid4().hex}",
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
        raw = self._generate_content(
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
        return LLMReportResult(
            executive_summary=summary,
            kpi_findings=kpi,
            risks=risks,
            recommendations=recommendations,
            markdown=markdown,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            provider_request_id=raw.get("provider_request_id") or f"gem-report-{uuid4().hex}",
            finish_reason=raw.get("finish_reason") or "stop",
            usage_source=usage_source,
            actual_model=actual_model if isinstance(actual_model, str) else None,
        )

    def generate(self, context: RAGPromptContext) -> LLMProviderOutput:
        raise RuntimeError("Gemini generate() is disabled for ordinary RAG paths")

    def _generate_content(
        self,
        *,
        prompt: BuiltPrompt,
        max_output_tokens: int,
        request_id: str,
        timeout_seconds: float,
    ) -> dict[str, Any]:
        # 模型路径只使用配置模型名；Key 仅放在 Header，避免进入可审计 URL。
        path = f"/models/{self.model_name}:generateContent"
        body = {
            "systemInstruction": {"parts": [{"text": prompt.system}]},
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt.user}],
                }
            ],
            "generationConfig": {
                "temperature": 0,
                "maxOutputTokens": max_output_tokens,
                "responseMimeType": "application/json",
            },
        }
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self._api_key.get_secret_value(),
            "X-Request-ID": request_id,
        }
        try:
            self.http_call_count += 1
            response = self._client.post(path, json=body, headers=headers, timeout=timeout_seconds)
            return self._parse_http_response(response)
        except (
            LLMProviderAuthenticationError,
            LLMProviderModelUnavailableError,
            LLMProviderResponseInvalidError,
            LLMProviderRateLimitError,
            LLMProviderUnavailableError,
            LLMProviderPartialFailureError,
        ):
            raise
        except httpx.TimeoutException as exc:
            raise LLMProviderTimeoutError("gemini timeout") from exc
        except httpx.TransportError as exc:
            raise LLMProviderUnavailableError("gemini transport error") from exc

    def _parse_http_response(self, response: httpx.Response) -> dict[str, Any]:
        status = response.status_code
        logger.info(
            "gemini_http_response",
            extra={
                "event": "gemini_http_response",
                "status": status,
                "provider": self.provider_name,
                "model": self.model_name,
                "content_length": len(response.content or b""),
            },
        )
        if status in {401, 403}:
            raise LLMProviderAuthenticationError("gemini authentication failed")
        if status == 404:
            raise LLMProviderModelUnavailableError("gemini model unavailable")
        if status == 429:
            raise LLMProviderRateLimitError("gemini rate limited")
        if status == 400:
            raise LLMProviderModelUnavailableError("gemini bad request or model error")
        if status >= 500:
            raise LLMProviderUnavailableError("gemini server error")
        if status >= 400:
            raise LLMProviderUnavailableError("gemini request failed")
        if len(response.content or b"") > _MAX_RESPONSE_BYTES:
            raise LLMProviderResponseInvalidError("provider response too large")
        try:
            payload = response.json()
        except ValueError as exc:
            raise LLMProviderResponseInvalidError("provider body is not JSON") from exc
        if not isinstance(payload, dict):
            raise LLMProviderResponseInvalidError("provider body root invalid")

        # candidates[0].content.parts[].text
        candidates = payload.get("candidates")
        if not isinstance(candidates, list) or not candidates:
            raise LLMProviderResponseInvalidError("missing candidates")
        first = candidates[0]
        if not isinstance(first, dict):
            raise LLMProviderResponseInvalidError("invalid candidate")
        content_obj = first.get("content") or {}
        parts = content_obj.get("parts") if isinstance(content_obj, dict) else None
        text_parts: list[str] = []
        if isinstance(parts, list):
            for part in parts:
                if isinstance(part, dict) and isinstance(part.get("text"), str):
                    text_parts.append(part["text"])
        content = "\n".join(text_parts).strip()
        usage_meta = payload.get("usageMetadata") if isinstance(payload.get("usageMetadata"), dict) else None
        if not content:
            prompt_tokens = int((usage_meta or {}).get("promptTokenCount") or 0)
            completion_tokens = int((usage_meta or {}).get("candidatesTokenCount") or 0)
            if prompt_tokens or completion_tokens:
                raise LLMProviderPartialFailureError(
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    latency_ms=1,
                )
            raise LLMProviderResponseInvalidError("empty gemini content")

        finish = first.get("finishReason") or "STOP"
        model_version = payload.get("modelVersion") or self.model_name
        return {
            "content": content,
            "model": model_version if isinstance(model_version, str) else self.model_name,
            "usage": usage_meta,
            "provider_request_id": str(payload.get("responseId") or uuid4().hex),
            "finish_reason": str(finish).lower(),
        }

    def _resolve_usage(
        self, usage: dict[str, Any] | None, *, prompt_chars: int, completion_text: str
    ) -> tuple[int, int, str]:
        if isinstance(usage, dict):
            prompt_tokens = usage.get("promptTokenCount")
            completion_tokens = usage.get("candidatesTokenCount")
            if prompt_tokens is not None and completion_tokens is not None:
                return max(0, int(prompt_tokens)), max(0, int(completion_tokens)), "provider_reported"
        input_tokens = max(1, (prompt_chars + 3) // 4)
        output_tokens = max(1, (len(completion_text) + 3) // 4)
        return input_tokens, output_tokens, "estimated"


__all__ = ["GeminiLLMProvider"]
