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

# 当前脚本所在目录。
BASE_DIR = Path(__file__).resolve().parent
# 示例资产目录。
ASSETS_DIR = BASE_DIR / "assets"


@dataclass
class ChunkScore:
    # 被打分的 chunk 对应的文档对象。
    document: Document
    # 检索得分。
    score: float
    # 命中的关键词列表。
    matched_terms: list[str] = field(default_factory=list)


# 解析查询文本和返回数量等参数。
def parse_args() -> argparse.Namespace:
    # 创建参数解析器。
    parser = argparse.ArgumentParser(description="高级 RAG 风格 demo")
    # 检索问题。
    parser.add_argument(
        "query",
        nargs="?",
        default="LangGraph 适合什么场景，RAG 怎么做引用和重排？",
        help="要检索的问题",
    )
    # 取前几个 chunk。
    parser.add_argument("--top-k", type=int, default=4, help="返回前几个 chunk")
    # 返回解析结果。
    return parser.parse_args()


# 从 assets 目录加载原始文档。
def load_documents() -> list[Document]:
    # 最终返回的文档列表。
    docs: list[Document] = []
    # 遍历 assets 下的所有 Markdown 文件。
    for path in sorted(ASSETS_DIR.glob("*.md")):
        # 每个文件都变成一个 LangChain Document。
        docs.append(Document(page_content=path.read_text(encoding="utf-8"), metadata={"source": path.name}))
    # 返回完整文档集。
    return docs


# 把长文切成适合检索的小 chunk。
def chunk_documents(documents: list[Document]) -> list[Document]:
    # 使用递归切分器，把长文切成更适合检索的小块。
    splitter = RecursiveCharacterTextSplitter(chunk_size=320, chunk_overlap=80)
    # 切分所有文档。
    chunks = splitter.split_documents(documents)
    # 给每个 chunk 编号，方便引用。
    for idx, chunk in enumerate(chunks, 1):
        chunk.metadata["chunk_id"] = idx
    # 返回切分后的 chunk。
    return chunks


ALIASES = {
    "langchain": ["langchain", "链", "prompt", "runnable", "tool calling"],
    "llamaindex": ["llamaindex", "索引", "query engine", "node parser"],
    "langgraph": ["langgraph", "state", "node", "edge", "循环", "分支"],
    "rag": ["rag", "检索", "向量", "rerank", "multi-query", "引用", "召回"],
    "multi-agent": ["multi-agent", "多 agent", "supervisor", "planner", "critic"],
}


# 根据问题类型生成多个改写版本。
def rewrite_queries(query: str) -> list[str]:
    # variants 里保存原问题和改写问题。
    variants = [query]
    # 统一小写版本，便于做英文判断。
    lower = query.lower()
    # “区别/对比”类问题，顺手加一个对比版本。
    if "区别" in query or "对比" in query:
        variants.append(query.replace("区别", "对比"))
    # 检索类问题，增加更泛化的检索词。
    if "rag" in lower or "检索" in query:
        variants.append("高级 RAG 检索 重排 引用")
    # Agent 相关问题，增加多 Agent 词汇。
    if "agent" in lower or "多智能体" in query:
        variants.append("多 Agent 监督者 协作")
    # LangGraph 问题，增加图结构关键词。
    if "langgraph" in lower:
        variants.append("LangGraph 状态图 节点 边")
    # 去重后返回。
    return list(dict.fromkeys(variants))


# 结合别名、token 和改写结果扩展检索词。
def expand_terms(query: str) -> list[str]:
    # terms 保存扩展后的检索词。
    terms = set()
    # 统一成小写便于英文匹配。
    lower = query.lower()
    # 先按别名表扩展。
    for aliases in ALIASES.values():
        for alias in aliases:
            if alias.lower() in lower or alias in query:
                terms.update(aliases)
    # 再把问题里切出来的 token 加进去。
    tokens = [tok for tok in re.split(r"[^\w\u4e00-\u9fff]+", query) if len(tok) >= 2]
    terms.update(tokens)
    # 再把改写后的 query 也加入。
    terms.update(rewrite_queries(query))
    # 过滤掉太短的 term。
    return [term for term in terms if len(term) >= 2]


