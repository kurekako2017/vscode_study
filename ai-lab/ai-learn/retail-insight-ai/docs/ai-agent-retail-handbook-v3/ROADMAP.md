# ai-agent-retail-handbook-v3 Roadmap

最后更新：2026-07-05

## 当前阶段

Sprint 11.3: RBAC Enforcement for Approval APIs

### Future Sprint Checklist

- [x] Human-readable documentation is trilingual: English / 中文（简体） / 日本語

当前状态：

- Approval API RBAC enforcement implemented on approval endpoints only
- Current user seam remains placeholder-based and default system admin passes all checks
- Denied approval access writes `security.permission.denied` audit facts
- Status: Completed / Verified

## Sprint 11.3: RBAC Enforcement for Approval APIs

### Current State

- 当前仍使用 `user_id="system"` 的 placeholder principal 作为 current user seam。
- 当前 RBAC 仅强制在 approval APIs 上，不扩展到 document / retrieval / RAG / task APIs。
- 当前 system admin 占位用户可以通过所有 approval permission checks。
- 当前 permission denied 会先写入 append-only audit log，再返回 `permission_denied`。

### Target State

- 未来可以在不改变 approval API response shape 的前提下替换 current user 来源。

### Result

- POST /api/v1/reports/{task_id}/submit-approval now requires `report.submit_approval`
- GET /api/v1/approvals now requires `approval.review`
- GET /api/v1/approvals/{approval_id} now requires `approval.review`
- POST /api/v1/approvals/{approval_id}/approve now requires `approval.approve`
- POST /api/v1/approvals/{approval_id}/reject now requires `approval.reject`
- POST /api/v1/reports/{task_id}/revise now requires `approval.revise`
- permission denied writes append-only audit facts
- backend tests cover allow / deny paths and denied audit logging
- handbook mirror synchronized

### Planned

- Future RBAC can replace the placeholder current user seam without changing approval API payloads.
- Keep approval RBAC isolated from document, retrieval, RAG, and task APIs until a later sprint.

## Sprint 11.1: Enterprise Security Foundation Contract Freeze

### Current State

- 当前还没有 RBAC、认证 middleware 或 Audit API 的 backend 实现。
- 当前 security model 只作为 docs contract 冻结，不改变现有 API 行为。

### Target State

- 未来可以在不改动 document / retrieval / approval response contract 的前提下接入身份与权限层。

### Result

- user / organization / department / role / permission / policy concepts frozen
- planned security APIs frozen
- RBAC approval-action matrix frozen
- audit log contract and operation log contract frozen
- handbook mirror synchronized

### Planned

- 保持当前 docs-only 边界，等待后续 backend security implementation。
- 未来实现只能补充认证与授权，不允许回写已冻结的权限名称和事件名称。

## Sprint 10.2: Approval API MVP Implementation

### Current State

- Approval workflow is now implemented as a backend MVP on top of the frozen contract.
- Immutable report version snapshots remain the revision boundary.

### Target State

- Future RBAC, audit expansion, and persistence backends can reuse the same approval contract.

### Result

- submit-approval / approvals list-detail / approve / reject / revise are now wired to the service boundary
- InMemory approval repository, immutable report version model, and approval events are implemented
- backend tests cover success and error paths

### Planned

- Keep the approval contract stable while the next sprint focuses on hardening and persistence seams.

## Sprint 10.1: Approval Workflow Contract Freeze

### Current State

- Approval workflow is still contract-only.
- Report revision remains an immutable snapshot boundary.

### Target State

- Future Approval API can be implemented without changing report / retrieval / internal RAG contract.

### Result

- approval domain model, API contract, event contract, error catalog, and state rules frozen
- report revision relationship, audit relationship, and future RBAC relationship documented
- docs and handbook mirror synchronized

### Planned

- Keep approval workflow as the next backend implementation boundary.
- Preserve immutable report version semantics.

## Sprint 9.5: LLM Provider Seam Stub MVP

### Current State

- Internal RAG 仍然默认走 deterministic extractive path。
- `StubLLMProvider` 已接入 `RAGAnswerGenerator`，但只有在 `INTERNAL_RAG_USE_LLM=true` 时才会使用。

### Target State

