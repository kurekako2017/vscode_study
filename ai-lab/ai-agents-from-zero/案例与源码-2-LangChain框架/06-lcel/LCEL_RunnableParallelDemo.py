"""
【案例】并行链：同时运行多条子链，汇总结果

对应教程章节：第 15 章 - LCEL 与链式调用 → 4.4 RunnableParallel（并行链）

知识点速览：
- `RunnableParallel` 解决的是“同一输入，要同时跑多条子链”的问题。
- 结果会以 `dict` 形式汇总返回，键名对应并行结构里的键，值对应每条子链的输出。
- 除了显式写 `RunnableParallel({...})`，LCEL 里也常直接用字典表达并行结构；并行完成后，还可以继续把这个字典交给后续链做总结或比较。
"""

import os

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from loguru import logger

from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

def build_chat_model():
    """优先 OpenRouter free；如果没有 key，再回退到本地 Ollama。"""
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    if openrouter_api_key:
        try:
            model = init_chat_model(
                model=os.getenv("OPENROUTER_MODEL", "openrouter/free"),
                model_provider="openai",
                api_key=openrouter_api_key,
                base_url="https://openrouter.ai/api/v1",
            )
            model.invoke("ping")
            return model
        except Exception as exc:
            print(f"OpenRouter 不可用，切换到本地 Ollama：{exc}")

    try:
        from langchain_ollama import ChatOllama
    except ImportError as exc:
        raise RuntimeError(
            "未配置 OPENROUTER_API_KEY，且本地 Ollama 依赖不可用；请配置 OpenRouter free 或安装 langchain-ollama。"
        ) from exc

    return ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "qwen2.5:7b"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    )


model = build_chat_model()

# 子链 1：中文简短介绍
prompt1 = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个知识渊博的计算机专家，请用中文简短回答"),
        ("human", "请简短介绍什么是{topic}"),
    ]
)
parser1 = StrOutputParser()
chain1 = prompt1 | model | parser1

# 子链 2：英文简短介绍（与 chain1 同结构，仅提示词语言不同）
prompt2 = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个知识渊博的计算机专家，请用英文简短回答"),
        ("human", "请简短介绍什么是{topic}"),
    ]
)
parser2 = StrOutputParser()
chain2 = prompt2 | model | parser2

# RunnableParallel：同一输入会同时喂给多个子链，结果按键汇总为 dict
parallel_chain = RunnableParallel({"chinese": chain1, "english": chain2})

# 一次 invoke，返回 {"chinese": "...", "english": "..."}
result = parallel_chain.invoke({"topic": "langchain"})
logger.info(result)

# 可选：打印并行链的 ASCII 图结构，便于理解“并行节点 + 汇总输出”的数据流
parallel_chain.get_graph().print_ascii()

"""
【输出示例】
2026-03-06 10:28:37.853 | INFO     | __main__:<module>:54 - {'chinese': 'LangChain 是一个开源框架，用于构建基于大语言模型（LLM）的应用程序。它提供模块化组件（如链（Chains）、提示模板、记忆（Memory）、工具（Tools）和数据连接器），帮助开发者轻松实现提示工程、外部数据检索（RAG）、多步推理、对话状态管理等功能，提升 LLM 应用的可控性、可扩展性和实用性。', 'english': 'LangChain is a framework for developing applications powered by large language models (LLMs), enabling chaining of prompts, LLM calls, and external tools (e.g., APIs, databases) to build complex, stateful, and context-aware workflows.'}
            +--------------------------------+
            | Parallel<chinese,english>Input |
            +--------------------------------+
                   ***               ***
                ***                     ***
              **                           **
+--------------------+              +--------------------+
| ChatPromptTemplate |              | ChatPromptTemplate |
+--------------------+              +--------------------+
           *                                   *
           *                                   *
           *                                   *
    +------------+                      +------------+
    | ChatOpenAI |                      | ChatOpenAI |
    +------------+                      +------------+
           *                                   *
           *                                   *
           *                                   *
  +-----------------+                 +-----------------+
  | StrOutputParser |                 | StrOutputParser |
  +-----------------+                 +-----------------+
                   ***               ***
                      ***         ***
                         **     **
            +---------------------------------+
            | Parallel<chinese,english>Output |
            +---------------------------------+
"""
