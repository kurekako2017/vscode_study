from __future__ import annotations

from typing import Protocol

from app.models.analysis import ResearchResult


class ResearchProvider(Protocol):
    """定义 Research Provider 最小合同，便于本地与未来外部实现互换。"""

    name: str

    async def research(self, question: str) -> ResearchResult:
        """根据问题返回带来源的调查结果。"""

        ...


class ResearchAgent:
    """封装调查能力，让 Workflow 不依赖具体模型或外部服务。"""

    def __init__(self, provider: ResearchProvider) -> None:
        """注入 Provider；核心 Workflow 因此不依赖外部系统实现。"""

        self._provider = provider

    async def run(self, question: str) -> ResearchResult:
        """委托 Provider 执行调查，并保持统一的 ResearchResult 合同。"""

        # Agent 不直接选择密钥或 URL，配置和外部访问应由 Provider 边界负责。
        return await self._provider.research(question)
