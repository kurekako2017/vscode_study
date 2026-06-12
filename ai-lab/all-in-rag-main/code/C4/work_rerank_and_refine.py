from __future__ import annotations

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.document_loaders import TextLoader
from pathlib import Path


def simple_rerank(query: str, docs: list[Document], top_k: int = 5):
    query_terms = set(query.lower().split())
    scored = []
    for doc in docs:
        score = len(query_terms & set(doc.page_content.lower().split()))
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


source = Path(__file__).resolve().parents[2] / "data" / "C4" / "txt" / "ai.txt"
if source.exists():
    documents = TextLoader(str(source), encoding="utf-8").load()
else:
    documents = [Document(page_content="AI 正在改变世界，但仍面临幻觉、偏见、成本和可靠性问题。")]

text_splitter = []
for document in documents:
    text = document.page_content
    for start in range(0, len(text), 500):
        text_splitter.append(Document(page_content=text[start:start + 500], metadata=dict(document.metadata)))

hf_bge_embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-large-zh-v1.5")
vectorstore = FAISS.from_documents(text_splitter, hf_bge_embeddings)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})

query = "AI还有哪些缺陷需要克服？"
print(f"\n{'='*20} 开始执行查询 {'='*20}")
print(f"查询: {query}\n")

print(f"--- (1) 基础检索结果 (Top 20) ---")
base_results = base_retriever.get_relevant_documents(query)
for i, doc in enumerate(base_results):
    print(f"  [{i+1}] {doc.page_content[:100]}...\n")

print(f"\n--- (2) 重排后结果 ---")
final_results = simple_rerank(query, base_results, top_k=5)
for i, doc in enumerate(final_results):
    print(f"  [{i+1}] {doc.page_content}\n")
