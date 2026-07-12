import { useState } from "react";

import { DashboardPage } from "./pages/DashboardPage";
import { ApprovalPage } from "./pages/ApprovalPage";
import { DocumentsPage } from "./pages/DocumentsPage";
import { RagPage } from "./pages/RagPage";
import { TasksPage } from "./pages/TasksPage";

type ViewTab = "dashboard" | "analysis" | "documents" | "rag" | "approval";

const navItems: Array<{ value: ViewTab; label: string }> = [
  { value: "dashboard", label: "Dashboard" },
  { value: "analysis", label: "Analysis / Tasks" },
  { value: "documents", label: "Documents" },
  { value: "rag", label: "RAG" },
  { value: "approval", label: "Approval" },
];

/**
 * App 现在只负责顶层导航和页面切换。
 *
 * 为什么这样拆：
 * - Dashboard、Tasks、Documents、RAG、Approval 已经是五个独立业务区，继续堆在一个文件里会让学习成本快速上升。
 * - 当前仍然不引入 Router，先保持 tab 切换的最小结构。
 */
export default function App() {
  const [activeView, setActiveView] = useState<ViewTab>("dashboard");

  return (
    <main className="shell">
      <header className="hero">
        <p className="eyebrow">RETAIL OPERATIONS / LOCAL STATIC ENVIRONMENT</p>
        <h1>Retail Insight AI</h1>
        <p className="lead">KPI の確定計算と調査結果を、監査可能な一つの分析レポートへ。</p>
      </header>

      <nav className="top-nav" aria-label="主要ページ">
        {navItems.map((item) => (
          <button
            key={item.value}
            type="button"
            aria-current={activeView === item.value ? "page" : undefined}
            className={activeView === item.value ? "nav-chip selected" : "nav-chip"}
            onClick={() => setActiveView(item.value)}
          >
            {item.label}
          </button>
        ))}
      </nav>

      {activeView === "dashboard" && <DashboardPage onNavigate={setActiveView} />}
      {activeView === "analysis" && <TasksPage />}
      {activeView === "documents" && <DocumentsPage />}
      {activeView === "rag" && <RagPage />}
      {activeView === "approval" && <ApprovalPage />}
    </main>
  );
}
