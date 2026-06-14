"""
文件功能概述：`code/C1/02_llamaIndex_example.py` 主要是 02LlamaIndex示例，这个文件里有 0 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 这个文件没有独立类或函数，主要靠模块级代码直接执行。
"""

import contextlib
import os
import sys
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai_like import OpenAILike
from openrouter_env import (
    describe_openrouter_runtime,
    resolve_openrouter_api_key,
    resolve_openrouter_base_url,
    resolve_openrouter_model,
)

ROOT = Path(__file__).resolve().parents[2]


@contextlib.contextmanager
def _without_local_code_path():
    code_path = str(ROOT / "code")
    original_sys_path = list(sys.path)
    try:
        sys.path = [item for item in sys.path if item != code_path]
        yield
    finally:
        sys.path = original_sys_path


with _without_local_code_path():
    from openai import OpenAI as OpenAIClient

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

load_dotenv(find_dotenv(usecwd=True))

api_key = resolve_openrouter_api_key()
if not api_key:
    raise ValueError("请先设置 OPENROUTER_API_KEY，或配置 openRouter/openRouterAPI")

print(f"使用模型: {describe_openrouter_runtime()}")

Settings.llm = OpenAILike(
    model=resolve_openrouter_model(),
    api_key=api_key,
    api_base=resolve_openrouter_base_url(),
    is_chat_model=True,
)
Settings.embed_model = _embed_model

docs = SimpleDirectoryReader(input_files=[str(ROOT / "data/C1/markdown/easy-rl-chapter1.md")]).load_data()
index = VectorStoreIndex.from_documents(docs)
retriever = index.as_retriever(similarity_top_k=min(3, len(docs)))

question = "文中举了哪些例子?"
retrieved_nodes = retriever.retrieve(question)
retrieved_docs = [node.node for node in retrieved_nodes]
context = "\n\n".join(doc.page_content for doc in retrieved_docs)[:12000]

prompt_text = f"""请根据下面提供的上下文信息来回答问题。
请确保你的回答完全基于这些上下文。
如果上下文中没有足够的信息来回答问题，请直接告知：“抱歉，我无法根据提供的上下文找到相关信息来回答此问题。”

上下文:
{context}

问题: {question}

回答:"""

client = OpenAIClient(
    api_key=api_key,
    base_url=resolve_openrouter_base_url(),
)
response = client.chat.completions.create(
    model=resolve_openrouter_model(),
    messages=[
        {
            "role": "system",
            "content": "你是一个严格基于上下文回答的助手，只能使用提供的文档内容作答。",
        },
        {"role": "user", "content": prompt_text},
    ],
    temperature=0.2,
    max_tokens=800,
)

print({"retrieved_docs": len(retrieved_docs), "source": str(ROOT / "data/C1/markdown/easy-rl-chapter1.md")})
print(response.choices[0].message.content)
