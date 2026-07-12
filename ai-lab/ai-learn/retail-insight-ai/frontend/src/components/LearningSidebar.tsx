import type { LearningEvent, LearningPage } from "../learning/learningTypes";

interface LearningSidebarProps {
  page: LearningPage;
  latestEvent: LearningEvent | null;
}

const workflowSteps: Array<{ page: LearningPage; label: string; connection: string }> = [
  { page: "documents", label: "文書管理", connection: "→ RAG検索：Backend 数据层已连接，页面条件手动输入" },
  { page: "rag", label: "RAG検索", connection: "→ 分析依頼：当前手动衔接" },
  { page: "tasks", label: "分析依頼", connection: "→ 承認管理：手动复制 task_id" },
  { page: "approval", label: "承認管理", connection: "→ 最终报告汇总：当前未连接" },
];

const pageInfo: Record<LearningPage, {
  navigation: string;
  component: string;
  step: string;
  tree: string[];
  props: string;
  sources: string[];
  test: string;
  cases: string;
  apiOverview: string[];
}> = {
  dashboard: {
    navigation: "学习总览",
    component: "DashboardPage",
    step: "总览 / 4",
    tree: ["App", "DashboardPage", "PageHeader", "企业业务流程区"],
    props: "App → DashboardPage → onNavigate",
    sources: ["frontend/src/App.tsx", "frontend/src/pages/DashboardPage.tsx"],
    test: "frontend/src/pages/DashboardPage.test.tsx",
    cases: "ERIP-E2E-001",
    apiOverview: ["无 API：onNavigate → App changeView()"],
  },
  documents: {
    navigation: "文書管理",
    component: "DocumentsPage",
    step: "1 / 4",
    tree: ["App", "DocumentsPage", "PageHeader", "文書アップロード / 一覧 / 詳細", "BusinessLearningPanel"],
    props: "当前页面没有业务 Props 传递。",
    sources: ["frontend/src/pages/DocumentsPage.tsx", "frontend/src/api.ts", "backend/app/api/documents.py", "backend/app/services/document_read_service.py"],
    test: "frontend/src/pages/DocumentsPage.test.tsx",
    cases: "DOC-BIZ-001 ～ DOC-BIZ-005",
    apiOverview: ["POST /api/v1/documents", "GET /api/v1/documents", "POST /api/v1/documents/{document_id}/import", "POST /api/v1/documents/{document_id}/chunks", "DELETE /api/v1/documents/{document_id}"],
  },
  rag: {
    navigation: "RAG検索",
    component: "RagPage",
    step: "2 / 4",
    tree: ["App", "RagPage", "PageHeader", "文書検索 Form", "Internal RAG 回答 Form", "结果区", "BusinessLearningPanel"],
    props: "当前页面没有业务 Props 传递。",
    sources: ["frontend/src/pages/RagPage.tsx", "frontend/src/api.ts", "backend/app/api/document_retrieval.py", "backend/app/api/internal_rag.py", "backend/app/services/internal_rag_service.py"],
    test: "frontend/src/pages/RagPage.test.tsx",
    cases: "RAG-BIZ-001 ～ RAG-BIZ-005",
    apiOverview: ["POST /api/v1/document-retrieval/search", "POST /api/v1/internal-rag/answer", "清除：不发送 API"],
  },
  tasks: {
    navigation: "分析依頼",
    component: "TasksPage",
    step: "3 / 4",
    tree: ["App", "TasksPage", "PageHeader", "分析依頼 Form", "SSE 执行状态", "分析レポート", "BusinessLearningPanel"],
    props: "当前页面没有业务 Props 传递。",
    sources: ["frontend/src/pages/TasksPage.tsx", "frontend/src/api.ts", "backend/app/api/tasks.py", "backend/app/services/task_service.py", "backend/app/workflow/graph.py"],
    test: "frontend/src/pages/TasksPage.test.tsx",
    cases: "TASK-BIZ-001 ～ TASK-BIZ-005",
    apiOverview: ["POST /api/tasks（202 Accepted）", "GET /api/tasks/{task_id}/events（SSE）", "GET /api/tasks/{task_id}/report（done 后）"],
  },
  approval: {
    navigation: "承認管理",
    component: "ApprovalPage",
    step: "4 / 4",
    tree: ["App", "ApprovalPage", "PageHeader", "承認待ち一覧", "承認依頼 Form", "承認詳細", "BusinessLearningPanel"],
    props: "当前页面没有业务 Props 传递。",
    sources: ["frontend/src/pages/ApprovalPage.tsx", "frontend/src/api.ts", "backend/app/api/approvals.py", "backend/app/services/approval_service.py"],
    test: "frontend/src/pages/ApprovalPage.test.tsx",
    cases: "APR-BIZ-001 ～ APR-BIZ-005",
    apiOverview: ["POST /api/v1/reports/{task_id}/submit-approval", "POST /api/v1/approvals/{approval_id}/approve", "POST /api/v1/approvals/{approval_id}/reject", "POST /api/v1/reports/{task_id}/revise"],
  },
};

/**
 * LearningSidebar 固定显示当前页面的真实学习入口与最近操作。
 *
 * 它由 App 提供当前页面和最近事件；页面只上报已有 handler 的结果。
 * 组件不拦截 fetch、不保存业务数据，因此不会影响原有 API、表单或状态机。
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
        </section>

        <section>
          <h3>02 企业业务流程</h3>
          <ol className="sidebar-flow">
            {workflowSteps.map((item, index) => (
              <li key={item.page} className={item.page === page ? "active" : ""}>
                <strong>{index + 1}. {item.label}</strong>
                <small>{item.connection}</small>
              </li>
            ))}
          </ol>
        </section>

        <section>
          <h3>03 组件树</h3>
          <pre>{info.tree.join("\n└─ ")}</pre>
        </section>

        <section>
          <h3>04 Props 传递</h3>
          <p>{info.props}</p>
        </section>

        <section>
          <h3>05 最近事件</h3>
          <p><strong>{latestEvent?.eventName ?? "尚未操作"}</strong></p>
          {latestEvent?.stateChanges.map((change) => <small key={change}>{change}</small>)}
        </section>

        <section>
          <h3>06 API 调用记录</h3>
          {latestEvent?.apiPath ? (
            <p><code>{latestEvent.apiMethod} {latestEvent.apiPath}</code><br />状态：{latestEvent.apiStatus ?? "请求中"}<br />真实 Backend API</p>
          ) : (
            <p>没有 API 请求<br />仅修改 React state</p>
          )}
        </section>

        <section>
          <h3>本页实际 API</h3>
          {info.apiOverview.map((api) => <code key={api}>{api}</code>)}
        </section>

        <section>
          <h3>07 Backend 调用链</h3>
          {latestEvent?.backendFlow ? <pre>{latestEvent.backendFlow.join("\n→ ")}</pre> : <p>请执行页面操作后查看对应调用链。</p>}
          {latestEvent?.note && <p className="learning-note">{latestEvent.note}</p>}
        </section>

        <section>
          <h3>08 源码与测试</h3>
          {info.sources.map((source) => <code key={source}>{source}</code>)}
          <code>{info.test}</code>
        </section>

        <section>
          <h3>09 当前业务测试 Case</h3>
          <p>{info.cases}</p>
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
