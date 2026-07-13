"""Unit of Work 实现：InMemory 保持原行为，PostgreSQL 共享同一连接。"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from app.db.connection import PostgresConnectionFactory


class InMemoryUnitOfWork:
    """默认学习模式的无外部资源事务边界。"""

    @contextmanager
    def transaction(self) -> Iterator[None]:
        yield


class PostgresUnitOfWork:
    """把多个 PostgreSQL Repository 调用收敛到同一数据库事务。"""

    def __init__(self, connection_factory: PostgresConnectionFactory) -> None:
        self._connection_factory = connection_factory

    def transaction(self):
        return self._connection_factory.transaction()


__all__ = ["InMemoryUnitOfWork", "PostgresUnitOfWork"]
