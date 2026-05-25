"""model_call_example.py

示例：最小的模型调用封装，使用 OpenAI 官方 SDK 的 Responses API。
需要设置环境变量 `OPENAI_API_KEY`。
运行：`python model_call_example.py "请给出三步学习计划"`
"""

import os
import sys
from typing import Optional

try:
    from openai import OpenAI
except Exception:  # pragma: no cover - graceful fallback if package missing
    OpenAI = None


DEFAULT_MODEL = "gpt-5"
SYSTEM_INSTRUCTIONS = (
    "You are a concise assistant for an LLM learning lab. Answer briefly and clearly."
)


def build_client() -> Optional[OpenAI]:
    """构建 OpenAI 客户端，若未安装 SDK 则返回 None。"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    if OpenAI is None:
        print("openai package is not installed; install with `pip install openai`.")
        sys.exit(1)
    return OpenAI(api_key=api_key)


def ask_once(client: OpenAI, model: str, prompt: str) -> str:
    """发送一次性请求并返回文本回答。"""
    response = client.responses.create(
        model=model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=prompt,
    )
    # Responses API 提供简化的输出接口 `output_text`
    # 注意：在复杂场景下，response 还包含 token-level 顶层结构、工具调用信息等。
    # 这里为了教学简洁，直接返回主文本回答；如果需要详细调试，可打印完整的 response 对象。
    return response.output_text


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Minimal model call example")
    parser.add_argument("prompt", nargs="?", default="Hello, explain agents in one line")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()

    client = build_client()
    print(ask_once(client, args.model, args.prompt))


if __name__ == "__main__":
    main()
