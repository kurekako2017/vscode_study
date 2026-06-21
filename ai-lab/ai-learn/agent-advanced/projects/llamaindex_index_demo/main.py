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

# 当前脚本目录。
BASE_DIR = Path(__file__).resolve().parent
# 示例文件目录。
ASSETS_DIR = BASE_DIR / "assets"


@dataclass
class Node:
    # 节点 ID。
    node_id: int
    # 原始文件名。
    source: str
    # 节点文本。
    text: str


@dataclass
class QueryResult:
    # 命中的节点。
    node: Node
    # 匹配分数。
    score: float


# 解析查询内容和 top-k 参数。
def parse_args() -> argparse.Namespace:
    # 创建参数解析器。
    parser = argparse.ArgumentParser(description="LlamaIndex 风格概念 demo")
    # 查询问题。
    parser.add_argument(
        "query",
        nargs="?",
        default="LlamaIndex 和 LangChain 有什么区别？",
        help="要查询的问题",
    )
    # top-k 参数。
    parser.add_argument("--top-k", type=int, default=3)
    # 返回解析结果。
    return parser.parse_args()


# 读取示例文档，返回文件名和正文。
def load_documents() -> list[tuple[str, str]]:
    # 这里返回 (文件名, 内容) 的列表。
    documents: list[tuple[str, str]] = []
    # 扫描 assets 目录下的 Markdown 文件。
    for path in sorted(ASSETS_DIR.glob("*.md")):
        documents.append((path.name, path.read_text(encoding="utf-8")))
    # 返回所有文档。
    return documents


# 把每篇文档按段落切成 Node。
def split_into_nodes(documents: list[tuple[str, str]]) -> list[Node]:
    # nodes 保存切分后的节点。
    nodes: list[Node] = []
    # 从 1 开始编号，便于阅读。
    node_id = 1
    # 遍历每篇文档。
    for source, text in documents:
        # 按空行切分章节。
        sections = [section.strip() for section in re.split(r"\n\s*\n", text) if section.strip()]
        # 每个章节都变成一个 Node。
        for section in sections:
            nodes.append(Node(node_id=node_id, source=source, text=section))
            node_id += 1
    # 返回所有节点。
    return nodes


# 为节点构建倒排索引，方便快速召回。
def build_inverted_index(nodes: list[Node]) -> dict[str, set[int]]:
    # 倒排索引：token -> node_id 集合。
    index: dict[str, set[int]] = defaultdict(set)
    # 遍历所有节点。
    for node in nodes:
        # 从文本里提取 token。
        tokens = re.findall(r"[A-Za-z0-9_+-]{2,}|[\u4e00-\u9fff]{2,}", node.text.lower())
        for token in tokens:
            index[token].add(node.node_id)
    # 返回倒排索引。
    return index


# 为查询补充相关词，提升检索覆盖率。
def expand_query(query: str) -> list[str]:
    # 先提取原始词。
    terms = re.findall(r"[A-Za-z0-9_+-]{2,}|[\u4e00-\u9fff]{2,}", query.lower())
    # LangChain 问题补充关联词。
    if "langchain" in query.lower():
        terms.extend(["prompt", "runnable", "tool"])
    # LangGraph 问题补充关联词。
    if "langgraph" in query.lower():
        terms.extend(["state", "node", "edge", "graph"])
    # RAG 问题补充关联词。
    if "rag" in query.lower() or "检索" in query:
        terms.extend(["检索", "node", "index", "citation"])
    # 对比类问题补充区别/对比。
    if "区别" in query or "对比" in query:
        terms.extend(["区别", "对比"])
    # 去重后返回。
    return list(dict.fromkeys([term for term in terms if len(term) >= 2]))


# 利用倒排索引召回节点并打分排序。
def retrieve(nodes: list[Node], index: dict[str, set[int]], query: str, top_k: int) -> list[QueryResult]:
    # 把 query 转成可检索词。
    query_terms = expand_query(query)
    # 每个 node_id 的总分。
    scores: dict[int, float] = defaultdict(float)
    # 先利用倒排索引做粗召回。
    for term in query_terms:
        matched_ids = index.get(term, set())
        for node_id in matched_ids:
            scores[node_id] += 1.0
    # 再做一轮文本级别的轻微加分。
    for node in nodes:
        text = node.text.lower()
        for term in query_terms:
            if term.lower() in text:
                scores[node.node_id] += 0.2
        # Markdown 标题节点通常信息密度更高。
        if node.text.lstrip().startswith("#"):
            scores[node.node_id] += 0.1
    # 把有分的节点转成 QueryResult。
    ranked = [
        QueryResult(node=node, score=scores[node.node_id])
        for node in nodes
        if scores[node.node_id] > 0
    ]
    # 结果按分数从高到低排序。
    ranked.sort(key=lambda item: item.score, reverse=True)
    # 返回前 top_k 个。
    return ranked[:top_k]


# 根据召回结果拼出带引用的回答。
def synthesize_answer(query: str, results: list[QueryResult]) -> str:
    # 先写问题。
    lines = [f"查询：{query}", "", "LlamaIndex 风格回答："]
    # 把命中的节点作为引用列出来。
    for idx, result in enumerate(results, 1):
        excerpt = result.node.text.replace("\n", " ")[:140]
        lines.append(f"{idx}. [{result.node.source}#{result.node.node_id}] {excerpt}")
    # 最后补一个总结。
    lines.append("")
    lines.append("结论：LlamaIndex 更像是把文档和查询结构化，然后交给查询引擎去组织答案。")
    # 返回多行文本。
    return "\n".join(lines)


# 程序入口，串联文档加载、索引和回答生成。
def main() -> None:
    print("MODEL: provider=local model=none mode=local-index")
    # 读取命令行参数。
    args = parse_args()
    # 加载文档。
    documents = load_documents()
    # 切成节点。
    nodes = split_into_nodes(documents)
    # 建立倒排索引。
    index = build_inverted_index(nodes)
    # 进行检索。
    results = retrieve(nodes, index, args.query, args.top_k)

    # 打印文档统计。
    print("=== 1. 文档 ===")
    for source, text in documents:
        print(f"- {source}: {len(text)} chars")

    # 打印 node 数量。
    print("\n=== 2. Node 数量 ===")
    print(len(nodes))

    # 打印召回结果。
    print("\n=== 3. 召回结果 ===")
    for result in results:
        print(f"- score={result.score:.2f} node={result.node.node_id} source={result.node.source}")

    # 打印最终回答。
    print("\n=== 4. 最终回答 ===")
    print(synthesize_answer(args.query, results))


if __name__ == "__main__":
    main()
