"""Provider Fallback Chain 单元测试：固定顺序、串行、MockTransport、零外网。"""

from __future__ import annotations

import json
import unittest
from decimal import Decimal
from uuid import uuid4

import httpx
from pydantic import SecretStr

from app.llm.attempt_models import (
    ProviderChainExhaustedError,
    ProviderChainQuotaStopError,
)
from app.llm.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    ControllableClock,
    InMemoryCircuitBreakerStore,
)
from app.llm.provider_chain import BoundProvider, ChainContext, ProviderChain
from app.llm.provider_registry import ProviderEndpointConfig
from app.models.ai_analysis import AIEvidence, LLMAnalysisInput, LLMProviderTimeoutError
from app.providers.gemini_llm_provider import GeminiLLMProvider
from app.providers.local_qwen_llm_provider import LocalQwenLLMProvider
from app.providers.nvidia_llm_provider import NVIDIALLMProvider
from app.providers.openrouter_llm_provider import OpenRouterLLMProvider
from app.providers.stub_llm_provider import StubLLMProvider


def _evidence() -> tuple[AIEvidence, ...]:
    return (
        AIEvidence(document_id="doc-1", chunk_id="chunk-1", score=Decimal("0.9"), excerpt="Sales declined in Q2."),
    )


def _analysis_json() -> str:
    return json.dumps(
        {
            "answer": "Sales declined due to weather.",
            "citations": [{"document_id": "doc-1", "chunk_id": "chunk-1"}],
            "insufficient_context": False,
            "warnings": [],
        }
    )


