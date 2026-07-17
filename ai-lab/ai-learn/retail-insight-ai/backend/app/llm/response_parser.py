"""Provider 结构化输出校验与本地 JSON 修复。

文件职责：不信任模型返回，校验 AI Analysis / Executive Report JSON。
谁调用它：OpenRouterLLMProvider。
设计理由：修复失败直接失败，不发起第二次收费调用。
"""

from __future__ import annotations

import json
import re
from typing import Any

from app.models.ai_analysis import (
    AIEvidence,
    LLMProviderCitationInvalidError,
    LLMProviderResponseInvalidError,
)


def extract_json_object(raw: str) -> dict[str, Any]:
    """解析 JSON；失败时尝试截取首个对象并做一次本地修复。"""

    text = (raw or "").strip()
    if not text:
        raise LLMProviderResponseInvalidError("empty provider content")
    try:
        payload = json.loads(text)
        if isinstance(payload, dict):
            return payload
    except json.JSONDecodeError:
        pass
    # 本地修复：去掉 markdown fence 与前后噪声，不调用模型。
    fenced = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.I | re.M).strip()
    match = re.search(r"\{.*\}", fenced, flags=re.S)
    candidate = match.group(0) if match else fenced
    try:
        payload = json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise LLMProviderResponseInvalidError("provider JSON is invalid") from exc
    if not isinstance(payload, dict):
        raise LLMProviderResponseInvalidError("provider JSON root must be an object")
    return payload


def parse_analysis_payload(
    payload: dict[str, Any], *, evidence: tuple[AIEvidence, ...]
) -> tuple[str, bool, tuple[str, ...]]:
    """返回 (answer, insufficient_context, warnings)；校验 citation 引用。"""

    answer = str(payload.get("answer") or "").strip()
    if not answer:
        raise LLMProviderResponseInvalidError("analysis answer missing")
    warnings_raw = payload.get("warnings") or []
    if not isinstance(warnings_raw, list):
        raise LLMProviderResponseInvalidError("warnings must be a list")
    warnings = tuple(str(item) for item in warnings_raw if str(item).strip())
    insufficient = bool(payload.get("insufficient_context", False))
    _validate_citations(payload.get("citations"), evidence)
    return answer, insufficient, warnings


def parse_report_payload(
    payload: dict[str, Any], *, evidence: tuple[AIEvidence, ...]
) -> tuple[str, str, tuple[str, ...], tuple[str, ...], tuple[str, ...], str]:
    """返回 title, executive_summary, kpi, risks, recommendations, markdown。"""

    title = str(payload.get("title") or "").strip() or "Executive Report"
    summary = str(payload.get("executive_summary") or "").strip()
    if not summary:
        raise LLMProviderResponseInvalidError("executive_summary missing")
    kpi = _string_list(payload.get("kpi_findings"), "kpi_findings")
    risks = _string_list(payload.get("risks"), "risks")
    recommendations = _string_list(payload.get("recommendations"), "recommendations")
    _validate_citations(payload.get("citations"), evidence)
    markdown = "\n".join(
        [
            f"# {title}",
            "",
            "## Executive Summary",
            summary,
            "",
            "## KPI Findings",
            *[f"- {item}" for item in kpi],
            "",
            "## Risks",
            *[f"- {item}" for item in risks],
            "",
            "## Recommendations",
            *[f"- {item}" for item in recommendations],
            "",
            "## Citations",
            *[f"- {item.document_id}/{item.chunk_id}" for item in evidence],
        ]
    )
    return title, summary, kpi, risks, recommendations, markdown


def _string_list(value: Any, field: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise LLMProviderResponseInvalidError(f"{field} must be a list")
    return tuple(str(item).strip() for item in value if str(item).strip())


def _validate_citations(value: Any, evidence: tuple[AIEvidence, ...]) -> None:
    if value is None:
        return
    if not isinstance(value, list):
        raise LLMProviderResponseInvalidError("citations must be a list")
    allowed = {(item.document_id, item.chunk_id) for item in evidence}
    for item in value:
        if not isinstance(item, dict):
            raise LLMProviderCitationInvalidError("citation item must be an object")
        document_id = str(item.get("document_id") or "").strip()
        chunk_id = str(item.get("chunk_id") or "").strip()
        if (document_id, chunk_id) not in allowed:
            raise LLMProviderCitationInvalidError("citation does not match evidence")


__all__ = ["extract_json_object", "parse_analysis_payload", "parse_report_payload"]
