"""
【案例】标准/工程化写法：用 LangChain 调用大模型（DeepSeek 优先，OpenRouter free 自动兜底）

对应教程章节：第 10 章 - LangChain 快速上手与 HelloWorld → 6、实战：企业级封装与流式输出

本案例演示从零到一的完整工程化写法：
- 先尝试使用 DeepSeek 官方接口通过 LangChain 发问，掌握 invoke（一次性返回）与 stream（流式返回）两种调用方式。
- 如果 DeepSeek 遇到认证失败、余额不足、网络不可用等问题，自动切换到 OpenRouter 的免费模型路由，保证你能继续把案例跑通。
- 将「初始化模型」封装成函数便于复用；用 .env 存密钥、logging 打日志、try/except 区分错误，符合正式项目习惯。
- 运行前在项目根目录配置 .env 中的 DEEPSEEK_API_KEY（可选）和 OPENROUTER_API_KEY（可选但建议准备），执行：python3 案例与源码-2-LangChain框架/01-helloworld/StandardDesc.py

补充说明：
- 为了让工程化示例更直观，这里继续使用很多同学在旧资料里更常见的 `ChatOpenAI` 写法；OpenRouter 与 DeepSeek 一样都走 OpenAI 兼容接口。
- 当前脚本的核心目标是“先学会把链路跑通”，所以默认会优先走云端，云端失败后自动回落到 OpenRouter 免费模型路由。
"""

# ========== 1. 导入与环境 ==========
# 下面每一行都是「把别人写好的功能拿进来」，后面才能用。

import os  # Python 自带：用来读「环境变量」（如 API 密钥）

# load_dotenv：从项目根目录的 .env 文件里，把变量加载到「环境」里，之后用 os.getenv("变量名") 就能读到。
# 把密钥写在 .env 里而不是代码里，既安全（不把密钥提交到 Git），又方便换环境（开发/生产用不同 .env）。
from dotenv import load_dotenv

# LangChainException：LangChain 在调用模型失败时会抛出的异常类型。
# 在 main() 里用 except LangChainException 单独接住这类错误，就能打出「模型调用失败」的日志，和配置错误、其他未知错误区分开。
from langchain_core.exceptions import LangChainException
from langchain_openai import (
    ChatOpenAI,
)  # 用 OpenAI 兼容接口和模型对话（阿里云等也兼容这个接口）

# 真正执行「从 .env 加载到环境」；encoding='utf-8' 避免 .env 里有中文时乱码。
load_dotenv(encoding="utf-8")

# ----- 日志配置 -----
# logging 是 Python 自带的日志库，不用 pip 安装。用 logger.info() / logger.error() 代替 print，方便区分「普通信息」和「错误」，且可统一格式、写文件等。
# 通过环境变量 LOG_LEVEL 控制输出多少：开发时用 INFO（看得到调试信息），生产时在 .env 里设 LOG_LEVEL=WARNING，就只打警告和错误，减少刷屏。
import logging

_log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, _log_level, logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)  # 当前模块的 logger，后面用 logger.info(...) 即可


# ========== 2. LLM 客户端初始化（封装为函数，便于多处复用） ==========
# 「LLM」= 大语言模型（如通义千问、DeepSeek）。这里把「创建可对话的客户端」封装成一个函数，以后在别处也能直接调 init_llm_client()，不用重复写一长串配置。


def init_llm_client() -> ChatOpenAI:
    """
    初始化 LLM 客户端（封装成函数，提高复用性）。

    Returns:
        ChatOpenAI: 初始化好的「对话客户端」，可以对其调用 .invoke(问题) 或 .stream(问题)。
    """
    api_key = (
        os.getenv("DEEPSEEK_API_KEY")
        or os.getenv("deepseek-api")
        or os.getenv("QWEN_API_KEY")
    )
    if not api_key:
        raise ValueError("未配置 DeepSeek API Key，已准备切换到 OpenRouter free")

    # 创建客户端：指定用哪个模型、密钥、接口地址，以及「回复风格」相关参数。
    llm = ChatOpenAI(
        model="deepseek-v4-flash",  # 使用 DeepSeek 官方 API 推荐模型
        api_key=api_key,
        base_url="https://api.deepseek.com",  # DeepSeek 官方 OpenAI 兼容地址
        temperature=0.7,  # 控制「随机程度」：0 更确定、重复性高；1 更随机、更有创意。一般 0.5～0.8 即可。
        max_tokens=2048,  # 单次回复最多生成多少个 token（约等于字数），防止回复过长或超限。
    )
    return llm


