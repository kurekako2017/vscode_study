"""PostgreSQL-only 高质量董事会报告编排服务。

文件职责：在 succeeded AI Analysis 之上执行 high_quality 路由、额度预占、Gateway 与 Report 落库。
调用关系：Router 传入 JWT CurrentUser；只经 LLMGatewayService 调 Provider；写 Report/ReportVersion。
输入输出：ai_analysis_id + confirmed → 正式 Report/Version 与 Decimal 成本。
设计理由：高质量调用更贵，必须更严门禁；生成后不自动进入 Approval。
日本现场面试：经营层报告是显式高成本动作，必须与日常分析额度隔离。
"""

from __future__ import annotations

import re
from decimal import Decimal, ROUND_UP
from time import monotonic
from uuid import uuid4

from app.errors.error_codes import ErrorCode
from app.errors.exceptions import AIAnalysisException
from app.llm.gateway import LLMGatewayService
from app.models.ai_analysis import (
    AIEvidence,
    ExecutiveReportResult,
    LLMProviderAuthenticationError,
    LLMProviderCitationInvalidError,
    LLMProviderModelUnavailableError,
    LLMProviderPartialFailureError,
    LLMProviderRateLimitError,
    LLMProviderResponseInvalidError,
    LLMProviderTimeoutError,
    LLMProviderUnavailableError,
    LLMReportInput,
)
from app.models.approval import ReportVersion
from app.models.document import DocumentStatus
from app.models.report import Report, ReportStatus
from app.models.task import Task, TaskStatus
from app.repositories.interfaces.approval_repository import ApprovalRepository
from app.repositories.interfaces.document_chunk_repository import DocumentChunkRepository
from app.repositories.interfaces.document_repository import DocumentRepository
from app.repositories.interfaces.report_repository import ReportRepository
from app.repositories.interfaces.task_repository import TaskRepository
from app.repositories.interfaces.unit_of_work import UnitOfWork
from app.repositories.postgres.llm_usage_repository import PostgresLLMUsageRepository
from app.schemas.executive_report_api import ExecutiveReportRequest
from app.security.contracts import CurrentUser
from app.services.persistent_audit_service import PersistentAuditContext, PersistentAuditService

_MILLION = Decimal(1_000_000)
_COST_QUANTUM = Decimal("0.00000001")
_OPERATION = "executive_report"


