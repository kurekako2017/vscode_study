"""DocumentChunkRepository 的 PostgreSQL 实现。"""

from __future__ import annotations

import json
from datetime import datetime

from app.db.connection import PostgresConnectionFactory
from app.models.document import DocumentChunk, DocumentMetadata
from app.repositories.postgres.document_serialization import metadata_to_dict


class PostgresDocumentChunkRepository:
    """按 document/version 原子替换 chunk 集合。"""

    def __init__(self, connection_factory: PostgresConnectionFactory) -> None:
        self._connection_factory = connection_factory

    def replace_for_document(self, document_id: str, version: int, chunks: list[DocumentChunk]) -> None:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM document_chunks WHERE document_id=%s AND version=%s",
                    (document_id, version),
                )
                for chunk in chunks:
                    cursor.execute(
                        """
                        INSERT INTO document_chunks (
                            chunk_id,document_id,version,chunk_index,content,character_count,metadata,created_at
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s::jsonb,%s)
                        """,
                        (
                            chunk.chunk_id, chunk.document_id, chunk.version, chunk.chunk_index,
                            chunk.content, chunk.character_count,
                            json.dumps(metadata_to_dict(chunk.metadata), ensure_ascii=False), chunk.created_at,
                        ),
                    )

    def list_for_document(self, document_id: str, version: int | None = None) -> list[DocumentChunk]:
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                if version is None:
                    cursor.execute("SELECT MAX(version) FROM document_chunks WHERE document_id=%s", (document_id,))
                    row = cursor.fetchone()
                    version = row[0] if row else None
                if version is None:
                    return []
                cursor.execute(
                    """
                    SELECT document_id,version,chunk_id,chunk_index,content,character_count,metadata,created_at
                    FROM document_chunks WHERE document_id=%s AND version=%s ORDER BY chunk_index
                    """,
                    (document_id, version),
                )
                rows = cursor.fetchall()
        return [self._to_domain(row) for row in rows]

    def _to_domain(self, row) -> DocumentChunk:
        document_id, version, chunk_id, chunk_index, content, count, metadata_json, created_at = row
        payload = dict(metadata_json)
        payload["created_at"] = datetime.fromisoformat(payload["created_at"])
        payload["updated_at"] = datetime.fromisoformat(payload["updated_at"])
        metadata = DocumentMetadata.from_mapping(payload)
        return DocumentChunk(
            document_id=document_id, version=version, chunk_id=chunk_id,
            chunk_index=chunk_index, content=content, character_count=count,
            metadata=metadata, created_at=created_at,
        )


__all__ = ["PostgresDocumentChunkRepository"]
