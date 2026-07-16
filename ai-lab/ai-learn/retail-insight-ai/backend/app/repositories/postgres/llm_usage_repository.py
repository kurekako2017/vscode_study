"""PostgreSQL LLM 成本 Ledger Repository。

文件职责：在数据库行锁下执行幂等占位、日额度预占和结算。
调用关系：AIAnalysisService 在三个短事务中调用；Provider 调用不在数据库事务内。
设计理由：唯一约束与 `FOR UPDATE` 是跨进程最终保障，不依赖 Python Lock/Redis。
日本现场面试：预占先提交、调模型、再结算，避免长事务锁住 quota 行。
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from app.db.connection import PostgresConnectionFactory
from app.models.ai_analysis import AIEvidence, AIAnalysisResult, ReservationOutcome
from app.security.contracts import CurrentUser


class PostgresLLMUsageRepository:
    def __init__(self, connection_factory: PostgresConnectionFactory) -> None:
        self._factory = connection_factory

    def reserve(
        self, *, request_id: str, idempotency_key: str, actor: CurrentUser,
        provider_name: str, model_name: str, input_tokens: int, output_tokens: int,
        input_price: Decimal, output_price: Decimal, estimated_cost: Decimal,
        currency: str, evidence: tuple[AIEvidence, ...], task_id: str | None,
        user_limits: tuple[int, int, Decimal], global_limits: tuple[int, int, Decimal],
    ) -> ReservationOutcome:
        """唯一键先占位，然后对 user/global bucket 稳定排序加锁。"""

        usage_id = f"llm-{uuid4().hex}"
        refs = [{"document_id": item.document_id, "chunk_id": item.chunk_id, "score": str(item.score)} for item in evidence]
        document_ids = sorted({item.document_id for item in evidence})
        with self._factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO llm_usage_ledger (
                    usage_id,request_id,idempotency_key,actor_user_id,actor_username,actor_role,
                    provider_name,model_name,operation,status,reserved_input_tokens,reserved_output_tokens,
                    input_price_per_million,output_price_per_million,estimated_cost,currency,task_id,
                    document_ids,evidence_refs)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'ai.analysis','reserved',%s,%s,%s,%s,%s,%s,%s,%s::jsonb,%s::jsonb)
                    ON CONFLICT (actor_user_id,idempotency_key) DO NOTHING RETURNING usage_id""",
                    (usage_id, request_id, idempotency_key, actor.user_id, actor.username, actor.role,
                     provider_name, model_name, input_tokens, output_tokens, input_price, output_price,
                     estimated_cost, currency, task_id, json.dumps(document_ids), json.dumps(refs)),
                )
                if cursor.fetchone() is None:
                    return self._existing(cursor, actor.user_id, idempotency_key)

                today = datetime.now(timezone.utc).date()
                scopes = (("global", "global", global_limits), ("user", actor.user_id, user_limits))
                for scope_type, scope_id, _ in scopes:
                    cursor.execute(
                        """INSERT INTO llm_quota_buckets (bucket_date,scope_type,scope_id)
                        VALUES (%s,%s,%s) ON CONFLICT DO NOTHING""", (today, scope_type, scope_id)
                    )
                reserved_tokens = input_tokens + output_tokens
                rejection: str | None = None
                for scope_type, scope_id, limits in scopes:
                    cursor.execute(
                        """SELECT request_count,token_count,cost FROM llm_quota_buckets
                        WHERE bucket_date=%s AND scope_type=%s AND scope_id=%s FOR UPDATE""",
                        (today, scope_type, scope_id),
                    )
                    request_count, token_count, cost = cursor.fetchone()
                    if request_count + 1 > limits[0] or token_count + reserved_tokens > limits[1] or Decimal(cost) + estimated_cost > limits[2]:
                        rejection = f"{scope_type}_daily_quota"
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
                        WHERE bucket_date=%s AND scope_type=%s AND scope_id=%s""",
                        (reserved_tokens, estimated_cost, today, scope_type, scope_id),
                    )
        return ReservationOutcome("reserved", usage_id)

    def settle_success(
        self, *, usage_id: str, analysis_id: str, answer: str,
        evidence: tuple[AIEvidence, ...], input_tokens: int, output_tokens: int,
        actual_cost: Decimal, latency_ms: int, provider_request_id: str, finish_reason: str,
    ) -> AIAnalysisResult:
        """结算差额并持久幂等可返回的结果快照。"""

        with self._factory.connection() as connection:
            with connection.cursor() as cursor:
                row = self._lock_usage(cursor, usage_id)
                reserved_tokens, estimated_cost, actor_user_id, provider, model, currency = row
                total = input_tokens + output_tokens
                self._adjust_buckets(cursor, actor_user_id, total - reserved_tokens, actual_cost - Decimal(estimated_cost))
                cursor.execute(
                    """UPDATE llm_usage_ledger SET status='succeeded',input_tokens=%s,output_tokens=%s,total_tokens=%s,
                    actual_cost=%s,latency_ms=%s,provider_request_id=%s,finish_reason=%s,analysis_id=%s,
                    completed_at=CURRENT_TIMESTAMP WHERE usage_id=%s AND status='reserved'""",
                    (input_tokens, output_tokens, total, actual_cost, latency_ms, provider_request_id, finish_reason, analysis_id, usage_id),
                )
                citations = [{"document_id": e.document_id, "chunk_id": e.chunk_id, "score": str(e.score), "excerpt": e.excerpt} for e in evidence]
                cursor.execute(
                    """INSERT INTO ai_analysis_results (analysis_id,usage_id,answer,citations,provider_name,model_name,
                    input_tokens,output_tokens,total_tokens,actual_cost,currency,status)
                    VALUES (%s,%s,%s,%s::jsonb,%s,%s,%s,%s,%s,%s,%s,'succeeded') RETURNING created_at""",
                    (analysis_id, usage_id, answer, json.dumps(citations, ensure_ascii=False), provider, model,
                     input_tokens, output_tokens, total, actual_cost, currency),
                )
                created_at = cursor.fetchone()[0]
        return AIAnalysisResult(analysis_id, answer, evidence, provider, model, input_tokens, output_tokens, total, actual_cost, currency, "succeeded", created_at)

    def settle_failure(self, *, usage_id: str, error_code: str, latency_ms: int | None = None) -> None:
        """失败不伪装成功；释放 token/cost 预占，保留 request attempt。"""

        with self._factory.connection() as connection:
            with connection.cursor() as cursor:
                reserved_tokens, estimated_cost, actor_user_id, *_ = self._lock_usage(cursor, usage_id)
                self._adjust_buckets(cursor, actor_user_id, -reserved_tokens, -Decimal(estimated_cost))
                cursor.execute(
                    """UPDATE llm_usage_ledger SET status='failed',error_code=%s,latency_ms=%s,
                    completed_at=CURRENT_TIMESTAMP WHERE usage_id=%s AND status='reserved'""",
                    (error_code, latency_ms, usage_id),
                )

    def _existing(self, cursor, actor_user_id: str, idempotency_key: str) -> ReservationOutcome:
        cursor.execute(
            """SELECT l.usage_id,l.status,l.error_code,r.analysis_id,r.answer,r.citations,r.provider_name,
            r.model_name,r.input_tokens,r.output_tokens,r.total_tokens,r.actual_cost,r.currency,r.status,r.created_at
            FROM llm_usage_ledger l LEFT JOIN ai_analysis_results r ON r.usage_id=l.usage_id
            WHERE l.actor_user_id=%s AND l.idempotency_key=%s""", (actor_user_id, idempotency_key)
        )
        row = cursor.fetchone()
        if row[1] == "succeeded":
            evidence = tuple(AIEvidence(item["document_id"], item["chunk_id"], Decimal(item["score"]), item["excerpt"]) for item in row[5])
            result = AIAnalysisResult(row[3], row[4], evidence, row[6], row[7], row[8], row[9], row[10], Decimal(row[11]), row[12].strip(), row[13], row[14])
            return ReservationOutcome("succeeded", row[0], existing_result=result)
        return ReservationOutcome(row[1], row[0], rejection_code=row[2])

    def _lock_usage(self, cursor, usage_id: str):
        cursor.execute(
            """SELECT reserved_input_tokens+reserved_output_tokens,estimated_cost,actor_user_id,
            provider_name,model_name,currency FROM llm_usage_ledger WHERE usage_id=%s FOR UPDATE""", (usage_id,)
        )
        row = cursor.fetchone()
        if row is None:
            raise KeyError("LLM usage reservation not found")
        return row

    def _adjust_buckets(self, cursor, actor_user_id: str, token_delta: int, cost_delta: Decimal) -> None:
        today = datetime.now(timezone.utc).date()
        for scope_type, scope_id in (("global", "global"), ("user", actor_user_id)):
            cursor.execute(
                """UPDATE llm_quota_buckets SET token_count=GREATEST(0,token_count+%s),
                cost=GREATEST(0,cost+%s),updated_at=CURRENT_TIMESTAMP
                WHERE bucket_date=%s AND scope_type=%s AND scope_id=%s""",
                (token_delta, cost_delta, today, scope_type, scope_id),
            )


__all__ = ["PostgresLLMUsageRepository"]
