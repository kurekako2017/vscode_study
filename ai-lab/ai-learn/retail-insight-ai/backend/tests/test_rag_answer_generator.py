from __future__ import annotations

import unittest
from datetime import datetime, timezone

from app.models.document import DocumentStatus, DocumentType, Language
from app.models.internal_rag import RAGFallbackReason
from app.providers.stub_llm_provider import StubLLMProvider
from app.schemas.document_api import DocumentResponse, DocumentSourceResponse
from app.schemas.document_retrieval_api import DocumentRetrievalResultResponse
from app.schemas.internal_rag_api import InternalRagAnswerMode, InternalRagAnswerRequest
from app.services.rag_answer_generator import RAGAnswerGenerator


class _TimeoutProvider:
    name = "timeout"

    def generate(self, context):  # type: ignore[no-untyped-def]
        raise TimeoutError("provider timeout")


class _InvalidProvider:
    name = "invalid"

    def generate(self, context):  # type: ignore[no-untyped-def]
        return {"answer": "", "citations": [], "usage": {}}


class RAGAnswerGeneratorTest(unittest.TestCase):
    """验证 RAGAnswerGenerator 的默认路径、stub provider 和 fallback 行为。"""

    def _retrieval_result(self, excerpt: str = "Monthly sales policy summary and rules."):
        source = DocumentSourceResponse(
            source_type="local_file",
            uri="upload://doc-1",
            label="policy.md",
            external_id=None,
        )
        metadata = DocumentResponse(
            document_id="doc-1",
            title="Monthly Sales Policy",
            description="Policy summary",
            owner="analysis-team",
            created_at=datetime(2026, 7, 4, tzinfo=timezone.utc),
            updated_at=datetime(2026, 7, 4, tzinfo=timezone.utc),
            version=1,
            language=Language.EN,
            document_type=DocumentType.MARKDOWN,
            status=DocumentStatus.VALIDATED,
            tags=("policy", "sales"),
            source=source,
            checksum="sha256-123",
        )
        return DocumentRetrievalResultResponse(
            document_id="doc-1",
            chunk_id="chk-1",
            chunk_index=0,
            content=excerpt,
            content_excerpt=excerpt,
            score=0.91,
            source=source,
            metadata=metadata,
        )

    def _request(self) -> InternalRagAnswerRequest:
        return InternalRagAnswerRequest(
            question="What is the monthly sales policy?",
            limit=5,
            answer_mode=InternalRagAnswerMode.EXTRACTIVE,
            require_citations=True,
        )

    def test_default_deterministic_path(self) -> None:
        generator = RAGAnswerGenerator()
        result = generator.generate(
            request=self._request(),
            question="What is the monthly sales policy?",
            retrieval_results=[self._retrieval_result()],
            total_matches=1,
        )

        self.assertFalse(result.used_llm_provider)
        self.assertEqual(result.provider_name, "deterministic")
        self.assertEqual(result.fallback_reason, RAGFallbackReason.DISABLED)
        self.assertTrue(result.answer.startswith("Extractive answer:"))
        self.assertEqual(result.usage.provider_name, "deterministic")
        self.assertEqual(result.usage.prompt_tokens, 0)
        self.assertEqual(result.usage.completion_tokens, 0)
        self.assertEqual(result.usage.estimated_cost, 0.0)
        self.assertEqual(result.usage.latency_ms, 0)

    def test_stub_provider_path(self) -> None:
        generator = RAGAnswerGenerator(provider=StubLLMProvider(), use_llm=True)
        result = generator.generate(
            request=self._request(),
            question="What is the monthly sales policy?",
            retrieval_results=[self._retrieval_result()],
            total_matches=1,
        )

        self.assertTrue(result.used_llm_provider)
        self.assertEqual(result.provider_name, "stub")
        self.assertEqual(result.fallback_reason, RAGFallbackReason.NONE)
        self.assertTrue(result.answer.startswith("Stub extractive answer:"))
        self.assertEqual(result.usage.provider_name, "stub")
        self.assertGreater(result.usage.prompt_tokens, 0)
        self.assertGreater(result.usage.completion_tokens, 0)
        self.assertGreater(result.usage.estimated_cost, 0.0)
        self.assertGreater(result.usage.latency_ms, 0)

    def test_provider_failure_falls_back_to_deterministic_mode(self) -> None:
        generator = RAGAnswerGenerator(provider=_TimeoutProvider(), use_llm=True)
        result = generator.generate(
            request=self._request(),
            question="What is the monthly sales policy?",
            retrieval_results=[self._retrieval_result()],
            total_matches=1,
        )

        self.assertFalse(result.used_llm_provider)
        self.assertEqual(result.provider_name, "timeout")
        self.assertEqual(result.fallback_reason, RAGFallbackReason.TIMEOUT)
        self.assertTrue(result.answer.startswith("Extractive answer:"))

    def test_invalid_provider_output_falls_back_to_deterministic_mode(self) -> None:
        generator = RAGAnswerGenerator(provider=_InvalidProvider(), use_llm=True)
        result = generator.generate(
            request=self._request(),
            question="What is the monthly sales policy?",
            retrieval_results=[self._retrieval_result()],
            total_matches=1,
        )

        self.assertFalse(result.used_llm_provider)
        self.assertEqual(result.provider_name, "invalid")
        self.assertEqual(result.fallback_reason, RAGFallbackReason.INVALID_OUTPUT)
        self.assertTrue(result.answer.startswith("Extractive answer:"))


if __name__ == "__main__":
    unittest.main()
