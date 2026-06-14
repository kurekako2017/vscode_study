"""
文件功能概述：`code/C3/07_recursive_retrieval_v2.py` 主要是 07递归检索v2，这个文件里有 0 个类、1 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 函数 `query_safe_recursive`：先接收输入参数 query_str，接着根据条件分支选择不同处理路径，再调用 print、VectorIndexRetriever、summary_retriever.retrieve 等内部步骤完成主要工作，最后返回结果。
"""

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from openrouter_env import (
    describe_openrouter_runtime,
    resolve_openrouter_api_key,
    resolve_openrouter_base_url,
    resolve_openrouter_model,
)

load_dotenv()

# 配置模型
print(f"使用模型: {describe_openrouter_runtime()}")
Settings.llm = OpenAILike(
    model=resolve_openrouter_model(),
    api_key=resolve_openrouter_api_key(),
    api_base=resolve_openrouter_base_url(),
    is_chat_model=True,
)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")

# 1. 加载和预处理数据
excel_file = Path(__file__).resolve().parents[2] / "data" / "C3" / "excel" / "movie.xlsx"
if excel_file.exists():
    xls = pd.ExcelFile(excel_file)
else:
    xls = None

summary_docs = []
content_docs = []

print("开始加载和处理Excel文件...")
if xls is None:
    sample = pd.DataFrame(
        [
            {"片名": "示例电影A", "评分人数": 1200},
            {"片名": "示例电影B", "评分人数": 300},
            {"片名": "示例电影C", "评分人数": 50},
        ]
    )
    xls_sheet_names = ["年份_1994"]
    iter_sheets = [(xls_sheet_names[0], sample)]
else:
    iter_sheets = [(sheet_name, pd.read_excel(xls, sheet_name=sheet_name)) for sheet_name in xls.sheet_names]

for sheet_name, df in iter_sheets:
    
    # 数据清洗
    if '评分人数' in df.columns:
        df['评分人数'] = df['评分人数'].astype(str).str.replace('人评价', '').str.strip()
        df['评分人数'] = pd.to_numeric(df['评分人数'], errors='coerce').fillna(0).astype(int)

    # 创建摘要文档 (用于路由)
    year = sheet_name.replace('年份_', '')
    summary_text = f"这个表格包含了年份为 {year} 的电影信息，包括电影名称、导演、评分、评分人数等。"
    summary_doc = Document(
        text=summary_text,
        metadata={"sheet_name": sheet_name}
    )
    summary_docs.append(summary_doc)
    
    # 创建内容文档 (用于最终问答)
    content_text = df.to_string(index=False)
    content_doc = Document(
        text=content_text,
        metadata={"sheet_name": sheet_name}
    )
    content_docs.append(content_doc)

print("数据加载和处理完成。\n")

# 2. 构建向量索引
# 使用默认的内存SimpleVectorStore，它支持元数据过滤

# 2.1 为摘要创建索引
summary_index = VectorStoreIndex(summary_docs)

# 2.2 为内容创建索引
content_index = VectorStoreIndex(content_docs)

print("摘要索引和内容索引构建完成。\n")

# 3. 定义两步式查询逻辑
def query_safe_recursive(query_str):  # 中文名称：查询safe递归
    print(f"--- 开始执行查询 ---")
    print(f"查询: {query_str}")
    
    # 第一步：路由 - 在摘要索引中找到最相关的表格
    print("\n第一步：在摘要索引中进行路由...")
    summary_retriever = VectorIndexRetriever(index=summary_index, similarity_top_k=1)
    retrieved_nodes = summary_retriever.retrieve(query_str)
    
    if not retrieved_nodes:
        return "抱歉，未能找到相关的电影年份信息。"
    
    # 获取匹配到的工作表名称
    matched_sheet_name = retrieved_nodes[0].node.metadata['sheet_name']
    print(f"路由结果：匹配到工作表 -> {matched_sheet_name}")
    
    # 第二步：检索 - 在内容索引中根据工作表名称过滤并检索具体内容
    print("\n第二步：在内容索引中检索具体信息...")
    content_retriever = VectorIndexRetriever(
        index=content_index,
        similarity_top_k=1, # 通常只返回最匹配的整个表格即可
        filters=MetadataFilters(
            filters=[ExactMatchFilter(key="sheet_name", value=matched_sheet_name)]
        )
    )
    
    # 创建查询引擎并执行查询
    query_engine = RetrieverQueryEngine.from_args(content_retriever)
    response = query_engine.query(query_str)
    
    print("--- 查询执行结束 ---\n")
    return response

# 4. 执行查询
query = "1994年评分人数最少的电影是哪一部？"
response = query_safe_recursive(query)

print(f"最终回答: {response}")
