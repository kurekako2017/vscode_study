"""rag_api_demo: 使用 FastAPI 提供的最小 RAG API 服务示例。

功能概览：
- 扫描指定目录（支持 .md/.txt/.pdf）并把文档切分为 chunk
- 基于关键词重合度做本地检索（PoC），取 top-k 作为上下文
- 将检索到的上下文发送给模型并返回带来源的回答

此示例适合 PoC 与教学，生产请替换为 embeddings + 向量检索，加入认证、限流与缓存。

学习地图：
- 运行命令：
    - uvicorn main:app --reload --port 8000
    - curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"question":"请总结文档重点"}'
- 输入输出：
    - 输入：HTTP JSON 请求（question、model） + 本地 docs 目录
    - 输出：结构化 JSON（answer、sources、source_count）
- 改造练习点：
    - 新增 /config endpoint 暴露当前 chunk 参数
    - 为 /ask 增加 top_k 可选参数
    - 将 load_state 改为可热更新的服务层对象
"""

import os
import re
from dataclasses import dataclass
from pathlib import Path

from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel, Field
from pypdf import PdfReader


DEFAULT_MODEL = "gpt-5"
DEFAULT_DOCS_DIR = "."
SUPPORTED_EXTENSIONS = {".md", ".txt", ".pdf"}
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200
TOP_K = 4
SYSTEM_INSTRUCTIONS = (
    "You are a document QA assistant for a Japanese IT project learning lab. "
    "Answer only from the provided retrieved context. "
    "If the context is insufficient, say that clearly. "
    "Mention source labels when possible."
)


@dataclass
class Chunk:
    """文档切分后的片段对象：包含来源标签、内容与得分。"""
    source_label: str
    content: str
    score: int = 0


class AskRequest(BaseModel):
    """/ask 请求体：问题文本 + 可选模型名。"""
    question: str = Field(min_length=1, description="Question about local documents.")
    model: str = Field(default=DEFAULT_MODEL, description="OpenAI model to use.")


class SourceItem(BaseModel):
    """来源条目：用于告诉调用方答案依据来自哪些文档片段。"""
    source_label: str
    score: int


class AskResponse(BaseModel):
    """/ask 响应体：答案正文 + 来源摘要，便于前端或调用方渲染。"""
    answer: str
    model: str
    docs_dir: str
    source_count: int
    sources: list[SourceItem]


class ReloadResponse(BaseModel):
    """/reload 响应体：用于确认文档索引是否已刷新。"""
    docs_dir: str
    chunk_count: int


