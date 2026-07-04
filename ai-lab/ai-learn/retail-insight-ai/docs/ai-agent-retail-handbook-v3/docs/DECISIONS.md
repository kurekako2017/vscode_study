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
