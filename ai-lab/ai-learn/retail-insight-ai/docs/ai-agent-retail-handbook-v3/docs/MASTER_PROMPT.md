# Master Prompt / 主主提示词 / マスタープロンプト

## 1. Purpose / 目的 / 目的

This document is the single master prompt for `Retail Insight AI`.
本文件是 `Retail Insight AI` 的唯一 Master Prompt。
本書は `Retail Insight AI` の唯一のマスタープロンプトです。

All AI tools working in this repository must follow this document before they write code, documents, tests, workflows, prompts, or Mermaid diagrams.
本仓库内的所有 AI 工具，在编写代码、文档、测试、Workflow、Prompt、Mermaid 之前，必须先遵守本文件。
本リポジトリ内のすべての AI ツールは、コード、文書、テスト、Workflow、Prompt、Mermaid を作成する前に本書へ従う必要があります。

## Master Prompt Summary / 摘要 / 要約

### Project Position

- `Retail Insight AI` is the current project.
- The current positioning is `Retail Analysis Domain Reference Implementation`.
- `Enterprise Retail Intelligence Platform (ERIP)` is only `Target State` / `Planned`, not current reality.

### Current State

- The repository is a local-first learning and reference implementation.
- `inmemory` is still the default repository backend.
- Phase 2 PostgreSQL persistence exists as an optional path and is not fully verified yet.
- Real LLM, production RAG, production approval API, Redis, and RabbitMQ are not enabled.

### Target State

- Freeze stable boundaries for Task, Workflow, Repository, Provider, Retrieval, Approval, Audit, and Documentation.
- Keep API and event evolution versioned.
- Preserve replaceable provider and repository implementations behind stable contracts.

### Execution Rules

- Read governance docs before editing.
- Follow frozen contract, prompt, coding, development, and architecture documents under `docs/`.
- Prefer contract consistency and documented assumptions over ad hoc shortcuts.

### Forbidden Operations

- Do not rewrite target-state planning as current production reality.
- Do not modify `backend/`, `frontend/`, `scripts/`, or database assets during standards-only document work unless explicitly requested.
- Do not bypass versioning, delete governance history, or hardcode secrets.

### Definition of Done

- The work is done only after scope completion, contract review, verification or blocker recording, architecture updates if needed, changelog update, and handbook mirror update.

### Three-language Documentation Rule

- Freeze-level documents must keep title, key terms, critical flow, and non-negotiable rules aligned across English, 简体中文, and 日本語.
- Human-readable project documentation is trilingual by default: English, 中文（简体）, 日本語.
- English-only is allowed only for code identifiers, API paths, class names, environment variables, enum values, error codes, and event names.
- Future sprint checklists must keep the item `Human-readable documentation is trilingual: English / 中文（简体） / 日本語` present as a permanent review reminder.

### Handbook Sync Rule

- Main project docs remain the source of truth.
- Handbook mirror docs must be updated in the same work session.
- Sync metadata blocks do not replace real handbook content updates.

### API / Event / Prompt Contract Rule

- API changes must follow `docs/API_CONTRACT.md`.
- SSE event changes must follow `docs/EVENT_CONTRACT.md`.
- Prompt family changes must follow `docs/PROMPT_STANDARD.md`.

## 2. Project Position / 项目定位 / プロジェクト位置づけ

- Current Project: `Retail Insight AI`
- Current Position: `Retail Analysis Domain Reference Implementation`
- Target Platform: `Enterprise Retail Intelligence Platform (ERIP)`
- Rule: ERIP must be described only as `Target State` or `Planned`, never as current production reality.

## 3. Architecture Freeze / 架构冻结 / アーキテクチャ凍結

- Architecture, workflow boundaries, API contracts, SSE event contracts, prompt categories, and development standards are frozen by documents under `docs/`.
- New work must extend these frozen contracts instead of redefining them.
- If a contract must change, update ADR, architecture docs, backlog, task, changelog, handbook mirror, and tests in the same change set.

## 4. Current State / 当前状态 / 現在状態

