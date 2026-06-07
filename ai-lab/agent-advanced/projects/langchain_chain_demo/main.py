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

# 默认模型名。
# 这里优先读取环境变量，方便以后切换供应商或模型。
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")


def parse_args() -> argparse.Namespace:
    # 创建命令行解析器。
    parser = argparse.ArgumentParser(description="LangChain 风格最小链路 demo")
    # 用户输入的问题，作为整个链路的核心输入。
    parser.add_argument("question", help="要询问的问题")
    # 强制使用 mock 模式，不访问真实 API。
    parser.add_argument(
        "--mock",
        action="store_true",
        help="强制使用 mock 模式",
    )
    # 尝试真实模式。
    parser.add_argument(
        "--real",
        action="store_true",
        help="尝试真实模型模式（需要 OPENROUTER_API_KEY / DEEPSEEK_API_KEY / OPENAI_API_KEY）",
    )
    # 真实模式下使用的模型名。
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"真实模式下使用的模型名，默认 {DEFAULT_MODEL}",
    )
    # 解析并返回结果。
    return parser.parse_args()


def build_prompt() -> ChatPromptTemplate:
    # 用 LangChain 的提示词模板封装 system + human 两段消息。
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
    # 用正则从文本里提取中英文关键词。
    raw_terms = re.findall(r"[A-Za-z0-9_+-]{2,}|[\u4e00-\u9fff]{2,}", text)
    # cleaned 用来保存去重后的关键词。
    cleaned: list[str] = []
    # 按原始顺序去重，保留最先出现的词。
    for term in raw_terms:
        if term not in cleaned:
            cleaned.append(term)
    # 最多返回 6 个词，避免输出太长。
    return cleaned[:6]


def mock_llm(prompt_value: Any) -> AIMessage:
    # 从 prompt 中取出最后一条消息，也就是 human 问题。
    question = prompt_value.to_messages()[-1].content.strip()
    # 根据问题提取一些关键词，模拟“模型理解”。
    keywords = extract_keywords(question)
    # 组装一个结构化的 JSON 结果。
    payload = {
        "summary": f"这是关于「{question}」的教学型回答。",
        "steps": [
            "先看 prompt 如何收集输入。",
            "再看模型如何接收和生成内容。",
            "最后把输出解析成结构化结果。",
        ],
        "keywords": keywords or ["LangChain", "Prompt", "Parser"],
    }
    # 把 JSON 作为 AIMessage 的内容返回，模拟模型输出。
    return AIMessage(content=json.dumps(payload, ensure_ascii=False, indent=2))


def build_real_llm():
    # 真实模式才需要导入 langchain_openai。
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:  # pragma: no cover - 依赖缺失时使用
        # 如果没装依赖，就直接报出明确错误。
        raise RuntimeError("缺少 langchain-openai，无法进入真实模式") from exc

    # 真实模式支持多个供应商的 API Key。
    api_key = (
        os.getenv("OPENROUTER_API_KEY")
        or os.getenv("DEEPSEEK_API_KEY")
        or os.getenv("OPENAI_API_KEY")
    )
    # 如果一个 Key 都没有，就不能继续走真实模式。
    if not api_key:
        raise RuntimeError("未配置可用 API Key，无法进入真实模式")

    # base_url 也做成环境变量，方便切换不同兼容服务。
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    # 返回 OpenAI 兼容客户端。
    return ChatOpenAI(
        model=DEFAULT_MODEL,
        api_key=api_key,
        base_url=base_url,
        temperature=0,
    )


def parse_response(message: AIMessage) -> dict[str, Any]:
    # 尝试把模型输出当作 JSON 解析。
    try:
        return json.loads(message.content)
    except json.JSONDecodeError:
        # 如果模型没有严格输出 JSON，就退回为纯文本结构。
        return {
            "summary": message.content.strip(),
            "steps": [],
            "keywords": [],
        }


def build_chain(use_mock: bool):
    # 先构造 prompt。
    prompt = build_prompt()
    # 根据开关决定使用 mock 还是真实模型。
    llm = RunnableLambda(mock_llm) if use_mock else build_real_llm()
    # prompt -> llm -> parse_response
    return prompt | llm | RunnableLambda(parse_response)


def main() -> None:
    # 解析命令行参数。
    args = parse_args()
    # 只要没有显式要求真实模式，就默认用 mock。
    use_mock = args.mock or not args.real

    # 如果用户要求真实模式，就先尝试构建真实链路。
    if args.real and not use_mock:
        try:
            chain = build_chain(False)
        except Exception as exc:
            # 真实模式失败时，自动回退到 mock，保证演示可继续。
            print(f"真实模式不可用，回退到 mock：{exc}")
            chain = build_chain(True)
    else:
        # 普通情况下直接构建 mock 链路。
        chain = build_chain(True)

    # 打印 Mermaid 图，方便学习链路结构。
    print("=== LangChain 风格链路（Mermaid） ===")
    print(chain.get_graph().draw_mermaid())
    # 执行链路并打印结果。
    print("=== 运行结果 ===")
    result = chain.invoke({"question": args.question})
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
