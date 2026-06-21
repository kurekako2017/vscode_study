"""dataclass_example.py

示例：使用 dataclass 来定义简单的数据结构并演示序列化。
运行：`python3 dataclass_example.py`
"""

# dataclass 适合定义轻量数据对象。
# 在 RAG 里常用来表示 Document、Chunk、Source 等结构。
from dataclasses import dataclass, asdict
import json


@dataclass
class Document:
    """表示一个简单文档的数据类。

    dataclass 自动生成构造函数、等于比较和可读的 repr，适合轻量数据容器。
    """
    # id: 文档编号，便于检索和追踪。
    id: int
    # title: 文档标题，展示或调试时更容易识别。
    title: str
    # content: 文档正文，RAG 场景里通常会进一步切分成 chunk。
    content: str


def main() -> None:
    """创建 dataclass 实例，并演示属性读取和字典转换。"""
    print("MODEL: provider=local model=none mode=python-dataclass")
    # 创建一个 Document 实例。
    # dataclass 会自动生成 __init__，所以可以直接传字段名。
    doc = Document(id=1, title="示例文档", content="这是一段示例内容。")

    # dataclass 可以方便地转为字典
    # 转成 dict 后，就更容易写入 JSON、返回 API 或交给其他函数处理。
    d = asdict(doc)
    print("as dict:", d)

    # 转为 JSON 字符串以便保存或传输
    # ensure_ascii=False 可以保留中文，不会变成 Unicode 转义。
    print("as json:", json.dumps(d, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    # 入口保护：直接运行文件时执行 main()。
    main()
