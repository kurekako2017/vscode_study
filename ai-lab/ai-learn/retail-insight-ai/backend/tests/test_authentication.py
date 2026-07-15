"""Enterprise JWT Authentication 的合同、错误回退与 OpenAPI 测试。"""

from __future__ import annotations

import unittest
from datetime import datetime, timedelta, timezone

import httpx

from app.config.settings import Settings
from app.main import create_app
from app.security.config import JWTConfig
from app.security.contracts import CurrentUser, TokenPayload
from app.security.errors import TokenExpiredError, UnauthorizedError
from app.security.jwt_provider import PyJWTProvider
from app.security.jwt_service import JWTService
from app.security.password import PasswordService
from app.security.user_provider import DeterministicTestUserProvider
from tests.auth_test_utils import (
    ADMIN_PASSWORD,
    EMPLOYEE_PASSWORD,
    MANAGER_PASSWORD,
    authorization_headers,
)


class AuthenticationUnitTest(unittest.TestCase):
    """验证密码、JWT 生成解析和安全失败分类。"""

    def setUp(self) -> None:
        self.config = JWTConfig(
            secret_key="unit-test-jwt-secret-key-with-at-least-32-bytes",
            algorithm="HS256",
            access_token_expire_minutes=30,
        )
        self.provider = PyJWTProvider(self.config)
        self.service = JWTService(self.provider, self.config)
        self.user = CurrentUser(
            user_id="user-admin", username="admin", role="admin"
        )

    def test_password_verification_uses_bcrypt_hash(self) -> None:
        user = DeterministicTestUserProvider().get_by_username("admin")
        self.assertIsNotNone(user)
        assert user is not None
        self.assertTrue(PasswordService().verify(ADMIN_PASSWORD, user.password_hash))
        self.assertFalse(PasswordService().verify("wrong-password", user.password_hash))
        self.assertTrue(user.password_hash.startswith("$2b$"))

    def test_jwt_generation_contains_frozen_payload_and_unique_jti(self) -> None:
        first = self.service.create_access_token(self.user)
        second = self.service.create_access_token(self.user)
        payload = self.service.parse_token(first.access_token)

        self.assertEqual(first.token_type, "bearer")
        self.assertEqual(first.expires_in, 1800)
        self.assertEqual(payload.sub, "user-admin")
        self.assertEqual(payload.user_id, "user-admin")
        self.assertEqual(payload.username, "admin")
        self.assertEqual(payload.role, "admin")
        self.assertNotEqual(
            payload.jti, self.service.parse_token(second.access_token).jti
        )

    def test_jwt_parse_returns_current_user(self) -> None:
        token = self.service.create_access_token(self.user)
        self.assertEqual(self.service.get_current_user(token.access_token), self.user)

    def test_expired_token_raises_token_expired(self) -> None:
        now = datetime.now(timezone.utc)
        expired = TokenPayload(
            sub="user-admin",
            user_id="user-admin",
            username="admin",
            role="admin",
            iat=now - timedelta(minutes=31),
            exp=now - timedelta(minutes=1),
            jti="expired-token-id",
        )
        token = self.provider.encode(expired.model_dump(mode="python"))

        with self.assertRaises(TokenExpiredError):
            self.service.parse_token(token)

    def test_invalid_signature_raises_unauthorized(self) -> None:
        foreign_config = JWTConfig(
            secret_key="different-signing-secret-key-with-at-least-32-bytes",
            algorithm="HS256",
            access_token_expire_minutes=30,
        )
        token = JWTService(
            PyJWTProvider(foreign_config), foreign_config
        ).create_access_token(self.user)

        with self.assertRaises(UnauthorizedError):
            self.service.parse_token(token.access_token)


class AuthenticationAPITest(unittest.IsolatedAsyncioTestCase):
    """验证 Login、Current User、Protected API、Bearer 与 Swagger。"""

    async def asyncSetUp(self) -> None:
        self.app = create_app(Settings(log_level="CRITICAL"))
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=self.app), base_url="http://test"
        )

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    async def test_login_success(self) -> None:
        response = await self.client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": ADMIN_PASSWORD},
        )
        self.assertEqual(response.status_code, 200)
        token = response.json()["data"]
        self.assertEqual(token["token_type"], "bearer")
        self.assertEqual(token["expires_in"], 1800)
        self.assertTrue(token["access_token"])

    async def test_three_deterministic_test_users_can_login(self) -> None:
        for username, password, role in (
            ("admin", ADMIN_PASSWORD, "admin"),
            ("manager", MANAGER_PASSWORD, "manager"),
            ("employee", EMPLOYEE_PASSWORD, "employee"),
        ):
            with self.subTest(username=username):
                response = await self.client.post(
                    "/api/v1/auth/login",
                    json={"username": username, "password": password},
                )
                self.assertEqual(response.status_code, 200)
                token = response.json()["data"]["access_token"]
                payload = self.app.state.container.jwt_service.parse_token(token)
                self.assertEqual(payload.role, role)

    async def test_login_failure_is_401_without_password_leak(self) -> None:
        response = await self.client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "wrong-password"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers["www-authenticate"], "Bearer")
        payload = response.json()
        self.assertEqual(payload["error"]["code"], "invalid_credentials")
        self.assertNotIn("wrong-password", response.text)

    async def test_missing_token_is_401(self) -> None:
        response = await self.client.get("/api/tasks/missing")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"]["code"], "unauthorized")
        self.assertEqual(response.headers["www-authenticate"], "Bearer")

    async def test_bearer_header_reaches_protected_api(self) -> None:
        response = await self.client.get(
            "/api/tasks/missing", headers=authorization_headers(self.app)
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"]["code"], "TASK_NOT_FOUND")

    async def test_current_user_comes_from_token(self) -> None:
        response = await self.client.get(
            "/api/v1/users/me", headers=authorization_headers(self.app)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["data"],
            {"user_id": "user-admin", "username": "admin", "role": "admin"},
        )

    async def test_invalid_bearer_signature_is_401(self) -> None:
        response = await self.client.get(
            "/api/tasks/missing",
            headers={"Authorization": "Bearer invalid.jwt.signature"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"]["code"], "unauthorized")

    async def test_expired_bearer_token_is_401_not_500(self) -> None:
        now = datetime.now(timezone.utc)
        expired = TokenPayload(
            sub="user-admin",
            user_id="user-admin",
            username="admin",
            role="admin",
            iat=now - timedelta(minutes=31),
            exp=now - timedelta(minutes=1),
            jti="expired-api-token-id",
        )
        settings = self.app.state.container.settings
        config = JWTConfig(
            secret_key=settings.jwt_secret_key.get_secret_value(),
            algorithm=settings.jwt_algorithm,
            access_token_expire_minutes=settings.jwt_access_token_expire_minutes,
        )
        token = PyJWTProvider(config).encode(expired.model_dump(mode="python"))

        response = await self.client.get(
            "/api/tasks/missing",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"]["code"], "token_expired")

    async def test_swagger_declares_bearer_security(self) -> None:
        schema = self.app.openapi()
        bearer = schema["components"]["securitySchemes"]["BearerAuth"]
        self.assertEqual(bearer["type"], "http")
        self.assertEqual(bearer["scheme"], "bearer")
        self.assertEqual(bearer["bearerFormat"], "JWT")
        self.assertEqual(
            schema["paths"]["/api/tasks"]["post"]["security"],
            [{"BearerAuth": []}],
        )
        self.assertNotIn(
            "security", schema["paths"]["/api/v1/auth/login"]["post"]
        )


if __name__ == "__main__":
    unittest.main()
