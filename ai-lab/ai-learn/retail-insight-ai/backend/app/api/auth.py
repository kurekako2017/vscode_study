"""Login API。

文件职责：提供用户名密码登录并返回 JWT Access Token。
谁调用它：Swagger、测试或其他 HTTP 客户端。
它调用谁：AuthenticationService。
输入：LoginRequest。
输出：统一 ApiResponse[AccessTokenResponse]。
设计理由：路由不校验 hash、不构造 JWT，也不包含 RBAC 权限判断。
日本现场面试：Authentication -> Current User -> API，Authorization 后续独立追加。
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from app.observability.logging import get_logger, get_request_id, log_event
from app.schemas.auth import AccessTokenResponse, LoginRequest
from app.schemas.common import ApiResponse, success_response
from app.security.authentication import AuthenticationService

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])
logger = get_logger(__name__)


async def get_authentication_service(request: Request) -> AuthenticationService:
    """从应用组合根注入认证服务。"""

    return request.app.state.container.authentication_service


@router.post("/login", response_model=ApiResponse[AccessTokenResponse])
async def login(
    payload: LoginRequest,
    service: AuthenticationService = Depends(get_authentication_service),
) -> ApiResponse[AccessTokenResponse]:
    """验证用户名密码并签发 Bearer Access Token。"""

    token = service.login(payload.username, payload.password.get_secret_value())
    log_event(
        logger,
        "info",
        "authentication_login_succeeded",
        "User authentication succeeded",
        status="success",
    )
    return success_response(AccessTokenResponse.from_contract(token), get_request_id())
