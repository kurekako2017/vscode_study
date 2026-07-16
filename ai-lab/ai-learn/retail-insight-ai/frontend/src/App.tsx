import { useEffect, useState } from "react";

import { AuthProvider, type AuthSession, useAuth } from "./auth/AuthContext";
import type { Permission } from "./auth/permissions";
import { LearningSidebar } from "./components/LearningSidebar";
import type { LearningEvent, LearningPage } from "./learning/learningTypes";
import { ApprovalPage } from "./pages/ApprovalPage";
import { DashboardPage } from "./pages/DashboardPage";
import { DocumentsPage } from "./pages/DocumentsPage";
import { LoginPage } from "./pages/LoginPage";
import { RagPage } from "./pages/RagPage";
import { TasksPage } from "./pages/TasksPage";
import { ProtectedRoute } from "./routing/ProtectedRoute";
import { navigateTo, useCurrentPath } from "./routing/navigation";

type ViewTab = "dashboard" | "analysis" | "documents" | "rag" | "approval";

interface NavItem {
  value: ViewTab;
  label: string;
  path: string;
  permission?: Permission;
  anyPermissions?: readonly Permission[];
}

const navItems: readonly NavItem[] = [
  { value: "dashboard", label: "学习总览", path: "/dashboard" },
  { value: "documents", label: "文書管理", path: "/documents", permission: "documents.read" },
  {
    value: "rag",
    label: "RAG検索",
    path: "/rag",
    anyPermissions: ["retrieval.query", "analysis.execute"],
  },
  { value: "analysis", label: "分析依頼", path: "/analysis", permission: "analysis.execute" },
  {
    value: "approval",
    label: "承認管理",
    path: "/approval",
    anyPermissions: ["approval.submit", "approval.review", "approval.admin"],
  },
];

const viewByPath: Readonly<Record<string, ViewTab>> = {
  "/dashboard": "dashboard",
  "/documents": "documents",
  "/rag": "rag",
  "/analysis": "analysis",
  "/approval": "approval",
};

const learningPageByView: Record<ViewTab, LearningPage> = {
  dashboard: "dashboard",
  analysis: "tasks",
  documents: "documents",
  rag: "rag",
  approval: "approval",
};

interface AppProps {
  /** 组件测试可注入身份，生产 main.tsx 不传。 */
  initialSession?: AuthSession | null;
}

/**
 * 顶层只装配 AuthProvider；认证状态、API Token 与权限判断不会散落到业务页。
 */
export default function App({ initialSession }: AppProps) {
  return (
    <AuthProvider initialSession={initialSession}>
      <ApplicationRoutes />
    </AuthProvider>
  );
}

function ApplicationRoutes() {
  const path = useCurrentPath();
  const auth = useAuth();

  useEffect(() => {
    if (path === "/") navigateTo("/dashboard", { replace: true });
    if (path === "/login" && !auth.isInitializing && auth.isAuthenticated) {
      navigateTo("/dashboard", { replace: true });
    }
  }, [auth.isAuthenticated, auth.isInitializing, path]);

  if (path === "/login") return <LoginPage />;

  return (
    <ProtectedRoute>
      <ApplicationShell path={path} />
    </ProtectedRoute>
  );
}

/**
 * ApplicationShell 负责 URL 页面切换、导航可见性和顶层用户信息。
 * 页面只接收 permission-derived boolean，不读取 role，也不接触 Access Token。
 */
