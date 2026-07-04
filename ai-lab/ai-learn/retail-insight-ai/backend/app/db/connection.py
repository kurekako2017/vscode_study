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


class PostgresConnectionFactory:
    """封装 PostgreSQL 连接创建、UTC 时区设置与 schema 初始化。"""

    def __init__(self, config: PostgresConfig) -> None:
        """保存配置，真正连接时再导入 psycopg。"""

        self._config = config

    @contextmanager
    def connection(self) -> Iterator[object]:
        """返回一个带事务控制的连接；成功提交，异常回滚。"""

        psycopg = self._load_psycopg()
        connection = psycopg.connect(
            host=self._config.host,
            port=self._config.port,
            dbname=self._config.db,
            user=self._config.user,
            password=self._config.password,
        )
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
