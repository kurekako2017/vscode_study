"""LlamaIndex 风格的概念 demo。

说明：
这个脚本不依赖真实的 llama-index 包，而是用纯 Python 做一个
“Document -> Node -> Index -> QueryEngine -> ResponseSynthesizer”的
最小实现，方便先理解概念。
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"


@dataclass
class Node:
    node_id: int
    source: str
    text: str


@dataclass
class QueryResult:
    node: Node
    score: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LlamaIndex 风格概念 demo")
    parser.add_argument(
        "query",
        nargs="?",
        default="LlamaIndex 和 LangChain 有什么区别？",
        help="要查询的问题",
    )
    parser.add_argument("--top-k", type=int, default=3)
    return parser.parse_args()


def load_documents() -> list[tuple[str, str]]:
    documents: list[tuple[str, str]] = []
    for path in sorted(ASSETS_DIR.glob("*.md")):
        documents.append((path.name, path.read_text(encoding="utf-8")))
    return documents


def split_into_nodes(documents: list[tuple[str, str]]) -> list[Node]:
    nodes: list[Node] = []
    node_id = 1
    for source, text in documents:
        sections = [section.strip() for section in re.split(r"\n\s*\n", text) if section.strip()]
        for section in sections:
            nodes.append(Node(node_id=node_id, source=source, text=section))
            node_id += 1
    return nodes


def build_inverted_index(nodes: list[Node]) -> dict[str, set[int]]:
    index: dict[str, set[int]] = defaultdict(set)
    for node in nodes:
        tokens = re.findall(r"[A-Za-z0-9_+-]{2,}|[\u4e00-\u9fff]{2,}", node.text.lower())
        for token in tokens:
            index[token].add(node.node_id)
    return index


def expand_query(query: str) -> list[str]:
    terms = re.findall(r"[A-Za-z0-9_+-]{2,}|[\u4e00-\u9fff]{2,}", query.lower())
    if "langchain" in query.lower():
        terms.extend(["prompt", "runnable", "tool"])
    if "langgraph" in query.lower():
        terms.extend(["state", "node", "edge", "graph"])
    if "rag" in query.lower() or "检索" in query:
        terms.extend(["检索", "node", "index", "citation"])
    if "区别" in query or "对比" in query:
        terms.extend(["区别", "对比"])
    return list(dict.fromkeys([term for term in terms if len(term) >= 2]))


def retrieve(nodes: list[Node], index: dict[str, set[int]], query: str, top_k: int) -> list[QueryResult]:
    query_terms = expand_query(query)
    scores: dict[int, float] = defaultdict(float)
    for term in query_terms:
        matched_ids = index.get(term, set())
        for node_id in matched_ids:
            scores[node_id] += 1.0
    for node in nodes:
        text = node.text.lower()
        for term in query_terms:
            if term.lower() in text:
                scores[node.node_id] += 0.2
        if node.text.lstrip().startswith("#"):
            scores[node.node_id] += 0.1
    ranked = [
        QueryResult(node=node, score=scores[node.node_id])
        for node in nodes
        if scores[node.node_id] > 0
    ]
    ranked.sort(key=lambda item: item.score, reverse=True)
    return ranked[:top_k]


def synthesize_answer(query: str, results: list[QueryResult]) -> str:
    lines = [f"查询：{query}", "", "LlamaIndex 风格回答："]
    for idx, result in enumerate(results, 1):
        excerpt = result.node.text.replace("\n", " ")[:140]
        lines.append(f"{idx}. [{result.node.source}#{result.node.node_id}] {excerpt}")
    lines.append("")
    lines.append("结论：LlamaIndex 更像是把文档和查询结构化，然后交给查询引擎去组织答案。")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    documents = load_documents()
    nodes = split_into_nodes(documents)
    index = build_inverted_index(nodes)
    results = retrieve(nodes, index, args.query, args.top_k)

    print("=== 1. 文档 ===")
    for source, text in documents:
        print(f"- {source}: {len(text)} chars")

    print("\n=== 2. Node 数量 ===")
    print(len(nodes))

    print("\n=== 3. 召回结果 ===")
    for result in results:
        print(f"- score={result.score:.2f} node={result.node.node_id} source={result.node.source}")

    print("\n=== 4. 最终回答 ===")
    print(synthesize_answer(args.query, results))


if __name__ == "__main__":
    main()
