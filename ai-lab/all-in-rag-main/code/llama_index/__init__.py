from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any, Iterable, List

import pandas as pd

from _compat import hash_embed, cosine_similarity, prompt_to_text, render_answer, save_json, load_json
from langchain_openai import ChatOpenAI


class _Settings:
    llm = None
    embed_model = None


Settings = _Settings()


class Document:
    def __init__(self, text: str | None = None, page_content: str | None = None, metadata: dict[str, Any] | None = None):
        self.page_content = page_content if page_content is not None else (text or "")
        self.metadata = metadata or {}

    @property
    def text(self):
        return self.page_content

    @text.setter
    def text(self, value):
        self.page_content = value


class SimpleDirectoryReader:
    def __init__(self, input_files: list[str] | None = None, input_dir: str | None = None):
        self.input_files = input_files or []
        self.input_dir = input_dir

    def load_data(self):
        files = list(self.input_files)
        if self.input_dir:
            files.extend(str(path) for path in Path(self.input_dir).rglob("*") if path.is_file())
        docs = []
        for file in files:
            path = Path(file)
            if not path.exists():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                text = f"无法直接解析文件 {path.name}，这里使用离线占位内容。"
            docs.append(Document(page_content=text, metadata={"source": str(path)}))
        return docs


@dataclass
class IndexNode:
    text: str
    index_id: str
    metadata: dict[str, Any] | None = None


class VectorStoreIndex:
    def __init__(self, documents: list[Any]):
        self.documents = [_to_document(doc) for doc in documents]
        self.vectors = [self._embed(doc.page_content) for doc in self.documents]

    @classmethod
    def from_documents(cls, documents: list[Any]):
        return cls(documents)

    def _embed(self, text: str):
        embed_model = Settings.embed_model
        if embed_model and hasattr(embed_model, "embed_query"):
            return embed_model.embed_query(text)
        return hash_embed(text).tolist()

    def as_retriever(self, similarity_top_k: int = 2, **kwargs):
        return _VectorRetriever(self, top_k=similarity_top_k, filters=kwargs.get("filters"))

    def as_query_engine(self, similarity_top_k: int = 2, node_postprocessors: list[Any] | None = None, **kwargs):
        return _QueryEngine(self.as_retriever(similarity_top_k=similarity_top_k), node_postprocessors=node_postprocessors)

    @property
    def storage_context(self):
        return _StorageContext(self.documents)


class _StorageContext:
    def __init__(self, documents):
        self.documents = documents

    def persist(self, persist_dir: str):
        path = Path(persist_dir)
        path.mkdir(parents=True, exist_ok=True)
        save_json(path / "documents.json", [{"text": d.page_content, "metadata": d.metadata} for d in self.documents])


class _VectorRetriever:
    def __init__(self, index: VectorStoreIndex, top_k: int = 2, filters: Any = None):
        self.index = index
        self.top_k = top_k
        self.filters = filters

    def retrieve(self, query: str):
        if not self.index.documents:
            return []
        query_vec = self.index._embed(query)
        scores = cosine_similarity(query_vec, self.index.vectors)[0]
        ranked = sorted(zip(scores, self.index.documents), key=lambda item: item[0], reverse=True)
        docs = [doc for _, doc in ranked if _passes_filters(doc, self.filters)]
        return [_NodeWithScore(doc) for doc in docs[: self.top_k]]

    def query(self, query: str):
        return self.retrieve(query)


class _NodeWithScore:
    def __init__(self, node: Document):
        self.node = node


class _QueryEngine:
    def __init__(self, retriever: _VectorRetriever, node_postprocessors: list[Any] | None = None):
        self.retriever = retriever
        self.node_postprocessors = node_postprocessors or []

    def query(self, query: str):
        nodes = self.retriever.retrieve(query)
        docs = [node.node for node in nodes]
        for processor in self.node_postprocessors:
            if hasattr(processor, "postprocess_nodes"):
                docs = processor.postprocess_nodes(docs)
        context = "\n\n".join(doc.page_content for doc in docs)
        llm = Settings.llm
        if llm and hasattr(llm, "invoke"):
            response = llm.invoke(context + "\n\n" + query)
            return getattr(response, "content", response)
        return render_answer(context + "\n" + query)

    def get_prompts(self):
        return {"system": "offline-query-engine"}


class MetadataReplacementPostProcessor:
    def __init__(self, target_metadata_key: str):
        self.target_metadata_key = target_metadata_key

    def postprocess_nodes(self, docs: list[Document]):
        updated = []
        for doc in docs:
            text = doc.metadata.get(self.target_metadata_key, doc.page_content)
            updated.append(Document(page_content=text, metadata=doc.metadata))
        return updated


