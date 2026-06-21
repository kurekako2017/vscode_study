"""rag_api_demo: 使用 FastAPI 提供的最小 RAG API 服务示例。

功能概览：
- 扫描指定目录（支持 .md/.txt/.pdf），并把文档切分为分块
- 基于关键词重合度做本地检索，取前几个结果作为上下文
- 将检索到的上下文发送给模型，并返回带来源的回答

处理特点：
- 默认按需加载，第一次访问接口时才构建内存状态
- 支持模拟 / 真实两种模式，方便本地学习和联调
- 适合和 React 前端、Spring Boot 客户端一起做端到端演示

学习地图：
- 运行命令：
  - `uvicorn main:app --reload --port 8000`
  - `curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"question":"请总结文档重点"}'`
- 输入输出：
  - 输入：HTTP JSON 请求（`question`、`model`）+ 本地 `docs` 目录
  - 输出：结构化 JSON（`answer`、`sources`、`source_count`）
- 改造练习点：
  - 新增 `/config` 接口暴露当前分块参数
  - 为 `/ask` 增加 `top_k` 可选参数
  - 将 `load_state` 改为可热更新的服务层对象
"""

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # 跨域中间件    
from openai import OpenAI
from pydantic import BaseModel, Field  # 请求和响应模型校验
from pypdf import PdfReader

for _parent in Path(__file__).resolve().parents:
    if (_parent / "llm_runtime.py").exists():
        sys.path.insert(0, str(_parent))
        break
from llm_runtime import build_fallback_client

# 默认模型名。
DEFAULT_MODEL = "gpt-5"
DEFAULT_DOCS_DIR = "."
# OpenRouter 兼容服务默认基址。
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
SUPPORTED_EXTENSIONS = {".md", ".txt", ".pdf"}

# 每个分块的大小和重叠长度。
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200

# 每次检索返回的分块数量。
TOP_K = 4

# 系统提示词：只允许基于检索到的上下文回答。
SYSTEM_INSTRUCTIONS = (
    "你是一个文档问答助手。"
    "只能根据提供的检索上下文回答。"
    "如果上下文不足，要明确说明。"
    "尽量在回答中提到来源标签。"
)

# 本地前端默认允许访问的来源。
DEFAULT_CORS_ORIGINS = {
    "http://localhost:3000",
    "http://localhost:4173",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:4173",
    "http://127.0.0.1:5173",
}


@dataclass
class Chunk:
    """文档切分后的片段对象，包含来源标签、内容与得分。"""
    # 来源标签，用于标识片段来自哪个文档。
    source_label: str
    # 片段内容。
    content: str
    # 得分，用于排序。
    score: int = 0  


class AskRequest(BaseModel):
    """`/ask` 请求体：问题文本 + 可选模型名。"""

    question: str = Field(min_length=1, description="关于本地文档的问题。")
    model: str = Field(default=DEFAULT_MODEL, description="要使用的模型名。")


class SourceItem(BaseModel):
    """来源条目，用于告诉调用方答案依据来自哪些文档片段。"""

    source_label: str
    score: int


class AskResponse(BaseModel):
    """`/ask` 响应体：答案正文 + 来源摘要。"""

    answer: str
    model: str
    docs_dir: str
    source_count: int
    sources: list[SourceItem]


class ReloadResponse(BaseModel):
    """`/reload` 响应体：用于确认文档索引是否已刷新。"""

    docs_dir: str
    chunk_count: int


def build_client() -> OpenAI:
    """根据环境变量创建 OpenAI 兼容客户端，缺失时抛出异常。"""

    return build_fallback_client()


def resolve_mode() -> str:
    """决定服务运行模式：`mock` 或 `real`。"""

    if os.getenv("RAG_API_MOCK") == "1":
        return "mock"
    return "real"


def build_mock_answer(question: str, top_chunks: list[Chunk]) -> str:
    """生成本地学习用的模拟回答。"""

    lines = ["[模拟模式]", f"问题：{question}"]
    lines.append(f"检索到的片段数量：{len(top_chunks)}")
    lines.append("练习建议：将关键词检索替换为向量检索，并在真实模式下测试。")
    return "\n".join(lines)


def get_docs_dir() -> Path:
    """获取并校验用于 RAG 的文档目录。"""

    # 从环境变量读取文档目录，默认使用当前目录。
    docs_dir = os.getenv("RAG_API_DOCS_DIR", DEFAULT_DOCS_DIR)
    path = Path(docs_dir).resolve()
    if not path.exists() or not path.is_dir():
        raise RuntimeError("RAG_API_DOCS_DIR 必须指向一个已存在的目录。")
    return path


def iter_text_files(base_dir: Path) -> list[Path]:
    """递归列出支持类型的文件路径，并返回排序结果。"""

    # 先收集所有支持的文本文件。
    files = []
    for path in base_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path)
    return sorted(files)


