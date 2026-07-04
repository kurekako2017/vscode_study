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

- `docs/DATA_CONTRACTS.md` 成为文件输入契约的单一来源
- `docs/APPROVAL_WORKFLOW.md` 成为审批状态机的单一来源
- `docs/DATABASE.md` 成为 Phase 2 表结构准备来源
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

- `docs/MASTER_PROMPT.md` 成为唯一 Master Prompt。
- `docs/API_CONTRACT.md` 与 `docs/EVENT_CONTRACT.md` 成为接口与事件冻结入口。
- `docs/PROMPT_STANDARD.md` 成为 Prompt 分类与模板冻结入口。
- `docs/CODING_STANDARD.md`、`docs/DEVELOPMENT_GUIDE.md`、`docs/AI_AGENT_DESIGN_GUIDE.md` 成为开发和设计冻结入口。
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
- `backend/app/repositories/implementations/in_memory/document_repository.py` 作为当前默认本地实现。
- `ImportBatch` 复用现有 `DataImport`，`ApprovalStatus` 复用现有报告审批状态语义。
- `docs/ARCHITECTURE.md`、`ROADMAP.md`、`TASK.md`、`docs/PROJECT_BACKLOG.md`、`docs/CHANGELOG.md` 以及 handbook 图册必须同步记录该冻结结果。

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

<!-- DOC-SYNC:START group=architecture -->
## 文档同步块

- group: `architecture`
- file: `retail-insight-ai/docs/DECISIONS.md`
- self_sha256: `fde8a8d32a6812c38add97db9042a1932dda711f32999bde03e862b86bef35d5`
- peers:
- `retail-insight-ai/docs/ARCHITECTURE.md` | sha256=99ec6a7ef9caa11ad9233e4d6e8d40c2a55ba621584fde27685bce1a52da50b0 | # retail-insight-ai Architecture / 最后更新：2026-06-29 / 本文件记录项目实际架构。未实现的能力必须明确标注，不得把规划写成现状。 / ## 技术架构图
- `ai-agent-retail-handbook-v3/03_AI核心知识.md` | sha256=b29ec1e0b01d85b5a69735c85dcc9e8cfac763e70e38b844dcca04cce5bb64e5 | # 03_AI核心知识 / ## 第一章 知识服务于项目 / 本书中的知识点只围绕 Retail Insight AI 展开。FastAPI、LangGraph、RAG、Streaming、Docker 都不是孤立知识，而是服务于日本小売業客户的经营分析任务。 / 【TL Review】
- `ai-agent-retail-handbook-v3/08_架构图册.md` | sha256=ab27e2cb38443f53f6aff5c2b5d5a495a1774894d29429f463b926c5993d4611 | # 08_架构图册 / # 目录 / - [1. Overall Architecture](#1-overall-architecture) / - [2. User to API Flow](#2-user-to-api-flow)
- `ai-agent-retail-handbook-v3/09_系统设计书.md` | sha256=506bedbfe7ebcb7f81c127c63a3ace28ee8d3329261015d798bb5b6783032f2e | # 09_系统设计书 / # 目录 / - [1. 项目概要](#1-项目概要) / - [2. 系统目标](#2-系统目标)
- `ai-agent-retail-handbook-v3/12_ADR.md` | sha256=1e6bffd61980a95594dd214ccd7db7261c5f63f13df186a392ead99cc8f47766 | # 12_ADR / # 目录 / - [ADR-001 使用 Task API](#adr-001-使用-task-api) / - [ADR-002 引入 TaskService](#adr-002-引入-taskservice)

说明：
- 这个块由 `scripts/sync_retail_handbook_docs.py` 自动维护。
- 只同步这个块，不覆盖各自正文。
- 任一组内文档正文变化时，整组文档的同步块都会一起刷新。
<!-- DOC-SYNC:END group=architecture -->
