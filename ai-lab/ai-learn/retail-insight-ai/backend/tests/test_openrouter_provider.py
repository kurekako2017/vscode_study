"""OpenRouter Provider 单元测试：MockTransport，零外网。"""

from __future__ import annotations

import json
import unittest
from decimal import Decimal
from typing import Callable

import httpx
from pydantic import SecretStr, ValidationError

from app.config.container import build_container
from app.config.settings import Settings
from app.llm.gateway import LLMGatewayService
from app.llm.model_router import ModelRouter
from app.llm.operation_policy import OperationPolicyRegistry
from app.llm.prompt_builder import PromptBuilder
from app.models.ai_analysis import (
    AIEvidence,
    LLMAnalysisInput,
    LLMProviderAuthenticationError,
    LLMProviderCitationInvalidError,
    LLMProviderModelUnavailableError,
    LLMProviderRateLimitError,
    LLMProviderResponseInvalidError,
    LLMProviderTimeoutError,
    LLMProviderUnavailableError,
    LLMReportInput,
)
from app.providers.openrouter_llm_provider import OpenRouterLLMProvider
from app.providers.stub_llm_provider import StubLLMProvider


def _evidence() -> tuple[AIEvidence, ...]:
    return (
        AIEvidence("doc-1", "chk-1", Decimal("0.9"), "Sales declined in Kanto beverages."),
    )


def _analysis_json(**overrides) -> str:
    payload = {
        "answer": "Evidence shows Kanto beverage sales declined.",
        "citations": [{"document_id": "doc-1", "chunk_id": "chk-1"}],
        "insufficient_context": False,
        "warnings": [],
    }
    payload.update(overrides)
    return json.dumps(payload)


def _report_json(**overrides) -> str:
    payload = {
        "title": "Board Report",
        "executive_summary": "Operations require attention on beverage sales.",
        "kpi_findings": ["Sales down in Kanto"],
        "risks": ["Inventory aging"],
        "recommendations": ["Review promotions"],
        "citations": [{"document_id": "doc-1", "chunk_id": "chk-1"}],
    }
    payload.update(overrides)
    return json.dumps(payload)


