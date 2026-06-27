import { FormEvent, useEffect, useRef, useState } from "react";

import { ApiClientError, createTask, getReport, subscribeToTask } from "./api";
import type { AnalysisMode, DisplayError, ReportResponse, TaskEvent, TaskStatus } from "./types";

const defaultQuestion = "売上と在庫の状況を分析し、市場トレンドと競合も確認してください";

const modeLabels: Record<AnalysisMode, string> = {
  hybrid: "KPI + Research",
  kpi: "KPI のみ",
  research: "Research のみ",
};

/**
 * 页面根组件：集中演示“提交任务 -> 接收 SSE -> 加载报告”的完整 React 数据流。
 *
 * 教学版暂不拆成多个组件，便于初学者在一个文件中看到状态如何驱动页面；各视觉区域
 * 分别对应未来可拆出的 TaskForm、TaskTimeline、ReportViewer 和 ErrorPanel。
 */
export default function App() {
  const [question, setQuestion] = useState(defaultQuestion);
  const [mode, setMode] = useState<AnalysisMode>("hybrid");
  const [taskId, setTaskId] = useState<string | null>(null);
  const [status, setStatus] = useState<TaskStatus | "idle">("idle");
  const [events, setEvents] = useState<TaskEvent[]>([]);
  const [report, setReport] = useState<ReportResponse | null>(null);
  const [error, setError] = useState<DisplayError | null>(null);
  const unsubscribeRef = useRef<(() => void) | null>(null);

  // EventSource 是浏览器外部资源；组件卸载时必须关闭，避免页面离开后仍接收事件。
  useEffect(() => () => unsubscribeRef.current?.(), []);

  /** 任务完成后单独读取最终报告，使 SSE 只承担进度通知而不传输大正文。 */
  async function loadReport(id: string) {
    try {
      setReport(await getReport(id));
    } catch (reason) {
      setError(
        reason instanceof ApiClientError
          ? { code: reason.code, message: reason.message }
          : { code: "REPORT_LOAD_ERROR", message: "レポート取得に失敗しました" },
      );
    }
  }

  /** 重置旧页面状态、创建任务，并订阅该任务后续的状态事件。 */
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
      // 保存取消订阅函数，重复提交或组件卸载时可以关闭旧连接。
      unsubscribeRef.current = subscribeToTask(created.task_id, {
        onEvent: (taskEvent) => {
          // 使用函数式 setState，确保连续到达的 SSE 不会覆盖前一个事件。
          setEvents((current) => [...current, taskEvent]);
          setStatus(taskEvent.status);
          if (taskEvent.event === "done") {
            unsubscribeRef.current?.();
            // 事件回调不是 async；void 明确表示这里启动异步加载但不阻塞回调。
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
      setError(
        reason instanceof ApiClientError
          ? { code: reason.code, message: reason.message }
          : { code: "TASK_CREATE_ERROR", message: "タスク作成に失敗しました" },
      );
    }
  }

  const busy = status === "queued" || status === "running";

  return (
    <main className="shell">
      <header className="hero">
        <p className="eyebrow">RETAIL OPERATIONS / LOCAL STATIC ENVIRONMENT</p>
        <h1>Retail Insight AI</h1>
        <p className="lead">KPI の確定計算と調査結果を、監査可能な一つの分析レポートへ。</p>
      </header>

      <section className="workspace" aria-label="分析ワークスペース">
        {/* TaskForm：收集问题与模式，busy 时禁用输入以避免同一页面重复提交。 */}
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

        {/* TaskTimeline：aria-live 让辅助技术感知异步状态变化。 */}
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
          {/* ErrorPanel：role=alert 让错误不仅依赖颜色表达。 */}
          {error && <div className="error" role="alert">[{error.code}] {error.message}</div>}
        </section>
      </section>

      {/* ReportViewer：当前用 pre 保留 Backend Markdown 的原始换行和格式。 */}
      <section className="report panel" aria-live="polite">
        <div className="panel-heading">
          <span>03</span>
          <h2>分析レポート</h2>
          {report && <small>{report.provider} / {new Date(report.created_at).toLocaleString("ja-JP")}</small>}
        </div>
        {report ? <pre>{report.markdown}</pre> : <p className="empty">完了したレポートがここに表示されます。</p>}
      </section>
    </main>
  );
}
