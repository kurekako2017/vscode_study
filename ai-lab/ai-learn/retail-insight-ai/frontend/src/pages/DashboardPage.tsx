import { PageHeader } from "../components/PageHeader";
import { StatusBadge } from "../components/StatusBadge";

type DashboardTarget = "analysis" | "documents" | "rag" | "approval";

interface DashboardPageProps {
  onNavigate: (target: DashboardTarget) => void;
}

const capabilityCards: Array<{
  title: string;
  description: string;
  status: string;
  target: DashboardTarget;
  actionLabel: string;
}> = [
  {
    title: "Analysis / Tasks",
    description: "Create a task, watch SSE progress, and read the generated report in one place.",
    status: "Available",
    target: "analysis",
    actionLabel: "Open Tasks",
  },
  {
    title: "Documents",
    description: "Upload documents, inspect detail, archive, import, and chunk with real backend APIs.",
    status: "Available",
    target: "documents",
    actionLabel: "Open Documents",
  },
  {
    title: "RAG",
    description: "Run keyword retrieval and deterministic internal RAG answer flows using current backend capabilities.",
    status: "Available",
    target: "rag",
    actionLabel: "Open RAG",
  },
  {
    title: "Approval",
    description: "Review approval queue, inspect detail, and submit approve / reject / revise actions.",
    status: "Available",
    target: "approval",
    actionLabel: "Open Approval",
  },
];

const runtimeFacts = [
  ["Repository", "InMemory"],
  ["Research Provider", "Static"],
  ["Retrieval", "Keyword"],
  ["RAG Answer", "Deterministic"],
  ["Identity", "System placeholder user"],
  ["Real LLM", "Disabled"],
  ["PostgreSQL", "Not verified in current runtime"],
  ["pgvector", "Not implemented"],
];

const boundaryFacts = [
  ["Task Workflow", "Available"],
  ["Document Management", "Available"],
  ["Keyword Retrieval", "Available"],
  ["Deterministic RAG", "Available"],
  ["Approval Workflow", "Available"],
  ["Real LLM", "Not Connected"],
  ["Vector Retrieval", "Not Available"],
];

/**
 * DashboardPage 负责把“当前这个本地 MVP 到底能做什么”先讲清楚。
 *
 * 为什么这样设计：
 * - 进入系统的第一屏先给全局地图，比直接落到某个业务页更适合演示和学习。
 * - 这里的内容全部基于当前真实实现事实，不依赖新增后端统计接口。
 */
export function DashboardPage({ onNavigate }: DashboardPageProps) {
  return (
    <>
      <PageHeader
        eyebrow="LOCAL MVP OVERVIEW"
        title="Dashboard"
        description="A single entry point for the current local MVP: workflow, documents, retrieval, and approval are available; real LLM and vector search are intentionally not connected."
      />

      <section className="dashboard-shell" aria-label="Dashboard overview">
        <section className="panel dashboard-panel">
          <div className="panel-heading">
            <span>01</span>
            <h2>System Overview</h2>
            <small>Current local implementation only</small>
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
            <span>02</span>
            <h2>Capability Boundary</h2>
            <small>Real features vs not connected yet</small>
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

        <section className="panel dashboard-panel">
          <div className="panel-heading">
            <span>03</span>
            <h2>Feature Entry</h2>
            <small>Shortcut cards for demo and learning</small>
          </div>
          <div className="dashboard-card-grid">
            {capabilityCards.map((card) => (
              <article key={card.title} className="result-card dashboard-card">
                <div className="subheading">
                  <strong>{card.title}</strong>
                  <StatusBadge value={card.status} />
                </div>
                <p className="page-description card-description">{card.description}</p>
                <button type="button" onClick={() => onNavigate(card.target)}>
                  {card.actionLabel}
                </button>
              </article>
            ))}
          </div>
        </section>
      </section>
    </>
  );
}
