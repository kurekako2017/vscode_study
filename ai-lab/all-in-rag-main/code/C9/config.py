"""
文件功能概述：`code/C9/config.py` 主要是 配置，这个文件里有 1 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `GraphRAGConfig`：功能概述：这个类是 `GraphRAGConfig`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__post_init__`：先进入当前步骤，最后把结果交给下一步或直接结束。 2. `from_dict`：先接收输入参数 cls, config_dict，再调用 cls 等内部步骤完成主要工作，最后返回结果。 3. `to_dict`：先进入当前步骤，最后返回结果。
"""


import os
from dataclasses import dataclass
from dataclasses import field
from typing import Dict, Any

@dataclass
class GraphRAGConfig:
    """
    功能概述：这个类是 `GraphRAGConfig`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__post_init__`：先进入当前步骤，最后把结果交给下一步或直接结束。
    2. `from_dict`：先接收输入参数 cls, config_dict，再调用 cls 等内部步骤完成主要工作，最后返回结果。
    3. `to_dict`：先进入当前步骤，最后返回结果。
    """

    # Neo4j数据库配置
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "all-in-rag"
    neo4j_database: str = "neo4j"

    # Milvus配置
    milvus_host: str = "localhost"
    milvus_port: int = 19530
    milvus_collection_name: str = "cooking_knowledge"
    milvus_dimension: int = 512  # BGE-small-zh-v1.5的向量维度

    # 模型配置
    embedding_model: str = "BAAI/bge-small-zh-v1.5"
    llm_model: str = field(default_factory=lambda: os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"))

    # 检索配置（LightRAG Round-robin策略）
    top_k: int = 5

    # 父文档检索配置
    enable_parent_doc_retrieval: bool = False  # 默认 False，不做父文档回填，直接把chunk当作上下文，有可能会出现步骤不全问题
    parent_doc_top_n: int = 3                   # 仅 RRF 分前 N 名做父文档替换
    parent_doc_max_chars: int = 4000            # 每篇父文档字符上限（兜底）

    # 生成配置
    temperature: float = 0.1
    max_tokens: int = 2048

    # 图数据处理配置
    chunk_size: int = 500
    chunk_overlap: int = 50
    max_graph_depth: int = 2  # 图遍历最大深度

    def __post_init__(self):  # 中文名称：特殊方法 __post_init__
        """初始化后的处理"""
        # LightRAG使用Round-robin策略，无需权重验证
        pass
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'GraphRAGConfig':  # 中文名称：fromdict
        """从字典创建配置对象"""
        return cls(**config_dict)
    
    def to_dict(self) -> Dict[str, Any]:  # 中文名称：todict
        """转换为字典"""
        return {
            'neo4j_uri': self.neo4j_uri,
            'neo4j_user': self.neo4j_user,
            'neo4j_password': self.neo4j_password,
            'neo4j_database': self.neo4j_database,
            'milvus_host': self.milvus_host,
            'milvus_port': self.milvus_port,
            'milvus_collection_name': self.milvus_collection_name,
            'milvus_dimension': self.milvus_dimension,
            'embedding_model': self.embedding_model,
            'llm_model': self.llm_model,
            'top_k': self.top_k,
            'enable_parent_doc_retrieval': self.enable_parent_doc_retrieval,
            'parent_doc_top_n': self.parent_doc_top_n,
            'parent_doc_max_chars': self.parent_doc_max_chars,

            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'chunk_size': self.chunk_size,
            'chunk_overlap': self.chunk_overlap,
            'max_graph_depth': self.max_graph_depth
        }

# 默认配置实例
DEFAULT_CONFIG = GraphRAGConfig() 
