import type { LearningEvent, LearningPage } from "../learning/learningTypes";

interface LearningSidebarProps {
  page: LearningPage;
  latestEvent: LearningEvent | null;
}

interface PageLearningInfo {
  navigation: string;
  component: string;
  step: string;
  purpose: string;
  tree: string[];
  props: string;
  inputs: string[];
  apiOverview: string[];
  backendOverview: string[];
  resultExplanation: string[];
  relationship: string[];
  sources: string[];
  test: string;
  cases: string;
  casePurpose: string;
}

const workflowSteps: Array<{ page: LearningPage; label: string; connection: string }> = [
  { page: "documents", label: "文書管理", connection: "→ RAG検索：Backend 数据层已连接，页面条件手动输入" },
  { page: "rag", label: "RAG検索", connection: "→ 分析依頼：当前手动衔接" },
  { page: "tasks", label: "分析依頼", connection: "→ 承認管理：手动复制 task_id" },
  { page: "approval", label: "承認管理", connection: "→ 最终报告汇总：当前未连接" },
];

const pageInfo: Record<LearningPage, PageLearningInfo> = {
  dashboard: {
    navigation: "学习总览",
    component: "DashboardPage",
    step: "总览 / 4",
    purpose: "查看 ERIP 当前实现、能力边界，以及文書管理到承認管理的业务学习顺序。",
    tree: ["App", "└─ DashboardPage", "   ├─ PageHeader", "   ├─ 企业业务流程区（页面内部区域）", "   └─ 系统概览与能力边界（页面内部区域）"],
    props: "App → DashboardPage → onNavigate、onLearningEvent",
    inputs: ["无业务表单输入", "入口按钮：文書管理 / RAG検索 / 分析依頼 / 承認管理"],
    apiOverview: ["入口按钮 → openBusinessStep() → App changeView()", "不调用 Backend API；仅更新 activeView。"],
    backendOverview: ["没有 Backend 调用。", "Dashboard 只展示当前前端已经确认的本地实现事实。"],
    resultExplanation: ["点击入口后切换页面，不创建文档、任务或审批记录。"],
    relationship: ["业务起点：学习总览", "顺序：文書管理 → RAG検索 → 分析依頼 → 承認管理"],
    sources: ["frontend/src/App.tsx", "frontend/src/pages/DashboardPage.tsx"],
    test: "frontend/src/pages/DashboardPage.test.tsx",
    cases: "ERIP-E2E-001",
    casePurpose: "用一个经营分析案例串联四个业务页面，并明确当前仍需手动衔接 ID。",
  },
  documents: {
    navigation: "文書管理",
    component: "DocumentsPage",
    step: "1 / 4",
    purpose: "上传、查看并处理企业内部资料，为后续检索提供 document_id 与 Chunk。",
    tree: ["App", "└─ DocumentsPage", "   ├─ PageHeader", "   ├─ 文書アップロード Form（页面内部区域）", "   ├─ 文書一覧 / 文書詳細（页面内部区域）", "   └─ BusinessLearningPanel"],
    props: "App → DocumentsPage → onLearningEvent；当前没有业务数据 Props 传递。",
    inputs: ["file", "title", "description", "owner", "language", "tags"],
    apiOverview: ["submitUpload() → uploadDocument() → POST /api/v1/documents → 创建上传会话", "loadDocuments() → listDocuments() → GET /api/v1/documents → 更新列表", "runDocumentAction(\"import\") → importDocument() → POST /api/v1/documents/{document_id}/import", "runDocumentAction(\"chunk\") → chunkDocument() → POST /api/v1/documents/{document_id}/chunks", "runDocumentAction(\"archive\") → archiveDocument() → DELETE /api/v1/documents/{document_id}"],
    backendOverview: ["backend/app/api/documents.py / document_imports.py / document_chunks.py：接收文书请求", "DocumentUploadService / DocumentReadService / DocumentImportService / DocumentChunkService：处理上传、读取、导入和分块", "InMemoryDocumentRepository / InMemoryDocumentChunkRepository：保存文书与 Chunk"],
    resultExplanation: ["上传成功后刷新列表。", "Import 与 Chunk 的结果来自后端真实状态；页面不伪造 Chunk 数量。", "Archive 只改变文书状态。"],
    relationship: ["前一步：无，企业资料入口", "后一步：RAG検索", "传递对象：document_id、Chunk", "连接方式：Backend 数据层已连接，页面不自动传 document_id。"],
    sources: ["frontend/src/pages/DocumentsPage.tsx", "frontend/src/api.ts", "backend/app/api/documents.py", "backend/app/services/document_read_service.py", "backend/app/repositories/implementations/in_memory/document_repository.py", "backend/app/schemas/document_api.py"],
    test: "frontend/src/pages/DocumentsPage.test.tsx",
    cases: "DOC-BIZ-001 ～ DOC-BIZ-005",
    casePurpose: "验证上传、列表、详情、导入、Chunk 与归档均由真实 API 结果驱动。",
  },
  rag: {
    navigation: "RAG検索",
    component: "RagPage",
    step: "2 / 4",
    purpose: "用当前 Keyword Retrieval 检索内部 Chunk，并生成带 Citation 的固定逻辑 RAG 回答。",
    tree: ["App", "└─ RagPage", "   ├─ PageHeader", "   ├─ 文書検索 Form（页面内部区域）", "   ├─ Internal RAG 回答 Form（页面内部区域）", "   ├─ 检索结果 / Citation 区（页面内部区域）", "   └─ BusinessLearningPanel"],
    props: "App → RagPage → onLearningEvent；当前没有业务数据 Props 传递。",
    inputs: ["query", "question", "limit", "language", "tags", "answer_mode", "require_citations"],
    apiOverview: ["submitRetrieval() → searchDocumentRetrieval() → POST /api/v1/document-retrieval/search → 更新 retrievalResult", "submitInternalRag() → answerInternalRag() → POST /api/v1/internal-rag/answer → 更新 ragResult", "clearRetrievalResult() / clearRagResult() → 不发送 API，仅清除 React state"],
    backendOverview: ["backend/app/api/document_retrieval.py search_documents()：接收检索请求", "DocumentRetrievalService.search() → InMemoryKeywordRetrieval.search()：按关键词检索 Chunk", "backend/app/api/internal_rag.py answer_internal_rag() → InternalRagService.answer()：用检索证据生成固定逻辑回答", "Schemas：document_retrieval_api.py、internal_rag_api.py"],
    resultExplanation: ["results / score / citation 是后端返回的检索依据。", "insufficient_context（422）表示证据不足，不是页面故障。", "当前未启用真实 LLM、Embedding 或 pgvector。"],
    relationship: ["前一步：文書管理", "后一步：分析依頼", "传递对象：citation、检索结论", "连接方式：当前手动衔接。"],
    sources: ["frontend/src/pages/RagPage.tsx", "frontend/src/api.ts", "backend/app/api/document_retrieval.py", "backend/app/api/internal_rag.py", "backend/app/services/document_retrieval_service.py", "backend/app/services/internal_rag_service.py", "backend/app/schemas/document_retrieval_api.py", "backend/app/schemas/internal_rag_api.py"],
    test: "frontend/src/pages/RagPage.test.tsx",
    cases: "RAG-BIZ-001 ～ RAG-BIZ-005",
    casePurpose: "验证检索、Citation、固定逻辑回答、空结果与证据不足的真实边界。",
  },
  tasks: {
    navigation: "分析依頼",
    component: "TasksPage",
    step: "3 / 4",
    purpose: "创建经营分析任务，观察 SSE 执行状态，并在完成后读取最终 report。",
    tree: ["App", "└─ TasksPage", "   ├─ PageHeader", "   ├─ 分析依頼 Form（页面内部区域）", "   ├─ 実行状態 Panel（页面内部区域）", "   ├─ SSE Event View（页面内部区域）", "   ├─ Report View（页面内部区域）", "   └─ BusinessLearningPanel"],
    props: "App → TasksPage → onLearningEvent；当前没有业务数据 Props 传递。",
    inputs: ["経営課題（question state）", "分析モード（mode state）"],
    apiOverview: ["初始：IDLE，尚未提交任务。", "submit() → createTask() → POST /api/tasks → 202 Accepted → taskId / status 更新 → subscribeToTask(task_id)", "subscribeToTask() → GET /api/tasks/{task_id}/events → SSE → events / status 更新", "done → loadReport() → getReport() → GET /api/tasks/{task_id}/report → 200 → report 更新"],
    backendOverview: ["backend/app/api/tasks.py create_task()：接收 HTTP 请求", "backend/app/services/task_service.py TaskService.create_task()：创建 queued Task 数据", "backend/app/repositories/implementations/in_memory/task_repository.py InMemoryTaskRepository.create()：保存 Task", "backend/app/api/tasks.py BackgroundTasks.add_task()：注册响应后的后台执行", "backend/app/services/task_service.py TaskService.run_task()：执行任务", "backend/app/workflow/graph.py AnalysisWorkflow.stream()：执行 LangGraph", "Workflow nodes：route → kpi → research → report", "backend/app/repositories/implementations/in_memory/report_repository.py InMemoryReportRepository.save()：保存报告", "backend/app/repositories/implementations/in_memory/event_repository.py InMemoryEventRepository：记录事件；SSE 将事件推送到页面"],
    resultExplanation: ["IDLE：还没有提交任务。", "queued：Backend 已接受任务；202 不代表 report 已完成。", "running：BackgroundTasks 中的 Workflow 正在执行。", "done：Workflow 已完成，页面随后读取 report。", "409：任务存在，但 report 尚未生成。", "404：task_id 不存在。"],
    relationship: ["前一步：RAG検索", "后一步：承認管理", "传递对象：task_id、report", "连接方式：当前手动复制 task_id。"],
    sources: ["frontend/src/pages/TasksPage.tsx", "frontend/src/api.ts", "backend/app/api/tasks.py", "backend/app/services/task_service.py", "backend/app/repositories/implementations/in_memory/task_repository.py", "backend/app/repositories/implementations/in_memory/report_repository.py", "backend/app/repositories/implementations/in_memory/event_repository.py", "backend/app/workflow/graph.py", "backend/app/schemas/task_api.py", "backend/app/schemas/report_api.py"],
    test: "frontend/src/pages/TasksPage.test.tsx",
    cases: "TASK-BIZ-001 ～ TASK-BIZ-005",
    casePurpose: "验证 202 受理、SSE queued/running/node/done、报告读取和未就绪／不存在错误。",
  },
  approval: {
    navigation: "承認管理",
    component: "ApprovalPage",
    step: "4 / 4",
    purpose: "基于已完成 report 的 task_id 创建审批，并执行承認、却下或修正依頼。",
    tree: ["App", "└─ ApprovalPage", "   ├─ PageHeader", "   ├─ 承認待ち一覧（页面内部区域）", "   ├─ 承認依頼 Form（页面内部区域）", "   ├─ 承認詳細 / 操作区（页面内部区域）", "   └─ BusinessLearningPanel"],
    props: "App → ApprovalPage → onLearningEvent；当前没有业务数据 Props 传递。",
    inputs: ["task_id", "approval_id", "decision comment", "revision instruction"],
    apiOverview: ["loadApprovals() → listApprovals() → GET /api/v1/approvals", "submitApproval() → POST /api/v1/reports/{task_id}/submit-approval", "handleApprove() → approveApproval() → POST /api/v1/approvals/{approval_id}/approve", "handleReject() → rejectApproval() → POST /api/v1/approvals/{approval_id}/reject", "handleRevise() → requestApprovalRevision() → POST /api/v1/reports/{task_id}/revise"],
    backendOverview: ["backend/app/api/approvals.py：接收审批列表、提交、批准、拒绝和修正请求", "AuditMiddleware.run()：在 approval API 上执行当前权限与审计边界", "ApprovalService：处理审批状态迁移与报告版本", "InMemoryApprovalRepository / InMemoryAuditRepository：保存审批与审计事实", "Schema：backend/app/schemas/approval_api.py"],
    resultExplanation: ["pending 表示等待审批。", "approved / rejected / revision_requested 是后端状态迁移结果。", "403 表示权限边界拒绝；409 表示当前状态不允许该操作。"],
    relationship: ["前一步：分析依頼", "后一步：最终审计报告", "传递对象：approval_id、report_version_id、审批事件", "连接方式：当前无最终汇总页。"],
    sources: ["frontend/src/pages/ApprovalPage.tsx", "frontend/src/api.ts", "backend/app/api/approvals.py", "backend/app/services/approval_service.py", "backend/app/repositories/implementations/in_memory/approval_repository.py", "backend/app/repositories/implementations/in_memory/audit_repository.py", "backend/app/schemas/approval_api.py"],
    test: "frontend/src/pages/ApprovalPage.test.tsx",
    cases: "APR-BIZ-001 ～ APR-BIZ-005",
    casePurpose: "验证提交审批、状态变化、403 权限拒绝与 409 状态冲突。",
  },
};

