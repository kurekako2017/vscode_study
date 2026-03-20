import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from openai import OpenAI


DEFAULT_MODEL = "gpt-5"
SUPPORTED_EXTENSIONS = {".md", ".txt"}
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200
TOP_K = 4
SYSTEM_INSTRUCTIONS = (
    "You are a document QA assistant for an LLM agent learning lab. "
    "Answer only from the provided retrieved context. "
    "If the context is insufficient, say that clearly. "
    "When possible, mention the cited source labels."
)


@dataclass
class Chunk:
    source_label: str
    content: str
    score: int = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Minimal local RAG demo for document QA."
    )
    parser.add_argument("question", help="Question to ask about local documents.")
    parser.add_argument(
        "--docs",
        default=".",
        help="Directory containing local markdown or text files. Default: current directory.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model name to use. Default: {DEFAULT_MODEL}",
    )
    return parser.parse_args()


def build_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key)


def iter_text_files(base_dir: Path) -> list[Path]:
    files = []
    for path in base_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path)
    return sorted(files)


def chunk_text(text: str) -> list[str]:
    normalized = text.replace("\r\n", "\n").strip()
    if not normalized:
        return []

    chunks = []
    start = 0
    # Keep a small overlap so answers can still use context that crosses chunk boundaries.
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
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        relative = file_path.relative_to(base_dir)
        for index, part in enumerate(chunk_text(text), start=1):
            label = f"{relative}#chunk{index}"
            chunks.append(Chunk(source_label=str(label), content=part))
    return chunks


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[A-Za-z0-9_\-\u4e00-\u9fff\u3040-\u30ff]+", text.lower()))


def retrieve(question: str, chunks: list[Chunk]) -> list[Chunk]:
    question_tokens = tokenize(question)
    ranked = []

    # This demo uses a simple keyword-overlap score instead of vector search.
    for chunk in chunks:
        chunk_tokens = tokenize(chunk.content)
        overlap = question_tokens & chunk_tokens
        score = len(overlap)
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
    # Constrain the model to the retrieved context so the demo behaves like a minimal RAG flow.
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


def main() -> None:
    args = parse_args()
    base_dir = Path(args.docs).resolve()

    if not base_dir.exists() or not base_dir.is_dir():
        print("ERROR: --docs must be an existing directory.", file=sys.stderr)
        sys.exit(1)

    chunks = build_chunks(base_dir)
    if not chunks:
        print("ERROR: no readable .md or .txt files were found.", file=sys.stderr)
        sys.exit(1)

    # The retrieval step happens before the model call so only the most relevant chunks are sent.
    top_chunks = retrieve(args.question, chunks)
    context = build_context(top_chunks)

    client = build_client()
    try:
        answer = answer_question(client, args.model, args.question, context)
    except Exception as exc:
        print(f"ERROR: request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    print("=== Answer ===")
    print(answer)
    print("\n=== Sources ===")
    if not top_chunks:
        print("No matching chunks found.")
        return

    for chunk in top_chunks:
        print(f"- {chunk.source_label} (score={chunk.score})")


if __name__ == "__main__":
    main()