- 未来真实 LLM provider 可以替换 stub provider，而不改变 API contract 或 retrieval boundary。

### Result

- `StubLLMProvider`、`RAGAnswerGenerator`、`LLM_PROVIDER=stub`、`INTERNAL_RAG_USE_LLM=false` 默认值已落地。
- provider failure / timeout / invalid output 都会回退到 deterministic answer。
- backend tests 与 compileall 已通过。

### Planned

- 继续保持 deterministic fallback 为默认路径。
- 未来若接入真实 provider，只允许替换 provider 实现，不允许改动 internal RAG response contract。

## Sprint 9.4: LLM Provider Seam Contract Freeze

### Current State

- Internal RAG 仍然是 deterministic answer assembly，没有真实 LLM provider。
- 当前只冻结未来 provider seam、prompt contract 和 fallback behavior。

### Target State

- 未来 summary / generative answer path 可以通过 `LLMProvider` 接入，但必须保持现有 response contract 不变。

### Result

- `LLMProvider`、`RAGAnswerGenerator`、provider error model、fallback behavior、token/cost/latency placeholder 已在文档层冻结。
- handbook 行为、backend、frontend、scripts 均未修改。

### Planned

- 继续保持 no-LLM path 为默认路径。
- 未来若接入模型，只允许在 answer generation seam 做替换。

## Sprint 9.3: Internal RAG Evaluation + Citation Quality MVP

### Current State

- Internal RAG 已实现 deterministic answer assembly，并新增内部 evaluation / citation quality checking。
- warnings taxonomy 已包含 `low_context`、`missing_citation`、`weak_match`。

### Target State

- 未来如果引入 LLM provider，仍要沿用当前 evaluation contract 与 citation quality checker。

### Result

- `coverage_score`、`citation_score`、`confidence` 和 warnings 已由内部 evaluation service 计算。
- backend tests 与 compileall 已通过。

### Planned

- 继续保持 `POST /api/v1/internal-rag/answer` 对外 response backward compatible。
- 继续保持 retrieval API contract / scoring / response shape 不变。

## Project Positioning

### Current State

当前项目名称：

`Retail Insight AI`

当前定位：

`Retail Analysis Domain Reference Implementation`

### Target State

未来平台目标：

`Enterprise Retail Intelligence Platform (ERIP)`

### Planned

handbook 后续所有路线图描述都必须显式区分 Current State、Target State 和 Planned。

## Architecture Principles

- Platform First
- Domain Driven
- Provider Pattern
- Repository Pattern
- Workflow Driven
- Configuration First
- Test First
- Documentation First
- Backward Compatibility

## Epic 0: Enterprise Platform Architecture Evolution

- [x] Approval Workflow Contract Freeze
- [ ] Architecture Freeze
- [ ] Directory Refactor
- [ ] Repository Abstraction
- [ ] Workflow Abstraction
- [ ] Provider Abstraction
- [ ] Documentation Standard
- [ ] Testing Standard

## Epic 12: Retrieval and RAG Platform

### Current State

当前 handbook 还未把 Retrieval and RAG Platform 作为独立横向平台能力展开。

### Target State

未来 Epic 12 覆盖结构化业务检索、社内文档检索、互联网检索、上下文合并、引用与风险控制。

### Planned

当前将 Epic 12 作为横向平台能力标记，不表示已经实现完整 RAG 平台。

## Sprint 8.1: Document Retrieval Contract Freeze

### Current State

- 当前实现仍以 Document Chunk Pipeline MVP 为最新后端边界。
- Document Retrieval 仅完成契约冻结，尚未进入 backend 实现。

### Target State

- Retrieval 成为 Chunk 与 future RAG 之间的稳定只读边界。
- 未来实现必须保持 keyword-only contract compatibility。

### Result

- 已冻结 `POST /api/v1/document-retrieval/search`。
- 已冻结 retrieval events 与 retrieval errors。
- 已更新 `TASK.md`、`docs/PROJECT_BACKLOG.md`、`docs/CHANGELOG.md`、`docs/DECISIONS.md`、`docs/ARCHITECTURE.md` 以及 handbook mirror。

### Planned

- 只做契约冻结，不实现 Retrieval API。
- 不引入 RAG / embedding / pgvector / hybrid search。

