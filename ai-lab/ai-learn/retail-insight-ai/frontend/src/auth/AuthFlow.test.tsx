import { StrictMode } from "react";
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import App from "../App";
import { setApiAccessToken } from "../api";
import { ACCESS_TOKEN_SESSION_KEY } from "./AuthContext";
import {
  ADMIN_SESSION,
  EMPLOYEE_SESSION,
  MANAGER_SESSION,
  buildTestJwt,
  buildTestSession,
} from "../test/auth-test-helpers";
import { jsonResponse } from "../test/page-test-helpers";

function loginSuccess(token: string, role: string) {
  return jsonResponse({
    success: true,
    request_id: "request-login",
    data: { access_token: token, token_type: "bearer", expires_in: 1800 },
    error: null,
  }, 200);
}

function currentUser(role: string) {
  return jsonResponse({
    success: true,
    request_id: "request-current-user",
    data: {
      user_id: `user-${role}`,
      username: role,
      role,
    },
    error: null,
  }, 200);
}

function emptyDocumentList(status = 200) {
  return jsonResponse({
    success: status < 400,
    request_id: "request-documents",
    data: status < 400 ? { items: [], next_cursor: null } : null,
    error: status < 400 ? null : {
      code: status === 401 ? "unauthorized" : "forbidden",
      message: status === 401 ? "Unauthorized" : "Forbidden",
      detail: {},
    },
  }, status);
}

