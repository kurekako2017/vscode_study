"""上传会话及幂等键的 PostgreSQL 实现。"""

from __future__ import annotations

from app.db.connection import PostgresConnectionFactory
from app.models.upload import UploadSessionRecord
from app.errors.base import AppException
from app.errors.error_codes import ErrorCode


class PostgresUploadSessionRepository:
    def __init__(self, connection_factory: PostgresConnectionFactory) -> None:
        self._connection_factory = connection_factory

    def save(self, record: UploadSessionRecord) -> None:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO upload_sessions (
                        upload_id,document_id,checksum,idempotency_key,status,progress,
                        error_code,error_message,created_at,updated_at
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (upload_id) DO UPDATE SET
                        status=EXCLUDED.status,progress=EXCLUDED.progress,error_code=EXCLUDED.error_code,
                        error_message=EXCLUDED.error_message,updated_at=EXCLUDED.updated_at
                    """,
                    (
                        record.upload_id,record.document_id,record.checksum,record.idempotency_key,
                        record.status,record.progress,record.error_code,record.error_message,
                        record.created_at,record.updated_at,
                    ),
                )
                if record.idempotency_key is not None:
                    cursor.execute(
                        """INSERT INTO upload_idempotency_keys (idempotency_key,upload_id,checksum)
                        VALUES (%s,%s,%s)
                        ON CONFLICT (idempotency_key) DO UPDATE SET
                            upload_id=upload_idempotency_keys.upload_id
                        WHERE upload_idempotency_keys.checksum=EXCLUDED.checksum""",
                        (record.idempotency_key, record.upload_id, record.checksum),
                    )
                    if cursor.rowcount == 0:
                        raise AppException(
                            ErrorCode.IDEMPOTENCY_CONFLICT,
                            "Same idempotency key was reused with a different file.",
                            409,
                            detail={"idempotency_key": record.idempotency_key},
                        )

    def get_by_checksum(self, checksum: str) -> UploadSessionRecord | None:
        return self._get("checksum", checksum)

    def get_by_idempotency_key(self, idempotency_key: str) -> UploadSessionRecord | None:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT s.upload_id,s.document_id,s.checksum,s.status,s.progress,
                    s.created_at,s.updated_at,k.idempotency_key,s.error_code,s.error_message
                    FROM upload_idempotency_keys k JOIN upload_sessions s ON s.upload_id=k.upload_id
                    WHERE k.idempotency_key=%s""",
                    (idempotency_key,),
                )
                row = cursor.fetchone()
        return UploadSessionRecord(*row) if row else None

    def _get(self, field: str, value: str) -> UploadSessionRecord | None:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT upload_id,document_id,checksum,status,progress,created_at,updated_at,
                    idempotency_key,error_code,error_message FROM upload_sessions WHERE {field}=%s""",
                    (value,),
                )
                row = cursor.fetchone()
        return UploadSessionRecord(*row) if row else None


__all__ = ["PostgresUploadSessionRepository"]
