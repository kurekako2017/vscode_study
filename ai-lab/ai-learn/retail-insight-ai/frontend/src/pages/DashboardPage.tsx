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
    title: "分析依頼",
    description: "分析依頼を作成し、SSE の進捗と生成されたレポートを確認します。",
    status: "可用",
    target: "analysis",
    actionLabel: "分析依頼を開く",
  },
  {
    title: "文書管理",
    description: "文書のアップロード、詳細確認、アーカイブ、Import、Chunk 操作を行います。",
    status: "可用",
    target: "documents",
    actionLabel: "文書管理を開く",
  },
  {
    title: "RAG",
    description: "キーワード検索と固定ロジックによる Internal RAG 回答を実行します。",
    status: "可用",
    target: "rag",
    actionLabel: "RAG検索を開く",
  },
  {
    title: "承認管理",
    description: "承認待ち一覧と詳細を確認し、承認、却下、修正依頼を実行します。",
    status: "可用",
    target: "approval",
    actionLabel: "承認管理を開く",
  },
];

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
        eyebrow="当前实现总览"
        title="Enterprise Retail Intelligence Platform"
        description="通过当前系统状态、功能边界和 API 连接情况，理解 ERIP 的整体实现。"
      />

      <section className="dashboard-shell" aria-label="ERIP 学习总览">
        <section className="panel dashboard-panel">
          <div className="panel-heading">
            <span>01</span>
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
            <span>02</span>
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

        <section className="panel dashboard-panel">
          <div className="panel-heading">
            <span>03</span>
            <h2>功能入口</h2>
            <small>用于演示与学习的快捷入口</small>
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
