from __future__ import annotations

from pymilvus import connections, MilvusClient, FieldSchema, CollectionSchema, DataType, Collection
from _compat import hash_embed


COLLECTION_NAME = "multimodal_dragon_demo"
MILVUS_URI = "http://localhost:19530"

samples = [
    {"img_id": "1", "title": "红色火龙", "description": "喷火的红色巨龙", "image_path": "dragon01.png"},
    {"img_id": "2", "title": "悬崖上的白龙", "description": "栖息在悬崖边缘的白色巨龙", "image_path": "dragon02.png"},
    {"img_id": "3", "title": "中华金龙", "description": "祥云间盘旋的金色中华龙", "image_path": "dragon03.png"},
]

connections.connect(uri=MILVUS_URI)
client = MilvusClient(uri=MILVUS_URI)
if client.has_collection(COLLECTION_NAME):
    client.drop_collection(COLLECTION_NAME)

fields = [
    FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, auto_id=True, max_length=100),
    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=384),
    FieldSchema(name="image_path", dtype=DataType.VARCHAR, max_length=512),
    FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=256),
]
collection = Collection(name=COLLECTION_NAME, schema=CollectionSchema(fields, description="离线龙检索"))
collection.create_index("vector", {"index_type": "AUTOINDEX", "metric_type": "COSINE"})
collection.insert([
    [hash_embed(f"{item['title']} {item['description']}", 384).tolist() for item in samples],
    [item["image_path"] for item in samples],
    [item["title"] for item in samples],
])
collection.load()

query = "悬崖上的巨龙"
results = collection.search([hash_embed(query, 384).tolist()], anns_field="vector", param={"metric_type": "COSINE"}, limit=3, output_fields=["image_path", "title"])[0]

print("多模态检索结果:")
for i, hit in enumerate(results, 1):
    print(f"{i}. {hit.entity['title']} -> {hit.entity['image_path']} (Score: {hit.distance:.4f})")

client.drop_collection(COLLECTION_NAME)
