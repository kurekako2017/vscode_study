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
        def __init__(self, text, category="NarrativeText"):
            self.text = text
            self.category = category

        def __str__(self):
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
