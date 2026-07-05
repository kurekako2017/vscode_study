# ai-agent-retail-handbook-v3 Architecture Decisions

本文件保存 Architecture Decision Record（ADR）。不得删除已生效或已废弃的历史决策。

## ADR-001

日期：2026-06-29

决策：采用 AI-LAB Project Governance V2，使用 ROADMAP、Backlog、TASK、CHANGELOG、ARCHITECTURE 和 DECISIONS 管理项目。

原因：统一项目阶段、任务、架构与决策记录，降低跨工具和跨会话恢复成本。

备选方案：继续只使用 README、TASK 和 Backlog；该方案无法稳定保存架构视图和决策依据。

影响：开始开发前需要读取治理文件；完成任务后需要同步任务状态和变更历史；重大架构变更必须新增 ADR。

## ADR-002

日期：2026-07-04

决策：retail-insight-ai 进入企业化改造阶段后，每个 Phase 完成都必须同步更新 handbook 文档，且 handbook 同步作为 Phase 完成门禁的一部分。

原因：主项目代码与 handbook 承担“可运行 + 可学习 + 可面试讲解 + 可企业升级”双重职责。若只更新主项目，不更新 handbook，会导致教学文档、测试方法、架构图和决策记录快速失真。

备选方案：仅在大版本或阶段性里程碑后再批量同步 handbook；该方案会产生阶段内信息断层，无法支持持续审计与教学使用。

影响：

- 每个 Phase 都必须检查并同步：
  `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/ARCHITECTURE.md`、`docs/CHANGELOG.md`、`docs/DECISIONS.md`。
- 若变更涉及测试、流程、系统设计、生产路线图，还必须同步检查并更新：
  `08_架构图册.md`、`09_系统设计书.md`、`10_Production_Roadmap.md`。
- 每个测试用例必须包含：
  用例目标、前端操作流程、后端处理流程、数据输入来源、预期输出、验收标准、Mermaid 前端流程图、Mermaid 后端流程图。
- 架构文档必须包含：
  前端流程图、后端流程图、数据流图、数据库 ER 图、LangGraph workflow 图、文档检索流程图、审批 workflow 图、互联网检索流程图。

## ADR-003

日期：2026-07-04

决策：保持项目名称为 `Retail Insight AI`，并将 `Enterprise Retail Intelligence Platform (ERIP)` 仅定义为未来企业平台化目标架构。

原因：当前仓库和当前实现仍是零售分析领域参考实现，如果直接把当前项目描述为 ERIP，会导致目标架构与现状边界失真。

备选方案：将当前项目直接重命名为 ERIP；该方案会错误表达实现状态，并增加仓库、文档和面试讲解的不一致风险。

影响：

- Repository 名称保持不变。
- 当前项目定位为 `Retail Analysis Domain Reference Implementation`。
- 所有后续平台化描述都必须区分：
  Current State
  Target State
  Planned
- handbook 侧新增 `Epic 0: Enterprise Platform Architecture Evolution`、Architecture Principles、Target Architecture 与 Definition of Done。

## ADR-004

日期：2026-07-04

决策：在 `Epic 0` 阶段先冻结 Enterprise Architecture，而不先修改业务代码、目录或基础设施实现。

原因：文件化输入、PostgreSQL、检索、审批、互联网搜索、Workflow 扩展和目录重构都依赖统一边界。如果没有冻结设计，后续每个 Phase 都会改变基线。

备选方案：直接进入代码改造；该方案会在没有统一目录、Repository、Provider、Workflow、ER 图和测试矩阵的情况下推进，风险过高。

影响：

- handbook 必须记录 Architecture Freeze、Directory Freeze、Repository Freeze、Provider Freeze、Workflow Freeze、Database Freeze、Testing Freeze、Documentation Freeze。
- 本次冻结文档成为后续 handbook 和主项目的统一设计基线。

## ADR-005

日期：2026-07-04

决策：将 `Epic 12: Retrieval and RAG Platform` 定义为横向平台能力，并明确本项目中的 RAG 不只包括社内文档，还包括结构化业务数据检索和互联网检索。

原因：日本 SES / 企业 AI Agent 项目中的检索能力，必须能解释业务事实、内部知识、外部市场信息和来源追踪，而不是只讲文档问答。

备选方案：仅把 RAG 解释为内部文档检索；该方案会低估业务检索和互联网检索在零售分析项目中的重要性。

影响：

