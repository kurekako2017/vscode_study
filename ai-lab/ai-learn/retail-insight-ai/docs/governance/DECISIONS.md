# retail-insight-ai Architecture Decisions

本文件保存 Architecture Decision Record（ADR）。不得删除已生效或已废弃的历史决策。

## ADR-001

日期：2026-06-29

决策：采用 AI-LAB Project Governance V2，使用 ROADMAP、Backlog、TASK、CHANGELOG、ARCHITECTURE 和 DECISIONS 管理项目。

原因：统一项目阶段、任务、架构与决策记录，降低跨工具和跨会话恢复成本。

备选方案：继续只使用 README、TASK 和 Backlog；该方案无法稳定保存架构视图和决策依据。

影响：开始开发前需要读取治理文件；完成任务后需要同步任务状态和变更历史；重大架构变更必须新增 ADR。

## ADR-002

日期：2026-07-04

决策：将 `Retail Insight AI` 明确定位为零售分析领域参考实现，并把 `Enterprise Retail Intelligence Platform (ERIP)` 定义为未来企业平台化目标架构。

原因：当前项目已经进入企业化演进阶段，如果不明确区分当前项目名称、当前实现边界和未来平台目标，后续目录设计、Provider / Repository 抽象、Workflow 抽象和文档表述会出现混乱。

备选方案：直接把当前项目称为 ERIP；该方案会错误暗示平台能力已经存在，与当前实现状态不符。

影响：

- Repository 名称保持不变，项目名称保持为 `Retail Insight AI`。
- ERIP 只允许出现在 Target State 或 Planned 语境中。
- 后续文档必须明确区分：
  Current State
  Target State
  Planned
- 平台化演进的治理入口新增 `Epic 0: Enterprise Platform Architecture Evolution`。

## ADR-003

日期：2026-07-04

决策：在 `Epic 0` 阶段先冻结 Enterprise Architecture，而不先修改业务代码或现有目录。

原因：当前项目后续要同时演进文件化输入、PostgreSQL、检索、审批、互联网搜索和平台化分层。如果没有统一冻结设计，后续每个 Phase 都会重复发明边界。

备选方案：边开发边演进架构；该方案短期快，但会导致 Repository、Provider、Workflow 和数据库边界反复变化。

影响：

- 本次冻结文档成为后续各 Phase 的唯一设计依据。
- 目录重构、Repository 抽象、Provider 抽象、Workflow 扩展和数据库实现必须以后续 Phase 方式落地。
- 当前 `backend/`、`frontend/`、`scripts/` 不做任何结构性改动。

## ADR-004

日期：2026-07-04

决策：将 `Epic 12: Retrieval and RAG Platform` 定义为横向平台能力，并明确本项目中的 RAG 不只包括社内文档，还包括结构化业务数据检索和互联网检索。

原因：企业 AI Agent 项目中的检索能力如果只被理解为“文档问答”，会导致业务数据事实、外部来源、引用追踪和幻觉控制缺乏统一设计。

备选方案：把 RAG 只限定为内部文档检索；该方案无法覆盖零售分析场景中 SQL 业务事实、外部市场信息和多来源上下文合并的实际需求。

影响：

- Retrieval Layer 必须独立建模。
- RAG 范围至少覆盖：
  Business Data Retrieval
  Internal Document Retrieval
  Internet Search Retrieval
- 必须定义：
  Retrieval provider interface
  Context merge strategy
  Source citation model
  Reference tracking
  Hallucination risk control
  Retrieval evaluation

## ADR-005

日期：2026-07-04

决策：Phase 1 先把 KPI 和 Research 的硬编码数据迁移到本地文件输入，同时为后续 Approval Workflow 预留报告状态边界，但不在本阶段实现审批功能。

原因：当前最高优先级是消除核心业务路径中的硬编码数据，同时保持 API、Workflow、SSE 和 Frontend 可运行。如果现在直接实现审批流，会把文件输入改造和状态机改造耦合在一起，增加回归成本。

备选方案：继续保留硬编码数据直到 PostgreSQL 接入时再一起改；该方案会延长 Demo 数据和真实输入边界混杂的时间，阻碍后续导入与检索设计。

影响：

- KPI 统一从 `backend/data/business/*.csv` 读取并计算。
- Research 统一从 `backend/data/research/*.json` 读取 `summary / sources`。
- `backend/data/documents/` 提前建立 Markdown 输入目录，为后续文档上传和检索预留边界。
- Report 当前状态为 `generated`，并预留：
  `draft`
  `pending_approval`
  `approved`
  `rejected`
  `revised`
- 当前继续保留 InMemory Repository，不接数据库。

## ADR-006

日期：2026-07-04

决策：在 Phase 1 与 Phase 2 之间增加 `Phase 1.5: Data Contract Freeze + Approval State Machine Design`，先冻结文件输入契约、导入错误模型与审批状态机，再进入 PostgreSQL 实现。

原因：如果不先冻结输入契约和审批状态机，Phase 2 的表结构、Repository 接口和后续审批 API 都会反复变化。

备选方案：直接进入 PostgreSQL 开发；该方案会让数据库 schema 反向驱动文件输入字段和审批状态，风险更高。

影响：

- `docs/architecture/DATA_CONTRACTS.md` 成为文件输入契约的单一来源
- `docs/architecture/APPROVAL_WORKFLOW.md` 成为审批状态机的单一来源
- `docs/database/DATABASE.md` 成为 Phase 2 表结构准备来源
- Phase 2 至少要覆盖：
  `data_imports`
  `import_errors`
  `reports.approval_status`
  `report_versions`
  `approval_requests`
  `approval_events`

