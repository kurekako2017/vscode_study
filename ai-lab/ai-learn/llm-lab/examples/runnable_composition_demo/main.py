"""LCEL Runnable 组合模式：Parallel、Branch、Passthrough、batch、stream。"""
from __future__ import annotations

import argparse
from operator import itemgetter

from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)


def classify(data: dict) -> str:
    """根据问题关键词返回简单意图；这是本地规则，不是模型分类。"""
    text = data["question"].lower()
    return "rag" if "rag" in text or "检索" in text else "agent"


def build_chain():
    """构建 enrich -> parallel -> route 三段 LCEL 链。"""
    # assign 保留原字典，同时追加 intent 和 length 两个字段。
    enrich = RunnablePassthrough.assign(
        intent=RunnableLambda(classify),
        length=RunnableLambda(lambda x: len(x["question"])),
    )
    parallel = RunnableParallel(
        # Parallel 对同一份输入同时计算三个输出，并汇总成新字典。
        original=itemgetter("question"),
        intent=itemgetter("intent"),
        facts=RunnableLambda(
            lambda x: ["检索、重排、引用"] if x["intent"] == "rag" else ["状态、工具、边界"]
        ),
    )
    route = RunnableBranch(
        # Branch 检查 intent：命中第一个条件走 RAG，否则走默认 Agent 分支。
        (lambda x: x["intent"] == "rag", lambda x: f"RAG 路线：{' → '.join(x['facts'])}"),
        lambda x: f"Agent 路线：{' → '.join(x['facts'])}",
    )
    return enrich | parallel | route


def main() -> None:
    """批量执行多个问题，或用 --stream 演示单个结果的流式迭代接口。"""
    print("MODEL: provider=local model=none mode=runnable-demo")
    parser = argparse.ArgumentParser()
    parser.add_argument("questions", nargs="*", default=["高级 RAG 怎么设计", "Agent 如何控制工具"])
    parser.add_argument("--stream", action="store_true")
    args = parser.parse_args()
    chain = build_chain()
    inputs = [{"question": q} for q in args.questions]
    if args.stream:
        # 本地字符串通常只产生一个 chunk，但调用方式与真实流式 Runnable 一致。
        for chunk in chain.stream(inputs[0]):
            print(chunk, end="", flush=True)
        print()
    else:
        for answer in chain.batch(inputs):
            print(answer)


if __name__ == "__main__":
    main()
