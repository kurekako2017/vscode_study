"""
文件功能概述：`code/C2/04_semantic_chunker.py` 主要是 04语义分块器，这个文件里有 0 个类、1 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 函数 `semantic_split`：先接收输入参数 text，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 chunks.append、sentence.strip、split 等内部步骤完成主要工作，最后返回结果。
"""

from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader


def semantic_split(text: str):  # 中文名称：语义切分
    sentences = [sentence.strip() for sentence in text.replace("\n", " ").split("。") if sentence.strip()]
    if not sentences:
        return [text]
    chunks = []
    current = sentences[0]
    for sentence in sentences[1:]:
        if len(current) + len(sentence) < 120:
            current += "。" + sentence
        else:
            chunks.append(current)
            current = sentence
    chunks.append(current)
    return chunks


source = Path(__file__).resolve().parents[2] / "data" / "C2" / "txt" / "蜂医.txt"
if source.exists():
    documents = TextLoader(str(source), encoding="utf-8").load()
else:
    documents = [Document(page_content="蜂医是一篇示例文本，用于演示语义分块。相似含义的句子会被放在一起。")]

docs = []
for document in documents:
    for chunk in semantic_split(document.page_content):
        docs.append(Document(page_content=chunk, metadata=dict(document.metadata)))

print(f"文本被切分为 {len(docs)} 个块。\n")
print("--- 前2个块内容示例 ---")
for i, chunk in enumerate(docs[:2]):
    print("=" * 60)
    print(f'块 {i+1} (长度: {len(chunk.page_content)}):\n"{chunk.page_content}"')
