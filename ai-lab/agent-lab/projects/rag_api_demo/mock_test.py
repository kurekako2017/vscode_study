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
    lines = ["[MOCK MODE]", f"问题: {question}"]
    lines.append(f"检索到的片段数量: {len(top_chunks)}")
    lines.append("练习建议: 将检索替换为向量检索并在 real 模式下测试。")
    return "\n".join(lines)


def main():
    # In a real run top_chunks would be retrieved from documents; here we keep it empty.
    top_chunks = []
    ans = build_mock_answer(QUESTION, top_chunks)
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
