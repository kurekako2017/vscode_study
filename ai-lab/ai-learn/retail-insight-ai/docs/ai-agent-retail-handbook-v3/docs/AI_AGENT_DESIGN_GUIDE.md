# AI Agent Design Guide / AI Agent 设计指南 / AI エージェント設計ガイド

## 1. Purpose / 目的 / 目的

This guide explains when to use workflow, agent, tool, repository, provider, retrieval, approval, and related enterprise controls.
本指南说明什么时候使用 workflow、agent、tool、repository、provider、retrieval、approval 以及相关企业控制。
本ガイドは workflow、agent、tool、repository、provider、retrieval、approval と関連する企業制御をいつ使うべきかを説明します。

## 2. Workflow vs Agent / Workflow 与 Agent / Workflow と Agent

- Use `Workflow` for deterministic, bounded, auditable business flow.
- Use `Agent` for open-ended research, tool choice, or iterative reasoning with clear guardrails.
- Prefer workflow first when both can solve the problem.

## 3. Tool / Tool / ツール

- Use a tool when a capability is external, side-effectful, or permission-sensitive.
- Define schema, timeout, error mapping, and audit requirements.

## 4. Repository / Repository / リポジトリ

- Use a repository for persistent business facts and state history.
- Do not use prompts as state storage.

## 5. Provider / Provider / プロバイダー

- Use a provider for replaceable source integrations.
- Good provider examples: research source, internet search source, document retrieval source, model provider.
- For model integrations, freeze an explicit `LLMProvider` concept so the model backend can change without affecting retrieval or API contracts.
- Provider contracts should include timeout, retry, usage accounting, and provider error mapping.
- Track placeholder fields for tokens, cost, latency, model name, and provider name even before real billing is introduced.

### `RAGAnswerGenerator`

- Use `RAGAnswerGenerator` as the answer assembly boundary between retrieval results and a future `LLMProvider`.
- It binds prompt inputs and validates prompt outputs, but it does not own retrieval, storage, or approval state.
- If provider output is unavailable, times out, is invalid, misses citations, or exceeds cost limits, fall back to deterministic extractive mode.

## 6. Business Retrieval / 业务检索 / 業務データ検索

- Use for structured internal facts such as sales, inventory, members, promotions.
- Prefer deterministic query generation and clear source windows.

## 7. Internal RAG / 内部 RAG / 社内 RAG

- Use for internal documents, manuals, policies, FAQs, and uploaded files.
- Use after retrieval when a grounded answer with citations is needed.
- Requires chunking, metadata, citation, ACL, evaluation, and a citation-safe answer contract.
- Keep the current no-LLM path as the default implementation until a future provider is explicitly wired in.
- `RAGAnswerGenerator` must not change the frozen `/api/v1/internal-rag/answer` response contract.

## 8. Internet Search / 互联网检索 / インターネット検索

- Use only for public external evidence such as market and competitor signals.
- Requires source trust review, freshness review, and citation.

## 9. Hybrid Search / 混合检索 / ハイブリッド検索

- Use only when keyword, structured facts, and semantic retrieval all add value.
- Define ranking, merge, and conflict resolution rules explicitly.

## 10. Approval / 审批 / 承認

- Use approval for publication, policy-sensitive outputs, and high-impact recommendations.
- Approval must be auditable and reversible where possible.

## 11. Human Review / 人工复核 / 人間レビュー

- Use human review when business risk, policy ambiguity, or evidence quality is high.
- Human review outcome must become structured system state, not hidden chat context.

## 12. Memory / 记忆 / メモリ

- Use memory only when repeated interactions benefit from explicit retained context.
- Separate transient workflow state from durable business memory.

## 13. MCP / MCP / MCP

- Use MCP when model-facing tools need standardized discovery, schema, and permission boundaries.
- Keep core business services stable behind internal APIs even when MCP is introduced.

## 14. Prompt / Prompt / プロンプト

- Use prompts for reasoning and language generation, not as a substitute for contracts or repositories.
- Prompt versions must be documented.
- Prompt families that drive `RAGAnswerGenerator` must document input fields, output schema, fallback mode, and provider assumptions separately from the retrieval provider contract.

## 15. Evaluation / 评估 / 評価

- Every agentic path must define quality evaluation, failure review, and rollback expectations.
- Evaluation covers correctness, citation quality, latency, and operator trust.

## 16. Audit / 审计 / 監査

- High-impact actions require audit trail:
  actor, request_id, trace_id, action, target, result, timestamp.

## 17. RBAC / RBAC / RBAC

- Use RBAC when data scope or action scope differs by role, department, or store.
- Retrieval and approval must respect RBAC boundaries.

## 18. Design Decision Matrix / 设计判断矩阵 / 設計判断マトリクス

| Need | Preferred Choice | Why |
|---|---|---|
| Fixed business process | Workflow | deterministic and testable |
| Open-ended evidence gathering | Agent + Tool | bounded autonomy |
| Durable fact storage | Repository | audit and replay |
| Replaceable integration | Provider | isolation and swapability |
| Structured internal facts | Business Retrieval | deterministic grounding |
| Internal docs | Internal RAG | retrieval + citation + grounded answer |
| Public web evidence | Internet Search | freshness and evidence |
| High-risk publication | Approval + Human Review | accountability |

## 19. Text Flow / 纯文本流程 / テキストフロー

```text
Business requirement arrives
│
├── deterministic and bounded -> Workflow
├── open-ended evidence gathering -> Agent
├── external capability needed -> Tool / Provider
├── persistent state needed -> Repository
├── structured facts needed -> Business Retrieval
├── document evidence needed -> Internal RAG
├── public evidence needed -> Internet Search
└── high-impact output -> Approval + Human Review + Audit
```
