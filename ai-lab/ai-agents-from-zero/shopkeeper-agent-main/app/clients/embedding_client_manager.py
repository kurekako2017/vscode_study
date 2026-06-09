"""
Embedding 客户端管理器

项目原始实现使用的是 HuggingFaceEndpointEmbeddings。
但这个项目在本地跑起来时，Embedding 服务通常是 Docker 里的 TEI
（Text Embeddings Inference）HTTP 服务，而不是 Hugging Face Hub 上的仓库 ID。

因此这里改成直接包一层 huggingface_hub.AsyncInferenceClient：
1. 支持本机 TEI 地址
2. 保留 aembed_query / aembed_documents 这套上层调用方式
3. 不要求把 URL 伪装成 Hugging Face repo_id
"""

import asyncio
from typing import Optional

from huggingface_hub import AsyncInferenceClient

from app.conf.app_config import EmbeddingConfig, app_config


class TEIEmbeddingClient:
    """面向 TEI 服务的最小 Embedding 客户端封装。"""

    def __init__(self, url: str, model: str, api_key: str | None = None):
        self.url = url
        self.model = model
        self.async_client = AsyncInferenceClient(
            base_url=url,
            api_key=api_key,
        )

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        """批量向量化文本。"""

        # TEI / embedding 接口对换行比较敏感，先做最小清洗。
        texts = [text.replace("\n", " ") for text in texts]
        result = await self.async_client.feature_extraction(text=texts)
        return result.tolist()

    async def aembed_query(self, text: str) -> list[float]:
        """单条文本向量化。"""

        return (await self.aembed_documents([text]))[0]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """同步版批量向量化。"""

        return asyncio.run(self.aembed_documents(texts))

    def embed_query(self, text: str) -> list[float]:
        """同步版单条向量化。"""

        return asyncio.run(self.aembed_query(text))


class EmbeddingClientManager:
    """管理 Embedding 服务客户端的初始化与复用。"""

    def __init__(self, config: EmbeddingConfig):
        self.client: Optional[TEIEmbeddingClient] = None
        self.config = config

    def _get_url(self) -> str:
        """拼接 Embedding 服务地址。"""

        return f"http://{self.config.host}:{self.config.port}"

    def init(self):
        """显式初始化客户端，避免模块导入时立即建立外部连接。"""

        self.client = TEIEmbeddingClient(
            url=self._get_url(),
            model=self.config.model,
            api_key=None,
        )


# 模块级单例，供整个项目复用同一套 Embedding 客户端管理器
embedding_client_manager = EmbeddingClientManager(app_config.embedding)


if __name__ == "__main__":
    embedding_client_manager.init()
    client = embedding_client_manager.client

    async def test():
        """执行一次最小化向量化调用，验证服务是否可用。"""

        text = "What is deep learning?"
        query_result = await client.aembed_query(text)
        print(query_result[:3])

    asyncio.run(test())
