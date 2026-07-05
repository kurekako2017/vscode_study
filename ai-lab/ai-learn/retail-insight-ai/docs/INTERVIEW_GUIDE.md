# INTERVIEW GUIDE

English summary: this is the first-pass interview narrative for Retail Insight AI. It explains what the project is, what the backend currently does, what I own, and how to answer the most likely interview questions without overstating unfinished work.
中文（简体）摘要：这是 Retail Insight AI 的第一版面试讲解稿，重点说明项目是什么、后端现在能做什么、我负责什么，以及怎么回答常见问题，同时不夸大未完成能力。
日本語要約：これは Retail Insight AI の面接向け一次説明資料です。何のプロジェクトか、backend が現在何をできるか、私の担当範囲、よくある質問への答え方を、未完了機能を誇張せずに整理しています。

## One-Sentence Overview / 一句话介绍 / 一言説明

- English: Retail Insight AI is a local-first learning project that demonstrates a full backend workflow for document handling, task analysis, deterministic internal RAG, approval, RBAC, and audit logging without requiring a real LLM or PostgreSQL.
- 中文（简体）：Retail Insight AI 是一个偏本地学习的项目，演示了文档处理、任务分析、确定性内部 RAG、审批、RBAC 和审计日志的完整后端链路，但不依赖真实 LLM 或 PostgreSQL。
- 日本語：Retail Insight AI は、本物の LLM や PostgreSQL に依存せず、ドキュメント処理、タスク分析、決定論的内部 RAG、承認、RBAC、監査ログの一連の backend フローを学べるローカル重視の学習プロジェクトです。

## Project Background / 项目背景 / 背景

| Topic | English | 中文（简体） | 日本語 |
| --- | --- | --- | --- |
| Why this exists | Learn Japanese-style AI agent delivery in a runnable codebase | 在可运行代码库里学习日本现场的 AI Agent 交付方式 | 日本の現場に近い形で AI Agent の進め方を学ぶため |
| Business value | Explain sales and operations analysis as a repeatable system | 把经营分析做成可重复说明的系统 | 経営分析を繰り返し説明できるシステムにするため |
| Current phase | Local static providers, in-memory/local repositories, FastAPI, React, SSE | 本地静态提供方、InMemory/本地仓库、FastAPI、React、SSE | ローカルの静的プロバイダ、InMemory/ローカルリポジトリ、FastAPI、React、SSE |

## System Architecture / 系统架构 / システム構成

```text
React -> FastAPI -> Task API -> TaskService -> Workflow -> KPI Engine -> Research Provider -> Report Generator -> SSE -> React
```

- English: the backend is split by responsibility, not by UI screens.
- 中文（简体）：后端是按职责拆分的，不是按页面拆分的。
- 日本語：backend は画面単位ではなく責務単位で分かれています。

## Tech Stack / 技术栈 / 技術スタック

| Layer | English | 中文（简体） | 日本語 |
| --- | --- | --- | --- |
| API | FastAPI | FastAPI | FastAPI |
| Workflow | LangGraph | LangGraph | LangGraph |
| UI | React | React | React |
| Storage | InMemory / local files | InMemory / 本地文件 | InMemory / ローカルファイル |
| Streaming | SSE | SSE | SSE |
| Testing | `unittest`, `compileall` | `unittest`、`compileall` | `unittest`、`compileall` |

## What I Own / 我负责的部分 / 担当範囲

- English: backend routes, services, repository seams, workflow seams, audit seams, and learning documentation.
- 中文（简体）：后端路由、服务层、仓库接缝、工作流接缝、审计接缝和学习文档。
- 日本語：backend のルート、service 層、repository の接続点、workflow の接続点、audit の接続点、学習文書です。

## Core Features / 核心功能 / コア機能

| Feature | English | 中文（简体） | 日本語 |
| --- | --- | --- | --- |
| Task chain | Create a task, stream status, fetch a report | 创建任务、推送状态、取回报告 | タスク作成、状態配信、レポート取得 |
| Documents | Upload, read, archive, import, chunk, retrieve | 上传、读取、归档、导入、切分、检索 | アップロード、読取、アーカイブ、インポート、チャンク、検索 |
| Internal RAG | Deterministic answer generation without LLM | 不接 LLM 的确定性答案生成 | LLM なしの決定論的な回答生成 |
| Approval | Submit, review, approve, reject | 提交审批、查看、批准、拒绝 | 承認申請、閲覧、承認、却下 |
| Security | Current user, roles, permissions, audit logs | 当前用户、角色、权限、审计日志 | 現在ユーザー、ロール、権限、監査ログ |

## API Main Chain / API 主链路 / API の主経路

1. `POST /api/tasks`
2. `GET /api/tasks/{task_id}`
3. `GET /api/tasks/{task_id}/report`
4. `POST /api/v1/documents`
5. `POST /api/v1/documents/{document_id}/import`
6. `POST /api/v1/documents/{document_id}/chunks`
7. `POST /api/v1/document-retrieval/search`
8. `POST /api/v1/internal-rag/answer`
9. `POST /api/v1/reports/{task_id}/submit-approval`
10. `GET /api/v1/users/me`
11. `GET /api/v1/security/roles`
12. `GET /api/v1/security/permissions`
13. `GET /api/v1/audit-logs`

