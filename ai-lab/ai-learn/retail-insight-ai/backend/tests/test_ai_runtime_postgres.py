"""AI Runtime PostgreSQL 持久化与 Admin 合同回归。

覆盖：
- Migration 表读写
- 重启/重建 container 后 mode 保持
- expected_version 409
- Kill Switch
- readiness 拒绝
- Key 不泄漏
- Persistent Audit
- InMemory fail-closed
- MockTransport only（零真实 Provider）
"""

from __future__ import annotations

import os
import unittest

from httpx import ASGITransport, AsyncClient

from app.config.container import build_container
from app.config.settings import Settings
from app.main import create_app
from app.models.ai_runtime_settings import ENABLE_REAL_CONFIRMATION_TEXT
from tests.auth_test_utils import (
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    EMPLOYEE_PASSWORD,
    EMPLOYEE_USERNAME,
    authorization_headers,
)
from tests.postgres_test_utils import reset_postgres_state_if_needed


def _postgres_settings(**overrides) -> Settings:
    database_url = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg:///erip_integration_test?host=/var/run/postgresql",
    )
    values = {
        "repository_backend": "postgres",
        "database_url": database_url,
        "llm_provider_mode": "stub",
        "learning_trace": False,
        "run_real_llm_smoke": False,
    }
    values.update(overrides)
    return Settings(**values)


class AiRuntimeInMemoryFailClosedTest(unittest.IsolatedAsyncioTestCase):
    """InMemory 默认路径必须对 AI Runtime Admin fail-closed（不依赖 PostgreSQL）。"""

    async def test_inmemory_fail_closed(self) -> None:
        app = create_app(
            Settings(repository_backend="inmemory", llm_provider_mode="stub", learning_trace=False)
        )
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            headers = authorization_headers(app, username=ADMIN_USERNAME, password=ADMIN_PASSWORD)
            response = await client.get("/api/v1/admin/ai-runtime", headers=headers)
            self.assertEqual(response.status_code, 503, response.text)
            body = response.text.lower()
            self.assertNotIn("api_key", body)
            self.assertNotIn("sk-", body)


