import {
  createContext,
  type ReactNode,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";

import {
  getCurrentUser,
  login as requestLogin,
  setApiAccessToken,
  setApiAuthHandlers,
} from "../api";
import type { CurrentUserResponse } from "../types";
import {
  getPermissionsForRole,
  hasAllPermissions as checkAllPermissions,
  hasAnyPermission as checkAnyPermission,
  hasPermission as checkPermission,
  type Permission,
} from "./permissions";
import { parseJwtIdentity } from "./jwtIdentity";
import { navigateTo } from "../routing/navigation";

export const ACCESS_TOKEN_SESSION_KEY = "erip.access_token";

export interface CurrentUser extends CurrentUserResponse {
  permissions: readonly Permission[];
}

export interface AuthSession {
  accessToken: string | null;
  currentUser: CurrentUser;
}

interface AuthContextValue {
  accessToken: string | null;
  currentUser: CurrentUser | null;
  isAuthenticated: boolean;
  isInitializing: boolean;
  authorizationNotice: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  clearAuthorizationNotice: () => void;
  hasPermission: (permission: Permission) => boolean;
  hasAnyPermission: (permissions: readonly Permission[]) => boolean;
  hasAllPermissions: (permissions: readonly Permission[]) => boolean;
}

interface AuthProviderProps {
  children: ReactNode;
  /** 仅用于组件测试注入已认证身份；生产入口不传此字段。 */
  initialSession?: AuthSession | null;
}

const AuthContext = createContext<AuthContextValue | null>(null);

function buildCurrentUser(identity: CurrentUserResponse): CurrentUser {
  return {
    ...identity,
    permissions: getPermissionsForRole(identity.role),
  };
}

function isCompleteIdentity(identity: CurrentUserResponse): boolean {
  return identity.user_id.trim().length > 0
    && identity.username.trim().length > 0
    && identity.role.trim().length > 0;
}

/**
 * AuthProvider 管理浏览器会话，页面只消费 CurrentUser 与 permission helper。
 *
 * 恢复链：sessionStorage token -> JWT 最小校验 -> Bearer `/users/me` -> 权限镜像。
 * 安全边界：只保存 Access Token，不保存密码、Authorization Header 或 permission 列表。
 */
export function AuthProvider({ children, initialSession }: AuthProviderProps) {
  const [accessToken, setAccessToken] = useState<string | null>(initialSession?.accessToken ?? null);
  const [currentUser, setCurrentUser] = useState<CurrentUser | null>(initialSession?.currentUser ?? null);
  const [isInitializing, setIsInitializing] = useState(initialSession === undefined);
  const [authorizationNotice, setAuthorizationNotice] = useState<string | null>(null);
  const restoreStarted = useRef(false);

  const clearSession = useCallback(() => {
    sessionStorage.removeItem(ACCESS_TOKEN_SESSION_KEY);
    setApiAccessToken(null);
    setAccessToken(null);
    setCurrentUser(null);
  }, []);

  const logout = useCallback(() => {
    clearSession();
    setAuthorizationNotice(null);
  }, [clearSession]);

  useEffect(() => {
    if (initialSession !== undefined) {
      setApiAccessToken(initialSession?.accessToken ?? null);
      return;
    }

    if (restoreStarted.current) return;
    restoreStarted.current = true;

    async function restoreSession() {
      const storedToken = sessionStorage.getItem(ACCESS_TOKEN_SESSION_KEY);
      const claims = storedToken ? parseJwtIdentity(storedToken) : null;
      if (storedToken === null || claims === null) {
        clearSession();
        setIsInitializing(false);
        return;
      }

      setApiAccessToken(storedToken);
      try {
        const identity = await getCurrentUser();
        if (
          !isCompleteIdentity(identity)
          || identity.user_id !== claims.user_id
          || identity.username !== claims.username
          || identity.role !== claims.role
        ) {
          throw new Error("JWT identity does not match CurrentUser");
        }
        setAccessToken(storedToken);
        setCurrentUser(buildCurrentUser(identity));
      } catch {
        clearSession();
      } finally {
        setIsInitializing(false);
      }
    }
    void restoreSession();
  }, [clearSession, initialSession]);

  useEffect(() => {
    setApiAuthHandlers({
      onUnauthorized: () => {
        clearSession();
        navigateTo("/login", {
          replace: true,
          state: { reason: "expired" },
        });
      },
      onForbidden: () => {
        setAuthorizationNotice("この操作を実行する権限がありません。セッションは維持されています。");
      },
    });
    return () => setApiAuthHandlers({});
  }, [clearSession]);

  const login = useCallback(async (username: string, password: string) => {
    const response = await requestLogin(username, password);
    const claims = parseJwtIdentity(response.access_token);
    if (claims === null || response.token_type.toLowerCase() !== "bearer") {
      clearSession();
      throw new Error("Invalid access token");
    }

    setApiAccessToken(response.access_token);
    try {
      const identity = await getCurrentUser();
      if (
        !isCompleteIdentity(identity)
        || identity.user_id !== claims.user_id
        || identity.username !== claims.username
        || identity.role !== claims.role
      ) {
        throw new Error("JWT identity does not match CurrentUser");
      }
      sessionStorage.setItem(ACCESS_TOKEN_SESSION_KEY, response.access_token);
      setAccessToken(response.access_token);
      setCurrentUser(buildCurrentUser(identity));
      setAuthorizationNotice(null);
    } catch (reason) {
      clearSession();
      throw reason;
    }
  }, [clearSession]);

  const value = useMemo<AuthContextValue>(() => {
    const permissions = currentUser?.permissions ?? [];
    return {
      accessToken,
      currentUser,
      isAuthenticated: currentUser !== null,
      isInitializing,
      authorizationNotice,
      login,
      logout,
      clearAuthorizationNotice: () => setAuthorizationNotice(null),
      hasPermission: (permission) => checkPermission(permissions, permission),
      hasAnyPermission: (required) => checkAnyPermission(permissions, required),
      hasAllPermissions: (required) => checkAllPermissions(permissions, required),
    };
  }, [accessToken, authorizationNotice, currentUser, isInitializing, login, logout]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (context === null) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
}
