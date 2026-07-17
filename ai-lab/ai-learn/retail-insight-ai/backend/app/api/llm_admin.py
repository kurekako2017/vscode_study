"""LLM 运行时配置只读/切换 API（管理员）。

文件职责：暴露当前 LLM_PROVIDER_MODE 与安全摘要，并允许 admin 在已配置密钥前提下切换模式。
谁调用它：Frontend AI 管理页；Swagger 手工验收。
它调用谁：Settings 校验、container rebuild、require_permission(security.manage)。
输入：可选 mode 更新请求。
输出：不含 API Key 的运行时摘要。
设计理由：页面可发现当前是 stub 还是 chain；真实模式 fail-closed 且默认仍 stub。
日本现场面试：成本开关必须可审计、可关闭，不能把 Key 放进 UI。
"""

from __future__ import annotations

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from app.config.container import build_container
from app.config.settings import Settings
from app.observability.logging import get_request_id, log_event, get_logger
from app.schemas.common import ApiResponse, success_response
from app.security.dependencies import require_permission
from app.security.rbac_contracts import Permission

router = APIRouter(prefix="/api/v1/admin/llm", tags=["admin-llm"])
logger = get_logger(__name__)

LlmMode = Literal["stub", "openrouter", "fallback_chain"]


class LlmRuntimeResponse(BaseModel):
    """安全可展示的 LLM 运行时摘要（无 Secret）。"""

    llm_provider_mode: LlmMode
    repository_backend: str
    chain_order: list[str]
    openrouter_key_configured: bool
    nvidia_key_configured: bool
    gemini_key_configured: bool
    local_qwen_enabled: bool
    run_real_llm_smoke: bool
    cost_risk_notes: list[str]
    switchable_modes: list[LlmMode]
    note: str


class LlmRuntimeUpdateRequest(BaseModel):
    """切换模式请求；禁止携带 API Key。"""

    llm_provider_mode: LlmMode = Field(description="stub | openrouter | fallback_chain")


def _key_set(secret) -> bool:
    if secret is None:
        return False
    try:
        return bool(secret.get_secret_value().strip())
    except Exception:
        return False


def _build_response(settings: Settings) -> LlmRuntimeResponse:
    mode = settings.llm_provider_mode
    chain = ["OpenRouter", "NVIDIA", "Gemini", "Local Qwen"]
    notes = [
        "默认与推荐验收：LLM_PROVIDER_MODE=stub，零外部费用。",
        "fallback_chain / openrouter 可能产生真实费用，仅在密钥已配置且人工确认时切换。",
        "API Key 只能来自服务端环境变量，UI 不可提交密钥。",
        "切换模式会重建 LLM Gateway；不写入密钥、不触发真实 smoke。",
    ]
    switchable: list[LlmMode] = ["stub"]
    if _key_set(settings.openrouter_api_key) or settings.openrouter_enabled:
        switchable.append("openrouter")
    # fallback_chain 允许在未全开时选择，但 build 时会 fail-closed
    switchable.append("fallback_chain")
    return LlmRuntimeResponse(
        llm_provider_mode=mode,  # type: ignore[arg-type]
        repository_backend=settings.repository_backend,
        chain_order=chain,
        openrouter_key_configured=_key_set(settings.openrouter_api_key),
        nvidia_key_configured=_key_set(settings.nvidia_api_key),
        gemini_key_configured=_key_set(settings.gemini_api_key),
        local_qwen_enabled=bool(settings.local_qwen_enabled),
        run_real_llm_smoke=bool(settings.run_real_llm_smoke),
        cost_risk_notes=notes,
        switchable_modes=switchable,
        note="正式页面验收请保持 stub。",
    )


@router.get("/runtime", response_model=ApiResponse[LlmRuntimeResponse])
async def get_llm_runtime(
    request: Request,
    _: Annotated[object, Depends(require_permission(Permission.SECURITY_MANAGE))],
) -> ApiResponse[LlmRuntimeResponse]:
    """管理员查看当前 LLM 模式与成本风险（无 Key）。"""

    settings: Settings = request.app.state.container.settings
    return success_response(_build_response(settings), get_request_id())


@router.put("/runtime", response_model=ApiResponse[LlmRuntimeResponse])
async def put_llm_runtime(
    payload: LlmRuntimeUpdateRequest,
    request: Request,
    _: Annotated[object, Depends(require_permission(Permission.SECURITY_MANAGE))],
) -> ApiResponse[LlmRuntimeResponse]:
    """管理员切换 stub/openrouter/fallback_chain；无密钥时 fail-closed。"""

    old: Settings = request.app.state.container.settings
    mode = payload.llm_provider_mode
    # 禁止通过本接口打开真实 smoke
    try:
        new_settings = old.model_copy(
            update={
                "llm_provider_mode": mode,
                "llm_provider": mode,
                "run_real_llm_smoke": False,
                "run_openrouter_smoke": False,
                "run_nvidia_smoke": False,
                "run_gemini_smoke": False,
                "run_local_qwen_smoke": False,
            }
        )
        # 触发校验（含 openrouter 必要字段）
        new_settings = Settings.model_validate(new_settings.model_dump(mode="python"))
    except Exception as exc:
        from app.errors.exceptions import ValidationAppException

        raise ValidationAppException(detail={"llm_provider_mode": str(exc)}) from exc

    # 重建组合根；PostgreSQL Repository 为无状态连接，可安全替换。
    request.app.state.container = build_container(new_settings)
    log_event(
        logger,
        "info",
        "llm_runtime_mode_changed",
        f"LLM provider mode updated by admin {old.llm_provider_mode} -> {mode}",
    )
    return success_response(_build_response(new_settings), get_request_id())
