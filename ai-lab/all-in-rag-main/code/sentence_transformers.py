"""
文件功能概述：`code/sentence_transformers.py` 主要是 句子变换器，这个文件里有 1 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `SentenceTransformer`：功能概述：这个类是 `SentenceTransformer`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 model_name, device，最后把结果交给下一步或直接结束。 2. `get_sentence_embedding_dimension`：先进入当前步骤，最后返回结果。 3. `encode`：先接收输入参数 texts, normalize_embeddings, batch_size, convert_to_numpy，接着根据条件分支选择不同处理路径，再调用 isinstance、hash_embed、embedding.tolist 等内部步骤完成主要工作，最后返回结果。
"""

from __future__ import annotations

from typing import Iterable, List

from _compat import DEFAULT_EMBED_DIM, hash_embed


class SentenceTransformer:
    """
    功能概述：这个类是 `SentenceTransformer`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 model_name, device，最后把结果交给下一步或直接结束。
    2. `get_sentence_embedding_dimension`：先进入当前步骤，最后返回结果。
    3. `encode`：先接收输入参数 texts, normalize_embeddings, batch_size, convert_to_numpy，接着根据条件分支选择不同处理路径，再调用 isinstance、hash_embed、embedding.tolist 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, model_name: str, device: str | None = None):  # 中文名称：初始化
        self.model_name = model_name
        self.device = device or "cpu"
        self._dimension = DEFAULT_EMBED_DIM

    def get_sentence_embedding_dimension(self) -> int:  # 中文名称：获取句子向量化dimension
        return self._dimension

    def encode(
        self,
        texts: str | Iterable[str],
        normalize_embeddings: bool = True,
        batch_size: int = 32,
        convert_to_numpy: bool = True,
    ):  # 中文名称：encode
        if isinstance(texts, str):
            texts = [texts]
        embeddings = [hash_embed(text, self._dimension) for text in texts]
        if convert_to_numpy:
            return embeddings
        return [embedding.tolist() for embedding in embeddings]

