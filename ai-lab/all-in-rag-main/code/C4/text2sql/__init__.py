"""
文件功能概述：`code/C4/text2sql/__init__.py` 主要是 初始化，这个文件里有 0 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 这个文件没有独立类或函数，主要靠模块级代码直接执行。
"""


__version__ = "1.0.0"
__author__ = "RAG Team"

from .knowledge_base import SimpleKnowledgeBase
from .sql_generator import SimpleSQLGenerator
from .text2sql_agent import SimpleText2SQLAgent

__all__ = [
    "SimpleKnowledgeBase",
    "SimpleSQLGenerator", 
    "SimpleText2SQLAgent"
] 