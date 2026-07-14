"""ERIP Alembic 空基线。

文件职责：
- 为未来 migration 提供标准 offline / online 运行入口。
- 只从当前进程读取 DATABASE_URL，不读取或修改项目 .env。

谁调用它：
- Alembic CLI 在未来执行 revision / upgrade 等显式命令时调用。

它调用谁：
- Alembic context 与 SQLAlchemy engine；Phase 2A 不由应用启动流程调用。

输入与输出：
- 输入为 DATABASE_URL；输出为 Alembic migration 上下文。

为什么这样设计：
- schema.sql 继续可用，同时先建立可审查的迁移框架；当前没有 metadata、migration 或自动升级。

日本现场面试怎么讲：
- Migration 与应用启动解耦，部署流水线必须显式执行，避免服务启动时偷偷改变生产数据库。
"""

from __future__ import annotations

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 当前项目使用手写 SQL schema，没有 SQLAlchemy ORM metadata；空基线必须保持 None。
target_metadata = None


def _database_url() -> str:
    """从进程环境读取连接串，禁止把凭据固化到 alembic.ini。"""

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL must be set explicitly for Alembic commands")
    return database_url


def _sqlalchemy_database_url() -> str:
    """把测试库连接串规范化为 SQLAlchemy 可识别的 psycopg 驱动格式。"""

    database_url = _database_url()
    if database_url.startswith("postgresql+psycopg://"):
        return database_url
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


def run_migrations_offline() -> None:
    """生成离线 SQL 上下文；只有显式 Alembic 命令才会进入这里。"""

    context.configure(
        url=_sqlalchemy_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """创建一次性连接执行 migration；Phase 2A 不调用 upgrade。"""

    # 先交给 Alembic ConfigParser 保存，读取 section 时会还原百分号，避免 URL 被二次转义。
    config.set_main_option("sqlalchemy.url", _sqlalchemy_database_url().replace("%", "%%"))
    section = config.get_section(config.config_ini_section) or {}
    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
