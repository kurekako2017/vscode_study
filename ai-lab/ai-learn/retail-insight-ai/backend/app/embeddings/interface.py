"""统一 Embedding Provider Protocol。

文件职责：冻结未来文本向量化 Adapter 的最小方法签名。
谁调用它：未来 Chunk Embedding Service；Phase 2A 只有 Factory Tests 使用。
它调用谁：Protocol 不调用任何实现或外部 API。
输入：一组文本；输出：与输入顺序一致的二维浮点数组。
为什么这样设计：业务编排只依赖协议，可替换 Local 或云端 Provider。
日本现场面试：这是 Dependency Inversion，厂商 SDK 被隔离在 Infrastructure Adapter。
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable


@runtime_checkable
class EmbeddingProvider(Protocol):
    """定义未来 Provider 必须满足的只读元数据和批量接口。"""

    name: str
    model: str | None
    dimensions: int | None

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        """把文本批次转换成向量；Phase 2A 的 Provider 会明确拒绝执行。"""

        ...


__all__ = ["EmbeddingProvider"]
