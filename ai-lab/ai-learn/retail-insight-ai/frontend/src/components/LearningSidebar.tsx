import type { LearningEvent, LearningPage } from "../learning/learningTypes";

interface LearningSidebarProps {
  page: LearningPage;
  latestEvent: LearningEvent | null;
}

interface SourceLocation {
  label: string;
  path: string;
  reason: string;
}

interface LifecycleStep {
  name: string;
  detail: string;
}

interface PageLearningInfo {
  navigation: string;
  component: string;
  step: string;
  businessObject: string;
  whyNeeded: string;
  initialState: string;
  lifecycle: LifecycleStep[];
  sources: SourceLocation[];
}

const pageInfo: Record<LearningPage, PageLearningInfo> = {
  dashboard: {
    navigation: "学习总览",
    component: "DashboardPage",
    step: "总览",
    businessObject: "Scenario01 的关东地区饮料销售下降。此页只提供文書、RAG、分析与承認四个业务入口，不创建业务记录。",
    whyNeeded: "业务人员先确认当前 MVP 的可用能力和边界，再按正确顺序进入页面，避免把本地固定数据误当作生产结论。",
    initialState: "渲染当前能力边界与业务流程卡片；不读取 Backend。",
    lifecycle: [
      { name: "Render", detail: "App 根据 activeView 渲染 DashboardPage。" },
      { name: "Choose", detail: "openBusinessStep() 记录学习操作，并请求 App 切换目标 tab。" },
      { name: "Switch", detail: "App.changeView() 更新 activeView，React 卸载总览并渲染目标页面。" },
    ],
    sources: [
      { label: "页面入口", path: "frontend/src/App.tsx", reason: "持有 activeView，并渲染当前业务页与 LearningSidebar。" },
      { label: "业务总览", path: "frontend/src/pages/DashboardPage.tsx", reason: "定义 Scenario01 的页面顺序、能力边界和入口事件。" },
    ],
  },
  documents: {
    navigation: "文書管理",
    component: "DocumentsPage",
    step: "1 / 4",
    businessObject: "Scenario01 的销售、库存、促销、顾客和竞品内部资料，以及由资料生成的 document_id 与 Chunk。",
    whyNeeded: "企业分析必须先把可追溯的内部资料登记并分块；RAG 才能返回证据，而不是让前端编造业务事实。",
    initialState: "mount 后通过 useEffect() 加载文书列表；选中文书变化时读取详情和 Chunk。",
    lifecycle: [
      { name: "Mount", detail: "useEffect() 调用 loadDocuments(true)，用 showArchived 决定列表范围。" },
      { name: "Select", detail: "selectedDocumentId 变化后，refreshSelectedDocument() 并行刷新详情与 Chunk。" },
      { name: "Operate", detail: "上传、Import、Chunk 或 Archive 成功后，刷新列表与当前文书。" },
      { name: "Render", detail: "React 根据 loading、error、selectedDocument 与 chunkData 重绘页面。" },
    ],
    sources: [
      { label: "页面状态", path: "frontend/src/pages/DocumentsPage.tsx", reason: "管理列表、选择、上传和文书操作的 React state。" },
      { label: "API 适配", path: "frontend/src/api.ts", reason: "封装 document HTTP 请求与响应解析。" },
      { label: "Router", path: "backend/app/api/documents.py", reason: "接收上传、读取和归档请求。" },
      { label: "业务服务", path: "backend/app/services/document_read_service.py", reason: "读取文书详情的服务边界。" },
    ],
  },
  rag: {
    navigation: "RAG検索",
    component: "RagPage",
    step: "2 / 4",
    businessObject: "Scenario01 已完成 Chunk 的内部资料、检索结果和 Citation；当前为 Keyword Retrieval 与固定逻辑回答。",
    whyNeeded: "业务人员需要先检查结论是否有内部证据支撑，才能把销售下降原因带入分析依頼和审批。",
    initialState: "页面初始只显示表单；没有自动检索，也不会自动继承文書管理页的条件。",
    lifecycle: [
      { name: "Input", detail: "用户填写检索条件或业务问题，React 保存在本页 state。" },
      { name: "Request", detail: "submitRetrieval() 或 submitInternalRag() 调用 api.ts，并设置 loading。" },
      { name: "Resolve", detail: "成功写入 results / citations；证据不足时保留 Backend 的 422 业务结果。" },
      { name: "Clear", detail: "清除按钮只重置 React result state，不发送 API 请求。" },
    ],
    sources: [
      { label: "页面状态", path: "frontend/src/pages/RagPage.tsx", reason: "管理检索表单、回答表单、结果、错误与清除操作。" },
      { label: "API 适配", path: "frontend/src/api.ts", reason: "封装检索与 Internal RAG HTTP 调用。" },
      { label: "检索 Router", path: "backend/app/api/document_retrieval.py", reason: "接收 Keyword Retrieval 请求。" },
      { label: "RAG Router", path: "backend/app/api/internal_rag.py", reason: "接收带 Citation 的内部问答请求。" },
    ],
  },
  tasks: {
    navigation: "分析依頼",
    component: "TasksPage",
    step: "3 / 4",
    businessObject: "Scenario01 的关东饮料销售下降经营课题、task_id、SSE 事件和最终 report。",
    whyNeeded: "企业把可确认的问题转成可追踪任务，以异步执行避免 HTTP 请求一直等待，并把执行过程和报告分开读取。",
    initialState: "初始为 idle；没有 task_id、SSE 事件或 report。",
    lifecycle: [
      { name: "Submit", detail: "submit() 清空旧状态，POST /api/tasks 后保存 task_id 与 queued 状态。" },
      { name: "Stream", detail: "subscribeToTask() 用 EventSource 接收 queued / running / done 等 SSE 事件。" },
      { name: "Complete", detail: "收到 done 后取消订阅，并调用 loadReport() 读取最终 report。" },
      { name: "Unmount", detail: "useEffect cleanup 调用取消订阅，防止旧 SSE 继续写入已离开的页面。" },
    ],
    sources: [
      { label: "页面状态", path: "frontend/src/pages/TasksPage.tsx", reason: "管理 taskId、status、events、report 和 SSE cleanup。" },
      { label: "API / SSE", path: "frontend/src/api.ts", reason: "创建任务、读取报告并建立 EventSource 订阅。" },
      { label: "Task Router", path: "backend/app/api/tasks.py", reason: "接受任务、注册后台执行并提供 SSE 与 report。" },
      { label: "Workflow", path: "backend/app/workflow/graph.py", reason: "执行 route → kpi → research → report 工作流。" },
    ],
  },
  approval: {
    navigation: "承認管理",
    component: "ApprovalPage",
    step: "4 / 4",
    businessObject: "Scenario01 已完成 report 的 task_id、approval_id、report_version_id 与审批审计事件。",
    whyNeeded: "经营结论需要经过责任人审批、拒绝或修正，并保留版本和审计事实，才能成为可追溯的企业决策依据。",
    initialState: "mount 后读取审批列表；提交审批需要用户手动输入已完成报告的 task_id。",
    lifecycle: [
      { name: "Mount", detail: "useEffect() 读取 approval 列表，并选择当前可见记录。" },
      { name: "Submit", detail: "提交 task_id 后由 Backend 创建 report version 与 approval request。" },
      { name: "Decide", detail: "承認、却下或修正依頼触发状态迁移，并刷新列表与详情。" },
      { name: "Audit", detail: "Approval API 经 AuditMiddleware 与权限边界；403、409 是业务结果而非页面故障。" },
    ],
    sources: [
      { label: "页面状态", path: "frontend/src/pages/ApprovalPage.tsx", reason: "管理列表、详情、提交和三种审批操作。" },
      { label: "API 适配", path: "frontend/src/api.ts", reason: "封装 approval HTTP 调用与错误解析。" },
      { label: "Approval Router", path: "backend/app/api/approvals.py", reason: "处理列表、提交、决定与修正请求。" },
      { label: "业务服务", path: "backend/app/services/approval_service.py", reason: "执行审批状态迁移、报告版本和审计边界。" },
    ],
  },
};

