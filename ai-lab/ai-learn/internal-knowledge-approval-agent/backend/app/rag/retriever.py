from app.rag.documents import DOCUMENTS, Document


def retrieve_documents(_: str) -> tuple[Document, ...]:
    """Phase-two deterministic local retriever; no network or model dependency."""

    return DOCUMENTS
