"""
文件功能概述：`code/pymilvus/__init__.py` 主要是 初始化，这个文件里有 13 个类、6 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `_DataType`：功能概述：这个类是 `_DataType`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
2. 类 `FieldSchema`：功能概述：这个类是 `FieldSchema`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
3. 类 `CollectionSchema`：功能概述：这个类是 `CollectionSchema`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
4. 类 `_IndexParams`：功能概述：这个类是 `_IndexParams`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先进入当前步骤，最后把结果交给下一步或直接结束。 2. `add_index`：先接收输入参数 **kwargs，再调用 self.indices.append 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
5. 类 `connections`：功能概述：这个类是 `connections`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `connect`：先接收输入参数 **kwargs，最后返回结果。
6. 类 `AnnSearchRequest`：功能概述：这个类是 `AnnSearchRequest`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 data, anns_field, param, limit，最后把结果交给下一步或直接结束。
7. 类 `RRFRanker`：功能概述：这个类是 `RRFRanker`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 k，最后把结果交给下一步或直接结束。
8. 类 `_Hit`：功能概述：这个类是 `_Hit`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 entity, distance，最后把结果交给下一步或直接结束。
9. 函数 `_cosine_score`：先接收输入参数 query_vec, doc_vec，接着根据条件分支选择不同处理路径，再调用 float、normalize_vectors、np.dot 等内部步骤完成主要工作，最后返回结果。
10. 函数 `_to_dense`：先接收输入参数 vec，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 isinstance、hasattr、np.asarray 等内部步骤完成主要工作，最后返回结果。
11. 函数 `_passes_expr`：先接收输入参数 entity, expr，接着根据条件分支选择不同处理路径，再调用 expr.strip、re.match、m.group 等内部步骤完成主要工作，最后返回结果。
12. 类 `_CollectionState`：功能概述：这个类是 `_CollectionState`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 name, schema，最后把结果交给下一步或直接结束。 2. `num_entities`：先进入当前步骤，再调用 len 等内部步骤完成主要工作，最后返回结果。
13. 函数 `_ensure_collection`：先接收输入参数 name，接着根据条件分支选择不同处理路径，再调用 _CollectionState 等内部步骤完成主要工作，最后返回结果。
14. 类 `MilvusClient`：功能概述：这个类是 `MilvusClient`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 uri，最后把结果交给下一步或直接结束。 2. `has_collection`：先接收输入参数 collection_name，最后返回结果。 3. `drop_collection`：先接收输入参数 collection_name，再调用 _GLOBAL_COLLECTIONS.pop 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 4. `create_collection`：先接收输入参数 collection_name, schema, consistency_level，再调用 _CollectionState 等内部步骤完成主要工作，最后返回结果。 5. `prepare_index_params`：先进入当前步骤，再调用 _IndexParams 等内部步骤完成主要工作，最后返回结果。 6. `create_index`：先接收输入参数 collection_name, index_params，再调用 indexes.append、_ensure_collection 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 7. `load_collection`：先接收输入参数 collection_name，再调用 _ensure_collection 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 8. `release_collection`：先接收输入参数 collection_name，再调用 _ensure_collection 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 9. `insert`：先接收输入参数 collection_name, data，再调用 _ensure_collection、_normalize_insert_data、collection.rows.extend 等内部步骤完成主要工作，最后返回结果。 10. `search`：先接收输入参数 collection_name, data, anns_field, search_params, limit, output_fields, expr, param, **kwargs，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 _ensure_collection、_to_dense、results.sort 等内部步骤完成主要工作，最后返回结果。 11. `hybrid_search`：先接收输入参数 collection_name, reqs, rerank, limit, output_fields, **kwargs，然后循环处理每一条数据，再调用 _ensure_collection、final.sort、enumerate 等内部步骤完成主要工作，最后返回结果。
15. 类 `Collection`：功能概述：这个类是 `Collection`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 name, schema, consistency_level，接着根据条件分支选择不同处理路径，再调用 _ensure_collection、_CollectionState 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `_state`：先进入当前步骤，再调用 _ensure_collection 等内部步骤完成主要工作，最后返回结果。 3. `num_entities`：先进入当前步骤，最后返回结果。 4. `is_empty`：先进入当前步骤，最后返回结果。 5. `create_index`：先接收输入参数 field_name, index_params，再调用 self._state.indexes.append 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 6. `insert`：先接收输入参数 data，再调用 _normalize_insert_data、self._state.rows.extend、len 等内部步骤完成主要工作，最后返回结果。 7. `flush`：先进入当前步骤，最后返回结果。 8. `load`：先进入当前步骤，最后把结果交给下一步或直接结束。 9. `search`：先接收输入参数 *args, **kwargs，再调用 MilvusClient、client.search 等内部步骤完成主要工作，最后返回结果。 10. `hybrid_search`：先接收输入参数 *args, **kwargs，再调用 MilvusClient、client.hybrid_search 等内部步骤完成主要工作，最后返回结果。
16. 函数 `_row_key`：先接收输入参数 entity，再调用 abs、hash、json.dumps 等内部步骤完成主要工作，最后返回结果。
17. 函数 `_normalize_insert_data`：先接收输入参数 collection, data，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 isinstance、all、len 等内部步骤完成主要工作，最后返回结果。
18. 类 `_BGEM3SparseMatrix`：功能概述：这个类是 `_BGEM3SparseMatrix`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 matrix，最后把结果交给下一步或直接结束。 2. `_getrow`：先接收输入参数 index，再调用 self.matrix.getrow 等内部步骤完成主要工作，最后返回结果。 3. `shape`：先进入当前步骤，最后返回结果。
19. 类 `BGEM3EmbeddingFunction`：功能概述：这个类是 `BGEM3EmbeddingFunction`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 use_fp16, device，再调用 TfidfVectorizer 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `dim`：先进入当前步骤，最后返回结果。 3. `fit_sparse`：先接收输入参数 docs，再调用 self.tfidf_vectorizer.fit 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 4. `__call__`：先接收输入参数 texts，接着根据条件分支选择不同处理路径，再调用 isinstance、np.asarray、self.tfidf_vectorizer.transform 等内部步骤完成主要工作，最后返回结果。
"""