describe("Frontend authentication and RBAC flow", () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("redirects an unauthenticated direct URL to login and preserves the original target", async () => {
    window.history.replaceState(null, "", "/documents");
    render(<App />);

    expect(await screen.findByRole("heading", { name: "ログイン" })).toBeInTheDocument();
    expect(window.location.pathname).toBe("/login");
    expect(window.history.state).toMatchObject({ returnTo: "/documents" });
  });

  it("logs in once, stores only the access token in sessionStorage, and returns to the target", async () => {
    const token = buildTestJwt("employee");
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(loginSuccess(token, "employee"))
      .mockResolvedValueOnce(currentUser("employee"))
      .mockResolvedValueOnce(emptyDocumentList());
    vi.stubGlobal("fetch", fetchMock);
    window.history.replaceState(null, "", "/documents");
    render(<App />);

    await screen.findByRole("heading", { name: "ログイン" });
    fireEvent.change(screen.getByLabelText("ユーザー名"), { target: { value: "employee" } });
    fireEvent.change(screen.getByLabelText("パスワード"), { target: { value: "secret-password" } });
    fireEvent.click(screen.getByRole("button", { name: "ログイン" }));

    expect(await screen.findByRole("heading", { name: "文書管理" })).toBeInTheDocument();
    expect(window.location.pathname).toBe("/documents");
    expect(sessionStorage.getItem(ACCESS_TOKEN_SESSION_KEY)).toBe(token);
    expect(localStorage.length).toBe(0);
    expect(JSON.stringify({ ...sessionStorage })).not.toContain("secret-password");

    const loginHeaders = new Headers((fetchMock.mock.calls[0][1] as RequestInit).headers);
    const meHeaders = new Headers((fetchMock.mock.calls[1][1] as RequestInit).headers);
    expect(loginHeaders.has("Authorization")).toBe(false);
    expect(meHeaders.get("Authorization")).toBe(`Bearer ${token}`);
  });

  it("shows a generic login failure and never stores a token", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse({
      success: false,
      request_id: "request-login-failure",
      data: null,
      error: { code: "invalid_credentials", message: "Invalid credentials", detail: {} },
    }, 401)));
    window.history.replaceState(null, "", "/login");
    render(<App />);

    fireEvent.change(screen.getByLabelText("ユーザー名"), { target: { value: "employee" } });
    fireEvent.change(screen.getByLabelText("パスワード"), { target: { value: "wrong-password" } });
    fireEvent.click(screen.getByRole("button", { name: "ログイン" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("ユーザー名またはパスワードを確認してください");
    expect(sessionStorage.getItem(ACCESS_TOKEN_SESSION_KEY)).toBeNull();
    expect(screen.getByLabelText("パスワード")).toHaveValue("");
  });

  it("prevents duplicate login requests while authentication is in flight", async () => {
    const token = buildTestJwt("employee");
    let resolveLogin: ((response: Response) => void) | undefined;
    const fetchMock = vi.fn()
      .mockImplementationOnce(() => new Promise<Response>((resolve) => {
        resolveLogin = resolve;
      }))
      .mockResolvedValueOnce(currentUser("employee"));
    vi.stubGlobal("fetch", fetchMock);
    window.history.replaceState(null, "", "/login");
    render(<App />);

    fireEvent.change(screen.getByLabelText("ユーザー名"), { target: { value: "employee" } });
    fireEvent.change(screen.getByLabelText("パスワード"), { target: { value: "password" } });
    const button = screen.getByRole("button", { name: "ログイン" });
    fireEvent.click(button);
    fireEvent.click(button);

    expect(fetchMock).toHaveBeenCalledTimes(1);
    resolveLogin?.(loginSuccess(token, "employee"));
    expect(await screen.findByText("权限来自前端冻结 Registry")).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("restores a valid refresh session through users/me", async () => {
    const token = buildTestJwt("manager");
    sessionStorage.setItem(ACCESS_TOKEN_SESSION_KEY, token);
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(currentUser("manager")));
    window.history.replaceState(null, "", "/dashboard");
    render(<App />);

    expect((await screen.findAllByText("manager")).length).toBeGreaterThan(0);
    expect(screen.getByText("前端冻结 Registry（9 项）")).toBeInTheDocument();
    expect(window.location.pathname).toBe("/dashboard");
  });

  it("does not duplicate refresh identity requests under React StrictMode", async () => {
    const token = buildTestJwt("admin");
    const fetchMock = vi.fn().mockResolvedValue(currentUser("admin"));
    sessionStorage.setItem(ACCESS_TOKEN_SESSION_KEY, token);
    vi.stubGlobal("fetch", fetchMock);
    window.history.replaceState(null, "", "/dashboard");

    render(<StrictMode><App /></StrictMode>);

    expect(await screen.findByLabelText("当前会话")).toHaveTextContent("admin");
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("rejects an expired refresh token before making a backend request", async () => {
    const fetchMock = vi.fn();
    sessionStorage.setItem(
      ACCESS_TOKEN_SESSION_KEY,
      buildTestJwt("employee", "employee", "user-employee", Math.floor(Date.now() / 1000) - 1),
    );
    vi.stubGlobal("fetch", fetchMock);
    window.history.replaceState(null, "", "/dashboard");
    render(<App />);

    expect(await screen.findByRole("heading", { name: "ログイン" })).toBeInTheDocument();
    expect(sessionStorage.getItem(ACCESS_TOKEN_SESSION_KEY)).toBeNull();
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("logs out by clearing the session and returning to login", async () => {
    window.history.replaceState(null, "", "/dashboard");
    render(<App initialSession={ADMIN_SESSION} />);

    fireEvent.click(screen.getByRole("button", { name: "ログアウト" }));

    expect(await screen.findByRole("heading", { name: "ログイン" })).toBeInTheDocument();
    expect(sessionStorage.getItem(ACCESS_TOKEN_SESSION_KEY)).toBeNull();
    expect(window.location.pathname).toBe("/login");
  });

  it("redirects an already authenticated user away from login", async () => {
    window.history.replaceState(null, "", "/login");
    render(<App initialSession={MANAGER_SESSION} />);

    await waitFor(() => expect(window.location.pathname).toBe("/dashboard"));
    expect(screen.getByRole("heading", { name: "Enterprise Retail Intelligence Platform", level: 1 })).toBeInTheDocument();
  });

  it("keeps unknown roles authenticated but fail-closed for permission routes", async () => {
    window.history.replaceState(null, "", "/documents");
    render(<App initialSession={buildTestSession("unknown")} />);

    expect(screen.getByRole("alert")).toHaveTextContent("アクセス権限がありません");
    expect(within(screen.getByRole("navigation", { name: "主要ページ" })).getAllByRole("button"))
      .toHaveLength(1);
  });

  it("shows employee owner approval access without review controls", () => {
    window.history.replaceState(null, "", "/approval");
    render(<App initialSession={EMPLOYEE_SESSION} />);

    expect(screen.getByLabelText("Approval ID")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "承認依頼を送信" })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "承認" })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "却下" })).not.toBeInTheDocument();
    expect(screen.queryByText("監査ログ")).not.toBeInTheDocument();
    expect(screen.queryByText("セキュリティ管理")).not.toBeInTheDocument();
  });

  it("shows manager review navigation and keeps security management absent", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse({
      success: true,
      request_id: "request-approval-list",
      data: { items: [], next_cursor: null },
      error: null,
    }, 200)));
    window.history.replaceState(null, "", "/approval");
    render(<App initialSession={MANAGER_SESSION} />);

    expect(await screen.findByRole("heading", { name: "承認待ち一覧" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "絞り込む" })).toBeInTheDocument();
    expect(screen.queryByText("セキュリティ管理")).not.toBeInTheDocument();
  });

  it("gives admin the complete frozen permission set without adding nonexistent pages", () => {
    window.history.replaceState(null, "", "/dashboard");
    render(<App initialSession={ADMIN_SESSION} />);

    expect(screen.getByText("前端冻结 Registry（10 项）")).toBeInTheDocument();
    expect(within(screen.getByRole("navigation", { name: "主要ページ" })).getAllByRole("button")).toHaveLength(6);
    expect(screen.queryByText("監査ログ")).not.toBeInTheDocument();
    expect(screen.queryByText("セキュリティ管理")).not.toBeInTheDocument();
  });

  it("clears the authenticated session and redirects once after a protected 401", async () => {
    setApiAccessToken("expired-token");
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(emptyDocumentList(401)));
    window.history.replaceState(null, "", "/documents");
    render(<App initialSession={{ ...EMPLOYEE_SESSION, accessToken: "expired-token" }} />);

    expect(await screen.findByRole("heading", { name: "ログイン" })).toBeInTheDocument();
    expect(window.history.state).toMatchObject({ reason: "expired" });
    expect(sessionStorage.getItem(ACCESS_TOKEN_SESSION_KEY)).toBeNull();
  });

  it("preserves the authenticated page and shows a non-destructive notice after 403", async () => {
    setApiAccessToken("valid-token");
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(emptyDocumentList(403)));
    window.history.replaceState(null, "", "/documents");
    render(<App initialSession={{ ...EMPLOYEE_SESSION, accessToken: "valid-token" }} />);

    expect(await screen.findByText("この操作を実行する権限がありません。セッションは維持されています。")).toBeInTheDocument();
    expect(window.location.pathname).toBe("/documents");
    expect(within(screen.getByLabelText("当前会话")).getAllByText("employee")).toHaveLength(2);
  });
});
