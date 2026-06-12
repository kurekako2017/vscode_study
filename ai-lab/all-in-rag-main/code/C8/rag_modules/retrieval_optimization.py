"""
文件功能概述：`code/C8/rag_modules/retrieval_optimization.py` 主要是 检索optimization，这个文件里有 1 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `RetrievalOptimizationModule`：功能概述：这个类是 `RetrievalOptimizationModule`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 vectorstore, chunks，再调用 self.setup_retrievers 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `setup_retrievers`：先进入当前步骤，再调用 logger.info、self.vectorstore.as_retriever、BM25Retriever.from_documents 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 3. `hybrid_search`：先接收输入参数 query, top_k，再调用 self.vector_retriever.invoke、self.bm25_retriever.invoke、self._rrf_rerank 等内部步骤完成主要工作，最后返回结果。 4. `metadata_filtered_search`：先接收输入参数 query, filters, top_k，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 self.hybrid_search、filters.items、filtered_docs.append 等内部步骤完成主要工作，最后返回结果。 5. `_rrf_rerank`：先接收输入参数 vector_docs, bm25_docs, k，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 enumerate、sorted、logger.info 等内部步骤完成主要工作，最后返回结果。
"""


import logging
import hashlib
from typing import List, Dict, Any

from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

logger = logging.getLogger(__name__)

class RetrievalOptimizationModule:
    """
    功能概述：这个类是 `RetrievalOptimizationModule`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 vectorstore, chunks，再调用 self.setup_retrievers 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `setup_retrievers`：先进入当前步骤，再调用 logger.info、self.vectorstore.as_retriever、BM25Retriever.from_documents 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    3. `hybrid_search`：先接收输入参数 query, top_k，再调用 self.vector_retriever.invoke、self.bm25_retriever.invoke、self._rrf_rerank 等内部步骤完成主要工作，最后返回结果。
    4. `metadata_filtered_search`：先接收输入参数 query, filters, top_k，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 self.hybrid_search、filters.items、filtered_docs.append 等内部步骤完成主要工作，最后返回结果。
    5. `_rrf_rerank`：先接收输入参数 vector_docs, bm25_docs, k，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 enumerate、sorted、logger.info 等内部步骤完成主要工作，最后返回结果。
    """
    
    def __init__(self, vectorstore: FAISS, chunks: List[Document]):  # 中文名称：初始化
        """
        初始化检索优化模块
        
        Args:
            vectorstore: FAISS向量存储
            chunks: 文档块列表
        """
        self.vectorstore = vectorstore
        self.chunks = chunks
        self.setup_retrievers()

    def setup_retrievers(self):  # 中文名称：setupretrievers
        """设置向量检索器和BM25检索器"""
        logger.info("正在设置检索器...")

        # 向量检索器
        self.vector_retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )

        # BM25检索器
        self.bm25_retriever = BM25Retriever.from_documents(
            self.chunks,
            k=5
        )



        logger.info("检索器设置完成")
    
    def hybrid_search(self, query: str, top_k: int = 3) -> List[Document]:  # 中文名称：混合搜索
        """
        混合检索 - 结合向量检索和BM25检索，使用RRF重排

        Args:
            query: 查询文本
            top_k: 返回结果数量

        Returns:
            检索到的文档列表
        """
        # 分别获取向量检索和BM25检索结果
        vector_docs = self.vector_retriever.invoke(query)
        bm25_docs = self.bm25_retriever.invoke(query)

        # 使用RRF重排
        reranked_docs = self._rrf_rerank(vector_docs, bm25_docs)
        return reranked_docs[:top_k]
    
    def metadata_filtered_search(self, query: str, filters: Dict[str, Any], top_k: int = 5) -> List[Document]:  # 中文名称：元数据filtered搜索
        """
        带元数据过滤的检索
        
        Args:
            query: 查询文本
            filters: 元数据过滤条件
            top_k: 返回结果数量
            
        Returns:
            过滤后的文档列表
        """
        # 先进行混合检索，获取更多候选
        docs = self.hybrid_search(query, top_k * 3)
        
        # 应用元数据过滤
        filtered_docs = []
        for doc in docs:
            match = True
            for key, value in filters.items():
                if key in doc.metadata:
                    if isinstance(value, list):
                        if doc.metadata[key] not in value:
                            match = False
                            break
                    else:
                        if doc.metadata[key] != value:
                            match = False
                            break
                else:
                    match = False
                    break
            
            if match:
                filtered_docs.append(doc)
                if len(filtered_docs) >= top_k:
                    break
        
        return filtered_docs

    def _rrf_rerank(self, vector_docs: List[Document], bm25_docs: List[Document], k: int = 60) -> List[Document]:  # 中文名称：rrfrerank
        """
        使用RRF (Reciprocal Rank Fusion) 算法重排文档

        Args:
            vector_docs: 向量检索结果
            bm25_docs: BM25检索结果
            k: RRF参数，用于平滑排名

        Returns:
            重排后的文档列表
        """
        doc_scores = {}
        doc_objects = {}

        # 计算向量检索结果的RRF分数
        for rank, doc in enumerate(vector_docs):
            # 使用文档内容的确定性哈希作为唯一标识
            doc_id = hashlib.md5(doc.page_content.encode('utf-8')).hexdigest()
            doc_objects[doc_id] = doc

            # RRF公式: 1 / (k + rank)
            rrf_score = 1.0 / (k + rank + 1)
            doc_scores[doc_id] = doc_scores.get(doc_id, 0) + rrf_score

            logger.debug(f"向量检索 - 文档{rank+1}: RRF分数 = {rrf_score:.4f}")

        # 计算BM25检索结果的RRF分数
        for rank, doc in enumerate(bm25_docs):
            doc_id = hashlib.md5(doc.page_content.encode('utf-8')).hexdigest()
            doc_objects[doc_id] = doc

            rrf_score = 1.0 / (k + rank + 1)
            doc_scores[doc_id] = doc_scores.get(doc_id, 0) + rrf_score

            logger.debug(f"BM25检索 - 文档{rank+1}: RRF分数 = {rrf_score:.4f}")

        # 按最终RRF分数排序
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

        # 构建最终结果
        reranked_docs = []
        for doc_id, final_score in sorted_docs:
            if doc_id in doc_objects:
                doc = doc_objects[doc_id]
                # 将RRF分数添加到文档元数据中
                doc.metadata['rrf_score'] = final_score
                reranked_docs.append(doc)
                logger.debug(f"最终排序 - 文档: {doc.page_content[:50]}... 最终RRF分数: {final_score:.4f}")

        logger.info(f"RRF重排完成: 向量检索{len(vector_docs)}个文档, BM25检索{len(bm25_docs)}个文档, 合并后{len(reranked_docs)}个文档")

        return reranked_docs


