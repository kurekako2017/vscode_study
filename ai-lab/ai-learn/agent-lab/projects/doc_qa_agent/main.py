"""doc_qa_agent: 本地 RAG 文档问答最小示例。

功能概览：
- 扫描指定目录下的 Markdown / 文本文件
- 将文档切分为重叠的 chunk（用于保证局部上下文）
- 使用简单的关键词重合度做检索（PoC 用法，非向量检索）
- 将检索到的 top-k chunk 拼接为上下文并调用模型回答

本示例适合教学与 PoC，生产环境请替换为 embeddings + 向量检索并添加缓存、限流与认证。

学习地图：
- 运行命令：
    - python3 main.py "问题" --docs .
    - python3 main.py "请总结这个目录中的 RAG 思路" --docs ../../..
- 输入输出：
    - 输入：问题文本、--docs 文档目录、--model 模型名
    - 输出：答案正文 + sources（chunk 标签及分数）
- 改造练习点：
    - 将关键词检索替换为向量检索
    - 增加 --top-k 参数并接入 retrieve
    - 在输出中加入每条来源的摘要片段
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from openai import OpenAI

for _parent in Path(__file__).resolve().parents:
    if (_parent / "llm_runtime.py").exists():
        sys.path.insert(0, str(_parent))
        break
from llm_runtime import build_fallback_client, has_real_provider

# 默认模型名，可用 `--model` 覆盖。
DEFAULT_MODEL = "gpt-5"
# OpenRouter 兼容服务默认基址。
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
# 支持的文件扩展名
SUPPORTED_EXTENSIONS = {".md", ".txt"}
# 每个 chunk 的大小
CHUNK_SIZE = 1200
# 每个 chunk 的重叠大小
CHUNK_OVERLAP = 200
# 每个问题返回的 chunk 数量
TOP_K = 4
# 系统指令强调“只基于检索上下文回答”，降低幻觉概率。
SYSTEM_INSTRUCTIONS = (
    "You are a document QA assistant for an LLM agent learning lab. "
    "Answer only from the provided retrieved context. "
    "If the context is insufficient, say that clearly. "
    "When possible, mention the cited source labels."
)


@dataclass
class Chunk:
    """表示一个文档切分后的小片段（chunk）。"""
    # 来源标签
    source_label: str
    # 内容
    content: str
    # 分数
    score: int = 0


def parse_args() -> argparse.Namespace:
    # 层次: 输入层 — 读取用户问题、文档目录与模型选择
    """解析命令行参数：问题文本、文档目录与模型名。"""
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(
        description="Minimal local RAG demo for document QA."
    )
    # 添加问题参数
    parser.add_argument("question", help="Question to ask about local documents.")
    # 添加文档目录参数
    parser.add_argument(
        "--docs",
        default=".",
        help="Directory containing local markdown or text files. Default: current directory.",
    )
    # 添加模型参数
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model name to use. Default: {DEFAULT_MODEL}",
    )
    # 添加 mock 模式参数
    parser.add_argument("--mock", action="store_true", help="Run in offline mock mode (no API calls).")
    # 添加 real 模式参数
    parser.add_argument("--real", action="store_true", help="Force real API mode (requires OPENROUTER_API_KEY or OPENAI_API_KEY).")
    return parser.parse_args()


def _has_real_credentials() -> bool:
    return has_real_provider()


def build_client() -> OpenAI:
    # 层次: 基础设施层 — 构建 OpenAI 客户端并处理环境依赖 （层次: 基础设施层 — 构建 OpenAI 客户端并处理环境依赖）
    """从 OpenRouter 或 OpenAI 兼容环境变量创建 OpenAI 客户端。"""
    # 从环境变量中获取 API Key
    return build_fallback_client()


def resolve_mode(force_mock: bool, force_real: bool) -> str:
    # 决定运行模式：'mock' | 'real'。
    # 如果 force_mock 为 True，则返回 "mock"     
    if force_mock:
        # 返回 "mock"
        return "mock"
    # 如果 force_real 为 True，则返回 "real"     
    if force_real:
        if not _has_real_credentials():
            # 打印错误信息
            print("ERROR: --real requested but OPENROUTER_API_KEY or OPENAI_API_KEY is not set.", file=sys.stderr)
            sys.exit(1)
        # 返回 "real"
        return "real"
    # 如果设置了可用 key，则返回 "real"     
    return "real" if _has_real_credentials() else "mock"


def build_mock_answer(question: str, top_chunks: list[Chunk]) -> str:
    """生成教学用的 mock 回答文本（没有外部依赖）。"""
    lines = ["[MOCK MODE]", f"收到问题: {question}"]
    lines.append("练习建议:")
    lines.append("1) 检查 parse_args() 如何接收参数")
    lines.append("2) 检查检索与上下文拼接流程")
    lines.append("3) 在有真实 API 时再切换 --real 进行完整测试")
    return "\n".join(lines)


def iter_text_files(base_dir: Path) -> list[Path]:
    # 层次: IO/索引层 — 负责查找与列出可检索的文件路径
    """递归查找支持的文本文件并返回排序后的列表。"""
    # 查找支持的文本文件并返回排序后的列表     
    files = []
    for path in base_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path)
    return sorted(files)


def chunk_text(text: str) -> list[str]:
    # 层次: 索引构建层 — 文本切分为可检索的 chunk
    """把长文本切分为带重叠的 chunk，用于保留跨块上下文信息。""" 
    # 标准化文本
    normalized = text.replace("\r\n", "\n").strip()
    if not normalized:
        return []

    # 初始化 chunk 列表    
    chunks = []
    # 初始化 start 为 0    
    start = 0
    # 循环切分文本为 chunk，直到处理完整个文本    
    while start < len(normalized):
        # 计算 end     （计算 end）
        end = min(len(normalized), start + CHUNK_SIZE)
        # 添加 chunk     （添加 chunk）
        chunks.append(normalized[start:end])
        # 如果 end 大于等于 normalized 的长度，则退出循环    
        if end >= len(normalized):
            # 退出循环     
            break
        # 计算 start     
        start = end - CHUNK_OVERLAP
    # 返回 chunk 列表     
    return chunks


def build_chunks(base_dir: Path) -> list[Chunk]:
    # 层次: 索引构建层 — 从文件生成带标签的 chunk 列表
    """读取目录下文件并把文件切分为带标签的 `Chunk` 列表。"""
    # 初始化 chunk 列表    
    chunks: list[Chunk] = []
    # 遍历文件路径     （
    for file_path in iter_text_files(base_dir):
        try:
            # 读取文件文本     
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # 继续下一个文件     
            continue

        relative = file_path.relative_to(base_dir)
        # 遍历 chunk   
        for index, part in enumerate(chunk_text(text), start=1):
            # 计算 label     
            label = f"{relative}#chunk{index}"
            # 添加 chunk    
            chunks.append(Chunk(source_label=str(label), content=part))
    return chunks


def tokenize(text: str) -> set[str]:
    # 层次: 工具层 — 简单分词，用于关键词匹配检索
    """对文本进行简单分词（英文、数字、部分中文/日文字符），用于关键词检索示例。"""
    return set(re.findall(r"[A-Za-z0-9_\-\u4e00-\u9fff\u3040-\u30ff]+", text.lower()))


def retrieve(question: str, chunks: list[Chunk]) -> list[Chunk]:
    # 层次: 检索层 — 简单关键词重合度检索实现（PoC）
    """基于关键词重合度对 chunk 进行打分并返回 top-k。

    注意：这是教学用的简单检索方法，生产请使用向量检索。
    """
    question_tokens = tokenize(question)
    # 初始化 ranked 列表
    ranked = []

    # 遍历 chunk
    for chunk in chunks:
        chunk_tokens = tokenize(chunk.content)
        # 计算 overlap
        overlap = question_tokens & chunk_tokens
        score = len(overlap)
        if score > 0:
            ranked.append(Chunk(chunk.source_label, chunk.content, score))
    ranked.sort(key=lambda item: (-item.score, item.source_label))
    return ranked[:TOP_K]


def build_context(top_chunks: list[Chunk]) -> str:
    # 层次: 上下文构建层 — 将检索结果封装为模型的上下文字符串
    """把 top-k chunks 拼接为模型可读的检索上下文。""" 
    if not top_chunks:
        return "No relevant local document chunks were retrieved."

    parts = []
    # 遍历 chunk
    for chunk in top_chunks:
        parts.append(f"[SOURCE: {chunk.source_label}]\n{chunk.content}")
    return "\n\n".join(parts)


def answer_question(client: OpenAI | None, model: str, question: str, context: str, mode: str) -> str:
    # 层次: 调用层 — 将构建好的 prompt 传给模型并返回答案（支持 mock）
    """调用模型回答，支持 mock 模式返回教学用文本。

    说明：
    - 若 mode == 'mock'，直接返回本地构造的示例回答，方便在无 API Key 环境下学习。
    - 在真实模式下，会把问题和检索到的上下文拼接成 prompt，并调用 SDK 的 Responses API。
    - 返回值为模型的主文本输出（`response.output_text`），上层负责打印或进一步处理。
    """
    if mode == "mock":
        return build_mock_answer(question, [])

    prompt = (
        f"Question:\n{question}\n\n"
        f"Retrieved context:\n{context}\n\n"
        "Answer the question based only on the retrieved context. "
        "If the answer is not fully supported, say so clearly."
    )
    response = client.responses.create(
        model=model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=prompt,
    )
    return response.output_text


def main() -> None:
    # 层次: 程序入口 — 验证输入目录、构建索引、检索并调用模型
    """主流程：校验目录 -> 构建 chunks -> 检索 -> 调用模型 -> 输出答案和来源。"""
    # 解析命令行参数
    args = parse_args()
    base_dir = Path(args.docs).resolve()

    # 如果 base_dir 不存在或不是目录，则打印错误信息并退出
    if not base_dir.exists() or not base_dir.is_dir():
        # 打印错误信息
        print("ERROR: --docs must be an existing directory.", file=sys.stderr)
        sys.exit(1)

    # 索引构建阶段：先读取并切分文档，后续检索和问答都依赖这个中间结果。
    chunks = build_chunks(base_dir)
    if not chunks:
        print("ERROR: no readable .md or .txt files were found.", file=sys.stderr)
        sys.exit(1)

    # The retrieval step happens before the model call so only the most relevant chunks are sent.
    top_chunks = retrieve(args.question, chunks)
    # 构建上下文
    context = build_context(top_chunks)
    # 决定运行模式
    mode = resolve_mode(args.mock, args.real)
    # Mock 回答来自本地模板；真实模式由统一运行时打印最终选中的模型。
    if mode == "mock":
        print("MODEL: provider=local model=mock mode=mock", file=sys.stderr)

    client = None
    if mode == "real":
        client = build_client()

    try:
        # 调用模型回答
        answer = answer_question(client, args.model, args.question, context, mode)
    except Exception as exc:
        print(f"ERROR: request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    print("=== Answer ===")
    print(answer)

    print("\n=== Sources ===")  
    if not top_chunks:
        print("No matching chunks found.")
        return

    # 遍历 chunk   
    for chunk in top_chunks:
        print(f"- {chunk.source_label} (score={chunk.score})")

if __name__ == "__main__":
    main()
