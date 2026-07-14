from __future__ import annotations

import unittest

from app.models.document import Document, DocumentMetadata, DocumentSource, DocumentStatus, DocumentType, Language
from app.models.internal_rag import InternalRagWarning
from app.schemas.document_api import DocumentResponse, DocumentSourceResponse
from app.schemas.document_retrieval_api import DocumentRetrievalResultResponse
from app.schemas.internal_rag_api import InternalRagCitationResponse
from app.services.internal_rag_evaluation_service import InternalRagEvaluationService


class InternalRagEvaluationServiceTest(unittest.TestCase):
    """验证 internal RAG 的 citation quality 和 evaluation 规则。"""

    def setUp(self) -> None:
        self.service = InternalRagEvaluationService()
        source = DocumentSource(source_type="upload_form", uri="upload://upl-1/policy.md", label="policy.md")
        metadata = DocumentMetadata(
            document_id="doc-1",
            title="Monthly Policy",
            description=None,
            owner="analysis-team",
            language=Language.EN,
            document_type=DocumentType.MARKDOWN,
            status=DocumentStatus.VALIDATED,
            tags=("sales",),
            source=source,
            checksum="sha256-test",
        )
        self.document = Document("# Monthly Policy\n\nPolicy details.", metadata)
        self.source_response = DocumentSourceResponse.from_domain(source)
        self.document_response = DocumentResponse.from_domain(self.document)

    def _result(self, *, chunk_id: str = "chk-1", excerpt: str = "Monthly policy details.", score: float = 0.9) -> DocumentRetrievalResultResponse:
        return DocumentRetrievalResultResponse(
            document_id="doc-1",
            chunk_id=chunk_id,
            chunk_index=0,
            content=excerpt,
            content_excerpt=excerpt,
            score=score,
            source=self.source_response,
            metadata=self.document_response,
        )

    def _citation(self, *, chunk_id: str = "chk-1", excerpt: str = "Monthly policy details.", score: float = 0.9) -> InternalRagCitationResponse:
        return InternalRagCitationResponse(
            document_id="doc-1",
            chunk_id=chunk_id,
            chunk_index=0,
            excerpt=excerpt,
            source=self.source_response,
            score=score,
        )

    def test_extractive_answer_has_perfect_citation_score(self) -> None:
        evaluation = self.service.evaluate(
            query="monthly policy",
            answer="Extractive answer:\n1. Monthly policy details.",
            citations=[self._citation()],
            retrieval_results=[self._result()],
            total_matches=1,
        )

        self.assertEqual(evaluation.citation_score, 1.0)
        self.assertEqual(evaluation.coverage_score, 1.0)
        self.assertGreaterEqual(evaluation.confidence, 0.95)
        self.assertEqual(evaluation.warnings, ())

    def test_missing_citation_triggers_warning(self) -> None:
        evaluation = self.service.evaluate(
            query="monthly policy",
            answer="Extractive answer:\n1. Monthly policy details.",
            citations=[self._citation(excerpt="Different excerpt", score=0.2)],
            retrieval_results=[self._result()],
            total_matches=1,
        )

        self.assertLess(evaluation.citation_score, 1.0)
        self.assertIn(InternalRagWarning.MISSING_CITATION, evaluation.warnings)

    def test_weak_match_and_low_context_generate_warnings(self) -> None:
        evaluation = self.service.evaluate(
            query="monthly policy",
            answer="Extractive answer:\n1. Monthly policy details.",
            citations=[self._citation(score=0.2)],
            retrieval_results=[
                self._result(chunk_id="chk-1", score=0.2, excerpt="Monthly policy details."),
                self._result(chunk_id="chk-2", score=0.2, excerpt="Monthly policy details."),
            ],
            total_matches=2,
        )

        self.assertIn(InternalRagWarning.LOW_CONTEXT, evaluation.warnings)
        self.assertIn(InternalRagWarning.WEAK_MATCH, evaluation.warnings)


if __name__ == "__main__":
    unittest.main()
