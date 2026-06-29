"""V1 固定社内文档语料。

文件职责：定义最小 Document 类型和两份本地资料，模拟 RAG 的文档来源。
谁调用它：Retriever 和 Answer Generator；它不访问网络或文件系统。
输入：模块内固定数据；输出：保留 title/content 的 Document tuple。
为什么需要这一层：以可重复语料先验证检索、审批、引用和 UI 全链路。
初学者重点：Document 是知识来源，不是最终回答；title 会成为当前 Citation。
日本现场面试：可说明这是 LocalStaticDocumentProvider，不夸大为生产知识库。
企业级替换：Wiki/FAQ/工单先做解析、Chunk、Embedding、ACL 元数据和索引刷新。
"""

from typing import TypedDict


class Document(TypedDict):
    title: str
    content: str


DOCUMENTS: tuple[Document, ...] = (
    {"title": "社内業務マニュアル v1.0", "content": "一般業務は担当部門の最新規程と手順書に従う。"},
    {"title": "情報取扱手順書 v1.0", "content": "機密情報と個人情報は承認済みの経路で取り扱う。"},
)