- Local-first demo and learning project.
- Default repository backend is `inmemory`.
- PostgreSQL exists as optional Phase 2 persistence path.
- No real LLM, no real OpenAI, no Redis, no RabbitMQ, no production RAG, no production approval API.
- FastAPI + React + SSE + LangGraph deterministic workflow is the current runtime baseline.

## 5. Target State / 目标状态 / 目標状態

- Stable enterprise-ready boundaries for Task, Workflow, Repository, Provider, Retrieval, Approval, Audit, and Documentation.
- Versioned APIs for new capabilities.
- Versioned SSE events for new event families.
- Replaceable provider and repository implementations without breaking service contracts.

## 6. Current Phase / 当前阶段 / 現在フェーズ

- Official runtime phase: `Phase 2: PostgreSQL Persistence MVP`
- Official documentation phase for this freeze: `Epic 14: Engineering Standards (Final Freeze)`
- Do not describe Phase 2 as fully complete until real PostgreSQL integration is verified.

## 7. Workflow Rules / Workflow 规则 / ワークフロールール

- Use deterministic workflow for bounded business processing.
- Use agentic behavior only where branching, tool selection, or open-ended research is necessary.
- Each node must define input state, output state, mutation, failure path, retry policy, and future enterprise replacement.
- Do not let prompts directly own business facts that belong in repositories or retrieval layers.

## 8. Repository Rules / Repository 规则 / リポジトリルール

- Service depends on repository interfaces, not storage details.
- `inmemory` remains the default learning path.
- PostgreSQL is opt-in until later phases promote it.
- Repository names must describe business meaning, not `mock` or `dummy`.

## 9. Provider Rules / Provider 规则 / プロバイダールール

- Providers wrap external or replaceable data/model/search sources.
- Current allowed providers are local/static providers.
- Real external providers require explicit contract docs, config docs, risk review, and tests before adoption.

## 10. Approval Rules / 审批规则 / 承認ルール

- Approval status is separate from task execution status.
- High-impact publication requires explicit approval flow.
- No irreversible approval transition without audit fields, actor identity, timestamp, and reason.

## 11. Retrieval Rules / 检索规则 / 検索ルール

- Separate:
  `Business Retrieval`
  `Internal RAG`
  `Internet Search`
- Context merge must preserve source metadata and confidence notes.
- Retrieval output must be structured input to workflow or report generation, not hidden prompt text.

## 12. RAG Rules / RAG 规则 / RAG ルール

- RAG means document source, chunking, retrieval, top-k, rerank, context assembly, answer generation, citation, ACL, evaluation, and monitoring.
- Do not claim “RAG supported” when only file reading exists.
- Internal RAG must preserve source path, chunk id, and retrieval reason.

## 13. PostgreSQL Rules / PostgreSQL 规则 / PostgreSQL ルール

- New persistence capabilities must be versioned at schema and contract level.
- SQL schema must preserve backward compatibility for active code paths.
- Migration scripts must be additive by default.
- No silent schema drift between docs and implementation.

## 14. Testing Rules / 测试规则 / テストルール

- Every phase requires unit tests, integration tests, frontend tests where applicable, and documentation verification.
- If environment blocks a test, document the exact blocker and exact manual command.
- Never report unexecuted verification as passed.

## 15. Documentation Rules / 文档规则 / ドキュメントルール

