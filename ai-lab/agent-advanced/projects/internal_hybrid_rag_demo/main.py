"""社内文件 + Wiki 混合检索 RAG demo。

这个 demo 用本地文件模拟两类资料来源：
- server_docs: 文件服务器/共享目录上的资料
- wiki_docs: 社内 Wiki 上的资料

重点演示四层：
1. 接入层：统一加载不同来源的文档
2. 检索层：对可访问文档进行关键词检索和 rerank
3. 权限层：按角色过滤不可见文档
4. 引用层：输出带来源的答案
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
CATALOG_PATH = ASSETS_DIR / "catalog.json"
VALID_ROLES = ("employee", "manager", "it_admin")

SERVER_HINTS = ("制度", "流程", "申请", "审批", "报销", "休假", "服务器", "文件")
WIKI_HINTS = ("wiki", "FAQ", "faq", "操作", "发布", "部署", "排障", "指南", "页面")
PHRASE_HINTS = {
    "远程办公": ["远程办公", "休假", "审批"],
    "发布流程": ["发布", "部署", "FAQ", "操作"],
    "发布": ["发布", "部署", "FAQ"],
    "访问控制": ["访问控制", "权限矩阵", "acl", "权限"],
    "权限": ["权限", "acl", "访问控制"],
    "事故": ["事故", "响应", "升级"],
}


@dataclass(frozen=True)
class KnowledgeDoc:
    doc_id: str
    title: str
    source_type: str
    path: Path
    acl: tuple[str, ...]
    url: str
    content: str

    @property
    def label(self) -> str:
        return f"{self.source_type}:{self.path.name}"


@dataclass
class RankedDoc:
    document: KnowledgeDoc
    score: float
    matched_terms: list[str] = field(default_factory=list)
    reason: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="社内文件 + Wiki 混合检索 RAG demo")
    parser.add_argument(
        "query",
        nargs="?",
        default="远程办公和发布流程有什么要求？",
        help="要检索的问题",
    )
    parser.add_argument(
        "--role",
        default="employee",
        choices=VALID_ROLES,
        help="当前用户角色，用于权限过滤",
    )
    parser.add_argument("--top-k", type=int, default=4, help="返回前几个结果")
    return parser.parse_args()


def load_catalog() -> list[dict]:
    if not CATALOG_PATH.exists():
        raise FileNotFoundError(f"Missing catalog file: {CATALOG_PATH}")
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def load_documents() -> list[KnowledgeDoc]:
    docs: list[KnowledgeDoc] = []
    for item in load_catalog():
        path = ASSETS_DIR / item["path"]
        content = path.read_text(encoding="utf-8")
        acl = tuple(item.get("acl", ("employee",)))
        docs.append(
            KnowledgeDoc(
                doc_id=item["doc_id"],
                title=item["title"],
                source_type=item["source_type"],
                path=path,
                acl=acl,
                url=item.get("url", f"file://{path.name}"),
                content=content,
            )
        )
    return docs


def can_access(document: KnowledgeDoc, role: str) -> bool:
    return "all" in document.acl or role in document.acl


def filter_by_role(documents: list[KnowledgeDoc], role: str) -> tuple[list[KnowledgeDoc], list[KnowledgeDoc]]:
    accessible: list[KnowledgeDoc] = []
    filtered: list[KnowledgeDoc] = []
    for document in documents:
        if can_access(document, role):
            accessible.append(document)
        else:
            filtered.append(document)
    return accessible, filtered


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[A-Za-z0-9_+-]{2,}|[\u4e00-\u9fff]{2,}", text.lower())
    ordered: list[str] = []
    for token in tokens:
        if token not in ordered:
            ordered.append(token)
    return ordered


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def expand_query_terms(query: str) -> list[str]:
    terms = tokenize(query)
    if contains_any(query, SERVER_HINTS):
        terms.extend(["server", "文件服务器", "制度", "流程"])
    if contains_any(query, WIKI_HINTS):
        terms.extend(["wiki", "faq", "操作", "发布"])
    for phrase, keywords in PHRASE_HINTS.items():
        if phrase in query:
            terms.extend(keywords)
    return list(dict.fromkeys(terms))


def score_document(document: KnowledgeDoc, query: str, terms: Iterable[str]) -> RankedDoc:
    haystack = f"{document.title}\n{document.content}\n{document.path.as_posix()}\n{document.source_type}".lower()
    query_lower = query.lower()
    matched_terms: list[str] = []
    score = 0.0

    for term in terms:
        term_lower = term.lower()
        if term_lower in haystack:
            matched_terms.append(term)
            score += 1.0
            score += min(haystack.count(term_lower), 3) * 0.2

    if document.title.lower() in query_lower:
        score += 1.5

    if document.source_type == "server" and contains_any(query, SERVER_HINTS):
        score += 0.8
    if document.source_type == "wiki" and contains_any(query, WIKI_HINTS):
        score += 0.8

    if document.source_type == "server" and any(term in query for term in ("制度", "审批", "报销", "休假")):
        score += 0.5
    if document.source_type == "wiki" and any(term in query for term in ("操作", "部署", "发布", "FAQ", "排障")):
        score += 0.5

    if document.source_type == "wiki" and "wiki" in query_lower:
        score += 0.3
    if document.source_type == "server" and ("文件" in query or "服务器" in query):
        score += 0.3

    reason = "title/content match" if matched_terms else "type hint only"
    return RankedDoc(document=document, score=score, matched_terms=matched_terms, reason=reason)


def retrieve(query: str, documents: list[KnowledgeDoc], top_k: int) -> list[RankedDoc]:
    terms = expand_query_terms(query)
    ranked = [score_document(document, query, terms) for document in documents]
    ranked = [item for item in ranked if item.score > 0]
    ranked.sort(key=lambda item: (-item.score, item.document.title))
    return ranked[:top_k]


def rerank(query: str, ranked: list[RankedDoc]) -> list[RankedDoc]:
    reranked: list[RankedDoc] = []
    for item in ranked:
        bonus = 0.0
        if item.document.source_type == "server" and contains_any(query, SERVER_HINTS):
            bonus += 0.2
        if item.document.source_type == "wiki" and contains_any(query, WIKI_HINTS):
            bonus += 0.2
        if len(item.matched_terms) >= 3:
            bonus += 0.2
        reranked.append(
            RankedDoc(
                document=item.document,
                score=item.score + bonus,
                matched_terms=item.matched_terms,
                reason=item.reason,
            )
        )
    reranked.sort(key=lambda item: (-item.score, item.document.title))
    return reranked


def excerpt_lines(text: str, limit: int = 2) -> list[str]:
    lines = []
    for line in text.splitlines():
        cleaned = line.strip().lstrip("-*•").strip()
        if cleaned:
            lines.append(cleaned)
        if len(lines) >= limit:
            break
    return lines


def synthesize_answer(query: str, role: str, accessible_docs: list[KnowledgeDoc], filtered_docs: list[KnowledgeDoc], results: list[RankedDoc]) -> str:
    lines = [f"问题：{query}", f"当前角色：{role}", ""]
    lines.append("建议答案：")
    if not results:
        lines.append("当前可访问资料里没有找到足够相关的内容，建议先扩大检索范围或补充资料。")
    else:
        lines.append("这类问题应该把服务器上的制度类资料和 Wiki 上的操作类资料一起看，但先做权限过滤，再做检索和引用。")
        for item in results:
            doc = item.document
            excerpt = " / ".join(excerpt_lines(doc.content))
            lines.append(
                f"- {doc.title} [{doc.label}]：{excerpt}（score={item.score:.2f}）"
            )

    lines.append("")
    lines.append("引用列表：")
    for item in results:
        doc = item.document
        lines.append(f"- {doc.title} | {doc.label} | {doc.url}")

    lines.append("")
    lines.append("权限与来源概况：")
    server_count = sum(1 for doc in accessible_docs if doc.source_type == "server")
    wiki_count = sum(1 for doc in accessible_docs if doc.source_type == "wiki")
    lines.append(f"- 可访问资料：{len(accessible_docs)} 篇（server={server_count}, wiki={wiki_count})")
    if filtered_docs:
        lines.append(f"- 被权限过滤：{len(filtered_docs)} 篇")
        for doc in filtered_docs:
            lines.append(f"  - {doc.title} [{doc.label}] acl={','.join(doc.acl)}")

    return "\n".join(lines)


def print_section(title: str) -> None:
    print(f"\n=== {title} ===")


def main() -> None:
    args = parse_args()
    documents = load_documents()
    accessible_docs, filtered_docs = filter_by_role(documents, args.role)
    retrieved = retrieve(args.query, accessible_docs, args.top_k)
    reranked = rerank(args.query, retrieved)
    answer = synthesize_answer(args.query, args.role, accessible_docs, filtered_docs, reranked)

    print_section("1. 接入层")
    print(f"载入资料总数：{len(documents)}")
    print(f"可访问资料数：{len(accessible_docs)}")
    print(f"权限过滤数：{len(filtered_docs)}")
    print("来源分布：")
    source_counter = Counter(doc.source_type for doc in documents)
    for source_type, count in sorted(source_counter.items()):
        print(f"- {source_type}: {count}")

    print_section("2. 权限层")
    if filtered_docs:
        for doc in filtered_docs:
            print(f"- 已过滤：{doc.title} [{doc.label}] acl={','.join(doc.acl)}")
    else:
        print("- 当前角色可以访问全部资料。")

    print_section("3. 检索层")
    for item in reranked:
        print(
            f"- score={item.score:.2f} source={item.document.label} matched={item.matched_terms}"
        )

    print_section("4. 引用层")
    print(answer)


if __name__ == "__main__":
    main()
