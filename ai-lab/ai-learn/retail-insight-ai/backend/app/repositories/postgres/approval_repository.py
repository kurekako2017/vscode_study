"""审批请求、审批事件与报告版本唯一事实源的 PostgreSQL 实现。"""

from __future__ import annotations

from app.db.connection import PostgresConnectionFactory
from app.models.approval import ApprovalEvent, ApprovalRequest, ReportVersion
from app.models.report import ReportStatus


class PostgresApprovalRepository:
    def __init__(self, connection_factory: PostgresConnectionFactory) -> None:
        self._connection_factory = connection_factory

    def save_report_version(self, version: ReportVersion) -> None:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO report_versions (
                        id,task_id,version_no,markdown,status,revision_reason,
                        revised_from_version_id,created_at,created_by
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    (
                        version.id,version.task_id,version.version_no,version.markdown,
                        version.status.value,version.revision_reason,version.revised_from_version_id,
                        version.created_at,version.created_by,
                    ),
                )

    def get_report_version(self, version_id: str) -> ReportVersion | None:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(self._version_select() + " WHERE id=%s", (version_id,))
                row = cursor.fetchone()
        return self._to_version(row) if row else None

    def list_report_versions(self, task_id: str) -> list[ReportVersion]:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(self._version_select() + " WHERE task_id=%s ORDER BY version_no", (task_id,))
                rows = cursor.fetchall()
        return [self._to_version(row) for row in rows]

    def get_latest_report_version(self, task_id: str) -> ReportVersion | None:
        versions = self.list_report_versions(task_id)
        return versions[-1] if versions else None

    def save_approval_request(self, request: ApprovalRequest) -> None:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO approval_requests (
                        id,task_id,report_version_id,status,requested_by,requested_at,
                        approver_id,decision_at,decision_reason,revision_no,revised_from_version_id
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (id) DO UPDATE SET
                        status=EXCLUDED.status,approver_id=EXCLUDED.approver_id,
                        decision_at=EXCLUDED.decision_at,decision_reason=EXCLUDED.decision_reason,
                        revision_no=EXCLUDED.revision_no,revised_from_version_id=EXCLUDED.revised_from_version_id,
                        report_version_id=EXCLUDED.report_version_id
                    """,
                    (
                        request.id,request.task_id,request.report_version_id,request.status.value,
                        request.requested_by,request.requested_at,request.approver_id,request.decision_at,
                        request.decision_reason,request.revision_no,request.revised_from_version_id,
                    ),
                )

    def get_approval_request(self, approval_id: str) -> ApprovalRequest | None:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(self._request_select() + " WHERE id=%s", (approval_id,))
                row = cursor.fetchone()
        return self._to_request(row) if row else None

    def list_approval_requests(
        self, *, task_id: str | None = None, status: ReportStatus | None = None
    ) -> list[ApprovalRequest]:
        clauses: list[str] = []
        params: list[str] = []
        if task_id is not None:
            clauses.append("task_id=%s")
            params.append(task_id)
        if status is not None:
            clauses.append("status=%s")
            params.append(status.value)
        suffix = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(self._request_select() + suffix + " ORDER BY requested_at,id", tuple(params))
                rows = cursor.fetchall()
        return [self._to_request(row) for row in rows]

    def save_approval_event(self, event: ApprovalEvent) -> None:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO approval_events (id,approval_id,task_id,event_type,actor_id,reason,created_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING
                    """,
                    (
                        event.id,event.approval_id,event.task_id,event.event_type,
                        event.actor_id,event.reason,event.created_at,
                    ),
                )

    def list_approval_events(self, approval_id: str) -> list[ApprovalEvent]:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT approval_id,task_id,event_type,actor_id,reason,id,created_at
                    FROM approval_events WHERE approval_id=%s ORDER BY created_at,id""",
                    (approval_id,),
                )
                rows = cursor.fetchall()
        return [ApprovalEvent(*row) for row in rows]

    def _version_select(self) -> str:
        return """SELECT task_id,version_no,markdown,status,revision_reason,
        revised_from_version_id,id,created_at,created_by FROM report_versions"""

    def _request_select(self) -> str:
        return """SELECT task_id,report_version_id,status,requested_by,id,requested_at,
        approver_id,decision_at,decision_reason,revision_no,revised_from_version_id FROM approval_requests"""

    def _to_version(self, row) -> ReportVersion:
        values = list(row)
        values[3] = ReportStatus(values[3])
        return ReportVersion(*values)

    def _to_request(self, row) -> ApprovalRequest:
        values = list(row)
        values[2] = ReportStatus(values[2])
        return ApprovalRequest(*values)


__all__ = ["PostgresApprovalRepository"]
