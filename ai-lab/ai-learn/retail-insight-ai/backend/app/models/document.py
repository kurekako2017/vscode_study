"""文档领域模型。

文件职责：
- 定义 Document / DocumentVersion / DocumentChunk / DocumentMetadata / DocumentSource。
- 定义文档域自己的状态、类型、语言与审批状态别名。
- 作为 Upload、版本管理、检索、审批和持久化之间的稳定领域边界。

谁会调用它：
- Service、Repository、测试代码，以及后续的 Upload / RAG / Approval 流程。

它调用谁：
- 只调用通用异常和时间工具，不依赖 API 或数据库层。

输入是什么：
- 文档正文、元数据、来源信息、状态迁移目标、版本快照。

输出是什么：
- 可校验、可持久化、可逐步演进的文档领域对象。

为什么需要这一层：
- 先把文档域的状态、版本、来源和校验规则固定下来，再接 Upload API 和 RAG。

日本现场面试怎么讲：
- 这是 Upload API 之前的领域基础层，未来可以平滑替换成 PostgreSQL、Chunk、RAG 和 Approval 组件。
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import StrEnum
from typing import Any, Mapping, Sequence

from app.errors.exceptions import ValidationAppException
from app.models.persistence import DataImport as ImportBatch
from app.models.report import ReportStatus as ApprovalStatus
from app.models.task import utc_now


class Language(StrEnum):
    """定义文档内容语言，便于后续检索、展示和路由。"""

    EN = "en"
    JA = "ja"
    ZH_CN = "zh-CN"
    UNKNOWN = "unknown"


class DocumentType(StrEnum):
    """定义当前文档域支持的文件类型。"""

    MARKDOWN = "markdown"
    PDF = "pdf"
    WORD = "word"
    EXCEL = "excel"
    CSV = "csv"
    JSON = "json"
    TEXT = "text"
    IMAGE = "image"

    @property
    def is_currently_supported(self) -> bool:
        """当前阶段是否允许直接进入文档域主链路。"""

        return self is not DocumentType.IMAGE


class DocumentStatus(StrEnum):
    """定义文档生命周期状态，当前默认只会创建 uploaded。"""

    UPLOADED = "uploaded"
    VALIDATED = "validated"
    INDEXED = "indexed"
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


def _validation_error(field: str, reason: str, **detail: Any) -> ValidationAppException:
    payload = {"field": field, "reason": reason, **detail}
    return ValidationAppException(payload)


def _require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise _validation_error(field, f"{field} must not be blank")
    return value.strip()


def _coerce_enum(enum_cls: type[StrEnum], value: Any, field: str) -> StrEnum:
    if isinstance(value, enum_cls):
        return value
    try:
        return enum_cls(str(value))
    except (TypeError, ValueError) as exc:
        raise _validation_error(field, f"unsupported {field}", value=value) from exc


def _normalize_tags(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        raise _validation_error("tags", "tags must be a sequence of strings")
    if not isinstance(value, Sequence):
        raise _validation_error("tags", "tags must be a sequence of strings")
    tags: list[str] = []
    for tag in value:
        if not isinstance(tag, str) or not tag.strip():
            raise _validation_error("tags", "each tag must be a non-empty string")
        tags.append(tag.strip())
    return tuple(tags)


@dataclass(frozen=True)
class DocumentSource:
    """保存文档来源信息，后续可扩展为对象存储、API、人工上传等来源。"""

    source_type: str
    uri: str
    label: str | None = None
    external_id: str | None = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "DocumentSource":
        """从字典构建来源信息，用于上传请求或导入流程。"""

        return cls(
            source_type=_require_text(data.get("source_type"), "source_type"),
            uri=_require_text(data.get("uri"), "uri"),
            label=data.get("label").strip() if isinstance(data.get("label"), str) and data.get("label").strip() else None,
            external_id=data.get("external_id").strip()
            if isinstance(data.get("external_id"), str) and data.get("external_id").strip()
            else None,
        )

    def validate(self) -> None:
        """校验来源字段，避免出现空来源或空 URI。"""

        _require_text(self.source_type, "source_type")
        _require_text(self.uri, "uri")


@dataclass(frozen=True)
class DocumentMetadata:
    """保存文档元数据，作为检索、版本管理和审计的共同输入。"""

    document_id: str
    title: str
    description: str | None
    owner: str
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    version: int = 1
    language: Language = Language.UNKNOWN
    document_type: DocumentType = DocumentType.TEXT
    status: DocumentStatus = DocumentStatus.UPLOADED
    tags: tuple[str, ...] = field(default_factory=tuple)
    source: DocumentSource | None = None
    checksum: str = ""

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "DocumentMetadata":
        """从外部输入构建元数据，并在此阶段完成基础字段校验。"""

        source = data.get("source")
        if source is None:
            raise _validation_error("source", "source is required")
        if isinstance(source, Mapping):
            source = DocumentSource.from_mapping(source)
        if not isinstance(source, DocumentSource):
            raise _validation_error("source", "source must be a mapping or DocumentSource")

        description = data.get("description")
        if isinstance(description, str) and not description.strip():
            description = None

        created_at = data.get("created_at", utc_now())
        updated_at = data.get("updated_at", created_at)
        if not isinstance(created_at, datetime) or not isinstance(updated_at, datetime):
            raise _validation_error("created_at", "created_at and updated_at must be datetime")

        try:
            version = int(data.get("version", 1))
        except (TypeError, ValueError) as exc:
            raise _validation_error("version", "version must be an integer") from exc

        metadata = cls(
            document_id=_require_text(data.get("document_id"), "document_id"),
            title=_require_text(data.get("title"), "title"),
            description=description,
            owner=_require_text(data.get("owner"), "owner"),
            created_at=created_at,
            updated_at=updated_at,
            version=version,
            language=_coerce_enum(Language, data.get("language", Language.UNKNOWN), "language"),  # type: ignore[arg-type]
            document_type=_coerce_enum(
                DocumentType,
                data.get("document_type", DocumentType.TEXT),
                "document_type",
            ),  # type: ignore[arg-type]
            status=_coerce_enum(DocumentStatus, data.get("status", DocumentStatus.UPLOADED), "status"),  # type: ignore[arg-type]
            tags=_normalize_tags(data.get("tags")),
            source=source,
            checksum=_require_text(data.get("checksum"), "checksum"),
        )
        metadata.validate()
        return metadata

    def validate(self, *, allow_future_type: bool = True) -> None:
        """校验元数据的完整性，当前阶段会拒绝 image 类型。"""

        _require_text(self.document_id, "document_id")
        _require_text(self.title, "title")
        _require_text(self.owner, "owner")
        _require_text(self.checksum, "checksum")
        if not isinstance(self.language, Language):
            raise _validation_error("language", "language must be a Language value")
        if not isinstance(self.document_type, DocumentType):
            raise _validation_error("document_type", "document_type must be a DocumentType value")
        if not isinstance(self.status, DocumentStatus):
            raise _validation_error("status", "status must be a DocumentStatus value")
        if self.version < 1:
            raise _validation_error("version", "version must be greater than 0")
        if self.source is None:
            raise _validation_error("source", "source is required")
        self.source.validate()
        if not allow_future_type and not self.document_type.is_currently_supported:
            raise _validation_error("document_type", "unsupported type", document_type=self.document_type.value)
        for tag in self.tags:
            if not isinstance(tag, str) or not tag.strip():
                raise _validation_error("tags", "each tag must be a non-empty string")


@dataclass(frozen=True)
class DocumentVersion:
    """保存某个文档版本的正文快照，供审批、回溯和版本管理使用。"""

    document_id: str
    version: int
    content: str
    metadata: DocumentMetadata
    approval_status: ApprovalStatus = ApprovalStatus.GENERATED
    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        """保护版本号和元数据的一致性。"""

        if self.version < 1:
            raise _validation_error("version", "version must be greater than 0")
        if self.metadata.document_id != self.document_id:
            raise _validation_error("document_id", "version metadata must match document_id")
        if self.metadata.version != self.version:
            raise _validation_error("version", "metadata version must match version")
        if not isinstance(self.content, str) or not self.content.strip():
            raise _validation_error("content", "content must not be blank")


@dataclass(frozen=True)
class DocumentChunk:
    """保存文档切片事实；embedding 可空，兼容 migration 前的旧数据。"""

    document_id: str
    version: int
    chunk_id: str
    chunk_index: int
    content: str
    character_count: int
    metadata: DocumentMetadata
    created_at: datetime = field(default_factory=utc_now)
    embedding: tuple[float, ...] | None = None

    def __post_init__(self) -> None:
        """向量存在时立即校验固定维度与有限值，防止坏数据进入仓储。"""

        if self.embedding is not None:
            from app.embeddings.service import validate_embedding_vector

            object.__setattr__(self, "embedding", validate_embedding_vector(self.embedding))


@dataclass
class Document:
    """文档聚合根，负责保护内容、元数据与状态迁移约束。"""

    content: str
    metadata: DocumentMetadata
    approval_status: ApprovalStatus = ApprovalStatus.GENERATED
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    @classmethod
    def create(cls, content: str, metadata: DocumentMetadata) -> "Document":
        """创建文档并执行当前阶段的基础校验。"""

        document = cls(content=content, metadata=metadata)
        document.validate_for_creation()
        return document

    @property
    def document_id(self) -> str:
        """提供文档 ID 便于 Repository 与 Service 直接引用。"""

        return self.metadata.document_id

    @property
    def version(self) -> int:
        """暴露当前元数据中的版本号。"""

        return self.metadata.version

    @property
    def status(self) -> DocumentStatus:
        """暴露当前文档状态，避免调用方直接依赖元数据结构。"""

        return self.metadata.status

    def validate_for_creation(self) -> None:
        """校验创建路径，当前阶段只接受 uploaded 状态和非空内容。"""

        self.validate_for_storage()
        if self.metadata.status is not DocumentStatus.UPLOADED:
            raise _validation_error(
                "status",
                "initial document status must be uploaded",
                status=self.metadata.status.value,
            )

    def validate_for_storage(self) -> None:
        """校验持久化路径，保证 Repository 只看到合法文档。"""

        self.metadata.validate(allow_future_type=False)
        if not isinstance(self.content, str) or not self.content.strip():
            raise _validation_error("content", "empty file")

    def transition_status(self, target: DocumentStatus) -> None:
        """按照文档生命周期推进状态，禁止跳跃式或回退式迁移。"""

        current = self.metadata.status
        if current == target:
            return

        allowed_transitions: dict[DocumentStatus, DocumentStatus] = {
            DocumentStatus.UPLOADED: DocumentStatus.VALIDATED,
            DocumentStatus.VALIDATED: DocumentStatus.INDEXED,
            DocumentStatus.INDEXED: DocumentStatus.DRAFT,
            DocumentStatus.DRAFT: DocumentStatus.PENDING_APPROVAL,
            DocumentStatus.PENDING_APPROVAL: DocumentStatus.APPROVED,
            DocumentStatus.APPROVED: DocumentStatus.PUBLISHED,
            DocumentStatus.PUBLISHED: DocumentStatus.ARCHIVED,
            DocumentStatus.ARCHIVED: DocumentStatus.ARCHIVED,
        }
        expected = allowed_transitions[current]
        if target != expected:
            raise _validation_error(
                "status",
                "invalid document status transition",
                current=current.value,
                target=target.value,
            )

        timestamp = utc_now()
        self.metadata = replace(self.metadata, status=target, updated_at=timestamp)
        self.updated_at = timestamp

    def archive(self) -> None:
        """将文档软删除为 archived，但保留全部事实数据。"""

        if self.metadata.status is DocumentStatus.ARCHIVED:
            return
        timestamp = utc_now()
        self.metadata = replace(self.metadata, status=DocumentStatus.ARCHIVED, updated_at=timestamp)
        self.updated_at = timestamp

    def to_version(self) -> DocumentVersion:
        """把当前文档快照转换为版本记录，供版本历史和审批流复用。"""

        return DocumentVersion(
            document_id=self.document_id,
            version=self.version,
            content=self.content,
            metadata=self.metadata,
            approval_status=self.approval_status,
        )


__all__ = [
    "ApprovalStatus",
    "Document",
    "DocumentChunk",
    "DocumentMetadata",
    "DocumentSource",
    "DocumentStatus",
    "DocumentType",
    "DocumentVersion",
    "ImportBatch",
    "Language",
]
