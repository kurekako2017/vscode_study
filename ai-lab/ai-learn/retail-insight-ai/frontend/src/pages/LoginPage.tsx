import { type FormEvent, useRef, useState } from "react";

import { ApiClientError } from "../api";
import { useAuth } from "../auth/AuthContext";
import { navigateTo } from "../routing/navigation";

const protectedPaths = new Set([
  "/dashboard",
  "/documents",
  "/rag",
  "/analysis",
  "/approval",
]);

function getReturnTarget(): string {
  const candidate = (window.history.state as { returnTo?: unknown } | null)?.returnTo;
  return typeof candidate === "string" && protectedPaths.has(candidate) ? candidate : "/dashboard";
}

/**
 * LoginPage 只收集 username/password 并调用 AuthContext。
 * 密码只存在于受控输入的短生命周期 state，成功或失败后都不会写入 storage 或日志。
 */
export function LoginPage() {
  const auth = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const loginInFlight = useRef(false);
  const expired = (window.history.state as { reason?: unknown } | null)?.reason === "expired";

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (loginInFlight.current || username.trim().length === 0 || password.length === 0) return;
    loginInFlight.current = true;
    setIsSubmitting(true);
    setErrorMessage(null);
    try {
      await auth.login(username.trim(), password);
      setPassword("");
      navigateTo(getReturnTarget(), { replace: true });
    } catch (reason) {
      setPassword("");
      setErrorMessage(
        reason instanceof ApiClientError && reason.code === "NETWORK_ERROR"
          ? "認証サービスに接続できません。しばらくしてから再試行してください。"
          : "ユーザー名またはパスワードを確認してください。",
      );
    } finally {
      loginInFlight.current = false;
      setIsSubmitting(false);
    }
  }

  return (
    <main className="login-shell">
      <section className="panel login-panel">
        <p className="eyebrow">ERIP Enterprise Access</p>
        <h1>ログイン</h1>
        <p>JWT 認証後、Backend が確認した CurrentUser とロール権限で画面を構成します。</p>
        {expired && <p className="status-banner warning" role="status">セッションの有効期限が切れました。再度ログインしてください。</p>}
        {errorMessage && <p className="status-banner error" role="alert">{errorMessage}</p>}
        <form className="stack-form" onSubmit={submit}>
          <label htmlFor="login-username">ユーザー名</label>
          <input
            id="login-username"
            autoComplete="username"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            disabled={isSubmitting}
            required
          />
          <label htmlFor="login-password">パスワード</label>
          <input
            id="login-password"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            disabled={isSubmitting}
            required
          />
          <button type="submit" disabled={isSubmitting || username.trim().length === 0 || password.length === 0}>
            {isSubmitting ? "ログイン中…" : "ログイン"}
          </button>
        </form>
      </section>
    </main>
  );
}
