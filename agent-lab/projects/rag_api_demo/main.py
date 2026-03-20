import os
import re
from dataclasses import dataclass
from pathlib import Path

from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel, Field
from pypdf import PdfReader


DEFAULT_MODEL = "gpt-5"
DEFAULT_DOCS_DIR = "."
SUPPORTED_EXTENSIONS = {".md", ".txt", ".pdf"}
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200
TOP_K = 4
SYSTEM_INSTRUCTIONS = (
    "You are a document QA assistant for a Japanese IT project learning lab. "
    "Answer only from the provided retrieved context. "
    "If the context is insufficient, say that clearly. "
    "Mention source labels when possible."
)


@dataclass
class Chunk:
    source_label: str
    content: str
    score: int = 0


class AskRequest(BaseModel):
    question: str = Field(min_length=1, description="Question about local documents.")
    model: str = Field(default=DEFAULT_MODEL, description="OpenAI model to use.")


class SourceItem(BaseModel):
    source_label: str
    score: int


class AskResponse(BaseModel):
    answer: str
    model: str
    docs_dir: str
    source_count: int
    sources: list[SourceItem]


class ReloadResponse(BaseModel):
    docs_dir: str
    chunk_count: int


def build_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key)


def get_docs_dir() -> Path:
    docs_dir = os.getenv("RAG_API_DOCS_DIR", DEFAULT_DOCS_DIR)
    path = Path(docs_dir).resolve()
    if not path.exists() or not path.is_dir():
        raise RuntimeError("RAG_API_DOCS_DIR must point to an existing directory.")
    return path


def iter_text_files(base_dir: Path) -> list[Path]:
    files = []
    for path in base_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path)
    return sorted(files)


def read_document_text(file_path: Path) -> str:
    suffix = file_path.suffix.lower()

    if suffix in {".md", ".txt"}:
        return file_path.read_text(encoding="utf-8")

    if suffix == ".pdf":
        # PDF text extraction quality depends on the original document structure.
        reader = PdfReader(str(file_path))
        pages = []
        for index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append(f"[PAGE {index}]\n{text}")
        return "\n\n".join(pages)

    raise ValueError(f"Unsupported file type: {suffix}")


def chunk_text(text: str) -> list[str]:
    normalized = text.replace("\r\n", "\n").strip()
    if not normalized:
        return []

    chunks = []
    start = 0
    # Overlap keeps adjacent chunks from losing too much local context.
    while start < len(normalized):
        end = min(len(normalized), start + CHUNK_SIZE)
        chunks.append(normalized[start:end])
        if end >= len(normalized):
            break
        start = end - CHUNK_OVERLAP
    return chunks


def build_chunks(base_dir: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    for file_path in iter_text_files(base_dir):
        try:
            text = read_document_text(file_path)
        except (UnicodeDecodeError, ValueError):
            continue

        relative = file_path.relative_to(base_dir)
        for index, part in enumerate(chunk_text(text), start=1):
            chunks.append(Chunk(source_label=f"{relative}#chunk{index}", content=part))
    return chunks


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[A-Za-z0-9_\-\u4e00-\u9fff\u3040-\u30ff]+", text.lower()))


def retrieve(question: str, chunks: list[Chunk]) -> list[Chunk]:
    question_tokens = tokenize(question)
    ranked: list[Chunk] = []

    # This PoC keeps retrieval local and cheap by using keyword overlap instead of embeddings.
    for chunk in chunks:
        chunk_tokens = tokenize(chunk.content)
        score = len(question_tokens & chunk_tokens)
        if score > 0:
            ranked.append(Chunk(chunk.source_label, chunk.content, score))

    ranked.sort(key=lambda item: (-item.score, item.source_label))
    return ranked[:TOP_K]


def build_context(top_chunks: list[Chunk]) -> str:
    if not top_chunks:
        return "No relevant local document chunks were retrieved."

    parts = []
    for chunk in top_chunks:
        parts.append(f"[SOURCE: {chunk.source_label}]\n{chunk.content}")
    return "\n\n".join(parts)


def answer_question(client: OpenAI, model: str, question: str, context: str) -> str:
    # The model is asked to answer only from retrieved context so the API behaves like a minimal RAG service.
    prompt = (
        f"Question:\n{question}\n\n"
        f"Retrieved context:\n{context}\n\n"
        "Answer the question based only on the retrieved context. "
        "If the answer is not fully supported, say so clearly."
    )
    response = client.responses.create(
        model=model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=prompt,
    )
    return response.output_text


app = FastAPI(title="rag_api_demo", version="0.1.0")
app.state.client = None
app.state.docs_dir = None
app.state.chunks = []


def load_state() -> None:
    docs_dir = get_docs_dir()
    chunks = build_chunks(docs_dir)
    if not chunks:
        raise RuntimeError("No readable .md, .txt, or .pdf files were found in docs directory.")
    # Cache the parsed chunks in memory so each request does not rescan the directory.
    app.state.client = build_client()
    app.state.docs_dir = docs_dir
    app.state.chunks = chunks


@app.on_event("startup")
def startup_event() -> None:
    load_state()


@app.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "docs_dir": str(app.state.docs_dir),
        "chunk_count": len(app.state.chunks),
    }


@app.post("/reload", response_model=ReloadResponse)
def reload_docs() -> ReloadResponse:
    try:
        load_state()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return ReloadResponse(
        docs_dir=str(app.state.docs_dir),
        chunk_count=len(app.state.chunks),
    )


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    if app.state.client is None or app.state.docs_dir is None:
        raise HTTPException(status_code=500, detail="Service is not initialized.")

    # Retrieve first, then pass only the top chunks to the model.
    top_chunks = retrieve(request.question, app.state.chunks)
    context = build_context(top_chunks)

    try:
        answer = answer_question(
            app.state.client,
            request.model,
            request.question,
            context,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return AskResponse(
        answer=answer,
        model=request.model,
        docs_dir=str(app.state.docs_dir),
        source_count=len(top_chunks),
        sources=[
            SourceItem(source_label=chunk.source_label, score=chunk.score)
            for chunk in top_chunks
        ],
    )