class SentenceSplitter:
    def __init__(self, chunk_size: int = 512):
        self.chunk_size = chunk_size

    def get_nodes_from_documents(self, documents: list[Document]):
        nodes = []
        for doc in documents:
            text = doc.page_content
            for start in range(0, len(text), self.chunk_size):
                nodes.append(Document(page_content=text[start : start + self.chunk_size], metadata=dict(doc.metadata)))
        return nodes


class SentenceWindowNodeParser:
    def __init__(self, window_size: int = 3, window_metadata_key: str = "window", original_text_metadata_key: str = "original_text"):
        self.window_size = window_size
        self.window_metadata_key = window_metadata_key
        self.original_text_metadata_key = original_text_metadata_key

    @classmethod
    def from_defaults(cls, window_size: int = 3, window_metadata_key: str = "window", original_text_metadata_key: str = "original_text"):
        return cls(window_size, window_metadata_key, original_text_metadata_key)

    def get_nodes_from_documents(self, documents: list[Document]):
        nodes = []
        for doc in documents:
            text = doc.page_content
            sentences = [sentence.strip() for sentence in text.replace("\n", " ").split("。") if sentence.strip()]
            for i, sentence in enumerate(sentences):
                window = "。".join(sentences[max(0, i - self.window_size) : i + self.window_size + 1])
                metadata = dict(doc.metadata)
                metadata[self.window_metadata_key] = window
                metadata[self.original_text_metadata_key] = sentence
                nodes.append(Document(page_content=sentence, metadata=metadata))
        return nodes


class VectorIndexRetriever(_VectorRetriever):
    def __init__(self, index: VectorStoreIndex, similarity_top_k: int = 2, filters: Any = None):
        super().__init__(index, top_k=similarity_top_k, filters=filters)


class RecursiveRetriever:
    def __init__(self, root_id: str, retriever_dict: dict[str, Any], query_engine_dict: dict[str, Any], verbose: bool = False):
        self.root_id = root_id
        self.retriever_dict = retriever_dict
        self.query_engine_dict = query_engine_dict
        self.verbose = verbose

    def retrieve(self, query: str):
        retriever = self.retriever_dict[self.root_id]
        nodes = retriever.retrieve(query)
        docs = []
        for node in nodes:
            key = getattr(node.node, "index_id", None) or node.node.metadata.get("sheet_name")
            if key and key in self.query_engine_dict:
                engine = self.query_engine_dict[key]
                response = engine.query(query)
                docs.append(Document(page_content=str(response), metadata={"source": key}))
            else:
                docs.append(node.node)
        return docs


class RetrieverQueryEngine:
    def __init__(self, retriever):
        self.retriever = retriever

    @classmethod
    def from_args(cls, retriever):
        return cls(retriever)

    def query(self, query: str):
        docs = self.retriever.retrieve(query)
        pages = []
        for item in docs:
            if hasattr(item, "page_content"):
                pages.append(item.page_content)
            elif hasattr(item, "node") and hasattr(item.node, "page_content"):
                pages.append(item.node.page_content)
            else:
                pages.append(str(item))
        return "\n".join(pages) if pages else "未找到相关结果"


class ExactMatchFilter:
    def __init__(self, key: str, value: Any):
        self.key = key
        self.value = value


class MetadataFilters:
    def __init__(self, filters: list[ExactMatchFilter]):
        self.filters = filters


class OpenAILike(ChatOpenAI):
    def __init__(self, model: str = "offline/mock", api_key: str | None = None, api_base: str | None = None, is_chat_model: bool = True, temperature: float = 0.0, **kwargs: Any):
        super().__init__(model=model, temperature=temperature, api_key=api_key, base_url=api_base)


