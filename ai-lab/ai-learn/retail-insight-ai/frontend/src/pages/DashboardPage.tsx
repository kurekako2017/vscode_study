import { PageHeader } from "../components/PageHeader";
import { StatusBadge } from "../components/StatusBadge";
import type { RecordLearningEvent } from "../learning/learningTypes";

type DashboardTarget = "analysis" | "documents" | "rag" | "approval";

interface DashboardPageProps {
  onNavigate: (target: DashboardTarget) => void;
  onLearningEvent?: RecordLearningEvent;
}

const runtimeFacts = [
  ["数据存储", "InMemory"],
  ["调研数据源", "静态数据"],
  ["检索方式", "关键词检索"],
  ["RAG 回答方式", "固定逻辑生成"],
  ["当前用户", "系统默认用户"],
  ["真实 LLM", "未启用"],
  ["PostgreSQL", "当前运行环境尚未验证"],
  ["pgvector", "尚未实现"],
];

const boundaryFacts = [
  ["任务工作流", "可用"],
  ["文书管理", "可用"],
  ["关键词检索", "可用"],
  ["固定逻辑 RAG", "可用"],
  ["审批工作流", "可用"],
  ["真实 LLM", "未连接"],
  ["向量检索", "尚未可用"],
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
    connection: "已连接：文书与 Chunk 由 Backend 保存；到 RAG検索为手动衔接。",
    target: "documents",
    actionLabel: "文書管理を開く",
  },
  {
    title: "RAG検索",
    purpose: "以 Keyword Retrieval 验证内部资料可以被检索，并查看 citation。",
    connection: "手动衔接：用户输入检索条件；结果不会自动带入分析依頼。",
    target: "rag",
    actionLabel: "RAG検索を開く",
  },
  {
    title: "分析依頼",
    purpose: "创建关东饮料销售下降分析任务，观察 SSE 并读取 report。",
    connection: "手动衔接：RAG 结论需手动写入问题；完成后复制 task_id 到承認管理。",
    target: "analysis",
    actionLabel: "分析依頼を開く",
  },
  {
    title: "承認管理",
    purpose: "基于已完成 report 的 task_id 创建 approval_id，执行承認、却下或修正依頼。",
    connection: "手动衔接：TasksPage 不会自动传递 task_id；审批审计由 Backend 记录。",
    target: "approval",
    actionLabel: "承認管理を開く",
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
export function DashboardPage({ onNavigate, onLearningEvent }: DashboardPageProps) {
  function openBusinessStep(target: DashboardTarget, actionLabel: string) {
    onLearningEvent?.({
      eventName: `openBusinessStep(${target})`,
      stateChanges: ["activeView: dashboard → target", `入口：${actionLabel}`],
      backendFlow: ["无 Backend 调用", "App.tsx changeView()", "React 重新渲染目标页面"],
      note: "导航只修改 React 本地状态，不发送 API 请求。",
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
                {step.target !== null && step.actionLabel && (
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
            <li><span>02</span><div><strong>RAG検索：验证资料是否可检索</strong><small>确认 results、score、citation 与空结果。</small></div></li>
            <li><span>03</span><div><strong>分析依頼：创建经营分析任务</strong><small>确认 task_id、SSE 和 report。</small></div></li>
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
            <p><strong>操作顺序：</strong>上传并处理“関東飲料売上分析.md” → 用 RAG検索确认 Chunk 与 citation → 创建 hybrid 分析任务 → 复制已完成 task_id 提交审批。</p>
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
