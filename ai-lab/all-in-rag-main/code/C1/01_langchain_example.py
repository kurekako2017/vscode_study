"""
文件功能概述：`code/C1/01_langchain_example.py` 主要是 01LangChain示例，这个文件里有 0 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 这个文件没有独立类或函数，主要靠模块级代码直接执行。
"""

import os
from pathlib import Path
# hugging face镜像设置，如果国内环境无法使用启用该设置
# os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import FakeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
# 加载环境变量，优先使用 .env 文件中的配置，失败则继续使用系统环境变量
load_dotenv()

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

# 提示词模板
prompt = ChatPromptTemplate.from_template("""请根据下面提供的上下文信息来回答问题。
请确保你的回答完全基于这些上下文。
如果上下文中没有足够的信息来回答问题，请直接告知：“抱歉，我无法根据提供的上下文找到相关信息来回答此问题。”

上下文:
{context}

问题: {question}

回答:"""
                                          )

# 配置大语言模型

# 使用 OpenRouter
api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("请先设置 OPENROUTER_API_KEY（或 OPENAI_API_KEY）环境变量")

llm = ChatOpenAI(
    model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
    temperature=0.7,
    max_tokens=4096,
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# llm = ChatOpenAI(
#     model="openai/gpt-4o-mini",
#     temperature=0.7,
#     max_tokens=4096,
#     api_key=api_key,
#     base_url="https://openrouter.ai/api/v1"
# )

# 用户查询
question = "文中举了哪些例子？"

# 在向量存储中查询相关文档
retrieved_docs = vectorstore.similarity_search(question, k=3)
# 将检索到的文档内容拼接成上下文，并调用大语言模型生成答案
docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
# 调用大语言模型生成答案
answer = llm.invoke(prompt.format(question=question, context=docs_content))
print(answer)
