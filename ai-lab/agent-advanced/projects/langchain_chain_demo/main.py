"""LangChain 风格最小链路 demo。

这个脚本演示三件事：
1. Prompt 模板
2. 模型调用
3. 输出解析

默认使用 mock 模式，保证无需 Key 也能运行。
"""

from __future__ import annotations

import argparse
import json
import os
import re
from typing import Any

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LangChain 风格最小链路 demo")
    parser.add_argument("question", help="要询问的问题")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="强制使用 mock 模式",
    )
    parser.add_argument(
        "--real",
        action="store_true",
        help="尝试真实模型模式（需要 OPENROUTER_API_KEY / DEEPSEEK_API_KEY / OPENAI_API_KEY）",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"真实模式下使用的模型名，默认 {DEFAULT_MODEL}",
    )
    return parser.parse_args()


def build_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是一个教学用的 LangChain 讲解器。"
                "请围绕用户问题输出严格 JSON，包含 summary、steps、keywords 三个字段。",
            ),
            ("human", "问题：{question}"),
        ]
    )


def extract_keywords(text: str) -> list[str]:
    raw_terms = re.findall(r"[A-Za-z0-9_+-]{2,}|[\u4e00-\u9fff]{2,}", text)
    cleaned: list[str] = []
    for term in raw_terms:
        if term not in cleaned:
            cleaned.append(term)
    return cleaned[:6]


def mock_llm(prompt_value: Any) -> AIMessage:
    question = prompt_value.to_messages()[-1].content.strip()
    keywords = extract_keywords(question)
    payload = {
        "summary": f"这是关于「{question}」的教学型回答。",
        "steps": [
            "先看 prompt 如何收集输入。",
            "再看模型如何接收和生成内容。",
            "最后把输出解析成结构化结果。",
        ],
        "keywords": keywords or ["LangChain", "Prompt", "Parser"],
    }
    return AIMessage(content=json.dumps(payload, ensure_ascii=False, indent=2))


def build_real_llm():
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:  # pragma: no cover - 依赖缺失时使用
        raise RuntimeError("缺少 langchain-openai，无法进入真实模式") from exc

    api_key = (
        os.getenv("OPENROUTER_API_KEY")
        or os.getenv("DEEPSEEK_API_KEY")
        or os.getenv("OPENAI_API_KEY")
    )
    if not api_key:
        raise RuntimeError("未配置可用 API Key，无法进入真实模式")

    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    return ChatOpenAI(
        model=DEFAULT_MODEL,
        api_key=api_key,
        base_url=base_url,
        temperature=0,
    )


def parse_response(message: AIMessage) -> dict[str, Any]:
    try:
        return json.loads(message.content)
    except json.JSONDecodeError:
        return {
            "summary": message.content.strip(),
            "steps": [],
            "keywords": [],
        }


def build_chain(use_mock: bool):
    prompt = build_prompt()
    llm = RunnableLambda(mock_llm) if use_mock else build_real_llm()
    return prompt | llm | RunnableLambda(parse_response)


def main() -> None:
    args = parse_args()
    use_mock = args.mock or not args.real

    if args.real and not use_mock:
        try:
            chain = build_chain(False)
        except Exception as exc:
            print(f"真实模式不可用，回退到 mock：{exc}")
            chain = build_chain(True)
    else:
        chain = build_chain(True)

    print("=== LangChain 风格链路（Mermaid） ===")
    print(chain.get_graph().draw_mermaid())
    print("=== 运行结果 ===")
    result = chain.invoke({"question": args.question})
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
