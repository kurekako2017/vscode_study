import { PageHeader } from "../components/PageHeader";
import { StatusBadge } from "../components/StatusBadge";
import type { RecordLearningEvent } from "../learning/learningTypes";

type DashboardTarget = "analysis" | "documents" | "rag" | "approval";

interface DashboardPageProps {
  onNavigate: (target: DashboardTarget) => void;
  onLearningEvent?: RecordLearningEvent;
  canNavigate?: (target: DashboardTarget) => boolean;
  currentUser?: {
    username: string;
    role: string;
    permissionCount: number;
  };
}

const boundaryFacts = [
  ["正式入口", "Docker http://127.0.0.1:8080"],
  ["开发入口", "Vite http://127.0.0.1:5173"],
  ["Repository", "PostgreSQL 正式 / InMemory 仅测试"],
  ["文书管理", "列表=DB；Import/Chunk 后可检索"],
  ["RAG/AI分析", "检索+显式 low_cost AI"],
  ["KPI任务分析", "/analysis Task+SSE（非 AI 成本页）"],
  ["LLM 默认", "stub（零费用）；AI管理可看模式"],
  ["真实付费 LLM", "默认关闭"],
];

const businessFlow: Array<{
  title: string;
  purpose: string;
  connection: string;
  target: DashboardTarget | null;
  actionLabel?: string;
}> = [
  {
    title: "文書管理",
    purpose: "登记关东地区饮料分类销售下降相关的内部资料，并生成 document_id、import_id 与 Chunk。",
    connection: "已连接：文书与 Chunk 由 Backend 保存；到 RAG/AI分析为手动衔接。",
    target: "documents",
    actionLabel: "文書管理を開く",
  },
  {
    title: "RAG/AI分析",
    purpose: "检索已 Chunk 文档；再显式触发 low_cost AI分析与 high_quality 董事会报告（展示 Provider/Model/Token/Cost）。",
    connection: "普通 RAG 默认可零 LLM；AI 不会自动跑。生成报告后可在承認管理下拉选择 task_id。",
    target: "rag",
    actionLabel: "打开 RAG/AI分析",
  },
  {
    title: "KPI任务分析",
    purpose: "旧 Task API + SSE 路径（hybrid/kpi/research），与成本 AI 分析不同。",
    connection: "产出 task report；企业审批主路径推荐 executive report 的 task_id。",
    target: "analysis",
    actionLabel: "打开 KPI任务分析",
  },
  {
    title: "承認管理",
    purpose: "从报告目录选择 task_id 提交审批，无需手抄。",
    connection: "API：GET /api/v1/reports → submit-approval；employee 403 / manager 200。",
    target: "approval",
    actionLabel: "打开承認管理",
  },
  {
    title: "最终可审计报告",
    purpose: "报告、approval_id、report_version_id 与审批事件共同构成当前可追踪依据。",
    connection: "当前未连接：前端没有单独的最终审计报告汇总页面。",
    target: null,
  },
];

/**
 * DashboardPage 负责把“当前这个本地 MVP 到底能做什么”先讲清楚。
 *
 * 为什么这样设计：
 * - 进入系统的第一屏先给全局地图，比直接落到某个业务页更适合演示和学习。
 * - 这里的内容全部基于当前真实实现事实，不依赖新增后端统计接口。
 */
