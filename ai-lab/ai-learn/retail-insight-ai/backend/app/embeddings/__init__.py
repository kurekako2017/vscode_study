"""Embedding Contract、Provider 与统一验证服务的对外入口。"""

from app.embeddings.config import EMBEDDING_DIMENSIONS, EmbeddingConfig, EmbeddingProviderName
from app.embeddings.factory import EmbeddingProviderFactory
from app.embeddings.interface import EmbeddingProvider
from app.embeddings.provider import (
    ConfiguredEmbeddingProvider,
    DeterministicTestEmbeddingProvider,
    DisabledEmbeddingProvider,
    EmbeddingExecutionDisabledError,
)
from app.embeddings.service import EmbeddingProviderError, EmbeddingService, EmbeddingValidationError

__all__ = [
    "EMBEDDING_DIMENSIONS",
    "ConfiguredEmbeddingProvider",
    "DeterministicTestEmbeddingProvider",
    "DisabledEmbeddingProvider",
    "EmbeddingConfig",
    "EmbeddingExecutionDisabledError",
    "EmbeddingProvider",
    "EmbeddingProviderError",
    "EmbeddingProviderFactory",
    "EmbeddingProviderName",
    "EmbeddingService",
    "EmbeddingValidationError",
]
