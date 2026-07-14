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

# 路由只承载 keyword/vector/hybrid 的 HTTP 入口，不负责向量 SQL 或融合排序。
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
    """按显式 retrieval_mode 检索；省略时继续执行兼容的 keyword 路径。"""

    data = service.search(request)
    return success_response(data, get_request_id())
