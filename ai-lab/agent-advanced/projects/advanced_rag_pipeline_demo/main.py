"""高级 RAG 风格 demo。

展示一个最小但完整的检索增强流水线：
1. 加载文档
2. 切分 chunk
3. rewrite query
4. 检索
5. rerank
6. 生成带引用的答案

默认使用本地资产，无需任何 Key。
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"


@dataclass
class ChunkScore:
    document: Document
    score: float
    matched_terms: list[str] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="高级 RAG 风格 demo")
    parser.add_argument(
        "query",
        nargs="?",
        default="LangGraph 适合什么场景，RAG 怎么做引用和重排？",
        help="要检索的问题",
    )
    parser.add_argument("--top-k", type=int, default=4, help="返回前几个 chunk")
    return parser.parse_args()


def load_documents() -> list[Document]:
    docs: list[Document] = []
    for path in sorted(ASSETS_DIR.glob("*.md")):
        docs.append(Document(page_content=path.read_text(encoding="utf-8"), metadata={"source": path.name}))
    return docs


def chunk_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=320, chunk_overlap=80)
    chunks = splitter.split_documents(documents)
    for idx, chunk in enumerate(chunks, 1):
        chunk.metadata["chunk_id"] = idx
    return chunks


ALIASES = {
    "langchain": ["langchain", "链", "prompt", "runnable", "tool calling"],
    "llamaindex": ["llamaindex", "索引", "query engine", "node parser"],
    "langgraph": ["langgraph", "state", "node", "edge", "循环", "分支"],
    "rag": ["rag", "检索", "向量", "rerank", "multi-query", "引用", "召回"],
    "multi-agent": ["multi-agent", "多 agent", "supervisor", "planner", "critic"],
}


def rewrite_queries(query: str) -> list[str]:
    variants = [query]
    lower = query.lower()
    if "区别" in query or "对比" in query:
        variants.append(query.replace("区别", "对比"))
    if "rag" in lower or "检索" in query:
        variants.append("高级 RAG 检索 重排 引用")
    if "agent" in lower or "多智能体" in query:
        variants.append("多 Agent 监督者 协作")
    if "langgraph" in lower:
        variants.append("LangGraph 状态图 节点 边")
    return list(dict.fromkeys(variants))


def expand_terms(query: str) -> list[str]:
    terms = set()
    lower = query.lower()
    for aliases in ALIASES.values():
        for alias in aliases:
            if alias.lower() in lower or alias in query:
                terms.update(aliases)
    tokens = [tok for tok in re.split(r"[^\w\u4e00-\u9fff]+", query) if len(tok) >= 2]
    terms.update(tokens)
    terms.update(rewrite_queries(query))
    return [term for term in terms if len(term) >= 2]


def score_chunk(document: Document, terms: Iterable[str]) -> ChunkScore:
    text = (document.page_content + " " + document.metadata.get("source", "")).lower()
    matched: list[str] = []
    score = 0.0
    for term in terms:
        term_l = term.lower()
        if term_l in text:
            matched.append(term)
            score += 1.0
            score += min(text.count(term_l), 3) * 0.3
    if document.page_content.lstrip().startswith("#"):
        score += 0.5
    if "source" in document.metadata:
        score += 0.2
    return ChunkScore(document=document, score=score, matched_terms=matched)


def retrieve(chunks: list[Document], query: str, top_k: int) -> list[ChunkScore]:
    terms = expand_terms(query)
    scored = [score_chunk(chunk, terms) for chunk in chunks]
    scored.sort(key=lambda item: item.score, reverse=True)
    return scored[:top_k]


def rerank(results: list[ChunkScore]) -> list[ChunkScore]:
    reranked = []
    for item in results:
        bonus = 0.0
        content = item.document.page_content.lower()
        if "步骤" in item.document.page_content or "管线" in item.document.page_content:
            bonus += 0.4
        if "引用" in item.document.page_content or "source" in content:
            bonus += 0.2
        reranked.append(ChunkScore(item.document, item.score + bonus, item.matched_terms))
    reranked.sort(key=lambda item: item.score, reverse=True)
    return reranked


def synthesize_answer(query: str, results: list[ChunkScore]) -> str:
    lines = [
        f"问题：{query}",
        "",
        "基于检索结果，我会这样回答：",
    ]
    for idx, item in enumerate(results, 1):
        source = item.document.metadata.get("source", "unknown")
        chunk_id = item.document.metadata.get("chunk_id", idx)
        excerpt = item.document.page_content.strip().splitlines()[0][:120]
        lines.append(f"{idx}. [{source}#{chunk_id}] {excerpt}")
    lines.append("")
    lines.append("简要结论：")
    lines.append(
        "高级 RAG 的关键不是单纯向量检索，而是把检索、重排、引用和生成做成稳定流水线。"
    )
    lines.append("如果查询偏向框架选型，可以优先看 LangChain / LlamaIndex / LangGraph 的职责边界。")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    documents = load_documents()
    chunks = chunk_documents(documents)
    retrieved = retrieve(chunks, args.query, args.top_k)
    reranked = rerank(retrieved)
    answer = synthesize_answer(args.query, reranked)

    print("=== 1. 原始文档 ===")
    for doc in documents:
        print(f"- {doc.metadata['source']}: {len(doc.page_content)} chars")

    print("\n=== 2. Chunk 数量 ===")
    print(len(chunks))

    print("\n=== 3. 检索 + Rerank 结果 ===")
    for item in reranked:
        print(
            f"- score={item.score:.2f} source={item.document.metadata.get('source')} "
            f"chunk={item.document.metadata.get('chunk_id')} matched={item.matched_terms}"
        )

    print("\n=== 4. 最终回答 ===")
    print(answer)


if __name__ == "__main__":
    main()
