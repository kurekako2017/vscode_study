import { useEffect, useState } from "react";

import { AuthProvider, type AuthSession, useAuth } from "./auth/AuthContext";
import type { Permission } from "./auth/permissions";
import { LearningSidebar } from "./components/LearningSidebar";
import { LifecycleProbe } from "./learning/LifecycleProbe";
import { LearningTraceProvider, useLearningTrace } from "./learning/LearningTraceContext";
import type { LearningEvent, LearningPage } from "./learning/learningTypes";
import { pageCatalog } from "./learning/pageCatalog";
import { AdminLlmPage } from "./pages/AdminLlmPage";
import { ApprovalPage } from "./pages/ApprovalPage";
import { DashboardPage } from "./pages/DashboardPage";
import { DocumentsPage } from "./pages/DocumentsPage";
import { LoginPage } from "./pages/LoginPage";
import { RagPage } from "./pages/RagPage";
import { TasksPage } from "./pages/TasksPage";
import { ProtectedRoute } from "./routing/ProtectedRoute";
import { navigateTo, useCurrentPath } from "./routing/navigation";

type ViewTab = "dashboard" | "analysis" | "documents" | "rag" | "approval" | "ai-admin";

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
    label: "RAG/AI分析",
    path: "/rag",
    anyPermissions: ["retrieval.query", "analysis.execute"],
  },
  { value: "analysis", label: "KPI任务分析", path: "/analysis", permission: "analysis.execute" },
  {
    value: "approval",
    label: "承認管理",
    path: "/approval",
    anyPermissions: ["approval.submit", "approval.review", "approval.admin"],
  },
  {
    value: "ai-admin",
    label: "AI管理",
    path: "/ai-admin",
    permission: "security.manage",
  },
];

const viewByPath: Readonly<Record<string, ViewTab>> = {
  "/dashboard": "dashboard",
  "/documents": "documents",
  "/rag": "rag",
  "/analysis": "analysis",
  "/approval": "approval",
  "/ai-admin": "ai-admin",
};

const learningPageByView: Record<ViewTab, LearningPage> = {
  dashboard: "dashboard",
  analysis: "tasks",
  documents: "documents",
  rag: "rag",
  approval: "approval",
  "ai-admin": "dashboard",
};

interface AppProps {
  /** 组件测试可注入身份，生产 main.tsx 不传。 */
  initialSession?: AuthSession | null;
  /** 测试可关闭 StrictMode 语义标记；生产 main.tsx 为 true。 */
  strictModeEnabled?: boolean;
}

/**
 * 顶层装配 AuthProvider + LearningTraceProvider。
 * 学习 Trace 不发送 Backend，不保存 Access Token 原文。
 */
