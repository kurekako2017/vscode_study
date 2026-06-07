"""多 Agent 协作 demo。

这里用纯 Python 模拟：
- Supervisor
- Planner
- Researcher
- Writer
- Critic

重点不是“Agent 数量”，而是“职责拆分”和“状态共享”。
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class TeamState:
    topic: str
    plan: list[str] = field(default_factory=list)
    research_notes: list[str] = field(default_factory=list)
    draft: str = ""
    critique: list[str] = field(default_factory=list)
    final_answer: str = ""
    log: list[str] = field(default_factory=list)


KNOWLEDGE_BASE = {
    "langchain": [
        "LangChain 更偏链式编排和工具集成。",
        "适合把 prompt、工具、模型和输出解析串起来。",
    ],
    "langgraph": [
        "LangGraph 更偏状态图和分支回路控制。",
        "适合复杂 Agent、循环、人工介入和多 Agent 协作。",
    ],
    "llamaindex": [
        "LlamaIndex 更偏文档索引和查询引擎。",
        "适合做知识库检索、节点化查询和引用回答。",
    ],
    "rag": [
        "高级 RAG 需要切分、检索、重排和引用。",
        "Query rewrite 和 multi-query 能提高召回质量。",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="多 Agent 协作 demo")
    parser.add_argument(
        "topic",
        nargs="?",
        default="如何学习 LangGraph 和高级 RAG",
        help="要协作处理的主题",
    )
    return parser.parse_args()


def planner_agent(topic: str) -> list[str]:
    if any(word in topic.lower() for word in ["rag", "检索"]):
        return ["梳理检索目标", "整理检索策略", "给出引用与调优建议"]
    if any(word in topic.lower() for word in ["graph", "workflow", "langgraph"]):
        return ["拆分状态", "定义节点", "设计边与循环"]
    return ["确定主题范围", "收集核心概念", "输出可执行建议"]


def expand_keywords(topic: str) -> Iterable[str]:
    lower = topic.lower()
    for key in KNOWLEDGE_BASE:
        if key in lower or key in topic:
            yield key


def researcher_agent(topic: str, plan: list[str]) -> list[str]:
    notes: list[str] = []
    for keyword in expand_keywords(topic):
        notes.extend(KNOWLEDGE_BASE[keyword])
    if not notes:
        notes = [
            "先明确问题背景。",
            "再给出可执行步骤。",
            "最后补充风险与下一步。",
        ]
    notes.extend([f"执行项：{item}" for item in plan])
    return notes


def writer_agent(topic: str, plan: list[str], research_notes: list[str]) -> str:
    return (
        f"主题：{topic}\n\n"
        "计划：\n- " + "\n- ".join(plan) + "\n\n"
        "研究要点：\n- " + "\n- ".join(research_notes[:6]) + "\n\n"
        "结论：应先把问题拆成小任务，再按职责分配给不同 Agent，最后由 Supervisor 汇总。"
    )


def critic_agent(draft: str) -> list[str]:
    issues = []
    if "风险" not in draft:
        issues.append("缺少风险提示")
    if "步骤" not in draft and "计划" not in draft:
        issues.append("缺少步骤化表达")
    if "结论" not in draft:
        issues.append("缺少最终结论")
    return issues


def supervisor(topic: str) -> TeamState:
    state = TeamState(topic=topic)
    state.log.append("Supervisor: 开始任务")

    state.plan = planner_agent(topic)
    state.log.append(f"Planner: {state.plan}")

    state.research_notes = researcher_agent(topic, state.plan)
    state.log.append(f"Researcher: 收集到 {len(state.research_notes)} 条研究要点")

    state.draft = writer_agent(topic, state.plan, state.research_notes)
    state.log.append("Writer: 生成第一版草稿")

    state.critique = critic_agent(state.draft)
    state.log.append(f"Critic: {state.critique or ['通过']}")

    if state.critique:
        state.research_notes.append("补充：需要显式写出风险、步骤和结论。")
        state.draft = writer_agent(topic, state.plan, state.research_notes)
        state.critique = critic_agent(state.draft)
        state.log.append("Writer: 根据 Critic 反馈修订草稿")
        state.log.append(f"Critic: {state.critique or ['通过']}")

    state.final_answer = (
        state.draft
        + "\n\n"
        + "协作日志：\n- "
        + "\n- ".join(state.log)
        + "\n\n风险提示：多 Agent 适合复杂任务，但角色过多时要注意成本和终止条件。"
    )
    return state


def main() -> None:
    args = parse_args()
    state = supervisor(args.topic)

    print("=== 最终答案 ===")
    print(state.final_answer)


if __name__ == "__main__":
    main()
