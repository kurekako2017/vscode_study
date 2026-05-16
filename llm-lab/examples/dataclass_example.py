"""dataclass_example.py

示例：使用 dataclass 来定义简单的数据结构并演示序列化。
运行：`python dataclass_example.py`
"""

from dataclasses import dataclass, asdict
import json


@dataclass
class Document:
    """表示一个简单文档的数据类。

    dataclass 自动生成构造函数、等于比较和可读的 repr，适合轻量数据容器。
    """
    id: int
    title: str
    content: str


def main() -> None:
    doc = Document(id=1, title="示例文档", content="这是一段示例内容。")

    # dataclass 可以方便地转为字典
    d = asdict(doc)
    print("as dict:", d)

    # 转为 JSON 字符串以便保存或传输
    print("as json:", json.dumps(d, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
