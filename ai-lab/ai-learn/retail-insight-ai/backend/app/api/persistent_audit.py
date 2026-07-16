"""FastAPI Persistent Audit yield Dependency。

文件职责：
- 把 Route 声明的 action/resource/permission 转换为 PostgreSQL 审计事务。
- 从 JWT Dependency 写入的 request.state.current_user 读取真实 actor。

谁调用它：
- Documents、Retrieval、Analysis、Approval、Audit、Security Router。

它调用谁：
- AppContainer 中的 PersistentAuditService。

输入与输出：
- 输入 PersistentAuditSpec 和当前 Request；Dependency 本身不返回业务数据。

为什么这样设计：
- 每个 Router 只声明一次审计动作，成功/失败逻辑集中处理，避免重复记录。

日本现场面试怎么讲：
- FastAPI yield Dependency 相当于请求级事务拦截器，InMemory 模式会直接旁路。
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Callable

from fastapi import Request

from app.observability.logging import get_request_id
from app.security.contracts import CurrentUser
from app.services.persistent_audit_service import (
    PersistentAuditContext,
    PersistentAuditSpec,
)


def persistent_audit_dependency(
    spec: PersistentAuditSpec,
) -> Callable[[Request], AsyncIterator[None]]:
    """为一个 endpoint 创建 PostgreSQL-only 审计 Dependency。"""

    async def dependency(request: Request) -> AsyncIterator[None]:
        service = request.app.state.container.persistent_audit_service

        def context_provider() -> PersistentAuditContext:
            current_user = getattr(request.state, "current_user", None)
            if current_user is not None and not isinstance(current_user, CurrentUser):
                current_user = None
            resource_id = getattr(request.state, "audit_resource_id", None)
            if not resource_id and spec.resource_id_param is not None:
                resource_id = request.path_params.get(spec.resource_id_param)
            metadata = getattr(request.state, "audit_metadata", {})
            return PersistentAuditContext(
                request_id=get_request_id(),
                http_method=request.method,
                api_path=request.url.path,
                resource_id=str(resource_id or spec.resource_id),
                current_user=current_user,
                metadata=dict(metadata) if isinstance(metadata, dict) else {},
            )

        async with service.operation(spec, context_provider):
            yield

    return dependency


__all__ = ["persistent_audit_dependency"]
