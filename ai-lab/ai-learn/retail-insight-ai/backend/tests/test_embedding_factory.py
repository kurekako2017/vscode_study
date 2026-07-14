from __future__ import annotations

import unittest
from math import inf, nan

from app.config.settings import Settings
from app.embeddings.config import EmbeddingConfig
from app.embeddings.factory import EmbeddingProviderFactory
from app.embeddings.interface import EmbeddingProvider
from app.embeddings.provider import (
    ConfiguredEmbeddingProvider,
    DeterministicTestEmbeddingProvider,
    DisabledEmbeddingProvider,
    EmbeddingExecutionDisabledError,
)
from app.embeddings.service import (
    EmbeddingProviderError,
    EmbeddingService,
    EmbeddingValidationError,
)


class EmbeddingProviderFactoryTest(unittest.TestCase):
    """验证 Provider 可统一选择，但 Phase 2A 绝不会产生向量或访问外部 API。"""

    def test_default_settings_build_disabled_provider(self) -> None:
        settings = Settings(embedding_provider="disabled", _env_file=None)

        provider = EmbeddingProviderFactory.from_settings(settings)

        self.assertIsInstance(provider, DisabledEmbeddingProvider)
        self.assertIsInstance(provider, EmbeddingProvider)
        self.assertEqual(provider.name, "disabled")

    def test_future_provider_names_share_one_foundation_contract(self) -> None:
        for provider_name in ("local", "openai", "openrouter", "nvidia"):
            with self.subTest(provider=provider_name):
                config = EmbeddingConfig(
                    provider=provider_name,
                    model=f"{provider_name}-embedding-model",
                    dimensions=384,
                )

                provider = EmbeddingProviderFactory.build(config)

                self.assertIsInstance(provider, ConfiguredEmbeddingProvider)
                self.assertIsInstance(provider, EmbeddingProvider)
                self.assertEqual(provider.name, provider_name)
                self.assertEqual(provider.model, f"{provider_name}-embedding-model")
                self.assertEqual(provider.dimensions, 384)

    def test_all_foundation_providers_fail_closed(self) -> None:
        providers = [
            EmbeddingProviderFactory.build(EmbeddingConfig()),
            EmbeddingProviderFactory.build(EmbeddingConfig(provider="local", model="local-model")),
        ]

        for provider in providers:
            with self.subTest(provider=provider.name):
                with self.assertRaises(EmbeddingExecutionDisabledError):
                    provider.embed(["向量を生成しない"])

    def test_enabled_provider_requires_model(self) -> None:
        with self.assertRaisesRegex(ValueError, "model is required"):
            EmbeddingConfig(provider="openai")

    def test_dimensions_must_be_positive(self) -> None:
        with self.assertRaisesRegex(ValueError, "must equal 384"):
            EmbeddingConfig(provider="local", model="local-model", dimensions=0)

    def test_deterministic_provider_is_stable_across_instances_and_batch(self) -> None:
        first = EmbeddingService(
            DeterministicTestEmbeddingProvider(model="deterministic-test-sha256-v1")
        )
        second = EmbeddingService(
            DeterministicTestEmbeddingProvider(model="deterministic-test-sha256-v1")
        )

        vector = first.embed_text("同じテキスト")
        batch = second.embed_batch(["同じテキスト", "別のテキスト"])

        self.assertEqual(vector, batch[0])
        self.assertEqual(len(vector), 384)
        self.assertNotEqual(batch[0], batch[1])

    def test_empty_text_and_empty_batch_are_rejected(self) -> None:
        service = EmbeddingService(DeterministicTestEmbeddingProvider())

        with self.assertRaisesRegex(EmbeddingValidationError, "must not be blank"):
            service.embed_text("   ")
        with self.assertRaisesRegex(EmbeddingValidationError, "must not be empty"):
            service.embed_batch([])

    def test_invalid_dimensions_and_non_finite_values_are_rejected(self) -> None:
        for vector in ([0.0], [0.0] * 383 + [nan], [0.0] * 383 + [inf]):
            with self.subTest(length=len(vector), tail=vector[-1]):
                provider = _StaticProvider(vector)
                with self.assertRaises(EmbeddingValidationError):
                    EmbeddingService(provider).embed_text("query")

    def test_provider_exception_is_not_swallowed(self) -> None:
        with self.assertRaisesRegex(EmbeddingProviderError, "provider 'broken' failed"):
            EmbeddingService(_BrokenProvider()).embed_text("query")


class _StaticProvider:
    name = "static-test"
    model = "static-test"
    dimensions = 384

    def __init__(self, vector: list[float]) -> None:
        self._vector = vector

    def embed_text(self, text: str) -> list[float]:
        return self._vector

    def embed_batch(self, texts) -> list[list[float]]:
        return [self._vector for _ in texts]

    def embed(self, texts) -> list[list[float]]:
        return self.embed_batch(texts)


class _BrokenProvider:
    name = "broken"
    model = "broken"
    dimensions = 384

    def embed_text(self, text: str) -> list[float]:
        raise RuntimeError("provider secret failure")

    def embed_batch(self, texts) -> list[list[float]]:
        raise RuntimeError("provider secret failure")

    def embed(self, texts) -> list[list[float]]:
        return self.embed_batch(texts)


if __name__ == "__main__":
    unittest.main()
