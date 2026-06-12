"""
文件功能概述：`code/C8/rag_modules/__init__.py` 主要是 初始化，这个文件里有 0 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 这个文件没有独立类或函数，主要靠模块级代码直接执行。
"""

from .data_preparation import DataPreparationModule
from .index_construction import IndexConstructionModule
from .retrieval_optimization import RetrievalOptimizationModule
from .generation_integration import GenerationIntegrationModule

__all__ = [
    'DataPreparationModule',
    'IndexConstructionModule', 
    'RetrievalOptimizationModule',
    'GenerationIntegrationModule'
]

__version__ = "1.0.0"
