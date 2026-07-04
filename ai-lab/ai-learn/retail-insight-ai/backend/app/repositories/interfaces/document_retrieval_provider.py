"""DocumentRetrievalProvider 的 Protocol。

文件职责：
- 定义文档检索后端的稳定合同。
- 把 keyword 搜索、未来 full-text search、hybrid search 等实现从 service 中抽离出去。

谁会调用它：
- `DocumentRetrievalService` 作为应用服务调用它。

它调用谁：
- 不直接调用其他层，只通过返回结果让 service 继续处理事件和 API 响应。

输入是什么：
- `DocumentRetrievalSearchRequest`。

输出是什么：
- 检索结果列表与总命中数。

为什么需要这一层：
- 先固定“检索后端”边界，再让 service 只负责 API、事件和错误语义，后续替换存储或搜索算法时就不必改 route。

日本现场面试怎么讲：
- 这是 retrieval provider 接口，service 不再直接碰 chunk storage，未来可以平滑切换成 PostgreSQL full-text 或其他检索实现。
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.schemas.document_retrieval_api import (
    DocumentRetrievalResultResponse,
    DocumentRetrievalSearchRequest,
)


@runtime_checkable
class DocumentRetrievalProvider(Protocol):
    """定义内部文档检索后端的最小合同。"""

    name: str

    def search(self, request: DocumentRetrievalSearchRequest) -> tuple[list[DocumentRetrievalResultResponse], int]:
        """执行检索并返回结果列表与总命中数。"""

        ...


__all__ = ["DocumentRetrievalProvider"]
