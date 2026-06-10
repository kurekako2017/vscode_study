"""真实 Qdrant 版骨架。

这个 demo 有两个目标：

1. 让你先看懂真实 Qdrant Client 的接入结构
2. 让你在没有服务时也能用 mock 模式先看流程

默认使用 hash embedding，保证离线也能跑；
如果你安装了 sentence-transformers，也可以换成真实 embedding。
"""

from __future__ import annotations

import argparse
import math
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


ASSET_DIR = Path(__file__).parent / "assets"
DEFAULT_COLLECTION = "agent_advanced_qdrant_demo"
DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
HASH_VECTOR_SIZE = 64


@dataclass
class Document:
    id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchHit:
    id: str
    score: float
    text: str
    metadata: dict[str, Any]


@dataclass
class Embedder:
    name: str
    vector_size: int
    encode: Callable[[str], list[float]]


def tokenize(text: str) -> list[str]:
    return [token for token in re.split(r"[^0-9A-Za-z\u4e00-\u9fff]+", text.lower()) if token]


def hash_embed(text: str, size: int = HASH_VECTOR_SIZE) -> list[float]:
    vector = [0.0] * size
    for token in tokenize(text):
        bucket = sum(ord(ch) for ch in token) % size
        vector[bucket] += 1.0 + (len(token) / 10.0)
    norm = math.sqrt(sum(value * value for value in vector))
    return vector if norm == 0 else [value / norm for value in vector]


def build_embedder(kind: str) -> Embedder:
    """构造 embedding 方案。

    默认是 hash 版，保证你没有下载模型时也能跑。
    如果传 `--embedding sentence-transformers`，就会尝试真实模型。
    """

    if kind in {"auto", "sentence-transformers"}:
        try:
            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer(DEFAULT_MODEL)
            vector_size = int(model.get_sentence_embedding_dimension())

            def encode(text: str) -> list[float]:
                embedding = model.encode(text, normalize_embeddings=True)
                if hasattr(embedding, "tolist"):
                    embedding = embedding.tolist()
                return [float(value) for value in embedding]

            return Embedder(name="sentence-transformers", vector_size=vector_size, encode=encode)
        except Exception as exc:  # pragma: no cover - 运行环境不同会走到这里
            if kind == "sentence-transformers":
                raise SystemExit(f"无法加载 sentence-transformers：{exc}") from exc
            print(f"[warn] sentence-transformers 不可用，回退到 hash embedding：{exc}", file=sys.stderr)

    return Embedder(name="hash", vector_size=HASH_VECTOR_SIZE, encode=lambda text: hash_embed(text, HASH_VECTOR_SIZE))


def load_documents(source_dir: Path = ASSET_DIR) -> list[Document]:
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
    print(f"\n=== {title} ===")
    for index, hit in enumerate(hits, start=1):
        print(f"{index}. id={hit.id} score={hit.score:.4f} source={hit.metadata.get('source')}")
        print(f"   topic={hit.metadata.get('topic')}")
        print(f"   snippet={hit.text[:160].replace(chr(10), ' ')}...")


class MockVectorStore:
    def __init__(self, collection_name: str, embedder: Embedder):
        self.collection_name = collection_name
        self.embedder = embedder
        self._items: list[dict[str, Any]] = []

    def upsert(self, documents: list[Document]) -> None:
        for doc in documents:
            self._items.append(
                {
                    "id": doc.id,
                    "text": doc.text,
                    "metadata": doc.metadata,
                    "vector": self.embedder.encode(doc.text),
                }
            )

    def search(self, query: str, top_k: int) -> list[SearchHit]:
        query_vector = self.embedder.encode(query)
        hits: list[SearchHit] = []
        for item in self._items:
            score = sum(a * b for a, b in zip(query_vector, item["vector"]))
            hits.append(SearchHit(id=item["id"], score=score, text=item["text"], metadata=item["metadata"]))
        hits.sort(key=lambda hit: hit.score, reverse=True)
        return hits[:top_k]


