"""高级 RAG 标准模式的离线、可比较实现。"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Child:
    """用于检索的小片段，同时保留其父文档 id。"""
    parent_id: str
    text: str

#   父文档集合
PARENTS = {
    "p1": "差旅规定：新干线费用可报销。超过三万日元必须由部门经理审批。申请单需附发票。",
    "p2": "远程办公：每周最多三天。海外远程办公需要信息安全部门事前审批。",
    "p3": "RAG 运维：回答必须附来源。低相关结果应触发查询改写或转人工处理。",
}


def tokens(text: str) -> set[str]:
    """把英文按单词、中文按二元字符切成集合，供离线相似度比较。"""
    lowered = text.lower()
    result = set(re.findall(r"[a-z0-9]+", lowered))
    for block in re.findall(r"[\u4e00-\u9fff]+", lowered):
        result.update(block[index:index + 2] for index in range(max(1, len(block) - 1)))
    return result


def children() -> list[Child]:
    """把每篇父文档按句号拆成 child chunk。"""
    result: list[Child] = []
    for pid, parent in PARENTS.items():
        result.extend(Child(pid, sentence) for sentence in parent.split("。") if sentence)
    return result


def hyde(query: str) -> str:
    """构造假设答案；真实 HyDE 通常由 LLM 生成，本例只用固定模板。"""
    return f"与问题相关的制度答案可能包含审批、费用、权限、来源等条件：{query}"

# 这个函数模拟了一个非常基础的 RAG 检索和纠正流程，适合教学和对比实验。
def retrieve(query: str, use_hyde: bool = True) -> list[tuple[Child, float]]:
    """按 token 交集数给 child chunk 排序，分数越高表示重叠越多。"""
    query_tokens = tokens(query + (" " + hyde(query) if use_hyde else ""))
    ranked = [(child, len(query_tokens & tokens(child.text))) for child in children()]
    return sorted(ranked, key=lambda item: item[1], reverse=True)

#   
def compress(query: str, text: str) -> str:
    """只保留父文档中与问题有词语交集的句子，模拟上下文压缩。"""
    q = tokens(query)
    sentences = [s for s in text.split("。") if q & tokens(s)]
    return "。".join(sentences) + ("。" if sentences else "")


def corrective_rag(query: str) -> dict:
    """低相关时走 fallback；有证据时回查父文档并生成带来源结果。"""
    ranked = retrieve(query)
    best, score = ranked[0]
    baseline_score = retrieve(query, use_hyde=False)[0][1]
    # 不用 HyDE 也完全无命中时，模板扩展得到的命中不应被当成可靠证据。
    if baseline_score == 0:
        return {"route": "fallback", "answer": "知识库证据不足，转人工或外部检索。", "sources": []}
    parent = PARENTS[best.parent_id]
    context = compress(query, parent) or parent
    return {
        "route": "answer",
        "answer": context,
        "sources": [best.parent_id],
        "retrieved_child": best.text,
        "score": score,
        "baseline_score": baseline_score,
    }


def main() -> None:
    """选择标准 CRAG 流程或无 HyDE 基线，并打印便于比较的结果。"""
    print("MODEL: provider=local model=none mode=local-rag")
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", default="新干线超过三万日元怎么审批")
    parser.add_argument("--baseline", action="store_true", help="关闭 HyDE")
    args = parser.parse_args()
    result = corrective_rag(args.query) if not args.baseline else retrieve(args.query, False)[0]
    print(result)


if __name__ == "__main__":
    main()
