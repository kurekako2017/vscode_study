from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_document_chunk_service
from app.observability.logging import get_request_id
from app.schemas.common import ApiResponse, success_response
from app.schemas.document_chunk_api import DocumentChunkListResponse
from app.services.document_chunk_service import DocumentChunkService

# 文档 chunk 路由负责把同步切片能力暴露成稳定 HTTP API。
router = APIRouter(prefix="/api/v1/documents", tags=["document-chunks"])


@router.post(
    path="/{document_id}/chunks",
    response_model=ApiResponse[DocumentChunkListResponse],
    status_code=status.HTTP_201_CREATED,
)
async def chunk_document(
    document_id: str,
    service: DocumentChunkService = Depends(get_document_chunk_service),
) -> ApiResponse[DocumentChunkListResponse]:
    """对已验证文档执行同步 chunk，并返回确定性的 chunk 列表。"""

    data = service.chunk_document(document_id)
    return success_response(data, get_request_id())


@router.get(
    path="/{document_id}/chunks",
    response_model=ApiResponse[DocumentChunkListResponse],
    status_code=status.HTTP_200_OK,
)
async def get_document_chunks(
    document_id: str,
    service: DocumentChunkService = Depends(get_document_chunk_service),
) -> ApiResponse[DocumentChunkListResponse]:
    """读取当前版本的 chunk 列表。"""

    data = service.get_chunks(document_id)
    return success_response(data, get_request_id())
