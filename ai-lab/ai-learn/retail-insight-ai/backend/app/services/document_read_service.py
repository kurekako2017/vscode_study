"""文档读服务。

文件职责：
- 提供低风险的 Document Read API 查询逻辑。
- 把列表过滤和单文档读取从路由中抽离出来，便于单测和后续仓储替换。

谁会调用它：
- `backend/app/api/documents.py` 的 GET 接口。

它调用谁：
- `DocumentRepository` 读取文档事实。

输入是什么：
- 过滤条件、document_id。

输出是什么：
- 文档列表或单个文档响应；缺失时抛出 `DocumentNotFoundException`。

为什么需要这一层：
- 让 Read API 只处理读边界，不和 Upload 或 Workflow 耦合。

日本现场面试怎么讲：
- 这是文档读模型的应用服务层，后续可以平滑替换成 PostgreSQL、缓存或搜索实现。
"""

from __future__ import annotations

from app.core.learning_trace import trace_step
from app.errors.exceptions import DocumentNotFoundException
from app.models.document import Document, DocumentStatus, DocumentType, Language
from app.repositories.interfaces.document_repository import DocumentRepository
from app.schemas.document_api import DocumentListResponse, DocumentResponse


class DocumentReadService:
    """封装列表过滤与单文档读取逻辑。"""

    def __init__(self, repository: DocumentRepository) -> None:
        """保存仓储接口引用。"""

        self._repository = repository

    def list_documents(
        self,
        *,
        status: DocumentStatus | None = None,
        document_type: DocumentType | None = None,
        language: Language | None = None,
        owner: str | None = None,
        tag: str | None = None,
        include_archived: bool = False,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> DocumentListResponse:
        """返回符合过滤条件的文档列表。"""

        # 记录读取 Service，方便初学者看到过滤参数即将交给 Repository 查询。
        trace_step(
            "GET",
            "/api/v1/documents",
            "Service",
            "DocumentReadService.list_documents()",
            class_name="DocumentReadService",
            method_name="list_documents",
            file_path="backend/app/services/document_read_service.py",
            label="DocumentReadService.list_documents()",
        )
        # 记录实际读取仓库的节点，下一步进入 InMemoryDocumentRepository.list_all()。
        trace_step(
            "GET",
            "/api/v1/documents",
            "Repository",
            "InMemoryDocumentRepository.list_all()",
            class_name=self._repository.__class__.__name__,
            method_name="list_all",
            file_path=(
                "backend/app/repositories/implementations/"
                "in_memory/document_repository.py"
            ),
            label="InMemoryDocumentRepository.list_all()",
        )
        documents = self._repository.list_all()
        filtered = [
            document
            for document in documents
            if self._matches(
                document,
                status=status,
                document_type=document_type,
                language=language,
                owner=owner,
                tag=tag,
                include_archived=include_archived,
            )
        ]
        if limit is not None:
            filtered = filtered[:limit]
        return DocumentListResponse.from_domain(filtered)

    def get_document(self, document_id: str) -> DocumentResponse:
        """按 ID 读取单个文档，不存在时返回稳定 404。"""

        document = self._repository.get(document_id)
        if document is None:
            raise DocumentNotFoundException(document_id)
        return DocumentResponse.from_domain(document)

    def _matches(
        self,
        document: Document,
        *,
        status: DocumentStatus | None,
        document_type: DocumentType | None,
        language: Language | None,
        owner: str | None,
        tag: str | None,
        include_archived: bool,
    ) -> bool:
        metadata = document.metadata
        if metadata.status is DocumentStatus.ARCHIVED and not include_archived and status is not DocumentStatus.ARCHIVED:
            return False
        if status is not None and metadata.status is not status:
            return False
        if document_type is not None and metadata.document_type is not document_type:
            return False
        if language is not None and metadata.language is not language:
            return False
        if owner is not None and metadata.owner != owner:
            return False
        if tag is not None and tag not in metadata.tags:
            return False
        return True


__all__ = ["DocumentReadService"]