- 必须单独设计 Retrieval Layer。
- 必须覆盖：
  Business Data Retrieval
  Internal Document Retrieval
  Internet Search Retrieval
  Context Merge
  Citation and Source Trace
  Hallucination Risk Control
  Retrieval Evaluation

## ADR-006

日期：2026-07-04

决策：Phase 1 先完成 KPI / Research 的文件化输入改造，并仅在报告模型中预留 Approval Workflow 状态边界，不在本阶段实现审批功能。

原因：需要先消除硬编码数据，建立稳定输入契约，同时保持现有 API、Workflow、SSE 和 Frontend 可运行。

影响：

- KPI 使用 `backend/data/business/*.csv`
- Research 使用 `backend/data/research/*.json`
- Documents 预留 `backend/data/documents/*.md`
- Report 当前状态为 `generated`
- 后续审批状态为：
  `draft / pending_approval / approved / rejected / revised`

## ADR-007

日期：2026-07-04

决策：增加 Phase 1.5，先冻结 Data Contract、Import Error Model 和 Approval State Machine，再进入 Phase 2 PostgreSQL。

原因：避免数据库 schema 在未冻结输入契约和审批状态前反复变化。

影响：

- Data Contract 成为文件输入基线
- Import Error Model 成为未来导入失败基线
- Approval State Machine 成为未来审批流基线
- PostgreSQL 至少准备：
  `data_imports`
  `import_errors`
  `reports.approval_status`
  `report_versions`
  `approval_requests`
  `approval_events`

## ADR-008

日期：2026-07-04


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
- `docs/API_CONTRACT.md`、`docs/ARCHITECTURE.md`、`TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/CHANGELOG.md` 以及 handbook mirror 需要同步记录该实现。
决策：Phase 2 采用双后端 Repository 策略，默认仍为 `inmemory`，仅在显式配置时启用 PostgreSQL。

原因：handbook 需要忠实反映主项目“本地可运行优先”的边界，不能把 PostgreSQL 说成默认必选依赖。

影响：

- Task / Event / Report 走统一 Repository Interface
- Approval / Import 本阶段仅保留 schema 扩展位
- handbook 在讲解 Phase 2 时必须区分代码已实现与联调已完成

## ADR-009

日期：2026-07-04

决策：Phase 2 在真实 PostgreSQL 集成测试完成前，统一标记为 `In Progress / Partially Verified`，不得描述为完全完成。

原因：当前环境缺少 Docker CLI，且实际运行 venv 未安装 `psycopg`，导致 PostgreSQL 集成测试被 skip。代码和 schema 已实现，不等于真实数据库联调已完成。

影响：

- handbook 必须同步记录 Phase 2 的部分验证状态
- handbook 必须同步记录真实联调命令
- handbook 图册必须采用 English / 中文（简体） / 日本語 三语言维护

## ADR-010

日期：2026-07-04

决策：handbook 必须镜像保存 Master Prompt、API Contract、Event Contract、Prompt Standard、Coding Standard、Development Guide 和 AI Agent Design Guide，并将其视为后续 AI 协作与教学讲解的冻结标准入口。

原因：如果 handbook 只保留概念讲解，而不镜像项目标准文档，后续学习材料、面试讲解和 AI 协作规范会逐步偏离主项目的真实工程边界。

备选方案：仅在 handbook 的架构章节中口头描述标准；该方案缺少可引用的单一来源，也无法支撑后续 Phase 的一致性审查。

影响：

- handbook `docs/` 新增 7 份标准镜像文档。
- 后续 AI 工具和学习者都必须先读这些标准文档，再读具体实现章节。
- 若主项目标准文档发生变更，handbook 镜像必须同一会话内刷新。

## ADR-011

日期：2026-07-04

决策：将 Phase 3.1 Document Domain Model 作为后续 Upload、Version Management、Internal RAG、Approval Workflow、Retrieval 和 PostgreSQL Persistence 的共同领域基线，并同步镜像到 handbook。

原因：文档领域的状态、版本、来源、元数据和校验逻辑必须先冻结，否则后续上传、审批、检索和持久化都会基于不稳定的语义。

备选方案：继续把文档领域拆散到 Upload API、RAG 和 Repository 实现里分别定义；该方案会导致契约重复、测试分散和 handbook 无法形成单一讲解入口。

影响：

- handbook 必须同步记录：
  `Document`
  `DocumentVersion`
  `DocumentChunk`
  `DocumentMetadata`
  `DocumentSource`
  `DocumentStatus`
  `DocumentType`
  `Language`
  `ApprovalStatus`
