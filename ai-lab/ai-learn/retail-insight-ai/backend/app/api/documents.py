from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, Header, Query, UploadFile, status

from app.api.dependencies import (
    get_document_archive_service,
    get_document_read_service,
    get_document_upload_service,
)
from app.observability.logging import get_request_id
from app.schemas.common import ApiResponse, success_response
from app.schemas.document_api import (
    DocumentArchiveResponse,
    DocumentListResponse,
    DocumentResponse,
    DocumentUploadSessionResponse,
)
from app.models.document import DocumentStatus, DocumentType, Language
from app.services.document_archive_service import DocumentArchiveService
from app.services.document_read_service import DocumentReadService
from app.services.document_upload_service import DocumentUploadService

# 文档路由。
router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.post(
    path="",
    response_model=ApiResponse[DocumentUploadSessionResponse],
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    metadata: str = Form(...),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    service: DocumentUploadService = Depends(get_document_upload_service),
) -> ApiResponse[DocumentUploadSessionResponse]:
    """接收上传文件与 metadata JSON，交给 service 执行同步冻结流程。"""

    content = await file.read()
    data = service.upload_document(
        filename=file.filename or "uploaded-file",
        content=content,
        content_type=file.content_type,
        metadata_json=metadata,
        idempotency_key=idempotency_key,
    )
    return success_response(data, get_request_id())


@router.get(path="", response_model=ApiResponse[DocumentListResponse], status_code=status.HTTP_200_OK)
async def list_documents(
    status_filter: DocumentStatus | None = Query(default=None, alias="status"),
    document_type: DocumentType | None = Query(default=None),
    language: Language | None = Query(default=None),
    owner: str | None = Query(default=None),
    tag: str | None = Query(default=None),
    include_archived: bool = Query(default=False),
    limit: int | None = Query(default=None, ge=1, le=100),
    cursor: str | None = Query(default=None),
    service: DocumentReadService = Depends(get_document_read_service),
) -> ApiResponse[DocumentListResponse]:
    """列出文档并支持低风险过滤，不改变上传事实。"""

    data = service.list_documents(
        status=status_filter,
        document_type=document_type,
        language=language,
        owner=owner,
        tag=tag,
        include_archived=include_archived,
        limit=limit,
        cursor=cursor,
    )
    return success_response(data, get_request_id())


@router.get(path="/{document_id}", response_model=ApiResponse[DocumentResponse], status_code=status.HTTP_200_OK)
async def get_document(
    document_id: str,
    service: DocumentReadService = Depends(get_document_read_service),
) -> ApiResponse[DocumentResponse]:
    """读取单个文档与其冻结元数据快照。"""

    data = service.get_document(document_id)
    return success_response(data, get_request_id())


@router.delete(
    path="/{document_id}",
    response_model=ApiResponse[DocumentArchiveResponse],
    status_code=status.HTTP_202_ACCEPTED,
)
async def archive_document(
    document_id: str,
    service: DocumentArchiveService = Depends(get_document_archive_service),
) -> ApiResponse[DocumentArchiveResponse]:
    """将文档软删除为 archived，同时保留版本与读取能力。"""

    data = service.archive_document(document_id)
    return success_response(data, get_request_id())
