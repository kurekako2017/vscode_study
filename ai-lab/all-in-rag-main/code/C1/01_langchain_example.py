"""
文件功能概述：`code/C1/01_langchain_example.py` 主要是 01LangChain示例，这个文件里有 0 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 这个文件没有独立类或函数，主要靠模块级代码直接执行。
"""

import contextlib
import os
import socket
import sys
from pathlib import Path
from urllib.parse import urlparse
# hugging face镜像设置，如果国内环境无法使用启用该设置
# os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
from dotenv import find_dotenv, load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from openrouter_env import (
    describe_openrouter_runtime,
    resolve_openrouter_api_key,
    resolve_openrouter_base_url,
    resolve_openrouter_model,
)
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import FakeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
# 加载环境变量，优先使用当前项目能找到的 .env，再回退到系统环境变量
load_dotenv(find_dotenv(usecwd=True))


@contextlib.contextmanager
def _without_local_code_path():
    """临时移除仓库内的 `code/` 路径，避免本地 mock 模块遮蔽官方包。"""
    code_path = str(ROOT / "code")
    original_sys_path = list(sys.path)
    try:
        sys.path = [item for item in sys.path if item != code_path]
        yield
    finally:
        sys.path = original_sys_path


def _build_openrouter_client():
    """使用工作区 `.env` 中的 OpenRouter 配置构建客户端。"""
    api_key = resolve_openrouter_api_key()
    if not api_key:
        raise ValueError(
            "请先在工作区 .env 中设置 OPENROUTER_API_KEY，"
            "或把 openRouter/openRouterAPI 导出为终端环境变量"
        )

    base_url = resolve_openrouter_base_url()
    parsed_url = urlparse(base_url)
    host = parsed_url.hostname
    if host:
        try:
            socket.gethostbyname(host)
        except socket.gaierror as exc:
            proxy_hint = ""
            if os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY"):
                proxy_hint = " 检查你的代理是否对当前终端生效。"
            raise SystemExit(
                f"无法解析 OpenRouter 域名: {host}。请检查 DNS 或网络代理。{proxy_hint}"
            ) from exc

    with _without_local_code_path():
        from openai import OpenAI as OpenAIClient

    return OpenAIClient(api_key=api_key, base_url=base_url)

# 定义示例文件路径
ROOT = Path(__file__).resolve().parents[2]
# 示例文件路径
markdown_path = ROOT / "data/C1/markdown/easy-rl-chapter1.md"

if not markdown_path.exists():
    raise FileNotFoundError(f"找不到示例文件: {markdown_path}")

# 加载本地markdown文件，避免 unstructured 触发额外的在线下载
docs = [Document(page_content=markdown_path.read_text(encoding="utf-8"), metadata={"source": str(markdown_path)})]

# 文本分块
text_splitter = RecursiveCharacterTextSplitter()
# 文本分块结果是一个 Document 对象列表，每个 Document 包含一个文本块和相关元数据（如来源文件路径）。
chunks = text_splitter.split_documents(docs)

# 中文嵌入模型，优先使用本地可用的 HuggingFace 模型，失败则降级到离线假向量
try:
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh-v1.5",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
except Exception as exc:
    print(f"警告: 无法加载 HuggingFace 嵌入模型，改用离线 FakeEmbeddings: {exc}")
    embeddings = FakeEmbeddings(size=384)
  
# 构建向量存储
vectorstore = InMemoryVectorStore(embeddings)
# 将分块结果添加到向量存储中，每个文本块会被转换成向量并存储，以便后续的相似度搜索使用。
vectorstore.add_documents(chunks)

# 用户查询
question = "文中举了哪些例子？"

# 在向量存储中查询相关文档
retrieved_docs = vectorstore.similarity_search(question, k=min(3, len(chunks)))
# 将检索到的文档内容拼接成上下文，并调用大语言模型生成答案
docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)[:12000]

prompt_text = f"""请根据下面提供的上下文信息来回答问题。
请确保你的回答完全基于这些上下文。
如果上下文中没有足够的信息来回答问题，请直接告知：“抱歉，我无法根据提供的上下文找到相关信息来回答此问题。”

上下文:
{docs_content}

问题: {question}

回答:"""

client = _build_openrouter_client()
print(f"使用模型: {describe_openrouter_runtime()}")
try:
    response = client.chat.completions.create(
        model=resolve_openrouter_model(),
        messages=[
            {
                "role": "system",
                "content": "你是一个严格基于上下文回答的助手，只能使用提供的文档内容作答。",
            },
            {"role": "user", "content": prompt_text},
        ],
        temperature=0.2,
        max_tokens=800,
    )
    answer = response.choices[0].message.content
    if not answer:
        raise RuntimeError("OpenRouter 返回了空内容")
except Exception as exc:
    raise SystemExit(
        f"OpenRouter 请求失败: {exc}"
    ) from exc

print(answer)
