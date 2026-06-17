"""
SQL 文本处理工具

负责把模型返回的 SQL 文本清洗成数据库可直接执行的形式。
"""

import re
from typing import Iterable

from app.agent.state import TableInfoState

_CODE_BLOCK_PATTERN = re.compile(r"^```(?:sql)?\s*|\s*```$", re.IGNORECASE)
# 这些正则分别用于识别 SQL 里出现的表名、JOIN 片段和字段引用。
_REFERENCED_TABLE_PATTERN = re.compile(r"\b([A-Za-z_][\w]*)\.")
_FROM_OR_JOIN_PATTERN = re.compile(r"\b(?:FROM|JOIN)\s+([A-Za-z_][\w]*)\b", re.IGNORECASE)
_CLAUSE_PATTERN = re.compile(
    r"\b(WHERE|GROUP\s+BY|ORDER\s+BY|HAVING|LIMIT)\b", re.IGNORECASE
)
_JOIN_PATTERN = re.compile(
    r"\bJOIN\s+([A-Za-z_][\w]*)\s+ON\s+(.+?)(?=\bJOIN\b|\bWHERE\b|\bGROUP\s+BY\b|\bORDER\s+BY\b|\bHAVING\b|\bLIMIT\b|$)",
    re.IGNORECASE | re.DOTALL,
)
_COLUMN_REF_PATTERN = re.compile(r"\b([A-Za-z_][\w]*)\.([A-Za-z_][\w]*)\b")
_TIME_FUNCTION_REPLACEMENTS = {
    r"YEAR\s*\(\s*fact_order\.date\s*\)": "dim_date.year",
    r"QUARTER\s*\(\s*fact_order\.date\s*\)": "dim_date.quarter",
    r"MONTH\s*\(\s*fact_order\.date\s*\)": "dim_date.month",
    r"DAY\s*\(\s*fact_order\.date\s*\)": "dim_date.day",
}


def normalize_sql(raw_sql: str) -> str:
    """移除模型常见的 Markdown 包装，返回可执行 SQL。"""

    # 大模型很喜欢把 SQL 包进 ```sql ... ```，这里先把外层包装清掉。
    sql = raw_sql.strip()
    sql = _CODE_BLOCK_PATTERN.sub("", sql).strip()
    return sql.rstrip(";").strip()


def enrich_sql_with_missing_joins(sql: str, table_infos: Iterable[TableInfoState]) -> str:
    """当 SQL 引用了候选表字段但遗漏 JOIN 时，按主外键名称补齐最小 JOIN。"""

    # 先找出 SQL 已经提到的表，再找出“引用了字段但没有真正 JOIN 进来”的表。
    referenced_tables = set(_REFERENCED_TABLE_PATTERN.findall(sql))
    present_tables = _FROM_OR_JOIN_PATTERN.findall(sql)
    if not referenced_tables or not present_tables:
        return sql

    table_info_map = {table_info["name"]: table_info for table_info in table_infos}
    ordered_present_tables = list(dict.fromkeys(present_tables))
    missing_tables = [
        table_name
        for table_name in referenced_tables
        if table_name not in ordered_present_tables and table_name in table_info_map
    ]

    for missing_table in missing_tables:
        # 选出能把缺失表接回来的最小 JOIN 条件。
        join_condition = _find_join_condition(
            missing_table=missing_table,
            present_tables=ordered_present_tables,
            table_info_map=table_info_map,
        )
        if not join_condition:
            continue

        join_sql = f" JOIN {missing_table} ON {join_condition}"
        clause_match = _CLAUSE_PATTERN.search(sql)
        if clause_match:
            sql = f"{sql[:clause_match.start()]}{join_sql} {sql[clause_match.start():]}"
        else:
            sql = f"{sql}{join_sql}"
        ordered_present_tables.append(missing_table)

    return sql


def repair_sql_with_schema(sql: str, table_infos: Iterable[TableInfoState]) -> str:
    """按当前 schema 修正模型常见的时间字段和 JOIN 错误。"""

    table_info_map = {table_info["name"]: table_info for table_info in table_infos}
    sql = _rewrite_time_dimension_filters(sql)
    sql = enrich_sql_with_missing_joins(sql, table_infos)
    sql = _repair_join_conditions(sql, table_info_map)
    sql = enrich_sql_with_missing_joins(sql, table_infos)
    return sql


def _find_join_condition(
    missing_table: str,
    present_tables: list[str],
    table_info_map: dict[str, TableInfoState],
) -> str | None:
    missing_info = table_info_map[missing_table]
    missing_primary_keys = {
        column["name"]
        for column in missing_info["columns"]
        if column["role"] == "primary_key"
    }
    missing_foreign_keys = {
        column["name"]
        for column in missing_info["columns"]
        if column["role"] == "foreign_key"
    }

    for present_table in present_tables:
        present_info = table_info_map.get(present_table)
        if not present_info:
            continue

        present_primary_keys = {
            column["name"]
            for column in present_info["columns"]
            if column["role"] == "primary_key"
        }
        present_foreign_keys = {
            column["name"]
            for column in present_info["columns"]
            if column["role"] == "foreign_key"
        }

        shared_keys = present_foreign_keys & missing_primary_keys
        if shared_keys:
            key = sorted(shared_keys)[0]
            return f"{present_table}.{key} = {missing_table}.{key}"

        shared_keys = missing_foreign_keys & present_primary_keys
        if shared_keys:
            key = sorted(shared_keys)[0]
            return f"{missing_table}.{key} = {present_table}.{key}"

    return None


def _rewrite_time_dimension_filters(sql: str) -> str:
    for pattern, replacement in _TIME_FUNCTION_REPLACEMENTS.items():
        sql = re.sub(pattern, replacement, sql, flags=re.IGNORECASE)
    return sql


def _repair_join_conditions(
    sql: str, table_info_map: dict[str, TableInfoState]
) -> str:
    def replace_join(match: re.Match[str]) -> str:
        joined_table = match.group(1)
        condition = " ".join(match.group(2).split())
        present_tables = _FROM_OR_JOIN_PATTERN.findall(sql[: match.end()])
        if not present_tables:
            return match.group(0)

        condition_refs = _COLUMN_REF_PATTERN.findall(condition)
        if not condition_refs:
            return match.group(0)

        invalid_ref_found = False
        for table_name, column_name in condition_refs:
            table_info = table_info_map.get(table_name)
            if not table_info:
                continue
            valid_columns = {column["name"] for column in table_info["columns"]}
            if column_name not in valid_columns:
                invalid_ref_found = True
                break

        if not invalid_ref_found:
            return match.group(0)

        join_condition = _find_join_condition(
            missing_table=joined_table,
            present_tables=list(dict.fromkeys(present_tables[:-1])),
            table_info_map=table_info_map,
        )
        if not join_condition:
            return match.group(0)

        return f"JOIN {joined_table} ON {join_condition} "

    return _JOIN_PATTERN.sub(replace_join, sql)
