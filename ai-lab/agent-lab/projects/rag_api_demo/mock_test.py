#!/usr/bin/env python3
"""Lightweight mock tester for rag_api_demo without FastAPI/uvicorn.

This script simulates the /ask mock response that the service would return
when running in mock mode (RAG_API_MOCK=1 or no OPENAI_API_KEY).

Usage:
    python3 mock_test.py "你的问题"
"""
import sys
import json
from pathlib import Path

QUESTION = sys.argv[1] if len(sys.argv) > 1 else "这是一次烟雾测试"


def build_mock_answer(question: str, top_chunks: list) -> str:
    """生成 mock 回答文本，模拟 /ask 在 mock 模式下的输出。"""
    lines = ["[MOCK MODE]", f"问题: {question}"]
    lines.append(f"检索到的片段数量: {len(top_chunks)}")
    lines.append("练习建议: 将检索替换为向量检索并在 real 模式下测试。")
    return "\n".join(lines)


def main():
    """入口：构造 mock 响应并以 JSON 形式输出到终端。"""
    # 在真实服务中 top_chunks 会来自检索流程，这里留空以保持脚本轻量
    top_chunks = []
    ans = build_mock_answer(QUESTION, top_chunks)
    # 组装与 /ask 一致的响应结构，便于本地验证
    out = {
        "answer": ans,
        "model": "mock",
        "docs_dir": str(Path('.').resolve()),
        "source_count": len(top_chunks),
        "sources": [],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