# 对单个 chunk 做关键词打分。
def score_chunk(document: Document, terms: Iterable[str]) -> ChunkScore:
    # 把正文和 source 一起拿来做匹配。
    text = (document.page_content + " " + document.metadata.get("source", "")).lower()
    # matched 保存命中的 term。
    matched: list[str] = []
    # 初始分数从 0 开始。
    score = 0.0
    # 按 term 逐个打分。
    for term in terms:
        term_l = term.lower()
        if term_l in text:
            matched.append(term)
            score += 1.0
            score += min(text.count(term_l), 3) * 0.3
    # 标题式 Markdown 通常更像章节，总是稍微加分。
    if document.page_content.lstrip().startswith("#"):
        score += 0.5
    # 有 source 的文档更方便引用，也加一点分。
    if "source" in document.metadata:
        score += 0.2
    # 返回分数对象。
    return ChunkScore(document=document, score=score, matched_terms=matched)


# 先召回，再按分数取前 top_k 个 chunk。
def retrieve(chunks: list[Document], query: str, top_k: int) -> list[ChunkScore]:
    # 先扩展查询词。
    terms = expand_terms(query)
    # 给每个 chunk 打分。
    scored = [score_chunk(chunk, terms) for chunk in chunks]
    # 分数高的排前面。
    scored.sort(key=lambda item: item.score, reverse=True)
    # 只保留 top_k 个。
    return scored[:top_k]


# 基于内容特征对召回结果做二次重排。
def rerank(results: list[ChunkScore]) -> list[ChunkScore]:
    # rerank 阶段再根据内容做少量二次修正。
    reranked = []
    for item in results:
        # bonus 是额外奖励分。
        bonus = 0.0
        # 包含步骤/管线等词时，通常更像答案核心部分。
        content = item.document.page_content.lower()
        if "步骤" in item.document.page_content or "管线" in item.document.page_content:
            bonus += 0.4
        # 包含引用相关内容时，再加一点。
        if "引用" in item.document.page_content or "source" in content:
            bonus += 0.2
        # 生成新的 ChunkScore，避免直接修改原对象。
        reranked.append(ChunkScore(item.document, item.score + bonus, item.matched_terms))
    # 重新排序。
    reranked.sort(key=lambda item: item.score, reverse=True)
    # 返回重排后的结果。
    return reranked


# 把检索命中的 chunk 组织成可读答案。
def synthesize_answer(query: str, results: list[ChunkScore]) -> str:
    # 先写问题抬头。
    lines = [
        f"问题：{query}",
        "",
        "基于检索结果，我会这样回答：",
    ]
    # 把每个命中的 chunk 变成答案引用。
    for idx, item in enumerate(results, 1):
        source = item.document.metadata.get("source", "unknown")
        chunk_id = item.document.metadata.get("chunk_id", idx)
        excerpt = item.document.page_content.strip().splitlines()[0][:120]
        lines.append(f"{idx}. [{source}#{chunk_id}] {excerpt}")
    # 收尾说明。
    lines.append("")
    lines.append("简要结论：")
    lines.append(
        "高级 RAG 的关键不是单纯向量检索，而是把检索、重排、引用和生成做成稳定流水线。"
    )
    lines.append("如果查询偏向框架选型，可以优先看 LangChain / LlamaIndex / LangGraph 的职责边界。")
    # 把多行拼成一个答案。
    return "\n".join(lines)


# 程序入口，串起加载、切分、检索、重排和输出。
def main() -> None:
    # 解析参数。
    args = parse_args()
    # 加载原始文档。
    documents = load_documents()
    # 切成 chunk。
    chunks = chunk_documents(documents)
    # 初步检索。
    retrieved = retrieve(chunks, args.query, args.top_k)
    # 重排结果。
    reranked = rerank(retrieved)
    # 合成答案。
    answer = synthesize_answer(args.query, reranked)

    # 打印原始文档统计。
    print("=== 1. 原始文档 ===")
    for doc in documents:
        print(f"- {doc.metadata['source']}: {len(doc.page_content)} chars")

    # 打印 chunk 数量。
    print("\n=== 2. Chunk 数量 ===")
    print(len(chunks))

    # 打印检索 + 重排结果。
    print("\n=== 3. 检索 + Rerank 结果 ===")
    for item in reranked:
        print(
            f"- score={item.score:.2f} source={item.document.metadata.get('source')} "
            f"chunk={item.document.metadata.get('chunk_id')} matched={item.matched_terms}"
        )

    # 打印最终答案。
    print("\n=== 4. 最终回答 ===")
    print(answer)


if __name__ == "__main__":
    main()
