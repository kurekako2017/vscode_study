"""Phase 2A 的无执行 Embedding Provider。

文件职责：承载 Factory 选择结果，但禁止真正生成向量或访问外部服务。
谁调用它：EmbeddingProviderFactory；未来具体 Adapter 会替换 Configured Provider。
它调用谁：不导入 OpenAI/OpenRouter/NVIDIA SDK，不调用网络。
输入：EmbeddingConfig 与 texts；输出：当前统一抛出禁用错误。
为什么这样设计：先验证依赖方向和配置切换，再单独评审模型、成本与数据安全。
日本现场面试：Foundation Provider 是 fail-closed 边界，未完成的能力不会静默返回伪向量。
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from app.embeddings.config import EmbeddingConfig


class EmbeddingExecutionDisabledError(RuntimeError):
    """表示当前阶段只建立接口，禁止执行 Embedding。"""


@dataclass(frozen=True)
class DisabledEmbeddingProvider:
    """默认 Provider，确保学习模式不会意外开始向量生成。"""

    name: str = "disabled"
    model: str | None = None
    dimensions: int | None = None

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        raise EmbeddingExecutionDisabledError("embedding execution is disabled")


@dataclass(frozen=True)
class ConfiguredEmbeddingProvider:
    """记录未来 Provider 配置，但在 Phase 2A 仍然 fail-closed。"""

    config: EmbeddingConfig

    @property
    def name(self) -> str:
        return self.config.provider

    @property
    def model(self) -> str | None:
        return self.config.model

    @property
    def dimensions(self) -> int | None:
        return self.config.dimensions

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        raise EmbeddingExecutionDisabledError(
            f"embedding provider '{self.name}' is configured but execution is unavailable in Phase 2A"
        )


__all__ = [
    "ConfiguredEmbeddingProvider",
    "DisabledEmbeddingProvider",
    "EmbeddingExecutionDisabledError",
]
