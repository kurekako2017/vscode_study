"""文档导入 API 的请求/响应 schema。

文件职责：
- 定义 Document Import Pipeline 的对外响应结构。
- 把导入会话状态固定为可序列化 schema，方便后续替换成异步实现。

谁会调用它：
- `backend/app/api/document_imports.py` 路由，以及导入相关测试。

它调用谁：
- 只依赖 Pydantic 和领域层状态枚举，不依赖仓储实现。

输入是什么：
- 导入 ID、document_id、状态、时间戳与错误信息。

输出是什么：
- 可序列化的 `DocumentImportResponse`。

为什么需要这一层：
- 先把导入结果字段固定下来，再让同步/异步实现细节在 service 层演进。

日本现场面试怎么讲：
- 这是文档导入流水线的稳定输出合同，未来即使换成队列或数据库，API 字段仍可保持兼容。
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.models.document_import import DocumentImportRecord, DocumentImportStatus


class DocumentImportResponse(BaseModel):
    """定义文档导入结果的成功响应合同。"""

    import_id: str
    document_id: str
    status: DocumentImportStatus
    created_at: datetime
    updated_at: datetime
    error_code: str | None = None
    error_message: str | None = None

    @classmethod
    def from_domain(cls, record: DocumentImportRecord) -> "DocumentImportResponse":
        """把领域记录对象转成可序列化响应。"""

        return cls(
            import_id=record.import_id,
            document_id=record.document_id,
            status=record.status,
            created_at=record.created_at,
            updated_at=record.updated_at,
            error_code=record.error_code,
            error_message=record.error_message,
        )


__all__ = ["DocumentImportResponse"]