## ADR-007

日期：2026-07-04

决策：Phase 2 采用 `REPOSITORY_BACKEND` 双后端策略，默认保持 `inmemory`，在显式配置时启用 PostgreSQL 持久化。

原因：本项目仍需要本地可运行、可学习和低门槛测试路径，不能因为引入 PostgreSQL 而破坏现有 API、Workflow、SSE 和 Frontend 的默认启动方式。同时 Phase 2 又必须为真实事务事实持久化提供最小可行实现。

备选方案：

- 直接把默认 Repository 切换为 PostgreSQL；该方案会让本地学习环境强依赖数据库。
- 完全不引入 PostgreSQL，只继续保留 InMemory；该方案无法为后续 Approval / Import / Report version 提供稳定事实层。

影响：

- `REPOSITORY_BACKEND` 仅支持 `inmemory` 与 `postgres`
- 默认值保持 `inmemory`
- Task / Event / Report Repository 通过同一接口切换
- Approval / Import 在本阶段只落地 schema 与基础模型，不开放 API

## ADR-008

日期：2026-07-04

决策：PostgreSQL 驱动优先选择 `psycopg[binary]`，并采用惰性导入方式，避免 InMemory 模式被数据库依赖阻塞。

原因：`psycopg` v3 是当前 PostgreSQL Python 驱动主线，API 现代、同步模式足以覆盖当前 Repository MVP；`[binary]` 便于本地与容器环境安装。惰性导入可以保证未启用 `postgres` backend 时，本地默认路径仍可工作。

备选方案：

- `psycopg2-binary`；兼容性高，但不是项目当前优先方向。
- 强制所有环境预装数据库驱动；会抬高本地学习门槛。

影响：

- 当前 PostgreSQL 集成测试在未安装 `psycopg` 的环境中会跳过并明确原因
- InMemory 模式不依赖 PostgreSQL 驱动即可运行
- 后续如果切到 async 或连接池方案，可在 Repository 实现层内部演进，不破坏 Service 接口

## ADR-009

日期：2026-07-04

决策：Phase 2 在真实 PostgreSQL 集成测试完成前，统一标记为 `In Progress / Partially Verified`，不得描述为完全完成。

原因：当前环境缺少 Docker CLI，且实际运行 venv 未安装 `psycopg`，导致 PostgreSQL 集成测试被 skip。代码和 schema 已实现，不等于真实数据库联调已完成。

备选方案：

- 将 Phase 2 标记为完成；该方案会夸大验证范围，不符合企业项目审计要求。

影响：

- 所有 Phase 2 文档必须显式记录：
  `Code implemented`
  `InMemory path verified`
  `PostgreSQL schema implemented`
  `PostgreSQL repository tests prepared`
  `PostgreSQL real integration test pending`
- 文档必须附带下一步真实联调命令。

## ADR-010

日期：2026-07-04

决策：在 `Epic 14: Engineering Standards (Final Freeze)` 中冻结 Master Prompt、API Contract、Event Contract、Prompt Standard、Coding Standard、Development Guide 和 AI Agent Design Guide，并要求 handbook 同步镜像同时落地。

原因：当前项目已经同时存在多类 AI 协作入口。如果没有单一 Master Prompt 和统一工程标准，不同 AI 工具会对 Workflow、Prompt、API 版本、SSE 事件和文档治理产生不同解释，导致后续 Phase 的实现和审查标准漂移。

备选方案：

- 继续把规则分散保存在 AGENTS、README、TASK、Architecture 文档中；该方案可读性差，且不能为后续 AI 工具提供唯一冻结入口。
- 等业务代码继续演进后再补标准；该方案会把标准冻结变成事后追认，无法真正起到前置约束作用。

影响：

- `docs/development/MASTER_PROMPT.md` 成为唯一 Master Prompt。
- `docs/contracts/API_CONTRACT.md` 与 `docs/contracts/EVENT_CONTRACT.md` 成为接口与事件冻结入口。
- `docs/development/PROMPT_STANDARD.md` 成为 Prompt 分类与模板冻结入口。
- `docs/development/CODING_STANDARD.md`、`docs/development/DEVELOPMENT_GUIDE.md`、`docs/architecture/AI_AGENT_DESIGN_GUIDE.md` 成为开发和设计冻结入口。
- `docs/ai-agent-retail-handbook-v3/docs/` 必须维护对应镜像。
- 后续若要破坏这些冻结规则，必须同一变更内更新 ADR、Architecture、Task、Backlog、Changelog、handbook 与相关测试。

## ADR-011

日期：2026-07-04

决策：先冻结 Document Domain Model，再进入 Upload API、Internal RAG、审批、版本管理与 PostgreSQL Document Repository 的下一阶段实现。

原因：文档上传、版本管理、切分、检索和审批会共享同一套 Document、DocumentVersion、DocumentMetadata、DocumentSource、DocumentStatus、DocumentType、Language 与 ApprovalStatus 语义。如果不先冻结这些基础模型，后续 Upload API、Chunk Pipeline、RAG 和持久化实现会出现重复定义和状态漂移。

备选方案：直接实现 Upload API 或 PostgreSQL Document Repository，再回头补领域模型；该方案会把领域语义反向写进接口和数据库，后续 RAG 和审批迁移成本更高。

