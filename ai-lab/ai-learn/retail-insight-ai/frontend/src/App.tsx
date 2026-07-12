import { useState } from "react";

import { DashboardPage } from "./pages/DashboardPage";
import { ApprovalPage } from "./pages/ApprovalPage";
import { DocumentsPage } from "./pages/DocumentsPage";
import { RagPage } from "./pages/RagPage";
import { TasksPage } from "./pages/TasksPage";

type ViewTab = "dashboard" | "analysis" | "documents" | "rag" | "approval";

const navItems: Array<{ value: ViewTab; label: string }> = [
  { value: "dashboard", label: "学习总览" },
  { value: "analysis", label: "分析依頼" },
  { value: "documents", label: "文書管理" },
  { value: "rag", label: "RAG検索" },
  { value: "approval", label: "承認管理" },
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
        <p className="eyebrow">ERIP 本地学习环境</p>
        <h1>Enterprise Retail Intelligence Platform</h1>
        <p className="lead">当前本地实现将 KPI 计算、调研数据和审批流程连接为可追踪的经营分析平台。</p>
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
