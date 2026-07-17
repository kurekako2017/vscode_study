import { useEffect, useState } from "react";

import { ApiClientError, getLlmRuntime, updateLlmRuntime } from "../api";
import { PageHeader } from "../components/PageHeader";
import { StatusBanner } from "../components/StatusBanner";
import type { DisplayError, LlmProviderMode, LlmRuntimeResponse } from "../types";

/**
 * 管理员 LLM 运行时面板：只读摘要 + 切换 stub/openrouter/fallback_chain。
 * 不提交 API Key；真实模式可能产生费用，默认验收保持 stub。
 */
export function AdminLlmPage() {
  const [runtime, setRuntime] = useState<LlmRuntimeResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<DisplayError | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    void load();
  }, []);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      setRuntime(await getLlmRuntime());
    } catch (reason) {
      setError(toError(reason));
      setRuntime(null);
    } finally {
      setLoading(false);
    }
  }

  async function applyMode(mode: LlmProviderMode) {
    if (mode !== "stub") {
      const ok = window.confirm(
        [
          `切换到 ${mode}？`,
          "非 stub 模式可能产生真实外部 API 费用。",
          "密钥只能来自服务端环境变量，本页不会提交 Key。",
          "正式验收请保持 stub。",
        ].join("\n"),
      );
      if (!ok) return;
    }
    setSaving(true);
    setError(null);
    setMessage(null);
    try {
      const next = await updateLlmRuntime(mode);
      setRuntime(next);
      setMessage(`已切换为 ${next.llm_provider_mode}（repository=${next.repository_backend}）`);
    } catch (reason) {
      setError(toError(reason));
    } finally {
      setSaving(false);
    }
  }

  function toError(reason: unknown): DisplayError {
    if (reason instanceof ApiClientError) return { code: reason.code, message: reason.message };
    return { code: "LLM_ADMIN_ERROR", message: "LLM 运行时读取/切换失败" };
  }

  return (
    <>
      <PageHeader
        eyebrow="AI 管理 / Admin"
        title="LLM 运行时与成本开关"
        description="查看当前 Provider 模式。默认 stub 零费用。openrouter / fallback_chain 仅在服务端已配置密钥时可用。"
      />
      <section className="panel">
        <div className="panel-heading">
          <span>LLM</span>
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
                <dt>当前模式</dt>
                <dd>
                  <strong>{runtime.llm_provider_mode}</strong>
                </dd>
              </div>
              <div>
                <dt>Repository</dt>
                <dd>{runtime.repository_backend}</dd>
              </div>
              <div>
                <dt>Fallback 顺序</dt>
                <dd>{runtime.chain_order.join(" → ")}</dd>
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
                <dd>{runtime.local_qwen_enabled ? "enabled 标志开启" : "未开启"}</dd>
              </div>
              <div>
                <dt>Real smoke</dt>
                <dd>{runtime.run_real_llm_smoke ? "ON（异常）" : "OFF（正确）"}</dd>
              </div>
            </dl>
            <div className="action-row">
              {(["stub", "fallback_chain", "openrouter"] as LlmProviderMode[]).map((mode) => (
                <button
                  key={mode}
                  type="button"
                  className={runtime.llm_provider_mode === mode ? undefined : "secondary-button"}
                  disabled={saving || runtime.llm_provider_mode === mode}
                  onClick={() => void applyMode(mode)}
                >
                  切换到 {mode}
                </button>
              ))}
            </div>
            <ul>
              {runtime.cost_risk_notes.map((note) => (
                <li key={note}>{note}</li>
              ))}
            </ul>
            <p className="empty">{runtime.note}</p>
          </>
        )}
      </section>
    </>
  );
}
