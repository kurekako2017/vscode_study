"""Embedding persistence、Vector Retrieval 与 Hybrid Retrieval 的本地合同测试。"""

from __future__ import annotations

import unittest
from uuid import uuid4

from app.config.retrieval import HybridRetrievalConfig
from app.embeddings.provider import DeterministicTestEmbeddingProvider
from app.embeddings.service import EmbeddingService, EmbeddingValidationError
from app.models.document import Document, DocumentChunk, DocumentMetadata
from app.repositories.implementations.in_memory.document_chunk_repository import (
    InMemoryDocumentChunkRepository,
)
from app.repositories.implementations.in_memory.document_repository import InMemoryDocumentRepository
from app.repositories.implementations.in_memory.document_retrieval import (
    HybridDocumentRetrieval,
    InMemoryKeywordRetrieval,
    VectorDocumentRetrieval,
)
from app.schemas.document_retrieval_api import DocumentRetrievalSearchRequest


class VectorRetrievalTest(unittest.TestCase):
    """用显式测试向量验证排序、过滤、fallback、融合与稳定性。"""

    def setUp(self) -> None:
        self.documents = InMemoryDocumentRepository()
        self.chunks = InMemoryDocumentChunkRepository()
        self.embedding = EmbeddingService(DeterministicTestEmbeddingProvider())
        keyword = InMemoryKeywordRetrieval(self.documents, self.chunks)
        vector = VectorDocumentRetrieval(self.documents, self.chunks, self.embedding)
        self.provider = HybridDocumentRetrieval(
            keyword,
            vector,
            HybridRetrievalConfig(keyword_weight=0.4, vector_weight=0.6),
        )

    def test_embedding_persistence_null_update_top_k_and_document_filter(self) -> None:
        first = self._save_chunk("semantic target", embedding=None)
        second = self._save_chunk("other content", embedding=self.embedding.embed_text("other query"))

        self.assertIsNone(self.chunks.list_for_document(first.document_id)[0].embedding)
        self.chunks.update_embedding(first.chunk_id, self.embedding.embed_text("semantic query"))
        matches = self.chunks.search_by_embedding(
            self.embedding.embed_text("semantic query"),
            limit=1,
            document_ids=[first.document_id, second.document_id],
        )

        self.assertEqual([item.chunk.chunk_id for item in matches], [first.chunk_id])
        self.assertEqual(len(matches[0].chunk.embedding or ()), 384)
        filtered = self.chunks.search_by_embedding(
            self.embedding.embed_text("semantic query"),
            limit=5,
            document_ids=[second.document_id],
        )
        self.assertEqual([item.chunk.document_id for item in filtered], [second.document_id])

    def test_null_embedding_returns_empty_and_wrong_dimension_fails(self) -> None:
        chunk = self._save_chunk("no vector", embedding=None)

        results, total = self.provider.search(
            DocumentRetrievalSearchRequest(query="no vector", retrieval_mode="vector")
        )

        self.assertEqual((results, total), ([], 0))
        with self.assertRaises(EmbeddingValidationError):
            self.chunks.update_embedding(chunk.chunk_id, [0.0])

    def test_vector_only_hit_and_stable_cosine_ordering(self) -> None:
        exact = self._save_chunk(
            "content without lexical overlap",
            embedding=self.embedding.embed_text("semantic query"),
        )
        self._save_chunk("another chunk", embedding=self.embedding.embed_text("different query"))
        request = DocumentRetrievalSearchRequest(
            query="semantic query",
            retrieval_mode="vector",
            top_k=1,
        )

        first, _ = self.provider.search(request)
        second, _ = self.provider.search(request)

        self.assertEqual(first, second)
        self.assertEqual(first[0].chunk_id, exact.chunk_id)
        self.assertEqual(first[0].retrieval_method, "vector")
        self.assertEqual(first[0].content, exact.content)

    def test_hybrid_supports_keyword_only_vector_only_and_deduplicates(self) -> None:
        keyword_only = self._save_chunk("inventory policy", embedding=None)
        vector_only = self._save_chunk(
            "semantic evidence",
            embedding=self.embedding.embed_text("inventory policy"),
        )

        results, total = self.provider.search(
            DocumentRetrievalSearchRequest(query="inventory policy", retrieval_mode="hybrid")
        )

        self.assertEqual(total, 2)
        self.assertEqual({item.chunk_id for item in results}, {keyword_only.chunk_id, vector_only.chunk_id})
        self.assertTrue(all(item.retrieval_method == "hybrid" for item in results))
        self.assertEqual(len(results), len({item.chunk_id for item in results}))

    def test_hybrid_without_embeddings_falls_back_to_keyword(self) -> None:
        expected = self._save_chunk("fallback keyword", embedding=None)

        results, total = self.provider.search(
            DocumentRetrievalSearchRequest(query="fallback", retrieval_mode="hybrid")
        )

        self.assertEqual(total, 1)
        self.assertEqual(results[0].chunk_id, expected.chunk_id)
        self.assertEqual(results[0].retrieval_method, "hybrid")

    def test_hybrid_empty_result_remains_empty(self) -> None:
        self._save_chunk("available evidence", embedding=None)

        results, total = self.provider.search(
            DocumentRetrievalSearchRequest(query="missing", retrieval_mode="hybrid")
        )

        self.assertEqual((results, total), ([], 0))

    def _save_chunk(self, content: str, *, embedding) -> DocumentChunk:
        document_id = f"doc-{uuid4().hex}"
        metadata = DocumentMetadata.from_mapping(
            {
                "document_id": document_id,
                "title": content,
                "owner": "retrieval-test",
                "language": "en",
                "document_type": "text",
                "status": "uploaded",
                "source": {"source_type": "test", "uri": f"test://{document_id}"},
                "checksum": f"sha256:{uuid4().hex}",
            }
        )
        document = Document.create(content, metadata)
        self.documents.create(document)
        chunk = DocumentChunk(
            document_id=document_id,
            version=1,
            chunk_id=f"chk-{uuid4().hex}",
            chunk_index=0,
            content=content,
            character_count=len(content),
            metadata=metadata,
            embedding=embedding,
        )
        self.chunks.replace_for_document(document_id, 1, [chunk])
        return chunk


if __name__ == "__main__":
    unittest.main()