- Documentation refactor must not delete existing complete content.
- Prefer adding, organizing, and merging. Do not compress a full explanation into one sentence when the original content is valuable.
- If a table becomes hard to understand, restore it into section-based explanations.
- Keep directory structures as tree diagrams with Chinese explanations.
- Keep `docs/TEST_CASES.md` permanently as a program-flow learning document, not a command list.
- Keep `docs/LEARNING_API_WALKTHROUGH.md` permanently as an interface-learning document, not a table-only summary.
- Keep enterprise testing system explanations in `README.md`, `docs/LEARNING_API_WALKTHROUGH.md`, `docs/TEST_CASES.md`, `RUNBOOK_LOCAL.md`, and `VERIFY_CHECKLIST.md`.
- `docs/ai-agent-retail-handbook-v3/` is the learning and interview center, and `docs/ai-agent-retail-handbook-v3/docs/` is the technical spec mirror.
- Before deleting any document, first confirm that README navigation has a replacement entry and that no useful content will be lost.
- Update `TASK.md`, `docs/PROJECT_BACKLOG.md`, and `docs/CHANGELOG.md` after every completed work session.
- Update `docs/ARCHITECTURE.md` for architecture changes.
- Update `docs/DECISIONS.md` for important decisions.
- Update handbook mirror files in `docs/ai-agent-retail-handbook-v3/`.
- Do not add a new Markdown file when the same kind of content can be merged into an existing document.
- Keep `README.md` as the navigation center.
- Keep `docs/LEARNING_API_WALKTHROUGH.md` for runnable learning.
- Keep `docs/TEST_CASES.md` for test learning.
- Keep `INTERVIEW_GUIDE.md` for interview preparation in the handbook mirror.
- Keep `RUNBOOK_LOCAL.md` for startup and troubleshooting.
- Keep `VERIFY_CHECKLIST.md` for verification.
- Keep `CODE_STUDY_GUIDE.md` for source reading order.

## 16. Three-Language Rules / 三语规则 / 三言語ルール

- Every freeze-level document must include English, 简体中文, and 日本語 for:
  title,
  key terms,
  critical flow,
  and rules that future AI tools must not misread.
- One language may be primary prose, but terminology and core flow must stay aligned across three languages.

## 17. Handbook Rules / Handbook 规则 / ハンドブックルール

- Main project docs are the source of truth.
- Handbook mirror docs must be refreshed in the same session.
- Sync blocks are metadata only; they do not replace real handbook content updates.

## 18. Definition of Done / 完成定义 / 完了定義

Work is done only when all of the following are complete:

- Code or document scope completed
- Contract impact reviewed
- Tests executed or blocked with reason
- Architecture updated
- ADR updated when needed
- Task updated
- Backlog updated
- Changelog updated
- Handbook mirror updated
- Mermaid and textual flow updated where relevant

## 19. Forbidden Operations / 禁止操作 / 禁止事項

- Do not rewrite current reality into target-state marketing text.
- Do not modify backend, frontend, scripts, or database for standards-only freeze tasks unless explicitly requested.
- Do not hardcode production secrets, prompts, or credentials.
- Do not bypass versioning for new APIs or new event families.
- Do not delete backlog history, changelog history, or ADR history.

## 20. AI Execution Rules / AI 执行规则 / AI 実行ルール

- Read governance docs before editing.
- Check current phase, backlog, task, and architecture status.
- Prefer stable contracts over ad hoc implementation convenience.
- When uncertain, document assumption, scope boundary, and follow-up task.
- Treat this file as the top-level execution prompt for Codex, Claude, Gemini, Cursor Agent, and similar tools in this repository.

## 21. Code Review Rules / 代码审查规则 / コードレビュールール

- Review for contract drift first.
- Review for backward compatibility second.
- Review for observability, auditability, and test gaps third.
- Reject undocumented workflow changes, undocumented prompt changes, and undocumented event changes.

## 22. Master Prompt Template / 模板 / テンプレート

Use the following frame when an AI tool starts a non-trivial task:

```text
Project: Retail Insight AI
Position: Retail Analysis Domain Reference Implementation
Freeze Status: Architecture / Workflow / Contract / Development Standard Frozen
Current Phase: Phase 2 PostgreSQL Persistence MVP
Task Scope: <fill here>
Allowed Changes: <fill here>
Protected Areas: backend/, frontend/, scripts/ unless explicitly requested
Required Reads: AGENTS.md, ROADMAP.md, docs/PROJECT_BACKLOG.md, TASK.md
Required Outputs: TASK, Backlog, Changelog, Architecture/ADR if impacted, handbook mirror if impacted
Contract Rules: Follow docs/API_CONTRACT.md and docs/EVENT_CONTRACT.md
Prompt Rules: Follow docs/PROMPT_STANDARD.md
Coding Rules: Follow docs/CODING_STANDARD.md
Development Rules: Follow docs/DEVELOPMENT_GUIDE.md and docs/AI_AGENT_DESIGN_GUIDE.md
Definition of Done: Complete only after contracts, docs, tests, and mirrors are updated
```
