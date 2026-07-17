"""PostgreSQL LLM 成本 Ledger Repository。

文件职责：在数据库行锁下执行幂等占位、按 route_tier 的日额度预占和结算。
调用关系：AIAnalysisService / ExecutiveReportService 在短事务中调用；Provider 不在事务内。
设计理由：唯一约束与 FOR UPDATE 是跨进程最终保障；额度桶按 low_cost/high_quality 分离。
日本现场面试：预占先提交、调模型、再结算，避免长事务锁住 quota 行。
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any
from uuid import uuid4

from app.db.connection import PostgresConnectionFactory
from app.llm.operation_policy import OperationPolicy
from app.models.ai_analysis import (
    AIEvidence,
    AIAnalysisResult,
    ExecutiveReportResult,
    ReservationOutcome,
)
from app.security.contracts import CurrentUser


class PostgresLLMUsageRepository:
    def __init__(self, connection_factory: PostgresConnectionFactory) -> None:
        self._factory = connection_factory

    def reserve(
        self, *, request_id: str, idempotency_key: str, actor: CurrentUser,
        policy: OperationPolicy, input_tokens: int, output_tokens: int,
        estimated_cost: Decimal, evidence: tuple[AIEvidence, ...],
        task_id: str | None, ai_analysis_id: str | None = None,
    ) -> ReservationOutcome:
        """唯一键先占位，然后对 user/global + route_tier bucket 稳定排序加锁。"""

        usage_id = f"llm-{uuid4().hex}"
        refs = [{"document_id": item.document_id, "chunk_id": item.chunk_id, "score": str(item.score)} for item in evidence]
        document_ids = sorted({item.document_id for item in evidence})
        with self._factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO llm_usage_ledger (
                    usage_id,request_id,idempotency_key,actor_user_id,actor_username,actor_role,
                    provider_name,model_name,operation,route_tier,selected_provider,selected_model,
                    policy_snapshot,token_limit_snapshot,price_snapshot,
                    status,reserved_input_tokens,reserved_output_tokens,
                    input_price_per_million,output_price_per_million,estimated_cost,currency,task_id,
                    document_ids,evidence_refs,ai_analysis_id)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb,%s::jsonb,%s::jsonb,
                    'reserved',%s,%s,%s,%s,%s,%s,%s,%s::jsonb,%s::jsonb,%s)
                    ON CONFLICT (actor_user_id,idempotency_key) DO NOTHING RETURNING usage_id""",
                    (
                        usage_id, request_id, idempotency_key, actor.user_id, actor.username, actor.role,
                        policy.provider_alias, policy.model_name, policy.operation, policy.route_tier,
                        policy.provider_alias, policy.model_name,
                        json.dumps(policy.snapshot()), json.dumps(policy.token_limit_snapshot()),
                        json.dumps(policy.price_snapshot()),
                        input_tokens, output_tokens,
                        policy.input_price_per_million, policy.output_price_per_million,
                        estimated_cost, policy.currency, task_id,
                        json.dumps(document_ids), json.dumps(refs), ai_analysis_id,
                    ),
                )
                if cursor.fetchone() is None:
                    return self._existing(cursor, actor.user_id, idempotency_key)

                today = datetime.now(timezone.utc).date()
                scopes = (
                    ("global", "global", (
                        policy.global_daily_request_limit,
                        policy.global_daily_token_limit,
                        policy.global_daily_cost_limit,
                    )),
                    ("user", actor.user_id, (
                        policy.user_daily_request_limit,
                        policy.user_daily_token_limit,
                        policy.user_daily_cost_limit,
                    )),
                )
                for scope_type, scope_id, _ in scopes:
                    cursor.execute(
                        """INSERT INTO llm_quota_buckets (bucket_date,scope_type,scope_id,route_tier)
                        VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
                        (today, scope_type, scope_id, policy.route_tier),
                    )
                reserved_tokens = input_tokens + output_tokens
                rejection: str | None = None
                for scope_type, scope_id, limits in scopes:
                    cursor.execute(
                        """SELECT request_count,token_count,cost FROM llm_quota_buckets
                        WHERE bucket_date=%s AND scope_type=%s AND scope_id=%s AND route_tier=%s FOR UPDATE""",
                        (today, scope_type, scope_id, policy.route_tier),
                    )
                    request_count, token_count, cost = cursor.fetchone()
                    if (
                        request_count + 1 > limits[0]
                        or token_count + reserved_tokens > limits[1]
                        or Decimal(cost) + estimated_cost > limits[2]
                    ):
                        rejection = f"{scope_type}_{policy.route_tier}_daily_quota"
                        break
                if rejection is not None:
                    cursor.execute(
                        """UPDATE llm_usage_ledger SET status='rejected',error_code=%s,completed_at=CURRENT_TIMESTAMP
                        WHERE usage_id=%s""", (rejection, usage_id)
                    )
                    return ReservationOutcome("rejected", usage_id, rejection_code=rejection)
                for scope_type, scope_id, _ in scopes:
                    cursor.execute(
                        """UPDATE llm_quota_buckets SET request_count=request_count+1,
                        token_count=token_count+%s,cost=cost+%s,updated_at=CURRENT_TIMESTAMP
                        WHERE bucket_date=%s AND scope_type=%s AND scope_id=%s AND route_tier=%s""",
                        (reserved_tokens, estimated_cost, today, scope_type, scope_id, policy.route_tier),
                    )
        return ReservationOutcome("reserved", usage_id)

    def settle_analysis_success(
        self, *, usage_id: str, analysis_id: str, answer: str,
        evidence: tuple[AIEvidence, ...], input_tokens: int, output_tokens: int,
        actual_cost: Decimal, latency_ms: int, provider_request_id: str, finish_reason: str,
        usage_source: str = "provider_reported", actual_model: str | None = None,
    ) -> AIAnalysisResult:
        """结算 AI 分析差额并持久幂等结果快照。"""

        with self._factory.connection() as connection:
            with connection.cursor() as cursor:
                row = self._lock_usage(cursor, usage_id)
                reserved_tokens, estimated_cost, actor_user_id, provider, model, currency, route_tier = row
                total = input_tokens + output_tokens
                settled_model = actual_model or model
                self._adjust_buckets(
                    cursor, actor_user_id, route_tier, total - reserved_tokens,
                    actual_cost - Decimal(estimated_cost),
                )
                cursor.execute(
                    """UPDATE llm_usage_ledger SET status='succeeded',input_tokens=%s,output_tokens=%s,total_tokens=%s,
                    actual_cost=%s,latency_ms=%s,provider_request_id=%s,finish_reason=%s,analysis_id=%s,
                    ai_analysis_id=%s,selected_model=%s,
                    policy_snapshot=policy_snapshot || %s::jsonb,
                    completed_at=CURRENT_TIMESTAMP
                    WHERE usage_id=%s AND status='reserved'""",
                    (
                        input_tokens, output_tokens, total, actual_cost, latency_ms,
                        provider_request_id, finish_reason, analysis_id, analysis_id,
                        settled_model,
                        json.dumps({"usage_source": usage_source, "actual_model": settled_model}),
                        usage_id,
                    ),
                )
                citations = [
                    {
                        "document_id": e.document_id,
                        "chunk_id": e.chunk_id,
                        "score": str(e.score),
                        "excerpt": e.excerpt,
                    }
                    for e in evidence
                ]
                cursor.execute(
                    """INSERT INTO ai_analysis_results (analysis_id,usage_id,answer,citations,provider_name,model_name,
                    input_tokens,output_tokens,total_tokens,actual_cost,currency,status)
                    VALUES (%s,%s,%s,%s::jsonb,%s,%s,%s,%s,%s,%s,%s,'succeeded') RETURNING created_at""",
                    (
                        analysis_id, usage_id, answer, json.dumps(citations, ensure_ascii=False),
                        provider, settled_model, input_tokens, output_tokens, total, actual_cost, currency,
                    ),
                )
                created_at = cursor.fetchone()[0]
        return AIAnalysisResult(
            analysis_id, answer, evidence, provider, settled_model, input_tokens, output_tokens, total,
            actual_cost, currency, "succeeded", created_at, route_tier, Decimal(estimated_cost),
        )

    def settle_report_success(
        self, *, usage_id: str, result: ExecutiveReportResult,
        latency_ms: int = 0, provider_request_id: str | None = None, finish_reason: str = "stop",
        usage_source: str = "provider_reported", actual_model: str | None = None,
    ) -> ExecutiveReportResult:
        """结算董事会报告并写回 report/version 关联，不把报告正文写入 Ledger。"""

        with self._factory.connection() as connection:
            with connection.cursor() as cursor:
                reserved_tokens, estimated_cost, actor_user_id, _provider, model, _currency, route_tier = (
                    self._lock_usage(cursor, usage_id)
                )
                total = result.input_tokens + result.output_tokens
                settled_model = actual_model or model
                self._adjust_buckets(
                    cursor, actor_user_id, route_tier, total - reserved_tokens,
                    result.actual_cost - Decimal(estimated_cost),
                )
                cursor.execute(
                    """UPDATE llm_usage_ledger SET status='succeeded',input_tokens=%s,output_tokens=%s,total_tokens=%s,
                    actual_cost=%s,latency_ms=%s,provider_request_id=%s,finish_reason=%s,
                    analysis_id=%s,ai_analysis_id=%s,report_id=%s,report_version_id=%s,task_id=%s,
                    selected_model=%s,policy_snapshot=policy_snapshot || %s::jsonb,
                    completed_at=CURRENT_TIMESTAMP
                    WHERE usage_id=%s AND status='reserved'""",
                    (
                        result.input_tokens, result.output_tokens, total, result.actual_cost,
                        latency_ms, provider_request_id or f"report:{result.report_version_id}", finish_reason,
                        result.analysis_id, result.analysis_id, result.report_id,
                        result.report_version_id, result.task_id,
                        settled_model,
                        json.dumps({"usage_source": usage_source, "actual_model": settled_model}),
                        usage_id,
                    ),
                )
        return result

    def settle_failure(
        self, *, usage_id: str, error_code: str, latency_ms: int | None = None,
        input_tokens: int = 0, output_tokens: int = 0,
        actual_cost: Decimal = Decimal("0"),
    ) -> None:
        """失败不伪装成功；释放 token/cost 预占，保留 request attempt。"""

        with self._factory.connection() as connection:
            with connection.cursor() as cursor:
                reserved_tokens, estimated_cost, actor_user_id, *_rest, route_tier = self._lock_usage(cursor, usage_id)
                total = input_tokens + output_tokens
                self._adjust_buckets(
                    cursor, actor_user_id, route_tier, total - reserved_tokens,
                    actual_cost - Decimal(estimated_cost),
                )
                cursor.execute(
                    """UPDATE llm_usage_ledger SET status='failed',error_code=%s,latency_ms=%s,
                    input_tokens=%s,output_tokens=%s,total_tokens=%s,actual_cost=%s,
                    completed_at=CURRENT_TIMESTAMP WHERE usage_id=%s AND status='reserved'""",
                    (error_code, latency_ms, input_tokens, output_tokens, total, actual_cost, usage_id),
                )

    def get_analysis_result(self, analysis_id: str) -> AIAnalysisResult | None:
        """读取已成功 AI Analysis；Executive Report 前置门禁用。"""

        with self._factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT r.analysis_id,r.answer,r.citations,r.provider_name,r.model_name,
                    r.input_tokens,r.output_tokens,r.total_tokens,r.actual_cost,r.currency,r.status,r.created_at,
                    COALESCE(l.route_tier,'low_cost'),l.actor_user_id,l.estimated_cost,l.evidence_refs,l.task_id
                    FROM ai_analysis_results r
                    JOIN llm_usage_ledger l ON l.usage_id=r.usage_id
                    WHERE r.analysis_id=%s AND r.status='succeeded'""",
                    (analysis_id,),
                )
                row = cursor.fetchone()
        if row is None:
            return None
        evidence = tuple(
            AIEvidence(item["document_id"], item["chunk_id"], Decimal(item["score"]), item["excerpt"])
            for item in row[2]
        )
        return AIAnalysisResult(
            row[0], row[1], evidence, row[3], row[4], row[5], row[6], row[7],
            Decimal(row[8]), row[9].strip(), row[10], row[11], row[12], Decimal(row[14]),
            actor_user_id=row[13], task_id=row[16],
        )

    def get_succeeded_report_by_idempotency(
        self, *, actor_user_id: str, idempotency_key: str,
    ) -> tuple[str, str, str] | None:
        """返回 (usage_id, report_id, report_version_id) 供幂等重放。"""

        with self._factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT usage_id,report_id,report_version_id,status FROM llm_usage_ledger
                    WHERE actor_user_id=%s AND idempotency_key=%s""",
                    (actor_user_id, idempotency_key),
                )
                row = cursor.fetchone()
        if row is None or row[3] != "succeeded" or not row[1] or not row[2]:
            return None
        return row[0], row[1], row[2]

    def _existing(self, cursor, actor_user_id: str, idempotency_key: str) -> ReservationOutcome:
        cursor.execute(
            """SELECT l.usage_id,l.status,l.error_code,l.operation,l.route_tier,
            l.report_id,l.report_version_id,l.task_id,l.ai_analysis_id,l.estimated_cost,
            r.analysis_id,r.answer,r.citations,r.provider_name,r.model_name,
            r.input_tokens,r.output_tokens,r.total_tokens,r.actual_cost,r.currency,r.status,r.created_at,
            l.provider_name,l.model_name,l.input_tokens,l.output_tokens,l.total_tokens,l.actual_cost,l.currency,
            l.completed_at,l.evidence_refs
            FROM llm_usage_ledger l
            LEFT JOIN ai_analysis_results r ON r.usage_id=l.usage_id
            WHERE l.actor_user_id=%s AND l.idempotency_key=%s""",
            (actor_user_id, idempotency_key),
        )
        row = cursor.fetchone()
        if row[1] == "succeeded" and row[3] == "ai_analysis" and row[10] is not None:
            evidence = tuple(
                AIEvidence(item["document_id"], item["chunk_id"], Decimal(item["score"]), item["excerpt"])
                for item in row[12]
            )
            result = AIAnalysisResult(
                row[10], row[11], evidence, row[13], row[14], row[15], row[16], row[17],
                Decimal(row[18]), row[19].strip(), row[20], row[21], row[4], Decimal(row[9]),
            )
            return ReservationOutcome("succeeded", row[0], existing_result=result)
        if row[1] == "succeeded" and row[3] == "executive_report" and row[5] and row[6]:
            # 服务层会加载 Report/ReportVersion 重建完整结果。
            return ReservationOutcome(
                "succeeded",
                row[0],
                existing_result={
                    "kind": "executive_report",
                    "usage_id": row[0],
                    "report_id": row[5],
                    "report_version_id": row[6],
                    "task_id": row[7],
                    "analysis_id": row[8],
                    "route_tier": row[4],
                    "provider_name": row[22],
                    "model_name": row[23],
                    "input_tokens": row[24],
                    "output_tokens": row[25],
                    "total_tokens": row[26],
                    "actual_cost": Decimal(row[27]),
                    "estimated_cost": Decimal(row[9]),
                    "currency": row[28].strip() if isinstance(row[28], str) else str(row[28]).strip(),
                    "created_at": row[29],
                    "evidence_refs": row[30] or [],
                },
            )
        if row[1] == "reserved":
            return ReservationOutcome("in_progress", row[0])
        return ReservationOutcome(row[1], row[0], rejection_code=row[2])

    def _lock_usage(self, cursor, usage_id: str):
        cursor.execute(
            """SELECT reserved_input_tokens+reserved_output_tokens,estimated_cost,actor_user_id,
            provider_name,model_name,currency,route_tier FROM llm_usage_ledger WHERE usage_id=%s FOR UPDATE""",
            (usage_id,),
        )
        row = cursor.fetchone()
        if row is None:
            raise KeyError("LLM usage reservation not found")
        return row

    def _adjust_buckets(
        self, cursor, actor_user_id: str, route_tier: str, token_delta: int, cost_delta: Decimal,
    ) -> None:
        today = datetime.now(timezone.utc).date()
        for scope_type, scope_id in (("global", "global"), ("user", actor_user_id)):
            cursor.execute(
                """UPDATE llm_quota_buckets SET token_count=GREATEST(0,token_count+%s),
                cost=GREATEST(0,cost+%s),updated_at=CURRENT_TIMESTAMP
                WHERE bucket_date=%s AND scope_type=%s AND scope_id=%s AND route_tier=%s""",
                (token_delta, cost_delta, today, scope_type, scope_id, route_tier),
            )


__all__ = ["PostgresLLMUsageRepository"]