def read_document_text(file_path: Path) -> str:
    """按文件类型读取文本；PDF 使用 pypdf 做基本提取。"""

    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        # PDF 按页提取文本。
        reader = PdfReader(str(file_path))
        parts: list[str] = []  # 初始化片段列表。
        for page in reader.pages:
            text = page.extract_text()
            if text:  # 如果文本不为空，则添加到片段列表。
                parts.append(text)  # 添加到片段列表。
        return "\n".join(parts)  # 返回片段列表。
    if suffix in {".txt", ".md"}:  # 如果文件类型为 .txt 或 .md，则直接读取。
        # 普通文本直接读取。
        return file_path.read_text(encoding="utf-8")  # 读取文件文本。
    raise ValueError(f"不支持的文件类型：{suffix}")  # 抛出异常。
# 层次: 索引构建层 — 文本切分为可检索的 chunk
def chunk_text(text: str) -> list[str]:
    """把文本切分为带重叠的 chunk，保留跨块上下文。"""

    # 统一换行并清理首尾空白。
    normalized = text.replace("\r\n", "\n").strip()
    if not normalized:  # 如果文本为空，则返回空列表。  
        return []  # 返回空列表。

    # 使用滑动窗口切块。
    chunks = []  # 初始化片段列表。
    start = 0  # 初始化 start 为 0。
    while start < len(normalized):  # 遍历文本。    
        end = min(len(normalized), start + CHUNK_SIZE)  # 计算 end。
        chunks.append(normalized[start:end])  # 添加到片段列表。
        if end >= len(normalized):  # 如果 end 大于等于 normalized 的长度，则退出循环。
            break  # 退出循环。
        start = end - CHUNK_OVERLAP  # 计算 start。
    return chunks  # 返回片段列表。


def build_chunks(base_dir: Path) -> list[Chunk]:
    """读取文档目录并构建带来源标签的 chunk 列表。"""

    # 收集所有可用分块。
    chunks: list[Chunk] = []
    for file_path in iter_text_files(base_dir):  # 遍历所有可用分块。
        try:
            text = read_document_text(file_path)  # 读取文件文本。
        except (UnicodeDecodeError, ValueError):
            continue  # 继续下一个文件。    

        relative = file_path.relative_to(base_dir)  # 计算文件相对路径。
        for index, part in enumerate(chunk_text(text), start=1):  # 遍历切分后的文本。
            chunks.append(Chunk(source_label=f"{relative}#chunk{index}", content=part))  # 添加到片段列表。
    return chunks  # 返回片段列表。


def tokenize(text: str) -> set[str]:
    """简单分词函数，支持英文、数字和部分中日韩字符。"""

    # 把文本切成可用于匹配的记号集合。
    return set(re.findall(r"[A-Za-z0-9_\-\u4e00-\u9fff\u3040-\u30ff]+", text.lower()))  # 返回记号集合。


def retrieve(question: str, chunks: list[Chunk]) -> list[Chunk]:
    """基于关键词重合度进行简单检索，并返回 top-k。"""

    # 先把问题切成记号，方便和分块对齐。
    question_tokens = tokenize(question)
    ranked: list[Chunk] = []

    for chunk in chunks:  # 遍历片段列表。  
        chunk_tokens = tokenize(chunk.content)
        score = len(question_tokens & chunk_tokens)  # 计算关键词重合度。
        if score > 0:  # 如果关键词重合度大于0，则添加到片段列表。
            ranked.append(Chunk(chunk.source_label, chunk.content, score))  # 添加到片段列表。

    ranked.sort(key=lambda item: (-item.score, item.source_label))  # 按得分和来源标签排序。
    return ranked[:TOP_K]  # 返回前TOP_K个片段。


def build_context(top_chunks: list[Chunk]) -> str:
    """把检索到的 chunk 拼接为模型可读的上下文。"""

    if not top_chunks:
        return "没有检索到相关的本地文档片段。"

    # 按来源标签拼接上下文。
    parts = []
    for chunk in top_chunks:
        parts.append(f"[SOURCE: {chunk.source_label}]\n{chunk.content}")
    return "\n\n".join(parts)


def answer_question(
    client: OpenAI | None,  # 模型客户端。
    model: str,  # 模型名称。
    question: str,  # 问题。
    context: str,  # 上下文。
    top_chunks: list[Chunk] | None = None,  # 来源信息。
) -> str:
    """基于检索上下文回答问题；模拟模式直接返回本地结果。"""

    # 先判断当前是模拟模式还是正式模式。
    mode = resolve_mode()  # 运行模式。
    if mode == "mock":
        return build_mock_answer(question, top_chunks or [])  # 构建模拟回答。

    # 把问题和上下文组装成模型输入。
    prompt = (
        f"问题：\n{question}\n\n"
        f"检索上下文：\n{context}\n\n"
        "只能根据检索上下文回答。"
        "如果答案没有被上下文充分支持，要明确说明。"
    )
    # 调用模型并返回输出文本。
    response = client.responses.create(
        model=model,  # 模型名称。
        instructions=SYSTEM_INSTRUCTIONS,  # 系统提示词。
        input=prompt,  # 输入。
    )
    return response.output_text  # 输出文本。   


