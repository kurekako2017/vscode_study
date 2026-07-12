import { useState } from "react";

import { DocumentsPage } from "./pages/DocumentsPage";
import { RagPage } from "./pages/RagPage";
import { TasksPage } from "./pages/TasksPage";

type ViewTab = "analysis" | "documents" | "rag";

/**
 * App 现在只负责顶层导航和页面切换。
 *
 * 为什么这样拆：
 * - Tasks、Documents、RAG 已经是三个独立业务区，继续堆在一个文件里会让学习成本快速上升。
 * - 当前仍然不引入 Router，先保持 tab 切换的最小结构。
 */
export default function App() {
  const [activeView, setActiveView] = useState<ViewTab>("analysis");

  return (
    <main className="shell">
      <header className="hero">
        <p className="eyebrow">RETAIL OPERATIONS / LOCAL STATIC ENVIRONMENT</p>
        <h1>Retail Insight AI</h1>
        <p className="lead">KPI の確定計算と調査結果を、監査可能な一つの分析レポートへ。</p>
      </header>

      <nav className="top-nav" aria-label="主要ページ">
        <button
          type="button"
          className={activeView === "analysis" ? "nav-chip selected" : "nav-chip"}
          onClick={() => setActiveView("analysis")}
        >
          Analysis / Tasks
        </button>
        <button
          type="button"
          className={activeView === "documents" ? "nav-chip selected" : "nav-chip"}
          onClick={() => setActiveView("documents")}
        >
          Documents
        </button>
        <button
          type="button"
          className={activeView === "rag" ? "nav-chip selected" : "nav-chip"}
          onClick={() => setActiveView("rag")}
        >
          RAG
        </button>
      </nav>

      {activeView === "analysis" && <TasksPage />}
      {activeView === "documents" && <DocumentsPage />}
      {activeView === "rag" && <RagPage />}
    </main>
  );
}
