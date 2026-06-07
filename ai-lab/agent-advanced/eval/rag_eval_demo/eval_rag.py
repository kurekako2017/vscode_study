"""最小 RAG 评估脚本。

这个脚本不追求学术级指标，只做最基础的：
- coverage：命中的参考来源比例
- precision：召回结果里有多少是真的相关

适合先把评估闭环跑起来。
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
# 样本文件路径。
SAMPLES_PATH = BASE_DIR / "samples.json"


@dataclass
class Sample:
    # 用户问题。
    question: str
    # 标准答案对应的来源列表。
    gold_sources: list[str]
    # 检索返回的来源列表。
    retrieved_sources: list[str]
    # 这条样本的答案文本。
    answer: str


def load_samples() -> list[Sample]:
    # 读取 JSON 原始内容。
    raw = json.loads(SAMPLES_PATH.read_text(encoding="utf-8"))
    # 把字典列表转成 Sample 对象列表。
    return [Sample(**item) for item in raw]


def coverage(gold_sources: list[str], retrieved_sources: list[str]) -> float:
    # 没有 gold 时，按 100% 处理，避免除零。
    if not gold_sources:
        return 1.0
    # 计算交集。
    matched = set(gold_sources) & set(retrieved_sources)
    # 覆盖率 = 命中的 gold 数 / gold 总数。
    return len(matched) / len(set(gold_sources))


def precision(gold_sources: list[str], retrieved_sources: list[str]) -> float:
    # 没有召回结果时，precision 记为 0。
    if not retrieved_sources:
        return 0.0
    # 计算交集。
    matched = set(gold_sources) & set(retrieved_sources)
    # 精确率 = 命中的结果数 / 结果总数。
    return len(matched) / len(set(retrieved_sources))


def main() -> None:
    # 加载所有样本。
    samples = load_samples()
    # 累计覆盖率。
    overall_coverage = 0.0
    # 累计精确率。
    overall_precision = 0.0

    # 打印报表标题。
    print("=== RAG Eval Report ===")
    # 逐条样本评估。
    for idx, sample in enumerate(samples, start=1):
        # 计算单条样本的 coverage。
        sample_coverage = coverage(sample.gold_sources, sample.retrieved_sources)
        # 计算单条样本的 precision。
        sample_precision = precision(sample.gold_sources, sample.retrieved_sources)
        # 累加。
        overall_coverage += sample_coverage
        overall_precision += sample_precision

        # 打印样本详情。
        print(f"\n[{idx}] {sample.question}")
        print(f"- gold: {sample.gold_sources}")
        print(f"- retrieved: {sample.retrieved_sources}")
        print(f"- coverage: {sample_coverage:.2f}")
        print(f"- precision: {sample_precision:.2f}")
        print(f"- answer: {sample.answer}")

    # 防止样本数为 0 时除零。
    count = len(samples) or 1
    # 打印汇总信息。
    print("\n=== Summary ===")
    print(f"- avg coverage: {overall_coverage / count:.2f}")
    print(f"- avg precision: {overall_precision / count:.2f}")
    print("- 这个脚本的作用不是做严格学术评估，而是先把社内 RAG 的反馈闭环跑起来。")


if __name__ == "__main__":
    main()
