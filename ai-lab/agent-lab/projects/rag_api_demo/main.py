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

from fastapi import FastAPI, HTTPException  # pyright: ignore[reportMissingImports]
from fastapi.middleware.cors import CORSMiddleware  # pyright: ignore[reportMissingImports]
from openai import OpenAI  # pyright: ignore[reportMissingImports]
from pydantic import BaseModel, Field
from pypdf import PdfReader  # pyright: ignore[reportMissingImports]    

# 默认模型名
DEFAULT_MODEL = "gpt-5"
DEFAULT_DOCS_DIR = "."
SUPPORTED_EXTENSIONS = {".md", ".txt", ".pdf"}
# 每个 chunk 的大小
CHUNK_SIZE = 1200
# 每个 chunk 的重叠大小
CHUNK_OVERLAP = 200
# 每个问题返回的 chunk 数量
TOP_K = 4
# 系统指令
SYSTEM_INSTRUCTIONS = (
    "You are a document QA assistant for a Japanese IT project learning lab. "
    "Answer only from the provided retrieved context. "
    "If the context is insufficient, say that clearly. "
    "Mention source labels when possible."
)

# 浏览器客户端默认允许的来源，便于本地 React/Next.js 前端访问。
DEFAULT_CORS_ORIGINS = {
    "http://localhost:3000",
    "http://localhost:4173",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:4173",
    "http://127.0.0.1:5173",
}

# 文档切分后的片段对象：包含来源标签、内容与得分。
@dataclass
class Chunk:
    """文档切分后的片段对象：包含来源标签、内容与得分。"""
    source_label: str
    content: str
    score: int = 0


# /ask 请求体：问题文本 + 可选模型名。
class AskRequest(BaseModel):
    """/ask 请求体：问题文本 + 可选模型名。"""
    question: str = Field(min_length=1, description="Question about local documents.")
    model: str = Field(default=DEFAULT_MODEL, description="OpenAI model to use.")


# 来源条目：用于告诉调用方答案依据来自哪些文档片段。
class SourceItem(BaseModel):
    """来源条目：用于告诉调用方答案依据来自哪些文档片段。"""
    source_label: str
    score: int


# /ask 响应体：答案正文 + 来源摘要，便于前端或调用方渲染。
class AskResponse(BaseModel):
    """/ask 响应体：答案正文 + 来源摘要，便于前端或调用方渲染。"""
    answer: str
    model: str
    docs_dir: str
    source_count: int
    sources: list[SourceItem]


# /reload 响应体：用于确认文档索引是否已刷新。
class ReloadResponse(BaseModel):
    """/reload 响应体：用于确认文档索引是否已刷新。"""
    docs_dir: str
    chunk_count: int