from __future__ import annotations

import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any, Dict, Iterable, List, Sequence

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from _compat import DEFAULT_EMBED_DIM, hash_embed, normalize_vectors


class _DataType:
    """
    功能概述：这个类是 `_DataType`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
    """
    VARCHAR = "VARCHAR"
    FLOAT_VECTOR = "FLOAT_VECTOR"
    SPARSE_FLOAT_VECTOR = "SPARSE_FLOAT_VECTOR"


DataType = _DataType()


@dataclass
class FieldSchema:
    """
    功能概述：这个类是 `FieldSchema`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
    """
    name: str
    dtype: str
    is_primary: bool = False
    auto_id: bool = False
    max_length: int | None = None
    dim: int | None = None


@dataclass
class CollectionSchema:
    """
    功能概述：这个类是 `CollectionSchema`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
    """
    fields: list[FieldSchema]
    description: str = ""


class _IndexParams:
    """
    功能概述：这个类是 `_IndexParams`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先进入当前步骤，最后把结果交给下一步或直接结束。
    2. `add_index`：先接收输入参数 **kwargs，再调用 self.indices.append 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    """
    def __init__(self):  # 中文名称：初始化
        self.indices: list[dict[str, Any]] = []

    def add_index(self, **kwargs: Any):  # 中文名称：add索引
        self.indices.append(kwargs)


class connections:
    """
    功能概述：这个类是 `connections`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `connect`：先接收输入参数 **kwargs，最后返回结果。
    """
    @staticmethod
    def connect(**kwargs: Any):  # 中文名称：connect
        return True


