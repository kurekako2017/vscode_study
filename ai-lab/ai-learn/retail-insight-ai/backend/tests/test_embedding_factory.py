from __future__ import annotations

import unittest

from app.config.settings import Settings
from app.embeddings.config import EmbeddingConfig
from app.embeddings.factory import EmbeddingProviderFactory
from app.embeddings.interface import EmbeddingProvider
from app.embeddings.provider import (
    ConfiguredEmbeddingProvider,
    DisabledEmbeddingProvider,
    EmbeddingExecutionDisabledError,
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
        with self.assertRaisesRegex(ValueError, "greater than zero"):
            EmbeddingConfig(provider="local", model="local-model", dimensions=0)


if __name__ == "__main__":
    unittest.main()
