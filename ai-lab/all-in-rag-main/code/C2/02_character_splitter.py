from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader


def character_split(text: str, chunk_size: int = 200, chunk_overlap: int = 10):
    step = max(1, chunk_size - chunk_overlap)
    return [text[i : i + chunk_size] for i in range(0, len(text), step)]


source = Path(__file__).resolve().parents[2] / "data" / "C2" / "txt" / "蜂医.txt"
if source.exists():
    docs = TextLoader(str(source), encoding="utf-8").load()
else:
    docs = [Document(page_content="蜂医是一篇示例文本，用于演示字符切分。RAG 会把长文本拆成多个块。")]

chunks = []
for doc in docs:
    for chunk in character_split(doc.page_content):
        chunks.append(Document(page_content=chunk, metadata=dict(doc.metadata)))

print(f"文本被切分为 {len(chunks)} 个块。\n")
print("--- 前5个块内容示例 ---")
for i, chunk in enumerate(chunks[:5]):
    print("=" * 60)
    print(f'块 {i+1} (长度: {len(chunk.page_content)}): "{chunk.page_content}"')
