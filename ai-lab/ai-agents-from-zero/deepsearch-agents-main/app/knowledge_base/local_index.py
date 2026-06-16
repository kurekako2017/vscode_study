"""
Local knowledge base indexing and retrieval helpers.

This module builds a lightweight in-repo retrieval index over the documents in
``docs/knowledge_base`` so the project can run without an external RAGFlow
service. It uses a simple hashed token vector representation and cosine
similarity, which is enough for small teaching corpora and keeps the runtime
dependency-free.
"""

# 这个模块实现的是“项目内自带的轻量知识库检索”。
# 初学者可以把它看成一个很小的本地 RAG：
# 1. 先从 docs/knowledge_base/ 读取文档
# 2. 再把文档切成 token 统计表示
# 3. 查询时按相似度排序，返回最相关的几段内容

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from math import sqrt
from pathlib import Path
import re
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
KB_ROOT = ROOT / "docs" / "knowledge_base"
SUPPORTED_EXTENSIONS = {".md", ".txt", ".pdf", ".docx"}


@dataclass(frozen=True)
class KnowledgeDoc:
    # 一个 KnowledgeDoc 就代表知识库中的一篇文档及其检索特征。
    path: Path
    relative_path: str
    title: str
    content: str
    tokens: Counter[str]

    @property
    def norm(self) -> float:
        return sqrt(sum(weight * weight for weight in self.tokens.values()))


def _iter_documents(root: Path) -> Iterable[Path]:
    # 递归扫描知识库目录，只保留当前项目支持的文件类型。
    if not root.exists():
        return []
    return sorted(
        path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def _read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _read_pdf_file(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        return ""

    try:
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        return ""


def _read_docx_file(path: Path) -> str:
    try:
        import docx
    except ImportError:
        return ""

    try:
        document = docx.Document(str(path))
        return "\n".join(paragraph.text for paragraph in document.paragraphs)
    except Exception:
        return ""


def _extract_text(path: Path) -> str:
    # 根据不同后缀选择不同读取方式。
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return _read_text_file(path)
    if suffix == ".pdf":
        return _read_pdf_file(path)
    if suffix == ".docx":
        return _read_docx_file(path)
    return ""


def _tokenize(text: str) -> Counter[str]:
    # 这里没有引入复杂 embedding，而是做了一个轻量 token 方案：
    # - 英文按单词切
    # - 中文按 2 字滑窗切
    # 对教学项目来说，这样已经足够演示“检索 -> 排序 -> 返回片段”的流程。
    normalized = text.lower()
    word_tokens = re.findall(r"[a-z0-9]+", normalized)
    cjk_chunks = re.findall(r"[\u4e00-\u9fff]{2,}", text)
    cjk_tokens: list[str] = []
    for chunk in cjk_chunks:
        if len(chunk) <= 2:
            cjk_tokens.append(chunk)
            continue
        cjk_tokens.extend(chunk[i : i + 2] for i in range(len(chunk) - 1))
    return Counter(word_tokens + cjk_tokens)


def _build_title(path: Path, content: str) -> str:
    # 优先使用文件名作为标题；如果没有，就退化到正文第一行。
    if path.stem:
        return path.stem
    for line in content.splitlines():
        line = line.strip().lstrip("#").strip()
        if line:
            return line[:80]
    return path.name


@lru_cache(maxsize=1)
def load_knowledge_docs() -> tuple[KnowledgeDoc, ...]:
    # lru_cache 让知识库索引只构建一次，避免每次查询都重复扫描整目录。
    docs: list[KnowledgeDoc] = []
    for path in _iter_documents(KB_ROOT):
        content = _extract_text(path).strip()
        if not content:
            continue
        docs.append(
            KnowledgeDoc(
                path=path,
                relative_path=str(path.relative_to(ROOT)).replace("\\", "/"),
                title=_build_title(path, content),
                content=content,
                tokens=_tokenize(content),
            )
        )
    return tuple(docs)


def clear_knowledge_cache() -> None:
    # 如果知识库目录里的文档更新了，可以清缓存后重新加载。
    load_knowledge_docs.cache_clear()


def cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0

    intersection = set(left) & set(right)
    numerator = sum(left[token] * right[token] for token in intersection)
    left_norm = sqrt(sum(weight * weight for weight in left.values()))
    right_norm = sqrt(sum(weight * weight for weight in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)


def search_knowledge_base(query: str, top_k: int = 3) -> list[dict[str, object]]:
    # 对外暴露的核心查询入口：
    # 输入一个问题，返回若干条最相关文档片段。
    docs = load_knowledge_docs()
    if not docs:
        return []

    query_tokens = _tokenize(query)
    scored: list[tuple[float, KnowledgeDoc]] = []
    for doc in docs:
        score = cosine_similarity(query_tokens, doc.tokens)
        if score <= 0:
            continue
        scored.append((score, doc))

    scored.sort(key=lambda item: item[0], reverse=True)
    results: list[dict[str, object]] = []
    for score, doc in scored[:top_k]:
        highlight = _build_snippet(doc.content, query_tokens)
        results.append(
            {
                "title": doc.title,
                "path": doc.relative_path,
                "score": round(score, 4),
                "snippet": highlight,
            }
        )
    return results


def _build_snippet(content: str, query_tokens: Counter[str], max_length: int = 260) -> str:
    # 返回给模型或前端时，不需要整篇文档，只给一个局部摘录更高效。
    if not content:
        return ""

    search_terms = [token for token, _ in query_tokens.most_common(8) if len(token) >= 2]
    lower_content = content.lower()
    for term in search_terms:
        position = lower_content.find(term)
        if position >= 0:
            start = max(0, position - 80)
            end = min(len(content), position + max_length)
            return content[start:end].replace("\n", " ").strip()

    return content[:max_length].replace("\n", " ").strip()


def has_local_knowledge_base() -> bool:
    # 这是健康检查和工具层判断“当前有没有知识库可用”的最简单入口。
    return len(load_knowledge_docs()) > 0