function eventSummary(event: LearningEvent | null) {
  if (event === null) {
    return { title: "尚未操作", detail: "当前显示页面初始状态。执行一次页面操作后，这里会替换为本次真实 handler、API 与 state 变化。" };
  }

  const transport = event.apiPath
    ? `${event.apiMethod ?? "API"} ${event.apiPath} · ${event.apiStatus ?? "请求中"}`
    : "本次操作不发送 API 请求";
  return { title: event.eventName, detail: transport };
}

/**
 * LearningSidebar V2 只负责当前 React 页面和最近一次操作的即时学习信息。
 *
 * 谁调用它：
 * - App.tsx 将 activeView 对应的 page 与页面 handler 上报的 LearningEvent 传入。
 *
 * 它不做什么：
 * - 不发送请求、不保存业务数据、不复制 Scenario01 原文，也不展示业务测试 Case。
 * - 测试 Case 继续由 BusinessLearningPanel 展示，避免侧栏变成静态说明书。
 *
 * 日本现场面试可以这样讲：
 * - 该组件把 UI 行为、状态变化、调用链和源码入口放在同一屏，但保持为纯展示组件，
 *   所以不会影响既有业务请求或页面生命周期。
 */
export function LearningSidebar({ page, latestEvent }: LearningSidebarProps) {
  const info = pageInfo[page];
  const currentEvent = eventSummary(latestEvent);

  return (
    <aside className="learning-sidebar" aria-label="固定学习面板">
      <div className="learning-sidebar-scroll">
        <div className="learning-sidebar-heading">
          <p className="page-eyebrow">ERIP / REACT MODERN LEARNING</p>
          <h2>实时学习面板</h2>
          <p>{info.navigation} · {info.component} · {info.step}</p>
        </div>

        <section className="learning-live" aria-live="polite">
          <h3>01 实时操作</h3>
          <strong>{currentEvent.title}</strong>
          <p>{currentEvent.detail}</p>
          {latestEvent?.stateChanges.map((change) => <code key={change}>{change}</code>)}
          {latestEvent?.note && <p className="learning-note">{latestEvent.note}</p>}
        </section>

        <section>
          <h3>02 当前业务对象</h3>
          <p>{info.businessObject}</p>
        </section>

        <section>
          <h3>03 企业为什么需要当前页面</h3>
          <p>{info.whyNeeded}</p>
        </section>

        <section>
          <h3>04 页面生命周期</h3>
          <p className="learning-initial-state"><strong>初始：</strong>{info.initialState}</p>
          <ol className="learning-lifecycle">
            {info.lifecycle.map((item, index) => (
              <li key={item.name}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                <div><strong>{item.name}</strong><small>{item.detail}</small></div>
              </li>
            ))}
          </ol>
        </section>

        <section>
          <h3>05 源码定位</h3>
          <p className="source-hint">先读页面 handler，再顺着 API 适配层进入 Router 与业务边界。</p>
          <ul className="learning-source-list">
            {info.sources.map((source) => (
              <li key={source.path}>
                <strong>{source.label}</strong>
                <code>{source.path}</code>
                <small>{source.reason}</small>
              </li>
            ))}
          </ul>
          {latestEvent?.backendFlow && (
            <div className="learning-current-flow">
              <strong>本次操作链路</strong>
              <code>{latestEvent.backendFlow.join(" → ")}</code>
            </div>
          )}
        </section>
      </div>
    </aside>
  );
}
