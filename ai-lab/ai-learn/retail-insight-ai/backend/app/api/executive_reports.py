"""显式 Executive Report HTTP 入口：high_quality 路由只允许经 Gateway。"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Header, Request

from app.api.dependencies import get_executive_report_service
from app.observability.logging import get_request_id
from app.schemas.ai_analysis_api import (
    AIAnalysisCitationResponse,
    AIAnalysisUsageResponse,
    AttemptedProviderSummary,
)
from app.schemas.common import ApiResponse, success_response
from app.schemas.executive_report_api import ExecutiveReportRequest, ExecutiveReportResponse
from app.security.contracts import CurrentUser
from app.security.dependencies import require_permission
from app.security.rbac_contracts import Permission
from app.services.executive_report_service import ExecutiveReportService
from app.services.persistent_audit_service import PersistentAuditContext

router = APIRouter(prefix="/api/v1/executive-reports", tags=["executive-reports"])


@router.post("", response_model=ApiResponse[ExecutiveReportResponse])
async def generate_executive_report(
    payload: ExecutiveReportRequest,
    request: Request,
    current_user: Annotated[CurrentUser, Depends(require_permission(Permission.ANALYSIS_EXECUTE))],
    service: Annotated[ExecutiveReportService, Depends(get_executive_report_service)],
    idempotency_key: Annotated[
        str,
        Header(alias="Idempotency-Key", min_length=8, max_length=128, pattern=r"^[A-Za-z0-9._:-]+$"),
    ],
) -> ApiResponse[ExecutiveReportResponse]:
    """客户端不得提交 provider/model/route_tier/price/actor。"""

    result = service.execute(
        payload, actor=current_user, idempotency_key=idempotency_key,
        context=PersistentAuditContext(
            request_id=get_request_id(), http_method=request.method, api_path=request.url.path,
            resource_id="executive-report", current_user=current_user,
        ),
    )
    attempted = [
        AttemptedProviderSummary(
            provider_name=item.provider_name,
            model_name=item.model_name,
            status=item.status,
            latency_ms=item.latency_ms,
        )
        for item in result.attempted_providers
    ]
    data = ExecutiveReportResponse(
        report_id=result.report_id,
        report_version_id=result.report_version_id,
        task_id=result.task_id,
        title=result.title,
        executive_summary=result.executive_summary,
        kpi_findings=list(result.kpi_findings),
        risks=list(result.risks),
        recommendations=list(result.recommendations),
        citations=[
            AIAnalysisCitationResponse(
                document_id=item.document_id, chunk_id=item.chunk_id,
                score=item.score, excerpt=item.excerpt,
            )
            for item in result.citations
        ],
        provider=result.provider_name,
        model=result.model_name,
        provider_name=result.provider_name,
        model_name=result.model_name,
        route_tier=result.route_tier,
        usage=AIAnalysisUsageResponse(
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            total_tokens=result.total_tokens,
        ),
        estimated_cost=result.estimated_cost,
        actual_cost=result.actual_cost,
        currency=result.currency,
        status=result.status,
        analysis_id=result.analysis_id,
        usage_id=result.usage_id,
        created_at=result.created_at,
        fallback_used=result.fallback_used,
        attempt_count=result.attempt_count,
        attempted_providers=attempted,
        total_input_tokens=result.input_tokens,
        total_output_tokens=result.output_tokens,
        total_tokens=result.total_tokens,
        total_actual_cost=result.actual_cost,
    )
    return success_response(data, get_request_id())


__all__ = ["router"]
