"""Audit service.

文件职责：
- 负责审计日志追加和只读查询。
- 在追加成功或失败时记录 `audit.log.created` / `audit.log.failed` 的结构化日志。

谁会调用它：
- `backend/app/api/audit_logs.py` 路由，以及未来任何需要写审计事实的业务服务。

它调用谁：
- 只调用 `AuditRepository` 和结构化日志工具，不依赖 HTTP 或数据库实现。

输入是什么：
- 审计操作类型、actor、资源、request_id、trace_id、metadata。

输出是什么：
- 已追加的 AuditLog，或审计日志列表。

为什么需要这一层：
- 审计写入逻辑集中在 service，路由只负责触发，不把 append 细节散落在多处。

日本现场面试怎么讲：
- 这是 audit trail 的写入口，记录成功和失败，但不暴露敏感正文。
"""

from __future__ import annotations

from typing import Any

from app.errors.exceptions import AuditLogAppendException
from app.models.audit import AuditLog, AuditLogResult
from app.observability.logging import get_logger, get_request_id, log_event
from app.repositories.interfaces.audit_repository import AuditRepository

logger = get_logger(__name__)


class AuditService:
    """封装审计事实的写入与读取。"""

    def __init__(self, repository: AuditRepository) -> None:
        """注入审计仓库接口，避免 service 绑定内存实现。"""

        self._repository = repository

    def record_audit_log(
        self,
        *,
        operation_type: str,
        actor_id: str | None,
        organization_id: str | None,
        department_id: str | None,
        resource_type: str,
        resource_id: str,
        result: AuditLogResult,
        request_id: str | None = None,
        trace_id: str,
        metadata: dict[str, Any] | None = None,
        error_code: str | None = None,
    ) -> AuditLog:
        """创建一条审计事实，并在失败时保留安全日志。"""

        log = AuditLog(
            operation_type=operation_type,
            actor_id=actor_id,
            organization_id=organization_id,
            department_id=department_id,
            resource_type=resource_type,
            resource_id=resource_id,
            result=result,
            request_id=request_id or get_request_id(),
            trace_id=trace_id,
            metadata=dict(metadata or {}),
            error_code=error_code,
        )
        try:
            stored = self._repository.append(log)
        except Exception as exc:  # pragma: no cover - repository failure path is covered by service tests
            log_event(
                logger,
                "error",
                "audit.log.failed",
                "Audit log append failed",
                request_id=log.request_id,
                task_id=log.audit_log_id,
                error_code="audit_log_failed",
                status="failed",
            )
            raise AuditLogAppendException(
                log.audit_log_id,
                detail={
                    "operation_type": operation_type,
                    "resource_type": resource_type,
                    "resource_id": resource_id,
                    "exception_type": type(exc).__name__,
                },
            ) from exc
        log_event(
            logger,
            "info",
            "audit.log.created",
            "Audit log appended",
            request_id=stored.request_id,
            task_id=stored.audit_log_id,
            status="created",
        )
        return stored

    def list_audit_logs(self) -> list[AuditLog]:
        """按追加顺序读取审计事实。"""

        return self._repository.list_all()
