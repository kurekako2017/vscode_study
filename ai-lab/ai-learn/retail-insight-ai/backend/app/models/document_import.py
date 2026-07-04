"""文档导入领域模型。

文件职责：
- 定义 Document Import Pipeline 的状态、结果和错误模型。
- 为后续 chunking、RAG、审批与审计保留稳定的导入会话边界。

谁会调用它：
- Document Import Service、API response schema 和单元测试。

它调用谁：
- 只调用 `utc_now` 作为时间来源，不依赖 API 或数据库层。

输入是什么：
- document_id、import_id、状态迁移目标和错误信息。

输出是什么：
- 可追踪的导入结果记录、导入错误和状态更新结果。

为什么需要这一层：
- 导入不是上传，也不是 chunking；先把导入会话单独建模，后续才能替换成队列或持久化实现。

日本现场面试怎么讲：
- 这是文档入库流水线的会话层，先同步跑通验证和状态记录，未来可以替换成异步批处理或数据库驱动实现。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from app.models.task import utc_now


class DocumentImportStatus(StrEnum):
    """定义文档导入会话状态。"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True)
class DocumentImportError:
    """保存导入失败时的安全错误信息。"""

    error_code: str
    error_message: str


@dataclass
class DocumentImportRecord:
    """保存一次文档导入会话的最终或中间状态。"""

    import_id: str
    document_id: str
    status: DocumentImportStatus = DocumentImportStatus.PENDING
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    error: DocumentImportError | None = None

    @property
    def error_code(self) -> str | None:
        """向 API 公开机器错误码。"""

        return self.error.error_code if self.error is not None else None

    @property
    def error_message(self) -> str | None:
        """向 API 公开用户可读错误消息。"""

        return self.error.error_message if self.error is not None else None

    def mark_running(self) -> None:
        """把会话推进到 running。"""

        timestamp = utc_now()
        self.status = DocumentImportStatus.RUNNING
        self.updated_at = timestamp

    def mark_completed(self) -> None:
        """把会话推进到 completed。"""

        timestamp = utc_now()
        self.status = DocumentImportStatus.COMPLETED
        self.updated_at = timestamp
        self.error = None

    def mark_failed(self, error_code: str, error_message: str) -> None:
        """把会话推进到 failed，并保存安全错误信息。"""

        timestamp = utc_now()
        self.status = DocumentImportStatus.FAILED
        self.updated_at = timestamp
        self.error = DocumentImportError(error_code=error_code, error_message=error_message)


__all__ = ["DocumentImportError", "DocumentImportRecord", "DocumentImportStatus"]