## Sprint 8.2: Document Retrieval API MVP Implementation

### Current State

- Document Retrieval API 已实现，并严格遵守 Sprint 8.1 冻结 contract。

### Target State

- Retrieval 仍保持 keyword-only 只读边界，后续可替换搜索后端但不破坏 contract。

### Result

- `POST /api/v1/document-retrieval/search` 已实现。
- 基于现有 in-memory document chunks 完成 keyword search。
- 已补充 retrieval tests 与 backend full suite verification。

### Planned

- 未来可在 contract 不变前提下引入 PostgreSQL full-text / hybrid search。
- 继续保持 Retrieval 不承担 LLM answer generation。

## Sprint 9.2: Internal RAG MVP without LLM

### Current State

- Internal RAG 已在 existing DocumentRetrievalProvider 之上完成 deterministic answer assembly。
- extractive / summary 两种 answer mode 都不调用 LLM。

### Target State

- 未来 summary mode 可以接入可插拔 LLM provider，但 citation contract 不变。

### Result

- `POST /api/v1/internal-rag/answer` 已实现。
- backend tests 与 compileall 已通过。

### Planned

- 继续保持 `POST /api/v1/internal-rag/answer` 与 retrieval API 分离。
- 未来若接 LLM provider，只能替换 answer assembly 层。

## Phase 1 Sync: 文件化输入基础

### Current State

主项目已完成本地 CSV / JSON / Markdown 文件输入的第一轮实现。

### Target State

文件输入成为 PostgreSQL、Approval Workflow、Document Upload 之前的稳定输入边界。

### Planned

- 当前 Report 状态为 `generated`
- 后续扩展：
  `draft / pending_approval / approved / rejected / revised`

## Phase 1.5 Sync: Contract Freeze and Approval Design

### Current State

主项目已完成 Phase 1.5 文档冻结。

### Target State

Data Contract、Import Error Model、Approval State Machine 成为 Phase 2 设计输入。

### Planned

- 当前只实现 `generated`
- 后续扩展：
  `draft / pending_approval / approved / rejected / revised / published / archived`

## Phase 2 Sync: PostgreSQL Persistence MVP

### Current State

主项目已完成 PostgreSQL Repository MVP，并保持 `inmemory` 为默认后端。

### Target State

Task、Event、Report 有可选事务持久化能力，同时 Approval / Import 为后续 Phase 预留稳定表结构。

### Planned

- 当前未完成真实 PostgreSQL 联调验收

## Phase 7 Sync: Document Chunk Pipeline MVP

### Current State

- `POST /api/v1/documents/{document_id}/chunks` 与 `GET /api/v1/documents/{document_id}/chunks` 已实现。
- 当前 chunk pipeline 只接受 `validated` 文档，只支持 `markdown` / `text`，并使用独立的 InMemory chunk repository。
- 当前 chunk 结果采用 deterministic replace 规则，同一文档版本重复 chunk 会覆盖并返回相同结果。

### Target State

- 文档切片成为 future RAG、全文检索、上下文组装与引用追踪的前置边界。
- chunk 结果必须稳定保存 `chunk_index`、`content`、`character_count` 与父文档 metadata snapshot。
- chunk pipeline 不改变 approval 状态，也不承担 search / embedding 职责。

### Result

- 支持 import 完成后的文档切片、chunk 查询与事件记录。

### Planned

- `versions`、`RAG`、`embedding`、`pgvector`、`Approval API`、`PostgreSQL Document Repository` 继续冻结未实现。
- 当前未实现 Approval API、Import API、Document Search、RAG、Internet Search
- 当前环境缺少 Docker CLI
- 当前环境未安装 `psycopg` 到实际运行 venv
- PostgreSQL 集成测试当前被 skip

## 1.9 Phase 3.1 Document Domain Model

### Current State

主项目已补齐 Document Domain Model 和 InMemory Document Repository。

### Target State

Document Domain 作为 Upload、Version Management、Internal RAG、Approval Workflow、Retrieval 与 PostgreSQL Persistence 的共同基础。

### Planned

- 当前只允许 `uploaded` 作为新建文档初始状态
- 当前不实现 Upload API、RAG、pgvector、Internet Search 或 PostgreSQL Document Repository

