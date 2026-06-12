"""
文件功能概述：`code/C4/02_text_to_metadata_filter.py` 主要是 02文本to元数据过滤，这个文件里有 0 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 这个文件没有独立类或函数，主要靠模块级代码直接执行。
"""

from __future__ import annotations

from langchain_core.documents import Document
from langchain_community.document_loaders import BiliBiliLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


video_urls = [
    "https://www.bilibili.com/video/BV1Bo4y1A7FU",
    "https://www.bilibili.com/video/BV1ug4y157xA",
    "https://www.bilibili.com/video/BV1yh411V7ge",
]

bili = []
loader = BiliBiliLoader(video_urls=video_urls)
docs = loader.load()
for doc in docs:
    original = doc.metadata
    doc.metadata = {
        "title": original.get("title", "未知标题"),
        "author": original.get("owner", {}).get("name", "未知作者"),
        "source": original.get("bvid", "未知ID"),
        "view_count": original.get("stat", {}).get("view", 0),
        "length": original.get("duration", 0),
    }
    bili.append(doc)

embed_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
vectorstore = Chroma.from_documents(bili, embed_model)

queries = [
    "时间最短的视频",
    "时长大于600秒的视频",
]

for query in queries:
    print(f"\n--- 查询: '{query}' ---")
    results = vectorstore.similarity_search(query, k=3)
    if "最短" in query:
        results = sorted(results, key=lambda doc: doc.metadata.get("length", 0))
    elif "大于600" in query:
        results = [doc for doc in results if doc.metadata.get("length", 0) > 600]

    if results:
        for doc in results:
            print(f"标题: {doc.metadata.get('title', '未知标题')}")
            print(f"作者: {doc.metadata.get('author', '未知作者')}")
            print(f"观看次数: {doc.metadata.get('view_count', '未知')}")
            print(f"时长: {doc.metadata.get('length', '未知')}秒")
            print("=" * 50)
    else:
        print("未找到匹配的视频")
