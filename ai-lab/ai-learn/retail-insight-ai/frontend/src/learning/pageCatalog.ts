/** 页面静态学习目录：源码、测试、Hook 与教学生命周期。 */

import type { LearningPage, PageCatalogEntry } from "./learningTypes";

export const pageCatalog: Record<LearningPage, PageCatalogEntry> = {
  dashboard: {
    page: "dashboard",
    route: "/dashboard",
    navigation: "学习总览",
    component: "DashboardPage",
    step: "总览",
    businessObject: "Scenario01 的关东地区饮料销售下降。此页只提供文書、RAG、分析与承認四个业务入口，不创建业务记录。",
    whyNeeded: "业务人员先确认当前 MVP 的可用能力和边界，再按正确顺序进入页面，避免把本地固定数据误当作生产结论。",
    initialState: "渲染当前能力边界与业务流程卡片；不读取 Backend。",
    hooks: [
      { name: "useState (via parent)", purpose: "App 保存 latestLearningEvent；本页通过回调上报。" },
      { name: "useAuth (context)", purpose: "展示当前用户与权限数量摘要，不接触 Access Token。" },
    ],
    sources: [
      { label: "页面入口", path: "frontend/src/App.tsx", reason: "读取 URL path，并渲染 ProtectedRoute、当前业务页与 LearningSidebar。" },
      { label: "业务总览", path: "frontend/src/pages/DashboardPage.tsx", reason: "定义 Scenario01 的页面顺序、能力边界和入口事件。" },
    ],
    tests: [
      { label: "导航与侧栏", path: "frontend/src/App.test.tsx", reason: "覆盖默认总览、导航顺序与侧栏展示。" },
      { label: "总览页", path: "frontend/src/pages/DashboardPage.test.tsx", reason: "覆盖能力边界与入口按钮。" },
    ],
    lifecycleTeaching: [
      { name: "Render", detail: "App 根据当前 URL path 渲染 DashboardPage。", technologies: ["React Component", "History API"] },
      { name: "Choose", detail: "openBusinessStep() 记录学习操作，并请求 App 切换目标 URL。", technologies: ["Event Handler", "History API"] },
      { name: "Switch", detail: "App.changeView() 更新 URL，React 卸载总览并渲染目标页面。", technologies: ["History API", "React Re-render"] },
    ],
  },
  documents: {
    page: "documents",
    route: "/documents",
    navigation: "文書管理",
    component: "DocumentsPage",
    step: "1 / 4",
    businessObject: "Scenario01 的销售、库存、促销、顾客和竞品内部资料，以及由资料生成的 document_id 与 Chunk。",
    whyNeeded: "企业分析必须先把可追溯的内部资料登记并分块；RAG 才能返回证据，而不是让前端编造业务事实。",
    initialState: "mount 后通过 useEffect() 加载文书列表；选中文书变化时读取详情和 Chunk。",
    hooks: [
      { name: "useState", purpose: "列表、选中、loading、error、上传状态。" },
      { name: "useEffect", purpose: "mount 拉列表；选中变化刷新详情与 Chunk。" },
    ],
    sources: [
      { label: "页面状态", path: "frontend/src/pages/DocumentsPage.tsx", reason: "管理列表、选择、上传和文书操作的 React state。" },
      { label: "API 适配", path: "frontend/src/api.ts", reason: "封装 document HTTP 请求与响应解析。" },
    ],
    tests: [
      { label: "文书页", path: "frontend/src/pages/DocumentsPage.test.tsx", reason: "列表、详情、Chunk 与权限按钮。" },
    ],
    lifecycleTeaching: [
      { name: "Mount", detail: "useEffect() 调用 loadDocuments(true)，用 showArchived 决定列表范围。", technologies: ["React useEffect", "Fetch API", "REST API"] },
      { name: "Select", detail: "selectedDocumentId 变化后，refreshSelectedDocument() 并行刷新详情与 Chunk。", technologies: ["React useState", "React useEffect", "Fetch API"] },
      { name: "Operate", detail: "上传、Import、Chunk 或 Archive 成功后，刷新列表与当前文书。", technologies: ["Event Handler", "Fetch API", "REST API"] },
      { name: "Render", detail: "React 根据 loading、error、selectedDocument 与 chunkData 重绘页面。", technologies: ["React Re-render"] },
    ],
  },
  rag: {
    page: "rag",
    route: "/rag",
    navigation: "RAG/AI分析",
    component: "RagPage",
    step: "2 / 4",
    businessObject: "Scenario01 已完成 Chunk 的内部资料、检索结果和 Citation；当前为 Keyword Retrieval 与固定逻辑回答；可显式触发 AI分析。",
    whyNeeded: "业务人员需要先检查结论是否有内部证据支撑，才能再做显式 AI分析与审批提交。",
    initialState: "页面初始只显示表单；没有自动检索，也不会自动继承文書管理页的条件。",
    hooks: [
      { name: "useState", purpose: "检索/RAG 表单、结果、AI 分析与董事会报告状态。" },
      { name: "Event handlers", purpose: "submitRetrieval / AI分析 / 生成取締役会報告。" },
    ],
    sources: [
      { label: "页面状态", path: "frontend/src/pages/RagPage.tsx", reason: "管理检索表单、回答表单、结果、错误与清除操作。" },
      { label: "API 适配", path: "frontend/src/api.ts", reason: "封装检索、Internal RAG、AI Analysis HTTP 调用。" },
    ],
    tests: [
      { label: "RAG 页", path: "frontend/src/pages/RagPage.test.tsx", reason: "检索、AI 分析、fallback 显示与权限。" },
    ],
    lifecycleTeaching: [
      { name: "Input", detail: "用户填写检索条件或业务问题，React 保存在本页 state。", technologies: ["Event Handler", "React useState"] },
      { name: "Request", detail: "submitRetrieval() 或 submitInternalRag() 调用 api.ts，并设置 loading。", technologies: ["Event Handler", "Fetch API"] },
      { name: "Resolve", detail: "成功写入 results / citations；证据不足时保留 Backend 的 422 业务结果。", technologies: ["Deterministic RAG", "React Re-render"] },
      { name: "Clear", detail: "清除按钮只重置 React result state，不发送 API 请求。", technologies: ["Event Handler", "React useState"] },
    ],
  },
  tasks: {
    page: "tasks",
    route: "/analysis",
    navigation: "KPI任务分析",
    component: "TasksPage",
    step: "3 / 4",
    businessObject: "Scenario01 的关东饮料销售下降经营课题、task_id、SSE 事件和最终 report（旧 Task API，非 low_cost AI 成本入口）。",
    whyNeeded: "企业把可确认的问题转成可追踪任务，以异步执行避免 HTTP 请求一直等待，并把执行过程和报告分开读取。",
    initialState: "初始为 idle；没有 task_id、SSE 事件或 report。",
    hooks: [
      { name: "useState", purpose: "taskId、status、events、report。" },
      { name: "useEffect", purpose: "unmount 时取消 SSE 订阅。" },
    ],
    sources: [
      { label: "页面状态", path: "frontend/src/pages/TasksPage.tsx", reason: "管理 taskId、status、events、report 和 SSE cleanup。" },
      { label: "API / SSE", path: "frontend/src/api.ts", reason: "创建任务、读取报告并建立可携带 Authorization Header 的 SSE fetch stream。" },
    ],
    tests: [
      { label: "任务页", path: "frontend/src/pages/TasksPage.test.tsx", reason: "提交与报告展示。" },
      { label: "App 集成", path: "frontend/src/App.test.tsx", reason: "SSE 与学习侧栏联动。" },
    ],
    lifecycleTeaching: [
      { name: "Submit", detail: "submit() 清空旧状态，POST /api/tasks 后保存 task_id 与 queued 状态。", technologies: ["Event Handler", "React useState", "Fetch API", "REST API", "FastAPI Router", "BackgroundTasks", "LangGraph"] },
      { name: "Stream", detail: "subscribeToTask() 用带 Bearer Header 的 fetch stream 接收 SSE 事件。", technologies: ["SSE / EventSource", "Fetch Stream"] },
      { name: "Complete", detail: "收到 done 后取消订阅，并调用 loadReport() 读取最终 report。", technologies: ["Fetch API", "REST API", "React useState", "React Re-render"] },
      { name: "Unmount", detail: "useEffect cleanup 调用取消订阅，防止旧 SSE 继续写入已离开的页面。", technologies: ["React useEffect", "SSE / EventSource"] },
    ],
  },
  approval: {
    page: "approval",
    route: "/approval",
    navigation: "承認管理",
    component: "ApprovalPage",
    step: "4 / 4",
    businessObject: "Scenario01 已完成 report 的 task_id、approval_id、report_version_id 与审批审计事件。",
    whyNeeded: "经营结论需要经过责任人审批、拒绝或修正，并保留版本和审计事实，才能成为可追溯的企业决策依据。",
    initialState: "mount 后读取审批列表，并 GET /api/v1/reports 加载可提交报告目录；默认选中一条 task_id，无需手抄。",
    hooks: [
      { name: "useState", purpose: "列表、详情、提交表单、报告目录与错误。" },
      { name: "useEffect", purpose: "mount 加载审批列表与报告目录。" },
    ],
    sources: [
      { label: "页面状态", path: "frontend/src/pages/ApprovalPage.tsx", reason: "管理列表、详情、报告下拉提交和三种审批操作。" },
      { label: "API 适配", path: "frontend/src/api.ts", reason: "封装 approval 与 listReportCatalog HTTP 调用。" },
    ],
    tests: [
      { label: "审批页", path: "frontend/src/pages/ApprovalPage.test.tsx", reason: "目录下拉、提交、批准、拒绝与权限。" },
    ],
    lifecycleTeaching: [
      { name: "Mount", detail: "useEffect() 读取 approval 列表与 report catalog，并选择当前可见记录。", technologies: ["React useEffect", "Fetch API", "REST API"] },
      { name: "Submit", detail: "从报告下拉选择 task_id 后由 Backend 创建 report version 与 approval request。", technologies: ["Event Handler", "Fetch API", "REST API", "FastAPI Router", "Service Layer", "Repository Pattern"] },
      { name: "Decide", detail: "承認、却下或修正依頼触发状态迁移，并刷新列表与详情。", technologies: ["Event Handler", "React useState", "FastAPI Router", "Service Layer", "Repository Pattern"] },
      { name: "Audit", detail: "Approval API 经 AuditMiddleware 与权限边界；403、409 是业务结果而非页面故障。", technologies: ["AuditMiddleware", "FastAPI Router", "Service Layer"] },
    ],
  },
  login: {
    page: "login",
    route: "/login",
    navigation: "ログイン",
    component: "LoginPage",
    step: "Auth",
    businessObject: "Access Token 会话建立；Token 只存 sessionStorage，不进入学习 Trace 正文。",
    whyNeeded: "企业 API 需要 JWT 身份；Login 是唯一匿名入口。",
    initialState: "表单空闲；不自动请求业务 API。",
    hooks: [
      { name: "useState", purpose: "username/password/error/loading。" },
      { name: "useAuth", purpose: "login() 写入会话；不在 UI 展示 Token。" },
    ],
    sources: [
      { label: "Login 页", path: "frontend/src/pages/LoginPage.tsx", reason: "登录表单与错误展示。" },
      { label: "AuthContext", path: "frontend/src/auth/AuthContext.tsx", reason: "会话恢复与 logout。" },
    ],
    tests: [
      { label: "认证流", path: "frontend/src/auth/AuthFlow.test.tsx", reason: "Login、401、ProtectedRoute。" },
    ],
    lifecycleTeaching: [
      { name: "Mount", detail: "渲染登录表单，不调用业务 API。", technologies: ["React Component"] },
      { name: "Submit", detail: "login() 调用 POST /api/v1/auth/login，成功后写入 sessionStorage。", technologies: ["Fetch API", "JWT"] },
      { name: "Redirect", detail: "Authenticated 后 navigate 到 /dashboard。", technologies: ["History API"] },
    ],
  },
};

export function catalogForRoute(pathname: string): PageCatalogEntry | null {
  const entry = Object.values(pageCatalog).find((item) => item.route === pathname);
  return entry ?? null;
}