## 1.10 Sprint 2 Document Upload API Contract Freeze

### Current State

当前实现仍只停留在 Document Domain Model，没有 Upload API 实现。

### Target State

冻结 Upload API、事件契约、验证流程和未来审批关系，作为后续实现的唯一输入契约。

### Result

已冻结 `POST /api/v1/documents`、`GET /api/v1/documents`、`GET /api/v1/documents/{document_id}`、`GET /api/v1/documents/{document_id}/versions`、`GET /api/v1/documents/{document_id}/chunks`、`DELETE /api/v1/documents/{document_id}`。

### Planned

只做契约冻结，不实现 Upload API，不修改 backend 业务代码，不修改 frontend，不安装依赖。

## 1.11 Sprint 2.5 Document Upload Workflow + Error Catalog + Upload Policy Freeze

### Current State

当前仍只停留在 Document Domain Model 与 Upload API contract freeze。

### Target State

冻结 Upload Workflow、Upload Session、Idempotency、Error Catalog、Upload Policy，作为 Upload API 实现前的最后边界。

### Result

已创建 `docs/ERROR_CATALOG.md` 与 `docs/UPLOAD_POLICY.md`，并冻结 Upload Workflow / Upload Session / Idempotency。

### Planned

只做契约冻结，不实现 Upload API，不修改 backend 业务代码，不修改 frontend，不安装依赖。

## 1.12 Sprint 3 Document Upload API MVP

### Current State

主项目已进入 `POST /api/v1/documents` 的同步 MVP 实现阶段。

### Target State

完成文档上传同步闭环：
multipart/form-data -> validation -> checksum -> duplicate / idempotency -> repository save -> event publish -> 201 response。

### Result

已实现 `POST /api/v1/documents`，并补充 backend 单元测试覆盖成功、空文件、类型不支持、缺少标题、重复 checksum、幂等重放与幂等冲突。

### Planned

继续保持 `GET /api/v1/documents`、`GET /api/v1/documents/{document_id}`、`GET /api/v1/documents/{document_id}/versions`、`GET /api/v1/documents/{document_id}/chunks`、`DELETE /api/v1/documents/{document_id}` 冻结但未实现；PostgreSQL Document Repository 仍只设计不实现。

## 1.13 Sprint 4 Document Read API MVP

### Current State

主项目已进入低风险读接口实现阶段。

### Target State

完成 `GET /api/v1/documents` 与 `GET /api/v1/documents/{document_id}` 的后端 MVP。

### Result

已实现列表读取、单文档读取与基础过滤，并补充 backend 单元测试覆盖空列表、上传后列表、上传后读取、缺失文档和过滤条件。

### Planned

`DELETE`、`versions`、`chunks` 继续保持冻结未实现；PostgreSQL Document Repository 仍只设计不实现。

## 1.14 Sprint 5 Document Archive API MVP

### Current State

主项目已进入 `DELETE /api/v1/documents/{document_id}` 的软删除实现阶段。

### Target State

完成文档归档删除的后端 MVP。

### Result

DELETE 语义冻结为 archive / soft delete，archived 文档保持可读，列表默认排除 archived。

### Planned

`versions`、`chunks` 继续保持冻结未实现；PostgreSQL Document Repository 仍只设计不实现。

## 1.15 Sprint 6 Document Import Pipeline MVP

### Current State

主项目已进入 `POST /api/v1/documents/{document_id}/import` 与 `GET /api/v1/document-imports/{import_id}` 的实现阶段。

### Target State

完成文档导入最小闭环，为 future chunking、RAG、全文检索和审批提供前置边界。

### Result

导入成功后，文档状态推进到 `validated`；导入失败时保留错误码与错误信息。

### Planned

`versions`、`chunks`、`RAG`、`embedding`、`pgvector`、`Approval API`、`PostgreSQL Document Repository` 继续保持冻结未实现。

## Definition of Done

任何一个 Phase 只有在以下项目全部满足后，才能标记完成：

- Code
- Unit Test
- Integration Test
- Frontend Test
- Handbook
- Changelog
- Decision Record
- Architecture Update
- Mermaid Diagram Update
- Task Update

## 下一阶段

