"""
文件功能概述：`Extra-chapter/PowerRAG-SDK-Text-QA/code/config.py` 主要是 配置，这个文件里有 1 个类、1 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 函数 `_bool_env`：先接收输入参数 name, default，接着根据条件分支选择不同处理路径，再调用 os.getenv、lower、raw.strip 等内部步骤完成主要工作，最后返回结果。
2. 类 `PowerRAGDemoConfig`：功能概述：这个类是 `PowerRAGDemoConfig`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
"""


from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _bool_env(name: str, default: bool = False) -> bool:  # 中文名称：boolenv
    raw = os.getenv(name)
    if raw is None:
        return default
    raw = raw.strip().lower()
    if raw in {"1", "true", "yes", "y", "on"}:
        return True
    if raw in {"0", "false", "no", "n", "off"}:
        return False
    return default


@dataclass(frozen=True)
class PowerRAGDemoConfig:
    """
    功能概述：这个类是 `PowerRAGDemoConfig`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
    """
    base_url: str = os.getenv("RAGFLOW_BASE_URL", "http://127.0.0.1:9380").strip()
    api_key: str = os.getenv("RAGFLOW_API_KEY", "").strip()
    dataset_name: str = os.getenv("RAGFLOW_DATASET_NAME", "powerrag_text_qa_demo").strip()
    embedding_model: str = os.getenv("RAGFLOW_EMBEDDING_MODEL", "").strip()

    top_k: int = int(os.getenv("RAGFLOW_TOP_K", "5"))
    candidate_k: int = int(os.getenv("RAGFLOW_CANDIDATE_K", "1024"))
    similarity_threshold: float = float(os.getenv("RAGFLOW_SIMILARITY_THRESHOLD", "0.2"))
    vector_similarity_weight: float = float(os.getenv("RAGFLOW_VECTOR_SIMILARITY_WEIGHT", "0.3"))
    keyword: bool = _bool_env("RAGFLOW_KEYWORD", False)


DEFAULT_CONFIG = PowerRAGDemoConfig()