class AnnSearchRequest:
    """
    功能概述：这个类是 `AnnSearchRequest`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 data, anns_field, param, limit，最后把结果交给下一步或直接结束。
    """
    def __init__(self, data, anns_field, param, limit):  # 中文名称：初始化
        self.data = data
        self.anns_field = anns_field
        self.param = param
        self.limit = limit


class RRFRanker:
    """
    功能概述：这个类是 `RRFRanker`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 k，最后把结果交给下一步或直接结束。
    """
    def __init__(self, k: int = 60):  # 中文名称：初始化
        self.k = k


class _Hit:
    """
    功能概述：这个类是 `_Hit`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 entity, distance，最后把结果交给下一步或直接结束。
    """
    def __init__(self, entity: dict[str, Any], distance: float):  # 中文名称：初始化
        self.entity = entity
        self.distance = distance


_GLOBAL_COLLECTIONS: dict[str, dict[str, Any]] = {}


def _cosine_score(query_vec: np.ndarray, doc_vec: np.ndarray) -> float:  # 中文名称：cosinescore
    if query_vec.ndim == 1:
        query_vec = query_vec[None, :]
    if doc_vec.ndim == 1:
        doc_vec = doc_vec[None, :]
    q = normalize_vectors(np.asarray(query_vec, dtype=np.float32))[0]
    d = normalize_vectors(np.asarray(doc_vec, dtype=np.float32))[0]
    return float(np.dot(q, d))


def _to_dense(vec):  # 中文名称：todense
    if isinstance(vec, np.ndarray):
        return vec.astype(np.float32)
    if isinstance(vec, list):
        return np.asarray(vec, dtype=np.float32)
    if hasattr(vec, "toarray"):
        arr = vec.toarray()
        return np.asarray(arr[0], dtype=np.float32) if arr.ndim == 2 else np.asarray(arr, dtype=np.float32)
    if isinstance(vec, dict):
        dim = max(vec.keys(), default=-1) + 1
        arr = np.zeros(dim, dtype=np.float32)
        for idx, value in vec.items():
            arr[int(idx)] = float(value)
        return arr
    return np.asarray(vec, dtype=np.float32)


def _passes_expr(entity: dict[str, Any], expr: str | None) -> bool:  # 中文名称：passesexpr
    if not expr:
        return True
    expr = expr.strip()
    m = re.match(r'(\w+)\s+in\s+\[(.*)\]', expr)
    if m:
        key, values = m.group(1), m.group(2)
        parsed = [v.strip().strip('"').strip("'") for v in values.split(",") if v.strip()]
        return str(entity.get(key)) in parsed
    m = re.match(r'(\w+)\s*==\s*["\']?(.*?)["\']?$', expr)
    if m:
        key, value = m.group(1), m.group(2)
        return str(entity.get(key)) == value
    return True


