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
    # 当前主题。
    topic: str
    # 规划出来的任务列表。
    plan: list[str] = field(default_factory=list)
    # 调研笔记。
    research_notes: list[str] = field(default_factory=list)
    # 草稿文本。
    draft: str = ""
    # 批评/审核意见。
    critique: list[str] = field(default_factory=list)
    # 最终答案。
    final_answer: str = ""
    # 协作日志。
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


# 解析主题输入，作为整个协作流程的起点。
def parse_args() -> argparse.Namespace:
    # 创建命令行解析器。
    parser = argparse.ArgumentParser(description="多 Agent 协作 demo")
    # 主题参数。
    parser.add_argument(
        "topic",
        nargs="?",
        default="如何学习 LangGraph 和高级 RAG",
        help="要协作处理的主题",
    )
    # 返回解析结果。
    return parser.parse_args()


# 规划者把大主题拆成可执行任务。
def planner_agent(topic: str) -> list[str]:
    # planner 负责把大主题拆成更小的任务。
    if any(word in topic.lower() for word in ["rag", "检索"]):
        return ["梳理检索目标", "整理检索策略", "给出引用与调优建议"]
    if any(word in topic.lower() for word in ["graph", "workflow", "langgraph"]):
        return ["拆分状态", "定义节点", "设计边与循环"]
    return ["确定主题范围", "收集核心概念", "输出可执行建议"]


# 从主题里挑出可映射到知识库的关键词。
def expand_keywords(topic: str) -> Iterable[str]:
    # 根据主题从知识库里挑关键字。
    lower = topic.lower()
    for key in KNOWLEDGE_BASE:
        if key in lower or key in topic:
            yield key


# 调研者根据主题和计划收集知识要点。
def researcher_agent(topic: str, plan: list[str]) -> list[str]:
    # 调研结果。
    notes: list[str] = []
    # 把知识库里对应主题的知识补进来。
    for keyword in expand_keywords(topic):
        notes.extend(KNOWLEDGE_BASE[keyword])
    # 如果没有命中知识库，就使用通用模板。
    if not notes:
        notes = [
            "先明确问题背景。",
            "再给出可执行步骤。",
            "最后补充风险与下一步。",
        ]
    # 把 plan 里的任务也转换成 notes。
    notes.extend([f"执行项：{item}" for item in plan])
    # 返回调研笔记。
    return notes


# 写作者把计划和调研结果组织成草稿。
def writer_agent(topic: str, plan: list[str], research_notes: list[str]) -> str:
    # writer 负责把信息组织成可读内容。
    return (
        f"主题：{topic}\n\n"
        "计划：\n- " + "\n- ".join(plan) + "\n\n"
        "研究要点：\n- " + "\n- ".join(research_notes[:6]) + "\n\n"
        "结论：应先把问题拆成小任务，再按职责分配给不同 Agent，最后由 Supervisor 汇总。"
    )


# 审校者检查草稿缺少什么内容。
def critic_agent(draft: str) -> list[str]:
    # critic 负责找缺点。
    issues = []
    # 缺少风险就是一个常见问题。
    if "风险" not in draft:
        issues.append("缺少风险提示")
    # 没有步骤化表达也要提醒。
    if "步骤" not in draft and "计划" not in draft:
        issues.append("缺少步骤化表达")
    # 没有结论就不完整。
    if "结论" not in draft:
        issues.append("缺少最终结论")
    # 返回问题列表。
    return issues


# 监督者串联各个 Agent，并维护共享状态。
def supervisor(topic: str) -> TeamState:
    # 创建一个共享状态对象。
    state = TeamState(topic=topic)
    # 记录流程日志。
    state.log.append("Supervisor: 开始任务")

    # 先让 planner 产出计划。
    state.plan = planner_agent(topic)
    state.log.append(f"Planner: {state.plan}")

    # 再让 researcher 基于 plan 收集知识。
    state.research_notes = researcher_agent(topic, state.plan)
    state.log.append(f"Researcher: 收集到 {len(state.research_notes)} 条研究要点")

    # writer 生成第一版草稿。
    state.draft = writer_agent(topic, state.plan, state.research_notes)
    state.log.append("Writer: 生成第一版草稿")

    # critic 检查草稿是否完整。
    state.critique = critic_agent(state.draft)
    state.log.append(f"Critic: {state.critique or ['通过']}")

    # 如果有问题，就进入第二轮修订。
    if state.critique:
        # 补充一条说明，告诉 writer 应该补风险等内容。
        state.research_notes.append("补充：需要显式写出风险、步骤和结论。")
        state.draft = writer_agent(topic, state.plan, state.research_notes)
        state.critique = critic_agent(state.draft)
        state.log.append("Writer: 根据 Critic 反馈修订草稿")
        state.log.append(f"Critic: {state.critique or ['通过']}")

    # 拼成最终答案。
    state.final_answer = (
        state.draft
        + "\n\n"
        + "协作日志：\n- "
        + "\n- ".join(state.log)
        + "\n\n风险提示：多 Agent 适合复杂任务，但角色过多时要注意成本和终止条件。"
    )
    # 返回整个状态。
    return state


# 程序入口，执行监督者协作流程并输出最终答案。
def main() -> None:
    print("MODEL: provider=local model=none mode=multi-agent-simulation")
    # 读取参数。
    args = parse_args()
    # 运行监督者流程。
    state = supervisor(args.topic)

    # 打印最终答案。
    print("=== 最终答案 ===")
    print(state.final_answer)


if __name__ == "__main__":
    main()
