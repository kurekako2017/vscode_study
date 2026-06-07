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
# 资源目录。
ASSETS_DIR = BASE_DIR / "assets"
# 配置目录。
CATALOG_PATH = ASSETS_DIR / "catalog.json"
# 支持的角色列表。
VALID_ROLES = ("employee", "manager", "it_admin")

# 文件服务器类资料的提示词。
SERVER_HINTS = ("制度", "流程", "申请", "审批", "报销", "休假", "服务器", "文件")
# Wiki 类资料的提示词。
WIKI_HINTS = ("wiki", "FAQ", "faq", "操作", "发布", "部署", "排障", "指南", "页面")
# 针对常见问题的短语扩展。
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
    # 文档唯一 ID。
    doc_id: str
    # 文档标题。
    title: str
    # 来源类型：server 或 wiki。
    source_type: str
    # 文档路径。
    path: Path
    # 访问控制列表。
    acl: tuple[str, ...]
    # 引用用的 URL。
    url: str
    # 文档正文。
    content: str

    @property
    def label(self) -> str:
        # 用于打印的标签。
        return f"{self.source_type}:{self.path.name}"


@dataclass
class RankedDoc:
    # 被打分的文档。
    document: KnowledgeDoc
    # 检索分数。
    score: float
    # 命中的词。
    matched_terms: list[str] = field(default_factory=list)
    # 打分原因。
    reason: str = ""


def parse_args() -> argparse.Namespace:
    # 创建命令行解析器。
    parser = argparse.ArgumentParser(description="社内文件 + Wiki 混合检索 RAG demo")
    # 用户输入的问题。
    parser.add_argument(
        "query",
        nargs="?",
        default="远程办公和发布流程有什么要求？",
        help="要检索的问题",
    )
    # 当前用户角色。
    parser.add_argument(
        "--role",
        default="employee",
        choices=VALID_ROLES,
        help="当前用户角色，用于权限过滤",
    )
    # 返回前几个结果。
    parser.add_argument("--top-k", type=int, default=4, help="返回前几个结果")
    # 返回解析结果。
    return parser.parse_args()


def load_catalog() -> list[dict]:
    # 先确认目录配置文件存在。
    if not CATALOG_PATH.exists():
        raise FileNotFoundError(f"Missing catalog file: {CATALOG_PATH}")
    # 读取 catalog.json。
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def load_documents() -> list[KnowledgeDoc]:
    # 最终文档列表。
    docs: list[KnowledgeDoc] = []
    # 逐条读取 catalog。
    for item in load_catalog():
        # 找到具体文档文件。
        path = ASSETS_DIR / item["path"]
        # 读出正文。
        content = path.read_text(encoding="utf-8")
        # acl 为空时，默认 employee 可见。
        acl = tuple(item.get("acl", ("employee",)))
        # 组装成 KnowledgeDoc。
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
    # 返回所有文档。
    return docs


def can_access(document: KnowledgeDoc, role: str) -> bool:
    # all 表示所有角色可见。
    return "all" in document.acl or role in document.acl


def filter_by_role(documents: list[KnowledgeDoc], role: str) -> tuple[list[KnowledgeDoc], list[KnowledgeDoc]]:
    # 可访问文档。
    accessible: list[KnowledgeDoc] = []
    # 被过滤掉的文档。
    filtered: list[KnowledgeDoc] = []
    # 逐个检查访问权限。
    for document in documents:
        if can_access(document, role):
            accessible.append(document)
        else:
            filtered.append(document)
    # 同时返回可访问和被过滤的列表。
    return accessible, filtered


def tokenize(text: str) -> list[str]:
    # 提取中英文 token。
    tokens = re.findall(r"[A-Za-z0-9_+-]{2,}|[\u4e00-\u9fff]{2,}", text.lower())
    # 有序去重。
    ordered: list[str] = []
    for token in tokens:
        if token not in ordered:
            ordered.append(token)
    # 返回 token 列表。
    return ordered


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    # 统一大小写后匹配。
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def expand_query_terms(query: str) -> list[str]:
    # 先把 query 切成词。
    terms = tokenize(query)
    # 如果像文件服务器类问题，就扩展相关词。
    if contains_any(query, SERVER_HINTS):
        terms.extend(["server", "文件服务器", "制度", "流程"])
    # 如果像 Wiki 类问题，就扩展相关词。
    if contains_any(query, WIKI_HINTS):
        terms.extend(["wiki", "faq", "操作", "发布"])
    # 针对固定短语再额外加词。
    for phrase, keywords in PHRASE_HINTS.items():
        if phrase in query:
            terms.extend(keywords)
    # 去重返回。
    return list(dict.fromkeys(terms))


def score_document(document: KnowledgeDoc, query: str, terms: Iterable[str]) -> RankedDoc:
    # 把标题、正文、路径、来源类型拼成一个大文本方便匹配。
    haystack = f"{document.title}\n{document.content}\n{document.path.as_posix()}\n{document.source_type}".lower()
    # query 小写版。
    query_lower = query.lower()
    # 记录命中的词。
    matched_terms: list[str] = []
    # 初始分。
    score = 0.0

    # 逐个 term 匹配。
    for term in terms:
        term_lower = term.lower()
        if term_lower in haystack:
            matched_terms.append(term)
            score += 1.0
            score += min(haystack.count(term_lower), 3) * 0.2

    # 标题直接命中时额外加分。
    if document.title.lower() in query_lower:
        score += 1.5

    # 文件服务器资料和服务器类问题更匹配。
    if document.source_type == "server" and contains_any(query, SERVER_HINTS):
        score += 0.8
    # Wiki 资料和 Wiki 类问题更匹配。
    if document.source_type == "wiki" and contains_any(query, WIKI_HINTS):
        score += 0.8

    # 针对制度类关键词给 server 额外加分。
    if document.source_type == "server" and any(term in query for term in ("制度", "审批", "报销", "休假")):
        score += 0.5
    # 针对操作类关键词给 wiki 额外加分。
    if document.source_type == "wiki" and any(term in query for term in ("操作", "部署", "发布", "FAQ", "排障")):
        score += 0.5

    # query 里直接提到 wiki，就稍微偏向 wiki 文档。
    if document.source_type == "wiki" and "wiki" in query_lower:
        score += 0.3
    # query 里直接提到文件/服务器，就稍微偏向 server 文档。
    if document.source_type == "server" and ("文件" in query or "服务器" in query):
        score += 0.3

    # 没命中时，reason 只保留类型提示。
    reason = "title/content match" if matched_terms else "type hint only"
    # 返回打分结果。
    return RankedDoc(document=document, score=score, matched_terms=matched_terms, reason=reason)