- `ImportBatch` 复用既有 `DataImport` 语义。
- `DocumentRepository Interface` 与 `InMemoryDocumentRepository` 作为当前唯一实现边界。
- `backend/app/repositories/implementations/in_memory/document_repository.py` 仅保留在正确路径。

## ADR-012

日期：2026-07-04

决策：先冻结 Document Upload API Contract，再进入 Upload API 实现阶段。

原因：上传接口、事件和验证流程一旦开始实现，如果没有先冻结请求体、响应体、错误码、状态码和未来审批关系，后续实现会在前端、后端和数据库之间产生重复契约。

备选方案：边实现边定义上传契约；该方案会使 `Document Domain`、事件流和审批关系反复调整，不利于后续测试和 handbook 同步。

影响：

- `docs/API_CONTRACT.md` 冻结 `POST /api/v1/documents`、`GET /api/v1/documents`、`GET /api/v1/documents/{document_id}`、`GET /api/v1/documents/{document_id}/versions`、`GET /api/v1/documents/{document_id}/chunks`、`DELETE /api/v1/documents/{document_id}`。
- `docs/EVENT_CONTRACT.md` 冻结 `document.upload.started`、`document.upload.validated`、`document.upload.completed`、`document.upload.failed`、`document.version.created`、`document.validation.failed`。
- `docs/DATABASE.md` 仅预留 Document Upload 持久化边界，不表示已实现 Upload API。
- 当前实现仍只允许 Document Domain Model，不引入 Upload API、RAG、pgvector 或前端变更。

## ADR-013

日期：2026-07-04

决策：在 Upload API 实现前，先冻结 Upload Workflow、Upload Session、Idempotency、Error Catalog 和 Upload Policy，作为最终实现前的最后契约层。

原因：仅冻结 endpoint 和 event 还不足以支持安全实现；上传会话、幂等、错误分类和策略边界必须先冻结，否则实现时会在重试、进度、错误提示和存储约束上反复返工。

备选方案：直接实现 Upload API，再补会话和错误目录；该方案会使前端提示、后端校验和未来审批关系之间出现契约缺口。

影响：

- `docs/ERROR_CATALOG.md` 成为上传、校验、仓储、审批、检索、数据库、事件和提供器错误的统一目录。
- `docs/UPLOAD_POLICY.md` 成为上传大小、扩展名、MIME、编码、幂等和删除语义的统一策略入口。
- `docs/API_CONTRACT.md` 必须包含 Upload Session 与 Idempotency 规则。
- `docs/EVENT_CONTRACT.md` 必须覆盖 Upload Workflow 事件族。
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
- `docs/API_CONTRACT.md` 需要把 Upload Session 明确为完成态响应。

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

- 直接实现 Chunk / RAG / Approval：该方案会把本阶段改动范围扩大到后续平台能力。
- 直接实现 PostgreSQL Import Repository：该方案会提高实现成本并延迟当前最小闭环。

影响：

- `backend/app/services/document_import_service.py` 成为导入状态机与事件发布入口。
- `backend/app/api/document_imports.py` 暴露 `POST /api/v1/documents/{document_id}/import` 与 `GET /api/v1/document-imports/{import_id}`。
- `docs/API_CONTRACT.md`、`docs/EVENT_CONTRACT.md`、`docs/ERROR_CATALOG.md`、`docs/ARCHITECTURE.md`、`docs/DATABASE.md` 需要同步导入契约。
- 成功导入后，文档状态推进到 `validated`，但不生成 chunk、不进入 RAG、不进入审批。

## ADR-016

日期：2026-07-04

决策：将 `DELETE /api/v1/documents/{document_id}` 冻结为 archive / soft delete，而不是物理删除，并且默认列表排除 archived，只有显式请求才包含 archived。

原因：文档域需要保留版本历史、上传事实和后续审计基础。物理删除会破坏已冻结的读接口和未来版本管理边界；默认排除 archived 可以避免读列表混入历史归档数据，同时又保留显式查询能力。

备选方案：

- 物理删除：会丢失事实数据，不适合当前文档域边界。
- 列表默认包含 archived：会让常规浏览结果混入历史归档项，增加理解成本。

影响：

