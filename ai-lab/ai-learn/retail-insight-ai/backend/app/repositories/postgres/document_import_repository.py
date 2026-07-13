"""Document Import 会话的 PostgreSQL 实现。"""

from __future__ import annotations

from app.db.connection import PostgresConnectionFactory
from app.models.document_import import DocumentImportError, DocumentImportRecord, DocumentImportStatus


class PostgresDocumentImportRepository:
    def __init__(self, connection_factory: PostgresConnectionFactory) -> None:
        self._connection_factory = connection_factory

    def save(self, record: DocumentImportRecord) -> None:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO document_imports (
                        import_id,document_id,status,error_code,error_message,created_at,updated_at
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (import_id) DO UPDATE SET
                        status=EXCLUDED.status,error_code=EXCLUDED.error_code,
                        error_message=EXCLUDED.error_message,updated_at=EXCLUDED.updated_at
                    """,
                    (
                        record.import_id, record.document_id, record.status.value,
                        record.error_code, record.error_message, record.created_at, record.updated_at,
                    ),
                )

    def get(self, import_id: str) -> DocumentImportRecord | None:
        return self._get("import_id", import_id)

    def get_by_document_id(self, document_id: str) -> DocumentImportRecord | None:
        return self._get("document_id", document_id)

    def _get(self, field: str, value: str) -> DocumentImportRecord | None:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT import_id,document_id,status,error_code,error_message,created_at,updated_at
                    FROM document_imports WHERE {field}=%s""",  # field 仅来自本类常量
                    (value,),
                )
                row = cursor.fetchone()
        if row is None:
            return None
        import_id, document_id, status, error_code, error_message, created_at, updated_at = row
        error = DocumentImportError(error_code, error_message) if error_code else None
        return DocumentImportRecord(
            import_id=import_id, document_id=document_id, status=DocumentImportStatus(status),
            created_at=created_at, updated_at=updated_at, error=error,
        )


__all__ = ["PostgresDocumentImportRepository"]
