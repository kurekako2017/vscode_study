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
