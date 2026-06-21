"""text_split_example.py

示例：把长文本切分为固定大小的块并支持重叠，常用于 RAG 前处理步骤。
运行：`python3 text_split_example.py`
"""

from typing import List


def sliding_window_split(text: str, chunk_size: int = 200, overlap: int = 50) -> List[str]:
    """使用滑动窗口按字符切分文本，返回切分后的块列表。"""
    # overlap 必须小于 chunk_size，否则窗口不会向前推进。
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    # chunks 用来保存切分后的文本块。
    chunks = []
    # start 表示当前 chunk 的起点下标。
    start = 0
    text_len = len(text)
    while start < text_len:
        # end 是当前 chunk 的终点下标。
        end = start + chunk_size
        # Python 切片 text[start:end] 会取 start 到 end 之前的文本。
        chunk = text[start:end]
        chunks.append(chunk)
        # 如果已经到达文本末尾，就结束循环。
        if end >= text_len:
            break
        # 下一块不是从 end 开始，而是回退 overlap 个字符。
        # 这样可以保留上下文，避免重要句子刚好被切断。
        start = end - overlap
    return chunks


if __name__ == "__main__":
    # 构造一段较长文本，模拟文档内容。
    sample = "这是一个用于演示文本切分的示例文本。" * 20
    # chunk_size=60 表示每块最多 60 个字符。
    # overlap=10 表示相邻两块重叠 10 个字符。
    parts = sliding_window_split(sample, chunk_size=60, overlap=10)
    # 打印切分结果概览。
    print(f"Split into {len(parts)} chunks, first chunk length: {len(parts[0])}")
