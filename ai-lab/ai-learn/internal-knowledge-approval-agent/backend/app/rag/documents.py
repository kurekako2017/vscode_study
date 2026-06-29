from typing import TypedDict


class Document(TypedDict):
    title: str
    content: str


DOCUMENTS: tuple[Document, ...] = (
    {"title": "社内業務マニュアル v1.0", "content": "一般業務は担当部門の最新規程と手順書に従う。"},
    {"title": "情報取扱手順書 v1.0", "content": "機密情報と個人情報は承認済みの経路で取り扱う。"},
)
