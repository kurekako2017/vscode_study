"""V1 确定性本地 Retriever。

文件职责：为任意问题返回固定文档，保持 Workflow 测试结果稳定。
谁调用它：Workflow AnswerGenerator Node；它调用 ``documents.DOCUMENTS``。
输入：问题字符串（V1 尚未用于打分）；输出：候选 Document tuple。
为什么需要这一层：先保留可替换的检索边界，再逐阶段增加检索能力。
初学者重点：当前没有 Chunk、Top-K 或 Rerank，不能把“返回全部文档”称为向量检索。
日本现场面试：可说明它模拟 Retriever 接口与 Citation 流程，而非生产检索质量。
企业级替换：此函数将由 ACL Filter → Hybrid Search → Top-K → Rerank → Context 组装替换，
并用 recall@k/MRR、groundedness、延迟和无权限泄露率持续评估。
"""

from app.rag.documents import DOCUMENTS, Document


def retrieve_documents(_: str) -> tuple[Document, ...]:
    """返回固定资料；当前没有网络、Embedding、VectorDB 或模型依赖。"""

    return DOCUMENTS
