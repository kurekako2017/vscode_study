"""Add pgvector embeddings to document chunks.

Revision ID: 20260714_02_chunk_embeddings
Revises: 20260714_01_initial_schema
Create Date: 2026-07-14
"""

from __future__ import annotations

from alembic import op

revision = "20260714_02_chunk_embeddings"
down_revision = "20260714_01_initial_schema"
branch_labels = None
depends_on = None

# Migration 必须保持历史不可变，因此在 revision 内固定数值；测试会与应用常量核对。
EMBEDDING_DIMENSIONS = 384
VECTOR_INDEX_NAME = "idx_document_chunks_embedding_hnsw"


def upgrade() -> None:
    """启用 pgvector，并为 chunk 增加 cosine HNSW 检索能力。"""

    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute(
        f"""
        ALTER TABLE document_chunks
        ADD COLUMN IF NOT EXISTS embedding vector({EMBEDDING_DIMENSIONS}) NULL
        """
    )
    op.execute(
        f"""
        CREATE INDEX IF NOT EXISTS {VECTOR_INDEX_NAME}
        ON document_chunks USING hnsw (embedding vector_cosine_ops)
        WHERE embedding IS NOT NULL
        """
    )


def downgrade() -> None:
    """删除项目字段与索引；共享 extension 默认保留，避免影响其他对象。"""

    op.execute(f"DROP INDEX IF EXISTS {VECTOR_INDEX_NAME}")
    op.execute("ALTER TABLE document_chunks DROP COLUMN IF EXISTS embedding")
