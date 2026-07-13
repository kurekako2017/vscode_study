"""Embedding Provider Factory。

文件职责：根据统一配置创建默认关闭或未来厂商的 Provider 壳。
谁调用它：未来组合根；Phase 2A 不接入 Container，避免影响 Learning Flow。
它调用谁：只创建本地 Python 对象，不加载 SDK、不访问网络。
输入：EmbeddingConfig 或 Settings；输出：满足 EmbeddingProvider 的对象。
为什么这样设计：集中 Provider 选择规则，避免 if/else 分散到业务代码。
日本现场面试：Factory 是 composition seam，Adapter 上线时只替换映射，不改 Workflow/API。
"""

from __future__ import annotations

from app.config.settings import Settings
from app.embeddings.config import EmbeddingConfig
from app.embeddings.interface import EmbeddingProvider
from app.embeddings.provider import ConfiguredEmbeddingProvider, DisabledEmbeddingProvider


class EmbeddingProviderFactory:
    """统一构建 EmbeddingProvider；当前所有可执行路径都保持关闭。"""

    @staticmethod
    def build(config: EmbeddingConfig) -> EmbeddingProvider:
        if config.provider == "disabled":
            return DisabledEmbeddingProvider()
        return ConfiguredEmbeddingProvider(config)

    @classmethod
    def from_settings(cls, settings: Settings) -> EmbeddingProvider:
        """从应用 Settings 构建 Provider，但不把它注入当前业务流程。"""

        return cls.build(EmbeddingConfig.from_settings(settings))


__all__ = ["EmbeddingProviderFactory"]