app = FastAPI(title="rag_api_demo", version="0.1.0")  # 创建 FastAPI 应用。

# 从环境变量读取前端来源配置。
cors_origins = [
    origin.strip()
    for origin in os.getenv("RAG_API_CORS_ORIGINS", "").split(",")
    if origin.strip()
]
if not cors_origins:  # 如果允许访问的来源为空，则使用默认允许访问的来源。  
    cors_origins = sorted(DEFAULT_CORS_ORIGINS)  # 默认允许访问的来源。

# 注册跨域中间件，方便前端联调。
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,  # 允许访问的来源。
    allow_credentials=True,  # 允许跨域请求。
    allow_methods=["*"],  # 允许所有方法。
    allow_headers=["*"],  # 允许所有头。
)

# 运行时状态放到应用状态对象里，方便各接口共享。
app.state.client = None  # 模型客户端。
app.state.docs_dir = None  # 文档目录。
app.state.chunks = []  # 片段列表。


def load_state() -> None:
    """初始化或重新加载服务状态。"""

    # 先加载文档目录并生成分块。
    docs_dir = get_docs_dir()
    chunks = build_chunks(docs_dir)  # 构建片段列表。
    if not chunks:  # 如果片段列表为空，则抛出异常。    
        raise RuntimeError("文档目录中没有可读取的 .md、.txt 或 .pdf 文件。")  # 文档目录中没有可读取的 .md、.txt 或 .pdf 文件。

    # 根据运行模式决定是否创建真实客户端。
    mode = resolve_mode()  # 运行模式。 
    if mode == "real":
        app.state.client = build_client()  # 创建真实客户端。
    else:
        app.state.client = None  # 创建模拟客户端。

    app.state.docs_dir = docs_dir  # 文档目录。
    app.state.chunks = chunks  # 片段列表。


def ensure_state_loaded() -> None:
    """按需初始化服务状态，避免启动时就预热索引。"""

    # 分块列表或文档目录为空时才加载。
    if getattr(app.state, "chunks", None) is None or getattr(app.state, "docs_dir", None) is None:
        load_state()  # 加载服务状态。  


@app.get("/")
def root() -> dict[str, object]:
    """根路径提示，避免把 404 误判为启动失败。"""

    # 返回服务基本信息。
    return {
        "service": "rag_api_demo",  # 服务名称。
        "status": "ok",  # 状态。
        "message": "Service is running. Use /health, /ask, and /reload.",  # 消息。
        "endpoints": ["/health", "/ask", "/reload"],  # 端点。
    }


@app.get("/health")
def health() -> dict[str, object]:
    """健康检查接口，返回当前文档目录和 chunk 数量。"""

    # 按需加载后再返回运行状态。
    ensure_state_loaded()
    # 返回当前文档目录和片段数量。
    return {
        "status": "ok",  # 状态。
        "docs_dir": str(app.state.docs_dir),  # 文档目录。
        "chunk_count": len(app.state.chunks),  # 片段数量。
    }


@app.post("/reload", response_model=ReloadResponse)
def reload_docs() -> ReloadResponse:
    """手动触发重新加载文档目录，并返回新的 chunk 数量。"""

    # 重新构建服务状态，失败则返回 500。
    try:
        load_state()  # 重新构建服务状态。
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    # 返回新的文档目录和片段数量。
    return ReloadResponse(
        docs_dir=str(app.state.docs_dir),  # 文档目录。
        chunk_count=len(app.state.chunks),
    )

    # 对外 API：接收问题、检索文档并返回模型回答与来源信息。
@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    """对外 API：接收问题、检索文档并返回模型回答与来源信息。"""

    # 先确保状态已加载，再执行检索和问答。
    ensure_state_loaded()
    top_chunks = retrieve(request.question, app.state.chunks)
    context = build_context(top_chunks)  # 构建上下文。

    # 调用回答函数生成最终答案。
    try:
        answer = answer_question(
            app.state.client,  # 模型客户端。
            request.model,  # 模型名称。
            request.question,  # 问题。
            context,  # 上下文。
            top_chunks=top_chunks,  # 来源信息。
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    # 返回模型回答与来源信息。
    return AskResponse(
        answer=answer,  # 模型回答。
        model=request.model,  # 模型名称。
        docs_dir=str(app.state.docs_dir),  # 文档目录。
        source_count=len(top_chunks),  # 来源数量。
        sources=[
            SourceItem(source_label=chunk.source_label, score=chunk.score)  # 来源信息。
            for chunk in top_chunks
        ],
    )
