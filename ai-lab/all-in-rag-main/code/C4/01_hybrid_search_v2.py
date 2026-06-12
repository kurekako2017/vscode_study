from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from pymilvus import connections, MilvusClient, FieldSchema, CollectionSchema, DataType, Collection, AnnSearchRequest, RRFRanker
from _compat import hash_embed


COLLECTION_NAME = "dragon_siglip_demo"
MILVUS_URI = "http://localhost:19530"


class OfflineSigLIPEmbeddingFunction:
    def __init__(self, device: str = "cpu"):
        self.device = device
        self.dense_dim = 384
        self.tfidf_vectorizer = TfidfVectorizer(max_features=10000)
        self.tfidf_fitted = False

    @property
    def dim(self):
        return {"dense": self.dense_dim, "sparse": 10000}

    def fit_sparse(self, docs):
        self.tfidf_vectorizer.fit(docs)
        self.tfidf_fitted = True

    def __call__(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        if not self.tfidf_fitted:
            self.fit_sparse(texts)
        dense = np.asarray([hash_embed(text, self.dense_dim) for text in texts], dtype=np.float32)
        sparse = self.tfidf_vectorizer.transform(texts)
        return {"dense": dense, "sparse": sparse}


print(f"--> 正在连接到 Milvus: {MILVUS_URI}")
connections.connect(uri=MILVUS_URI)

print("--> 正在初始化离线 SigLIP 替代嵌入模型...")
ef = OfflineSigLIPEmbeddingFunction(device="cpu")

milvus_client = MilvusClient(uri=MILVUS_URI)
if milvus_client.has_collection(COLLECTION_NAME):
    milvus_client.drop_collection(COLLECTION_NAME)

fields = [
    FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=True, max_length=100),
    FieldSchema(name="img_id", dtype=DataType.VARCHAR, max_length=100),
    FieldSchema(name="path", dtype=DataType.VARCHAR, max_length=256),
    FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=256),
    FieldSchema(name="description", dtype=DataType.VARCHAR, max_length=4096),
    FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=64),
    FieldSchema(name="location", dtype=DataType.VARCHAR, max_length=128),
    FieldSchema(name="environment", dtype=DataType.VARCHAR, max_length=64),
    FieldSchema(name="sparse_vector", dtype=DataType.SPARSE_FLOAT_VECTOR),
    FieldSchema(name="dense_vector", dtype=DataType.FLOAT_VECTOR, dim=ef.dim["dense"]),
]

collection = Collection(name=COLLECTION_NAME, schema=CollectionSchema(fields, description="离线龙混合检索示例"))
collection.create_index("sparse_vector", {"index_type": "SPARSE_INVERTED_INDEX", "metric_type": "IP"})
collection.create_index("dense_vector", {"index_type": "AUTOINDEX", "metric_type": "IP"})
collection.load()

if collection.is_empty:
    dataset = [
        {"img_id": "1", "path": "dragon01.png", "title": "红色火龙", "description": "一条喷火的红色巨龙", "category": "western_dragon", "location": "山谷", "environment": "火山"},
        {"img_id": "2", "path": "dragon02.png", "title": "悬崖上的白龙", "description": "一头雄伟的白色巨龙栖息在悬崖边缘", "category": "western_dragon", "location": "悬崖", "environment": "海岸"},
        {"img_id": "3", "path": "dragon03.png", "title": "中华金龙", "description": "一条金色的中华龙在祥云间盘旋", "category": "chinese_dragon", "location": "祥云", "environment": "天空"},
        {"img_id": "4", "path": "dragon04.png", "title": "奔跑的奶龙", "description": "一只Q版的黄色小恐龙", "category": "movie_character", "location": "草地", "environment": "童话"},
    ]

    docs = [" ".join([item["title"], item["description"], item["location"], item["environment"]]) for item in dataset]
    embeddings = ef(docs)
    collection.insert([
        [item["img_id"] for item in dataset],
        [item["path"] for item in dataset],
        [item["title"] for item in dataset],
        [item["description"] for item in dataset],
        [item["category"] for item in dataset],
        [item["location"] for item in dataset],
        [item["environment"] for item in dataset],
        [embeddings["sparse"]._getrow(i).toarray()[0].tolist() for i in range(len(dataset))],
        embeddings["dense"].tolist(),
    ])

search_query = "悬崖上的巨龙"
search_filter = 'category in ["western_dragon", "chinese_dragon", "movie_character"]'
top_k = 5

print(f"\n{'='*20} 开始混合搜索 {'='*20}")
print(f"查询: '{search_query}'")

query_embeddings = ef([search_query])
dense_vec = query_embeddings["dense"][0]
sparse_vec = query_embeddings["sparse"]._getrow(0)

search_params = {"metric_type": "IP", "params": {}}

print("\n--- [单独] 密集向量搜索结果 ---")
dense_results = collection.search(
    [dense_vec],
    anns_field="dense_vector",
    param=search_params,
    limit=top_k,
    expr=search_filter,
    output_fields=["title", "path", "description", "category", "location", "environment"],
)[0]
for i, hit in enumerate(dense_results, 1):
    print(f"{i}. {hit.entity.get('title')} (Score: {hit.distance:.4f})")

print("\n--- [单独] 稀疏向量搜索结果 ---")
sparse_results = collection.search(
    [sparse_vec],
    anns_field="sparse_vector",
    param=search_params,
    limit=top_k,
    expr=search_filter,
    output_fields=["title", "path", "description", "category", "location", "environment"],
)[0]
for i, hit in enumerate(sparse_results, 1):
    print(f"{i}. {hit.entity.get('title')} (Score: {hit.distance:.4f})")

print("\n--- [混合] 稀疏+密集向量搜索结果 ---")
rerank = RRFRanker(k=60)
dense_req = AnnSearchRequest([dense_vec], "dense_vector", search_params, limit=top_k)
sparse_req = AnnSearchRequest([sparse_vec], "sparse_vector", search_params, limit=top_k)
results = collection.hybrid_search([sparse_req, dense_req], rerank=rerank, limit=top_k, output_fields=["title", "path", "description", "category", "location", "environment"])[0]
for i, hit in enumerate(results, 1):
    print(f"{i}. {hit.entity.get('title')} (Score: {hit.distance:.4f})")
