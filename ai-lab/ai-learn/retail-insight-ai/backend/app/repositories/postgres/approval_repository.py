"""审批请求、业务历史与报告版本唯一事实源的 PostgreSQL 实现。

文件职责：
- 保存 ApprovalRequest 当前状态、不可变 ReportVersion 和 append-only ApprovalEvent。
- 提供 PostgreSQL 行锁，保护重复提交和并发审批。

谁调用它：
- ApprovalService 通过稳定 Repository 接口调用。

输入与输出：
- 输入审批领域对象或业务 ID；输出恢复后的领域对象。

为什么这样设计：
- 状态机留在 Service，数据库层只负责事实持久化、约束和并发串行化。

日本现场面试怎么讲：
- 报告行锁保护 submit/resubmit，审批行锁保护 approve/reject，数据库约束作为最后防线。
"""

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

    def lock_report(self, task_id: str) -> bool:
        """在当前事务锁定报告行，串行化 submit/revise/resubmit。"""

        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT task_id FROM reports WHERE task_id=%s FOR UPDATE",
                    (task_id,),
                )
                return cursor.fetchone() is not None

    def save_approval_request(self, request: ApprovalRequest) -> None:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO approval_requests (
                        id,task_id,report_version_id,status,
                        requested_by,requested_by_username,requested_by_role,requested_at,
                        approver_id,approver_username,approver_role,
                        decision_at,decision_reason,revision_no,revised_from_version_id
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (id) DO UPDATE SET
                        status=EXCLUDED.status,
                        requested_by=EXCLUDED.requested_by,
                        requested_by_username=EXCLUDED.requested_by_username,
                        requested_by_role=EXCLUDED.requested_by_role,
                        approver_id=EXCLUDED.approver_id,
                        approver_username=EXCLUDED.approver_username,
                        approver_role=EXCLUDED.approver_role,
                        decision_at=EXCLUDED.decision_at,decision_reason=EXCLUDED.decision_reason,
                        revision_no=EXCLUDED.revision_no,revised_from_version_id=EXCLUDED.revised_from_version_id,
                        report_version_id=EXCLUDED.report_version_id,updated_at=CURRENT_TIMESTAMP
                    """,
                    (
                        request.id,request.task_id,request.report_version_id,request.status.value,
                        request.requested_by,request.requested_by_username,request.requested_by_role,
                        request.requested_at,request.approver_id,request.approver_username,
                        request.approver_role,request.decision_at,request.decision_reason,
                        request.revision_no,request.revised_from_version_id,
                    ),
                )

    def get_approval_request(self, approval_id: str) -> ApprovalRequest | None:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(self._request_select() + " WHERE id=%s", (approval_id,))
                row = cursor.fetchone()
        return self._to_request(row) if row else None

    def get_approval_request_for_update(
        self, approval_id: str
    ) -> ApprovalRequest | None:
        """只在决策事务中加锁；普通详情读取保持无锁。"""

        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    self._request_select() + " WHERE id=%s FOR UPDATE",
                    (approval_id,),
                )
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
                    INSERT INTO approval_events (
                        id,approval_id,task_id,event_type,actor_id,reason,
                        from_status,to_status,actor_username,actor_role,
                        report_version_id,created_at
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    (
                        event.id,event.approval_id,event.task_id,event.event_type,
                        event.actor_id,event.reason,
                        event.from_status.value if event.from_status is not None else None,
                        event.to_status.value if event.to_status is not None else None,
                        event.actor_username,event.actor_role,event.report_version_id,
                        event.created_at,
                    ),
                )

    def list_approval_events(self, approval_id: str) -> list[ApprovalEvent]:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    self._event_select()
                    + " WHERE approval_id=%s ORDER BY created_at ASC,id ASC",
                    (approval_id,),
                )
                rows = cursor.fetchall()
        return [self._to_event(row) for row in rows]

    def list_task_approval_events(self, task_id: str) -> list[ApprovalEvent]:
        """读取同一报告跨提交、拒绝、修订和重提的完整历史。"""

        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    self._event_select()
                    + " WHERE task_id=%s ORDER BY created_at ASC,id ASC",
                    (task_id,),
                )
                rows = cursor.fetchall()
        return [self._to_event(row) for row in rows]

    def _version_select(self) -> str:
        return """SELECT task_id,version_no,markdown,status,revision_reason,
        revised_from_version_id,id,created_at,created_by FROM report_versions"""

    def _request_select(self) -> str:
        return """SELECT task_id,report_version_id,status,
        requested_by,requested_by_username,requested_by_role,id,requested_at,
        approver_id,approver_username,approver_role,decision_at,decision_reason,
        revision_no,revised_from_version_id FROM approval_requests"""

    def _event_select(self) -> str:
        return """SELECT approval_id,task_id,event_type,actor_id,reason,
        from_status,to_status,actor_username,actor_role,report_version_id,id,created_at
        FROM approval_events"""

    def _to_version(self, row) -> ReportVersion:
        values = list(row)
        values[3] = ReportStatus(values[3])
        return ReportVersion(*values)

    def _to_request(self, row) -> ApprovalRequest:
        values = list(row)
        values[2] = ReportStatus(values[2])
        return ApprovalRequest(*values)

    def _to_event(self, row) -> ApprovalEvent:
        values = list(row)
        values[5] = ReportStatus(values[5]) if values[5] is not None else None
        values[6] = ReportStatus(values[6]) if values[6] is not None else None
        return ApprovalEvent(*values)


__all__ = ["PostgresApprovalRepository"]
