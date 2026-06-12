"""
文件功能概述：`code/langchain_community/document_loaders.py` 主要是 文档loaders，这个文件里有 2 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `TextLoader`：功能概述：这个类是 `TextLoader`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 file_path, encoding，最后把结果交给下一步或直接结束。 2. `load`：先进入当前步骤，再调用 Path、path.read_text、Document 等内部步骤完成主要工作，最后返回结果。
2. 类 `BiliBiliLoader`：功能概述：这个类是 `BiliBiliLoader`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 video_urls，最后把结果交给下一步或直接结束。 2. `load`：先进入当前步骤，然后循环处理每一条数据，再调用 enumerate、docs.append、Document 等内部步骤完成主要工作，最后返回结果。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from langchain_core.documents import Document


class TextLoader:
    """
    功能概述：这个类是 `TextLoader`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 file_path, encoding，最后把结果交给下一步或直接结束。
    2. `load`：先进入当前步骤，再调用 Path、path.read_text、Document 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, file_path: str, encoding: str = "utf-8"):  # 中文名称：初始化
        self.file_path = file_path
        self.encoding = encoding

    def load(self) -> List[Document]:  # 中文名称：加载
        path = Path(self.file_path)
        text = path.read_text(encoding=self.encoding)
        return [Document(page_content=text, metadata={"source": str(path)})]


class BiliBiliLoader:
    """
    功能概述：这个类是 `BiliBiliLoader`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 video_urls，最后把结果交给下一步或直接结束。
    2. `load`：先进入当前步骤，然后循环处理每一条数据，再调用 enumerate、docs.append、Document 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, video_urls: List[str]):  # 中文名称：初始化
        self.video_urls = video_urls

    def load(self) -> List[Document]:  # 中文名称：加载
        docs = []
        for index, url in enumerate(self.video_urls, 1):
            docs.append(
                Document(
                    page_content=f"这是一个离线占位视频文档，来源于 {url}",
                    metadata={
                        "title": f"视频{index}",
                        "owner": {"name": f"作者{index}"},
                        "bvid": url.rsplit("/", 1)[-1],
                        "stat": {"view": 1000 * index},
                        "duration": 120 * index,
                    },
                )
            )
        return docs

