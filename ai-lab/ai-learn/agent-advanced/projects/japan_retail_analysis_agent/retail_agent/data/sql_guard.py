from __future__ import annotations

"""SQL safety guard.

教学要点：
- 当前实现只是教学级 SELECT-only 字符串检查。
- 生产环境必须升级为 SQL AST parser、表/字段白名单、查询成本限制。
"""


def assert_select_only(sql: str) -> None:
    """Reject non-SELECT or multi-statement SQL.

    这是教学级护栏：让读者看到“执行 SQL 前必须有安全边界”。
    它不能替代生产级 SQL parser，因为字符串检查无法理解复杂 SQL 语法。
    """
    normalized = sql.strip().lower()
    # 分号会打开多语句风险；写操作关键字说明 SQL 不再是只读查询。
    forbidden = [";", " insert ", " update ", " delete ", " drop ", " alter ", " pragma "]
    if not normalized.startswith("select") or any(token in f" {normalized} " for token in forbidden):
        raise ValueError("Only one read-only SELECT statement is allowed.")