export default function App({ initialSession, strictModeEnabled = true }: AppProps) {
  return (
    <LearningTraceProvider strictModeEnabled={strictModeEnabled}>
      <AuthProvider initialSession={initialSession}>
        <LifecycleProbe
          componentId="App"
          displayName="App"
          hooks={["useState", "useEffect", "useAuth", "useLearningTrace"]}
        >
          <ApplicationRoutes />
        </LifecycleProbe>
      </AuthProvider>
    </LearningTraceProvider>
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

  if (path === "/login") {
    return (
      <LifecycleProbe
        componentId="LoginPage"
        displayName="LoginPage"
        page="login"
        route="/login"
        isPageRoot
        hooks={pageCatalog.login.hooks.map((item) => item.name)}
      >
        <LoginPage />
      </LifecycleProbe>
    );
  }

  return (
    <LifecycleProbe
      componentId="ProtectedRoute.Shell"
      displayName="ProtectedRoute"
      parentId="App"
      hooks={["useAuth"]}
    >
      <ProtectedRoute>
        <ApplicationShell path={path} />
      </ProtectedRoute>
    </LifecycleProbe>
  );
}

/**
 * ApplicationShell 负责 URL 页面切换、导航可见性和顶层用户信息。
 * 页面只接收 permission-derived boolean，不读取 role，也不接触 Access Token。
 */
function ApplicationShell({ path }: { path: string }) {
  const auth = useAuth();
  const trace = useLearningTrace();
  const activeView = viewByPath[path];
  const [latestLearningEvent, setLatestLearningEvent] = useState<LearningEvent | null>(null);
  const learningPage = activeView ? learningPageByView[activeView] : "dashboard";

  useEffect(() => {
    if (!activeView) return;
    const page = learningPageByView[activeView];
    trace.setRouteContext(path, page);
    // 安全 Props 边：只记录 prop 名与类型摘要，不记录 Token。
    trace.recordProp("ApplicationShell", pageCatalog[page].component, "onLearningEvent", "function");
    if (activeView === "documents") {
      trace.recordProp("ApplicationShell", "DocumentsPage", "canWrite", auth.hasPermission("documents.write"));
      trace.recordProp("ApplicationShell", "DocumentsPage", "canArchive", auth.hasPermission("documents.archive"));
    }
    if (activeView === "rag") {
      trace.recordProp("ApplicationShell", "RagPage", "canRetrieve", auth.hasPermission("retrieval.query"));
      trace.recordProp("ApplicationShell", "RagPage", "canAnalyze", auth.hasPermission("analysis.execute"));
    }
    if (activeView === "approval") {
      trace.recordProp("ApplicationShell", "ApprovalPage", "canSubmit", auth.hasPermission("approval.submit"));
      trace.recordProp("ApplicationShell", "ApprovalPage", "canReview", auth.hasPermission("approval.review"));
      trace.recordProp(
        "ApplicationShell",
        "ApprovalPage",
        "currentUserLabel",
        `${auth.currentUser?.username} (${auth.currentUser?.role})`,
      );
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeView, path]);

  function recordLearningEvent(event: LearningEvent) {
    setLatestLearningEvent(event);
    trace.recordLearningEvent(event);
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

  const pageRevision = `${path}::${latestLearningEvent?.eventName ?? "idle"}`;

  return (
    <LifecycleProbe
      componentId="ApplicationShell"
      displayName="ApplicationShell"
      parentId="ProtectedRoute.Shell"
      page={learningPage}
      route={path}
      revision={pageRevision}
      hooks={["useState", "useEffect", "useAuth", "useLearningTrace"]}
    >
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
                <LifecycleProbe
                  componentId="DashboardPage"
                  displayName="DashboardPage"
                  parentId="ApplicationShell"
                  page="dashboard"
                  route="/dashboard"
                  isPageRoot
                  revision={pageRevision}
                  hooks={pageCatalog.dashboard.hooks.map((item) => item.name)}
                >
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
                </LifecycleProbe>
              )}
              {activeView === "analysis" && (
                <LifecycleProbe
                  componentId="TasksPage"
                  displayName="TasksPage"
                  parentId="ApplicationShell"
                  page="tasks"
                  route="/analysis"
                  isPageRoot
                  revision={pageRevision}
                  hooks={pageCatalog.tasks.hooks.map((item) => item.name)}
                >
                  <ProtectedRoute permission="analysis.execute">
                    <TasksPage onLearningEvent={recordLearningEvent} />
                  </ProtectedRoute>
                </LifecycleProbe>
              )}
              {activeView === "documents" && (
                <LifecycleProbe
                  componentId="DocumentsPage"
                  displayName="DocumentsPage"
                  parentId="ApplicationShell"
                  page="documents"
                  route="/documents"
                  isPageRoot
                  revision={pageRevision}
                  hooks={pageCatalog.documents.hooks.map((item) => item.name)}
                >
                  <ProtectedRoute permission="documents.read">
                    <DocumentsPage
                      onLearningEvent={recordLearningEvent}
                      canWrite={auth.hasPermission("documents.write")}
                      canArchive={auth.hasPermission("documents.archive")}
                    />
                  </ProtectedRoute>
                </LifecycleProbe>
              )}
              {activeView === "rag" && (
                <LifecycleProbe
                  componentId="RagPage"
                  displayName="RagPage"
                  parentId="ApplicationShell"
                  page="rag"
                  route="/rag"
                  isPageRoot
                  revision={pageRevision}
                  hooks={pageCatalog.rag.hooks.map((item) => item.name)}
                >
                  <ProtectedRoute anyPermissions={["retrieval.query", "analysis.execute"]}>
                    <RagPage
                      onLearningEvent={recordLearningEvent}
                      canRetrieve={auth.hasPermission("retrieval.query")}
                      canAnalyze={auth.hasPermission("analysis.execute")}
                    />
                  </ProtectedRoute>
                </LifecycleProbe>
              )}
              {activeView === "ai-admin" && (
                <LifecycleProbe
                  componentId="AdminLlmPage"
                  displayName="AdminLlmPage"
                  parentId="ApplicationShell"
                  page="dashboard"
                  route="/ai-admin"
                  isPageRoot
                  revision={pageRevision}
                  hooks={pageCatalog.dashboard.hooks.map((item) => item.name)}
                >
                  <ProtectedRoute permission="security.manage">
                    <AdminLlmPage />
                  </ProtectedRoute>
                </LifecycleProbe>
              )}
              {activeView === "approval" && (
                <LifecycleProbe
                  componentId="ApprovalPage"
                  displayName="ApprovalPage"
                  parentId="ApplicationShell"
                  page="approval"
                  route="/approval"
                  isPageRoot
                  revision={pageRevision}
                  hooks={pageCatalog.approval.hooks.map((item) => item.name)}
                >
                  <ProtectedRoute anyPermissions={["approval.submit", "approval.review", "approval.admin"]}>
                    <ApprovalPage
                      onLearningEvent={recordLearningEvent}
                      canSubmit={auth.hasPermission("approval.submit")}
                      canReview={auth.hasPermission("approval.review")}
                      currentUserLabel={`${auth.currentUser?.username} (${auth.currentUser?.role})`}
                    />
                  </ProtectedRoute>
                </LifecycleProbe>
              )}
            </div>
            <LifecycleProbe
              componentId="LearningSidebar"
              displayName="LearningSidebar"
              parentId="ApplicationShell"
              page={learningPage}
              route={path}
              revision={pageRevision}
              hooks={["useLearningTraceOptional"]}
            >
              <LearningSidebar
                page={learningPage}
                latestEvent={latestLearningEvent}
                route={path}
              />
            </LifecycleProbe>
          </div>
        ) : (
          <section className="panel access-denied" role="alert">
            <p className="eyebrow">404</p>
            <h2>ページが見つかりません</h2>
            <button type="button" onClick={() => navigateTo("/dashboard", { replace: true })}>ダッシュボードへ戻る</button>
          </section>
        )}
      </main>
    </LifecycleProbe>
  );
}
