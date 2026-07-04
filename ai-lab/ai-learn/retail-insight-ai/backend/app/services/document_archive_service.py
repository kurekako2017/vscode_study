"""文档归档服务。

文件职责：
- 提供 DELETE /api/v1/documents/{document_id} 的软删除实现。
- 把归档、事件发布与 404 映射从路由中抽离出来，便于测试和后续替换仓储。

谁会调用它：
- `backend/app/api/documents.py` 的 DELETE 接口。

它调用谁：
- `DocumentRepository` 读取并保存文档事实。
- `EventPublisher` 记录归档完成事件。

输入是什么：
- `document_id`。

输出是什么：
- 归档后的 `DocumentArchiveResponse`；缺失时抛出 `DocumentNotFoundException`。

为什么需要这一层：
- DELETE 语义是软删除，不能交给路由直接操作仓储实现。

日本现场面试怎么讲：
- 这是文档生命周期的应用服务层，当前只做软删除，未来可平滑扩展审批前置条件和审计事件。
"""

from __future__ import annotations

from app.errors.exceptions import DocumentNotFoundException
from app.events.publisher import EventPublisher
from app.models.document import DocumentStatus
from app.observability.logging import get_logger, log_event
from app.repositories.interfaces.document_repository import DocumentRepository
from app.schemas.document_api import DocumentArchiveResponse

logger = get_logger(__name__)


class DocumentArchiveService:
    """封装文档归档和归档事件发布逻辑。"""

    def __init__(self, repository: DocumentRepository, event_publisher: EventPublisher) -> None:
        """保存仓储和事件发布器引用。"""

        self._repository = repository
        self._event_publisher = event_publisher

    def archive_document(self, document_id: str) -> DocumentArchiveResponse:
        """将文档软删除为 archived，不物理删除事实数据。"""

        document = self._repository.get(document_id)
        if document is None:
            raise DocumentNotFoundException(document_id)

        if document.status is not DocumentStatus.ARCHIVED:
            document.archive()
            self._repository.update(document)
            self._event_publisher.publish(
                document_id,
                "document.archive.completed",
                "Document archived",
                {"document_id": document_id, "status": document.status.value},
            )
            log_event(
                logger,
                "info",
                "document.archive.completed",
                "Document archived",
                task_id=document_id,
                status=document.status.value,
                node="document_archive_service",
            )

        return DocumentArchiveResponse.from_domain(document)


__all__ = ["DocumentArchiveService"]
