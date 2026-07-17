"""管理员 AI Runtime 配置 API（PostgreSQL 持久化）。

文件职责：GET/PATCH /api/v1/admin/ai-runtime。
谁调用它：Frontend AI 管理页；验收脚本。
它调用谁：AiRuntimeService、require_permission(security.manage)、CurrentUser。
输入：JWT + confirmed + expected_version + 可选 mode/kill_switch。
输出：不含 API Key 的运行时视图。
设计理由：配置持久化、乐观锁、二次确认、Kill Switch、审计。
日本现场面试：Secret 不进库、不回响应；actor 只来自 JWT。
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from app.models.ai_runtime_settings import ENABLE_REAL_CONFIRMATION_TEXT
from app.observability.logging import get_request_id
from app.schemas.common import ApiResponse, success_response
from app.security.contracts import CurrentUser
from app.security.dependencies import get_current_user, require_permission
from app.security.rbac_contracts import Permission
from app.services.ai_runtime_service import (
    AiRuntimeService,
    AiRuntimeUnavailableException,
    AiRuntimeView,
)
from app.services.persistent_audit_service import PersistentAuditContext

router = APIRouter(prefix="/api/v1/admin/ai-runtime", tags=["admin-ai-runtime"])

LlmMode = Literal["stub", "openrouter", "fallback_chain"]


class ProviderReadinessResponse(BaseModel):
    name: str
    ready: bool
    key_configured: bool
    low_cost_model: str | None = None
    high_quality_model: str | None = None
    enabled: bool


class UpdatedByResponse(BaseModel):
    user_id: str | None = None
    username: str | None = None


class AiRuntimeResponse(BaseModel):
    """GET/PATCH 成功响应；禁止出现任何 Key 原文。"""

    effective_mode: LlmMode
    configured_mode: LlmMode
    real_calls_enabled: bool
    kill_switch: bool
    version: int
    updated_at: datetime
    updated_by: UpdatedByResponse
    provider_readiness: list[ProviderReadinessResponse]
    openrouter_key_configured: bool
    nvidia_key_configured: bool
    gemini_key_configured: bool
    local_qwen_enabled: bool
    low_cost_model: str
    high_quality_model: str
    fallback_order: list[str]
    timeout_seconds: float
    total_timeout_seconds: float
    budget_summary: dict[str, str]
    repository_backend: str
    run_real_llm_smoke: bool
    confirmation_text_required_for_real: str = ENABLE_REAL_CONFIRMATION_TEXT
    note: str


class AiRuntimePatchRequest(BaseModel):
    """PATCH 合同：必须 confirmed + expected_version；启用真实模式时 confirmation_text。"""

    expected_version: int = Field(ge=1)
    confirmed: bool = False
    mode: LlmMode | None = None
    kill_switch: bool | None = None
    confirmation_text: str | None = Field(default=None, max_length=64)


def _to_response(view: AiRuntimeView) -> AiRuntimeResponse:
    return AiRuntimeResponse(
        effective_mode=view.effective_mode,
        configured_mode=view.configured_mode,
        real_calls_enabled=view.real_calls_enabled,
        kill_switch=view.kill_switch,
        version=view.version,
        updated_at=view.updated_at,
        updated_by=UpdatedByResponse(
            user_id=view.updated_by.get("user_id"),
            username=view.updated_by.get("username"),
        ),
        provider_readiness=[
            ProviderReadinessResponse(
                name=item.name,
                ready=item.ready,
                key_configured=item.key_configured,
                low_cost_model=item.low_cost_model,
                high_quality_model=item.high_quality_model,
                enabled=item.enabled,
            )
            for item in view.provider_readiness
        ],
        openrouter_key_configured=view.openrouter_key_configured,
        nvidia_key_configured=view.nvidia_key_configured,
        gemini_key_configured=view.gemini_key_configured,
        local_qwen_enabled=view.local_qwen_enabled,
        low_cost_model=view.low_cost_model,
        high_quality_model=view.high_quality_model,
        fallback_order=view.fallback_order,
        timeout_seconds=view.timeout_seconds,
        total_timeout_seconds=view.total_timeout_seconds,
        budget_summary=view.budget_summary,
        repository_backend=view.repository_backend,
        run_real_llm_smoke=view.run_real_llm_smoke,
        note=view.note,
    )


def _get_service(request: Request) -> AiRuntimeService:
    service = getattr(request.app.state.container, "ai_runtime_service", None)
    if service is None:
        raise AiRuntimeUnavailableException()
    return service


@router.get("", response_model=ApiResponse[AiRuntimeResponse])
async def get_ai_runtime(
    request: Request,
    _: Annotated[object, Depends(require_permission(Permission.SECURITY_MANAGE))],
) -> ApiResponse[AiRuntimeResponse]:
    """管理员读取 AI Runtime（PostgreSQL）；InMemory fail-closed。"""

    service = _get_service(request)
    if not service.available:
        raise AiRuntimeUnavailableException(
            {"repository_backend": request.app.state.container.repository_backend}
        )
    return success_response(_to_response(service.get_view()), get_request_id())


@router.patch("", response_model=ApiResponse[AiRuntimeResponse])
async def patch_ai_runtime(
    payload: AiRuntimePatchRequest,
    request: Request,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    _: Annotated[object, Depends(require_permission(Permission.SECURITY_MANAGE))],
) -> ApiResponse[AiRuntimeResponse]:
    """管理员更新 mode / kill_switch；actor 只来自 CurrentUser。"""

    service = _get_service(request)
    if not service.available:
        raise AiRuntimeUnavailableException(
            {"repository_backend": request.app.state.container.repository_backend}
        )

    def rebuild(new_settings) -> None:
        from app.config.container import build_container

        # 重建后保留同一 app 上的 container 引用。
        request.app.state.container = build_container(new_settings)

    # 注入 rebuild；避免循环 import 固定在构造时。
    service._rebuild_container = rebuild

    audit_context = PersistentAuditContext(
        request_id=get_request_id() or "unknown",
        http_method=request.method,
        api_path=str(request.url.path),
        resource_id="default",
        current_user=current_user,
        actor_username=current_user.username,
    )
    view = service.patch(
        actor=current_user,
        expected_version=payload.expected_version,
        confirmed=payload.confirmed,
        mode=payload.mode,
        kill_switch=payload.kill_switch,
        confirmation_text=payload.confirmation_text,
        audit_context=audit_context,
    )
    return success_response(_to_response(view), get_request_id())
