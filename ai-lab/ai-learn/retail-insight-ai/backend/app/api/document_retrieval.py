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

# 文档检索路由只承载 keyword-only search 的 HTTP 入口，不负责排序细节或存储实现。
router = APIRouter(prefix="/api/v1/document-retrieval", tags=["document-retrieval"])


@router.post(
    path="/search",
    response_model=ApiResponse[DocumentRetrievalSearchResponse],
    status_code=status.HTTP_200_OK,
)
async def search_documents(
    request: DocumentRetrievalSearchRequest,
    service: DocumentRetrievalService = Depends(get_document_retrieval_service),
) -> ApiResponse[DocumentRetrievalSearchResponse]:
    """执行 keyword-only 文档检索，并返回稳定的来源追踪结果。"""

    data = service.search(request)
    return success_response(data, get_request_id())
