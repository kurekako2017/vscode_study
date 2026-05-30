"""structured_output_demo: 演示如何让模型返回结构化数据并用 Pydantic 验证。

该示例展示：
- 使用 Pydantic 定义输出 schema（`AgentPlan`）作为 contract
- 用 Responses API 的 `parse` 将模型输出解析并验证为 Pydantic 模型

对下游系统而言，稳定的 schema 能显著降低解析错误和生产风险。

学习地图：
- 运行命令：
    - python3 main.py "做一个客服 Agent 的开发计划"
    - python3 main.py "给我一个 RAG 学习路线" --model gpt-4o
- 输入输出：
    - 输入：自然语言需求 prompt
    - 输出：通过 Pydantic 校验后的 AgentPlan JSON
- 改造练习点：
    - 在 AgentPlan 中新增 timeline 字段并更新提示词
    - 对 user_type 增加默认值与兜底策略
    - 将结果保存到本地 JSON 文件
"""

import argparse
import json
import os
import sys
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel, Field


DEFAULT_MODEL = "gpt-4o"
SYSTEM_INSTRUCTIONS = (
    "You are an assistant for an LLM agent learning lab. "
    "Analyze the user's idea and return a structured development plan."
)


class AgentPlan(BaseModel):
    """Pydantic 模型：定义期望的结构化输出字段与类型。

    当将模型输出解析到该类型时，若字段缺失或类型不匹配，SDK 会抛出错误，便于及早发现问题。
    """
    goal: str = Field(description="The main goal of the requested agent.")
    user_type: Literal["beginner", "intermediate", "advanced"] = Field(
        description="Estimated user level for this project."
    )
    core_capabilities: list[str] = Field(
        description="Key capabilities the agent should have."
    )
    tools: list[str] = Field(description="Recommended tools or functions.")
    deliverables: list[str] = Field(
        description="Concrete output artifacts or demos to build."
    )
    risks: list[str] = Field(description="Main development risks or cautions.")


def parse_args() -> argparse.Namespace:
    # 层次: 输入层 — 解析用户的自然语言请求与模型选项
    """解析命令行参数：接收自然语言请求并可选择模型。"""
    parser = argparse.ArgumentParser(
        description="Minimal structured output demo with OpenAI Responses API."
    )
    parser.add_argument("prompt", help="Natural-language project request.")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model name to use. Default: {DEFAULT_MODEL}",
    )
    return parser.parse_args()


def build_client() -> OpenAI:
    # 层次: 基础设施层 — 构建 OpenAI 客户端并处理缺失情况
    """创建 OpenAI 客户端，要求通过环境变量提供 `OPENAI_API_KEY`。"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key)


def generate_plan(client: OpenAI, model: str, prompt: str) -> AgentPlan:
    # 层次: 调用层 — 请求模型并使用 SDK 的 parse 功能将输出映射为 `AgentPlan`
    """调用 Responses API 的 `parse` 功能，直接将输出解析为 `AgentPlan`。

    `text_format=AgentPlan` 告知 SDK 使用 Pydantic 验证模型输出结构。
    """
    response = client.responses.parse(
        model=model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=prompt,
        text_format=AgentPlan,
    )
    return response.output_parsed


def main() -> None:
    # 层次: 程序入口 — 读取参数、调用构建流程并展示结果
    """主流程：读取参数 -> 请求结构化输出 -> 打印可读 JSON。"""
    args = parse_args()
    client = build_client()

    try:
        plan = generate_plan(client, args.model, args.prompt)
    except Exception as exc:
        print(f"ERROR: request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    # 同时打印 pretty 和 compact 两种 JSON，便于对比“人读友好”与“机器传输”格式。
    pretty_json = json.dumps(plan.model_dump(), ensure_ascii=False, indent=2)
    compact_json = plan.model_dump_json(ensure_ascii=False)

    print("=== Parsed JSON ===")
    print(pretty_json)
    print("\n=== Raw JSON ===")
    print(compact_json)


if __name__ == "__main__":
    main()