/**
 * LearningSidebar 固定显示当前页面的真实学习入口、当前事件和已核对的源码链路。
 * App 只传入页面名与最近一次页面 handler 的结果；本组件不发请求、不保存业务数据。
 */
export function LearningSidebar({ page, latestEvent }: LearningSidebarProps) {
  const info = pageInfo[page];

  return (
    <aside className="learning-sidebar" aria-label="固定学习面板">
      <div className="learning-sidebar-scroll">
        <p className="page-eyebrow">ERIP LEARNING PANEL</p>
        <h2>实时学习面板</h2>

        <section>
          <h3>01 当前页面</h3>
          <p>当前导航：<strong>{info.navigation}</strong></p>
          <p>当前组件：<code>{info.component}</code></p>
          <p>当前业务步骤：{info.step}</p>
          <p>页面用途：{info.purpose}</p>
        </section>

        <section>
          <h3>02 当前路由与页面切换</h3>
          <pre>App.tsx → changeView() → setActiveView() → activeView → {info.component}</pre>
          <p>页面导航不调用 Backend API；这里只改变 React state。</p>
        </section>

        <section>
          <h3>03 企业业务流程</h3>
          <ol className="sidebar-flow" aria-label="企业业务流程">
            {workflowSteps.map((item, index) => (
              <li key={item.page} className={item.page === page ? "active" : ""}>
                <strong>{index + 1}. {item.label}</strong>
                <small>{item.connection}</small>
              </li>
            ))}
          </ol>
        </section>

        <section>
          <h3>04 组件树</h3>
          <pre>{info.tree.join("\n")}</pre>
        </section>

        <section>
          <h3>05 Props 传递</h3>
          <p>{info.props}</p>
        </section>

        <section>
          <h3>06 当前页面输入</h3>
          <ul>{info.inputs.map((input) => <li key={input}>{input}</li>)}</ul>
        </section>

        <section>
          <h3>07 最近事件与 State 变化</h3>
          <p><strong>{latestEvent?.eventName ?? "尚未操作。"}</strong></p>
          {latestEvent?.stateChanges.map((change) => <small key={change}>{change}</small>)}
        </section>

        <section>
          <h3>08 API 调用流程</h3>
          {latestEvent?.apiPath ? (
            <p><code>{latestEvent.eventName} → {latestEvent.apiMethod} {latestEvent.apiPath}</code><br />Response Status：{latestEvent.apiStatus ?? "请求中"}<br />真实 Backend API</p>
          ) : (
            <p>最近操作没有 API 请求，或尚未操作。</p>
          )}
          <h4>本页主要 API</h4>
          {info.apiOverview.map((api) => <code key={api}>{api}</code>)}
        </section>

        <section>
          <h3>09 Backend 调用流程</h3>
          <pre>{info.backendOverview.join("\n↓\n")}</pre>
          {latestEvent?.backendFlow && <><h4>最近操作实际链路</h4><pre>{latestEvent.backendFlow.join("\n→ ")}</pre></>}
          {latestEvent?.note && <p className="learning-note">{latestEvent.note}</p>}
        </section>

        <section>
          <h3>10 页面结果解释</h3>
          <ul>{info.resultExplanation.map((item) => <li key={item}>{item}</li>)}</ul>
        </section>

        <section>
          <h3>11 企业业务关系</h3>
          <ul>{info.relationship.map((item) => <li key={item}>{item}</li>)}</ul>
        </section>

        <section>
          <h3>12 对应源码与测试</h3>
          {info.sources.map((source) => <code key={source}>{source}</code>)}
          <code>{info.test}</code>
        </section>

        <section>
          <h3>13 当前业务测试 Case</h3>
          <p><strong>{info.cases}</strong></p>
          <p>{info.casePurpose}</p>
        </section>

        {page === "rag" && (
          <section>
            <h3>RAG 当前边界</h3>
            <p>可用：Keyword Retrieval、Chunk 检索、Citation、Deterministic Internal RAG Answer。</p>
            <p>未启用／未实现：真实 LLM、Embedding、pgvector 向量检索。</p>
          </section>
        )}
      </div>
    </aside>
  );
}