def run_mock(documents: list[Document], query: str, top_k: int, embedder: Embedder, collection_name: str) -> None:
    store = MockVectorStore(collection_name=collection_name, embedder=embedder)
    store.upsert(documents)
    print(f"mode = mock")
    print(f"backend = qdrant-like")
    print(f"collection = {collection_name}")
    print(f"documents = {len(documents)}")
    print(f"embedding = {embedder.name} (dim={embedder.vector_size})")
    print(f"query = {query}")
    print_hits("search hits", store.search(query, top_k=top_k))


def build_qdrant_client(url: str, api_key: str | None) -> Any:
    try:
        from qdrant_client import QdrantClient
    except ImportError as exc:  # pragma: no cover - 依赖缺失时提示
        raise SystemExit("缺少 qdrant-client，请先安装 requirements.txt") from exc

    kwargs: dict[str, Any] = {"url": url}
    if api_key:
        kwargs["api_key"] = api_key
    return QdrantClient(**kwargs)


def recreate_collection(client: Any, collection_name: str) -> None:
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass


def run_real(
    documents: list[Document],
    query: str,
    top_k: int,
    embedder: Embedder,
    collection_name: str,
    url: str,
    api_key: str | None,
    recreate: bool,
) -> None:
    try:
        from qdrant_client.http import models as qmodels
    except ImportError as exc:  # pragma: no cover
        raise SystemExit("缺少 qdrant-client 的 http models，请先安装 requirements.txt") from exc

    client = build_qdrant_client(url=url, api_key=api_key)
    if recreate:
        recreate_collection(client, collection_name)

    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=qmodels.VectorParams(size=embedder.vector_size, distance=qmodels.Distance.COSINE),
        )

    points = [
        qmodels.PointStruct(id=doc.id, vector=embedder.encode(doc.text), payload={"text": doc.text, **doc.metadata})
        for doc in documents
    ]
    client.upsert(collection_name=collection_name, points=points)

    results = client.search(
        collection_name=collection_name,
        query_vector=embedder.encode(query),
        limit=top_k,
        with_payload=True,
    )
    hits = [
        SearchHit(
            id=str(result.id),
            score=float(result.score),
            text=str((result.payload or {}).get("text", "")),
            metadata={k: v for k, v in (result.payload or {}).items() if k != "text"},
        )
        for result in results
    ]

    print(f"mode = real")
    print(f"backend = qdrant")
    print(f"qdrant_url = {url}")
    print(f"collection = {collection_name}")
    print(f"documents = {len(documents)}")
    print(f"embedding = {embedder.name} (dim={embedder.vector_size})")
    print(f"query = {query}")
    print_hits("search hits", hits)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="真实 Qdrant 版骨架")
    parser.add_argument("query", help="要检索的问题")
    parser.add_argument("--mode", choices=["mock", "real"], default="mock")
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--source-dir", default=str(ASSET_DIR))
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--embedding", choices=["auto", "hash", "sentence-transformers"], default="auto")
    parser.add_argument("--qdrant-url", default=os.getenv("QDRANT_URL", "http://localhost:6333"))
    parser.add_argument("--qdrant-api-key", default=os.getenv("QDRANT_API_KEY"))
    parser.add_argument("--recreate", action="store_true", help="重建 collection，适合调试时清空旧数据")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_dir = Path(args.source_dir)
    documents = load_documents(source_dir)
    if not documents:
        raise SystemExit(f"{source_dir} 中没有找到示例文档")

    embedder = build_embedder(args.embedding)
    if args.mode == "mock":
        run_mock(documents, args.query, args.top_k, embedder, args.collection)
    else:
        run_real(
            documents=documents,
            query=args.query,
            top_k=args.top_k,
            embedder=embedder,
            collection_name=args.collection,
            url=args.qdrant_url,
            api_key=args.qdrant_api_key,
            recreate=args.recreate,
        )

    print("\n=== how to read this demo ===")
    print("1. embedder 负责把文本变成向量")
    print("2. documents 先写入 collection")
    print("3. search 会返回 top-k 命中")
    print("4. real 模式对应真实 Qdrant Client，mock 模式方便先看流程")


if __name__ == "__main__":
    main()