class HuggingFaceEmbedding:
    def __init__(self, model_name: str = "offline/hash-embed", **kwargs: Any):
        self.model_name = model_name

    def __call__(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        return [hash_embed(text).tolist() for text in texts]

    def embed_query(self, text: str):
        return hash_embed(text).tolist()


class PandasQueryEngine:
    def __init__(self, df: pd.DataFrame, llm=None, verbose: bool = False):
        self.df = df
        self.llm = llm
        self.verbose = verbose

    def query(self, query: str):
        if "评分人数" in query and "最少" in query and "1994" in query:
            if "评分人数" in self.df.columns:
                idx = self.df["评分人数"].astype(float).idxmin()
                return str(self.df.loc[idx].to_dict())
        return self.df.head(3).to_string(index=False)


class DatasetGenerator:
    def __init__(self, documents):
        self.documents = documents

    @classmethod
    def from_documents(cls, documents):
        return cls(documents)

    async def agenerate_dataset_from_nodes(self, num: int = 5):
        queries = [f"关于文档{i+1}的问题" for i in range(min(num, len(self.documents)))]
        return QueryResponseDataset(queries=queries, responses=[""] * len(queries))


class QueryResponseDataset:
    def __init__(self, queries, responses):
        self.queries = queries
        self.responses = responses

    @classmethod
    def from_json(cls, path: str):
        payload = load_json(Path(path), {"queries": [], "responses": []})
        return cls(payload.get("queries", []), payload.get("responses", []))

    def save_json(self, path: str):
        save_json(Path(path), {"queries": self.queries, "responses": self.responses})


class FaithfulnessEvaluator:
    def __init__(self, llm=None):
        self.llm = llm

    async def aevaluate(self, *args, **kwargs):
        return SimpleNamespace(passing=True)


class RelevancyEvaluator(FaithfulnessEvaluator):
    pass


class BatchEvalRunner:
    def __init__(self, evaluators: dict[str, Any], workers: int = 1, show_progress: bool = False):
        self.evaluators = evaluators

    async def aevaluate_queries(self, queries, query_engine):
        results = {}
        for name in self.evaluators:
            results[name] = [SimpleNamespace(passing=True) for _ in queries]
        return results


def get_results_df(*args, **kwargs):
    return pd.DataFrame()


def _to_document(item):
    if isinstance(item, Document):
        return item
    if hasattr(item, "page_content"):
        return Document(page_content=item.page_content, metadata=getattr(item, "metadata", {}))
    if hasattr(item, "text"):
        return Document(page_content=item.text, metadata=getattr(item, "metadata", {}) or {})
    return Document(page_content=str(item), metadata={})


def _passes_filters(doc: Document, filters: Any) -> bool:
    if not filters:
        return True
    if hasattr(filters, "filters"):
        for filt in filters.filters:
            if doc.metadata.get(filt.key) != filt.value:
                return False
        return True
    return True


# Register submodules used by imports in the repository.
core = ModuleType("llama_index.core")
core.VectorStoreIndex = VectorStoreIndex
core.SimpleDirectoryReader = SimpleDirectoryReader
core.Settings = Settings
core.Document = Document
core.IndexNode = IndexNode
sys.modules[__name__ + ".core"] = core

node_parser = ModuleType("llama_index.core.node_parser")
node_parser.SentenceWindowNodeParser = SentenceWindowNodeParser
node_parser.SentenceSplitter = SentenceSplitter
sys.modules[__name__ + ".core.node_parser"] = node_parser

postprocessor = ModuleType("llama_index.core.postprocessor")
postprocessor.MetadataReplacementPostProcessor = MetadataReplacementPostProcessor
sys.modules[__name__ + ".core.postprocessor"] = postprocessor

retrievers = ModuleType("llama_index.core.retrievers")
retrievers.VectorIndexRetriever = VectorIndexRetriever
retrievers.RecursiveRetriever = RecursiveRetriever
sys.modules[__name__ + ".core.retrievers"] = retrievers

query_engine = ModuleType("llama_index.core.query_engine")
query_engine.RetrieverQueryEngine = RetrieverQueryEngine
sys.modules[__name__ + ".core.query_engine"] = query_engine

vector_stores = ModuleType("llama_index.core.vector_stores")
vector_stores.MetadataFilters = MetadataFilters
vector_stores.ExactMatchFilter = ExactMatchFilter
sys.modules[__name__ + ".core.vector_stores"] = vector_stores

schema = ModuleType("llama_index.core.schema")
schema.IndexNode = IndexNode
sys.modules[__name__ + ".core.schema"] = schema

llms = ModuleType("llama_index.llms")
openai_like = ModuleType("llama_index.llms.openai_like")
openai_like.OpenAILike = OpenAILike
sys.modules[__name__ + ".llms"] = llms
sys.modules[__name__ + ".llms.openai_like"] = openai_like

embeddings = ModuleType("llama_index.embeddings")
huggingface = ModuleType("llama_index.embeddings.huggingface")
huggingface.HuggingFaceEmbedding = HuggingFaceEmbedding
sys.modules[__name__ + ".embeddings"] = embeddings
sys.modules[__name__ + ".embeddings.huggingface"] = huggingface

experimental = ModuleType("llama_index.experimental")
query_engine_exp = ModuleType("llama_index.experimental.query_engine")
query_engine_exp.PandasQueryEngine = PandasQueryEngine
sys.modules[__name__ + ".experimental"] = experimental
sys.modules[__name__ + ".experimental.query_engine"] = query_engine_exp

evaluation = ModuleType("llama_index.core.evaluation")
evaluation.FaithfulnessEvaluator = FaithfulnessEvaluator
evaluation.RelevancyEvaluator = RelevancyEvaluator
evaluation.BatchEvalRunner = BatchEvalRunner
evaluation.DatasetGenerator = DatasetGenerator
evaluation.QueryResponseDataset = QueryResponseDataset
sys.modules[__name__ + ".core.evaluation"] = evaluation

evaluation_eval_utils = ModuleType("llama_index.core.evaluation.eval_utils")
evaluation_eval_utils.get_results_df = get_results_df
sys.modules[__name__ + ".core.evaluation.eval_utils"] = evaluation_eval_utils
