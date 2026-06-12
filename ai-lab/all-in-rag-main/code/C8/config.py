"""
文件功能概述：`code/C8/config.py` 主要是 配置，这个文件里有 1 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `RAGConfig`：功能概述：这个类是 `RAGConfig`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__post_init__`：先进入当前步骤，最后把结果交给下一步或直接结束。 2. `from_dict`：先接收输入参数 cls, config_dict，再调用 cls 等内部步骤完成主要工作，最后返回结果。 3. `to_dict`：先进入当前步骤，最后返回结果。
"""


import os
from dataclasses import dataclass
from dataclasses import field
from typing import Dict, Any

@dataclass
class RAGConfig:
    """
    功能概述：这个类是 `RAGConfig`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__post_init__`：先进入当前步骤，最后把结果交给下一步或直接结束。
    2. `from_dict`：先接收输入参数 cls, config_dict，再调用 cls 等内部步骤完成主要工作，最后返回结果。
    3. `to_dict`：先进入当前步骤，最后返回结果。
    """

    # 路径配置
    data_path: str = "../../data/C8/cook"
    index_save_path: str = "./vector_index"

    # 模型配置
    embedding_model: str = "BAAI/bge-small-zh-v1.5"
    llm_model: str = field(default_factory=lambda: os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"))

    # 检索配置
    top_k: int = 3

    # 生成配置
    temperature: float = 0.1
    max_tokens: int = 2048

    def __post_init__(self):  # 中文名称：特殊方法 __post_init__
        """初始化后的处理"""
        pass
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'RAGConfig':  # 中文名称：fromdict
        """从字典创建配置对象"""
        return cls(**config_dict)
    
    def to_dict(self) -> Dict[str, Any]:  # 中文名称：todict
        """转换为字典"""
        return {
            'data_path': self.data_path,
            'index_save_path': self.index_save_path,
            'embedding_model': self.embedding_model,
            'llm_model': self.llm_model,
            'top_k': self.top_k,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens
        }

# 默认配置实例
DEFAULT_CONFIG = RAGConfig()