影响：

- `backend/app/models/document.py` 成为文档域的单一模型入口。
- `backend/app/repositories/interfaces/document_repository.py` 成为文档事实存储的唯一接口入口。

## ADR-012

日期：2026-07-04

决策：将 `DELETE /api/v1/documents/{document_id}` 冻结为 archive / soft delete，而不是物理删除，并且默认列表排除 archived，只有显式请求才包含 archived。

原因：文档域在当前阶段需要保留版本历史、上传事实和后续审计基础。物理删除会破坏已冻结的读接口和未来版本管理边界；默认排除 archived 可以避免读列表混入历史归档数据，同时又保留显式查询能力。

备选方案：

- 物理删除；该方案会丢失事实数据，不适合当前文档域边界。
- 列表默认包含 archived；该方案会让常规浏览结果混入历史归档项，增加理解成本。

影响：

- `backend/app/models/document.py` 增加软删除归档能力。
- `backend/app/repositories/implementations/in_memory/document_repository.py` 的 delete 语义改为 archive。
- `GET /api/v1/documents` 默认过滤 archived，但可通过 `include_archived=true` 或 `status=archived` 显式查看。
- `DELETE` 事件语义可以通过 `document.archive.completed` 逐步接入审计和 SSE。
- `backend/app/repositories/implementations/in_memory/document_repository.py` 作为当前默认本地实现。
- `ImportBatch` 复用现有 `DataImport`，`ApprovalStatus` 复用现有报告审批状态语义。
- `docs/architecture/ARCHITECTURE.md`、`ROADMAP.md`、`TASK.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/governance/CHANGELOG.md` 以及 handbook 图册必须同步记录该冻结结果。

## ADR-012

日期：2026-07-04

决策：先冻结 Document Upload API Contract，再进入 Upload API 实现阶段。

原因：上传接口、事件和验证流程一旦开始实现，如果没有先冻结请求体、响应体、错误码、状态码和未来审批关系，后续实现会在前端、后端和数据库之间产生重复契约。

备选方案：边实现边定义上传契约；该方案会使 `Document Domain`、事件流和审批关系反复调整，不利于后续测试和 handbook 同步。

影响：

- `docs/contracts/API_CONTRACT.md` 冻结 `POST /api/v1/documents`、`GET /api/v1/documents`、`GET /api/v1/documents/{document_id}`、`GET /api/v1/documents/{document_id}/versions`、`GET /api/v1/documents/{document_id}/chunks`、`DELETE /api/v1/documents/{document_id}`。
- `docs/contracts/EVENT_CONTRACT.md` 冻结 `document.upload.started`、`document.upload.validated`、`document.upload.completed`、`document.upload.failed`、`document.version.created`、`document.validation.failed`。
- `docs/database/DATABASE.md` 仅预留 Document Upload 持久化边界，不表示已实现 Upload API。
- 当前实现仍只允许 Document Domain Model，不引入 Upload API、RAG、pgvector 或前端变更。

## ADR-013

日期：2026-07-04

决策：在 Upload API 实现前，先冻结 Upload Workflow、Upload Session、Idempotency、Error Catalog 和 Upload Policy，作为最终实现前的最后契约层。

原因：仅冻结 endpoint 和 event 还不足以支持安全实现；上传会话、幂等、错误分类和策略边界必须先冻结，否则实现时会在重试、进度、错误提示和存储约束上反复返工。

备选方案：直接实现 Upload API，再补会话和错误目录；该方案会使前端提示、后端校验和未来审批关系之间出现契约缺口。

影响：

- `docs/contracts/ERROR_CATALOG.md` 成为上传、校验、仓储、审批、检索、数据库、事件和提供器错误的统一目录。
- `docs/contracts/UPLOAD_POLICY.md` 成为上传大小、扩展名、MIME、编码、幂等和删除语义的统一策略入口。
- `docs/contracts/API_CONTRACT.md` 必须包含 Upload Session 与 Idempotency 规则。
- `docs/contracts/EVENT_CONTRACT.md` 必须覆盖 Upload Workflow 事件族。
- 当前实现边界仍然停留在 Document Domain Model + contract freeze，不进入 Upload API 代码实现。

## ADR-014

日期：2026-07-04

决策：`POST /api/v1/documents` 采用同步 MVP 实现，成功时返回完成态 `DocumentUploadSession`，重复 checksum 返回已有结果，`Idempotency-Key` 同 key 不同 checksum 返回冲突。

原因：当前阶段没有异步存储队列或独立 session 后台 worker；同步实现更适合当前的本地可运行与教学目标，同时能把 checksum、幂等和重复检测的边界一次性冻结在 service 层。

备选方案：把 Upload API 做成异步 accepted/completed 两阶段；该方案需要额外的后台 worker、session 持久化与更复杂的前端轮询逻辑，不符合当前 MVP 范围。

影响：

- `backend/app/api/documents.py` 直接调用同步上传 service。
- `backend/app/services/document_upload_service.py` 负责校验、checksum、重复检测、幂等和事件发布。
- `backend/tests/test_document_upload_api.py` 必须覆盖成功、空文件、类型不支持、缺少标题、重复 checksum、幂等重放和幂等冲突。
- `docs/contracts/API_CONTRACT.md` 需要把 Upload Session 明确为完成态响应。

## ADR-015

日期：2026-07-04

