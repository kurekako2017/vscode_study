from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from langchain_core.documents import Document


class TextLoader:
    def __init__(self, file_path: str, encoding: str = "utf-8"):
        self.file_path = file_path
        self.encoding = encoding

    def load(self) -> List[Document]:
        path = Path(self.file_path)
        text = path.read_text(encoding=self.encoding)
        return [Document(page_content=text, metadata={"source": str(path)})]


class BiliBiliLoader:
    def __init__(self, video_urls: List[str]):
        self.video_urls = video_urls

    def load(self) -> List[Document]:
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

