"""
文件功能概述：`code/C1/02_llamaIndex_example.py` 主要是 02LlamaIndex示例，这个文件里有 0 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 这个文件没有独立类或函数，主要靠模块级代码直接执行。
"""

import os
from pathlib import Path
# os.environ['HF_ENDPOINT']='https://hf-mirror.com'
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings 
from llama_index.llms.openai_like import OpenAILike
try:
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    _embed_model = HuggingFaceEmbedding("BAAI/bge-small-zh-v1.5")
except Exception as exc:
    print(f"警告: 无法加载 HuggingFaceEmbedding，改用默认离线 embedding: {exc}")
    try:
        from llama_index.core.embeddings.mock_embed_model import MockEmbedding
        _embed_model = MockEmbedding(embed_dim=384)
    except Exception as inner_exc:
        raise RuntimeError(f"无法初始化任何 embedding 模型: {inner_exc}") from inner_exc

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("请先设置 OPENROUTER_API_KEY（或 OPENAI_API_KEY）环境变量")

# 使用 OpenRouter
Settings.llm = OpenAILike(
    model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
    api_key=api_key,
    api_base="https://openrouter.ai/api/v1",
    is_chat_model=True
)

# Settings.llm = OpenAI(
#     model="openai/gpt-4o-mini",
#     api_key=os.getenv("OPENROUTER_API_KEY"),
#     api_base="https://openrouter.ai/api/v1"
# )
Settings.embed_model = _embed_model

ROOT = Path(__file__).resolve().parents[2]
docs = SimpleDirectoryReader(input_files=[str(ROOT / "data/C1/markdown/easy-rl-chapter1.md")]).load_data()

index = VectorStoreIndex.from_documents(docs)

query_engine = index.as_query_engine()

print(query_engine.get_prompts())

print(query_engine.query("文中举了哪些例子?"))