决策：`GET /api/v1/documents` 与 `GET /api/v1/documents/{document_id}` 先直接复用现有 `InMemoryDocumentRepository` 做低风险读实现，并在 service 层完成基础过滤和 404 映射。

原因：当前阶段只需要文档域的稳定读取与最小过滤，不需要引入新的搜索层、缓存层或 PostgreSQL 仓储。直接复用现有内存仓储可以在不改变上传行为的前提下完成最小读闭环。

备选方案：先为读取能力设计独立检索层或 PostgreSQL Document Repository；该方案会扩大本阶段改动范围，不符合低风险 MVP 目标。

影响：

- `backend/app/services/document_read_service.py` 负责列表过滤和单文档读取。
- `backend/app/api/documents.py` 增加读接口，但不触碰 Upload 行为。
- `document_not_found` 使用稳定 404 语义。
- 过滤条件只覆盖当前易实现的 status、document_type、language、owner、tag。

## ADR-016

日期：2026-07-04

决策：将 Document Import Pipeline 作为独立的同步 MVP 实现，复用现有 `InMemoryDocumentRepository`，并把导入状态、导入事件与导入读取资源冻结为独立 API。

原因：Import Pipeline 是未来 Chunking、Internal RAG、全文检索、审批和审计的前置边界，但当前阶段不应直接引入 chunk、embedding、pgvector 或 PostgreSQL Import Repository。同步 MVP 可以在不增加外部依赖的前提下，把导入状态、错误和事件先固定下来。

备选方案：

- 直接实现 Chunk / RAG / Approval；该方案会把本阶段改动范围扩大到后续平台能力。
- 直接实现 PostgreSQL Import Repository；该方案会提高实现成本并延迟当前最小闭环。

影响：

- `backend/app/services/document_import_service.py` 成为导入状态机与事件发布入口。
- `backend/app/api/document_imports.py` 暴露 `POST /api/v1/documents/{document_id}/import` 与 `GET /api/v1/document-imports/{import_id}`。
- `docs/contracts/API_CONTRACT.md`、`docs/contracts/EVENT_CONTRACT.md`、`docs/contracts/ERROR_CATALOG.md`、`docs/architecture/ARCHITECTURE.md`、`docs/database/DATABASE.md` 需要同步导入契约。
- 成功导入后，文档状态推进到 `validated`，但不生成 chunk、不进入 RAG、不进入审批。

## ADR-017

日期：2026-07-04

决策：将 Document Chunk Pipeline 作为独立的同步 MVP 实现，采用 deterministic replace 规则，并复用独立的 InMemory chunk repository。

原因：Chunk Pipeline 是 Import 之后通往 RAG、全文检索和上下文组装的前置边界，但当前阶段不应直接把 chunk、embedding 或 search 与 Document 本体强耦合。deterministic replace 可以让重复 chunk 结果稳定，并为后续持久化替换提供清晰合同。

备选方案：

- 把 chunk 结果直接塞进 DocumentRepository；该方案会混淆文档事实和切片事实。
- 只返回一次性结果、不存储 chunk；该方案无法支持后续 GET /chunks、检索或审计。

影响：

- `backend/app/services/document_chunk_service.py` 成为 chunk 状态机与事件发布入口。
- `backend/app/api/document_chunks.py` 暴露 `POST /api/v1/documents/{document_id}/chunks` 与 `GET /api/v1/documents/{document_id}/chunks`。
- `backend/app/repositories/interfaces/document_chunk_repository.py` 为切片事实提供独立存储边界。
- `docs/contracts/API_CONTRACT.md`、`docs/contracts/EVENT_CONTRACT.md`、`docs/contracts/ERROR_CATALOG.md`、`docs/architecture/ARCHITECTURE.md` 需要同步 chunk 契约。
- 仅支持 `markdown` 和 `text` 进入当前 chunk 闭环，重复 chunk 会覆盖旧结果并保持确定性。

## ADR-018

日期：2026-07-04

决策：将 Document Retrieval Contract 冻结为 keyword-only read boundary，并把它作为 chunk pipeline 与 future RAG 之间的独立稳定接口，而不是直接实现 RAG。

原因：内部检索是文档域向 RAG 演进前的关键只读边界。如果不先冻结请求、响应、事件和错误码，后续检索实现会随着 RAG、hybrid search 和 future approval 频繁变动。

备选方案：

- 直接把 retrieval 绑定到 RAG 或 hybrid search；该方案会让当前冻结边界和未来生成式能力耦合。
- 继续等待 RAG 实现后再补 retrieval contract；该方案会延迟检索边界冻结，增加后续重构成本。

影响：

- `docs/contracts/API_CONTRACT.md` 冻结 `POST /api/v1/document-retrieval/search`。
- `docs/contracts/EVENT_CONTRACT.md` 冻结 `document.retrieval.started`、`document.retrieval.completed`、`document.retrieval.failed`。
- `docs/contracts/ERROR_CATALOG.md` 冻结 `invalid_query`、`retrieval_unavailable`、`repository_error` 的检索语义。
- `docs/architecture/ARCHITECTURE.md` 增加 Document Retrieval Flow、Source Trace Flow、Future RAG Integration Flow。
- 当前实现仍停留在 Document Chunk Pipeline MVP，retrieval implementation 继续后置。

## ADR-019

日期：2026-07-04

决策：将 Retrieval API MVP 实现为 deterministic keyword-only search，并且只在现有 in-memory document chunks 上执行过滤与排序，不引入 LLM、embedding、pgvector 或 PostgreSQL 搜索后端。