def _completion(
    *,
    content: str,
    model: str = "meta/low-cost-test",
    usage: dict | None = None,
    status: int = 200,
    request_id: str = "gen-1",
) -> httpx.Response:
    body = {
        "id": request_id,
        "model": model,
        "choices": [{"message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
    }
    if usage is not None:
        body["usage"] = usage
    return httpx.Response(
        status,
        headers={"content-type": "application/json"},
        json=body,
    )


class OpenRouterProviderUnitTest(unittest.TestCase):
    def _provider(
        self,
        handler: Callable[[httpx.Request], httpx.Response],
        *,
        model: str = "meta/low-cost-test",
        provider_name: str = "openrouter-low-cost",
        max_retries: int = 1,
    ) -> OpenRouterLLMProvider:
        transport = httpx.MockTransport(handler)
        return OpenRouterLLMProvider(
            provider_name=provider_name,
            model_name=model,
            api_key=SecretStr("test-key-not-real"),
            base_url="https://openrouter.example/api/v1",
            timeout_seconds=5.0,
            max_retries=max_retries,
            http_referer="https://example.local",
            app_title="ERIP Test",
            transport=transport,
        )

    def test_low_cost_analyze_maps_model_and_auth_header(self) -> None:
        seen: dict = {}

        def handler(request: httpx.Request) -> httpx.Response:
            seen["url"] = str(request.url)
            seen["auth"] = request.headers.get("Authorization")
            seen["referer"] = request.headers.get("HTTP-Referer")
            seen["title"] = request.headers.get("X-Title")
            body = json.loads(request.content.decode())
            seen["model"] = body["model"]
            seen["messages"] = body["messages"]
            return _completion(
                content=_analysis_json(),
                model="meta/low-cost-test",
                usage={"prompt_tokens": 11, "completion_tokens": 7},
            )

        provider = self._provider(handler)
        result = provider.analyze(
            LLMAnalysisInput(
                question="Why did sales drop?",
                evidence=_evidence(),
                max_output_tokens=64,
                request_id="req-1",
                timeout_seconds=5.0,
            )
        )
        self.assertEqual(seen["model"], "meta/low-cost-test")
        self.assertEqual(seen["auth"], "Bearer test-key-not-real")
        self.assertEqual(seen["referer"], "https://example.local")
        self.assertEqual(seen["title"], "ERIP Test")
        self.assertIn("/chat/completions", seen["url"])
        self.assertEqual(result.input_tokens, 11)
        self.assertEqual(result.output_tokens, 7)
        self.assertEqual(result.usage_source, "provider_reported")
        self.assertEqual(result.actual_model, "meta/low-cost-test")
        self.assertIn("declined", result.answer)
        # 安全：日志/异常不得包含 Key（这里断言请求 body 不含 Key）
        self.assertNotIn("test-key-not-real", json.dumps(seen["messages"]))

    def test_high_quality_generate_report_uses_distinct_model(self) -> None:
        seen_models: list[str] = []

        def handler(request: httpx.Request) -> httpx.Response:
            body = json.loads(request.content.decode())
            seen_models.append(body["model"])
            return _completion(
                content=_report_json(),
                model="meta/high-quality-test",
                usage={"prompt_tokens": 20, "completion_tokens": 30},
            )

        provider = self._provider(
            handler,
            model="meta/high-quality-test",
            provider_name="openrouter-high-quality",
        )
        result = provider.generate_report(
            LLMReportInput(
                title="Board",
                analysis_answer="Sales declined",
                evidence=_evidence(),
                max_output_tokens=256,
                request_id="req-2",
                timeout_seconds=5.0,
            )
        )
        self.assertEqual(seen_models, ["meta/high-quality-test"])
        self.assertEqual(result.executive_summary.startswith("Operations"), True)
        self.assertEqual(result.usage_source, "provider_reported")

    def test_missing_usage_is_marked_estimated(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            return _completion(content=_analysis_json(), usage=None)

        provider = self._provider(handler)
        result = provider.analyze(
            LLMAnalysisInput(
                question="q", evidence=_evidence(), max_output_tokens=32,
                request_id="r", timeout_seconds=5.0,
            )
        )
        self.assertEqual(result.usage_source, "estimated")
        self.assertGreater(result.input_tokens, 0)
        self.assertGreater(result.output_tokens, 0)

    def test_model_mismatch_is_rejected(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            return _completion(content=_analysis_json(), model="other/model")

        provider = self._provider(handler)
        with self.assertRaises(LLMProviderModelUnavailableError):
            provider.analyze(
                LLMAnalysisInput(
                    question="q", evidence=_evidence(), max_output_tokens=32,
                    request_id="r", timeout_seconds=5.0,
                )
            )

    def test_401_does_not_retry(self) -> None:
        calls = {"n": 0}

        def handler(request: httpx.Request) -> httpx.Response:
            calls["n"] += 1
            return httpx.Response(401, headers={"content-type": "application/json"}, json={"error": {"message": "no"}})

        provider = self._provider(handler, max_retries=1)
        with self.assertRaises(LLMProviderAuthenticationError):
            provider.analyze(
                LLMAnalysisInput(
                    question="q", evidence=_evidence(), max_output_tokens=32,
                    request_id="r", timeout_seconds=5.0,
                )
            )
        self.assertEqual(calls["n"], 1)
        self.assertEqual(provider.http_call_count, 1)

    def test_400_does_not_retry(self) -> None:
        calls = {"n": 0}

        def handler(request: httpx.Request) -> httpx.Response:
            calls["n"] += 1
            return httpx.Response(400, headers={"content-type": "application/json"}, json={"error": {"message": "bad"}})

        provider = self._provider(handler, max_retries=1)
        with self.assertRaises(LLMProviderResponseInvalidError):
            provider.analyze(
                LLMAnalysisInput(
                    question="q", evidence=_evidence(), max_output_tokens=32,
                    request_id="r", timeout_seconds=5.0,
                )
            )
        self.assertEqual(calls["n"], 1)

    def test_429_retries_once(self) -> None:
        calls = {"n": 0}

        def handler(request: httpx.Request) -> httpx.Response:
            calls["n"] += 1
            if calls["n"] == 1:
                return httpx.Response(429, headers={"content-type": "application/json"}, json={"error": {"message": "rate"}})
            return _completion(content=_analysis_json(), usage={"prompt_tokens": 1, "completion_tokens": 1})

        provider = self._provider(handler, max_retries=1)
        result = provider.analyze(
            LLMAnalysisInput(
                question="q", evidence=_evidence(), max_output_tokens=32,
                request_id="r", timeout_seconds=5.0,
            )
        )
        self.assertEqual(calls["n"], 2)
        self.assertEqual(result.input_tokens, 1)

    def test_5xx_retries_then_fails(self) -> None:
        calls = {"n": 0}

        def handler(request: httpx.Request) -> httpx.Response:
            calls["n"] += 1
            return httpx.Response(503, headers={"content-type": "application/json"}, json={"error": {"message": "down"}})

        provider = self._provider(handler, max_retries=1)
        with self.assertRaises(LLMProviderUnavailableError):
            provider.analyze(
                LLMAnalysisInput(
                    question="q", evidence=_evidence(), max_output_tokens=32,
                    request_id="r", timeout_seconds=5.0,
                )
            )
        self.assertEqual(calls["n"], 2)

    def test_invalid_json_does_not_second_paid_call(self) -> None:
        calls = {"n": 0}

        def handler(request: httpx.Request) -> httpx.Response:
            calls["n"] += 1
            return _completion(content="not-json-at-all")

        provider = self._provider(handler, max_retries=1)
        with self.assertRaises(LLMProviderResponseInvalidError):
            provider.analyze(
                LLMAnalysisInput(
                    question="q", evidence=_evidence(), max_output_tokens=32,
                    request_id="r", timeout_seconds=5.0,
                )
            )
        self.assertEqual(calls["n"], 1)

    def test_invalid_citation_rejected(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            return _completion(
                content=_analysis_json(citations=[{"document_id": "doc-x", "chunk_id": "chk-x"}]),
                usage={"prompt_tokens": 1, "completion_tokens": 1},
            )

        provider = self._provider(handler)
        with self.assertRaises(LLMProviderCitationInvalidError):
            provider.analyze(
                LLMAnalysisInput(
                    question="q", evidence=_evidence(), max_output_tokens=32,
                    request_id="r", timeout_seconds=5.0,
                )
            )

    def test_prompt_builder_does_not_embed_secrets(self) -> None:
        prompt = PromptBuilder().build_analysis(
            LLMAnalysisInput(
                question="q", evidence=_evidence(), max_output_tokens=32,
                request_id="r", timeout_seconds=5.0,
            )
        )
        blob = prompt.system + prompt.user
        self.assertNotIn("Bearer", blob)
        self.assertNotIn("OPENROUTER", blob)
        self.assertIn("<EVIDENCE", prompt.user)


class OpenRouterSettingsAndRoutingTest(unittest.TestCase):
    def test_default_mode_is_stub(self) -> None:
        settings = Settings(_env_file=None)
        self.assertEqual(settings.llm_provider_mode, "stub")
        self.assertEqual(settings.llm_low_cost_provider_alias, "stub-low-cost")
        self.assertFalse(settings.openrouter_api_key_configured())

    def test_unknown_mode_fail_closed(self) -> None:
        with self.assertRaises(ValidationError):
            Settings(llm_provider_mode="nvidia", _env_file=None)  # type: ignore[arg-type]

    def test_openrouter_missing_key_fail_closed(self) -> None:
        with self.assertRaises(ValidationError):
            Settings(
                llm_provider_mode="openrouter",
                openrouter_low_cost_model="a/low",
                openrouter_high_quality_model="a/high",
                _env_file=None,
            )

    def test_openrouter_mode_maps_models_and_prices(self) -> None:
        settings = Settings(
            llm_provider_mode="openrouter",
            openrouter_api_key=SecretStr("configured-but-not-printed"),
            openrouter_low_cost_model="vendor/low",
            openrouter_high_quality_model="vendor/high",
            openrouter_low_input_price=Decimal("0.1"),
            openrouter_low_output_price=Decimal("0.2"),
            openrouter_high_input_price=Decimal("1.1"),
            openrouter_high_output_price=Decimal("2.2"),
            _env_file=None,
        )
        self.assertEqual(settings.llm_low_cost_provider_alias, "openrouter-low-cost")
        self.assertEqual(settings.llm_high_quality_provider_alias, "openrouter-high-quality")
        self.assertEqual(settings.llm_low_cost_model_name, "vendor/low")
        self.assertEqual(settings.llm_high_quality_model_name, "vendor/high")
        self.assertEqual(settings.llm_input_price_per_million, Decimal("0.1"))
        self.assertEqual(settings.llm_hq_output_price_per_million, Decimal("2.2"))
        self.assertTrue(settings.openrouter_api_key_configured())
        registry = OperationPolicyRegistry(settings)
        low = registry.get("ai_analysis")
        high = registry.get("executive_report")
        self.assertEqual(low.model_name, "vendor/low")
        self.assertEqual(high.model_name, "vendor/high")
        self.assertEqual(low.route_tier, "low_cost")
        self.assertEqual(high.route_tier, "high_quality")

    def test_gateway_routes_do_not_cross_stub_providers(self) -> None:
        settings = Settings(_env_file=None)
        low = StubLLMProvider(provider_name="stub-low-cost", model_name="stub-low-cost-v1")
        high = StubLLMProvider(provider_name="stub-high-quality", model_name="stub-high-quality-v1")
        registry = OperationPolicyRegistry(settings)
        router = ModelRouter(
            policy_registry=registry,
            providers_by_alias={
                "stub-low-cost": low,
                "stub-high-quality": high,
            },
        )
        gateway = LLMGatewayService(policy_registry=registry, model_router=router)
        gateway.analyze(
            operation="ai_analysis",
            request=LLMAnalysisInput(
                question="q", evidence=_evidence(), max_output_tokens=32,
                request_id="r", timeout_seconds=5.0,
            ),
        )
        self.assertEqual(low.analyze_call_count, 1)
        self.assertEqual(high.generate_report_call_count, 0)
        gateway.generate_report(
            operation="executive_report",
            request=LLMReportInput(
                title="t", analysis_answer="a", evidence=_evidence(),
                max_output_tokens=64, request_id="r2", timeout_seconds=5.0,
            ),
        )
        self.assertEqual(high.generate_report_call_count, 1)
        self.assertEqual(low.generate_report_call_count, 0)

    def test_stub_container_has_zero_http_clients_on_providers(self) -> None:
        container = build_container(Settings(log_level="CRITICAL", _env_file=None))
        self.assertIsInstance(container.llm_provider, StubLLMProvider)
        self.assertIsInstance(container.llm_provider_high_quality, StubLLMProvider)
        self.assertFalse(hasattr(container.llm_provider, "http_call_count") and container.llm_provider.http_call_count)  # type: ignore[attr-defined]

    def test_openrouter_container_builds_two_providers_without_network(self) -> None:
        settings = Settings(
            llm_provider_mode="openrouter",
            openrouter_api_key=SecretStr("configured-but-not-printed"),
            openrouter_low_cost_model="vendor/low",
            openrouter_high_quality_model="vendor/high",
            repository_backend="inmemory",
            log_level="CRITICAL",
            _env_file=None,
        )
        container = build_container(settings)
        self.assertIsInstance(container.llm_provider, OpenRouterLLMProvider)
        self.assertIsInstance(container.llm_provider_high_quality, OpenRouterLLMProvider)
        self.assertEqual(container.llm_provider.model_name, "vendor/low")
        self.assertEqual(container.llm_provider_high_quality.model_name, "vendor/high")
        # 未调用前 HTTP 计数为 0；默认 RAG 仍禁用 Provider。
        self.assertEqual(container.llm_provider.http_call_count, 0)
        self.assertEqual(container.llm_provider_high_quality.http_call_count, 0)
        self.assertIsNone(container.rag_answer_generator._provider)  # type: ignore[attr-defined]


class OpenRouterTimeoutRetryTest(unittest.TestCase):
    def test_timeout_retries_once(self) -> None:
        calls = {"n": 0}

        def handler(request: httpx.Request) -> httpx.Response:
            calls["n"] += 1
            if calls["n"] == 1:
                raise httpx.ReadTimeout("slow")
            return _completion(
                content=_analysis_json(),
                usage={"prompt_tokens": 2, "completion_tokens": 3},
            )

        transport = httpx.MockTransport(handler)
        provider = OpenRouterLLMProvider(
            provider_name="openrouter-low-cost",
            model_name="meta/low-cost-test",
            api_key=SecretStr("test-key-not-real"),
            base_url="https://openrouter.example/api/v1",
            max_retries=1,
            transport=transport,
        )
        result = provider.analyze(
            LLMAnalysisInput(
                question="q", evidence=_evidence(), max_output_tokens=32,
                request_id="r", timeout_seconds=5.0,
            )
        )
        self.assertEqual(calls["n"], 2)
        self.assertEqual(result.output_tokens, 3)

    def test_timeout_exhaustion(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            raise httpx.ReadTimeout("slow")

        provider = OpenRouterLLMProvider(
            provider_name="openrouter-low-cost",
            model_name="meta/low-cost-test",
            api_key=SecretStr("test-key-not-real"),
            max_retries=1,
            transport=httpx.MockTransport(handler),
        )
        with self.assertRaises(LLMProviderTimeoutError):
            provider.analyze(
                LLMAnalysisInput(
                    question="q", evidence=_evidence(), max_output_tokens=32,
                    request_id="r", timeout_seconds=5.0,
                )
            )


if __name__ == "__main__":
    unittest.main()
