"""Enterprise RBAC Authorization 的合同、Dependency 与 API 权限矩阵测试。

文件职责：覆盖 Role Mapping、Resolver、Authorization Service、403 与受保护 API。
谁调用它：unittest discovery；InMemory/PostgreSQL 两套 baseline 都执行同一组测试。
它调用谁：真实 AppContainer、JWTService 和 FastAPI 路由，不替换授权 Dependency。
输入：不同 role 的合法 Bearer Token。
输出：允许路径继续进入业务 API，拒绝路径稳定返回 forbidden/permission/role。
设计理由：使用真实 Token → CurrentUser → RBAC 链验证，不降低既有业务断言。
日本现场面试：同一测试可在双 Repository Backend 运行，证明授权不依赖持久层。
"""

from __future__ import annotations

import unittest

import httpx

from app.config.settings import Settings
from app.main import create_app
from app.security.authorization_service import AuthorizationService
from app.security.contracts import CurrentUser
from app.security.errors import ForbiddenError
from app.security.permission_registry import PermissionRegistry
from app.security.permission_resolver import PermissionResolver
from app.security.rbac_contracts import Permission, PermissionChecker, Role
from tests.auth_test_utils import ADMIN_PASSWORD
from tests.postgres_test_utils import reset_postgres_state_if_needed


class AuthorizationUnitTest(unittest.TestCase):
    """验证集中目录、解析器、Checker Contract 与 fail-closed 行为。"""

    def setUp(self) -> None:
        self.registry = PermissionRegistry()
        self.resolver = PermissionResolver(self.registry)
        self.service = AuthorizationService(self.resolver, self.registry)

    def test_role_mapping_is_centralized_and_complete(self) -> None:
        mappings = self.registry.list_role_mappings()
        self.assertEqual([item.role for item in mappings], list(Role))
        self.assertEqual(
            self.resolver.resolve(Role.ADMIN.value), frozenset(Permission)
        )
        self.assertIn(
            Permission.APPROVAL_ADMIN,
            self.resolver.resolve(Role.MANAGER.value),
        )
        self.assertNotIn(
            Permission.AUDIT_READ,
            self.resolver.resolve(Role.EMPLOYEE.value),
        )

    def test_permission_resolver_denies_unknown_role(self) -> None:
        self.assertEqual(self.resolver.resolve("unknown-role"), frozenset())

    def test_authorization_service_satisfies_permission_checker(self) -> None:
        checker: PermissionChecker = self.service
        user = CurrentUser(
            user_id="user-employee", username="employee", role="employee"
        )
        result = checker.check_permission(user, Permission.DOCUMENTS_READ)
        self.assertTrue(result.allowed)
        self.assertEqual(result.permission, Permission.DOCUMENTS_READ)
        self.assertEqual(result.role, "employee")

    def test_authorization_service_raises_forbidden_with_context(self) -> None:
        user = CurrentUser(
            user_id="user-employee", username="employee", role="employee"
        )
        with self.assertRaises(ForbiddenError) as context:
            self.service.require_permission(user, Permission.SECURITY_MANAGE)
        self.assertEqual(context.exception.permission, "security.manage")
        self.assertEqual(context.exception.role, "employee")


