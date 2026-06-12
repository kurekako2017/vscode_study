#!/usr/bin/env python3
"""
文件功能概述：`run.py` 主要是 运行，这个文件里有 0 个类、4 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 函数 `_build_parser`：先进入当前步骤，再调用 argparse.ArgumentParser、parser.add_argument 等内部步骤完成主要工作，最后返回结果。
2. 函数 `_print_commands`：先进入当前步骤，然后循环处理每一条数据，再调用 print、sorted、join 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
3. 函数 `_run`：先接收输入参数 alias, extra_args，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 print、os.environ.copy、child_env.setdefault 等内部步骤完成主要工作，最后返回结果。
4. 函数 `main`：先进入当前步骤，接着根据条件分支选择不同处理路径，再调用 _build_parser、parser.parse_args、_run 等内部步骤完成主要工作，最后返回结果。
"""


from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODE = ROOT / "code"
AGENT_DIR = CODE / "C9" / "agent(代码系ai生成)"
POWERRAG_DIR = ROOT / "Extra-chapter" / "PowerRAG-SDK-Text-QA" / "code"


COMMANDS: dict[str, tuple[Path, Path, str]] = {
    "c1-1": (CODE, CODE / "C1" / "01_langchain_example.py", "Chapter 1 LangChain example"),
    "c1-2": (CODE, CODE / "C1" / "02_llamaIndex_example.py", "Chapter 1 LlamaIndex example"),
    "c1-fix": (CODE, CODE / "C1" / "fix_nltk.py", "Chapter 1 NLTK fix"),
    "c2-1": (CODE, CODE / "C2" / "01_unstructured_example.py", "Chapter 2 unstructured example"),
    "c2-2": (CODE, CODE / "C2" / "02_character_splitter.py", "Chapter 2 character splitter"),
    "c2-3": (CODE, CODE / "C2" / "03_recursive_character_splitter.py", "Chapter 2 recursive splitter"),
    "c2-4": (CODE, CODE / "C2" / "04_semantic_chunker.py", "Chapter 2 semantic chunker"),
    "c3-1": (CODE, CODE / "C3" / "01_bge_visualized.py", "Chapter 3 BGE visualized"),
    "c3-2": (CODE, CODE / "C3" / "02_langchain_faiss.py", "Chapter 3 LangChain FAISS"),
    "c3-3": (CODE, CODE / "C3" / "03_llamaindex_vector.py", "Chapter 3 LlamaIndex vector"),
    "c3-4": (CODE, CODE / "C3" / "04_multi_milvus.py", "Chapter 3 multi Milvus"),
    "c3-5": (CODE, CODE / "C3" / "05_sentence_window_retrieval.py", "Chapter 3 sentence window retrieval"),
    "c3-6": (CODE, CODE / "C3" / "06_recursive_retrieval.py", "Chapter 3 recursive retrieval"),
    "c3-7": (CODE, CODE / "C3" / "07_recursive_retrieval_v2.py", "Chapter 3 recursive retrieval v2"),
    "c3-download": (CODE, CODE / "C3" / "download_model.py", "Chapter 3 download model"),
    "c3-dragon": (CODE, CODE / "C3" / "work_multimodal_dragon_search.py", "Chapter 3 multimodal dragon search"),
    "c3-hybrid": (CODE, CODE / "C3" / "work_hybrid_multimodal_search.py", "Chapter 3 hybrid multimodal search"),
    "c4-1": (CODE, CODE / "C4" / "01_hybrid_search.py", "Chapter 4 hybrid search"),
    "c4-1v2": (CODE, CODE / "C4" / "01_hybrid_search_v2.py", "Chapter 4 hybrid search v2"),
    "c4-2": (CODE, CODE / "C4" / "02_text_to_metadata_filter.py", "Chapter 4 text to metadata filter"),
    "c4-3": (CODE, CODE / "C4" / "03_text2sql_demo.py", "Chapter 4 text2sql demo"),
    "c4-3v2": (CODE, CODE / "C4" / "03_text2sql_demo_v2.py", "Chapter 4 text2sql demo v2"),
    "c4-4": (CODE, CODE / "C4" / "04_text_to_metadata_filter_v2.py", "Chapter 4 text to metadata filter v2"),
    "c4-5": (CODE, CODE / "C4" / "05_llm_based_routing.py", "Chapter 4 LLM-based routing"),
    "c4-6": (CODE, CODE / "C4" / "06_embedding_based_routing.py", "Chapter 4 embedding-based routing"),
    "c4-7": (CODE, CODE / "C4" / "07_rerank_and_refine.py", "Chapter 4 rerank and refine"),
    "c4-work": (CODE, CODE / "C4" / "work_rerank_and_refine.py", "Chapter 4 rerank and refine work"),
    "c5-1": (CODE, CODE / "C5" / "01_pydantic.py", "Chapter 5 pydantic"),
    "c5-2": (CODE, CODE / "C5" / "02_function_calling_example.py", "Chapter 5 function calling"),
    "c6-1": (CODE, CODE / "C6" / "01_llamaindex_evaluation_example.py", "Chapter 6 evaluation example"),
    "c8": (CODE, CODE / "C8" / "main.py", "Chapter 8 recipe RAG system"),
    "c9": (CODE, CODE / "C9" / "main.py", "Chapter 9 graph RAG system"),
    "c9-agent-test": (AGENT_DIR, AGENT_DIR / "run_ai_agent.py", "C9 agent test"),
    "c9-agent-run": (AGENT_DIR, AGENT_DIR / "run_ai_agent.py", "C9 agent run"),
    "c9-agent-status": (AGENT_DIR, AGENT_DIR / "batch_manager.py", "C9 agent status"),
    "c9-agent-continue": (AGENT_DIR, AGENT_DIR / "batch_manager.py", "C9 agent continue"),
    "c9-agent-merge": (AGENT_DIR, AGENT_DIR / "batch_manager.py", "C9 agent merge"),
    "c9-agent-details": (AGENT_DIR, AGENT_DIR / "batch_manager.py", "C9 agent details"),
    "powerrag": (POWERRAG_DIR, POWERRAG_DIR / "main.py", "PowerRAG text QA"),
}


