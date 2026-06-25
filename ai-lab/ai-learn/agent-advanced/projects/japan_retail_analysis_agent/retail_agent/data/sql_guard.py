from __future__ import annotations

"""SQL safety guard.

教学要点：
- 当前实现只是教学级 SELECT-only 字符串检查。
- 生产环境必须升级为 SQL AST parser、表/字段白名单、查询成本限制。
"""


def assert_select_only(sql: str) -> None:
    """Reject non-SELECT or multi-statement SQL."""
    normalized = sql.strip().lower()
    forbidden = [";", " insert ", " update ", " delete ", " drop ", " alter ", " pragma "]
    if not normalized.startswith("select") or any(token in f" {normalized} " for token in forbidden):
        raise ValueError("Only one read-only SELECT statement is allowed.")
