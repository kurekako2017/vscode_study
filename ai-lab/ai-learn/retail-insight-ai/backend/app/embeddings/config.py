"""Embedding Provider 的统一配置模型。

文件职责：把应用 Settings 转成与 Provider 无关的最小配置。
谁调用它：EmbeddingProviderFactory 与 factory tests。
它调用谁：只读取 Settings 字段，不读取 API Key，也不访问网络。
输入：provider、model、dimensions；输出：不可变 EmbeddingConfig。
为什么这样设计：未来替换 Local/OpenAI/OpenRouter/NVIDIA 时不改变上层接口。
日本现场面试：先冻结配置合同，再逐个实现 Adapter，避免业务层绑定厂商 SDK。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from app.config.settings import Settings


EMBEDDING_DIMENSIONS = 384
EmbeddingProviderName = Literal[
    "disabled", "deterministic_test", "local", "openai", "openrouter", "nvidia"
]
SUPPORTED_EMBEDDING_PROVIDERS = frozenset(
    {"disabled", "deterministic_test", "local", "openai", "openrouter", "nvidia"}
)


@dataclass(frozen=True)
class EmbeddingConfig:
    """保存 Provider 选择与模型元数据；不保存任何 Secret。"""

    provider: EmbeddingProviderName = "disabled"
    model: str | None = None
    dimensions: int = EMBEDDING_DIMENSIONS

    def __post_init__(self) -> None:
        if self.provider not in SUPPORTED_EMBEDDING_PROVIDERS:
            raise ValueError(f"unsupported embedding provider: {self.provider}")
        if self.dimensions != EMBEDDING_DIMENSIONS:
            raise ValueError(f"embedding dimensions must equal {EMBEDDING_DIMENSIONS}")
        if self.provider != "disabled" and not (self.model or "").strip():
            raise ValueError("embedding model is required when provider is enabled")

    @classmethod
    def from_settings(cls, settings: "Settings") -> "EmbeddingConfig":
        """从全局配置提取 Embedding 子配置，不让 Provider 依赖整个应用。"""

        return cls(
            provider=settings.embedding_provider,
            model=settings.embedding_model,
            dimensions=settings.embedding_dimensions,
        )


__all__ = [
    "EMBEDDING_DIMENSIONS",
    "EmbeddingConfig",
    "EmbeddingProviderName",
    "SUPPORTED_EMBEDDING_PROVIDERS",
]