def init_openrouter_client() -> ChatOpenAI:
    """初始化 OpenRouter 客户端，作为 DeepSeek 失败时的免费兜底方案。"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("未配置 OPENROUTER_API_KEY，请先在 .env 中填写 OpenRouter Key")

    model = os.getenv("OPENROUTER_MODEL", "openrouter/free")
    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.7,
        max_tokens=2048,
    )


def choose_runtime_model():
    """
    按「DeepSeek 优先，OpenRouter free 兜底」顺序返回可用模型。

    返回值：
        tuple[模型对象, 模型来源名称]
    """
    deepseek_error = None
    try:
        llm = init_llm_client()
        # 先做一次最小探活，确保不仅是对象创建成功，而且真正能访问到 DeepSeek。
        llm.invoke("ping")
        return llm, "DeepSeek"
    except Exception as e:
        deepseek_error = e
        logger.warning(f"DeepSeek 不可用，切换到 OpenRouter free：{str(e)}")

    openrouter_llm = init_openrouter_client()
    try:
        openrouter_llm.invoke("ping")
        return openrouter_llm, "OpenRouter"
    except Exception as e:
        raise RuntimeError(
            "DeepSeek 与 OpenRouter 都不可用，请先检查：\n"
            "1. DeepSeek API Key 是否有效、账号是否有额度；\n"
            "2. OPENROUTER_API_KEY 是否已配置，且 OpenRouter 账号可用；\n"
            "3. 如果你想强制指定免费模型，可把 OPENROUTER_MODEL 设为 `openrouter/free` 或某个 `:free` 模型。\n"
            f"DeepSeek 原始错误：{deepseek_error}\n"
            f"OpenRouter 原始错误：{e}"
        ) from e


# ========== 3. 主逻辑：invoke（一次性） + stream（流式）两种调用方式 ==========
# 这里把「问问题、拿回答、打日志」都放在 main() 里，并用 try/except 把可能出现的错误分开处理，避免程序一报错就崩掉、且能打出清晰错误信息。


def main():
    """主函数：封装核心逻辑，符合 Python 工程化规范。"""
    try:
        # 先拿到「可对话的客户端」，优先 DeepSeek，失败后切到 OpenRouter
        llm, provider_name = choose_runtime_model()
        logger.info(f"LLM客户端初始化成功，当前使用：{provider_name}")

        # ----- 方式一：invoke（一次性拿完整回复） -----
        # 发一个问题，程序会等模型全部答完，再一次性把 response 给你。适合短问答。
        question = "你是谁"
        try:
            response = llm.invoke(question)
        except Exception as e:
            if provider_name == "DeepSeek":
                logger.warning(f"DeepSeek 本次调用失败，自动切换到 OpenRouter free：{str(e)}")
                llm = init_openrouter_client()
                provider_name = "OpenRouter"
                response = llm.invoke(question)
            else:
                raise
        logger.info(f"问题：{question}")
        logger.info(f"回答：{response.content}")  # .content 里是模型的纯文字回复

        # ----- 方式二：stream（流式，边生成边输出） -----
        # 模型边想边返回，每次返回一小段（chunk），用 for 循环一段段打印，就像打字机效果。适合长文或需要「实时看到输出」的场景。
        print("==================== 以下是流式输出（另一种调用方式）")
        print("*" * 50)
        stream_question = "介绍下 langchain，300字以内"
        try:
            response_stream = llm.stream(stream_question)
        except Exception as e:
            if provider_name == "DeepSeek":
                logger.warning(f"DeepSeek 流式调用失败，自动切换到 OpenRouter free：{str(e)}")
                llm = init_openrouter_client()
                provider_name = "OpenRouter"
                response_stream = llm.stream(stream_question)
            else:
                raise
        for chunk in response_stream:
            print(chunk.content, end="")  # end="" 表示不换行，紧挨着打
        print()  # 流式结束后补一个换行，避免和后续输出粘在一起

    # ----- 异常处理：根据错误类型打不同日志，方便排查 -----
    # try 里面的代码一旦报错，会跳到下面某个 except；若都不匹配，再往上抛。
    except LangChainException as e:
        # 例如：网络失败、API 限流、模型返回异常等，LangChain 会抛出 LangChainException
        logger.error(f"模型调用失败：{str(e)}")
    except Exception as e:
        # 其他没预料到的错误都归到这里，避免程序静默崩溃
        logger.error(f"未知错误：{str(e)}")


# ========== 脚本入口 ==========
# __name__ 是 Python 给每个模块自动设置的内置变量，表示「当前模块的名字」：
#   - 直接运行本文件时（如 python StandardDesc.py），Python 会把 __name__ 设为字符串 "__main__"（前后各两个下划线），
#     于是下面的条件为真，会执行 main()；
#   - 被别的文件 import 时，__name__ 是模块名（如 "01_helloworld.StandardDesc"），不等于 "__main__"，不会执行 main()，
#     避免一导入就自动跑一遍问问题。
#
# 注意：必须写 "__main__" 不能写成 "main"。Python 规定「主程序」的 __name__ 就是 "__main__"，
# 若写成 if __name__ == "main": 则条件永远为假（因为 __name__ 实际是 "__main__"），直接运行脚本时 main() 也不会被调用。
#
# 这里直接写 main() 即可，因为本文件的 main 是普通函数（def main），调用即执行。
# 若 main 是异步函数（async def main），则必须写 asyncio.run(main())，否则协程不会真正运行。
if __name__ == "__main__":
    main()

"""
【输出示例】
2026-03-26 17:30:58,192 - INFO - LLM客户端初始化成功
2026-03-26 17:31:03,613 - INFO - HTTP Request: POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions "HTTP/1.1 200 OK"
2026-03-26 17:31:03,617 - INFO - 问题：你是谁
2026-03-26 17:31:03,617 - INFO - 回答：你好！我是DeepSeek，由深度求索公司创造的AI助手。😊

