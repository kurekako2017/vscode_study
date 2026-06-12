"""
文件功能概述：`code/C2/01_unstructured_example.py` 主要是 01非结构化示例，这个文件里有 0 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 这个文件没有独立类或函数，主要靠模块级代码直接执行。
"""

from pathlib import Path
from collections import Counter


pdf_path = Path(__file__).resolve().parents[2] / "data" / "C2" / "pdf" / "rag.pdf"

try:
    from unstructured.partition.auto import partition

    if pdf_path.exists():
        elements = partition(filename=str(pdf_path), content_type="application/pdf")
    else:
        raise FileNotFoundError(str(pdf_path))
except Exception as exc:
    print(f"警告: 无法使用 unstructured 解析 PDF，改用离线占位文本: {exc}")
    class _Element:
        """
        功能概述：这个类是 `_Element`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
        调用流程：
        1. `__init__`：先接收输入参数 text, category，最后把结果交给下一步或直接结束。
        2. `__str__`：先进入当前步骤，最后返回结果。
        """
        def __init__(self, text, category="NarrativeText"):  # 中文名称：初始化
            self.text = text
            self.category = category

        def __str__(self):  # 中文名称：字符串表示
            return self.text

    sample_text = "RAG 是检索增强生成。它先检索，再生成。"
    elements = [_Element(line) for line in sample_text.split("。") if line]

print(f"解析完成: {len(elements)} 个元素, {sum(len(str(e)) for e in elements)} 字符")
types = Counter(getattr(e, "category", "Unknown") for e in elements)
print(f"元素类型: {dict(types)}")

print("\n所有元素:")
for i, element in enumerate(elements, 1):
    print(f"Element {i} ({getattr(element, 'category', 'Unknown')}):")
    print(element)
    print("=" * 60)
