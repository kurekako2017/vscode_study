#!/usr/bin/env python3
"""
轻量级 mock 测试器，用于模拟 rag_api_demo 在 mock 模式下的响应。
Usage:
    python3 mock_test.py "你的问题"
"""
import sys
import json
from pathlib import Path

# 问题     （问题）
QUESTION = sys.argv[1] if len(sys.argv) > 1 else "这是一次烟雾测试"


# 生成 mock 回答文本，模拟 /ask 在 mock 模式下的输出。
def build_mock_answer(question: str, top_chunks: list) -> str:
    """生成 mock 回答文本，模拟 /ask 在 mock 模式下的输出。"""
    lines = ["[MOCK MODE]", f"问题: {question}"]
    # 添加检索到的片段数量     （添加检索到的片段数量）
    lines.append(f"检索到的片段数量: {len(top_chunks)}")
    # 添加练习建议     （添加练习建议）
    lines.append("练习建议: 将检索替换为向量检索并在 real 模式下测试。")
    # 返回 mock 回答文本     （返回 mock 回答文本）
    return "\n".join(lines)


def main():
    """入口：构造 mock 响应并以 JSON 形式输出到终端。"""
    print("MODEL: provider=local model=mock mode=mock", file=sys.stderr)
    # 在真实服务中 top_chunks 会来自检索流程，这里留空以保持脚本轻量     （在真实服务中 top_chunks 会来自检索流程，这里留空以保持脚本轻量）
    top_chunks = []
    # 构建 mock 回答文本     （构建 mock 回答文本）
    ans = build_mock_answer(QUESTION, top_chunks)
    # 组装与 /ask 一致的响应结构，便于本地验证
    # 组装与 /ask 一致的响应结构，便于本地验证     （组装与 /ask 一致的响应结构，便于本地验证）
    out = {
        "answer": ans,
        # 添加模型名称     （添加模型名称）
        "model": "mock",
        # 添加 docs 目录     （添加 docs 目录）
        "docs_dir": str(Path('.').resolve()),
        # 添加来源数量     （添加来源数量）
        "source_count": len(top_chunks),
        # 添加来源列表     （添加来源列表）
        "sources": [],
    }
    # 打印 JSON 响应     （打印 JSON 响应）
    print(json.dumps(out, ensure_ascii=False, indent=2))
    # 打印 JSON 响应     （打印 JSON 响应）
    print(ans)

if __name__ == '__main__':
    # 如果命令行参数为空，则打印帮助信息     （如果命令行参数为空，则打印帮助信息）
    if len(sys.argv) == 1:
        print("Usage: python3 mock_test.py \"你的问题\"")
        sys.exit(1)
    # 主函数     （主函数）
    main()
