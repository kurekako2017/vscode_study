"""真实 Chroma 版骨架。

这个 demo 的重点是：

1. 让你看懂 Chroma 的 collection / metadata / query 结构
2. 给你一个本地持久化的真实向量库骨架
3. 在没有安装依赖时，也能用 mock 模式先看流程
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


ASSET_DIR = Path(__file__).parent / "assets"
DEFAULT_COLLECTION = "agent_advanced_chroma_demo"
DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
HASH_VECTOR_SIZE = 64


@dataclass
class Document:
    """最小文档对象，模拟 Chroma 里要入库的文本块。"""

    id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchHit:
    """检索返回的一条结果。"""

    id: str
    score: float
    text: str
    metadata: dict[str, Any]


@dataclass
class Embedder:
    """把文本变成向量的工具对象。"""

    name: str
    vector_size: int
    encode: Callable[[str], list[float]]


def tokenize(text: str) -> list[str]:
    # 保留中英文和数字，其余字符都视为分隔符。
    return [token for token in re.split(r"[^0-9A-Za-z\u4e00-\u9fff]+", text.lower()) if token]


def hash_embed(text: str, size: int = HASH_VECTOR_SIZE) -> list[float]:
    # 和教学版一致：把 token 映射到固定桶位，方便离线演示。
    vector = [0.0] * size
    for token in tokenize(text):
        bucket = sum(ord(ch) for ch in token) % size
        vector[bucket] += 1.0 + (len(token) / 10.0)
    norm = math.sqrt(sum(value * value for value in vector))
    return vector if norm == 0 else [value / norm for value in vector]


def build_embedder(kind: str) -> Embedder:
    # `auto` 会优先尝试真实模型，失败后再回退到 hash embedding。
    if kind in {"auto", "sentence-transformers"}:
        try:
            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer(DEFAULT_MODEL)
            vector_size = int(model.get_sentence_embedding_dimension())

            def encode(text: str) -> list[float]:
                # 真实模型通常会返回 numpy / tensor，这里统一转成普通 list。
                embedding = model.encode(text, normalize_embeddings=True)
                if hasattr(embedding, "tolist"):
                    embedding = embedding.tolist()
                return [float(value) for value in embedding]

            return Embedder(name="sentence-transformers", vector_size=vector_size, encode=encode)
        except Exception as exc:  # pragma: no cover
            if kind == "sentence-transformers":
                raise SystemExit(f"无法加载 sentence-transformers：{exc}") from exc
            # 没装依赖时，先用 hash 版本把流程跑通。
            print(f"[warn] sentence-transformers 不可用，回退到 hash embedding：{exc}", file=sys.stderr)

    return Embedder(name="hash", vector_size=HASH_VECTOR_SIZE, encode=lambda text: hash_embed(text, HASH_VECTOR_SIZE))


def load_documents(source_dir: Path = ASSET_DIR) -> list[Document]:
    # 约定：每个 markdown 文件都是一个示例文档。
    documents: list[Document] = []
    for file_path in sorted(source_dir.glob("*.md")):
        documents.append(
            Document(
                id=file_path.stem,
                text=file_path.read_text(encoding="utf-8"),
                metadata={
                    "source": file_path.name,
                    "topic": file_path.stem.replace("_", " "),
                },
            )
        )
    return documents


def print_hits(title: str, hits: list[SearchHit]) -> None:
    # 打印时把长文本截断，让初学者更容易看结果。
    print(f"\n=== {title} ===")
    for index, hit in enumerate(hits, start=1):
        print(f"{index}. id={hit.id} score={hit.score:.4f} source={hit.metadata.get('source')}")
        print(f"   topic={hit.metadata.get('topic')}")
        print(f"   snippet={hit.text[:160].replace(chr(10), ' ')}...")


class MockVectorStore:
    """不依赖 chromadb 的本地模拟实现。"""

    def __init__(self, collection_name: str, embedder: Embedder):
        self.collection_name = collection_name
        self.embedder = embedder
        self._items: list[dict[str, Any]] = []

    def upsert(self, documents: list[Document]) -> None:
        # 这里模拟 collection.upsert()：保存文档、元数据和向量。
        for doc in documents:
            self._items.append(
                {
                    "id": doc.id,
                    "text": doc.text,
                    "metadata": doc.metadata,
                    "vector": self.embedder.encode(doc.text),
                }
            )

    def query(self, query: str, top_k: int) -> list[SearchHit]:
        # 先把 query 转向量，再对每个文档算相似度。
        query_vector = self.embedder.encode(query)
        hits: list[SearchHit] = []
        for item in self._items:
            score = sum(a * b for a, b in zip(query_vector, item["vector"]))
            hits.append(SearchHit(id=item["id"], score=score, text=item["text"], metadata=item["metadata"]))
        hits.sort(key=lambda hit: hit.score, reverse=True)
        return hits[:top_k]


def run_mock(documents: list[Document], query: str, top_k: int, embedder: Embedder, collection_name: str) -> None:
    # mock 模式下不依赖外部服务，适合先看数据流。
    store = MockVectorStore(collection_name=collection_name, embedder=embedder)
    store.upsert(documents)
    print(f"mode = mock")
    print(f"backend = chroma-like")
    print(f"collection = {collection_name}")
    print(f"documents = {len(documents)}")
    print(f"embedding = {embedder.name} (dim={embedder.vector_size})")
    print(f"query = {query}")
    print_hits("search hits", store.query(query, top_k=top_k))


def build_chroma_client(persist_dir: str) -> Any:
    # 真实模式才会导入 chromadb，避免 mock 模式也强制安装依赖。
    try:
        import chromadb
    except ImportError as exc:  # pragma: no cover
        raise SystemExit("缺少 chromadb，请先安装 requirements.txt") from exc

    return chromadb.PersistentClient(path=persist_dir)


def recreate_collection(client: Any, collection_name: str) -> None:
    # 调试时如果 collection 旧了，可以先删掉再重建。
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass


def run_real(
    documents: list[Document],
    query: str,
    top_k: int,
    embedder: Embedder,
    collection_name: str,
    persist_dir: str,
    recreate: bool,
) -> None:
    client = build_chroma_client(persist_dir)
    if recreate:
        recreate_collection(client, collection_name)

    # 真实 Chroma 里先创建或获取 collection，再批量 upsert 文档。
    collection = client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
    ids = [doc.id for doc in documents]
    texts = [doc.text for doc in documents]
    metadatas = [doc.metadata for doc in documents]
    embeddings = [embedder.encode(doc.text) for doc in documents]
    collection.upsert(ids=ids, documents=texts, metadatas=metadatas, embeddings=embeddings)

    # query_embeddings 是“先把查询句子转成向量，再做检索”。
    result = collection.query(
        query_embeddings=[embedder.encode(query)],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    # 解析 Chroma 返回的结果，构建 SearchHit 列表。注意 Chroma 返回的是距离（distance），不是直接的相似度分数（score），这里简单转一下。
    hits: list[SearchHit] = []
    for idx, doc_id in enumerate(result["ids"][0]):
        # Chroma 返回的是距离，不是直接的相似度分数，这里简单转一下。
        distance = float(result["distances"][0][idx])
        text = result["documents"][0][idx]
        metadata = result["metadatas"][0][idx] or {}
        hits.append(
            SearchHit(
                id=str(doc_id),
                score=1.0 - distance,
                text=str(text),
                metadata=dict(metadata),
            )
        )

    print(f"mode = real")
    print(f"backend = chroma")
    print(f"persist_dir = {persist_dir}")
    print(f"collection = {collection_name}")
    print(f"documents = {len(documents)}")
    print(f"embedding = {embedder.name} (dim={embedder.vector_size})")
    print(f"query = {query}")
    print_hits("search hits", hits)

#   命令行参数解析，提供一些选项让你切换模式、指定 collection 名、选择 embedding 方法等。
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="真实 Chroma 版骨架")
    parser.add_argument("query", help="要检索的问题")
    parser.add_argument("--mode", choices=["mock", "real"], default="mock")
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--source-dir", default=str(ASSET_DIR))
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--embedding", choices=["auto", "hash", "sentence-transformers"], default="auto")
    parser.add_argument("--persist-dir", default="./chroma_data")
    parser.add_argument("--recreate", action="store_true", help="重建 collection，适合调试时清空旧数据")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_dir = Path(args.source_dir)
    # 加载示例文档，真实项目里你可能会从数据库、API 或文件系统加载。
    documents = load_documents(source_dir)
    if not documents:
        raise SystemExit(f"{source_dir} 中没有找到示例文档")
    # 构建 embedder，真实项目里你也可以接入其他向量化工具。
    embedder = build_embedder(args.embedding)
    # mock 和 real 共用同一套文档加载和 embedding，只是存储层不同。
    if args.mode == "mock":
        run_mock(documents, args.query, args.top_k, embedder, args.collection)
    else:
        run_real(
            documents=documents,
            query=args.query,
            top_k=args.top_k,
            embedder=embedder,
            collection_name=args.collection,
            persist_dir=args.persist_dir,
            recreate=args.recreate,
        )

    print("\n=== how to read this demo ===")
    print("1. embedder 负责把文本变成向量")
    print("2. documents 先写入 collection")
    print("3. query 会返回 top-k 命中")
    print("4. real 模式对应真实 Chroma Client，mock 模式方便先看流程")


if __name__ == "__main__":
    main()