class AuthorizationAPITest(unittest.IsolatedAsyncioTestCase):
    """通过真实 FastAPI Dependency 验证角色到 API 的授权矩阵。"""

    async def asyncSetUp(self) -> None:
        settings = Settings(log_level="CRITICAL")
        reset_postgres_state_if_needed(settings)
        self.app = create_app(settings)
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=self.app), base_url="http://test"
        )

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    def _headers(self, role: str) -> dict[str, str]:
        """直接签发真实测试 JWT，避免把 API 授权测试耦合到密码验证耗时。"""

        current_user = CurrentUser(
            user_id=f"user-{role}", username=role, role=role
        )
        token = self.app.state.container.jwt_service.create_access_token(current_user)
        return {"Authorization": f"Bearer {token.access_token}"}

    def _assert_forbidden(
        self, response: httpx.Response, permission: Permission, role: str
    ) -> None:
        """统一断言 403 envelope，不把权限不足误判为 401 或 500。"""

        self.assertEqual(response.status_code, 403)
        self.assertNotIn("www-authenticate", response.headers)
        error = response.json()["error"]
        self.assertEqual(error["code"], "forbidden")
        self.assertEqual(error["detail"]["permission"], permission.value)
        self.assertEqual(error["detail"]["role"], role)

    async def test_health_and_login_remain_anonymous(self) -> None:
        health = await self.client.get("/health")
        login = await self.client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": ADMIN_PASSWORD},
        )
        self.assertEqual(health.status_code, 200)
        self.assertEqual(login.status_code, 200)

    async def test_current_user_requires_authentication_but_no_extra_permission(self) -> None:
        response = await self.client.get(
            "/api/v1/users/me", headers=self._headers("employee")
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["role"], "employee")

    async def test_documents_permission_allows_read_and_denies_archive(self) -> None:
        headers = self._headers("employee")
        read_response = await self.client.get("/api/v1/documents", headers=headers)
        archive_response = await self.client.delete(
            "/api/v1/documents/missing-document", headers=headers
        )
        self.assertEqual(read_response.status_code, 200)
        self._assert_forbidden(
            archive_response, Permission.DOCUMENTS_ARCHIVE, "employee"
        )

    async def test_retrieval_permission_allows_employee_query(self) -> None:
        response = await self.client.post(
            "/api/v1/document-retrieval/search",
            headers=self._headers("employee"),
            json={"query": "sales", "retrieval_mode": "keyword"},
        )
        self.assertEqual(response.status_code, 200)

    async def test_approval_permissions_separate_submit_review_and_admin(self) -> None:
        headers = self._headers("employee")
        submit = await self.client.post(
            "/api/v1/reports/missing-task/submit-approval",
            headers=headers,
            json={"comment": "review"},
        )
        review = await self.client.get("/api/v1/approvals", headers=headers)
        admin = await self.client.post(
            "/api/v1/approvals/missing-approval/approve",
            headers=headers,
            json={"comment": "approve"},
        )
        self.assertNotEqual(submit.status_code, 403)
        self._assert_forbidden(review, Permission.APPROVAL_REVIEW, "employee")
        self._assert_forbidden(admin, Permission.APPROVAL_ADMIN, "employee")

    async def test_audit_and_security_permissions_are_distinct(self) -> None:
        manager_headers = self._headers("manager")
        audit = await self.client.get(
            "/api/v1/audit-logs", headers=manager_headers
        )
        security = await self.client.get(
            "/api/v1/security/roles", headers=manager_headers
        )
        self.assertEqual(audit.status_code, 200)
        self._assert_forbidden(
            security, Permission.SECURITY_MANAGE, "manager"
        )

    async def test_unknown_role_is_denied_instead_of_raising_500(self) -> None:
        response = await self.client.get(
            "/api/v1/documents", headers=self._headers("contractor")
        )
        self._assert_forbidden(
            response, Permission.DOCUMENTS_READ, "contractor"
        )

    async def test_swagger_keeps_bearer_on_permission_protected_apis(self) -> None:
        schema = self.app.openapi()
        for path, method in (
            ("/api/v1/documents", "get"),
            ("/api/v1/document-retrieval/search", "post"),
            ("/api/v1/approvals", "get"),
            ("/api/v1/audit-logs", "get"),
        ):
            self.assertEqual(
                schema["paths"][path][method]["security"],
                [{"BearerAuth": []}],
            )
        self.assertNotIn("security", schema["paths"]["/health"]["get"])
        self.assertNotIn(
            "security", schema["paths"]["/api/v1/auth/login"]["post"]
        )


if __name__ == "__main__":
    unittest.main()
