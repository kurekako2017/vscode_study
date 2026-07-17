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
from app.repositories.interfaces.document_chunk_repository import DocumentChunkRepository
from app.repositories.interfaces.document_repository import DocumentRepository
from app.schemas.document_api import DocumentListResponse, DocumentResponse

# 列表默认上限，保证分页语义明确；客户端可传 1..100。
_DEFAULT_LIST_LIMIT = 50


class DocumentReadService:
    """封装列表过滤与单文档读取逻辑。"""

    def __init__(
        self,
        repository: DocumentRepository,
        chunk_repository: DocumentChunkRepository | None = None,
    ) -> None:
        """保存仓储接口引用；chunk_repository 用于列表 chunk_count / searchable。"""

        self._repository = repository
        self._chunk_repository = chunk_repository
    # 列表过滤
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
        """返回符合过滤条件的文档列表（稳定排序 + 默认 limit）。"""

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
        # 稳定排序：created_at DESC，同秒按 document_id ASC
        filtered.sort(
            key=lambda doc: (
                -doc.created_at.timestamp(),
                doc.document_id,
            )
        )
        effective_limit = _DEFAULT_LIST_LIMIT if limit is None else limit
        filtered = filtered[:effective_limit]
        chunk_counts = self._chunk_counts_for(filtered)
        response = DocumentListResponse.from_domain(filtered, chunk_counts=chunk_counts)

        # 记录本次真实返回数量，帮助初学者判断过滤和 limit 的最终结果。
        trace_step(
            "GET",
            "/api/v1/documents",
            "Result Summary",
            f"Documents found: {len(response.items)}",
            label=f"Documents found: {len(response.items)}",
        )
        # 只记录响应中的 title，最多展示前 10 个，避免输出正文或敏感元数据。
        for item in response.items[:10]:
            trace_step(
                "GET",
                "/api/v1/documents",
                "Result Summary",
                f"Document: {item.title}",
                label=f"Document: {item.title}",
            )
        if len(response.items) > 10:
            remaining = len(response.items) - 10
            trace_step(
                "GET",
                "/api/v1/documents",
                "Result Summary",
                f"Documents remaining: {remaining}",
                label=f"Documents remaining: {remaining}",
            )
        return response

    def get_document(self, document_id: str) -> DocumentResponse:
        """按 ID 读取单个文档，不存在时返回稳定 404。"""

        # 记录进入单文档读取 Service，区分 Router 接收请求和业务查询。
        trace_step(
            "GET",
            f"/api/v1/documents/{document_id}",
            "Service",
            "DocumentReadService.get_document()",
            class_name="DocumentReadService",
            method_name="get_document",
            file_path="backend/app/services/document_read_service.py",
            document_id=document_id,
            label="DocumentReadService.get_document()",
        )
        # 记录真正读取文档仓库的步骤，确认 document_id 进入哪个 Repository 方法。
        trace_step(
            "GET",
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
                "GET",
                f"/api/v1/documents/{document_id}",
                "Result",
                "Document not found",
                document_id=document_id,
                status="404",
                label="Document not found",
            )
            raise DocumentNotFoundException(document_id)
        # 只记录真实元数据标题，不输出正文、路径、checksum 或敏感 metadata。
        trace_step(
            "GET",
            f"/api/v1/documents/{document_id}",
            "Result",
            f"Document found: {document.metadata.title}",
            document_id=document_id,
            status="200",
            label=f"Document found: {document.metadata.title}",
        )
        count = self._chunk_count(document)
        return DocumentResponse.from_domain(document, chunk_count=count)

    def _chunk_counts_for(self, documents: list[Document]) -> dict[str, int]:
        """为列表项批量计算 chunk_count（无 chunk 仓储时返回 0）。"""

        result: dict[str, int] = {}
        for document in documents:
            result[document.document_id] = self._chunk_count(document)
        return result

    def _chunk_count(self, document: Document) -> int:
        if self._chunk_repository is None:
            return 0
        try:
            chunks = self._chunk_repository.list_for_document(
                document.document_id, document.version
            )
            return len(chunks)
        except Exception:
            return 0

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