原因：当前阶段的目标是把已冻结的检索 contract 落地为可运行的最小实现，同时保持后续 full-text search、hybrid search 或 retrieval provider 替换点清晰。如果一开始就接入生成式或向量检索，会破坏当前 contract 的稳定性和可学习性。

备选方案：

- 直接把 retrieval 绑定到 RAG / embedding / hybrid search；该方案会让 MVP 边界和未来生成式能力耦合。
- 继续只冻结 contract、不实现 API；该方案会让检索边界停留在文档层，无法验证请求、响应、事件与错误语义。

影响：

- `backend/app/api/document_retrieval.py` 暴露 `POST /api/v1/document-retrieval/search`。
- `backend/app/services/document_retrieval_service.py` 负责关键词检索、过滤、确定性排序与事件发布。
- `backend/app/schemas/document_retrieval_api.py` 固定检索请求与响应结构。
- `backend/tests/test_document_retrieval_api.py` 覆盖空查询、无结果、归档过滤、include_archived 与排序确定性。
- 未来 full-text search、hybrid search、retrieval provider 或 PostgreSQL 搜索后端都必须保持 contract 兼容。

## ADR-020

日期：2026-07-04

决策：将 `DocumentRetrievalService` 从 raw chunk storage 中解耦出来，改为依赖 `DocumentRetrievalProvider`，并保留当前 `InMemoryKeywordRetrieval` 作为唯一本地实现。

原因：Retrieval API 已经冻结了 HTTP contract，但如果 service 继续直接读取 chunk repository，那么后续切换 PostgreSQL full-text、hybrid search 或其他检索后端时，service 层仍会绑定存储细节。把检索算法下沉到 provider，可以保持 service 只负责 API、事件和错误语义。

备选方案：

- 继续让 service 直接操作 `DocumentChunkRepository`；该方案会让检索实现与 chunk storage 强耦合。
- 直接把 retrieval 收敛成 RAG；该方案会破坏当前 keyword-only contract。

影响：

- `backend/app/services/document_retrieval_service.py` 只保留 API/事件/错误边界。
- `backend/app/repositories/interfaces/document_retrieval_provider.py` 定义检索后端合同。
- `backend/app/repositories/implementations/in_memory/document_retrieval.py` 提供当前 keyword-only 本地实现。
- `backend/app/config/container.py` 在组合根中装配 retrieval provider。
- `docs/architecture/ARCHITECTURE.md` 需要同步更新 retrieval layer boundary。

## ADR-021

日期：2026-07-04

决策：将 `POST /api/v1/internal-rag/answer` 冻结为基于现有 Document Retrieval Provider 的上层只读回答 contract，并显式区分 retrieval 与 answer generation。

原因：如果直接把内部 RAG 写成“带答案生成的检索 API”而不先冻结 contract，后续 summary mode、citation 规则、未来 LLM provider、审批集成和错误语义都会跟着实现细节漂移。先冻结 contract 可以把 retrieval provider、citation model 和 answer mode 分层固定下来。

备选方案：

- 继续只保留 document-retrieval/search，不冻结 internal RAG contract；该方案会延迟 grounded answer 边界的冻结。
- 直接把 internal RAG 与真实 LLM / embedding / pgvector 绑定；该方案会把当前 phase 拉进生成式实现，破坏 docs-only freeze 目标。

影响：

- `docs/contracts/API_CONTRACT.md` 新增 `/api/v1/internal-rag/answer`。
- `docs/contracts/EVENT_CONTRACT.md` 新增 `internal_rag.*` 事件族。
- `docs/contracts/ERROR_CATALOG.md` 新增 internal RAG 错误码分组。
- `docs/development/PROMPT_STANDARD.md` 新增 Internal RAG prompt family。
- `docs/architecture/ARCHITECTURE.md` 增加 Internal RAG Flow、Retrieval to Citation Flow、Future LLM Provider Flow、Future Approval Integration Flow。
- 后续如果要实现真正回答能力，必须以新的 provider / workflow 变体落地，而不能回写当前 retrieval contract。

## ADR-022

日期：2026-07-04

决策：在现有 `DocumentRetrievalProvider` 之上实现 deterministic Internal RAG MVP，并保持 extractive / summary 两种 answer mode 都不调用 LLM。

原因：当前阶段目标是把 internal RAG contract 从 freeze 推到可运行的最小实现，但仍要避免引入真实 LLM、embedding 或 pgvector。使用 existing retrieval provider 作为唯一上下文来源，可以保持 citation 规则、错误语义和 retrieval boundary 不变，同时让 answer assembly 逻辑保持可测试、可重复。

备选方案：

- 直接接入真实 LLM provider；该方案会提前进入生成式阶段，不符合当前 sprint 的 no-LLM 约束。
- 只保留 contract freeze，不实现 MVP；该方案无法验证 citation 规则、insufficient_context 和 archived filter 行为。

影响：

- `backend/app/services/internal_rag_service.py` 作为 grounded answer service。
- `backend/app/api/internal_rag.py` 暴露 `POST /api/v1/internal-rag/answer`。
- `backend/tests/test_internal_rag_api.py` 覆盖 extractive、summary、invalid_question、insufficient_context、citations、archived exclusion。
- `docs/architecture/ARCHITECTURE.md` 需要同步记录 Internal RAG MVP without LLM 的真实实现边界。

## ADR-023

日期：2026-07-04

