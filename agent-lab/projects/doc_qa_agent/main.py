"""doc_qa_agent: 本地 RAG 文档问答最小示例。

功能概览：
- 扫描指定目录下的 Markdown / 文本文件
- 将文档切分为重叠的 chunk（用于保证局部上下文）
- 使用简单的关键词重合度做检索（PoC 用法，非向量检索）
- 将检索到的 top-k chunk 拼接为上下文并调用模型回答

本示例适合教学与 PoC，生产环境请替换为 embeddings + 向量检索并添加缓存、限流与认证。
"""

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
    """表示一个文档切分后的小片段（chunk）。"""
    source_label: str
    content: str
    score: int = 0


def parse_args() -> argparse.Namespace:
    """解析命令行参数：问题文本、文档目录与模型名。"""
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
    """从 `OPENAI_API_KEY` 创建 OpenAI 客户端，缺失则退出。"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key)


def iter_text_files(base_dir: Path) -> list[Path]:
    """递归查找支持的文本文件并返回排序后的列表。"""
    files = []
    for path in base_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path)
    return sorted(files)


def chunk_text(text: str) -> list[str]:
    """把长文本切分为带重叠的 chunk，用于保留跨块上下文信息。"""
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
    """读取目录下文件并把文件切分为带标签的 `Chunk` 列表。"""
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
    """对文本进行简单分词（英文、数字、部分中文/日文字符），用于关键词检索示例。"""
    return set(re.findall(r"[A-Za-z0-9_\-\u4e00-\u9fff\u3040-\u30ff]+", text.lower()))


def retrieve(question: str, chunks: list[Chunk]) -> list[Chunk]:
    """基于关键词重合度对 chunk 进行打分并返回 top-k。

    注意：这是教学用的简单检索方法，生产请使用向量检索。
    """
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
    """把 top-k chunks 拼接为模型可读的检索上下文。"""
    if not top_chunks:
        return "No relevant local document chunks were retrieved."

    parts = []
    for chunk in top_chunks:
        parts.append(f"[SOURCE: {chunk.source_label}]\n{chunk.content}")
    return "\n\n".join(parts)


def answer_question(client: OpenAI, model: str, question: str, context: str) -> str:
    """调用模型回答，强制其仅基于传入的检索上下文回答问题。"""
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