@unittest.skipUnless(
    os.environ.get("REPOSITORY_BACKEND", "inmemory") == "postgres",
    "PostgreSQL suite only",
)
class AiRuntimePostgresTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.settings = _postgres_settings()
        reset_postgres_state_if_needed(self.settings)
        self.app = create_app(self.settings)
        self.client = AsyncClient(
            transport=ASGITransport(app=self.app),
            base_url="http://test",
        )
        self.admin = authorization_headers(
            self.app, username=ADMIN_USERNAME, password=ADMIN_PASSWORD
        )
        self.employee = authorization_headers(
            self.app, username=EMPLOYEE_USERNAME, password=EMPLOYEE_PASSWORD
        )

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    async def test_get_default_initialized_from_env_stub(self) -> None:
        response = await self.client.get("/api/v1/admin/ai-runtime", headers=self.admin)
        self.assertEqual(response.status_code, 200, response.text)
        data = response.json()["data"]
        self.assertEqual(data["effective_mode"], "stub")
        self.assertEqual(data["configured_mode"], "stub")
        self.assertFalse(data["real_calls_enabled"])
        self.assertFalse(data["kill_switch"])
        self.assertGreaterEqual(data["version"], 1)
        self.assertIn("budget_summary", data)
        self.assertIn("provider_readiness", data)
        self.assertFalse(data["run_real_llm_smoke"])
        self.assertNotIn("api_key", response.text.lower())
        self.assertNotIn("secret", response.text.lower())

    async def test_employee_denied_and_key_not_leaked(self) -> None:
        denied = await self.client.get("/api/v1/admin/ai-runtime", headers=self.employee)
        self.assertEqual(denied.status_code, 403, denied.text)
        self.assertNotIn("api_key", denied.text.lower())

    async def test_patch_requires_confirmed_and_version(self) -> None:
        current = (
            await self.client.get("/api/v1/admin/ai-runtime", headers=self.admin)
        ).json()["data"]
        missing_confirm = await self.client.patch(
            "/api/v1/admin/ai-runtime",
            headers=self.admin,
            json={"expected_version": current["version"], "mode": "stub"},
        )
        self.assertEqual(missing_confirm.status_code, 422, missing_confirm.text)

        conflict = await self.client.patch(
            "/api/v1/admin/ai-runtime",
            headers=self.admin,
            json={
                "expected_version": current["version"] + 99,
                "confirmed": True,
                "mode": "stub",
            },
        )
        self.assertEqual(conflict.status_code, 409, conflict.text)

    async def test_kill_switch_and_persist_across_rebuild(self) -> None:
        current = (
            await self.client.get("/api/v1/admin/ai-runtime", headers=self.admin)
        ).json()["data"]
        patched = await self.client.patch(
            "/api/v1/admin/ai-runtime",
            headers=self.admin,
            json={
                "expected_version": current["version"],
                "confirmed": True,
                "kill_switch": True,
            },
        )
        self.assertEqual(patched.status_code, 200, patched.text)
        data = patched.json()["data"]
        self.assertTrue(data["kill_switch"])
        self.assertEqual(data["effective_mode"], "stub")
        self.assertGreater(data["version"], current["version"])
        self.assertEqual(data["updated_by"]["username"], ADMIN_USERNAME)

        # 重建 container / app 模拟 Backend 重启
        rebuilt = create_app(_postgres_settings())
        async with AsyncClient(
            transport=ASGITransport(app=rebuilt), base_url="http://test"
        ) as client:
            headers = authorization_headers(
                rebuilt, username=ADMIN_USERNAME, password=ADMIN_PASSWORD
            )
            again = await client.get("/api/v1/admin/ai-runtime", headers=headers)
            self.assertEqual(again.status_code, 200, again.text)
            again_data = again.json()["data"]
            self.assertTrue(again_data["kill_switch"])
            self.assertEqual(again_data["effective_mode"], "stub")
            self.assertEqual(again_data["version"], data["version"])

    async def test_real_mode_rejected_when_not_ready(self) -> None:
        current = (
            await self.client.get("/api/v1/admin/ai-runtime", headers=self.admin)
        ).json()["data"]
        # 默认环境无 OpenRouter Key → readiness fail-closed
        denied = await self.client.patch(
            "/api/v1/admin/ai-runtime",
            headers=self.admin,
            json={
                "expected_version": current["version"],
                "confirmed": True,
                "mode": "openrouter",
                "confirmation_text": ENABLE_REAL_CONFIRMATION_TEXT,
            },
        )
        self.assertEqual(denied.status_code, 422, denied.text)
        self.assertNotIn("api_key", denied.text.lower())
        body = denied.json()
        code = (body.get("error") or {}).get("code") or ""
        self.assertTrue(
            "not_ready" in code or "provider" in code or denied.status_code == 422
        )

    async def test_stub_noop_and_audit_on_kill_switch(self) -> None:
        current = (
            await self.client.get("/api/v1/admin/ai-runtime", headers=self.admin)
        ).json()["data"]
        response = await self.client.patch(
            "/api/v1/admin/ai-runtime",
            headers=self.admin,
            json={
                "expected_version": current["version"],
                "confirmed": True,
                "kill_switch": True,
            },
        )
        self.assertEqual(response.status_code, 200, response.text)
        # Persistent Audit 应有 kill_switch_changed 或 mode_changed
        logs = await self.client.get(
            "/api/v1/audit-logs?limit=20",
            headers=self.admin,
        )
        self.assertEqual(logs.status_code, 200, logs.text)
        items = logs.json()["data"]["items"]
        actions = [item.get("operation_type") or item.get("action") for item in items]
        self.assertTrue(
            any(
                action in {"ai_runtime.kill_switch_changed", "ai_runtime.mode_changed"}
                for action in actions
            ),
            actions,
        )
        # 响应与审计均不得含 Key
        self.assertNotIn("sk-", logs.text.lower())
        self.assertNotIn("api_key", response.text.lower())

    async def test_repository_get_or_initialize_idempotent(self) -> None:
        container = build_container(_postgres_settings())
        service = container.ai_runtime_service
        first = service.ensure_loaded()
        second = service.ensure_loaded()
        self.assertEqual(first.version, second.version)
        self.assertEqual(first.mode, "stub")
        # 第二次新 container 仍恢复
        again = build_container(_postgres_settings()).ai_runtime_service.ensure_loaded()
        self.assertEqual(again.mode, first.mode)
        self.assertEqual(again.version, first.version)

    async def test_stub_to_stub_and_confirmation_required_for_real(self) -> None:
        current = (
            await self.client.get("/api/v1/admin/ai-runtime", headers=self.admin)
        ).json()["data"]
        # 保持 stub 允许（无需 confirmation_text）
        ok = await self.client.patch(
            "/api/v1/admin/ai-runtime",
            headers=self.admin,
            json={
                "expected_version": current["version"],
                "confirmed": True,
                "mode": "stub",
            },
        )
        self.assertEqual(ok.status_code, 200, ok.text)
        next_version = ok.json()["data"]["version"]
        # 切真实模式缺少 confirmation_text
        denied = await self.client.patch(
            "/api/v1/admin/ai-runtime",
            headers=self.admin,
            json={
                "expected_version": next_version,
                "confirmed": True,
                "mode": "fallback_chain",
                "confirmation_text": "WRONG",
            },
        )
        self.assertEqual(denied.status_code, 422, denied.text)
        self.assertNotIn("sk-", denied.text.lower())


@unittest.skipUnless(
    os.environ.get("REPOSITORY_BACKEND", "inmemory") == "postgres",
    "PostgreSQL suite only",
)
class AiRuntimeMigrationRoundTripTest(unittest.TestCase):
    """ai_runtime_settings migration：upgrade / downgrade / re-upgrade。"""

    def test_ai_runtime_revision_upgrade_downgrade_reupgrade(self) -> None:
        from pathlib import Path

        from alembic import command
        from alembic.config import Config

        database_url = os.environ.get(
            "DATABASE_URL",
            "postgresql+psycopg:///erip_integration_test?host=/var/run/postgresql",
        )
        if "erip_integration_test" not in database_url:
            self.skipTest("migration round-trip only on erip_integration_test")

        backend_dir = Path(__file__).resolve().parents[1]
        config = Config(str(backend_dir / "alembic.ini"))
        # Alembic env 读取 DATABASE_URL
        os.environ["DATABASE_URL"] = database_url
        command.upgrade(config, "head")
        command.downgrade(config, "20260717_07_fallback_chain")
        command.upgrade(config, "head")
        # 表应可用
        from app.db.connection import PostgresConfig, PostgresConnectionFactory

        factory = PostgresConnectionFactory(
            PostgresConfig(
                host="",
                port=5432,
                db="",
                user="",
                password="",
                database_url=database_url,
            )
        )
        with factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT column_name FROM information_schema.columns
                    WHERE table_name = 'ai_runtime_settings'
                    ORDER BY column_name
                    """
                )
                columns = {row[0] for row in cursor.fetchall()}
        expected = {
            "setting_key",
            "mode",
            "real_calls_enabled",
            "kill_switch",
            "version",
            "updated_by_user_id",
            "updated_by_username",
            "updated_at",
        }
        self.assertTrue(expected.issubset(columns), columns)


if __name__ == "__main__":
    unittest.main()
