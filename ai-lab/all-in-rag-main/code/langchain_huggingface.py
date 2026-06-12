"""
文件功能概述：`code/langchain_huggingface.py` 主要是 LangChainhuggingface，这个文件里有 1 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `HuggingFaceEmbeddings`：功能概述：这个类是 `HuggingFaceEmbeddings`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `embed_documents`：先接收输入参数 texts，再调用 tolist、hash_embed 等内部步骤完成主要工作，最后返回结果。 2. `embed_query`：先接收输入参数 text，再调用 tolist、hash_embed 等内部步骤完成主要工作，最后返回结果。 3. `__call__`：先接收输入参数 texts，再调用 self.embed_documents、list 等内部步骤完成主要工作，最后返回结果。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, List

from _compat import DEFAULT_EMBED_DIM, hash_embed


@dataclass
class HuggingFaceEmbeddings:
    """
    功能概述：这个类是 `HuggingFaceEmbeddings`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `embed_documents`：先接收输入参数 texts，再调用 tolist、hash_embed 等内部步骤完成主要工作，最后返回结果。
    2. `embed_query`：先接收输入参数 text，再调用 tolist、hash_embed 等内部步骤完成主要工作，最后返回结果。
    3. `__call__`：先接收输入参数 texts，再调用 self.embed_documents、list 等内部步骤完成主要工作，最后返回结果。
    """
    model_name: str = "offline/hash-embed"
    model_kwargs: dict[str, Any] | None = None
    encode_kwargs: dict[str, Any] | None = None
    dimension: int = DEFAULT_EMBED_DIM

    def embed_documents(self, texts: List[str]) -> List[List[float]]:  # 中文名称：embed文档
        return [hash_embed(text, self.dimension).tolist() for text in texts]

    def embed_query(self, text: str) -> List[float]:  # 中文名称：embed查询
        return hash_embed(text, self.dimension).tolist()

    def __call__(self, texts: Iterable[str]) -> List[List[float]]:  # 中文名称：可调用执行
        return self.embed_documents(list(texts))

