"""应用事务边界合同。Service 只依赖此接口，不感知具体数据库。"""

from __future__ import annotations

from contextlib import AbstractContextManager
from typing import Protocol, runtime_checkable


@runtime_checkable
class UnitOfWork(Protocol):
    """为一个业务动作提供原子提交或整体回滚。"""

    def transaction(self) -> AbstractContextManager[None]:
        """返回事务上下文。"""

        ...


__all__ = ["UnitOfWork"]
