import { FormEvent, useEffect, useRef, useState } from "react";

import { ApiClientError, createTask, getReport, subscribeToTask } from "../api";
import { PageHeader } from "../components/PageHeader";
import { StatusBanner } from "../components/StatusBanner";
import type { AnalysisMode, DisplayError, ReportResponse, TaskEvent, TaskStatus } from "../types";

const defaultQuestion = "売上と在庫の状況を分析し、市場トレンドと競合も確認してください";

const modeLabels: Record<AnalysisMode, string> = {
  hybrid: "KPI + Research",
  kpi: "KPI のみ",
  research: "Research のみ",
};

/**
 * TasksPage 负责现有 Task → SSE → Report 主链路。
 *
 * 谁调用它：
 * - `App.tsx` 在 Analysis / Tasks tab 下渲染它。
 *
 * 它调用谁：
 * - `api.ts` 中的 task 创建、SSE 订阅和 report 读取函数。
 *
 * 日本现场面试可以这样讲：
 * - 这是前端最小 workflow 页面，展示了 request、progress stream 和 final report 三段式数据流。
 */
export function TasksPage() {
  const [question, setQuestion] = useState(defaultQuestion);
  const [mode, setMode] = useState<AnalysisMode>("hybrid");
  const [taskId, setTaskId] = useState<string | null>(null);
  const [status, setStatus] = useState<TaskStatus | "idle">("idle");
  const [events, setEvents] = useState<TaskEvent[]>([]);
  const [report, setReport] = useState<ReportResponse | null>(null);
  const [error, setError] = useState<DisplayError | null>(null);
  const unsubscribeRef = useRef<(() => void) | null>(null);

  useEffect(() => () => unsubscribeRef.current?.(), []);

  function toDisplayError(reason: unknown, fallbackCode: string, fallbackMessage: string): DisplayError {
    if (reason instanceof ApiClientError) {
      return { code: reason.code, message: reason.message };
    }
    return { code: fallbackCode, message: fallbackMessage };
  }

  async function loadReport(id: string) {
    try {
      setReport(await getReport(id));
    } catch (reason) {
      setError(toDisplayError(reason, "REPORT_LOAD_ERROR", "レポート取得に失敗しました"));
    }
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    unsubscribeRef.current?.();
    setTaskId(null);
    setStatus("queued");
    setEvents([]);
    setReport(null);
    setError(null);

    try {
      const created = await createTask(question.trim(), mode);
      setTaskId(created.task_id);
      setStatus(created.status);
      // 保存取消订阅函数，防止重复提交后旧 SSE 还继续写入页面状态。
      unsubscribeRef.current = subscribeToTask(created.task_id, {
        onEvent: (taskEvent) => {
          setEvents((current) => [...current, taskEvent]);
          setStatus(taskEvent.status);
          if (taskEvent.event === "done") {
            unsubscribeRef.current?.();
            void loadReport(created.task_id);
          }
          if (taskEvent.event === "error") {
            unsubscribeRef.current?.();
            setError({
              code: taskEvent.error_code ?? "TASK_EXECUTION_ERROR",
              message: taskEvent.message,
            });
          }
        },
        onTransportError: () => setError({
          code: "SSE_CONNECTION_ERROR",
          message: "進捗ストリームが切断されました",
        }),
      });
    } catch (reason) {
      setStatus("idle");
      setError(toDisplayError(reason, "TASK_CREATE_ERROR", "タスク作成に失敗しました"));
    }
  }

  const busy = status === "queued" || status === "running";

  return (
    <>
      <PageHeader
        eyebrow="TASK WORKFLOW"
        title="Analysis / Tasks"
        description="Create a deterministic analysis task, observe SSE progress, and inspect the final generated report from the current local workflow."
      />

      <section className="workspace" aria-label="分析ワークスペース">
        <form className="task-form panel" onSubmit={submit}>
          <div className="panel-heading">
            <span>01</span>
            <h2>分析依頼</h2>
          </div>
          <label htmlFor="question">確認したい経営課題</label>
          <textarea
            id="question"
            rows={6}
            maxLength={1000}
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            disabled={busy}
          />
          <fieldset disabled={busy}>
            <legend>分析モード</legend>
            <div className="mode-grid">
              {(Object.keys(modeLabels) as AnalysisMode[]).map((value) => (
                <label className={mode === value ? "mode selected" : "mode"} key={value}>
                  <input
                    type="radio"
                    name="mode"
                    value={value}
                    checked={mode === value}
                    onChange={() => setMode(value)}
                  />
                  {modeLabels[value]}
                </label>
              ))}
            </div>
          </fieldset>
          <button type="submit" disabled={busy || question.trim().length === 0}>
            {busy ? "分析実行中…" : "分析を開始"}
          </button>
          <p className="boundary">ローカル固定データを使用。実際の経営判断には使用できません。</p>
        </form>

        <section className="timeline panel" aria-live="polite">
          <div className="panel-heading">
            <span>02</span>
            <h2>実行状態</h2>
          </div>
          <div className={`status status-${status}`}>
            <span className="status-dot" />
            {status.toUpperCase()}
          </div>
          {taskId && <p className="task-id">TASK {taskId}</p>}
          {events.length === 0 ? (
            <p className="empty">分析を開始すると、Workflow の各 Node がここに表示されます。</p>
          ) : (
            <ol className="event-list">
              {events.map((item) => (
                <li key={item.sequence}>
                  <span>{String(item.sequence).padStart(2, "0")}</span>
                  <div>
                    <strong>{item.message}</strong>
                    <small>{item.node ?? item.event}</small>
                  </div>
                </li>
              ))}
            </ol>
          )}
          {error && <StatusBanner tone="error">[{error.code}] {error.message}</StatusBanner>}
        </section>
      </section>

      <section className="report panel" aria-live="polite">
        <div className="panel-heading">
          <span>03</span>
          <h2>分析レポート</h2>
          {report && <small>{report.provider} / {new Date(report.created_at).toLocaleString("ja-JP")}</small>}
        </div>
        {report ? <pre>{report.markdown}</pre> : <p className="empty">完了したレポートがここに表示されます。</p>}
      </section>
    </>
  );
}
