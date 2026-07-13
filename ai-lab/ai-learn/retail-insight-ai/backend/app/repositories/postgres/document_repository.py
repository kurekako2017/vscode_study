"""DocumentRepository 的 PostgreSQL 实现，保存完整正文、元数据与软删除状态。"""

from __future__ import annotations

import json

from app.db.connection import PostgresConnectionFactory
from app.errors.exceptions import ValidationAppException
from app.models.document import Document, DocumentMetadata
from app.models.report import ReportStatus
from app.repositories.postgres.document_serialization import source_to_json


class PostgresDocumentRepository:
    """把 Document 聚合映射到 documents 表。"""

    def __init__(self, connection_factory: PostgresConnectionFactory) -> None:
        self._connection_factory = connection_factory

    def create(self, document: Document) -> None:
        document.validate_for_creation()
        try:
            with self._connection_factory.connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(self._insert_sql(), self._params(document))
        except Exception as exc:
            self._raise_constraint_error(exc, document)

    def get(self, document_id: str) -> Document | None:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(self._select_sql() + " WHERE document_id = %s", (document_id,))
                row = cursor.fetchone()
        return self._to_domain(row) if row else None

    def list_all(self) -> list[Document]:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(self._select_sql() + " ORDER BY document_id")
                rows = cursor.fetchall()
        return [self._to_domain(row) for row in rows]

    def update(self, document: Document) -> None:
        document.validate_for_storage()
        try:
            with self._connection_factory.connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE documents SET
                            title=%s, description=%s, owner=%s, version=%s, language=%s,
                            document_type=%s, status=%s, tags=%s::jsonb, source=%s::jsonb,
                            checksum=%s, content=%s, approval_status=%s,
                            metadata_created_at=%s, metadata_updated_at=%s,
                            created_at=%s, updated_at=%s
                        WHERE document_id=%s
                        """,
                        self._params(document)[1:] + (document.document_id,),
                    )
                    if cursor.rowcount == 0:
                        raise KeyError(document.document_id)
        except KeyError:
            raise
        except Exception as exc:
            self._raise_constraint_error(exc, document)

    def delete(self, document_id: str) -> None:
        document = self.get(document_id)
        if document is None:
            raise KeyError(document_id)
        document.archive()
        self.update(document)

    def find_by_checksum(self, checksum: str) -> Document | None:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(self._select_sql() + " WHERE checksum = %s", (checksum,))
                row = cursor.fetchone()
        return self._to_domain(row) if row else None

    def _insert_sql(self) -> str:
        return """
            INSERT INTO documents (
                document_id, title, description, owner, version, language, document_type,
                status, tags, source, checksum, content, approval_status,
                metadata_created_at, metadata_updated_at, created_at, updated_at
            ) VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb,%s::jsonb,%s,%s,%s,%s,%s,%s,%s
            )
        """

    def _select_sql(self) -> str:
        return """
            SELECT document_id,title,description,owner,version,language,document_type,status,
                   tags,source,checksum,content,approval_status,metadata_created_at,
                   metadata_updated_at,created_at,updated_at FROM documents
        """

    def _params(self, document: Document) -> tuple:
        metadata = document.metadata
        return (
            document.document_id, metadata.title, metadata.description, metadata.owner,
            metadata.version, metadata.language.value, metadata.document_type.value,
            metadata.status.value, json.dumps(list(metadata.tags), ensure_ascii=False),
            source_to_json(metadata.source), metadata.checksum, document.content,
            document.approval_status.value, metadata.created_at, metadata.updated_at,
            document.created_at, document.updated_at,
        )

    def _to_domain(self, row) -> Document:
        (
            document_id,title,description,owner,version,language,document_type,status,tags,
            source,checksum,content,approval_status,metadata_created_at,metadata_updated_at,
            created_at,updated_at,
        ) = row
        metadata = DocumentMetadata.from_mapping(
            {
                "document_id": document_id, "title": title, "description": description,
                "owner": owner, "version": version, "language": language,
                "document_type": document_type, "status": status, "tags": list(tags or []),
                "source": dict(source), "checksum": checksum,
                "created_at": metadata_created_at, "updated_at": metadata_updated_at,
            }
        )
        return Document(
            content=content, metadata=metadata, approval_status=ReportStatus(approval_status),
            created_at=created_at, updated_at=updated_at,
        )

    def _raise_constraint_error(self, exc: Exception, document: Document) -> None:
        constraint = getattr(getattr(exc, "diag", None), "constraint_name", "") or ""
        field = "checksum" if "checksum" in constraint else "document_id"
        raise ValidationAppException(
            {"field": field, "reason": f"duplicate {field}", field: getattr(document.metadata, field)}
        ) from exc


__all__ = ["PostgresDocumentRepository"]