export function DashboardPage({
  onNavigate,
  onLearningEvent,
  canNavigate = () => true,
  currentUser,
}: DashboardPageProps) {
  const runtimeFacts = [
    ["正式数据存储", "PostgreSQL（Compose 权威）"],
    ["辅助测试存储", "InMemory（仅 unittest，非验收）"],
    ["调研数据源", "静态 / Stub Provider"],
    ["检索方式", "关键词检索（已 Chunk 文档）"],
    ["RAG 回答方式", "固定逻辑 / extractive（默认可零 LLM）"],
    ["当前用户", currentUser?.username ?? "系统默认用户"],
    ["当前角色", currentUser?.role ?? "未认证"],
    ["权限来源", currentUser ? `前端冻结 Registry（${currentUser.permissionCount} 项）` : "未加载"],
    ["LLM 模式", "默认 stub；admin 可在 AI管理 查看"],
    ["真实付费 LLM", "默认关闭（禁止验收开启）"],
    ["pgvector", "教学路线预留，当前非主链"],
  ];

  function openBusinessStep(target: DashboardTarget, actionLabel: string) {
    onLearningEvent?.({
      eventName: `openBusinessStep(${target})`,
      stateChanges: ["URL path: /dashboard → target", `入口：${actionLabel}`],
      backendFlow: ["无 Backend 调用", "App.tsx changeView()", "History API 更新并重新渲染目标页面"],
      note: "导航只修改浏览器 URL 与 React 页面状态，不发送 API 请求。",
    });
    onNavigate(target);
  }

  return (
    <>
      <PageHeader
        eyebrow="当前实现总览"
        title="Enterprise Retail Intelligence Platform"
        description="通过当前系统状态、功能边界和 API 连接情况，理解 ERIP 的整体实现。"
      />

      <section className="dashboard-shell" aria-label="ERIP 学习总览">
        <section className="panel dashboard-panel">
          <div className="panel-heading">
            <span>01</span>
            <h2>企业业务流程</h2>
            <small>关东地区饮料分类销售额下降案例</small>
          </div>
          <div className="dashboard-card-grid" aria-label="企业业务流程卡片">
            {businessFlow.map((step) => (
              <article key={step.title} className="result-card dashboard-card">
                <strong>{step.title}</strong>
                <p className="page-description card-description">{step.purpose}</p>
                <p className="boundary">{step.connection}</p>
                {step.target !== null && step.actionLabel && canNavigate(step.target) && (
                  <button type="button" onClick={() => step.target !== null && openBusinessStep(step.target, step.actionLabel!)}>{step.actionLabel}</button>
                )}
              </article>
            ))}
          </div>
        </section>

        <section className="panel dashboard-panel">
          <div className="panel-heading">
            <span>02</span>
            <h2>推荐学习顺序</h2>
            <small>先验证业务事实，再对照实际源码</small>
          </div>
          <ol className="event-list">
            <li><span>01</span><div><strong>文書管理：登记内部资料</strong><small>确认 document_id、import_id 和 Chunk。</small></div></li>
            <li><span>02</span><div><strong>RAG/AI分析：检索 + 显式 AI</strong><small>确认 results、citation；需要时再点 AI分析（看 Provider/Cost）。</small></div></li>
            <li><span>03</span><div><strong>KPI任务分析（可选）：Task + SSE</strong><small>旧 hybrid 链路；企业审批主路径优先 executive report。</small></div></li>
            <li><span>04</span><div><strong>承認管理：审核结果</strong><small>手动输入 task_id，确认 approval_id 与状态迁移。</small></div></li>
            <li><span>05</span><div><strong>调用流程：确认前后端代码链</strong><small>展开各业务页的「业务测试与源码学习」。</small></div></li>
          </ol>
        </section>

        <section className="panel dashboard-panel">
          <div className="panel-heading">
            <span>03</span>
            <h2>企业综合测试案例</h2>
            <small>ERIP-E2E-001</small>
          </div>
          <div className="learning-flow">
            <p><strong>案件背景：</strong>关东地区饮料分类销售额下降，经营企划需要登记内部资料、检索依据、生成经营报告并完成负责人审批。</p>
            <p><strong>操作顺序：</strong>上传 Scenario01 → Import → Chunk → RAG/AI分析确认 citation → 显式 AI分析/董事会报告 → 承認管理下拉选择 task_id 提交（无需手抄）。</p>
            <p><strong>预期业务结果：</strong>页面分别显示 document_id／import_id／Chunk、检索结果与 citation、task_id／report、approval_id／report_version_id。</p>
            <p><strong>确认点：</strong>这些 ID 当前均需手动衔接；系统没有自动把文书、RAG 结果或 task_id 串成单一请求。</p>
          </div>
        </section>

        <section className="panel dashboard-panel">
          <div className="panel-heading">
            <span>04</span>
            <h2>系统概览</h2>
            <small>当前本地实现</small>
          </div>
          <dl className="detail-grid runtime-grid">
            {runtimeFacts.map(([label, value]) => (
              <div key={label}>
                <dt>{label}</dt>
                <dd>{value}</dd>
              </div>
            ))}
          </dl>
        </section>

        <section className="panel dashboard-panel">
          <div className="panel-heading">
            <span>05</span>
            <h2>当前能力边界</h2>
            <small>已实现功能与尚未连接的能力</small>
          </div>
          <div className="dashboard-boundary-grid">
            {boundaryFacts.map(([label, value]) => (
              <article key={label} className="result-card boundary-card">
                <div className="subheading">
                  <strong>{label}</strong>
                  <StatusBadge value={value.replaceAll(" ", "_")} />
                </div>
                <p className="empty">{value}</p>
              </article>
            ))}
          </div>
        </section>

      </section>
    </>
  );
}
