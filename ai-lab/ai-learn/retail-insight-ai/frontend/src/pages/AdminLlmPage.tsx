import { useEffect, useState } from "react";

import { ApiClientError, getAiRuntime, patchAiRuntime } from "../api";
import { PageHeader } from "../components/PageHeader";
import { StatusBanner } from "../components/StatusBanner";
import type { AiRuntimeResponse, DisplayError, LlmProviderMode } from "../types";

/**
 * 管理员 AI Runtime 面板：PostgreSQL 持久化 mode / kill_switch。
 * 不提交 API Key；Stub→Real 需 confirmation_text=ENABLE_REAL_LLM。
 */
export function AdminLlmPage() {
  const [runtime, setRuntime] = useState<AiRuntimeResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<DisplayError | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [confirmationText, setConfirmationText] = useState("");

  useEffect(() => {
    void load();
  }, []);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      setRuntime(await getAiRuntime());
    } catch (reason) {
      setError(toError(reason));
      setRuntime(null);
    } finally {
      setLoading(false);
    }
  }

  async function applyMode(mode: LlmProviderMode) {
    if (!runtime) return;
    if (mode !== "stub") {
      const ok = window.confirm(
        [
          `切换到 ${mode}？`,
          "非 stub 模式可能产生真实外部 API 费用。",
          "密钥只能来自服务端环境变量，本页不会提交 Key。",
          `二次确认文案必须为：${runtime.confirmation_text_required_for_real}`,
          "正式验收请保持 stub。",
        ].join("\n"),
      );
      if (!ok) return;
    }
    setSaving(true);
    setError(null);
    setMessage(null);
    try {
      const next = await patchAiRuntime({
        mode,
        expected_version: runtime.version,
        confirmed: true,
        confirmation_text:
          mode !== "stub" ? confirmationText || runtime.confirmation_text_required_for_real : undefined,
      });
      setRuntime(next);
      setMessage(
        `已切换 configured=${next.configured_mode} / effective=${next.effective_mode} (v${next.version})`,
      );
    } catch (reason) {
      setError(toError(reason));
    } finally {
      setSaving(false);
    }
  }

  async function toggleKillSwitch(next: boolean) {
    if (!runtime) return;
    const ok = window.confirm(
      next
        ? "开启 Kill Switch？将强制 effective_mode=stub，阻断真实 Provider 调用。"
        : "关闭 Kill Switch？将恢复 configured_mode（若为真实模式可能产生费用）。",
    );
    if (!ok) return;
    setSaving(true);
    setError(null);
    setMessage(null);
    try {
      const nextRuntime = await patchAiRuntime({
        kill_switch: next,
        expected_version: runtime.version,
        confirmed: true,
        confirmation_text:
          !next && runtime.configured_mode !== "stub"
            ? confirmationText || runtime.confirmation_text_required_for_real
            : undefined,
      });
      setRuntime(nextRuntime);
      setMessage(`Kill Switch = ${nextRuntime.kill_switch ? "ON" : "OFF"} (v${nextRuntime.version})`);
    } catch (reason) {
      setError(toError(reason));
    } finally {
      setSaving(false);
    }
  }

  function toError(reason: unknown): DisplayError {
    if (reason instanceof ApiClientError) return { code: reason.code, message: reason.message };
    return { code: "AI_RUNTIME_ERROR", message: "AI Runtime 读取/切换失败" };
  }

  return (
    <>
      <PageHeader
        eyebrow="AI 管理 / Admin"
        title="AI Runtime 与成本开关"
        description="PostgreSQL 持久化 mode / kill_switch / version。默认 stub 零费用。API Key 永不进入数据库或响应。"
      />
      <section className="panel">
        <div className="panel-heading">
          <span>AI Runtime</span>
          <h2>运行时状态</h2>
          <button type="button" className="secondary-button" onClick={() => void load()} disabled={loading || saving}>
            刷新
          </button>
        </div>
        {message && <StatusBanner tone="success">{message}</StatusBanner>}
        {error && <StatusBanner tone="error">[{error.code}] {error.message}</StatusBanner>}
        {loading || !runtime ? (
          <p className="empty">读取中…</p>
        ) : (
          <>
            <dl className="detail-grid result-meta-grid">
              <div>
                <dt>Effective mode</dt>
                <dd>
                  <strong>{runtime.effective_mode}</strong>
                </dd>
              </div>
              <div>
                <dt>Configured mode</dt>
                <dd>{runtime.configured_mode}</dd>
              </div>
              <div>
                <dt>Real calls</dt>
                <dd>{runtime.real_calls_enabled ? "enabled" : "disabled"}</dd>
              </div>
              <div>
                <dt>Kill Switch</dt>
                <dd>{runtime.kill_switch ? "ON" : "OFF"}</dd>
              </div>
              <div>
                <dt>Version</dt>
                <dd>{runtime.version}</dd>
              </div>
              <div>
                <dt>Updated by</dt>
                <dd>{runtime.updated_by.username ?? "—"}</dd>
              </div>
              <div>
                <dt>Updated at</dt>
                <dd>{new Date(runtime.updated_at).toLocaleString("ja-JP")}</dd>
              </div>
              <div>
                <dt>Repository</dt>
                <dd>{runtime.repository_backend}</dd>
              </div>
              <div>
                <dt>Fallback 顺序</dt>
                <dd>{runtime.fallback_order.join(" → ")}</dd>
              </div>
              <div>
                <dt>low / high 模型</dt>
                <dd>
                  {runtime.low_cost_model} / {runtime.high_quality_model}
                </dd>
              </div>
              <div>
                <dt>Timeout</dt>
                <dd>
                  {runtime.timeout_seconds}s / total {runtime.total_timeout_seconds}s
                </dd>
              </div>
              <div>
                <dt>OpenRouter Key</dt>
                <dd>{runtime.openrouter_key_configured ? "已配置" : "未配置"}</dd>
              </div>
              <div>
                <dt>NVIDIA Key</dt>
                <dd>{runtime.nvidia_key_configured ? "已配置" : "未配置"}</dd>
              </div>
              <div>
                <dt>Gemini Key</dt>
                <dd>{runtime.gemini_key_configured ? "已配置" : "未配置"}</dd>
              </div>
              <div>
                <dt>Local Qwen</dt>
                <dd>{runtime.local_qwen_enabled ? "enabled" : "未开启"}</dd>
              </div>
              <div>
                <dt>Real smoke</dt>
                <dd>{runtime.run_real_llm_smoke ? "ON（异常）" : "OFF（正确）"}</dd>
              </div>
            </dl>

            <div className="subheading">
              <strong>Provider readiness</strong>
            </div>
            <ul>
              {runtime.provider_readiness.map((item) => (
                <li key={item.name}>
                  {item.name}: {item.ready ? "ready" : "not ready"}
                  {item.key_configured ? " / key=yes" : " / key=no"}
                </li>
              ))}
            </ul>

            <div className="subheading">
              <strong>安全预算摘要</strong>
            </div>
            <ul>
              {Object.entries(runtime.budget_summary).map(([key, value]) => (
                <li key={key}>
                  {key}: {value}
                </li>
              ))}
            </ul>

            <label htmlFor="confirm-text">Stub→Real confirmation_text</label>
            <input
              id="confirm-text"
              value={confirmationText}
              placeholder={runtime.confirmation_text_required_for_real}
              onChange={(event) => setConfirmationText(event.target.value)}
              disabled={saving}
            />

            <div className="action-row">
              {(["stub", "fallback_chain", "openrouter"] as LlmProviderMode[]).map((mode) => (
                <button
                  key={mode}
                  type="button"
                  className={runtime.configured_mode === mode ? undefined : "secondary-button"}
                  disabled={saving || runtime.configured_mode === mode}
                  onClick={() => void applyMode(mode)}
                >
                  切换到 {mode}
                </button>
              ))}
              <button
                type="button"
                className="secondary-button"
                disabled={saving}
                onClick={() => void toggleKillSwitch(!runtime.kill_switch)}
              >
                {runtime.kill_switch ? "关闭 Kill Switch" : "开启 Kill Switch"}
              </button>
            </div>
            <p className="empty">{runtime.note}</p>
          </>
        )}
      </section>
    </>
  );
}
