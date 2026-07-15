"""认证测试辅助函数；只在测试环境持有 deterministic user 的验收密码。"""

from __future__ import annotations

from fastapi import FastAPI

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Admin#2026!"
MANAGER_USERNAME = "manager"
MANAGER_PASSWORD = "Manager#2026!"
EMPLOYEE_USERNAME = "employee"
EMPLOYEE_PASSWORD = "Employee#2026!"


def authorization_headers(
    application: FastAPI,
    *,
    username: str = ADMIN_USERNAME,
    password: str = ADMIN_PASSWORD,
) -> dict[str, str]:
    """通过真实 AuthenticationService 取得测试 Bearer Header。"""

    token = application.state.container.authentication_service.login(
        username, password
    )
    return {"Authorization": f"Bearer {token.access_token}"}
