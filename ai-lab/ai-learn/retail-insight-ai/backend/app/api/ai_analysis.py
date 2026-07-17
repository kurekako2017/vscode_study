"""显式 AI Analysis HTTP 入口：这是唯一允许调用 LLMProvider 的 Router。"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Header, Request

from app.api.dependencies import get_ai_analysis_service
from app.observability.logging import get_request_id
from app.schemas.ai_analysis_api import (
    AIAnalysisCitationResponse,
    AIAnalysisRequest,
    AIAnalysisResponse,
    AIAnalysisUsageResponse,
    AttemptedProviderSummary,
)
from app.schemas.common import ApiResponse, success_response
from app.security.contracts import CurrentUser
from app.security.dependencies import require_permission
from app.security.rbac_contracts import Permission
from app.services.ai_analysis_service import AIAnalysisService
from app.services.persistent_audit_service import PersistentAuditContext

router = APIRouter(prefix="/api/v1/ai-analysis", tags=["ai-analysis"])


@router.post("", response_model=ApiResponse[AIAnalysisResponse])
async def execute_ai_analysis(
    payload: AIAnalysisRequest,
    request: Request,
    current_user: Annotated[CurrentUser, Depends(require_permission(Permission.ANALYSIS_EXECUTE))],
    service: Annotated[AIAnalysisService, Depends(get_ai_analysis_service)],
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=128, pattern=r"^[A-Za-z0-9._:-]+$")],
) -> ApiResponse[AIAnalysisResponse]:
    """CurrentUser 只来自已验证 JWT，请求体不存在 actor/owner 字段。"""

    result = service.execute(
        payload, actor=current_user, idempotency_key=idempotency_key,
        context=PersistentAuditContext(
            request_id=get_request_id(), http_method=request.method, api_path=request.url.path,
            resource_id="ai-analysis", current_user=current_user,
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
    data = AIAnalysisResponse(
        analysis_id=result.analysis_id, answer=result.answer,
        citations=[AIAnalysisCitationResponse(document_id=item.document_id, chunk_id=item.chunk_id,
                                              score=item.score, excerpt=item.excerpt) for item in result.citations],
        provider=result.provider_name, model=result.model_name,
        provider_name=result.provider_name, model_name=result.model_name,
        route_tier=result.route_tier,
        usage=AIAnalysisUsageResponse(input_tokens=result.input_tokens, output_tokens=result.output_tokens,
                                      total_tokens=result.total_tokens),
        cost=result.actual_cost, currency=result.currency, status=result.status,
        created_at=result.created_at,
        usage_id=result.usage_id,
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
