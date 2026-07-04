# Coding Standard / 编码规范 / コーディング標準

## 1. Scope / 范围 / 範囲

These standards apply to code, tests, prompts, Mermaid diagrams, SQL, and architecture-facing docs.
这些规范适用于代码、测试、Prompt、Mermaid、SQL 和架构相关文档。
本標準はコード、テスト、Prompt、Mermaid、SQL、アーキテクチャ関連文書に適用されます。

## 2. Python / Python / Python

- Use type hints on public functions and service boundaries.
- Prefer small functions with explicit inputs and outputs.
- Keep business rules out of route handlers.
- Use structured exceptions, not generic string errors.

## 3. FastAPI / FastAPI / FastAPI

- Routes validate input, call services, and return typed schemas.
- Async task intake must return `202 Accepted` when execution continues in background.
- Request correlation ids must flow through logs and events.

## 4. TypeScript / TypeScript / TypeScript

- Use explicit domain types for API contracts and SSE events.
- Avoid `any` in contract-facing code.
- Keep API adapters separate from view logic.

## 5. React / React / React

- Components should separate page orchestration, presentational rendering, and API side effects.
- Loading, error, and completed states must be explicit.
- SSE subscriptions must clean up on unmount and task switch.

## 6. Repository / Repository / リポジトリ

- Repositories abstract storage concerns.
- Services depend on interfaces or stable contracts.
- Repository implementations must not leak storage-specific response shapes into business services.

## 7. Provider / Provider / プロバイダー

- Providers wrap replaceable sources such as research, search, model, or external data.
- Providers return stable typed results, not transport-specific raw payloads.
- Use provider names that describe source responsibility.

## 8. Workflow / Workflow / ワークフロー

- Each node must document input state, output state, mutation, and failure behavior.
- Workflow edges must be explainable and testable.
- State transitions must not depend on hidden prompt behavior alone.

## 9. Exception / Exception / 例外

- Map domain failures to stable error codes.
- Do not swallow exceptions silently.
- Error messages for operators must be short and actionable.

## 10. Mermaid / Mermaid / Mermaid

- Every important Mermaid diagram must also have a plain-text flow.
- Frozen diagrams require terminology consistency with contracts and docs.
- Mermaid nodes must use stable names already used in code and docs.

## 11. Logging / Logging / ロギング

- Use structured logs.
- Minimum fields for important flows:
  `timestamp`, `level`, `service`, `request_id`, `task_id`, `event`, `status`, `error_code`, `duration_ms`
- Never log secrets, full prompts, or confidential full documents.

## 12. Testing / Testing / テスト

- Unit tests verify pure logic and boundary checks.
- Integration tests verify repository, API, workflow, and event contracts.
- Frontend tests verify user states and SSE behavior where applicable.
- Blocked tests must declare exact blockers.

## 13. Comment / 注释 / コメント

- Core files require Chinese teaching comments in this repository.
- Comments explain responsibility, caller/callee chain, input/output, design reason, interview explanation, and enterprise replacement direction.
- Do not add noise comments that restate obvious code.

## 14. Naming / 命名 / 命名

- Use domain names, not implementation jokes or placeholders.
- Avoid `mock`, `fake`, `dummy` in core production path names for local implementations.
- Distinguish `task status` from `approval status`.

## 15. SQL / SQL / SQL

- Use explicit column names and consistent timestamps.
- Prefer additive schema changes.
- Schema names and enum meanings must match contract docs.

## 16. Migration / Migration / マイグレーション

- Every schema change needs migration intent, rollback note, and document update.
- Migration must preserve existing read paths unless a new version is introduced.
- Docs and schema must not drift.

## 17. Trilingual Key Terms / 三语术语 / 三言語用語

| English | 中文（简体） | 日本語 |
|---|---|---|
| Coding Standard | 编码规范 | コーディング標準 |
| Repository | 仓储层 | リポジトリ |
| Provider | 提供层 | プロバイダー |
| Workflow Node | 工作流节点 | ワークフローノード |
| Error Code | 错误码 | エラーコード |
| Structured Logging | 结构化日志 | 構造化ログ |

## 18. Definition / 定义 / 定義

Good code in this repository is:

- runnable,
- teachable,
- reviewable,
- contract-safe,
- and replaceable by enterprise components later.