English: this is the story I would tell as “request in, structured processing, safe persistence, response out.”
中文（简体）：我会把这条链路讲成“请求进来、结构化处理、安全落盘、再返回结果”。
日本語：この流れは「リクエストを受け、構造化して、安全に保存し、結果を返す」と説明します。

## RAG Design / RAG 怎么设计 / RAG の設計

- English: document chunks are retrieved locally with keyword search, then the answer is assembled deterministically so the project stays explainable and testable.
- 中文（简体）：文档 chunk 先做本地关键字检索，再用确定性规则组装答案，这样项目更容易解释和测试。
- 日本語：文書チャンクをローカルのキーワード検索で取得し、決定論的に回答を組み立てることで、説明しやすくテストしやすい状態を保ちます。

## Approval Workflow / 审批工作流 / 承認ワークフロー

- English: reports move into an approval state after generation, and approval actions are split into submit/review/approve/reject so the contract is explicit.
- 中文（简体）：报告生成后进入审批状态，审批动作拆成提交、查看、批准、拒绝，合同更清晰。
- 日本語：レポート生成後に承認状態へ進み、承認アクションを申請・閲覧・承認・却下に分けて契約を明確にしています。

## RBAC / Audit Design / RBAC 与审计设计 / RBAC と監査設計

- English: approval endpoints are guarded by permission checks, and denied access writes append-only audit facts.
- 中文（简体）：审批接口由权限校验保护，拒绝访问会写入追加式审计事实。
- 日本語：承認 API は権限チェックで守られ、拒否時には append-only の監査事実が記録されます。

## Why Repository Pattern / 为什么用 Repository Pattern / なぜ Repository Pattern か

- English: it isolates storage details from services, so in-memory and PostgreSQL can be swapped without rewriting business logic.
- 中文（简体）：它把存储细节从服务层隔离出去，后面切换 InMemory 和 PostgreSQL 时不用重写业务逻辑。
- 日本語：保存の詳細を service から分離するので、InMemory と PostgreSQL を入れ替えても業務ロジックを大きく書き換えずに済みます。

## Why Provider Pattern / 为什么用 Provider Pattern / なぜ Provider Pattern か

- English: it lets the project replace local static research or LLM logic later without changing the workflow contract.
- 中文（简体）：它让本地静态 Research 或未来 LLM 实现可以替换，而不改变工作流合同。
- 日本語：ローカルの静的 Research や将来の LLM 実装を差し替えても、workflow 契約を変えずに済みます。

## Why InMemory by Default / 为什么现在默认 InMemory / なぜ今は InMemory か

- English: the default must be runnable in one machine with zero infrastructure setup.
- 中文（简体）：默认必须能在一台机器上跑起来，不需要额外基础设施。
- 日本語：デフォルトは 1 台のマシンで追加インフラなしに起動できる必要があります。

## Future Expansion / 后续怎么扩展 / 今後どう拡張するか

| Future area | English | 中文（简体） | 日本語 |
| --- | --- | --- | --- |
| PostgreSQL | Replace selected repositories while keeping API contracts stable | 替换部分仓库实现，同时保持 API 合同稳定 | 一部 repository を差し替えつつ API 契約は安定維持 |
| Real LLM | Swap the provider seam, keep deterministic fallback | 替换 provider 接缝，保留确定性 fallback | provider の接続点を差し替え、決定論的 fallback を維持 |
| JWT/OAuth | Replace the placeholder current user seam | 替换占位 current user 接缝 | プレースホルダの current user 接続点を置き換える |
| MCP | Add integration later as a separate capability | 之后作为独立能力接入 | 別機能として後から統合する |

## Current Runnable Envelope / 当前可运行能力 / 現在の実行可能範囲

### Already Runnable / 已经可以跑 / すでに実行可能

- Task API chain
- Document upload/read/archive/import/chunk/retrieval
- Internal RAG without LLM
- Approval submit/review/approve/reject
- Security read model
- Audit log read model

### Skeleton Runnable / 骨架可以跑 / 骨格は実行可能

- PostgreSQL repository wiring
- LLM provider seam
- RBAC and audit seams

### Planned / 未来计划 / 今後の予定

- frontend polish
- real authentication
- JWT/OAuth
- real LLM provider
- pgvector
- internet search
- MCP
- production deployment

## Interview Questions / 面试官可能问的问题 / 面接で聞かれそうな質問

| Question | Suggested answer points |
| --- | --- |
| Why did you choose InMemory first? | English: to keep the project runnable and teachable; 中文：为了先跑通、先学会；日本語：まず動かして学べる状態を優先した |
| Why not real LLM now? | English: to keep behavior deterministic and testable; 中文：先保证确定性和可测性；日本語：決定論とテスト容易性を優先した |
| How do you explain RAG here? | English: deterministic retrieval + answer assembly; 中文：检索加确定性答案组装；日本語：検索と決定論的回答組み立て |
| Why RBAC on approval only? | English: it reduces risk and keeps the boundary explicit; 中文：先把边界做清楚，降低回归风险；日本語：境界を明確にしてリスクを下げる |
| How can PostgreSQL be added later? | English: by swapping repositories behind the same contract; 中文：在同一合同下替换仓库实现；日本語：同じ契約の裏で repository を差し替える |

## Interview Closing / 面试收尾 / 面接の締め

- English: the project is runnable, explainable, and easy to extend.
- 中文（简体）：这个项目现在是可运行、可讲解、可扩展的。
- 日本語：このプロジェクトは、実行可能で説明しやすく、拡張しやすいです。
