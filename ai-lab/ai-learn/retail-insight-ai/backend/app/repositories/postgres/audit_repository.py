"""PostgreSQL append-only Persistent Audit Repository。

文件职责：
- 把统一 AuditLog 追加到 PostgreSQL，并提供企业审计过滤、分页和稳定倒序查询。
- 保留旧列名 ``operation_type / actor_id / created_at``，避免破坏已有数据。

谁调用它：
- AuditService 和 PostgreSQL 集成测试。

它调用谁：
- PostgresConnectionFactory 取得事务内共享连接。

输入与输出：
- 输入 AuditLog / AuditLogFilter；输出不可变 AuditLog 或 AuditLogPage。

为什么这样设计：
- 普通业务 API 只允许 append/read，Repository 不提供 update/delete。

日本现场面试怎么讲：
- 成功业务与审计共用 Unit of Work；查询以 created_at DESC、id DESC 保证稳定分页。
"""

from __future__ import annotations

import json

from app.db.connection import PostgresConnectionFactory
from app.models.audit import AuditLog, AuditLogFilter, AuditLogPage, AuditLogResult


class PostgresAuditRepository:
    def __init__(self, connection_factory: PostgresConnectionFactory) -> None:
        self._connection_factory = connection_factory

    def append(self, log: AuditLog) -> AuditLog:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO audit_logs (
                        id,operation_type,actor_id,organization_id,department_id,resource_type,
                        resource_id,result,request_id,trace_id,metadata,error_code,created_at,
                        actor_username,actor_role,permission,http_method,api_path,status_code
                    ) VALUES (
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb,%s,%s,
                        %s,%s,%s,%s,%s,%s
                    )
                    """,
                    (
                        log.audit_log_id,
                        log.operation_type,
                        log.actor_id,
                        log.organization_id,
                        log.department_id,
                        log.resource_type,
                        log.resource_id,
                        log.result.value,
                        log.request_id,
                        log.trace_id,
                        json.dumps(log.metadata, ensure_ascii=False),
                        log.error_code,
                        log.timestamp,
                        log.actor_username,
                        log.actor_role,
                        log.permission,
                        log.http_method,
                        log.api_path,
                        log.status_code,
                    ),
                )
        return log

    def list_all(self) -> list[AuditLog]:
        """保留旧 MVP 的追加顺序读取，避免改变 InMemory/旧测试合同。"""

        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT operation_type,actor_id,organization_id,department_id,resource_type,
                    resource_id,result,request_id,trace_id,metadata,error_code,id,created_at,
                    actor_username,actor_role,permission,http_method,api_path,status_code
                    FROM audit_logs ORDER BY created_at,id"""
                )
                rows = cursor.fetchall()
        return self._to_domain(rows)

    def query(self, filters: AuditLogFilter) -> AuditLogPage:
        """执行参数化过滤；多取一条判断是否存在下一页。"""

        clauses: list[str] = []
        parameters: list[object] = []
        filter_columns = (
            ("actor_id", filters.actor_user_id),
            ("actor_username", filters.actor_username),
            ("actor_role", filters.actor_role),
            ("operation_type", filters.action),
            ("resource_type", filters.resource_type),
            ("resource_id", filters.resource_id),
            ("request_id", filters.request_id),
        )
        for column, value in filter_columns:
            if value is not None:
                clauses.append(f"{column} = %s")
                parameters.append(value)
        if filters.result is not None:
            clauses.append("result = %s")
            parameters.append(filters.result.value)
        if filters.start_time is not None:
            clauses.append("created_at >= %s")
            parameters.append(filters.start_time)
        if filters.end_time is not None:
            clauses.append("created_at <= %s")
            parameters.append(filters.end_time)

        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        parameters.extend((filters.limit + 1, filters.offset))
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT operation_type,actor_id,organization_id,department_id,resource_type,
                           resource_id,result,request_id,trace_id,metadata,error_code,id,created_at,
                           actor_username,actor_role,permission,http_method,api_path,status_code
                    FROM audit_logs
                    {where_sql}
                    ORDER BY created_at DESC, id DESC
                    LIMIT %s OFFSET %s
                    """,
                    parameters,
                )
                rows = cursor.fetchall()

        has_more = len(rows) > filters.limit
        page_rows = rows[: filters.limit]
        return AuditLogPage(
            items=self._to_domain(page_rows),
            next_offset=filters.offset + filters.limit if has_more else None,
        )

    def _to_domain(self, rows: list[tuple[object, ...]]) -> list[AuditLog]:
        """用关键字映射数据库行，避免未来新增列破坏 dataclass 位置参数。"""

        result: list[AuditLog] = []
        for row in rows:
            result.append(
                AuditLog(
                    operation_type=str(row[0]),
                    actor_id=row[1],
                    organization_id=row[2],
                    department_id=row[3],
                    resource_type=str(row[4]),
                    resource_id=str(row[5]),
                    result=AuditLogResult(row[6]),
                    request_id=str(row[7]),
                    trace_id=str(row[8]),
                    metadata=dict(row[9] or {}),
                    error_code=row[10],
                    audit_log_id=str(row[11]),
                    timestamp=row[12],
                    actor_username=row[13],
                    actor_role=row[14],
                    permission=row[15],
                    http_method=row[16],
                    api_path=row[17],
                    status_code=row[18],
                )
            )
        return result


__all__ = ["PostgresAuditRepository"]