- `backend/app/models/document.py` 增加软删除归档能力。
- `backend/app/repositories/implementations/in_memory/document_repository.py` 的 delete 语义改为 archive。
- `GET /api/v1/documents` 默认过滤 archived，但可通过 `include_archived=true` 或 `status=archived` 显式查看。
- `DELETE` 事件语义可以通过 `document.archive.completed` 逐步接入审计和 SSE。

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
- `docs/API_CONTRACT.md`、`docs/EVENT_CONTRACT.md`、`docs/ERROR_CATALOG.md`、`docs/ARCHITECTURE.md` 需要同步 chunk 契约。
- 仅支持 `markdown` 和 `text` 进入当前 chunk 闭环，重复 chunk 会覆盖旧结果并保持确定性。

## ADR-018

日期：2026-07-04

决策：将 Document Retrieval Contract 冻结为 keyword-only read boundary，并把它作为 chunk pipeline 与 future RAG 之间的独立稳定接口，而不是直接实现 RAG。

原因：内部检索是文档域向 RAG 演进前的关键只读边界。如果不先冻结请求、响应、事件和错误码，后续检索实现会随着 RAG、hybrid search 和 future approval 频繁变动。

备选方案：

- 直接把 retrieval 绑定到 RAG 或 hybrid search；该方案会让当前冻结边界和未来生成式能力耦合。
- 继续等待 RAG 实现后再补 retrieval contract；该方案会延迟检索边界冻结，增加后续重构成本。

影响：

- `docs/API_CONTRACT.md` 冻结 `POST /api/v1/document-retrieval/search`。
- `docs/EVENT_CONTRACT.md` 冻结 `document.retrieval.started`、`document.retrieval.completed`、`document.retrieval.failed`。
- `docs/ERROR_CATALOG.md` 冻结 `invalid_query`、`retrieval_unavailable`、`repository_error` 的检索语义。
- `docs/ARCHITECTURE.md` 增加 Document Retrieval Flow、Source Trace Flow、Future RAG Integration Flow。
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

影响：

- `backend/app/services/document_retrieval_service.py` 只保留 API/事件/错误边界。
- `backend/app/repositories/interfaces/document_retrieval_provider.py` 定义检索后端合同。
- `backend/app/repositories/implementations/in_memory/document_retrieval.py` 提供当前 keyword-only 本地实现。
- `backend/app/config/container.py` 在组合根中装配 retrieval provider。
- `docs/ARCHITECTURE.md` 需要同步更新 retrieval layer boundary。

## ADR-021

日期：2026-07-04

决策：将 `POST /api/v1/internal-rag/answer` 冻结为基于现有 Document Retrieval Provider 的上层只读回答 contract，并显式区分 retrieval 与 answer generation。

原因：如果直接把内部 RAG 写成“带答案生成的检索 API”而不先冻结 contract，后续 summary mode、citation 规则、未来 LLM provider、审批集成和错误语义都会跟着实现细节漂移。先冻结 contract 可以把 retrieval provider、citation model 和 answer mode 分层固定下来。

影响：

- `docs/API_CONTRACT.md` 新增 `/api/v1/internal-rag/answer`。
- `docs/EVENT_CONTRACT.md` 新增 `internal_rag.*` 事件族。
- `docs/ERROR_CATALOG.md` 新增 internal RAG 错误码分组。
- `docs/PROMPT_STANDARD.md` 新增 Internal RAG prompt family。
- `docs/ARCHITECTURE.md` 增加 Internal RAG Flow、Retrieval to Citation Flow、Future LLM Provider Flow、Future Approval Integration Flow。
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
- `docs/ARCHITECTURE.md` 需要同步记录 Internal RAG MVP without LLM 的真实实现边界。

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
- `docs/ARCHITECTURE.md` 需要记录 RAG Evaluation Flow 与 Citation Quality Flow。

## ADR-024

日期：2026-07-04

决策：冻结未来 `LLMProvider` 与 `RAGAnswerGenerator` seam 作为 Internal RAG 的可替换模型接入点，但当前默认行为继续保持 deterministic extractive fallback。

原因：当前项目需要先把 model integration boundary、prompt contract、provider error model 和 usage accounting placeholders 冻结下来，避免未来接入真实模型时把 retrieval contract、citation contract 和 API response 一起改掉。

备选方案：

- 直接把 LLM 接到 Internal RAG；该方案会把未来模型选择和当前 retrieval boundary 绑定，增加回归风险。
- 继续只写概念、不冻结 seam；该方案会让后续 provider 接入时重新定义 prompt contract 与错误模型。

影响：