def retrieve(query: str, documents: list[KnowledgeDoc], top_k: int) -> list[RankedDoc]:
    # 扩展检索词。
    terms = expand_query_terms(query)
    # 逐篇文档打分。
    ranked = [score_document(document, query, terms) for document in documents]
    # 只保留有分数的文档。
    ranked = [item for item in ranked if item.score > 0]
    # 先按分数，再按标题稳定排序。
    ranked.sort(key=lambda item: (-item.score, item.document.title))
    # 返回前 top_k 个。
    return ranked[:top_k]


def rerank(query: str, ranked: list[RankedDoc]) -> list[RankedDoc]:
    # 对初步检索结果做二次修正。
    reranked: list[RankedDoc] = []
    for item in ranked:
        # 额外奖励分。
        bonus = 0.0
        if item.document.source_type == "server" and contains_any(query, SERVER_HINTS):
            bonus += 0.2
        if item.document.source_type == "wiki" and contains_any(query, WIKI_HINTS):
            bonus += 0.2
        if len(item.matched_terms) >= 3:
            bonus += 0.2
        # 创建新的 RankedDoc，避免原对象被改掉。
        reranked.append(
            RankedDoc(
                document=item.document,
                score=item.score + bonus,
                matched_terms=item.matched_terms,
                reason=item.reason,
            )
        )
    # 重新排序。
    reranked.sort(key=lambda item: (-item.score, item.document.title))
    # 返回重排后结果。
    return reranked


def excerpt_lines(text: str, limit: int = 2) -> list[str]:
    # 保存截取出来的行。
    lines = []
    # 一行一行读取。
    for line in text.splitlines():
        # 去掉列表符号和空白。
        cleaned = line.strip().lstrip("-*•").strip()
        if cleaned:
            lines.append(cleaned)
        if len(lines) >= limit:
            break
    # 返回摘要行。
    return lines


def synthesize_answer(query: str, role: str, accessible_docs: list[KnowledgeDoc], filtered_docs: list[KnowledgeDoc], results: list[RankedDoc]) -> str:
    # 答案主体的第一行。
    lines = [f"问题：{query}", f"当前角色：{role}", ""]
    lines.append("建议答案：")
    # 如果没有结果，就提示扩大范围。
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

    # 引用列表单独列出来。
    lines.append("")
    lines.append("引用列表：")
    for item in results:
        doc = item.document
        lines.append(f"- {doc.title} | {doc.label} | {doc.url}")

    # 再补一个权限与来源概况。
    lines.append("")
    lines.append("权限与来源概况：")
    server_count = sum(1 for doc in accessible_docs if doc.source_type == "server")
    wiki_count = sum(1 for doc in accessible_docs if doc.source_type == "wiki")
    lines.append(f"- 可访问资料：{len(accessible_docs)} 篇（server={server_count}, wiki={wiki_count})")
    if filtered_docs:
        lines.append(f"- 被权限过滤：{len(filtered_docs)} 篇")
        for doc in filtered_docs:
            lines.append(f"  - {doc.title} [{doc.label}] acl={','.join(doc.acl)}")

    # 拼成最终答案文本。
    return "\n".join(lines)


def print_section(title: str) -> None:
    # 分隔输出，方便阅读。
    print(f"\n=== {title} ===")


def main() -> None:
    # 解析参数。
    args = parse_args()
    # 加载所有文档。
    documents = load_documents()
    # 权限过滤。
    accessible_docs, filtered_docs = filter_by_role(documents, args.role)
    # 先检索。
    retrieved = retrieve(args.query, accessible_docs, args.top_k)
    # 再重排。
    reranked = rerank(args.query, retrieved)
    # 生成最终答案。
    answer = synthesize_answer(args.query, args.role, accessible_docs, filtered_docs, reranked)

    # 打印接入层统计。
    print_section("1. 接入层")
    print(f"载入资料总数：{len(documents)}")
    print(f"可访问资料数：{len(accessible_docs)}")
    print(f"权限过滤数：{len(filtered_docs)}")
    print("来源分布：")
    source_counter = Counter(doc.source_type for doc in documents)
    for source_type, count in sorted(source_counter.items()):
        print(f"- {source_type}: {count}")

    # 打印权限层。
    print_section("2. 权限层")
    if filtered_docs:
        for doc in filtered_docs:
            print(f"- 已过滤：{doc.title} [{doc.label}] acl={','.join(doc.acl)}")
    else:
        print("- 当前角色可以访问全部资料。")

    # 打印检索层。
    print_section("3. 检索层")
    for item in reranked:
        print(
            f"- score={item.score:.2f} source={item.document.label} matched={item.matched_terms}"
        )

    # 打印引用层。
    print_section("4. 引用层")
    print(answer)


if __name__ == "__main__":
    main()
