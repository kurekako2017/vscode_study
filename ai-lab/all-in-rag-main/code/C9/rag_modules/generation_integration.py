"""
文件功能概述：`code/C9/rag_modules/generation_integration.py` 主要是 generationintegration，这个文件里有 1 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `GenerationIntegrationModule`：功能概述：这个类是 `GenerationIntegrationModule`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 model_name, temperature, max_tokens，接着根据条件分支选择不同处理路径，再调用 os.getenv、OpenAI、logger.info 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `generate_adaptive_answer`：先接收输入参数 question, documents，再尝试执行核心处理，出错时进入异常兜底，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 join、doc.page_content.strip、self.client.chat.completions.create 等内部步骤完成主要工作，最后返回结果。 3. `generate_adaptive_answer_stream`：先接收输入参数 question, documents, max_retries，再尝试执行核心处理，出错时进入异常兜底，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 join、range、doc.page_content.strip 等内部步骤完成主要工作，最后返回结果。
"""


import logging
import os
import time
from typing import List

from openai import OpenAI
from langchain_core.documents import Document
from openrouter_env import (
    describe_openrouter_runtime,
    resolve_openrouter_api_key,
    resolve_openrouter_base_url,
    resolve_openrouter_model,
)

logger = logging.getLogger(__name__)

class GenerationIntegrationModule:
    """
    功能概述：这个类是 `GenerationIntegrationModule`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 model_name, temperature, max_tokens，接着根据条件分支选择不同处理路径，再调用 os.getenv、OpenAI、logger.info 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `generate_adaptive_answer`：先接收输入参数 question, documents，再尝试执行核心处理，出错时进入异常兜底，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 join、doc.page_content.strip、self.client.chat.completions.create 等内部步骤完成主要工作，最后返回结果。
    3. `generate_adaptive_answer_stream`：先接收输入参数 question, documents, max_retries，再尝试执行核心处理，出错时进入异常兜底，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 join、range、doc.page_content.strip 等内部步骤完成主要工作，最后返回结果。
    """

    def __init__(self, model_name: str = None, temperature: float = 0.1, max_tokens: int = 2048):  # 中文名称：初始化
        """
        初始化生成集成模块
        """
        self.model_name = model_name or resolve_openrouter_model()
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # 初始化OpenAI客户端（使用OpenRouter）
        api_key = resolve_openrouter_api_key()
        if not api_key:
            raise ValueError("请设置 OPENROUTER_API_KEY，或配置 openRouter/openRouterAPI")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=resolve_openrouter_base_url()
        )

        logger.info("生成模块初始化完成: %s", describe_openrouter_runtime())

    def generate_adaptive_answer(self, question: str, documents: List[Document]) -> str:  # 中文名称：generateadaptiveanswer
        """
        智能统一答案生成
        自动适应不同类型的查询，无需预先分类
        """
        # 构建上下文
        context_parts = []
        
        for doc in documents:
            content = doc.page_content.strip()
            if content:
                # 添加检索层级信息（如果有的话）
                level = doc.metadata.get('retrieval_level', '')
                if level:
                    context_parts.append(f"[{level.upper()}] {content}")
                else:
                    context_parts.append(content)
        
        context = "\n\n".join(context_parts)
        
        # LightRAG风格的统一提示词
        prompt = f"""
        作为一位专业的烹饪助手，请基于以下信息回答用户的问题。

        检索到的相关信息：
        {context}

        用户问题：{question}

        请提供准确、实用的回答。根据问题的性质：
        - 如果是询问多个菜品，请提供清晰的列表
        - 如果是询问具体制作方法，请提供详细步骤
        - 如果是一般性咨询，请提供综合性回答

        回答：
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"LightRAG答案生成失败: {e}")
            return f"抱歉，生成回答时出现错误：{str(e)}"
    
    def generate_adaptive_answer_stream(self, question: str, documents: List[Document], max_retries: int = 3):  # 中文名称：generateadaptiveanswerstream
        """
        LightRAG风格的流式答案生成（带重试机制）
        """
        # 构建上下文
        context_parts = []
        
        for doc in documents:
            content = doc.page_content.strip()
            if content:
                level = doc.metadata.get('retrieval_level', '')
                if level:
                    context_parts.append(f"[{level.upper()}] {content}")
                else:
                    context_parts.append(content)
        
        context = "\n\n".join(context_parts)
        
        # LightRAG风格的统一提示词
        prompt = f"""
        作为一位专业的烹饪助手，请基于以下信息回答用户的问题。

        检索到的相关信息：
        {context}

        用户问题：{question}

        请提供准确、实用的回答。根据问题的性质：
        - 如果是询问多个菜品，请提供清晰的列表
        - 如果是询问具体制作方法，请提供详细步骤
        - 如果是一般性咨询，请提供综合性回答

        回答：
        """
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    stream=True,
                    timeout=60  # 增加超时设置
                )
                
                if attempt == 0:
                    print("开始流式生成回答...\n")
                else:
                    print(f"第{attempt + 1}次尝试流式生成...\n")
                
                full_response = ""
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        yield content  # 使用yield返回流式内容
                
                # 如果成功完成，退出重试循环
                return
                
            except Exception as e:
                logger.warning(f"流式生成第{attempt + 1}次尝试失败: {e}")
                
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2  # 递增等待时间
                    print(f"⚠️ 连接中断，{wait_time}秒后重试...")
                    time.sleep(wait_time)
                    continue
                else:
                    # 所有重试都失败，使用非流式作为后备
                    logger.error(f"流式生成完全失败，尝试非流式后备方案")
                    print("⚠️ 流式生成失败，切换到标准模式...")
                    
                    try:
                        fallback_response = self.generate_adaptive_answer(question, documents)
                        yield fallback_response
                        return
                    except Exception as fallback_error:
                        logger.error(f"后备生成也失败: {fallback_error}")
                        error_msg = f"抱歉，生成回答时出现网络错误，请稍后重试。错误信息：{str(e)}"
                        yield error_msg
                        return 
