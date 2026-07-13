"""Document 与 JSONB/数据库行之间的集中转换，避免多个 Repository 重复定义格式。"""

from __future__ import annotations

import json
from typing import Any

from app.models.document import DocumentMetadata, DocumentSource


def source_to_json(source: DocumentSource | None) -> str:
    """把来源对象转换为稳定 JSON。"""

    if source is None:
        return "null"
    return json.dumps(
        {
            "source_type": source.source_type,
            "uri": source.uri,
            "label": source.label,
            "external_id": source.external_id,
        },
        ensure_ascii=False,
    )


def metadata_to_dict(metadata: DocumentMetadata) -> dict[str, Any]:
    """把完整元数据转换为 chunk 可复原的 JSONB 结构。"""

    return {
        "document_id": metadata.document_id,
        "title": metadata.title,
        "description": metadata.description,
        "owner": metadata.owner,
        "created_at": metadata.created_at.isoformat(),
        "updated_at": metadata.updated_at.isoformat(),
        "version": metadata.version,
        "language": metadata.language.value,
        "document_type": metadata.document_type.value,
        "status": metadata.status.value,
        "tags": list(metadata.tags),
        "source": json.loads(source_to_json(metadata.source)),
        "checksum": metadata.checksum,
    }


__all__ = ["metadata_to_dict", "source_to_json"]
