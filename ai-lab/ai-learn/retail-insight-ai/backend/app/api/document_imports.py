from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_document_import_service
from app.observability.logging import get_request_id
from app.schemas.common import ApiResponse, success_response
from app.schemas.document_import_api import DocumentImportResponse
from app.services.document_import_service import DocumentImportService

# 文档导入路由只承载 Import Pipeline 的 HTTP 入口，不负责解析或持久化细节。
router = APIRouter(tags=["document-imports"])


@router.post(
    path="/api/v1/documents/{document_id}/import",
    response_model=ApiResponse[DocumentImportResponse],
    status_code=status.HTTP_201_CREATED,
)
async def import_document(
    document_id: str,
    service: DocumentImportService = Depends(get_document_import_service),
) -> ApiResponse[DocumentImportResponse]:
    """把已上传文档送入导入流水线，并返回最终导入记录。"""

    data = service.import_document(document_id)
    return success_response(data, get_request_id())


@router.get(
    path="/api/v1/document-imports/{import_id}",
    response_model=ApiResponse[DocumentImportResponse],
    status_code=status.HTTP_200_OK,
)
async def get_document_import(
    import_id: str,
    service: DocumentImportService = Depends(get_document_import_service),
) -> ApiResponse[DocumentImportResponse]:
    """读取某次文档导入记录。"""

    data = service.get_import(import_id)
    return success_response(data, get_request_id())
