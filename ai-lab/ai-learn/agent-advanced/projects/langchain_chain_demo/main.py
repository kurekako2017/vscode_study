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
import sys
from pathlib import Path
from typing import Any
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

for _parent in Path(__file__).resolve().parents:
    if (_parent / "llm_runtime.py").exists():
        sys.path.insert(0, str(_parent))
        break
from llm_runtime import build_fallback_client

# 默认模型名。
# 这里优先读取环境变量，方便以后切换供应商或模型。
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")


# 解析问题输入和 mock / real 模式开关。
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
    # 是否同时打印模型原始输出，便于理解“原始结果”和“解析后结果”的差别。
    parser.add_argument(
        "--show-raw",
        action="store_true",
        help="打印模型原始输出，再打印解析后的结果",
    )
    # 解析并返回结果。
    return parser.parse_args()


# 构造用于教学的 Prompt 模板。
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


# 从问题里抽取关键词，模拟模型理解。
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


# 用本地逻辑模拟模型输出 JSON。
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


# 构建真实模型客户端，供 real 模式使用。
def build_real_llm(model: str):
    client = build_fallback_client()

    def invoke(prompt_value: Any) -> AIMessage:
        messages = prompt_value.to_messages()
        instructions = str(messages[0].content) if len(messages) > 1 else None
        prompt = str(messages[-1].content)
        response = client.responses.create(
            model=model,
            instructions=instructions,
            input=prompt,
        )
        return AIMessage(content=response.output_text)

    return RunnableLambda(invoke)


# 把模型输出解析成结构化字典。
def parse_response(message: AIMessage) -> dict[str, Any]:
    # 尝试把模型输出当作 JSON 解析。
    content = str(message.content).strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # 如果模型没有严格输出 JSON，就退回为纯文本结构。
        return {
            "summary": content,
            "steps": [],
            "keywords": [],
        }


# 组合 prompt、LLM 和解析器，形成一条链。
def build_chain(use_mock: bool, model: str = DEFAULT_MODEL):
    # 先构造 prompt。
    prompt = build_prompt()
    # 根据开关决定使用 mock 还是真实模型。
    llm = RunnableLambda(mock_llm) if use_mock else build_real_llm(model)
    # prompt -> llm -> parse_response
    return prompt | llm | RunnableLambda(parse_response)


# 只构造 prompt -> llm，用于查看原始模型输出。
def build_generation_chain(use_mock: bool, model: str = DEFAULT_MODEL):
    # 先构造 prompt。
    prompt = build_prompt()
    # 根据开关决定使用 mock 还是真实模型。
    llm = RunnableLambda(mock_llm) if use_mock else build_real_llm(model)
    # prompt -> llm
    return prompt | llm


# 程序入口，构建链路并执行一次推理。
def main() -> None:
    # 解析命令行参数。
    args = parse_args()

    # 默认优先尝试真实模式，只有显式指定 --mock 时才直接用 mock。
    if args.mock:
        print("=== 模式 ===")
        print("mock（强制本地模拟）")
        print("MODEL: provider=local model=mock mode=mock", file=sys.stderr)
        # 用户明确要求 mock，就跳过真实模型。
        chain = build_chain(True, args.model)
    else:
        print("=== 模式 ===")
        print("real（优先尝试真实模型，失败后回退到 mock）")
        # 默认先尝试真实链路，不可用时再回退到 mock。
        try:
            chain = build_chain(False, args.model)
        except Exception as exc:
            # 真实模式失败时，自动回退到 mock，保证演示可继续。
            print(f"真实模式不可用，回退到 mock：{exc}")
            chain = build_chain(True, args.model)

    # 打印 Mermaid 图，方便学习链路结构。
    print("=== LangChain 风格链路（Mermaid） ===")
    print(chain.get_graph().draw_mermaid())  # 打印 Mermaid 图，方便学习链路结构。

    # 如果用户想看原始模型输出，就先打印原始内容，再打印解析结果。
    if args.show_raw:
        generation_chain = build_generation_chain(args.mock, args.model)
        raw_message = generation_chain.invoke({"question": args.question})
        print("=== 原始结果 ===")
        print(raw_message.content)
        print("=== 解析后结果 ===")
        print(
            json.dumps(parse_response(raw_message), ensure_ascii=False, indent=2)
        )
    else:
        # 默认只打印解析后的结果，输出更干净。
        print("=== 运行结果 ===")
        result = chain.invoke({"question": args.question})  # 执行链路并打印结果。
        print(json.dumps(result, ensure_ascii=False, indent=2))  # 打印结果。


if __name__ == "__main__":
    main()