class _CollectionState:
    """
    功能概述：这个类是 `_CollectionState`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 name, schema，最后把结果交给下一步或直接结束。
    2. `num_entities`：先进入当前步骤，再调用 len 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, name: str, schema: CollectionSchema | None = None):  # 中文名称：初始化
        self.name = name
        self.schema = schema
        self.rows: list[dict[str, Any]] = []
        self.indexes: list[dict[str, Any]] = []
        self.loaded = False

    @property
    def num_entities(self) -> int:  # 中文名称：numentities
        return len(self.rows)


def _ensure_collection(name: str) -> _CollectionState:  # 中文名称：ensurecollection
    if name not in _GLOBAL_COLLECTIONS:
        _GLOBAL_COLLECTIONS[name] = _CollectionState(name)
    return _GLOBAL_COLLECTIONS[name]


class MilvusClient:
    """
    功能概述：这个类是 `MilvusClient`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 uri，最后把结果交给下一步或直接结束。
    2. `has_collection`：先接收输入参数 collection_name，最后返回结果。
    3. `drop_collection`：先接收输入参数 collection_name，再调用 _GLOBAL_COLLECTIONS.pop 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    4. `create_collection`：先接收输入参数 collection_name, schema, consistency_level，再调用 _CollectionState 等内部步骤完成主要工作，最后返回结果。
    5. `prepare_index_params`：先进入当前步骤，再调用 _IndexParams 等内部步骤完成主要工作，最后返回结果。
    6. `create_index`：先接收输入参数 collection_name, index_params，再调用 indexes.append、_ensure_collection 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    7. `load_collection`：先接收输入参数 collection_name，再调用 _ensure_collection 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    8. `release_collection`：先接收输入参数 collection_name，再调用 _ensure_collection 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    9. `insert`：先接收输入参数 collection_name, data，再调用 _ensure_collection、_normalize_insert_data、collection.rows.extend 等内部步骤完成主要工作，最后返回结果。
    10. `search`：先接收输入参数 collection_name, data, anns_field, search_params, limit, output_fields, expr, param, **kwargs，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 _ensure_collection、_to_dense、results.sort 等内部步骤完成主要工作，最后返回结果。
    11. `hybrid_search`：先接收输入参数 collection_name, reqs, rerank, limit, output_fields, **kwargs，然后循环处理每一条数据，再调用 _ensure_collection、final.sort、enumerate 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, uri: str | None = None):  # 中文名称：初始化
        self.uri = uri

    def has_collection(self, collection_name: str) -> bool:  # 中文名称：是否具有collection
        return collection_name in _GLOBAL_COLLECTIONS

    def drop_collection(self, collection_name: str):  # 中文名称：dropcollection
        _GLOBAL_COLLECTIONS.pop(collection_name, None)

    def create_collection(self, collection_name: str, schema: CollectionSchema, consistency_level: str = "Strong"):  # 中文名称：创建collection
        _GLOBAL_COLLECTIONS[collection_name] = _CollectionState(collection_name, schema=schema)
        return True

    def prepare_index_params(self):  # 中文名称：prepare索引params
        return _IndexParams()

    def create_index(self, collection_name: str, index_params: Any):  # 中文名称：创建索引
        _ensure_collection(collection_name).indexes.append(index_params)

    def load_collection(self, collection_name: str):  # 中文名称：加载collection
        _ensure_collection(collection_name).loaded = True

    def release_collection(self, collection_name: str):  # 中文名称：releasecollection
        _ensure_collection(collection_name).loaded = False

    def insert(self, collection_name: str, data: Any):  # 中文名称：insert
        collection = _ensure_collection(collection_name)
        rows = _normalize_insert_data(collection, data)
        collection.rows.extend(rows)
        return {"insert_count": len(rows)}

    def search(
        self,
        collection_name: str,
        data: Sequence[Any],
        anns_field: str,
        search_params: dict[str, Any] | None = None,
        limit: int = 10,
        output_fields: list[str] | None = None,
        expr: str | None = None,
        param: dict[str, Any] | None = None,
        **kwargs: Any,
    ):  # 中文名称：搜索
        if search_params is None:
            search_params = param or {}
        collection = _ensure_collection(collection_name)
        query_vec = _to_dense(data[0])
        results: list[_Hit] = []
        for row in collection.rows:
            if not _passes_expr(row, expr):
                continue
            doc_vec = _to_dense(row.get(anns_field, []))
            score = _cosine_score(query_vec, doc_vec)
            entity = {field: row.get(field) for field in (output_fields or row.keys())}
            results.append(_Hit(entity, score))
        results.sort(key=lambda h: h.distance, reverse=True)
        return [results[:limit]]

    def hybrid_search(self, collection_name: str, reqs: list[AnnSearchRequest], rerank: RRFRanker, limit: int, output_fields: list[str] | None = None, **kwargs: Any):  # 中文名称：混合搜索
        collection = _ensure_collection(collection_name)
        ranked: dict[int, float] = {}
        entities: dict[int, dict[str, Any]] = {}
        for req in reqs:
            partial = self.search(collection_name, req.data, req.anns_field, req.param, req.limit, output_fields=output_fields)[0]
            for rank, hit in enumerate(partial):
                row_key = _row_key(hit.entity)
                ranked[row_key] = ranked.get(row_key, 0.0) + 1.0 / (rerank.k + rank + 1)
                entities[row_key] = hit.entity
        final = [_Hit(entity=entities[key], distance=score) for key, score in ranked.items()]
        final.sort(key=lambda h: h.distance, reverse=True)
        return [final[:limit]]


