"""append-only AuditRepository 的 PostgreSQL 实现。"""

from __future__ import annotations

import json

from app.db.connection import PostgresConnectionFactory
from app.models.audit import AuditLog, AuditLogResult


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
                        resource_id,result,request_id,trace_id,metadata,error_code,created_at
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb,%s,%s)
                    """,
                    (
                        log.audit_log_id,log.operation_type,log.actor_id,log.organization_id,
                        log.department_id,log.resource_type,log.resource_id,log.result.value,
                        log.request_id,log.trace_id,json.dumps(log.metadata, ensure_ascii=False),
                        log.error_code,log.timestamp,
                    ),
                )
        return log

    def list_all(self) -> list[AuditLog]:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT operation_type,actor_id,organization_id,department_id,resource_type,
                    resource_id,result,request_id,trace_id,metadata,error_code,id,created_at
                    FROM audit_logs ORDER BY created_at,id"""
                )
                rows = cursor.fetchall()
        result: list[AuditLog] = []
        for row in rows:
            values = list(row)
            values[6] = AuditLogResult(values[6])
            values[9] = dict(values[9] or {})
            result.append(AuditLog(*values))
        return result


__all__ = ["PostgresAuditRepository"]
