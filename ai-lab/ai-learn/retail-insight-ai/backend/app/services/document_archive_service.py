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

from app.core.learning_trace import trace_step
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

        # 记录进入归档 Service，区分 Router 接收请求和归档业务处理。
        trace_step(
            "DELETE",
            f"/api/v1/documents/{document_id}",
            "Service",
            "DocumentArchiveService.archive_document()",
            class_name="DocumentArchiveService",
            method_name="archive_document",
            file_path="backend/app/services/document_archive_service.py",
            document_id=document_id,
            label="DocumentArchiveService.archive_document()",
        )
        # 记录读取归档目标的 Repository 步骤，404 分支也需要保留这条链路。
        trace_step(
            "DELETE",
            f"/api/v1/documents/{document_id}",
            "Repository",
            "InMemoryDocumentRepository.get()",
            class_name=self._repository.__class__.__name__,
            method_name="get",
            file_path=(
                "backend/app/repositories/implementations/"
                "in_memory/document_repository.py"
            ),
            document_id=document_id,
            label="InMemoryDocumentRepository.get()",
        )
        document = self._repository.get(document_id)
        if document is None:
            # 单独记录未命中，帮助初学者区分查询完成和业务 404。
            trace_step(
                "DELETE",
                f"/api/v1/documents/{document_id}",
                "Result",
                "Document not found",
                document_id=document_id,
                status="404",
                label="Document not found",
            )
            raise DocumentNotFoundException(document_id)

        if document.status is not DocumentStatus.ARCHIVED:
            document.archive()
            # 记录真正写回归档状态的 Repository 步骤。
            trace_step(
                "DELETE",
                f"/api/v1/documents/{document_id}",
                "Repository",
                "InMemoryDocumentRepository.update()",
                class_name=self._repository.__class__.__name__,
                method_name="update",
                file_path=(
                    "backend/app/repositories/implementations/"
                    "in_memory/document_repository.py"
                ),
                document_id=document_id,
                label="InMemoryDocumentRepository.update()",
            )
            self._repository.update(document)
            # 只记录真实标题，不输出正文、路径、checksum 或敏感 metadata。
            trace_step(
                "DELETE",
                f"/api/v1/documents/{document_id}",
                "Result",
                f"Document archived: {document.metadata.title}",
                document_id=document_id,
                status="202",
                label=f"Document archived: {document.metadata.title}",
            )
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
