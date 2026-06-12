from __future__ import annotations

from pymilvus import connections, MilvusClient, FieldSchema, CollectionSchema, DataType, Collection, AnnSearchRequest, RRFRanker
from _compat import hash_embed


COLLECTION_NAME = "hybrid_multimodal_demo"
MILVUS_URI = "http://localhost:19530"

samples = [
    {"img_id": "1", "title": "红色火龙", "description": "喷火的红色巨龙", "category": "western_dragon"},
    {"img_id": "2", "title": "悬崖上的白龙", "description": "栖息在悬崖边缘的白色巨龙", "category": "western_dragon"},
    {"img_id": "3", "title": "中华金龙", "description": "祥云间盘旋的金色中华龙", "category": "chinese_dragon"},
    {"img_id": "4", "title": "奔跑的奶龙", "description": "可爱的小恐龙角色", "category": "movie_character"},
]

connections.connect(uri=MILVUS_URI)
client = MilvusClient(uri=MILVUS_URI)
if client.has_collection(COLLECTION_NAME):
    client.drop_collection(COLLECTION_NAME)

fields = [
    FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, auto_id=True, max_length=100),
    FieldSchema(name="dense_vector", dtype=DataType.FLOAT_VECTOR, dim=384),
    FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=256),
    FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=64),
]
collection = Collection(name=COLLECTION_NAME, schema=CollectionSchema(fields, description="离线混合多模态"))
collection.create_index("dense_vector", {"index_type": "AUTOINDEX", "metric_type": "COSINE"})
collection.insert([
    [hash_embed(f"{item['title']} {item['description']}", 384).tolist() for item in samples],
    [item["title"] for item in samples],
    [item["category"] for item in samples],
])
collection.load()

query = "悬崖上的巨龙"
query_vec = hash_embed(query, 384).tolist()
results = collection.search([query_vec], anns_field="dense_vector", param={"metric_type": "COSINE"}, limit=4, output_fields=["title", "category"])[0]
print("混合多模态搜索结果:")
for i, hit in enumerate(results, 1):
    print(f"{i}. {hit.entity['title']} ({hit.entity['category']}) -> {hit.distance:.4f}")

client.drop_collection(COLLECTION_NAME)
