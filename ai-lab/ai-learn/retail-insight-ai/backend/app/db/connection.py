"""PostgreSQL 连接层。

文件职责：
- 为 PostgreSQL Repository 提供统一连接与事务边界。
- 当前由 `backend/app/config/container.py` 在组合根创建。
- 当前只服务 Task / Event / Report 持久化，不接审批 API。

谁调用它：
- `backend/app/repositories/postgres/` 下的 Repository。
- `build_container()` 在 postgres 模式下调用 `initialize_schema()`。

它调用谁：
- `psycopg` 驱动，采用延迟导入，避免 InMemory 模式因为缺少依赖而失败。

输入：
- Settings 中的 PostgreSQL 主机、端口、数据库、用户、密码。

输出：
- 带 UTC 时区设置的数据库连接。

为什么这样设计：
- 让 Repository 只关心 SQL，不关心连接细节、时区设置和事务收敛。

日本现场面试怎么讲：
- 这是典型的 Infrastructure Adapter。当前保持同步阻塞实现，先把事务事实持久化打通，
  后续再考虑连接池、重试、超时和迁移工具。
"""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


@dataclass(frozen=True)
class PostgresConfig:
    """保存 PostgreSQL 连接参数。"""

    host: str
    port: int
    db: str
    user: str
    password: str
    database_url: str | None = None


class PostgresConnectionFactory:
    """封装 PostgreSQL 连接创建、UTC 时区设置与 schema 初始化。"""

    def __init__(self, config: PostgresConfig) -> None:
        """保存配置，真正连接时再导入 psycopg。"""

        self._config = config
        # 同一调用链中的 Repository 共享连接，才能由 Unit of Work 统一提交或回滚。
        self._active_connection: ContextVar[object | None] = ContextVar(
            "postgres_active_connection",
            default=None,
        )

    @contextmanager
    def connection(self) -> Iterator[object]:
        """返回一个带事务控制的连接；成功提交，异常回滚。"""

        active = self._active_connection.get()
        if active is not None:
            yield active
            return

        psycopg = self._load_psycopg()
        connection = self._connect(psycopg)
        try:
            with connection.cursor() as cursor:
                cursor.execute("SET TIME ZONE 'UTC'")
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    @contextmanager
    def transaction(self) -> Iterator[None]:
        """开启可嵌套事务；内部 Repository 自动复用当前连接。"""

        active = self._active_connection.get()
        if active is not None:
            # psycopg 的嵌套 transaction 会创建 savepoint。
            # 这样请求级 Persistent Audit 可以包住业务调用，而业务 Service 自己的
            # Unit of Work 在失败时仍只回滚自身写入，不会吞掉外层 failure audit。
            with active.transaction():
                yield
            return

        psycopg = self._load_psycopg()
        connection = self._connect(psycopg)
        token = self._active_connection.set(connection)
        try:
            with connection.cursor() as cursor:
                cursor.execute("SET TIME ZONE 'UTC'")
            yield
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            self._active_connection.reset(token)
            connection.close()

    def health_check(self) -> None:
        """执行真实连通性检查；失败直接抛出，禁止静默回退。"""

        with self.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                if cursor.fetchone() != (1,):
                    raise RuntimeError("PostgreSQL health check returned an unexpected result")

    def initialize_schema(self, schema_path: Path) -> None:
        """执行 schema.sql；使用 IF NOT EXISTS 保证可重复执行。"""

        sql = schema_path.read_text(encoding="utf-8")
        with self.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)

    def _load_psycopg(self):
        """延迟导入 psycopg，避免 InMemory 模式启动时依赖缺失。"""

        try:
            import psycopg
        except ImportError as exc:
            raise RuntimeError(
                "psycopg is required when REPOSITORY_BACKEND=postgres"
            ) from exc
        return psycopg

    def _connect(self, psycopg):
        """兼容 SQLAlchemy 风格 psycopg URL 与离散连接参数。"""

        if self._config.database_url:
            url = self._config.database_url.replace("postgresql+psycopg://", "postgresql://", 1)
            return psycopg.connect(url)
        return psycopg.connect(
            host=self._config.host,
            port=self._config.port,
            dbname=self._config.db,
            user=self._config.user,
            password=self._config.password,
        )
