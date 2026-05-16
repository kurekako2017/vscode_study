"""text_split_example.py

示例：把长文本切分为固定大小的块并支持重叠，常用于 RAG 前处理步骤。
运行：`python text_split_example.py`
"""

from typing import List


def sliding_window_split(text: str, chunk_size: int = 200, overlap: int = 50) -> List[str]:
    """使用滑动窗口按字符切分文本，返回切分后的块列表。"""
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        if end >= text_len:
            break
        start = end - overlap
    return chunks


if __name__ == "__main__":
    sample = "这是一个用于演示文本切分的示例文本。" * 20
    parts = sliding_window_split(sample, chunk_size=60, overlap=10)
    print(f"Split into {len(parts)} chunks, first chunk length: {len(parts[0])}")