def _completion(*, content: str, model: str, usage=None) -> httpx.Response:
    body = {
        "id": f"chatcmpl-{uuid4().hex[:8]}",
        "model": model,
        "choices": [{"message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
        "usage": usage if usage is not None else {"prompt_tokens": 10, "completion_tokens": 5},
    }
    return httpx.Response(200, json=body)


def _endpoint(
    name: str,
    *,
    low: str,
    high: str,
    timeout: float = 2.0,
) -> ProviderEndpointConfig:
    return ProviderEndpointConfig(
        name=name,  # type: ignore[arg-type]
        enabled=True,
        base_url="https://example.invalid/v1",
        api_key=SecretStr("test-key"),
        low_cost_model=low,
        high_quality_model=high,
        low_input_price_per_million=Decimal("1"),
        low_output_price_per_million=Decimal("2"),
        high_input_price_per_million=Decimal("3"),
        high_output_price_per_million=Decimal("6"),
        attempt_timeout_seconds=timeout,
        requires_api_key=True,
        max_retries=0,
    )


def _openai_provider(name: str, model: str, handler) -> OpenRouterLLMProvider | NVIDIALLMProvider | LocalQwenLLMProvider:
    transport = httpx.MockTransport(handler)
    if name == "openrouter":
        return OpenRouterLLMProvider(
            provider_name="openrouter",
            model_name=model,
            api_key=SecretStr("k"),
            base_url="https://openrouter.invalid/v1",
            timeout_seconds=2.0,
            max_retries=0,
            transport=transport,
        )
    if name == "nvidia":
        return NVIDIALLMProvider(
            provider_name="nvidia",
            model_name=model,
            api_key=SecretStr("k"),
            base_url="https://nvidia.invalid/v1",
            timeout_seconds=2.0,
            max_retries=0,
            transport=transport,
        )
    return LocalQwenLLMProvider(
        provider_name="local_qwen",
        model_name=model,
        base_url="http://127.0.0.1:9/v1",
        api_key=SecretStr("k"),
        timeout_seconds=2.0,
        max_retries=0,
        transport=transport,
    )


def _gemini_provider(model: str, handler) -> GeminiLLMProvider:
    return GeminiLLMProvider(
        provider_name="gemini",
        model_name=model,
        api_key=SecretStr("k"),
        base_url="https://gemini.invalid/v1beta",
        timeout_seconds=2.0,
        transport=httpx.MockTransport(handler),
    )


def _context(**kwargs) -> ChainContext:
    base = dict(
        usage_id="llm-test",
        request_id="req-1",
        idempotency_key="idem-1",
        operation="ai_analysis",
        route_tier="low_cost",
        currency="USD",
        total_timeout_seconds=30.0,
        max_provider_attempts=4,
        estimated_input_tokens=20,
        max_output_tokens=64,
    )
    base.update(kwargs)
    return ChainContext(**base)  # type: ignore[arg-type]


class ProviderFallbackChainTest(unittest.TestCase):
    def test_fixed_order_and_stop_on_first_success(self) -> None:
        calls: list[str] = []

        def or_handler(request: httpx.Request) -> httpx.Response:
            calls.append("openrouter")
            return _completion(content=_analysis_json(), model="openrouter-low-test")

        def nv_handler(request: httpx.Request) -> httpx.Response:
            calls.append("nvidia")
            return _completion(content=_analysis_json(), model="nvidia-low-test")

        chain = ProviderChain(
            providers=[
                BoundProvider(
                    _endpoint("openrouter", low="openrouter-low-test", high="openrouter-high-test"),
                    _openai_provider("openrouter", "openrouter-low-test", or_handler),
                    "openrouter-low-test",
                    "low_cost",
                ),
                BoundProvider(
                    _endpoint("nvidia", low="nvidia-low-test", high="nvidia-high-test"),
                    _openai_provider("nvidia", "nvidia-low-test", nv_handler),
                    "nvidia-low-test",
                    "low_cost",
                ),
            ]
        )
        outcome = chain.analyze(
            LLMAnalysisInput(
                question="Why?",
                evidence=_evidence(),
                max_output_tokens=64,
                request_id="r1",
                timeout_seconds=2.0,
            ),
            _context(),
        )
        self.assertEqual(calls, ["openrouter"])
        self.assertEqual(outcome.provider_name, "openrouter")
        self.assertFalse(outcome.fallback_used)
        self.assertEqual(outcome.attempt_count, 1)

    def test_timeout_falls_back_to_nvidia(self) -> None:
        calls: list[str] = []

        def or_handler(request: httpx.Request) -> httpx.Response:
            calls.append("openrouter")
            raise httpx.ReadTimeout("slow")

        def nv_handler(request: httpx.Request) -> httpx.Response:
            calls.append("nvidia")
            return _completion(content=_analysis_json(), model="nvidia-low-test")

        chain = ProviderChain(
            providers=[
                BoundProvider(
                    _endpoint("openrouter", low="openrouter-low-test", high="openrouter-high-test"),
                    _openai_provider("openrouter", "openrouter-low-test", or_handler),
                    "openrouter-low-test",
                    "low_cost",
                ),
                BoundProvider(
                    _endpoint("nvidia", low="nvidia-low-test", high="nvidia-high-test"),
                    _openai_provider("nvidia", "nvidia-low-test", nv_handler),
                    "nvidia-low-test",
                    "low_cost",
                ),
            ]
        )
        outcome = chain.analyze(
            LLMAnalysisInput(
                question="Why?",
                evidence=_evidence(),
                max_output_tokens=64,
                request_id="r1",
                timeout_seconds=2.0,
            ),
            _context(),
        )
        self.assertEqual(calls, ["openrouter", "nvidia"])
        self.assertEqual(outcome.provider_name, "nvidia")
        self.assertTrue(outcome.fallback_used)
        self.assertEqual(outcome.attempt_count, 2)
        self.assertEqual(outcome.attempted_providers[0].status, "timed_out")
        self.assertEqual(outcome.attempted_providers[1].status, "succeeded")
        # timeout charge_possible 计入 total cost
        self.assertGreater(outcome.total_actual_cost, Decimal("0"))

    def test_full_chain_openrouter_nvidia_gemini_qwen(self) -> None:
        calls: list[str] = []

        def fail_timeout(name: str):
            def handler(request: httpx.Request) -> httpx.Response:
                calls.append(name)
                raise httpx.ReadTimeout("slow")

            return handler

        def qwen_ok(request: httpx.Request) -> httpx.Response:
            calls.append("local_qwen")
            return _completion(content=_analysis_json(), model="qwen-low-test")

        def gemini_fail(request: httpx.Request) -> httpx.Response:
            calls.append("gemini")
            return httpx.Response(503, json={"error": {"message": "unavailable"}})

        chain = ProviderChain(
            providers=[
                BoundProvider(
                    _endpoint("openrouter", low="openrouter-low-test", high="openrouter-high-test"),
                    _openai_provider("openrouter", "openrouter-low-test", fail_timeout("openrouter")),
                    "openrouter-low-test",
                    "low_cost",
                ),
                BoundProvider(
                    _endpoint("nvidia", low="nvidia-low-test", high="nvidia-high-test"),
                    _openai_provider("nvidia", "nvidia-low-test", fail_timeout("nvidia")),
                    "nvidia-low-test",
                    "low_cost",
                ),
                BoundProvider(
                    _endpoint("gemini", low="gemini-low-test", high="gemini-high-test"),
                    _gemini_provider("gemini-low-test", gemini_fail),
                    "gemini-low-test",
                    "low_cost",
                ),
                BoundProvider(
                    _endpoint("local_qwen", low="qwen-low-test", high="qwen-high-test"),
                    _openai_provider("local_qwen", "qwen-low-test", qwen_ok),
                    "qwen-low-test",
                    "low_cost",
                ),
            ]
        )
        outcome = chain.analyze(
            LLMAnalysisInput(
                question="Why?",
                evidence=_evidence(),
                max_output_tokens=64,
                request_id="r1",
                timeout_seconds=2.0,
            ),
            _context(),
        )
        self.assertEqual(calls, ["openrouter", "nvidia", "gemini", "local_qwen"])
        self.assertEqual(outcome.provider_name, "local_qwen")
        self.assertTrue(outcome.fallback_used)
        self.assertEqual(outcome.attempt_count, 4)

    def test_all_fail_returns_exhausted(self) -> None:
        def fail(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("down")

        chain = ProviderChain(
            providers=[
                BoundProvider(
                    _endpoint("openrouter", low="openrouter-low-test", high="openrouter-high-test"),
                    _openai_provider("openrouter", "openrouter-low-test", fail),
                    "openrouter-low-test",
                    "low_cost",
                ),
            ]
        )
        with self.assertRaises(ProviderChainExhaustedError) as ctx:
            chain.analyze(
                LLMAnalysisInput(
                    question="Why?",
                    evidence=_evidence(),
                    max_output_tokens=64,
                    request_id="r1",
                    timeout_seconds=2.0,
                ),
                _context(),
            )
        self.assertEqual(ctx.exception.failure.attempt_count, 1)

    def test_429_and_5xx_trigger_fallback(self) -> None:
        calls: list[str] = []

        def or_handler(request: httpx.Request) -> httpx.Response:
            calls.append("openrouter")
            return httpx.Response(429, json={"error": {"message": "rate"}})

        def nv_handler(request: httpx.Request) -> httpx.Response:
            calls.append("nvidia")
            return httpx.Response(503, json={"error": {"message": "busy"}})

        def gem_handler(request: httpx.Request) -> httpx.Response:
            calls.append("gemini")
            return httpx.Response(
                200,
                json={
                    "candidates": [{"content": {"parts": [{"text": _analysis_json()}]}, "finishReason": "STOP"}],
                    "usageMetadata": {"promptTokenCount": 8, "candidatesTokenCount": 4},
                    "modelVersion": "gemini-low-test",
                    "responseId": "gem-1",
                },
            )

        chain = ProviderChain(
            providers=[
                BoundProvider(
                    _endpoint("openrouter", low="openrouter-low-test", high="openrouter-high-test"),
                    _openai_provider("openrouter", "openrouter-low-test", or_handler),
                    "openrouter-low-test",
                    "low_cost",
                ),
                BoundProvider(
                    _endpoint("nvidia", low="nvidia-low-test", high="nvidia-high-test"),
                    _openai_provider("nvidia", "nvidia-low-test", nv_handler),
                    "nvidia-low-test",
                    "low_cost",
                ),
                BoundProvider(
                    _endpoint("gemini", low="gemini-low-test", high="gemini-high-test"),
                    _gemini_provider("gemini-low-test", gem_handler),
                    "gemini-low-test",
                    "low_cost",
                ),
            ]
        )
        outcome = chain.analyze(
            LLMAnalysisInput(
                question="Why?",
                evidence=_evidence(),
                max_output_tokens=64,
                request_id="r1",
                timeout_seconds=2.0,
            ),
            _context(),
        )
        self.assertEqual(calls, ["openrouter", "nvidia", "gemini"])
        self.assertEqual(outcome.provider_name, "gemini")
        self.assertEqual(outcome.attempted_providers[0].status, "rate_limited")
        self.assertEqual(outcome.attempted_providers[1].status, "unavailable")

    def test_auth_config_records_and_falls_back(self) -> None:
        def or_handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(401, json={"error": {"message": "bad key"}})

        def nv_handler(request: httpx.Request) -> httpx.Response:
            return _completion(content=_analysis_json(), model="nvidia-low-test")

        chain = ProviderChain(
            providers=[
                BoundProvider(
                    _endpoint("openrouter", low="openrouter-low-test", high="openrouter-high-test"),
                    _openai_provider("openrouter", "openrouter-low-test", or_handler),
                    "openrouter-low-test",
                    "low_cost",
                ),
                BoundProvider(
                    _endpoint("nvidia", low="nvidia-low-test", high="nvidia-high-test"),
                    _openai_provider("nvidia", "nvidia-low-test", nv_handler),
                    "nvidia-low-test",
                    "low_cost",
                ),
            ]
        )
        outcome = chain.analyze(
            LLMAnalysisInput(
                question="Why?",
                evidence=_evidence(),
                max_output_tokens=64,
                request_id="r1",
                timeout_seconds=2.0,
            ),
            _context(),
        )
        self.assertEqual(outcome.provider_name, "nvidia")
        self.assertEqual(outcome.attempts[0].status, "configuration_error")
        self.assertEqual(outcome.attempts[0].error_category, "authentication")

    def test_quota_stop_before_next_provider(self) -> None:
        def or_handler(request: httpx.Request) -> httpx.Response:
            raise httpx.ReadTimeout("slow")

        def nv_handler(request: httpx.Request) -> httpx.Response:
            raise AssertionError("nvidia must not be called")

        chain = ProviderChain(
            providers=[
                BoundProvider(
                    _endpoint("openrouter", low="openrouter-low-test", high="openrouter-high-test"),
                    _openai_provider("openrouter", "openrouter-low-test", or_handler),
                    "openrouter-low-test",
                    "low_cost",
                ),
                BoundProvider(
                    _endpoint("nvidia", low="nvidia-low-test", high="nvidia-high-test"),
                    _openai_provider("nvidia", "nvidia-low-test", nv_handler),
                    "nvidia-low-test",
                    "low_cost",
                ),
            ]
        )
        # 第一次 attempt 允许；第二次拒绝
        afford_calls = {"n": 0}

        def can_afford(cost: Decimal) -> bool:
            afford_calls["n"] += 1
            return afford_calls["n"] == 1

        with self.assertRaises(ProviderChainQuotaStopError):
            chain.analyze(
                LLMAnalysisInput(
                    question="Why?",
                    evidence=_evidence(),
                    max_output_tokens=64,
                    request_id="r1",
                    timeout_seconds=2.0,
                ),
                _context(can_afford=can_afford),
            )

    def test_circuit_open_skips_without_charge_attempt(self) -> None:
        clock = ControllableClock()
        store = InMemoryCircuitBreakerStore()
        breaker = CircuitBreaker(
            store=store,
            config=CircuitBreakerConfig(failure_threshold=1, open_duration_seconds=30, half_open_probe_limit=1),
            clock=clock,
        )
        # 先让 openrouter 失败一次打开熔断
        breaker.record_failure("openrouter")
        self.assertEqual(store.get("openrouter").state, "open")

        calls: list[str] = []

        def or_handler(request: httpx.Request) -> httpx.Response:
            calls.append("openrouter")
            return _completion(content=_analysis_json(), model="openrouter-low-test")

        def nv_handler(request: httpx.Request) -> httpx.Response:
            calls.append("nvidia")
            return _completion(content=_analysis_json(), model="nvidia-low-test")

        chain = ProviderChain(
            providers=[
                BoundProvider(
                    _endpoint("openrouter", low="openrouter-low-test", high="openrouter-high-test"),
                    _openai_provider("openrouter", "openrouter-low-test", or_handler),
                    "openrouter-low-test",
                    "low_cost",
                ),
                BoundProvider(
                    _endpoint("nvidia", low="nvidia-low-test", high="nvidia-high-test"),
                    _openai_provider("nvidia", "nvidia-low-test", nv_handler),
                    "nvidia-low-test",
                    "low_cost",
                ),
            ],
            circuit_breaker=breaker,
        )
        outcome = chain.analyze(
            LLMAnalysisInput(
                question="Why?",
                evidence=_evidence(),
                max_output_tokens=64,
                request_id="r1",
                timeout_seconds=2.0,
            ),
            _context(),
        )
        self.assertEqual(calls, ["nvidia"])
        self.assertEqual(outcome.provider_name, "nvidia")
        self.assertTrue(any(s.status == "skipped_circuit_open" for s in outcome.attempted_providers))
        # skipped 不进入 attempts 账本（无收费）
        self.assertEqual(len(outcome.attempts), 1)

    def test_circuit_half_open_without_sleep(self) -> None:
        clock = ControllableClock()
        store = InMemoryCircuitBreakerStore()
        breaker = CircuitBreaker(
            store=store,
            config=CircuitBreakerConfig(failure_threshold=1, open_duration_seconds=10, half_open_probe_limit=1),
            clock=clock,
        )
        breaker.record_failure("openrouter")
        self.assertEqual(store.get("openrouter").state, "open")
        clock.advance(11)
        allowed, reason = breaker.allow_request("openrouter")
        self.assertTrue(allowed)
        self.assertEqual(reason, "half_open_probe")
        self.assertEqual(store.get("openrouter").state, "half_open")
        breaker.record_success("openrouter")
        self.assertEqual(store.get("openrouter").state, "closed")

    def test_chain_rejects_out_of_order_providers(self) -> None:
        with self.assertRaises(ValueError):
            ProviderChain(
                providers=[
                    BoundProvider(
                        _endpoint("nvidia", low="nvidia-low-test", high="nvidia-high-test"),
                        StubLLMProvider(provider_name="nvidia", model_name="nvidia-low-test"),
                        "nvidia-low-test",
                        "low_cost",
                    ),
                    BoundProvider(
                        _endpoint("openrouter", low="openrouter-low-test", high="openrouter-high-test"),
                        StubLLMProvider(provider_name="openrouter", model_name="openrouter-low-test"),
                        "openrouter-low-test",
                        "low_cost",
                    ),
                ]
            )

    def test_low_high_models_do_not_cross(self) -> None:
        seen: list[str] = []

        def handler(request: httpx.Request) -> httpx.Response:
            body = json.loads(request.content.decode())
            seen.append(body["model"])
            return _completion(content=_analysis_json(), model=body["model"])

        low = BoundProvider(
            _endpoint("openrouter", low="openrouter-low-test", high="openrouter-high-test"),
            _openai_provider("openrouter", "openrouter-low-test", handler),
            "openrouter-low-test",
            "low_cost",
        )
        high = BoundProvider(
            _endpoint("openrouter", low="openrouter-low-test", high="openrouter-high-test"),
            _openai_provider("openrouter", "openrouter-high-test", handler),
            "openrouter-high-test",
            "high_quality",
        )
        ProviderChain(providers=[low]).analyze(
            LLMAnalysisInput(
                question="q", evidence=_evidence(), max_output_tokens=16,
                request_id="r", timeout_seconds=2.0,
            ),
            _context(route_tier="low_cost"),
        )
        self.assertEqual(seen, ["openrouter-low-test"])


if __name__ == "__main__":
    unittest.main()