class ExecutiveReportService:
    def __init__(
        self, *, gateway: LLMGatewayService,
        usage_repository: PostgresLLMUsageRepository | None,
        document_repository: DocumentRepository,
        chunk_repository: DocumentChunkRepository,
        task_repository: TaskRepository,
        report_repository: ReportRepository,
        approval_repository: ApprovalRepository,
        persistent_audit_service: PersistentAuditService,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._gateway = gateway
        self._usage = usage_repository
        self._documents = document_repository
        self._chunks = chunk_repository
        self._tasks = task_repository
        self._reports = report_repository
        self._approvals = approval_repository
        self._audit = persistent_audit_service
        self._uow = unit_of_work

    def execute(
        self, request: ExecutiveReportRequest, *, actor: CurrentUser,
        idempotency_key: str, context: PersistentAuditContext,
    ) -> ExecutiveReportResult:
        if self._usage is None:
            raise AIAnalysisException(
                ErrorCode.AI_ANALYSIS_REQUIRES_POSTGRES, "Executive report requires PostgreSQL", 503,
            )
        try:
            policy = self._gateway.policy_for(_OPERATION)
        except LookupError as exc:
            raise AIAnalysisException(ErrorCode.VALIDATION_ERROR, "Unknown LLM operation", 422) from exc
        if not request.confirmed:
            raise AIAnalysisException(
                ErrorCode.AI_ANALYSIS_CONFIRMATION_REQUIRED, "Explicit confirmation is required", 422,
            )

        analysis = self._usage.get_analysis_result(request.ai_analysis_id)
        if analysis is None or analysis.status != "succeeded":
            raise AIAnalysisException(
                ErrorCode.EXECUTIVE_REPORT_ANALYSIS_REQUIRED,
                "A succeeded AI analysis is required before generating an executive report", 422,
                {"ai_analysis_id": request.ai_analysis_id},
            )
        if analysis.actor_user_id not in {None, actor.user_id} and actor.role != "admin":
            raise AIAnalysisException(
                ErrorCode.FORBIDDEN, "AI analysis is not accessible for this actor", 403,
                {"ai_analysis_id": request.ai_analysis_id},
            )
        if not analysis.citations:
            raise AIAnalysisException(
                ErrorCode.INSUFFICIENT_CONTEXT, "Executive report requires non-empty citations", 422,
            )
        evidence = self._reload_evidence(analysis.citations, policy.evidence_max_count, policy.evidence_max_chars)
        if not evidence:
            raise AIAnalysisException(
                ErrorCode.EVIDENCE_INVALID, "Evidence is unavailable or archived", 422,
            )

        estimated_input = self._estimate_tokens(request.title, analysis.answer, evidence)
        if estimated_input > policy.max_input_tokens:
            raise AIAnalysisException(
                ErrorCode.LLM_REQUEST_COST_EXCEEDED, "Executive report input exceeds the per-request token cap", 422,
                {"max_input_tokens": policy.max_input_tokens},
            )
        estimated_cost = self._cost(estimated_input, policy.max_output_tokens, policy)
        if estimated_cost > policy.request_max_cost:
            raise AIAnalysisException(
                ErrorCode.LLM_REQUEST_COST_EXCEEDED, "Executive report exceeds the per-request cost cap", 422,
                {"max_cost": str(policy.request_max_cost), "currency": policy.currency},
            )

        task_id = request.task_id or analysis.task_id
        # Provider 调用前检查既有 Report 状态，避免高成本成功后才失败。
        if task_id is not None:
            existing_report = self._reports.get(task_id)
            if existing_report is not None and existing_report.status in {
                ReportStatus.PENDING_APPROVAL, ReportStatus.APPROVED,
                ReportStatus.PUBLISHED, ReportStatus.ARCHIVED,
            }:
                raise AIAnalysisException(
                    ErrorCode.INVALID_APPROVAL_STATE,
                    "Existing report cannot accept a new executive report version", 409,
                    {"task_id": task_id, "status": existing_report.status.value},
                )
        with self._uow.transaction():
            outcome = self._usage.reserve(
                request_id=context.request_id, idempotency_key=idempotency_key, actor=actor,
                policy=policy, input_tokens=estimated_input, output_tokens=policy.max_output_tokens,
                estimated_cost=estimated_cost, evidence=evidence, task_id=task_id,
                ai_analysis_id=request.ai_analysis_id,
            )
            if outcome.kind == "rejected":
                self._audit.record_executive_report_event(
                    context=context, actor=actor, action="executive_report.quota_rejected",
                    result="failure", status_code=429, error_code="llm_quota_exceeded",
                    usage_id=outcome.usage_id, operation=_OPERATION, route_tier=policy.route_tier,
                    analysis_id=request.ai_analysis_id,
                )

        if outcome.kind == "succeeded" and isinstance(outcome.existing_result, dict):
            return self._restore_existing(outcome.existing_result, request.title, evidence, estimated_cost)
        if outcome.kind == "reserved":
            return self._invoke_and_settle(
                outcome.usage_id, request, analysis, evidence, actor, context, policy, estimated_cost, task_id,
            )
        if outcome.kind == "rejected":
            raise AIAnalysisException(
                ErrorCode.LLM_QUOTA_EXCEEDED, "Daily high-quality LLM quota exceeded", 429,
                {"scope": outcome.rejection_code},
            )
        raise AIAnalysisException(
            ErrorCode.AI_ANALYSIS_IN_PROGRESS,
            "This executive report idempotency key is already final or in progress", 409,
            {"status": outcome.kind},
        )

    def _invoke_and_settle(
        self, usage_id: str, request: ExecutiveReportRequest, analysis, evidence,
        actor: CurrentUser, context: PersistentAuditContext, policy, estimated_cost: Decimal,
        task_id: str | None,
    ) -> ExecutiveReportResult:
        started = monotonic()
        try:
            provider_result = self._gateway.generate_report(
                operation=_OPERATION,
                request=LLMReportInput(
                    title=request.title,
                    analysis_answer=analysis.answer,
                    evidence=evidence,
                    max_output_tokens=policy.max_output_tokens,
                    request_id=context.request_id,
                    timeout_seconds=policy.timeout_seconds,
                ),
            )
        except LLMProviderPartialFailureError as exc:
            return self._fail(
                usage_id, actor, context, "provider_partial_failure", 502,
                ErrorCode.PROVIDER_FAILED, started, policy, request.ai_analysis_id,
                input_tokens=exc.input_tokens, output_tokens=exc.output_tokens, latency_ms=exc.latency_ms,
            )
        except LLMProviderTimeoutError:
            return self._fail(
                usage_id, actor, context, "provider_timeout", 504, ErrorCode.PROVIDER_TIMEOUT,
                started, policy, request.ai_analysis_id,
            )
        except LLMProviderRateLimitError:
            return self._fail(
                usage_id, actor, context, "provider_rate_limited", 429, ErrorCode.PROVIDER_RATE_LIMITED,
                started, policy, request.ai_analysis_id,
            )
        except LLMProviderAuthenticationError:
            return self._fail(
                usage_id, actor, context, "provider_authentication_failed", 502,
                ErrorCode.PROVIDER_AUTHENTICATION_FAILED, started, policy, request.ai_analysis_id,
            )
        except LLMProviderModelUnavailableError:
            return self._fail(
                usage_id, actor, context, "provider_model_unavailable", 502,
                ErrorCode.PROVIDER_MODEL_UNAVAILABLE, started, policy, request.ai_analysis_id,
            )
        except LLMProviderUnavailableError:
            return self._fail(
                usage_id, actor, context, "provider_unavailable", 502,
                ErrorCode.PROVIDER_UNAVAILABLE, started, policy, request.ai_analysis_id,
            )
        except LLMProviderResponseInvalidError:
            return self._fail(
                usage_id, actor, context, "provider_response_invalid", 502,
                ErrorCode.PROVIDER_RESPONSE_INVALID, started, policy, request.ai_analysis_id,
            )
        except LLMProviderCitationInvalidError:
            return self._fail(
                usage_id, actor, context, "provider_citation_invalid", 502,
                ErrorCode.PROVIDER_CITATION_INVALID, started, policy, request.ai_analysis_id,
            )
        except Exception:
            return self._fail(
                usage_id, actor, context, "provider_failed", 502, ErrorCode.PROVIDER_FAILED,
                started, policy, request.ai_analysis_id,
            )

        actual_cost = self._cost(provider_result.input_tokens, provider_result.output_tokens, policy)
        latency_ms = max(1, int((monotonic() - started) * 1000))
        resolved_task_id = task_id or f"task-er-{uuid4().hex}"
        report_version_id = f"rv-{uuid4().hex}"
        with self._uow.transaction():
            if self._tasks.get(resolved_task_id) is None:
                self._tasks.create(Task(
                    task_id=resolved_task_id,
                    question=request.title,
                    mode="hybrid",
                    status=TaskStatus.COMPLETED,
                ))
            report = Report(
                task_id=resolved_task_id,
                markdown=provider_result.markdown,
                provider=policy.provider_alias,
                status=ReportStatus.GENERATED,
            )
            previous = self._approvals.get_latest_report_version(resolved_task_id)
            version = ReportVersion(
                task_id=resolved_task_id,
                version_no=1 if previous is None else previous.version_no + 1,
                markdown=provider_result.markdown,
                status=ReportStatus.GENERATED,
                revision_reason=f"executive_report:{request.ai_analysis_id}",
                revised_from_version_id=previous.id if previous is not None else None,
                id=report_version_id,
                created_by=actor.user_id,
            )
            self._reports.save(report)
            self._approvals.save_report_version(version)
            result = ExecutiveReportResult(
                report_id=resolved_task_id,
                report_version_id=version.id,
                task_id=resolved_task_id,
                title=request.title,
                executive_summary=provider_result.executive_summary,
                kpi_findings=provider_result.kpi_findings,
                risks=provider_result.risks,
                recommendations=provider_result.recommendations,
                citations=evidence,
                provider_name=policy.provider_alias,
                model_name=policy.model_name,
                route_tier=policy.route_tier,
                input_tokens=provider_result.input_tokens,
                output_tokens=provider_result.output_tokens,
                total_tokens=provider_result.input_tokens + provider_result.output_tokens,
                estimated_cost=estimated_cost,
                actual_cost=actual_cost,
                currency=policy.currency,
                status="succeeded",
                created_at=version.created_at,
                analysis_id=request.ai_analysis_id,
                usage_id=usage_id,
                markdown=provider_result.markdown,
            )
            settled = self._usage.settle_report_success(
                usage_id=usage_id, result=result, latency_ms=latency_ms,
                provider_request_id=provider_result.provider_request_id,
                finish_reason=provider_result.finish_reason,
                usage_source=provider_result.usage_source,
                actual_model=provider_result.actual_model,
            )
            self._audit.record_executive_report_event(
                context=context, actor=actor, action="executive_report.generated",
                result="success", status_code=200, usage_id=usage_id,
                analysis_id=request.ai_analysis_id, report_id=resolved_task_id,
                report_version_id=version.id, token_count=settled.total_tokens,
                cost=str(settled.actual_cost), currency=settled.currency,
                operation=_OPERATION, route_tier=policy.route_tier,
                provider=policy.provider_alias, model=policy.model_name,
            )
        return settled

    def _fail(
        self, usage_id: str, actor: CurrentUser, context: PersistentAuditContext,
        error_code: str, status_code: int, public_code: ErrorCode, started: float, policy,
        analysis_id: str, input_tokens: int = 0, output_tokens: int = 0, latency_ms: int | None = None,
    ):
        assert self._usage is not None
        latency = latency_ms if latency_ms is not None else max(0, int((monotonic() - started) * 1000))
        actual_cost = self._cost(input_tokens, output_tokens, policy) if input_tokens or output_tokens else Decimal("0")
        with self._uow.transaction():
            self._usage.settle_failure(
                usage_id=usage_id, error_code=error_code, latency_ms=latency,
                input_tokens=input_tokens, output_tokens=output_tokens, actual_cost=actual_cost,
            )
            self._audit.record_executive_report_event(
                context=context, actor=actor, action="executive_report.failed",
                result="failure", status_code=status_code, error_code=error_code,
                usage_id=usage_id, operation=_OPERATION, route_tier=policy.route_tier,
                analysis_id=analysis_id,
            )
        raise AIAnalysisException(public_code, "Executive report provider failed", status_code)

    def _restore_existing(
        self, payload: dict, title: str, evidence: tuple[AIEvidence, ...], estimated_cost: Decimal,
    ) -> ExecutiveReportResult:
        version = self._approvals.get_report_version(payload["report_version_id"])
        if version is None:
            raise AIAnalysisException(
                ErrorCode.REPORT_NOT_FOUND, "Idempotent executive report version is missing", 500,
            )
        summary, kpi, risks, recommendations = self._parse_markdown(version.markdown)
        return ExecutiveReportResult(
            report_id=payload["report_id"],
            report_version_id=payload["report_version_id"],
            task_id=payload["task_id"] or payload["report_id"],
            title=title or self._title_from_markdown(version.markdown),
            executive_summary=summary,
            kpi_findings=kpi,
            risks=risks,
            recommendations=recommendations,
            citations=evidence or self._citations_from_refs(payload.get("evidence_refs") or []),
            provider_name=payload["provider_name"],
            model_name=payload["model_name"],
            route_tier=payload["route_tier"],
            input_tokens=payload["input_tokens"],
            output_tokens=payload["output_tokens"],
            total_tokens=payload["total_tokens"],
            estimated_cost=payload.get("estimated_cost") or estimated_cost,
            actual_cost=payload["actual_cost"],
            currency=payload["currency"],
            status="succeeded",
            created_at=payload["created_at"] or version.created_at,
            analysis_id=payload["analysis_id"] or "",
            usage_id=payload["usage_id"],
            markdown=version.markdown,
        )

    def _reload_evidence(
        self, citations: tuple[AIEvidence, ...], max_count: int, max_chars: int,
    ) -> tuple[AIEvidence, ...]:
        selected: list[AIEvidence] = []
        remaining = max_chars
        for item in citations[:max_count]:
            document = self._documents.get(item.document_id)
            if document is None or document.metadata.status is DocumentStatus.ARCHIVED:
                continue
            chunks = {
                chunk.chunk_id: chunk
                for chunk in self._chunks.list_for_document(item.document_id, document.metadata.version)
            }
            chunk = chunks.get(item.chunk_id)
            if chunk is None:
                continue
            excerpt = str(getattr(chunk, "content"))[:remaining]
            if not excerpt:
                break
            selected.append(AIEvidence(item.document_id, item.chunk_id, item.score, excerpt))
            remaining -= len(excerpt)
            if remaining <= 0:
                break
        return tuple(selected)

    def _estimate_tokens(self, title: str, analysis_answer: str, evidence: tuple[AIEvidence, ...]) -> int:
        return max(1, (len(title) + len(analysis_answer) + sum(len(item.excerpt) for item in evidence) + 3) // 4)

    def _cost(self, input_tokens: int, output_tokens: int, policy) -> Decimal:
        value = (
            Decimal(input_tokens) * policy.input_price_per_million
            + Decimal(output_tokens) * policy.output_price_per_million
        ) / _MILLION
        return value.quantize(_COST_QUANTUM, rounding=ROUND_UP)

    def _parse_markdown(self, markdown: str) -> tuple[str, tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
        summary = self._section_body(markdown, "Executive Summary")
        kpi = self._bullet_items(self._section_body(markdown, "KPI Findings"))
        risks = self._bullet_items(self._section_body(markdown, "Risks"))
        recommendations = self._bullet_items(self._section_body(markdown, "Recommendations"))
        return summary, kpi, risks, recommendations

    def _section_body(self, markdown: str, heading: str) -> str:
        pattern = rf"## {re.escape(heading)}\n(.*?)(?=\n## |\Z)"
        match = re.search(pattern, markdown, flags=re.S)
        return match.group(1).strip() if match else ""

    def _bullet_items(self, body: str) -> tuple[str, ...]:
        items = [line[2:].strip() for line in body.splitlines() if line.startswith("- ")]
        return tuple(items)

    def _title_from_markdown(self, markdown: str) -> str:
        for line in markdown.splitlines():
            if line.startswith("# "):
                return line[2:].strip()
        return "Executive Report"

    def _citations_from_refs(self, refs: list) -> tuple[AIEvidence, ...]:
        items: list[AIEvidence] = []
        for ref in refs:
            if not isinstance(ref, dict):
                continue
            items.append(AIEvidence(
                str(ref.get("document_id", "")),
                str(ref.get("chunk_id", "")),
                Decimal(str(ref.get("score", "0"))),
                "",
            ))
        return tuple(items)


__all__ = ["ExecutiveReportService"]
