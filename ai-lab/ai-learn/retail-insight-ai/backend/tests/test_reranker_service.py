from __future__ import annotations

import unittest
from datetime import datetime, timezone

from app.config.reranker import RerankerConfig
from app.models.document import DocumentStatus, DocumentType, Language
from app.schemas.document_api import DocumentResponse, DocumentSourceResponse
from app.schemas.document_retrieval_api import DocumentRetrievalResultResponse
from app.services.reranker_provider import DeterministicRerankerProvider, RerankerProvider
from app.services.reranker_service import RerankerService


class _RecordingProvider(RerankerProvider):
    name = "recording"

    def __init__(self) -> None:
        self.received: list[DocumentRetrievalResultResponse] = []
        self._delegate = DeterministicRerankerProvider()

    def rerank(
        self,
        query: str,
        chunks: list[DocumentRetrievalResultResponse],
    ):
        self.received = list(chunks)
        return self._delegate.rerank(query, chunks)


class _FailingProvider(RerankerProvider):
    name = "failing"

    def rerank(
        self,
        query: str,
        chunks: list[DocumentRetrievalResultResponse],
    ):
        raise RuntimeError("reranker unavailable")


class RerankerServiceTest(unittest.TestCase):
    """验证 deterministic provider、Top-N/Top-K 和无损 fallback。"""

    def setUp(self) -> None:
        self.source = DocumentSourceResponse(
            source_type="local_file",
            uri="upload://doc-1",
            label="policy.md",
            external_id=None,
        )
        self.metadata = DocumentResponse(
            document_id="doc-1",
            title="Retail Policy",
            description="Policy summary",
            owner="analysis-team",
            created_at=datetime(2026, 7, 14, tzinfo=timezone.utc),
            updated_at=datetime(2026, 7, 14, tzinfo=timezone.utc),
            version=1,
            language=Language.EN,
            document_type=DocumentType.MARKDOWN,
            status=DocumentStatus.VALIDATED,
            tags=("policy", "sales"),
            source=self.source,
            checksum="sha256-test",
        )

    def _chunk(
        self,
        chunk_id: str,
        content: str,
        *,
        score: float = 0.5,
        chunk_index: int = 0,
        document_id: str = "doc-1",
    ) -> DocumentRetrievalResultResponse:
        metadata = self.metadata.model_copy(update={"document_id": document_id})
        return DocumentRetrievalResultResponse(
            document_id=document_id,
            chunk_id=chunk_id,
            chunk_index=chunk_index,
            content=content,
            content_excerpt=content,
            score=score,
            retrieval_method="hybrid",
            source=self.source,
            metadata=metadata,
        )

    def test_deterministic_sort_is_stable_across_provider_instances(self) -> None:
        chunks = [
            self._chunk("chk-a", "general policy notes", score=0.95),
            self._chunk("chk-b", "monthly sales policy details", score=0.45, chunk_index=1),
            self._chunk("chk-c", "monthly sales overview", score=0.60, chunk_index=2),
        ]

        first = DeterministicRerankerProvider().rerank("monthly sales policy", chunks)
        second = DeterministicRerankerProvider().rerank("monthly sales policy", chunks)

        self.assertEqual(first, second)
        self.assertEqual(first[0].chunk.chunk_id, "chk-b")
        self.assertEqual(
            [item.rerank_score for item in first],
            sorted((item.rerank_score for item in first), reverse=True),
        )

    def test_top_n_candidates_and_final_top_k_are_applied(self) -> None:
        provider = _RecordingProvider()
        service = RerankerService(
            provider,
            RerankerConfig(candidate_limit=3, top_k=2),
        )
        chunks = [self._chunk(f"chk-{index}", f"sales policy {index}") for index in range(5)]

        outcome = service.rerank("sales policy", chunks)

        self.assertEqual(len(provider.received), 3)
        self.assertEqual(len(outcome.chunks), 2)
        self.assertTrue(outcome.used_provider)

    def test_top_n_expands_when_requested_top_k_is_larger(self) -> None:
        provider = _RecordingProvider()
        service = RerankerService(
            provider,
            RerankerConfig(candidate_limit=2, top_k=1),
        )
        chunks = [self._chunk(f"chk-{index}", "sales policy") for index in range(4)]

        outcome = service.rerank("sales policy", chunks, top_k=4)

        self.assertEqual(service.candidate_limit_for(4), 4)
        self.assertEqual(len(provider.received), 4)
        self.assertEqual(len(outcome.chunks), 4)

    def test_original_chunk_content_score_and_metadata_are_not_modified(self) -> None:
        chunk = self._chunk("chk-1", "monthly sales policy", score=0.37)
        before = chunk.model_dump()

        ranked = DeterministicRerankerProvider().rerank("monthly sales policy", [chunk])

        self.assertEqual(chunk.model_dump(), before)
        self.assertEqual(ranked[0].chunk.content, chunk.content)
        self.assertEqual(ranked[0].chunk.score, 0.37)
        self.assertEqual(ranked[0].chunk.metadata, chunk.metadata)
        self.assertIsNotNone(ranked[0].rerank_score)
        self.assertIn("keyword_coverage", ranked[0].reason)
        self.assertEqual(ranked[0].metadata["provider"], "deterministic")

    def test_duplicate_chunk_identity_is_returned_once(self) -> None:
        first = self._chunk("chk-duplicate", "monthly sales policy", score=0.8)
        duplicate = first.model_copy(deep=True)

        ranked = DeterministicRerankerProvider().rerank(
            "monthly sales policy",
            [first, duplicate],
        )

        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0].chunk.chunk_id, "chk-duplicate")

    def test_equal_content_with_different_chunk_ids_is_preserved(self) -> None:
        ranked = DeterministicRerankerProvider().rerank(
            "sales policy",
            [
                self._chunk("chk-a", "sales policy", score=0.5),
                self._chunk("chk-b", "sales policy", score=0.5, chunk_index=1),
            ],
        )

        self.assertEqual({item.chunk.chunk_id for item in ranked}, {"chk-a", "chk-b"})

    def test_empty_and_single_chunk_inputs_are_supported(self) -> None:
        service = RerankerService(DeterministicRerankerProvider())

        empty = service.rerank("sales policy", [])
        single = service.rerank("sales policy", [self._chunk("chk-1", "sales policy")])

        self.assertEqual(empty.chunks, ())
        self.assertFalse(empty.used_provider)
        self.assertEqual(len(single.chunks), 1)
        self.assertTrue(single.used_provider)

    def test_disabled_provider_preserves_hybrid_order(self) -> None:
        chunks = [
            self._chunk("chk-first", "other", score=0.9),
            self._chunk("chk-second", "sales policy", score=0.1, chunk_index=1),
        ]
        service = RerankerService(
            DeterministicRerankerProvider(),
            RerankerConfig(enabled=False),
        )

        outcome = service.rerank("sales policy", chunks, top_k=2)

        self.assertEqual([item.chunk.chunk_id for item in outcome.chunks], ["chk-first", "chk-second"])
        self.assertFalse(outcome.used_provider)
        self.assertEqual(outcome.fallback_reason, "disabled")
        self.assertIsNone(outcome.chunks[0].rerank_score)

    def test_missing_provider_preserves_hybrid_order(self) -> None:
        chunks = [self._chunk("chk-1", "sales policy")]

        outcome = RerankerService(None).rerank("sales policy", chunks)

        self.assertEqual(outcome.chunks[0].chunk, chunks[0])
        self.assertEqual(outcome.fallback_reason, "missing_provider")

    def test_provider_exception_preserves_hybrid_order(self) -> None:
        chunks = [
            self._chunk("chk-first", "other", score=0.9),
            self._chunk("chk-second", "sales policy", score=0.1, chunk_index=1),
        ]

        outcome = RerankerService(_FailingProvider()).rerank("sales policy", chunks, top_k=2)

        self.assertEqual([item.chunk.chunk_id for item in outcome.chunks], ["chk-first", "chk-second"])
        self.assertFalse(outcome.used_provider)
        self.assertEqual(outcome.fallback_reason, "provider_error")


if __name__ == "__main__":
    unittest.main()
