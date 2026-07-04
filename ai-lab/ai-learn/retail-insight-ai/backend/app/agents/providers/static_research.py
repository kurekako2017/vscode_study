"""无需外部网络的 Static Research Provider。

文件职责：
- 被 `ResearchAgent` 调用。
- 从本地 JSON 文件读取 Research summary / sources。
- 当前不接互联网检索、不接 RAG、不接数据库。

输入：
- 用户问题字符串（当前仅保留接口兼容，Phase 1 不做查询路由）
- `LocalResearchDataLoader`

输出：
- `ResearchResult`

为什么需要这一层：
- 把 Research 数据来源从硬编码切换到文件输入，同时保持 Provider 接口稳定。

日本现场面试怎么讲：
- 当前是 Static Provider + Local JSON Dataset。
- 未来可以替换为 Internal Search / Internet Search / Hybrid Retrieval Provider。
"""

from __future__ import annotations

from app.data_loaders import LocalResearchDataLoader
from app.errors.exceptions import ResearchProviderException
from app.models.analysis import ResearchResult


class StaticResearchProvider:
    """提供本地静态调查资料，作为 Research Provider 的可部署默认实现。"""

    name = "static"

    def __init__(
        self,
        data_loader: LocalResearchDataLoader,
        fail: bool = False,
    ) -> None:
        """注入本地 JSON 加载器，并保留故障注入开关。"""

        self._data_loader = data_loader
        self._fail = fail

    async def research(self, question: str) -> ResearchResult:
        """返回本地 JSON 维护的带来源结果，不调用外部 LLM 或搜索服务。"""

        if self._fail:
            raise ResearchProviderException(provider=self.name)
        dataset = self._data_loader.load_research_dataset()
        return ResearchResult(
            summary=dataset.summary,
            sources=dataset.sources,
            provider=self.name,
            data_version=dataset.data_version,
        )