function ApplicationShell({ path }: { path: string }) {
  const auth = useAuth();
  const activeView = viewByPath[path];
  const [latestLearningEvent, setLatestLearningEvent] = useState<LearningEvent | null>(null);

  function recordLearningEvent(event: LearningEvent) {
    setLatestLearningEvent(event);
  }

  function canOpen(item: NavItem): boolean {
    if (item.permission) return auth.hasPermission(item.permission);
    if (item.anyPermissions) return auth.hasAnyPermission(item.anyPermissions);
    return true;
  }

  function changeView(nextView: ViewTab) {
    const item = navItems.find((candidate) => candidate.value === nextView);
    if (!item || !canOpen(item)) return;
    setLatestLearningEvent(null);
    navigateTo(item.path);
  }

  function canNavigateDashboardTarget(target: Exclude<ViewTab, "dashboard">): boolean {
    const item = navItems.find((candidate) => candidate.value === target);
    return item ? canOpen(item) : false;
  }

  function logout() {
    auth.logout();
    navigateTo("/login", { replace: true });
  }

  return (
    <main className="shell">
      <header className="hero">
        <div>
          <p className="eyebrow">ERIP 本地学习环境</p>
          <h1>Enterprise Retail Intelligence Platform</h1>
          <p className="lead">当前本地实现将 KPI 计算、调研数据和审批流程连接为可追踪的经营分析平台。</p>
        </div>
        <div className="session-summary" aria-label="当前会话">
          <strong>{auth.currentUser?.username}</strong>
          <span>{auth.currentUser?.role}</span>
          <small>权限来自前端冻结 Registry</small>
          <button type="button" className="secondary-button" onClick={logout}>ログアウト</button>
        </div>
      </header>

      {auth.authorizationNotice && (
        <div className="status-banner warning global-auth-notice" role="alert">
          <span>{auth.authorizationNotice}</span>
          <button type="button" className="secondary-button" onClick={auth.clearAuthorizationNotice}>閉じる</button>
        </div>
      )}

      <nav className="top-nav" aria-label="主要ページ">
        {navItems.filter(canOpen).map((item) => (
          <button
            key={item.value}
            type="button"
            aria-current={activeView === item.value ? "page" : undefined}
            className={activeView === item.value ? "nav-chip selected" : "nav-chip"}
            onClick={() => changeView(item.value)}
          >
            {item.label}
          </button>
        ))}
      </nav>

      {activeView ? (
        <div className="app-learning-layout">
          <div className="app-learning-main">
            {activeView === "dashboard" && (
              <DashboardPage
                onNavigate={changeView}
                onLearningEvent={recordLearningEvent}
                canNavigate={canNavigateDashboardTarget}
                currentUser={auth.currentUser ? {
                  username: auth.currentUser.username,
                  role: auth.currentUser.role,
                  permissionCount: auth.currentUser.permissions.length,
                } : undefined}
              />
            )}
            {activeView === "analysis" && (
              <ProtectedRoute permission="analysis.execute">
                <TasksPage onLearningEvent={recordLearningEvent} />
              </ProtectedRoute>
            )}
            {activeView === "documents" && (
              <ProtectedRoute permission="documents.read">
                <DocumentsPage
                  onLearningEvent={recordLearningEvent}
                  canWrite={auth.hasPermission("documents.write")}
                  canArchive={auth.hasPermission("documents.archive")}
                />
              </ProtectedRoute>
            )}
            {activeView === "rag" && (
              <ProtectedRoute anyPermissions={["retrieval.query", "analysis.execute"]}>
                <RagPage
                  onLearningEvent={recordLearningEvent}
                  canRetrieve={auth.hasPermission("retrieval.query")}
                  canAnalyze={auth.hasPermission("analysis.execute")}
                />
              </ProtectedRoute>
            )}
            {activeView === "approval" && (
              <ProtectedRoute anyPermissions={["approval.submit", "approval.review", "approval.admin"]}>
                <ApprovalPage
                  onLearningEvent={recordLearningEvent}
                  canSubmit={auth.hasPermission("approval.submit")}
                  canReview={auth.hasPermission("approval.review")}
                  currentUserLabel={`${auth.currentUser?.username} (${auth.currentUser?.role})`}
                />
              </ProtectedRoute>
            )}
          </div>
          <LearningSidebar page={learningPageByView[activeView]} latestEvent={latestLearningEvent} />
        </div>
      ) : (
        <section className="panel access-denied" role="alert">
          <p className="eyebrow">404</p>
          <h2>ページが見つかりません</h2>
          <button type="button" onClick={() => navigateTo("/dashboard", { replace: true })}>ダッシュボードへ戻る</button>
        </section>
      )}
    </main>
  );
}
