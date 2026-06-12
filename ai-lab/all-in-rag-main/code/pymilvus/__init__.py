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
    VARCHAR = "VARCHAR"
    FLOAT_VECTOR = "FLOAT_VECTOR"
    SPARSE_FLOAT_VECTOR = "SPARSE_FLOAT_VECTOR"


DataType = _DataType()


@dataclass
class FieldSchema:
    name: str
    dtype: str
    is_primary: bool = False
    auto_id: bool = False
    max_length: int | None = None
    dim: int | None = None


@dataclass
class CollectionSchema:
    fields: list[FieldSchema]
    description: str = ""


class _IndexParams:
    def __init__(self):
        self.indices: list[dict[str, Any]] = []

    def add_index(self, **kwargs: Any):
        self.indices.append(kwargs)


class connections:
    @staticmethod
    def connect(**kwargs: Any):
        return True


class AnnSearchRequest:
    def __init__(self, data, anns_field, param, limit):
        self.data = data
        self.anns_field = anns_field
        self.param = param
        self.limit = limit


class RRFRanker:
    def __init__(self, k: int = 60):
        self.k = k


class _Hit:
    def __init__(self, entity: dict[str, Any], distance: float):
        self.entity = entity
        self.distance = distance


_GLOBAL_COLLECTIONS: dict[str, dict[str, Any]] = {}


def _cosine_score(query_vec: np.ndarray, doc_vec: np.ndarray) -> float:
    if query_vec.ndim == 1:
        query_vec = query_vec[None, :]
    if doc_vec.ndim == 1:
        doc_vec = doc_vec[None, :]
    q = normalize_vectors(np.asarray(query_vec, dtype=np.float32))[0]
    d = normalize_vectors(np.asarray(doc_vec, dtype=np.float32))[0]
    return float(np.dot(q, d))


def _to_dense(vec):
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


def _passes_expr(entity: dict[str, Any], expr: str | None) -> bool:
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
    def __init__(self, name: str, schema: CollectionSchema | None = None):
        self.name = name
        self.schema = schema
        self.rows: list[dict[str, Any]] = []
        self.indexes: list[dict[str, Any]] = []
        self.loaded = False

    @property
    def num_entities(self) -> int:
        return len(self.rows)


def _ensure_collection(name: str) -> _CollectionState:
    if name not in _GLOBAL_COLLECTIONS:
        _GLOBAL_COLLECTIONS[name] = _CollectionState(name)
    return _GLOBAL_COLLECTIONS[name]


class MilvusClient:
    def __init__(self, uri: str | None = None):
        self.uri = uri

    def has_collection(self, collection_name: str) -> bool:
        return collection_name in _GLOBAL_COLLECTIONS

    def drop_collection(self, collection_name: str):
        _GLOBAL_COLLECTIONS.pop(collection_name, None)

    def create_collection(self, collection_name: str, schema: CollectionSchema, consistency_level: str = "Strong"):
        _GLOBAL_COLLECTIONS[collection_name] = _CollectionState(collection_name, schema=schema)
        return True

    def prepare_index_params(self):
        return _IndexParams()

    def create_index(self, collection_name: str, index_params: Any):
        _ensure_collection(collection_name).indexes.append(index_params)

    def load_collection(self, collection_name: str):
        _ensure_collection(collection_name).loaded = True

    def release_collection(self, collection_name: str):
        _ensure_collection(collection_name).loaded = False

    def insert(self, collection_name: str, data: Any):
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
    ):
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

    def hybrid_search(self, collection_name: str, reqs: list[AnnSearchRequest], rerank: RRFRanker, limit: int, output_fields: list[str] | None = None, **kwargs: Any):
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
    def __init__(self, name: str, schema: CollectionSchema | None = None, consistency_level: str = "Strong"):
        self.name = name
        if schema is not None:
            _GLOBAL_COLLECTIONS[name] = _CollectionState(name, schema=schema)
        _ensure_collection(name)

    @property
    def _state(self) -> _CollectionState:
        return _ensure_collection(self.name)

    @property
    def num_entities(self) -> int:
        return self._state.num_entities

    @property
    def is_empty(self) -> bool:
        return self._state.num_entities == 0

    def create_index(self, field_name: str, index_params: dict[str, Any]):
        self._state.indexes.append({"field": field_name, "params": index_params})

    def insert(self, data: Any):
        rows = _normalize_insert_data(self._state, data)
        self._state.rows.extend(rows)
        return {"insert_count": len(rows)}

    def flush(self):
        return True

    def load(self):
        self._state.loaded = True

    def search(self, *args, **kwargs):
        client = MilvusClient()
        return client.search(self.name, *args, **kwargs)

    def hybrid_search(self, *args, **kwargs):
        client = MilvusClient()
        return client.hybrid_search(self.name, *args, **kwargs)


def _row_key(entity: dict[str, Any]) -> int:
    return abs(hash(json.dumps(entity, sort_keys=True, ensure_ascii=False))) % (10**12)


def _normalize_insert_data(collection: _CollectionState, data: Any) -> list[dict[str, Any]]:
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
    def __init__(self, matrix):
        self.matrix = matrix

    def _getrow(self, index: int):
        return self.matrix.getrow(index)

    @property
    def shape(self):
        return self.matrix.shape


class BGEM3EmbeddingFunction:
    def __init__(self, use_fp16: bool = False, device: str = "cpu"):
        self.use_fp16 = use_fp16
        self.device = device
        self.dense_dim = DEFAULT_EMBED_DIM
        self.tfidf_vectorizer = TfidfVectorizer(max_features=10000)
        self._fitted = False

    @property
    def dim(self):
        return {"dense": self.dense_dim, "sparse": 10000}

    def fit_sparse(self, docs: list[str]):
        self.tfidf_vectorizer.fit(docs)
        self._fitted = True

    def __call__(self, texts: str | list[str]):
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
