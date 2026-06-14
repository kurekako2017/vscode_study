"""
文件功能概述：`code/C4/text2sql/sql_generator.py` 主要是 SQLgenerator，这个文件里有 1 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `SimpleSQLGenerator`：功能概述：这个类是 `SimpleSQLGenerator`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 api_key，再调用 ChatOpenAI、os.getenv 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `generate_sql`：先接收输入参数 user_query, knowledge_results，接着根据条件分支选择不同处理路径，再调用 self._build_context、self.llm.invoke、response.content.strip 等内部步骤完成主要工作，最后返回结果。 3. `fix_sql`：先接收输入参数 original_sql, error_message, knowledge_results，接着根据条件分支选择不同处理路径，再调用 self._build_context、self.llm.invoke、response.content.strip 等内部步骤完成主要工作，最后返回结果。 4. `_build_context`：先接收输入参数 knowledge_results，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 ddl_info.append、join、qsql_examples.append 等内部步骤完成主要工作，最后返回结果。
"""

import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from openrouter_env import (
    resolve_openrouter_api_key,
    resolve_openrouter_base_url,
    resolve_openrouter_model,
)


class SimpleSQLGenerator:
    """
    功能概述：这个类是 `SimpleSQLGenerator`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 api_key，再调用 ChatOpenAI、os.getenv 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `generate_sql`：先接收输入参数 user_query, knowledge_results，接着根据条件分支选择不同处理路径，再调用 self._build_context、self.llm.invoke、response.content.strip 等内部步骤完成主要工作，最后返回结果。
    3. `fix_sql`：先接收输入参数 original_sql, error_message, knowledge_results，接着根据条件分支选择不同处理路径，再调用 self._build_context、self.llm.invoke、response.content.strip 等内部步骤完成主要工作，最后返回结果。
    4. `_build_context`：先接收输入参数 knowledge_results，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 ddl_info.append、join、qsql_examples.append 等内部步骤完成主要工作，最后返回结果。
    """
    
    def __init__(self, api_key: str = None):  # 中文名称：初始化
        self.llm = ChatOpenAI(
            model=resolve_openrouter_model(),
            temperature=0,
            api_key=(api_key or resolve_openrouter_api_key()),
            base_url=resolve_openrouter_base_url()
        )
    
    def generate_sql(self, user_query: str, knowledge_results: List[Dict[str, Any]]) -> str:  # 中文名称：generateSQL
        """生成SQL语句"""
        # 构建上下文
        context = self._build_context(knowledge_results)
        
        # 构建提示
        prompt = f"""你是一个SQL专家。请根据以下信息将用户问题转换为SQL查询语句。

数据库信息：
{context}

用户问题：{user_query}

要求：
1. 只返回SQL语句，不要包含任何解释
2. 确保SQL语法正确
3. 使用上下文中提供的表名和字段名
4. 如果需要JOIN，请根据表结构进行合理关联

SQL语句："""

        response = self.llm.invoke(prompt)
        
        # 清理SQL语句
        sql = response.content.strip()
        if sql.startswith("```sql"):
            sql = sql[6:]
        if sql.startswith("```"):
            sql = sql[3:]
        if sql.endswith("```"):
            sql = sql[:-3]
        
        return sql.strip()
    
    def fix_sql(self, original_sql: str, error_message: str, knowledge_results: List[Dict[str, Any]]) -> str:  # 中文名称：fixSQL
        """修复SQL语句"""
        context = self._build_context(knowledge_results)
        
        prompt = f"""请修复以下SQL语句的错误。

数据库信息：
{context}

原始SQL：
{original_sql}

错误信息：
{error_message}

请返回修复后的SQL语句（只返回SQL，不要解释）："""

        response = self.llm.invoke(prompt)
        
        # 清理SQL语句
        fixed_sql = response.content.strip()
        if fixed_sql.startswith("```sql"):
            fixed_sql = fixed_sql[6:]
        if fixed_sql.startswith("```"):
            fixed_sql = fixed_sql[3:]
        if fixed_sql.endswith("```"):
            fixed_sql = fixed_sql[:-3]
        
        return fixed_sql.strip()
    
    def _build_context(self, knowledge_results: List[Dict[str, Any]]) -> str:  # 中文名称：构建context
        """构建上下文信息"""
        context = ""
        
        # 按类型分组
        ddl_info = []
        qsql_examples = []
        descriptions = []
        
        for result in knowledge_results:
            if result["type"] == "ddl":
                ddl_info.append(result["content"])
            elif result["type"] == "qsql":
                qsql_examples.append(result["content"])
            elif result["type"] == "description":
                descriptions.append(result["content"])
        
        # 构建上下文
        if ddl_info:
            context += "=== 表结构信息 ===\n"
            context += "\n".join(ddl_info) + "\n\n"
        
        if descriptions:
            context += "=== 表和字段描述 ===\n"
            context += "\n".join(descriptions) + "\n\n"
        
        if qsql_examples:
            context += "=== 查询示例 ===\n"
            context += "\n".join(qsql_examples) + "\n\n"
        
        return context 
