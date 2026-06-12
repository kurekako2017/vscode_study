"""
文件功能概述：`code/langchain_community/utils/math.py` 主要是 math，这个文件里有 0 个类、1 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 函数 `cosine_similarity`：先接收输入参数 a, b，再调用 _cosine_similarity 等内部步骤完成主要工作，最后返回结果。
"""

from __future__ import annotations

import numpy as np

from _compat import cosine_similarity as _cosine_similarity


def cosine_similarity(a, b):  # 中文名称：cosinesimilarity
    return _cosine_similarity(a, b)

