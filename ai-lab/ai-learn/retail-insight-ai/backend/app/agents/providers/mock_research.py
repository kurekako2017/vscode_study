from __future__ import annotations

from app.models.analysis import ResearchResult


class MockResearchProvider:
    """提供无网络、结果固定且可注入失败的教学 Research 实现。"""

    name = "mock"

    def __init__(self, fail: bool = False) -> None:
        """保存失败开关，用于稳定验证异常和 SSE error 路径。"""

        self._fail = fail

    async def research(self, question: str) -> ResearchResult:
        """返回固定带来源结果；保留 question 参数以遵守 Provider 合同。"""

        if self._fail:
            raise RuntimeError("Mock research provider failure")
        return ResearchResult(
            summary=(
                "市場では価格だけでなく、在庫回転と会員向け施策を組み合わせた"
                "運用が重要です。競合比較では、地域と商品カテゴリを分けて確認します。"
            ),
            sources=[
                "mock://market-trend/2026-06",
                "mock://competitor-summary/2026-06",
            ],
            provider=self.name,
        )
