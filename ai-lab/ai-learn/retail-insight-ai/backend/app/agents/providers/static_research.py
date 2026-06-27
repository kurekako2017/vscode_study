"""无需外部网络的 Static Research Provider。"""

from __future__ import annotations

from app.errors.exceptions import ResearchProviderException
from app.models.analysis import ResearchResult


class StaticResearchProvider:
    """提供本地静态调查资料，作为 Research Provider 的可部署默认实现。"""

    name = "static"

    def __init__(self, fail: bool = False) -> None:
        """保存故障注入开关，仅用于验证标准错误路径。"""

        self._fail = fail

    async def research(self, question: str) -> ResearchResult:
        """返回本地维护的带来源结果，不调用外部 LLM 或搜索服务。"""

        if self._fail:
            raise ResearchProviderException(provider=self.name)
        return ResearchResult(
            summary=(
                "市場では価格だけでなく、在庫回転と会員向け施策を組み合わせた"
                "運用が重要です。競合比較では、地域と商品カテゴリを分けて確認します。"
            ),
            sources=[
                "static://market-trend/2026-06",
                "static://competitor-summary/2026-06",
            ],
            provider=self.name,
        )
