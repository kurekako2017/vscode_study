"""向量数据库最小教学版。

这个 demo 用纯 Python 模拟三种常见向量库风格：

- Qdrant 风格：collection + payload + similarity search
- Chroma 风格：collection + metadata + similarity search
- Memory 风格：内存实现，方便先理解数据流

核心目标不是追求性能，而是让初学者看懂：

1. 文本如何向量化
2. 向量如何写入 collection
3. 查询时如何做相似度检索
4. 不同“向量数据库风格”在接口组织上有什么差别
"""

from __future__ import annotations

import argparse
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# 示例文档目录，程序会把这里的 `.md` 文件读进来做检索演示。
ASSET_DIR = Path(__file__).parent / "assets"
# 向量长度固定，方便教学时理解“文本 -> 向量 -> 相似度”的完整流程。
VECTOR_SIZE = 32


@dataclass
class Document:
    """最小文档对象。

    text:  文本内容
    metadata: 额外元数据，例如来源、标签、分类等
    """

    id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchHit:
    """检索命中结果。"""

    id: str
    score: float
    text: str
    metadata: dict[str, Any]


def tokenize(text: str) -> list[str]:
    """把中文/英文文本切成最简单的 token。

    这里故意不引入第三方分词库，只做教学演示。
    """

    # 用正则把标点、空白和其他分隔符去掉，保留中英文和数字。
    return [token for token in re.split(r"[^0-9A-Za-z\u4e00-\u9fff]+", text.lower()) if token]


def embed_text(text: str, size: int = VECTOR_SIZE) -> list[float]:
    """把文本转成一个固定长度向量。

    这不是生产级 embedding，只是一个便于离线演示的 hash 向量。
    """

    vector = [0.0] * size
    tokens = tokenize(text)
    if not tokens:
        return vector

    for token in tokens:
        # 把每个 token 映射到一个固定桶位，多个词会累积到同一个位置。
        bucket = sum(ord(ch) for ch in token) % size
        # 词越长，权重略高一点，让向量更容易体现文本差异。
        weight = 1.0 + (len(token) / 10.0)
        vector[bucket] += weight

    # 归一化后再做相似度计算，结果会更稳定。
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]


def cosine_similarity(lhs: list[float], rhs: list[float]) -> float:
    """余弦相似度。"""

    return sum(a * b for a, b in zip(lhs, rhs))


def load_documents() -> list[Document]:
    """加载 assets 里的示例文档。"""

    docs: list[Document] = []
    for file_path in sorted(ASSET_DIR.glob("*.md")):
        # 每个 markdown 文件都当成一篇小文档，便于演示文档入库。
        docs.append(
            Document(
                id=file_path.stem,
                text=file_path.read_text(encoding="utf-8"),
                metadata={
                    "source": file_path.name,
                    "topic": file_path.stem.replace("_", " "),
                },
            )
        )
    return docs


class MemoryVectorDB:
    """内存版向量库。

    下面两个“风格类”都会复用它，只是接口展示方式不同。
    """

    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self._items: list[dict[str, Any]] = []

    def upsert(self, documents: list[Document]) -> None:
        # 这里模拟“写入 collection”的动作：保存原文、元数据和向量。
        for doc in documents:
            self._items.append(
                {
                    "id": doc.id,
                    "text": doc.text,
                    "metadata": doc.metadata,
                    "vector": embed_text(doc.text),
                }
            )

    def search(self, query: str, top_k: int = 3) -> list[SearchHit]:
        # 查询同样先转向量，再和库里的每个文档逐个算相似度。
        query_vector = embed_text(query)
        hits: list[SearchHit] = []
        for item in self._items:
            score = cosine_similarity(query_vector, item["vector"])
            hits.append(
                SearchHit(
                    id=item["id"],
                    score=score,
                    text=item["text"],
                    metadata=item["metadata"],
                )
            )
        hits.sort(key=lambda item: item.score, reverse=True)
        return hits[:top_k]


class QdrantLikeStore:
    """Qdrant 风格：collection + payload + similarity search。"""

    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self._db = MemoryVectorDB(collection_name)

    def upsert(self, documents: list[Document]) -> None:
        # 教学版不连真实服务，只复用内存实现来表现接口风格。
        self._db.upsert(documents)

    def search(self, query: str, top_k: int = 3) -> list[SearchHit]:
        return self._db.search(query, top_k=top_k)


class ChromaLikeStore:
    """Chroma 风格：collection + metadata + similarity search。"""

    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self._db = MemoryVectorDB(collection_name)

    def add_documents(self, documents: list[Document]) -> None:
        # Chroma 常用的是 `add_documents()` 这样的命名，所以这里保留这个接口。
        self._db.upsert(documents)

    def query(self, query: str, n_results: int = 3) -> list[SearchHit]:
        return self._db.search(query, top_k=n_results)


def print_hits(title: str, hits: list[SearchHit]) -> None:
    """把命中结果打印得更适合学习。"""

    print(f"\n=== {title} ===")
    for index, hit in enumerate(hits, start=1):
        print(f"{index}. id={hit.id}  score={hit.score:.4f}  source={hit.metadata.get('source')}")
        print(f"   topic={hit.metadata.get('topic')}")
        snippet = hit.text[:180].replace("\n", " ")
        print(f"   snippet={snippet}...")


def build_store(backend: str) -> Any:
    """根据参数创建不同风格的向量库。"""

    if backend == "qdrant":
        # 这里强调的是“Qdrant 风格”的 API 形状，而不是实际连接服务。
        return QdrantLikeStore(collection_name="knowledge_chunks")
    if backend == "chroma":
        # 这里强调的是“Chroma 风格”的 API 形状。
        return ChromaLikeStore(collection_name="knowledge_chunks")
    if backend == "memory":
        # 最朴素的内存实现，最适合先理解数据流。
        return MemoryVectorDB(collection_name="knowledge_chunks")
    raise ValueError(f"Unsupported backend: {backend}")


def main() -> None:
    parser = argparse.ArgumentParser(description="向量数据库最小教学版 demo")
    parser.add_argument("query", help="要检索的问题")
    parser.add_argument("--backend", choices=["qdrant", "chroma", "memory"], default="qdrant")
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    documents = load_documents()
    if not documents:
        raise SystemExit("assets/ 里没有找到示例文档，请先确认 assets/*.md 是否存在。")

    store = build_store(args.backend)
    print(f"backend = {args.backend}")
    print(f"collection = {store.collection_name}")
    print(f"documents = {len(documents)}")

    # 不同后端只是“写入和查询的方法名”不同，底层数据流是一致的。
    if isinstance(store, QdrantLikeStore):
        store.upsert(documents)
        hits = store.search(args.query, top_k=args.top_k)
    elif isinstance(store, ChromaLikeStore):
        store.add_documents(documents)
        hits = store.query(args.query, n_results=args.top_k)
    else:
        store.upsert(documents)
        hits = store.search(args.query, top_k=args.top_k)

    print(f"query = {args.query}")
    print_hits("search hits", hits)

    print("\n=== how to read this demo ===")
    print("1. 文本先被 embed_text() 转成向量")
    print("2. upsert()/add_documents() 把文档写入 collection")
    print("3. search()/query() 按余弦相似度返回 top-k")
    print("4. Qdrant/Chroma 的区别主要在接口和数据模型命名")


if __name__ == "__main__":
    main()