# 构建 OpenAI 客户端，缺失抛出异常以便上层处理。
def build_client() -> OpenAI:
    # 层次: 基础设施层 — 构建 OpenAI 客户端并在缺失时抛出以便上层处理
    """根据环境变量创建 OpenAI 客户端，缺失抛出异常以便上层处理。

    说明：在需要真实调用时使用此函数；若找不到 API Key 会抛出异常，调用方应当捕获或在启动阶段处理。
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key)


# 决定服务运行模式：'mock' 或 'real'。可通过环境变量 RAG_API_MOCK=1 强制 mock。
def resolve_mode() -> str:
    """决定服务运行模式：'mock' 或 'real'。可通过环境变量 RAG_API_MOCK=1 强制 mock。

    优先级：RAG_API_MOCK 环境变量 > OPENAI_API_KEY 自动判断。
    """
    if os.getenv("RAG_API_MOCK") == "1":
        return "mock"
    return "real" if os.getenv("OPENAI_API_KEY") else "mock"


# 生成 RAG mock 回答，包含检索提示与练习建议。
def build_mock_answer(question: str, top_chunks: list[Chunk]) -> str:
    """生成 RAG mock 回答，包含检索提示与练习建议。

    说明：用于在没有外网或 API Key 的环境中做本地学习和验证，回答中包含检索到的片段数量以便观察检索效果。
    """
    lines = ["[MOCK MODE]", f"问题: {question}"]
    lines.append("检索到的片段数量: {}".format(len(top_chunks)))
    lines.append("练习建议: 将检索替换为向量检索并在 real 模式下测试。")
    return "\n".join(lines)


# 获取并校验用于 RAG 的文档目录（可通过环境变量覆盖）。
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
    """根据文件类型读取文本内容；对 PDF 使用 pypdf 做基本提取。"""
    # 获取文件后缀     （获取文件后缀）
    suffix = file_path.suffix.lower()
    # 如果文件后缀为 .pdf，则使用 pypdf 读取文本     （如果文件后缀为 .pdf，则使用 pypdf 读取文本）
    if suffix == ".pdf":
        reader = PdfReader(str(file_path))
        # 初始化 parts 列表     （初始化 parts 列表）
        parts: list[str] = []
        # 遍历每一页     （遍历每一页）
        for page in reader.pages:
            text = page.extract_text()
            # 如果 text 不为空，则添加到 parts 列表     （如果 text 不为空，则添加到 parts 列表）
            if text:
                # 添加 text     （添加 text）
                parts.append(text)
        # 返回 parts 列表     （返回 parts 列表）
        return "\n".join(parts)
    # 如果文件后缀为 .txt 或 .md，则使用 read_text 读取文本     （如果文件后缀为 .txt 或 .md，则使用 read_text 读取文本）
    elif suffix == ".txt" or suffix == ".md":
        return file_path.read_text(encoding="utf-8")
    # 如果文件后缀为其他，则抛出异常     （如果文件后缀为其他，则抛出异常）
    else:
        raise ValueError(f"Unsupported file type: {suffix}")


def chunk_text(text: str) -> list[str]:
    # 层次: 索引构建层 — 切分文本为带重叠 chunk
    """把文本切分为带重叠的 chunk，保留跨块上下文。"""
    # 标准化文本     （标准化文本）
    normalized = text.replace("\r\n", "\n").strip()
    # 如果标准化文本为空，则返回空列表     （如果标准化文本为空，则返回空列表）
    if not normalized:
        return []

    chunks = []
    start = 0
    # 循环切分文本为 chunk，直到处理完整个文本     （循环切分文本为 chunk，直到处理完整个文本）
    while start < len(normalized):
        # 计算 end     （计算 end）
        end = min(len(normalized), start + CHUNK_SIZE)
        # 添加 chunk     （添加 chunk）
        chunks.append(normalized[start:end])
        # 如果 end 大于等于 normalized 的长度，则退出循环     （如果 end 大于等于 normalized 的长度，则退出循环）
        if end >= len(normalized):
            # 退出循环     （退出循环）
            break
        # 计算 start     （计算 start）
        start = end - CHUNK_OVERLAP
    return chunks


# 读取指定目录下的文件并构建带来源标签的 chunk 列表。
def build_chunks(base_dir: Path) -> list[Chunk]:
    # 层次: 索引构建层 — 构建带来源标签的 chunk 列表并返回
    """读取指定目录下的文件并构建带来源标签的 chunk 列表。"""
    # 初始化 chunks 列表     （初始化 chunks 列表）
    chunks: list[Chunk] = []
    # 遍历文件路径     （遍历文件路径）
    for file_path in iter_text_files(base_dir):
        try:
            # 读取文件文本     （读取文件文本）
            text = read_document_text(file_path)
        # 如果异常，则继续下一个文件     （如果异常，则继续下一个文件）
        except (UnicodeDecodeError, ValueError):
            continue
        # 计算相对路径     （计算相对路径）
        relative = file_path.relative_to(base_dir)
        # 遍历 chunk     （遍历 chunk）
        for index, part in enumerate(chunk_text(text), start=1):
            # 添加 chunk     （添加 chunk）
            chunks.append(Chunk(source_label=f"{relative}#chunk{index}", content=part))
    return chunks


# 简单分词函数，支持英文、数字和部分中日韩字符，用于关键词检索示例。
def tokenize(text: str) -> set[str]:
    # 层次: 工具层 — 简单分词实现，用于检索评分
    """简单分词函数，支持英文、数字和部分中日韩字符，用于关键词检索示例。"""
    return set(re.findall(r"[A-Za-z0-9_\-\u4e00-\u9fff\u3040-\u30ff]+", text.lower()))


# 基于关键词重合度进行简单检索并返回 top-k。
def retrieve(question: str, chunks: list[Chunk]) -> list[Chunk]:
    # 层次: 检索层 — 使用关键词重合度实现简单检索（PoC）
    """基于关键词重合度进行简单检索并返回 top-k。"""
    question_tokens = tokenize(question)
    ranked: list[Chunk] = []

    # 遍历 chunks     （遍历 chunks）
    for chunk in chunks:
        # 分词     （分词）
        chunk_tokens = tokenize(chunk.content)
        # 计算分数     （计算分数）
        score = len(question_tokens & chunk_tokens)
        # 如果分数大于 0，则添加到 ranked 列表     （如果分数大于 0，则添加到 ranked 列表）
        if score > 0:
            # 添加 chunk     （添加 chunk）
            ranked.append(Chunk(chunk.source_label, chunk.content, score))

    # 排序     （排序）
    ranked.sort(key=lambda item: (-item.score, item.source_label))
    # 返回 top-k     （返回 top-k）
    return ranked[:TOP_K]


def build_context(top_chunks: list[Chunk]) -> str:
    # 层次: 上下文构建层 — 将 top chunks 拼接为模型可读的上下文
    """把检索到的 top chunks 拼接为供模型使用的上下文字符串。"""
    if not top_chunks:
        return "No relevant local document chunks were retrieved."
    # 初始化 parts 列表     （初始化 parts 列表）       
    parts = []
    for chunk in top_chunks:
        # 添加 part     （添加 part）
        parts.append(f"[SOURCE: {chunk.source_label}]\n{chunk.content}")
    return "\n\n".join(parts)

# 调用模型回答，限制其仅基于传入的检索上下文回答问题。
def answer_question(client: OpenAI | None, model: str, question: str, context: str, top_chunks: list[Chunk] | None = None) -> str:
    # 层次: 调用层 — 用检索上下文构造 prompt 并请求模型回答或返回 mock
    """调用模型回答，限制其仅基于传入的检索上下文回答问题。"""
    # 如果 mode 为 "mock"，则返回 mock 回答     （如果 mode 为 "mock"，则返回 mock 回答）
    mode = resolve_mode()
    if mode == "mock":
        return build_mock_answer(question, top_chunks or [])
    # 初始化 prompt     （初始化 prompt）     （初始化 prompt）
    prompt = (  
        f"Question:\n{question}\n\n"
        f"Retrieved context:\n{context}\n\n"
        "Answer the question based only on the retrieved context. "
        "If the answer is not fully supported, say so clearly."
    )
    # 创建 Responses API 请求     （创建 Responses API 请求）
    response = client.responses.create(
        model=model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=prompt,
    )
    # 返回模型的输出文本     （返回模型的输出文本）
    return response.output_text


# 创建 FastAPI 应用     （创建 FastAPI 应用）
app = FastAPI(title="rag_api_demo", version="0.1.0")

cors_origins = [
    origin.strip()
    for origin in os.getenv("RAG_API_CORS_ORIGINS", "").split(",")
    if origin.strip()
]
if not cors_origins:
    cors_origins = sorted(DEFAULT_CORS_ORIGINS)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 将运行时状态挂在 app.state，方便在多个 endpoint 间共享。     （将运行时状态挂在 app.state，方便在多个 endpoint 间共享。）
# 将运行时状态挂在 app.state，方便在多个 endpoint 间共享。
app.state.client = None
# 将运行时状态挂在 app.state，方便在多个 endpoint 间共享。
app.state.docs_dir = None
# 将运行时状态挂在 app.state，方便在多个 endpoint 间共享。
app.state.chunks = []
# 将运行时状态挂在 app.state，方便在多个 endpoint 间共享。


# 初始化或重新加载服务状态：扫描文档目录并缓存 chunks 与客户端实例。
def load_state() -> None:
    # 层次: 状态管理层 — 初始化或重新加载服务状态：扫描文档目录并缓存 chunks 与客户端实例。
    """初始化或重新加载服务状态：扫描文档目录并缓存 chunks 与客户端实例。"""
    docs_dir = get_docs_dir()
    chunks = build_chunks(docs_dir)
    # 如果 chunks 为空，则抛出异常     （如果 chunks 为空，则抛出异常）
    if not chunks:
        raise RuntimeError("No readable .md, .txt, or .pdf files were found in docs directory.")
    # Cache the parsed chunks in memory so each request does not rescan the directory.
    # 缓存解析后的 chunks 在内存中，以便每个请求不需要重新扫描目录。
    mode = resolve_mode()
    # 如果 mode 为 "real"，则构建客户端     （如果 mode 为 "real"，则构建客户端）
    if mode == "real":
        app.state.client = build_client()
    # 如果 mode 为 "mock"，则客户端为空     （如果 mode 为 "mock"，则客户端为空）
    else:
        app.state.client = None
    # 将运行时状态挂在 app.state，方便在多个 endpoint 间共享。
    app.state.docs_dir = docs_dir
    # 将运行时状态挂在 app.state，方便在多个 endpoint 间共享。
    app.state.chunks = chunks
    # 将运行时状态挂在 app.state，方便在多个 endpoint 间共享。

def ensure_state_loaded() -> None:
    """按需初始化服务状态，避免应用启动时就预热。"""
    if getattr(app.state, "chunks", None) is None or getattr(app.state, "docs_dir", None) is None:
        load_state()


@app.get("/")
def root() -> dict[str, object]:
    """根路径提示，避免手动验证时把 404 误判为启动失败。"""
    return {
        "service": "rag_api_demo",
        "status": "ok",
        "message": "Service is running. Use /health, /ask, and /reload.",
        "endpoints": ["/health", "/ask", "/reload"],
    }


# 健康检查接口，返回当前 docs 目录和 chunk 数量。
@app.get("/health")
def health() -> dict[str, object]:
    # 层次: 健康检查层 — 健康检查接口，返回当前 docs 目录和 chunk 数量。
    """健康检查接口，返回当前 docs 目录和 chunk 数量。"""
    ensure_state_loaded()
    return {
        # 返回状态     （返回状态）
        "status": "ok",
        "docs_dir": str(app.state.docs_dir),
        "chunk_count": len(app.state.chunks),
    }


# 手动触发重新加载文档目录并返回新的 chunk 计数。
@app.post("/reload", response_model=ReloadResponse)
def reload_docs() -> ReloadResponse:
    """手动触发重新加载文档目录并返回新的 chunk 计数。"""
    # 层次: 重载管理层 — 手动触发重新加载文档目录并返回新的 chunk 计数。
    try:
        load_state()
    # 如果异常，则抛出异常     （如果异常，则抛出异常）
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    # 返回 ReloadResponse     （返回 ReloadResponse）
    return ReloadResponse(
        # 返回 docs 目录     （返回 docs 目录）
        docs_dir=str(app.state.docs_dir),
        # 返回 chunk 数量     （返回 chunk 数量）
        chunk_count=len(app.state.chunks),
    )


# 对外 API：接收问题、检索文档并返回模型回答与来源信息。
@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    """对外 API：接收问题、检索文档并返回模型回答与来源信息。"""
    # 层次: 业务接口层 — 对外 API：接收问题、检索文档并返回模型回答与来源信息。
    ensure_state_loaded()
    # 检索文档     （检索文档）
    top_chunks = retrieve(request.question, app.state.chunks)
    # 构建上下文     （构建上下文）
    context = build_context(top_chunks)
    # 回答问题     （回答问题） 
    try:
        # 回答问题     （回答问题） （调用模型回答问题）    
        answer = answer_question(
            app.state.client,
            request.model,
            request.question,
            context,
            top_chunks=top_chunks,
        )
    # 如果异常，则抛出异常     （如果异常，则抛出异常）
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    # 返回 AskResponse     （返回 AskResponse）
    return AskResponse(
        answer=answer,
        model=request.model,
        docs_dir=str(app.state.docs_dir),
        source_count=len(top_chunks),
        # 返回来源信息     （返回来源信息）
        sources=[
            SourceItem(source_label=chunk.source_label, score=chunk.score)
            for chunk in top_chunks
        ],
        # 返回来源信息     （返回来源信息） 
    )
