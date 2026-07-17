"""可提交审批的报告目录 API。

文件职责：列出最近 executive/task 报告的 task_id 与审批状态，避免用户手工记忆 task_id。
谁调用它：Frontend 承認管理页提交表单。
它调用谁：ReportRepository.list_recent。
输入：limit 查询参数。
输出：task_id / provider / approval_status / created_at（无 markdown 全文）。
设计理由：Approval submit 合同仍用 task_id path，但 UI 必须可发现可选 task。
日本现场面试：业务对象列表由后端提供，前端不做本地猜 ID。
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel, Field

from app.observability.logging import get_request_id
from app.schemas.common import ApiResponse, success_response
from app.security.dependencies import require_permission
from app.security.rbac_contracts import Permission

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


class ReportCatalogItem(BaseModel):
    task_id: str
    provider: str
    approval_status: str
    created_at: datetime
    markdown_preview: str = Field(description="截断预览，非全文")


class ReportCatalogResponse(BaseModel):
    items: list[ReportCatalogItem]
    total: int


@router.get("", response_model=ApiResponse[ReportCatalogResponse])
async def list_report_catalog(
    request: Request,
    _: Annotated[object, Depends(require_permission(Permission.APPROVAL_SUBMIT))],
    limit: int = Query(default=30, ge=1, le=100),
) -> ApiResponse[ReportCatalogResponse]:
    """列出可供 submit-approval 选择的报告 task_id。"""

    repo = request.app.state.container.report_repository
    reports = repo.list_recent(limit=limit)
    items = [
        ReportCatalogItem(
            task_id=item.task_id,
            provider=item.provider,
            approval_status=item.status.value,
            created_at=item.created_at,
            markdown_preview=(item.markdown[:160] + "…") if len(item.markdown) > 160 else item.markdown,
        )
        for item in reports
    ]
    return success_response(ReportCatalogResponse(items=items, total=len(items)), get_request_id())
