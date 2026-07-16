import { type ReactNode, useEffect } from "react";

import { useAuth } from "../auth/AuthContext";
import type { Permission } from "../auth/permissions";
import { navigateTo } from "./navigation";

interface ProtectedRouteProps {
  children: ReactNode;
  permission?: Permission;
  anyPermissions?: readonly Permission[];
  allPermissions?: readonly Permission[];
}

/**
 * ProtectedRoute 处理认证与页面级权限；按钮级权限仍由页面 props 控制。
 * 它不替代 Backend 授权，只防止无权用户看到或直达不属于自己的前端入口。
 */
export function ProtectedRoute({
  children,
  permission,
  anyPermissions,
  allPermissions,
}: ProtectedRouteProps) {
  const auth = useAuth();

  useEffect(() => {
    if (!auth.isInitializing && !auth.isAuthenticated) {
      navigateTo("/login", {
        replace: true,
        state: { returnTo: window.location.pathname },
      });
    }
  }, [auth.isAuthenticated, auth.isInitializing]);

  if (auth.isInitializing || !auth.isAuthenticated) {
    return <p className="auth-loading" role="status">認証状態を確認しています…</p>;
  }

  const allowed = permission
    ? auth.hasPermission(permission)
    : anyPermissions
      ? auth.hasAnyPermission(anyPermissions)
      : allPermissions
        ? auth.hasAllPermissions(allPermissions)
        : true;

  if (!allowed) {
    return (
      <section className="panel access-denied" role="alert">
        <p className="eyebrow">403 Forbidden</p>
        <h2>アクセス権限がありません</h2>
        <p>現在のロールには、このページを表示するための権限がありません。</p>
        <button type="button" onClick={() => navigateTo("/dashboard", { replace: true })}>
          ダッシュボードへ戻る
        </button>
      </section>
    );
  }

  return children;
}
