from __future__ import annotations

from pymilvus import connections, MilvusClient, FieldSchema, CollectionSchema, DataType, Collection, AnnSearchRequest, RRFRanker
from _compat import hash_embed
import numpy as np


COLLECTION_NAME = "multimodal_demo"
MILVUS_URI = "http://localhost:19530"

print("--> 正在初始化离线多模态示例...")
connections.connect(uri=MILVUS_URI)
client = MilvusClient(uri=MILVUS_URI)
if client.has_collection(COLLECTION_NAME):
    client.drop_collection(COLLECTION_NAME)

fields = [
    FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, auto_id=True, max_length=100),
    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=384),
    FieldSchema(name="image_path", dtype=DataType.VARCHAR, max_length=512),
]
collection = Collection(name=COLLECTION_NAME, schema=CollectionSchema(fields, description="离线多模态示例"))
collection.create_index("vector", {"index_type": "HNSW", "metric_type": "COSINE"})

images = [
    "dragon01.png",
    "dragon02.png",
    "dragon03.png",
    "dragon04.png",
]
vectors = [hash_embed(name, 384).tolist() for name in images]
collection.insert([vectors, images])
collection.load()

query = "一条龙"
query_vec = hash_embed(query, 384).tolist()
results = collection.search([query_vec], anns_field="vector", param={"metric_type": "COSINE"}, limit=3, output_fields=["image_path"])[0]

print("检索结果:")
for i, hit in enumerate(results, 1):
    print(f"  Top {i}: 距离={hit.distance:.4f}, 路径='{hit.entity['image_path']}'")

client.drop_collection(COLLECTION_NAME)
print(f"已删除 Collection: '{COLLECTION_NAME}'")