SHORTCUTS = {
    "c1": ["c1-1", "c1-2", "c1-fix"],
    "c2": ["c2-1", "c2-2", "c2-3", "c2-4"],
    "c3": ["c3-1", "c3-2", "c3-3", "c3-4", "c3-5", "c3-6", "c3-7", "c3-download", "c3-dragon", "c3-hybrid"],
    "c4": ["c4-1", "c4-1v2", "c4-2", "c4-3", "c4-3v2", "c4-4", "c4-5", "c4-6", "c4-7", "c4-work"],
    "c5": ["c5-1", "c5-2"],
    "c6": ["c6-1"],
    "c8": ["c8"],
    "c9": ["c9"],
    "c9-agent": ["c9-agent-test", "c9-agent-run", "c9-agent-status", "c9-agent-continue", "c9-agent-merge", "c9-agent-details"],
    "all": [
        "c1-1", "c1-2", "c1-fix",
        "c2-1", "c2-2", "c2-3", "c2-4",
        "c3-1", "c3-2", "c3-3", "c3-4", "c3-5", "c3-6", "c3-7", "c3-download", "c3-dragon", "c3-hybrid",
        "c4-1", "c4-1v2", "c4-2", "c4-3", "c4-3v2", "c4-4", "c4-5", "c4-6", "c4-7", "c4-work",
        "c5-1", "c5-2",
        "c6-1",
        "c8",
        "c9",
    ],
}


def _build_parser() -> argparse.ArgumentParser:  # 中文名称：构建parser
    parser = argparse.ArgumentParser(description="Unified launcher for all-in-rag-main")
    parser.add_argument("command", nargs="?", help="Alias such as c1-1, c8, c9-agent-test, powerrag, all")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Extra args passed to the target script")
    parser.add_argument("--list", action="store_true", help="List available commands")
    return parser


def _print_commands() -> None:  # 中文名称：printcommands
    print("Available commands:")
    for key in sorted(COMMANDS):
        print(f"  {key:16} {COMMANDS[key][2]}")
    print("\nGroups:")
    for key in sorted(SHORTCUTS):
        joined = ", ".join(SHORTCUTS[key])
        print(f"  {key:16} {joined}")


def _run(alias: str, extra_args: list[str]) -> int:  # 中文名称：运行
    if alias not in COMMANDS:
        if alias in SHORTCUTS:
            for item in SHORTCUTS[alias]:
                code = _run(item, extra_args if item == alias else [])
                if code != 0:
                    return code
            return 0

        print(f"Unknown command: {alias}")
        _print_commands()
        return 2

    cwd, script, desc = COMMANDS[alias]
    if not script.exists():
        print(f"Missing script for {alias}: {script}")
        return 2

    print(f"[{alias}] {desc}")
    cmd = [sys.executable, str(script), *extra_args]
    child_env = os.environ.copy()
    child_env.setdefault("OPENROUTER_API_KEY", "offline")
    child_env.setdefault("OPENAI_API_KEY", child_env["OPENROUTER_API_KEY"])
    child_env.setdefault("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    child_env.setdefault("OPENAI_BASE_URL", child_env["OPENROUTER_BASE_URL"])
    child_env.setdefault("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    child_env.setdefault("LLM_QWEN_MAX", child_env["OPENROUTER_MODEL"])
    pythonpath = child_env.get("PYTHONPATH", "")
    child_env["PYTHONPATH"] = str(CODE) + (os.pathsep + pythonpath if pythonpath else "")
    result = subprocess.run(cmd, cwd=str(script.parent), env=child_env)
    return result.returncode


def main() -> int:  # 中文名称：主函数
    parser = _build_parser()
    ns = parser.parse_args()

    if ns.list or not ns.command:
        _print_commands()
        return 0 if ns.command is None else 0

    return _run(ns.command, ns.args)


if __name__ == "__main__":
    raise SystemExit(main())
