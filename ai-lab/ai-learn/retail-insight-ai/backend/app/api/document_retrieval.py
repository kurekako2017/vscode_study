from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_document_retrieval_service
from app.observability.logging import get_request_id
from app.schemas.common import ApiResponse, success_response
from app.schemas.document_retrieval_api import (
    DocumentRetrievalSearchRequest,
    DocumentRetrievalSearchResponse,
)
from app.services.document_retrieval_service import DocumentRetrievalService
from app.security.dependencies import require_permission
from app.security.rbac_contracts import Permission
from app.api.persistent_audit import persistent_audit_dependency
from app.services.persistent_audit_service import PersistentAuditSpec

# 路由只承载 keyword/vector/hybrid 的 HTTP 入口，不负责向量 SQL 或融合排序。
router = APIRouter(
    prefix="/api/v1/document-retrieval",
    tags=["document-retrieval"],
    dependencies=[Depends(require_permission(Permission.RETRIEVAL_QUERY))],
)


@router.post(
    path="/search",
    response_model=ApiResponse[DocumentRetrievalSearchResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            persistent_audit_dependency(
                PersistentAuditSpec(
                    action="retrieval.query",
                    resource_type="document_retrieval",
                    resource_id="document-retrieval",
                    success_status_code=status.HTTP_200_OK,
                    permission=Permission.RETRIEVAL_QUERY.value,
                )
            )
        )
    ],
)
async def search_documents(
    request: DocumentRetrievalSearchRequest,
    service: DocumentRetrievalService = Depends(get_document_retrieval_service),
) -> ApiResponse[DocumentRetrievalSearchResponse]:
    """按显式 retrieval_mode 检索；省略时继续执行兼容的 keyword 路径。"""

    data = service.search(request)
    return success_response(data, get_request_id())
