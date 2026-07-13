"""Embedding Foundation 对外入口；Phase 2A 仅提供接缝，不执行向量生成。"""

from app.embeddings.config import EmbeddingConfig, EmbeddingProviderName
from app.embeddings.factory import EmbeddingProviderFactory
from app.embeddings.interface import EmbeddingProvider
from app.embeddings.provider import (
    ConfiguredEmbeddingProvider,
    DisabledEmbeddingProvider,
    EmbeddingExecutionDisabledError,
)

__all__ = [
    "ConfiguredEmbeddingProvider",
    "DisabledEmbeddingProvider",
    "EmbeddingConfig",
    "EmbeddingExecutionDisabledError",
    "EmbeddingProvider",
    "EmbeddingProviderFactory",
    "EmbeddingProviderName",
]