def build_client() -> OpenAI:
    # 层次: 基础设施层 — 构建 OpenAI 客户端并在缺失时抛出以便上层处理
    """根据环境变量创建 OpenAI 客户端，缺失抛出异常以便上层处理。"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key)


def get_docs_dir() -> Path:
    # 层次: 配置/IO 层 — 解析并校验文档目录配置
    """获取并校验用于 RAG 的文档目录（可通过环境变量覆盖）。"""
    docs_dir = os.getenv("RAG_API_DOCS_DIR", DEFAULT_DOCS_DIR)
    path = Path(docs_dir).resolve()
    if not path.exists() or not path.is_dir():
        raise RuntimeError("RAG_API_DOCS_DIR must point to an existing directory.")
    return path


def iter_text_files(base_dir: Path) -> list[Path]:
    # 层次: IO/索引层 — 列出支持的文档文件路径
    """递归列出支持类型的文件路径并返回排序列表。"""
    files = []
    for path in base_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path)
    return sorted(files)


def read_document_text(file_path: Path) -> str:
    # 层次: IO/解析层 — 根据文件类型提取文本（支持 md/txt/pdf）
    """根据文件类型读取文本内容；对 PDF 使用 `pypdf` 做基本提取。"""
    suffix = file_path.suffix.lower()

    if suffix in {".md", ".txt"}:
        return file_path.read_text(encoding="utf-8")

    if suffix == ".pdf":
        # PDF text extraction quality depends on the original document structure.
        reader = PdfReader(str(file_path))
        pages = []
        for index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append(f"[PAGE {index}]\n{text}")
        return "\n\n".join(pages)

    raise ValueError(f"Unsupported file type: {suffix}")


def chunk_text(text: str) -> list[str]:
    # 层次: 索引构建层 — 切分文本为带重叠 chunk
    """把文本切分为带重叠的 chunk，保留跨块上下文。"""
    normalized = text.replace("\r\n", "\n").strip()
    if not normalized:
        return []

    chunks = []
    start = 0
    # Overlap keeps adjacent chunks from losing too much local context.
    while start < len(normalized):
        end = min(len(normalized), start + CHUNK_SIZE)
        chunks.append(normalized[start:end])
        if end >= len(normalized):
            break
        start = end - CHUNK_OVERLAP
    return chunks


def build_chunks(base_dir: Path) -> list[Chunk]:
    # 层次: 索引构建层 — 构建带来源标签的 chunk 列表并返回
    """读取指定目录下的文件并构建带来源标签的 chunk 列表。"""
    chunks: list[Chunk] = []
    for file_path in iter_text_files(base_dir):
        try:
            text = read_document_text(file_path)
        except (UnicodeDecodeError, ValueError):
            continue

        relative = file_path.relative_to(base_dir)
        for index, part in enumerate(chunk_text(text), start=1):
            chunks.append(Chunk(source_label=f"{relative}#chunk{index}", content=part))
    return chunks


def tokenize(text: str) -> set[str]:
    # 层次: 工具层 — 简单分词实现，用于检索评分
    """简单分词函数，支持英文、数字和部分中日韩字符，用于关键词检索示例。"""
    return set(re.findall(r"[A-Za-z0-9_\-\u4e00-\u9fff\u3040-\u30ff]+", text.lower()))


def retrieve(question: str, chunks: list[Chunk]) -> list[Chunk]:
    # 层次: 检索层 — 使用关键词重合度实现简单检索（PoC）
    """基于关键词重合度进行简单检索并返回 top-k。"""
    question_tokens = tokenize(question)
    ranked: list[Chunk] = []

    # This PoC keeps retrieval local and cheap by using keyword overlap instead of embeddings.
    for chunk in chunks:
        chunk_tokens = tokenize(chunk.content)
        score = len(question_tokens & chunk_tokens)
        if score > 0:
            ranked.append(Chunk(chunk.source_label, chunk.content, score))

    ranked.sort(key=lambda item: (-item.score, item.source_label))
    return ranked[:TOP_K]


def build_context(top_chunks: list[Chunk]) -> str:
    # 层次: 上下文构建层 — 将 top chunks 拼接为模型可读的上下文
    """把检索到的 top chunks 拼接为供模型使用的上下文字符串。"""
    if not top_chunks:
        return "No relevant local document chunks were retrieved."

    parts = []
    for chunk in top_chunks:
        parts.append(f"[SOURCE: {chunk.source_label}]\n{chunk.content}")
    return "\n\n".join(parts)


def answer_question(client: OpenAI, model: str, question: str, context: str) -> str:
    # 层次: 调用层 — 用检索上下文构造 prompt 并请求模型回答
    """调用模型回答，限制其仅基于传入的检索上下文回答问题。"""
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


app = FastAPI(title="rag_api_demo", version="0.1.0")
# 将运行时状态挂在 app.state，方便在多个 endpoint 间共享。
app.state.client = None
app.state.docs_dir = None
app.state.chunks = []


def load_state() -> None:
    """初始化或重新加载服务状态：扫描文档目录并缓存 chunks 与客户端实例。"""
    docs_dir = get_docs_dir()
    chunks = build_chunks(docs_dir)
    if not chunks:
        raise RuntimeError("No readable .md, .txt, or .pdf files were found in docs directory.")
    # Cache the parsed chunks in memory so each request does not rescan the directory.
    app.state.client = build_client()
    app.state.docs_dir = docs_dir
    app.state.chunks = chunks


@app.on_event("startup")
def startup_event() -> None:
    """服务启动时预热：加载文档并构建内存索引。"""
    load_state()


@app.get("/health")
def health() -> dict[str, object]:
    """健康检查接口，返回当前 docs 目录和 chunk 数量。"""
    return {
        "status": "ok",
        "docs_dir": str(app.state.docs_dir),
        "chunk_count": len(app.state.chunks),
    }


@app.post("/reload", response_model=ReloadResponse)
def reload_docs() -> ReloadResponse:
    """手动触发重新加载文档目录并返回新的 chunk 计数。"""
    try:
        load_state()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return ReloadResponse(
        docs_dir=str(app.state.docs_dir),
        chunk_count=len(app.state.chunks),
    )


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    """对外 API：接收问题、检索文档并返回模型回答与来源信息。"""
    if app.state.client is None or app.state.docs_dir is None:
        raise HTTPException(status_code=500, detail="Service is not initialized.")

    # Retrieve first, then pass only the top chunks to the model.
    top_chunks = retrieve(request.question, app.state.chunks)
    context = build_context(top_chunks)

    try:
        answer = answer_question(
            app.state.client,
            request.model,
            request.question,
            context,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return AskResponse(
        answer=answer,
        model=request.model,
        docs_dir=str(app.state.docs_dir),
        source_count=len(top_chunks),
        sources=[
            SourceItem(source_label=chunk.source_label, score=chunk.score)
            for chunk in top_chunks
        ],
    )