决策：在 deterministic Internal RAG MVP 之上增加 evaluation service 与 citation quality checker，并用 warning taxonomy 表达低上下文、弱匹配和引用缺失风险。

原因：internal RAG 如果只返回 answer 和 citations，而没有稳定的评估层，就无法区分“有引用但质量一般”和“完全没有上下文”的场景。加入 evaluation service 后，可以在不改变 API response contract 的前提下，把 citation quality、coverage 和 confidence 变成可测试、可解释的内部能力。

备选方案：

- 只在 API response 里追加更多评估字段；该方案会改变对外 contract，不符合 backward compatibility 目标。
- 把 warning 逻辑散落在 service 和 route 中；该方案会让质量判断难以测试和复用。

影响：

- `backend/app/services/internal_rag_evaluation_service.py` 成为内部评估边界。
- `backend/app/models/internal_rag.py` 定义 `InternalRagEvaluationResult` 与 warning taxonomy。
- `backend/tests/test_internal_rag_evaluation.py` 覆盖 citation_score、missing_citation、weak_match、low_context。
- `docs/architecture/ARCHITECTURE.md` 需要记录 RAG Evaluation Flow 与 Citation Quality Flow。

## ADR-024

日期：2026-07-04

决策：冻结未来 `LLMProvider` 与 `RAGAnswerGenerator` seam 作为 Internal RAG 的可替换模型接入点，但当前默认行为继续保持 deterministic extractive fallback。

原因：当前项目需要先把 model integration boundary、prompt contract、provider error model 和 usage accounting placeholders 冻结下来，避免未来接入真实模型时把 retrieval contract、citation contract 和 API response 一起改掉。

备选方案：

- 直接把 LLM 接到 Internal RAG；该方案会把未来模型选择和当前 retrieval boundary 绑定，增加回归风险。
- 继续只写概念、不冻结 seam；该方案会让后续 provider 接入时重新定义 prompt contract 与错误模型。

影响：

- `docs/development/PROMPT_STANDARD.md` 冻结未来 LLM prompt family 的 input / output / fallback contract。
- `docs/architecture/AI_AGENT_DESIGN_GUIDE.md` 明确 `LLMProvider` 与 `RAGAnswerGenerator` 的职责边界。
- `docs/contracts/ERROR_CATALOG.md` 冻结 future LLM provider error model。
- `docs/architecture/ARCHITECTURE.md` 冻结 optional LLM provider flow、fallback flow 与 token/cost/latency tracking placeholders。
- `POST /api/v1/internal-rag/answer` 的 response 结构保持不变，当前仍以 deterministic extractive mode 为默认实现。

## ADR-025

日期：2026-07-04

决策：在已冻结的 LLM provider seam 上落地 StubLLMProvider + RAGAnswerGenerator MVP，并通过 `LLM_PROVIDER=stub` 和 `INTERNAL_RAG_USE_LLM=false` 控制默认仍然走 deterministic fallback。

原因：当前阶段需要验证 provider seam 的实际代码路径、容错逻辑和 usage placeholder 记录，但仍不能接入真实模型或外部 API。Stub provider 可以让测试验证 seam，同时不改变 internal RAG 的 frozen response contract。

备选方案：

- 直接接真实 LLM provider；该方案不符合当前 no-external-API 约束。
- 只保留 contract freeze，不实现 seam；该方案无法验证 fallback、usage placeholder 和 provider path。

影响：

- `backend/app/providers/` 新增 `LLMProvider` 协议和 `StubLLMProvider`。
- `backend/app/services/rag_answer_generator.py` 成为 answer assembly seam。
- `backend/app/config/settings.py` 新增 `llm_provider` / `internal_rag_use_llm` 配置。
- `backend/tests/test_rag_answer_generator.py` 覆盖默认 deterministic、stub provider、timeout fallback、invalid output fallback、usage placeholder。
- `docs/architecture/ARCHITECTURE.md` 需要记录 Stub LLM Provider Flow 与 fallback behavior。

## ADR-026

日期：2026-07-04

决策：先冻结 Approval Workflow contract，再进入 Approval API 实现阶段，并把 report revision、audit 和 future RBAC 关系写入架构与数据库准备文档。

原因：Approval Workflow 会直接影响 report 版本、审计轨迹和后续权限控制。如果不先冻结 API、event、error 和 state machine，后续实现会在 report revision、audit 与 RBAC 之间反复变更。

备选方案：

- 先实现 Approval API 再补 contract；该方案会让状态机、事件和错误码在前后端之间漂移。
- 继续只保留 report `generated`；该方案无法承接企业阶段的审核与发布边界。

影响：

- `docs/contracts/API_CONTRACT.md` 新增 `/api/v1/reports/{task_id}/submit-approval`、`/api/v1/approvals`、`/api/v1/approvals/{approval_id}`、`/api/v1/approvals/{approval_id}/approve`、`/api/v1/approvals/{approval_id}/reject`、`/api/v1/reports/{task_id}/revise`。
- `docs/contracts/EVENT_CONTRACT.md` 新增 `approval.submitted`、`approval.approved`、`approval.rejected`、`approval.revised`、`approval.published`、`approval.failed`。
- `docs/contracts/ERROR_CATALOG.md` 新增 approval workflow error section。
- `docs/architecture/ARCHITECTURE.md` 与 `docs/database/DATABASE.md` 记录 report revision relationship、audit relationship 与 future RBAC relationship。
- `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/governance/CHANGELOG.md` 以及 handbook mirror 需要同步记录。