1. 将 retail-insight-ai 的 Phase 1 到 Phase 8 规划同步映射到 handbook。
2. 为测试文档和架构文档建立固定模板与缺失章节。
3. 将 CHANGELOG 和 DECISIONS 作为每次功能变更的强制同步入口。

## Handbook 同步路线

1. 主项目 Phase 规划更新
2. handbook 任务、Backlog、Roadmap 同步
3. handbook 架构、系统设计、生产路线图同步
4. handbook CHANGELOG 与 DECISIONS 同步
5. 通过同步门禁后才允许关闭主项目 Phase

## 长期规划

- 保持可运行、可验证、可维护。
- 持续偿还高优先级技术债。
- 重要架构变化记录到 `docs/DECISIONS.md`。
- 每个阶段结束后更新本路线图。

<!-- DOC-SYNC:START group=governance -->
## 文档同步块

- group: `governance`
- file: `ai-agent-retail-handbook-v3/ROADMAP.md`
- self_sha256: `8bea54fca33668303cb3ebc6a86e9fb359d814605450746eb7575075bc4600cf`
- peers:
- `retail-insight-ai/ROADMAP.md` | sha256=5bf39c8dbde1e5279088478951af2f3c02a4506bcbf3682403b3e45a02846cae | # retail-insight-ai Roadmap / 最后更新：2026-06-29 / ## 当前阶段 / 待根据项目现状确认。
- `retail-insight-ai/TASK.md` | sha256=83a6ef1d9395a1c0026514c5d8fab074fb8428781ab712ad25764c1c82decc05 | # retail-insight-ai 当前任务 / 最后更新：2026-07-02 / ## 当前阶段 / Phase 2: Internal Knowledge Approval Agent
- `retail-insight-ai/docs/PROJECT_BACKLOG.md` | sha256=b1dd8a6cee6a7fc07965026b8aefe8c9c8f08669871abd5ce2b8eb3dc1d5d477 | # retail-insight-ai Project Backlog / 最后更新：2026-07-02 / ## 项目目标 / 构建企业级 Retail Insight AI 平台，包含：
- `retail-insight-ai/docs/CHANGELOG.md` | sha256=cf9c2939e3369aa13c65a636fb64c44d56b672866b23771cf1dda5f1dbe755b3 | # retail-insight-ai CHANGELOG / ## 2026-07-02 / - 建立 retail-insight-ai 与 ai-agent-retail-handbook-v3 的跨项目文档同步机制。 / - 新增 `../scripts/sync_retail_handbook_docs.py` 与 `../doc-sync.manifest.json`。
- `ai-agent-retail-handbook-v3/TASK.md` | sha256=8375c8be41775af3f492dbc66e69653096db6bcdc4838d411eacf72cd81d5c82 | # 当前任务 / 最后更新：2026-07-02 / ## 当前阶段 / 待确认
- `ai-agent-retail-handbook-v3/docs/PROJECT_BACKLOG.md` | sha256=4b25c1fa793fa7ce50f3cc87341c8136603a8fc0eeae44e3b57dfcfd17f4dfc7 | # 项目总待办清单 / 最后更新：2026-07-02 / ## 项目目标 / 待确认
- `ai-agent-retail-handbook-v3/docs/CHANGELOG.md` | sha256=db921303a94dca1268fc38339f4c13606461269c65ca79c1de024cc1d36601c3 | # CHANGELOG / ## 2026-07-02 / - 建立 ai-agent-retail-handbook-v3 与 retail-insight-ai 的跨项目文档同步机制。 / - 新增 `../scripts/sync_retail_handbook_docs.py` 与 `../doc-sync.manifest.json`。
- `ai-agent-retail-handbook-v3/10_Production_Roadmap.md` | sha256=d904e6883e84c4bb5adda4d7adab4499e1e0f6f5e52bf97f46ecd7150271e64e | # 10_Production_Roadmap / # 目录 / - [1. Roadmap 原则](#1-roadmap-原则) / - [2. Level 1 Demo](#2-level-1-demo)

说明：
- 这个块由 `scripts/sync_retail_handbook_docs.py` 自动维护。
- 只同步这个块，不覆盖各自正文。
- 任一组内文档正文变化时，整组文档的同步块都会一起刷新。
<!-- DOC-SYNC:END group=governance -->
