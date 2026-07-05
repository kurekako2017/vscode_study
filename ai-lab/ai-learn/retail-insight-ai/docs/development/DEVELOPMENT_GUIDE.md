# Development Guide / 开发指南 / 開発ガイド

## 1. Purpose / 目的 / 目的

Use this guide when adding new capabilities without breaking frozen standards.
新增能力时，按本指南执行，避免破坏冻结规范。
新機能追加時は、本ガイドに従い凍結済み標準を破壊しないこと。

## 2. Add a New API / 新增 API / 新規 API 追加

1. Check whether an existing endpoint can be extended safely.
2. If it is new, version it under `/api/v1/...`.
3. Define request, response, statuses, and error codes in `docs/contracts/API_CONTRACT.md`.
4. Add tests for success, validation failure, and not-found or conflict paths.
5. Update handbook mirror.

## 3. Add a New Repository / 新增 Repository / 新規 Repository 追加

1. Define repository interface responsibility.
2. Keep service contract unchanged where possible.
3. Document current implementation and future enterprise replacement.
4. Add integration tests for persistence behavior.

## 4. Add a New Provider / 新增 Provider / 新規 Provider 追加

1. Define what source it wraps.
2. Define typed provider output.
3. Define failure mapping and retry policy.
4. Document config and secrets boundary.

## 5. Add a New Workflow / 新增 Workflow / 新規 Workflow 追加

1. Define state shape.
2. Define nodes, edges, routing conditions, and terminal conditions.
3. Define approval or interrupt points if the workflow is high impact.
4. Add Mermaid plus plain-text flow.

## 6. Add PostgreSQL Capability / 新增 PostgreSQL / PostgreSQL 追加

1. Define schema and migration intent.
2. Preserve old read/write path or introduce a versioned path.
3. Update repository contract, architecture docs, and verification commands.
4. Record environment blockers if real integration cannot run.

## 7. Add RAG Capability / 新增 RAG / RAG 追加

1. Define document source.
2. Define chunk strategy.
3. Define retrieval strategy, top-k, filters, rerank, and context merge.
4. Define citation output and evaluation path.
5. Document ACL and hallucination risk controls.

## 8. Add Approval Capability / 新增审批 / 承認機能追加

1. Separate task status from approval status.
2. Define approval request and approval event contracts.
3. Require audit fields for human actions.
4. Define retry, reject, revise, publish, and archive boundaries.

## 9. Add a Test / 新增测试 / テスト追加

1. Define goal.
2. Define input source.
3. Define expected output.
4. Define acceptance criteria.
5. Add Mermaid and text flow if the test documents a business process.

## 10. Add Handbook Content / 新增 Handbook / ハンドブック追加

1. Update the main project doc first.
2. Mirror the content in `docs/ai-agent-retail-handbook-v3/`.
3. Refresh sync blocks.
4. Keep handbook educational wording aligned with the project source of truth.

## 11. Add Mermaid / 新增 Mermaid / Mermaid 追加

1. Keep node names aligned with code and contracts.
2. Add English, 中文（简体）, 日本語 labels for freeze-level diagrams.
3. Add plain-text flow directly below or above the diagram.

## 12. Standard Delivery Checklist / 交付清单 / 標準チェックリスト

- Contract updated
- Tests added or blocker documented
- Architecture updated if needed
- ADR updated if needed
- Task updated
- Backlog updated
- Changelog updated
- Handbook mirror updated
- [ ] Human-readable documentation is trilingual: English / 中文（简体） / 日本語
- Keep the trilingual checklist item in future sprint planning so the rule remains a standing review point.
