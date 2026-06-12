"""
文件功能概述：`code/langchain_community/embeddings.py` 主要是 向量化，这个文件里有 3 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `FakeEmbeddings`：功能概述：这个类是 `FakeEmbeddings`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `embed_documents`：先接收输入参数 texts，再调用 tolist、hash_embed 等内部步骤完成主要工作，最后返回结果。 2. `embed_query`：先接收输入参数 text，再调用 tolist、hash_embed 等内部步骤完成主要工作，最后返回结果。
2. 类 `HuggingFaceEmbeddings`：功能概述：这个类是 `HuggingFaceEmbeddings`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 model_name, model_kwargs, encode_kwargs, size，再调用 __init__、super 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
3. 类 `HuggingFaceBgeEmbeddings`：功能概述：这个类是 `HuggingFaceBgeEmbeddings`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, List

from _compat import DEFAULT_EMBED_DIM, hash_embed


@dataclass
class FakeEmbeddings:
    """
    功能概述：这个类是 `FakeEmbeddings`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `embed_documents`：先接收输入参数 texts，再调用 tolist、hash_embed 等内部步骤完成主要工作，最后返回结果。
    2. `embed_query`：先接收输入参数 text，再调用 tolist、hash_embed 等内部步骤完成主要工作，最后返回结果。
    """
    size: int = DEFAULT_EMBED_DIM

    def embed_documents(self, texts: List[str]) -> List[List[float]]:  # 中文名称：embed文档
        return [hash_embed(text, self.size).tolist() for text in texts]

    def embed_query(self, text: str) -> List[float]:  # 中文名称：embed查询
        return hash_embed(text, self.size).tolist()


class HuggingFaceEmbeddings(FakeEmbeddings):
    """
    功能概述：这个类是 `HuggingFaceEmbeddings`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 model_name, model_kwargs, encode_kwargs, size，再调用 __init__、super 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    """
    def __init__(self, model_name: str = "offline/hash-embed", model_kwargs: dict[str, Any] | None = None, encode_kwargs: dict[str, Any] | None = None, size: int = DEFAULT_EMBED_DIM):  # 中文名称：初始化
        super().__init__(size=size)
        self.model_name = model_name
        self.model_kwargs = model_kwargs or {}
        self.encode_kwargs = encode_kwargs or {}


class HuggingFaceBgeEmbeddings(HuggingFaceEmbeddings):
    """
    功能概述：这个类是 `HuggingFaceBgeEmbeddings`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
    """
    pass

