"""AI Runtime 配置应用服务（PostgreSQL 企业能力）。

文件职责：
- 从 PostgreSQL 恢复 / 更新 AI Runtime 单例配置。
- 计算 effective_mode、provider readiness、安全预算摘要。
- 强制二次确认、expected_version、Kill Switch 与 fail-closed。

谁调用它：Admin AI Runtime API；build_container 启动恢复。
它调用谁：PostgresAiRuntimeSettingsRepository、Settings、PersistentAuditService。
输入：CurrentUser + PATCH 合同。
输出：不含 Key 的运行时视图。
为什么需要：进程内切换在重启后丢失，且无法多实例共享。
日本现场面试：配置持久化 + 乐观锁 + 审计，Secret 永远不进库。
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Callable, Literal

from app.config.settings import Settings
from app.errors.base import AppException
from app.errors.error_codes import ErrorCode
from app.errors.exceptions import ValidationAppException
from app.models.ai_runtime_settings import (
    ENABLE_REAL_CONFIRMATION_TEXT,
    AiRuntimeMode,
    AiRuntimeSettingsRecord,
)
from app.repositories.postgres.ai_runtime_settings_repository import (
    AiRuntimeVersionConflictError,
    PostgresAiRuntimeSettingsRepository,
)
from app.security.contracts import CurrentUser
from app.services.persistent_audit_service import PersistentAuditContext, PersistentAuditService

LlmMode = Literal["stub", "openrouter", "fallback_chain"]


class AiRuntimeUnavailableException(AppException):
    """InMemory 或不支持后端时 fail-closed。"""

    def __init__(self, detail: dict[str, Any] | None = None) -> None:
        super().__init__(
            ErrorCode.AI_RUNTIME_UNAVAILABLE,
            "AI runtime management requires PostgreSQL repository backend",
            503,
            detail=detail or {"repository_backend": "inmemory"},
        )


class AiRuntimeVersionConflictException(AppException):
    """expected_version 冲突返回 409。"""

    def __init__(self, *, expected_version: int, current_version: int | None) -> None:
        super().__init__(
            ErrorCode.AI_RUNTIME_VERSION_CONFLICT,
            "AI runtime settings version conflict",
            409,
            detail={
                "expected_version": expected_version,
                "current_version": current_version,
            },
        )


class AiRuntimeNotReadyException(AppException):
    """目标 mode 的 Provider 未就绪。"""

    def __init__(self, detail: dict[str, Any] | None = None) -> None:
        super().__init__(
            ErrorCode.AI_RUNTIME_PROVIDER_NOT_READY,
            "Target AI runtime mode is not ready",
            422,
            detail=detail or {},
        )


class AiRuntimeConfirmationRequiredException(AppException):
    """启用真实模式缺少 confirmed / confirmation_text。"""

    def __init__(self, detail: dict[str, Any] | None = None) -> None:
        super().__init__(
            ErrorCode.AI_RUNTIME_CONFIRMATION_REQUIRED,
            "Confirmation required to change AI runtime",
            422,
            detail=detail or {},
        )


@dataclass(frozen=True)
class ProviderReadinessItem:
    name: str
    ready: bool
    key_configured: bool
    low_cost_model: str | None
    high_quality_model: str | None
    enabled: bool


@dataclass(frozen=True)
class AiRuntimeView:
    """Admin GET/PATCH 安全响应视图（无 Secret）。"""

    effective_mode: LlmMode
    configured_mode: LlmMode
    real_calls_enabled: bool
    kill_switch: bool
    version: int
    updated_at: datetime
    updated_by: dict[str, str | None]
    provider_readiness: list[ProviderReadinessItem]
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
    note: str


class AiRuntimeService:
    """PostgreSQL-only AI Runtime 管理；InMemory 由 API 层 fail-closed。"""

    def __init__(
        self,
        *,
        settings: Settings,
        repository: PostgresAiRuntimeSettingsRepository | None,
        persistent_audit_service: PersistentAuditService,
        rebuild_container: Callable[[Settings], Any] | None = None,
    ) -> None:
        self._settings = settings
        self._repository = repository
        self._persistent_audit = persistent_audit_service
        self._rebuild_container = rebuild_container
        self._cached: AiRuntimeSettingsRecord | None = None

    @property
    def available(self) -> bool:
        return (
            self._settings.repository_backend == "postgres"
            and self._repository is not None
        )

    def ensure_loaded(self) -> AiRuntimeSettingsRecord:
        """启动或首次访问时加载 / 初始化单例。"""

        if not self.available or self._repository is None:
            raise AiRuntimeUnavailableException()
        if self._cached is not None:
            return self._cached
        record = self._repository.get_or_initialize(
            default_mode=self._settings.llm_provider_mode  # type: ignore[arg-type]
        )
        self._cached = record
        return record

    def apply_to_settings(self, base: Settings) -> Settings:
        """用持久化配置覆盖 Settings 的 llm_provider_mode（Kill Switch 生效）。"""

        if not self.available or self._repository is None:
            return base
        record = self.ensure_loaded()
        effective = record.effective_mode
        if (
            base.llm_provider_mode == effective
            and base.llm_provider == effective
        ):
            return base
        updated = base.model_copy(
            update={
                "llm_provider_mode": effective,
                "llm_provider": effective,
                "run_real_llm_smoke": False,
                "run_openrouter_smoke": False,
                "run_nvidia_smoke": False,
                "run_gemini_smoke": False,
                "run_local_qwen_smoke": False,
            }
        )
        # stub 始终可校验；real 模式若缺 Key，在启动路径由 Settings validator fail-closed。
        return Settings.model_validate(updated.model_dump(mode="python"))

    def get_view(self) -> AiRuntimeView:
        record = self.ensure_loaded()
        return self._build_view(record, self._settings)

    def patch(
        self,
        *,
        actor: CurrentUser,
        expected_version: int,
        confirmed: bool,
        mode: LlmMode | None = None,
        kill_switch: bool | None = None,
        confirmation_text: str | None = None,
        audit_context: PersistentAuditContext | None = None,
    ) -> AiRuntimeView:
        """更新运行时配置并重建 LLM 栈。"""

        if not self.available or self._repository is None:
            raise AiRuntimeUnavailableException()
        if not confirmed:
            raise AiRuntimeConfirmationRequiredException(
                {"field": "confirmed", "reason": "confirmed must be true"}
            )

        current = self.ensure_loaded()
        next_mode: LlmMode = mode if mode is not None else current.mode
        next_kill = kill_switch if kill_switch is not None else current.kill_switch
        if next_mode not in ("stub", "openrouter", "fallback_chain"):
            raise ValidationAppException(
                {"mode": "mode must be stub, openrouter, or fallback_chain"}
            )

        enabling_real = (
            next_mode != "stub"
            and not next_kill
            and (current.mode == "stub" or current.kill_switch or not current.real_calls_enabled)
        )
        if enabling_real:
            if (confirmation_text or "").strip() != ENABLE_REAL_CONFIRMATION_TEXT:
                raise AiRuntimeConfirmationRequiredException(
                    {
                        "field": "confirmation_text",
                        "required": ENABLE_REAL_CONFIRMATION_TEXT,
                        "reason": "Stub→Real requires exact confirmation_text",
                    }
                )

        # Provider readiness：目标 effective mode 必须至少有一个对应 tier ready。
        target_effective: LlmMode = "stub" if next_kill else next_mode
        readiness = self._provider_readiness(self._settings)
        if target_effective != "stub":
            self._assert_mode_ready(target_effective, readiness)

        # 预算合法性：Settings 已校验 Decimal ≥ 0；此处再做 fail-closed 摘要检查。
        if not self._budget_config_valid(self._settings):
            raise ValidationAppException(
                {"budget": "LLM budget configuration is invalid"}
            )

        next_real = target_effective != "stub"
        mode_changed = next_mode != current.mode
        kill_changed = next_kill != current.kill_switch

        try:
            updated = self._repository.update_with_version(
                mode=next_mode,
                real_calls_enabled=next_real,
                kill_switch=next_kill,
                expected_version=expected_version,
                updated_by_user_id=actor.user_id,
                updated_by_username=actor.username,
            )
        except AiRuntimeVersionConflictError as exc:
            current_version = exc.current.version if exc.current else None
            raise AiRuntimeVersionConflictException(
                expected_version=expected_version,
                current_version=current_version,
            ) from exc

        self._cached = updated

        # 用 effective mode 重建 Settings / Container。
        new_settings = self._settings.model_copy(
            update={
                "llm_provider_mode": updated.effective_mode,
                "llm_provider": updated.effective_mode,
                "run_real_llm_smoke": False,
                "run_openrouter_smoke": False,
                "run_nvidia_smoke": False,
                "run_gemini_smoke": False,
                "run_local_qwen_smoke": False,
            }
        )
        try:
            new_settings = Settings.model_validate(new_settings.model_dump(mode="python"))
        except Exception as exc:
            # 恢复 DB 到旧版本会很复杂；fail-closed 返回校验错误，要求管理员修 Key 后重试。
            raise ValidationAppException({"llm_provider_mode": str(exc)}) from exc

        self._settings = new_settings
        if self._rebuild_container is not None:
            self._rebuild_container(new_settings)

        if audit_context is not None and self._persistent_audit.enabled:
            # 单 request_id 只写一条最终事件：优先 kill_switch，其次 mode。
            if kill_changed:
                action = "ai_runtime.kill_switch_changed"
            else:
                action = "ai_runtime.mode_changed"
            self._persistent_audit.record_ai_runtime_event(
                context=audit_context,
                actor=actor,
                action=action,
                result="success",
                status_code=200,
                from_mode=current.mode,
                to_mode=updated.mode,
                mode_changed=mode_changed,
                kill_changed=kill_changed,
                kill_switch=updated.kill_switch,
                effective_mode=updated.effective_mode,
                version=updated.version,
            )

        return self._build_view(updated, new_settings)

    def _build_view(
        self, record: AiRuntimeSettingsRecord, settings: Settings
    ) -> AiRuntimeView:
        readiness = self._provider_readiness(settings)
        low_model, high_model = self._display_models(settings, record.effective_mode)
        return AiRuntimeView(
            effective_mode=record.effective_mode,
            configured_mode=record.mode,
            real_calls_enabled=bool(record.real_calls_enabled and not record.kill_switch),
            kill_switch=record.kill_switch,
            version=record.version,
            updated_at=record.updated_at,
            updated_by={
                "user_id": record.updated_by_user_id,
                "username": record.updated_by_username,
            },
            provider_readiness=readiness,
            openrouter_key_configured=self._key_set(settings.openrouter_api_key),
            nvidia_key_configured=self._key_set(settings.nvidia_api_key),
            gemini_key_configured=self._key_set(settings.gemini_api_key),
            local_qwen_enabled=bool(settings.local_qwen_enabled),
            low_cost_model=low_model,
            high_quality_model=high_model,
            fallback_order=["OpenRouter", "NVIDIA", "Gemini", "Local Qwen"],
            timeout_seconds=float(settings.llm_timeout_seconds),
            total_timeout_seconds=float(settings.llm_total_timeout_seconds),
            budget_summary=self._budget_summary(settings),
            repository_backend=settings.repository_backend,
            run_real_llm_smoke=bool(settings.run_real_llm_smoke),
            note=(
                "PostgreSQL 持久化；API Key 仅环境变量；默认验收请保持 stub。"
                f" Kill Switch={'ON' if record.kill_switch else 'OFF'}."
            ),
        )

    def _assert_mode_ready(
        self, mode: LlmMode, readiness: list[ProviderReadinessItem]
    ) -> None:
        if mode == "stub":
            return
        if mode == "openrouter":
            item = next((r for r in readiness if r.name == "openrouter"), None)
            if item is None or not item.ready:
                raise AiRuntimeNotReadyException(
                    {
                        "mode": mode,
                        "reason": "openrouter provider not ready (key or models missing)",
                    }
                )
            return
        # fallback_chain：至少一个 provider ready（low + high 模型齐备）
        if not any(item.ready for item in readiness):
            raise AiRuntimeNotReadyException(
                {
                    "mode": mode,
                    "reason": "fallback_chain requires at least one ready provider",
                }
            )

    def _provider_readiness(self, settings: Settings) -> list[ProviderReadinessItem]:
        items: list[ProviderReadinessItem] = []
        items.append(
            ProviderReadinessItem(
                name="openrouter",
                ready=(
                    self._key_set(settings.openrouter_api_key)
                    and bool(settings.openrouter_low_cost_model)
                    and bool(settings.openrouter_high_quality_model)
                ),
                key_configured=self._key_set(settings.openrouter_api_key),
                low_cost_model=settings.openrouter_low_cost_model,
                high_quality_model=settings.openrouter_high_quality_model,
                enabled=bool(settings.openrouter_enabled)
                or self._key_set(settings.openrouter_api_key),
            )
        )
        items.append(
            ProviderReadinessItem(
                name="nvidia",
                ready=(
                    self._key_set(settings.nvidia_api_key)
                    and bool(settings.nvidia_low_cost_model)
                    and bool(settings.nvidia_high_quality_model)
                ),
                key_configured=self._key_set(settings.nvidia_api_key),
                low_cost_model=settings.nvidia_low_cost_model,
                high_quality_model=settings.nvidia_high_quality_model,
                enabled=bool(settings.nvidia_enabled)
                or self._key_set(settings.nvidia_api_key),
            )
        )
        items.append(
            ProviderReadinessItem(
                name="gemini",
                ready=(
                    self._key_set(settings.gemini_api_key)
                    and bool(settings.gemini_low_cost_model)
                    and bool(settings.gemini_high_quality_model)
                ),
                key_configured=self._key_set(settings.gemini_api_key),
                low_cost_model=settings.gemini_low_cost_model,
                high_quality_model=settings.gemini_high_quality_model,
                enabled=bool(settings.gemini_enabled)
                or self._key_set(settings.gemini_api_key),
            )
        )
        items.append(
            ProviderReadinessItem(
                name="local_qwen",
                ready=bool(
                    settings.local_qwen_enabled
                    and settings.local_qwen_low_cost_model
                    and settings.local_qwen_high_quality_model
                ),
                key_configured=False,
                low_cost_model=settings.local_qwen_low_cost_model,
                high_quality_model=settings.local_qwen_high_quality_model,
                enabled=bool(settings.local_qwen_enabled),
            )
        )
        return items

    def _display_models(
        self, settings: Settings, effective_mode: LlmMode
    ) -> tuple[str, str]:
        if effective_mode == "stub":
            return settings.llm_low_cost_model_name, settings.llm_high_quality_model_name
        if effective_mode == "openrouter":
            return (
                settings.openrouter_low_cost_model or settings.llm_low_cost_model_name,
                settings.openrouter_high_quality_model or settings.llm_high_quality_model_name,
            )
        # fallback_chain：展示第一个 ready provider 的模型，否则 stub 名
        for item in self._provider_readiness(settings):
            if item.ready and item.low_cost_model and item.high_quality_model:
                return item.low_cost_model, item.high_quality_model
        return settings.llm_low_cost_model_name, settings.llm_high_quality_model_name

    def _budget_summary(self, settings: Settings) -> dict[str, str]:
        return {
            "currency": settings.llm_currency,
            "low_request_max_cost": str(settings.llm_request_max_cost),
            "low_user_daily_cost_limit": str(settings.llm_user_daily_cost_limit),
            "low_global_daily_cost_limit": str(settings.llm_global_daily_cost_limit),
            "high_request_max_cost": str(settings.llm_hq_request_max_cost),
            "high_user_daily_cost_limit": str(settings.llm_hq_user_daily_cost_limit),
            "high_global_daily_cost_limit": str(settings.llm_hq_global_daily_cost_limit),
        }

    @staticmethod
    def _budget_config_valid(settings: Settings) -> bool:
        values = [
            settings.llm_request_max_cost,
            settings.llm_user_daily_cost_limit,
            settings.llm_global_daily_cost_limit,
            settings.llm_hq_request_max_cost,
            settings.llm_hq_user_daily_cost_limit,
            settings.llm_hq_global_daily_cost_limit,
        ]
        return all(isinstance(v, Decimal) and v >= 0 for v in values)

    @staticmethod
    def _key_set(secret) -> bool:
        if secret is None:
            return False
        try:
            return bool(secret.get_secret_value().strip())
        except Exception:
            return False


__all__ = [
    "AiRuntimeConfirmationRequiredException",
    "AiRuntimeNotReadyException",
    "AiRuntimeService",
    "AiRuntimeUnavailableException",
    "AiRuntimeVersionConflictException",
    "AiRuntimeView",
    "ProviderReadinessItem",
]