## ADR-027

日期：2026-07-04

决策：将人类可读项目文档的语言策略冻结为三语标准：English、中文（简体）、日本語。

原因：本项目既要服务英文执行稳定性，又要服务中文教学与日本语项目语境。若文档长期混用单语或多处只写英文，后续治理文档、架构图、错误目录和工作流说明会更容易被误读。

备选方案：

- 继续允许任意单语写法；该方案会降低教学可读性和跨语种一致性。
- 只要求部分文档三语；该方案会让冻结文档与一般文档之间出现解释断层。

影响：

- `docs/development/MASTER_PROMPT.md`、`docs/development/CODING_STANDARD.md`、`docs/development/DEVELOPMENT_GUIDE.md` 冻结文档语言政策。
- `docs/contracts/API_CONTRACT.md`、`docs/contracts/EVENT_CONTRACT.md`、`docs/contracts/ERROR_CATALOG.md`、`docs/architecture/ARCHITECTURE.md`、`TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/governance/CHANGELOG.md` 同步记录该规则。
- English-only 仅允许用于 code identifiers、API paths、class names、environment variables、enum values、error codes、event names。
- 后续新增文档必须先检查三语一致性，再进入评审。

## ADR-028

日期：2026-07-05

决策：Approval Workflow contract 冻结后，先实现 backend-only Approval API MVP，使用 InMemory approval repository、immutable report version snapshot 和 ApprovalService 作为当前实现边界。

原因：审批 contract 已冻结，但仍需要真实验证 report revision、audit event、拒绝原因和 revision snapshot 的关系，且不能把 RBAC、外部 workflow engine 或前端改动提前引入。

备选方案：继续停留在 contract freeze；该方案无法验证审批状态机与版本边界的真实运行路径。

影响：

- `POST /api/v1/reports/{task_id}/submit-approval`、`GET /api/v1/approvals`、`GET /api/v1/approvals/{approval_id}`、`POST /api/v1/approvals/{approval_id}/approve`、`POST /api/v1/approvals/{approval_id}/reject`、`POST /api/v1/reports/{task_id}/revise` 进入 backend MVP。
- 审批历史与 report version 事实层保持可替换，后续可演进到 PostgreSQL repository。
- `docs/architecture/ARCHITECTURE.md`、`TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/governance/CHANGELOG.md` 以及 handbook mirror 需要同步记录该实现结果。
- Approval API / Approval Events / Approval Errors / Approval Architecture sections were checked for trilingual coverage and supplemented where English-only prose remained.

## ADR-029

日期：2026-07-05

决策：先冻结企业安全基础合同，再进入 RBAC / Audit / Authentication 的 backend 实现阶段，并把用户、组织、部门、角色、权限与策略写入架构与数据库准备文档。

原因：企业安全能力会直接影响审批、审计和未来身份接入。如果不先冻结 `users/me`、`security/roles`、`security/permissions`、`audit-logs`、权限模型和审计契约，后续实现会在授权边界和审计事实之间反复变更。

备选方案：

- 先实现 RBAC 再补 contract；该方案会让角色、权限和审计边界在前后端之间漂移。
- 继续只依赖隐式权限判断；该方案无法承接企业审计和审批治理要求。

影响：

- `docs/contracts/API_CONTRACT.md`、`docs/contracts/EVENT_CONTRACT.md`、`docs/contracts/ERROR_CATALOG.md`、`docs/architecture/ARCHITECTURE.md`、`docs/database/DATABASE.md` 冻结企业安全基础合同。
- `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/governance/CHANGELOG.md` 以及 handbook mirror 需要同步记录该冻结。
- 后续 RBAC 实现必须沿用 frozen role / permission names 和 audit log contract，不能重新命名。
- English-only 仍只允许用于 code identifiers、API paths、class names、environment variables、enum values、error codes 和 event names。

## ADR-030

日期：2026-07-05

决策：在企业安全基础合同冻结之后，先实现 backend-only Security Domain MVP 和 append-only InMemory Audit MVP，使用 system placeholder principal、static role/permission catalog 和 AuditService 作为当前实现边界。

原因：只有 contract freeze 还不足以验证 current user snapshot、冻结目录读取和 audit append-only seam 的真实运行路径；但此阶段又不能引入真实认证、JWT、OAuth、RBAC enforcement 或 PostgreSQL audit repository，因此需要一个可运行但仍然本地化的 MVP。

备选方案：

- 继续停留在 contract freeze；该方案无法验证 users/me、security/roles、security/permissions 和 audit-logs 的后端读模型。
- 直接接入真实认证 / RBAC / PostgreSQL 审计；该方案会提前引入当前阶段禁止的外部依赖与安全复杂度。

影响：

- `GET /api/v1/users/me` 现在返回 `user_id="system"` 的 placeholder principal。
- `GET /api/v1/security/roles` 与 `GET /api/v1/security/permissions` 现在返回 frozen static catalog。
- `GET /api/v1/audit-logs` 现在读取 append-only InMemoryAuditRepository。
- `audit.log.created` / `audit.log.failed` 作为结构化日志事件记录 append 成功与失败。
- `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/governance/CHANGELOG.md`、`docs/architecture/ARCHITECTURE.md` 以及 handbook mirror 需要同步记录该实现结果。
- 当前仍不实现真实登录、RBAC enforcement、JWT、OAuth、PostgreSQL audit repository 或 frontend 变更。

