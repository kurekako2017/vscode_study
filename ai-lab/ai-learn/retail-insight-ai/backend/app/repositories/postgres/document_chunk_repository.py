"""DocumentChunkRepository 的 PostgreSQL 实现。"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from datetime import datetime

from app.db.connection import PostgresConnectionFactory
from app.embeddings.service import validate_embedding_vector
from app.models.document import DocumentChunk, DocumentMetadata
from app.repositories.interfaces.document_chunk_repository import VectorChunkMatch
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
                            chunk_id,document_id,version,chunk_index,content,character_count,
                            metadata,created_at,embedding
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s::jsonb,%s,%s::vector)
                        """,
                        (
                            chunk.chunk_id, chunk.document_id, chunk.version, chunk.chunk_index,
                            chunk.content, chunk.character_count,
                            json.dumps(metadata_to_dict(chunk.metadata), ensure_ascii=False), chunk.created_at,
                            self._vector_literal(chunk.embedding),
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
                    SELECT document_id,version,chunk_id,chunk_index,content,character_count,
                           metadata,created_at,embedding
                    FROM document_chunks WHERE document_id=%s AND version=%s ORDER BY chunk_index
                    """,
                    (document_id, version),
                )
                rows = cursor.fetchall()
        return [self._to_domain(row) for row in rows]

    def update_embedding(self, chunk_id: str, embedding: Sequence[float] | None) -> None:
        """通过 pgvector 类型更新 embedding，旧 chunk 仍允许保持 NULL。"""

        literal = self._vector_literal(embedding)
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE document_chunks SET embedding=%s::vector WHERE chunk_id=%s",
                    (literal, chunk_id),
                )
                if cursor.rowcount != 1:
                    raise KeyError(f"document chunk not found: {chunk_id}")

    def search_by_embedding(
        self,
        embedding: Sequence[float],
        *,
        limit: int,
        document_ids: Sequence[str] | None = None,
        document_versions: Mapping[str, int] | None = None,
    ) -> list[VectorChunkMatch]:
        """使用 pgvector `<=>` cosine distance，并以稳定字段完成 tie-break。"""

        if limit < 1:
            raise ValueError("vector search limit must be greater than zero")
        literal = self._vector_literal(embedding)
        where = "embedding IS NOT NULL"
        parameters: list[object] = [literal]
        if document_ids is not None:
            if not document_ids:
                return []
            where += " AND document_id = ANY(%s)"
            parameters.append(list(document_ids))
        if document_versions is not None:
            if not document_versions:
                return []
            version_pairs = list(document_versions.items())
            placeholders = ",".join(["(%s,%s)"] * len(version_pairs))
            where += f" AND (document_id,version) IN ({placeholders})"
            for document_id, version in version_pairs:
                parameters.extend([document_id, version])
        parameters.extend([literal, limit])
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT document_id,version,chunk_id,chunk_index,content,character_count,
                           metadata,created_at,embedding,
                           1 - (embedding <=> %s::vector) AS cosine_similarity
                    FROM document_chunks
                    WHERE {where}
                    ORDER BY embedding <=> %s::vector, document_id, chunk_index, chunk_id
                    LIMIT %s
                    """,
                    parameters,
                )
                rows = cursor.fetchall()
        return [VectorChunkMatch(self._to_domain(row[:-1]), float(row[-1])) for row in rows]

    def _to_domain(self, row) -> DocumentChunk:
        document_id, version, chunk_id, chunk_index, content, count, metadata_json, created_at, embedding = row
        payload = dict(metadata_json)
        payload["created_at"] = datetime.fromisoformat(payload["created_at"])
        payload["updated_at"] = datetime.fromisoformat(payload["updated_at"])
        metadata = DocumentMetadata.from_mapping(payload)
        return DocumentChunk(
            document_id=document_id, version=version, chunk_id=chunk_id,
            chunk_index=chunk_index, content=content, character_count=count,
            metadata=metadata, created_at=created_at, embedding=self._parse_vector(embedding),
        )

    def _vector_literal(self, embedding: Sequence[float] | None) -> str | None:
        """使用明确文本格式交给 pgvector cast，避免依赖额外 Python adapter。"""

        if embedding is None:
            return None
        normalized = validate_embedding_vector(embedding)
        return "[" + ",".join(format(value, ".17g") for value in normalized) + "]"

    def _parse_vector(self, value: object | None) -> tuple[float, ...] | None:
        """兼容 psycopg 将 vector 返回为文本或序列的行为。"""

        if value is None:
            return None
        if isinstance(value, str):
            values = [float(item) for item in value.strip("[]").split(",") if item]
        else:
            values = [float(item) for item in value]  # type: ignore[union-attr]
        return validate_embedding_vector(values)


__all__ = ["PostgresDocumentChunkRepository"]