class Collection:
    """
    功能概述：这个类是 `Collection`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 name, schema, consistency_level，接着根据条件分支选择不同处理路径，再调用 _ensure_collection、_CollectionState 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `_state`：先进入当前步骤，再调用 _ensure_collection 等内部步骤完成主要工作，最后返回结果。
    3. `num_entities`：先进入当前步骤，最后返回结果。
    4. `is_empty`：先进入当前步骤，最后返回结果。
    5. `create_index`：先接收输入参数 field_name, index_params，再调用 self._state.indexes.append 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    6. `insert`：先接收输入参数 data，再调用 _normalize_insert_data、self._state.rows.extend、len 等内部步骤完成主要工作，最后返回结果。
    7. `flush`：先进入当前步骤，最后返回结果。
    8. `load`：先进入当前步骤，最后把结果交给下一步或直接结束。
    9. `search`：先接收输入参数 *args, **kwargs，再调用 MilvusClient、client.search 等内部步骤完成主要工作，最后返回结果。
    10. `hybrid_search`：先接收输入参数 *args, **kwargs，再调用 MilvusClient、client.hybrid_search 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, name: str, schema: CollectionSchema | None = None, consistency_level: str = "Strong"):  # 中文名称：初始化
        self.name = name
        if schema is not None:
            _GLOBAL_COLLECTIONS[name] = _CollectionState(name, schema=schema)
        _ensure_collection(name)

    @property
    def _state(self) -> _CollectionState:  # 中文名称：state
        return _ensure_collection(self.name)

    @property
    def num_entities(self) -> int:  # 中文名称：numentities
        return self._state.num_entities

    @property
    def is_empty(self) -> bool:  # 中文名称：是否empty
        return self._state.num_entities == 0

    def create_index(self, field_name: str, index_params: dict[str, Any]):  # 中文名称：创建索引
        self._state.indexes.append({"field": field_name, "params": index_params})

    def insert(self, data: Any):  # 中文名称：insert
        rows = _normalize_insert_data(self._state, data)
        self._state.rows.extend(rows)
        return {"insert_count": len(rows)}

    def flush(self):  # 中文名称：flush
        return True

    def load(self):  # 中文名称：加载
        self._state.loaded = True

    def search(self, *args, **kwargs):  # 中文名称：搜索
        client = MilvusClient()
        return client.search(self.name, *args, **kwargs)

    def hybrid_search(self, *args, **kwargs):  # 中文名称：混合搜索
        client = MilvusClient()
        return client.hybrid_search(self.name, *args, **kwargs)


def _row_key(entity: dict[str, Any]) -> int:  # 中文名称：rowkey
    return abs(hash(json.dumps(entity, sort_keys=True, ensure_ascii=False))) % (10**12)


def _normalize_insert_data(collection: _CollectionState, data: Any) -> list[dict[str, Any]]:  # 中文名称：normalizeinsertdata
    if isinstance(data, list) and data and all(isinstance(row, dict) for row in data):
        return [dict(row) for row in data]

    if not isinstance(data, list) or not data:
        return []

    field_names = []
    if collection.schema:
        field_names = [field.name for field in collection.schema.fields if not field.auto_id]
    if field_names and len(data) == len(field_names) and all(isinstance(column, list) for column in data):
        row_count = len(data[0])
        rows: list[dict[str, Any]] = []
        for i in range(row_count):
            row = {}
            for field_name, column in zip(field_names, data):
                if hasattr(column, "_getrow"):
                    sparse_row = column._getrow(i)
                    if hasattr(sparse_row, "toarray"):
                        row[field_name] = sparse_row.toarray()[0].tolist()
                    else:
                        row[field_name] = sparse_row
                else:
                    row[field_name] = column[i]
            rows.append(row)
        return rows

    if field_names and len(data) == len(field_names):
        row_count = None
        for column in data:
            if isinstance(column, list):
                row_count = len(column)
                break
            if hasattr(column, "shape"):
                row_count = column.shape[0]
                break
        if row_count is not None:
            rows: list[dict[str, Any]] = []
            for i in range(row_count):
                row = {}
                for field_name, column in zip(field_names, data):
                    if hasattr(column, "_getrow"):
                        sparse_row = column._getrow(i)
                        row[field_name] = sparse_row.toarray()[0].tolist() if hasattr(sparse_row, "toarray") else sparse_row
                    elif hasattr(column, "shape") and not isinstance(column, list):
                        row[field_name] = column[i].tolist() if hasattr(column[i], "tolist") else column[i]
                    else:
                        row[field_name] = column[i]
                rows.append(row)
            return rows

    if len(data) == 1 and isinstance(data[0], list) and data[0] and isinstance(data[0][0], dict):
        return [dict(row) for row in data[0]]

    return []


class _BGEM3SparseMatrix:
    """
    功能概述：这个类是 `_BGEM3SparseMatrix`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 matrix，最后把结果交给下一步或直接结束。
    2. `_getrow`：先接收输入参数 index，再调用 self.matrix.getrow 等内部步骤完成主要工作，最后返回结果。
    3. `shape`：先进入当前步骤，最后返回结果。
    """
    def __init__(self, matrix):  # 中文名称：初始化
        self.matrix = matrix

    def _getrow(self, index: int):  # 中文名称：getrow
        return self.matrix.getrow(index)

    @property
    def shape(self):  # 中文名称：shape
        return self.matrix.shape


class BGEM3EmbeddingFunction:
    """
    功能概述：这个类是 `BGEM3EmbeddingFunction`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 use_fp16, device，再调用 TfidfVectorizer 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `dim`：先进入当前步骤，最后返回结果。
    3. `fit_sparse`：先接收输入参数 docs，再调用 self.tfidf_vectorizer.fit 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    4. `__call__`：先接收输入参数 texts，接着根据条件分支选择不同处理路径，再调用 isinstance、np.asarray、self.tfidf_vectorizer.transform 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, use_fp16: bool = False, device: str = "cpu"):  # 中文名称：初始化
        self.use_fp16 = use_fp16
        self.device = device
        self.dense_dim = DEFAULT_EMBED_DIM
        self.tfidf_vectorizer = TfidfVectorizer(max_features=10000)
        self._fitted = False

    @property
    def dim(self):  # 中文名称：dim
        return {"dense": self.dense_dim, "sparse": 10000}

    def fit_sparse(self, docs: list[str]):  # 中文名称：fitsparse
        self.tfidf_vectorizer.fit(docs)
        self._fitted = True

    def __call__(self, texts: str | list[str]):  # 中文名称：可调用执行
        if isinstance(texts, str):
            texts = [texts]
        dense = np.asarray([hash_embed(text, self.dense_dim) for text in texts], dtype=np.float32)
        if not self._fitted:
            self.fit_sparse(texts)
        sparse = self.tfidf_vectorizer.transform(texts)
        return {"dense": dense, "sparse": _BGEM3SparseMatrix(sparse)}


model = ModuleType("pymilvus.model")
hybrid = ModuleType("pymilvus.model.hybrid")
hybrid.BGEM3EmbeddingFunction = BGEM3EmbeddingFunction
model.hybrid = hybrid
sys.modules[__name__ + ".model"] = model
sys.modules[__name__ + ".model.hybrid"] = hybrid