我是一个纯文本模型，可以帮你解答各种问题、进行对话、协助处理文档等。虽然我不支持多模态识别，但我具有文件上传功能，可以读取和处理图像、txt、pdf、ppt、word、excel等文件中的文字信息。

我的知识截止到2024年7月，拥有128K的上下文处理能力，而且完全免费使用！如果需要最新信息，你可以手动开启联网搜索功能。

有什么我可以帮助你的吗？无论是学习、工作还是日常问题，我都很乐意为你提供帮助！✨
==================== 以下是流式输出（另一种调用方式）
**************************************************
2026-03-26 17:31:04,798 - INFO - HTTP Request: POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions "HTTP/1.1 200 OK"
LangChain 是一个用于开发大语言模型（LLM）应用的开源框架。它核心解决了LLM应用中的两大问题：**数据实时性**（LLM训练数据可能过时）和**领域局限性**（缺乏特定领域知识）。

其核心思想是通过“链”式设计，将LLM与外部数据源和工具连接起来，构建功能更强的应用。主要组件包括：
*   **模型**：兼容多种LLM（如GPT、Claude等）。
*   **提示模板**：管理并优化与LLM的交互提示。
*   **数据检索**：能从外部文档、数据库、网络等获取实时信息。
*   **链**：将多个组件按顺序组合，完成复杂任务（如问答、摘要）。
*   **代理**：让LLM自主选择调用工具（如计算器、搜索引擎）来完成任务。

简而言之，LangChain如同“乐高积木”，帮助开发者快速搭建基于LLM的智能应用，如知识库问答、文档分析、智能客服等，极大地提升了开发效率。
"""