## ADR-031

日期：2026-07-05

决策：在 Security Domain + InMemory Audit MVP 之上，先只对 Approval Workflow APIs 实现 backend-only RBAC enforcement，并通过 current user seam、permission catalog 和 audit append-only seam 记录 permission denied 事实。

原因：Approval API 已经有稳定 contract 和 report revision boundary，但企业安全能力需要先验证当前用户、权限判定和 denied audit 事实的真实运行路径。把 RBAC 限定在 approval APIs 上，可以保持 document / retrieval / RAG / task APIs 现状不变，同时为后续真实认证和更细粒度授权留出替换点。

备选方案：

- 立即把 RBAC 扩展到所有 API；该方案会扩大本 sprint 范围，并引入不必要的回归面。
- 继续不做 RBAC enforcement；该方案会让 approval 安全边界停留在 contract-only，无法验证 denied audit path。

影响：

- `backend/app/services/security_service.py` 提供 current user seam 以及 permission check helper。
- `backend/app/api/approvals.py` 只在 approval APIs 上调用 RBAC helper。
- `permission_denied` 通过 append-only audit log 记录 denied facts。
- `backend/tests/test_approval_api.py` 覆盖 allow / deny 路径和 denied audit logging。
- `docs/contracts/API_CONTRACT.md`、`docs/architecture/ARCHITECTURE.md`、`TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/governance/CHANGELOG.md` 以及 handbook mirror 需要同步记录该实现。

## ADR-032

日期：2026-07-05

决策：将本次 Final Wrap-up Sprint 只定义为项目收口与验证，不新增功能，不扩展 frontend、PostgreSQL、真实认证、真实 LLM、pgvector、internet search、MCP 或 production deployment 范围，并把当前已完成能力与未完成能力写入三语摘要。

原因：项目已经进入可运行、可学习、可面试讲解的收口阶段。此时继续扩展功能会模糊已验证边界，也会让学习者难以判断当前版本到底支持什么、还缺什么。

备选方案：

- 继续边收口边新增功能；该方案会破坏当前的验证结论，且不利于明确项目边界。
- 只更新代码不更新文档；该方案会让已完成能力、未完成能力和测试结果无法在治理文档中对齐。

影响：

- `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/governance/CHANGELOG.md`、`docs/architecture/ARCHITECTURE.md` 以及 handbook mirror 需要记录最终收口结果。
- 当前完成能力被固定为：Document Upload / Read / Archive / Import / Chunk / Retrieval、Internal RAG without LLM、LLM Provider Stub Seam、Approval Workflow、RBAC for Approval APIs、Approval Audit Middleware、Security Domain、InMemory Audit Log。
- 当前未完成能力被固定为：frontend UI、PostgreSQL repository full migration、real authentication、JWT/OAuth、real LLM provider、pgvector、internet search、MCP、production deployment。
- English / 中文（简体） / 日本語 三语摘要继续作为人类可读文档的默认表达方式。

<!-- DOC-SYNC:START group=architecture -->
## 文档同步块

- group: `architecture`
- file: `retail-insight-ai/docs/governance/DECISIONS.md`
- self_sha256: `fde8a8d32a6812c38add97db9042a1932dda711f32999bde03e862b86bef35d5`
- peers:
- `retail-insight-ai/docs/architecture/ARCHITECTURE.md` | sha256=99ec6a7ef9caa11ad9233e4d6e8d40c2a55ba621584fde27685bce1a52da50b0 | # retail-insight-ai Architecture / 最后更新：2026-06-29 / 本文件记录项目实际架构。未实现的能力必须明确标注，不得把规划写成现状。 / ## 技术架构图
- `ai-agent-retail-handbook-v3/03_AI核心知识.md` | sha256=b29ec1e0b01d85b5a69735c85dcc9e8cfac763e70e38b844dcca04cce5bb64e5 | # 03_AI核心知识 / ## 第一章 知识服务于项目 / 本书中的知识点只围绕 Retail Insight AI 展开。FastAPI、LangGraph、RAG、Streaming、Docker 都不是孤立知识，而是服务于日本小売業客户的经营分析任务。 / 【TL Review】
- `ai-agent-retail-handbook-v3/08_架构图册.md` | sha256=ab27e2cb38443f53f6aff5c2b5d5a495a1774894d29429f463b926c5993d4611 | # 08_架构图册 / # 目录 / - [1. Overall Architecture](#1-overall-architecture) / - [2. User to API Flow](#2-user-to-api-flow)
- `ai-agent-retail-handbook-v3/09_系统设计书.md` | sha256=506bedbfe7ebcb7f81c127c63a3ace28ee8d3329261015d798bb5b6783032f2e | # 09_系统设计书 / # 目录 / - [1. 项目概要](#1-项目概要) / - [2. 系统目标](#2-系统目标)
- `ai-agent-retail-handbook-v3/12_ADR.md` | sha256=1e6bffd61980a95594dd214ccd7db7261c5f63f13df186a392ead99cc8f47766 | # 12_ADR / # 目录 / - [ADR-001 使用 Task API](#adr-001-使用-task-api) / - [ADR-002 引入 TaskService](#adr-002-引入-taskservice)

说明：
- 这个块由 `scripts/sync_retail_handbook_docs.py` 自动维护。
- 只同步这个块，不覆盖各自正文。
- 任一组内文档正文变化时，整组文档的同步块都会一起刷新。
<!-- DOC-SYNC:END group=architecture -->
