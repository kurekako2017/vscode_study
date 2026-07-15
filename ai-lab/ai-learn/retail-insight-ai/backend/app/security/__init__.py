"""Enterprise Security package 的延迟加载公开边界。

本目录集中维护 Authentication 与 Authorization，但保持两条职责链独立：JWT 只生成
``CurrentUser``，RBAC 再由服务端 Registry 解析权限。延迟加载避免导入单个安全合同
时触发 FastAPI schema 初始化，谁调用公开对象都只加载实际需要的模块。
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

# 公开名称到真实模块的映射；这不是 permission matrix，只是 Python package export 表。
_EXPORTS = {
    "AccessToken": ("app.security.contracts", "AccessToken"),
    "AuthenticationService": (
        "app.security.authentication",
        "AuthenticationService",
    ),
    "AuthorizationResult": (
        "app.security.rbac_contracts",
        "AuthorizationResult",
    ),
    "AuthorizationService": (
        "app.security.authorization_service",
        "AuthorizationService",
    ),
    "CurrentUser": ("app.security.contracts", "CurrentUser"),
    "JWTProvider": ("app.security.jwt_provider", "JWTProvider"),
    "JWTService": ("app.security.jwt_service", "JWTService"),
    "Permission": ("app.security.rbac_contracts", "Permission"),
    "PermissionChecker": (
        "app.security.rbac_contracts",
        "PermissionChecker",
    ),
    "PermissionRegistry": (
        "app.security.permission_registry",
        "PermissionRegistry",
    ),
    "PermissionResolver": (
        "app.security.permission_resolver",
        "PermissionResolver",
    ),
    "PyJWTProvider": ("app.security.jwt_provider", "PyJWTProvider"),
    "Role": ("app.security.rbac_contracts", "Role"),
    "RoleMapping": ("app.security.rbac_contracts", "RoleMapping"),
    "TokenPayload": ("app.security.contracts", "TokenPayload"),
}


def __getattr__(name: str) -> Any:
    """首次访问公开对象时才导入对应实现，并缓存到 package namespace。"""

    target = _EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attribute_name = target
    value = getattr(import_module(module_name), attribute_name)
    globals()[name] = value
    return value

__all__ = [
    "AccessToken",
    "AuthenticationService",
    "AuthorizationResult",
    "AuthorizationService",
    "CurrentUser",
    "JWTProvider",
    "JWTService",
    "Permission",
    "PermissionChecker",
    "PermissionRegistry",
    "PermissionResolver",
    "PyJWTProvider",
    "Role",
    "RoleMapping",
    "TokenPayload",
]