- `docs/PROMPT_STANDARD.md` 冻结未来 LLM prompt family 的 input / output / fallback contract。
- `docs/AI_AGENT_DESIGN_GUIDE.md` 明确 `LLMProvider` 与 `RAGAnswerGenerator` 的职责边界。
- `docs/ERROR_CATALOG.md` 冻结 future LLM provider error model。
- `docs/ARCHITECTURE.md` 冻结 optional LLM provider flow、fallback flow 与 token/cost/latency tracking placeholders。
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
- `docs/ARCHITECTURE.md` 需要记录 Stub LLM Provider Flow 与 fallback behavior。

## ADR-026

日期：2026-07-04

决策：先冻结 Approval Workflow contract，再进入 Approval API 实现阶段，并把 report revision、audit 和 future RBAC 关系写入架构与数据库准备文档。

原因：Approval Workflow 会直接影响 report 版本、审计轨迹和后续权限控制。如果不先冻结 API、event、error 和 state machine，后续实现会在 report revision、audit 与 RBAC 之间反复变更。

备选方案：

- 先实现 Approval API 再补 contract；该方案会让状态机、事件和错误码在前后端之间漂移。
- 继续只保留 report `generated`；该方案无法承接企业阶段的审核与发布边界。

影响：

- `docs/API_CONTRACT.md` 新增 `/api/v1/reports/{task_id}/submit-approval`、`/api/v1/approvals`、`/api/v1/approvals/{approval_id}`、`/api/v1/approvals/{approval_id}/approve`、`/api/v1/approvals/{approval_id}/reject`、`/api/v1/reports/{task_id}/revise`。
- `docs/EVENT_CONTRACT.md` 新增 `approval.submitted`、`approval.approved`、`approval.rejected`、`approval.revised`、`approval.published`、`approval.failed`。
- `docs/ERROR_CATALOG.md` 新增 approval workflow error section。
- `docs/ARCHITECTURE.md` 与 `docs/DATABASE.md` 记录 report revision relationship、audit relationship 与 future RBAC relationship。
- `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/CHANGELOG.md` 以及 handbook mirror 需要同步记录。

## ADR-027

日期：2026-07-04

决策：将人类可读项目文档的语言策略冻结为三语标准：English、中文（简体）、日本語。

原因：本项目既要服务英文执行稳定性，又要服务中文教学与日本语项目语境。若文档长期混用单语或多处只写英文，后续治理文档、架构图、错误目录和工作流说明会更容易被误读。

备选方案：

- 继续允许任意单语写法；该方案会降低教学可读性和跨语种一致性。
- 只要求部分文档三语；该方案会让冻结文档与一般文档之间出现解释断层。

影响：

- `docs/MASTER_PROMPT.md`、`docs/CODING_STANDARD.md`、`docs/DEVELOPMENT_GUIDE.md` 冻结文档语言政策。
- `docs/API_CONTRACT.md`、`docs/EVENT_CONTRACT.md`、`docs/ERROR_CATALOG.md`、`docs/ARCHITECTURE.md`、`TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/CHANGELOG.md` 同步记录该规则。
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
- `docs/ARCHITECTURE.md`、`TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/CHANGELOG.md` 以及 handbook mirror 需要同步记录该实现结果。
- Approval API / Approval Events / Approval Errors / Approval Architecture sections were checked for trilingual coverage and supplemented where English-only prose remained.

## ADR-029

日期：2026-07-05

决策：先冻结企业安全基础合同，再进入 RBAC / Audit / Authentication 的 backend 实现阶段，并把用户、组织、部门、角色、权限与策略写入架构与数据库准备文档。

原因：企业安全能力会直接影响审批、审计和未来身份接入。如果不先冻结 `users/me`、`security/roles`、`security/permissions`、`audit-logs`、权限模型和审计契约，后续实现会在授权边界和审计事实之间反复变更。

备选方案：

- 先实现 RBAC 再补 contract；该方案会让角色、权限和审计边界在前后端之间漂移。
- 继续只依赖隐式权限判断；该方案无法承接企业审计和审批治理要求。

影响：

- `docs/API_CONTRACT.md`、`docs/EVENT_CONTRACT.md`、`docs/ERROR_CATALOG.md`、`docs/ARCHITECTURE.md`、`docs/DATABASE.md` 冻结企业安全基础合同。
- `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/CHANGELOG.md` 以及 handbook mirror 需要同步记录该冻结。
- 后续 RBAC 实现必须沿用 frozen role / permission names 和 audit log contract，不能重新命名。
- English-only 仍只允许用于 code identifiers、API paths、class names、environment variables、enum values、error codes 和 event names。
