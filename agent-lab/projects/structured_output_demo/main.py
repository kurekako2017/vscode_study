"""structured_output_demo: 演示如何让模型返回结构化数据并用 Pydantic 验证。

该示例展示：
- 使用 Pydantic 定义输出 schema（`AgentPlan`）作为 contract
- 用 Responses API 的 `parse` 将模型输出解析并验证为 Pydantic 模型

对下游系统而言，稳定的 schema 能显著降低解析错误和生产风险。
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
    """创建 OpenAI 客户端，要求通过环境变量提供 `OPENAI_API_KEY`。"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key)


def generate_plan(client: OpenAI, model: str, prompt: str) -> AgentPlan:
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
    args = parse_args()
    client = build_client()

    try:
        plan = generate_plan(client, args.model, args.prompt)
    except Exception as exc:
        print(f"ERROR: request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    # 打印已解析的 Pydantic 对象的可读和压缩 JSON 表现，便于学习 API 输出格式。
    pretty_json = json.dumps(plan.model_dump(), ensure_ascii=False, indent=2)
    compact_json = plan.model_dump_json(ensure_ascii=False)

    print("=== Parsed JSON ===")
    print(pretty_json)
    print("\n=== Raw JSON ===")
    print(compact_json)


if __name__ == "__main__":
    main()
