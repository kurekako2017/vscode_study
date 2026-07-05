from fastapi import Depends, Request

from app.config.container import AppContainer
from app.events.publisher import EventPublisher
from app.repositories.interfaces.event_repository import EventRepository
from app.services.approval_service import ApprovalService
from app.services.audit_middleware import AuditMiddleware
from app.services.audit_service import AuditService
from app.services.document_archive_service import DocumentArchiveService
from app.services.document_chunk_service import DocumentChunkService
from app.services.document_import_service import DocumentImportService
from app.services.document_read_service import DocumentReadService
from app.services.document_retrieval_service import DocumentRetrievalService
from app.services.document_upload_service import DocumentUploadService
from app.services.internal_rag_service import InternalRagService
from app.services.rbac_guard import RBACGuard
from app.services.security_service import SecurityService
from app.services.task_service import TaskService


async def get_container(request: Request) -> AppContainer:
    """从 FastAPI 应用状态取得本次 App 独享的依赖容器。"""

    return request.app.state.container


async def get_task_service(request: Request) -> TaskService:
    """向路由注入 TaskService，避免路由直接构造业务依赖。"""

    return request.app.state.container.task_service


async def get_event_repository(request: Request) -> EventRepository:
    """向 SSE 路由暴露事件读取接口，而不是具体存储细节。"""

    return request.app.state.container.event_repository


async def get_event_publisher(request: Request) -> EventPublisher:
    """按需构造轻量事件发布器；底层 Repository 仍由容器统一持有。"""

    return EventPublisher(request.app.state.container.event_repository)


async def get_document_upload_service(request: Request) -> DocumentUploadService:
    """向文档上传路由注入同步上传 service。"""

    return request.app.state.container.document_upload_service


async def get_document_read_service(request: Request) -> DocumentReadService:
    """向文档读取路由注入同步读 service。"""

    return request.app.state.container.document_read_service


async def get_document_chunk_service(request: Request) -> DocumentChunkService:
    """向文档 chunk 路由注入同步 chunk service。"""

    return request.app.state.container.document_chunk_service


async def get_document_retrieval_service(request: Request) -> DocumentRetrievalService:
    """向文档检索路由注入同步 retrieval service。"""

    return request.app.state.container.document_retrieval_service


async def get_document_import_service(request: Request) -> DocumentImportService:
    """向文档导入路由注入同步 import service。"""

    return request.app.state.container.document_import_service


async def get_document_archive_service(request: Request) -> DocumentArchiveService:
    """向文档归档路由注入同步 archive service。"""

    return request.app.state.container.document_archive_service


async def get_internal_rag_service(request: Request) -> InternalRagService:
    """向 internal RAG 路由注入 grounded answer service。"""

    return request.app.state.container.internal_rag_service


async def get_approval_service(request: Request) -> ApprovalService:
    """向 approval 路由注入审批工作流 service。"""

    return request.app.state.container.approval_service


async def get_security_service(request: Request) -> SecurityService:
    """向 security 路由注入当前用户和冻结目录 service。"""

    return request.app.state.container.security_service


async def get_audit_service(request: Request) -> AuditService:
    """向 audit 路由注入 append-only 审计 service。"""

    return request.app.state.container.audit_service


async def get_audit_middleware(
    security_service: SecurityService = Depends(get_security_service),
    audit_service: AuditService = Depends(get_audit_service),
) -> AuditMiddleware:
    """向 approval 路由注入 approval 专用审计中间层。"""

    return AuditMiddleware(
        audit_service=audit_service,
        security_service=security_service,
        rbac_guard=RBACGuard(security_service, audit_service),
    )


async def get_rbac_guard(
    security_service: SecurityService = Depends(get_security_service),
    audit_service: AuditService = Depends(get_audit_service),
) -> RBACGuard:
    """向需要统一授权的路由注入可复用 RBAC guard。"""

    return RBACGuard(security_service, audit_service)
