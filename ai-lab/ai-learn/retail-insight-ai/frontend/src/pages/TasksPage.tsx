import { FormEvent, useEffect, useRef, useState } from "react";

import { ApiClientError, createTask, getReport, subscribeToTask } from "../api";
import { BusinessLearningPanel } from "../components/BusinessLearningPanel";
import { PageHeader } from "../components/PageHeader";
import { StatusBanner } from "../components/StatusBanner";
import type { AnalysisMode, DisplayError, ReportResponse, TaskEvent, TaskStatus } from "../types";
import type { RecordLearningEvent } from "../learning/learningTypes";

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
interface TasksPageProps {
  onLearningEvent?: RecordLearningEvent;
}

export function TasksPage({ onLearningEvent }: TasksPageProps = {}) {
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
      const nextReport = await getReport(id);
      setReport(nextReport);
      onLearningEvent?.({ eventName: "loadReport()", apiMethod: "GET", apiPath: `/api/tasks/${id}/report`, apiStatus: "200 OK", stateChanges: ["report: null → response", "status: completed"], backendFlow: ["tasks.py get_report()", "TaskService.get_report()", "InMemoryReportRepository.get()"] });
    } catch (reason) {
      setError(toDisplayError(reason, "REPORT_LOAD_ERROR", "レポート取得に失敗しました"));
      onLearningEvent?.({ eventName: "loadReport()", apiMethod: "GET", apiPath: `/api/tasks/${id}/report`, apiStatus: "Backend error / 409 when unfinished", stateChanges: ["error: null → error"], backendFlow: ["tasks.py get_report()", "TaskService.get_report()"] });
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
      onLearningEvent?.({ eventName: "submit()", apiMethod: "POST", apiPath: "/api/tasks", apiStatus: "202 Accepted", stateChanges: [`taskId: null → ${created.task_id}`, `status: queued`, "events/report: 清空"], backendFlow: ["tasks.py create_task()", "TaskService.create_task()", "InMemoryTaskRepository.create()", "BackgroundTasks.add_task()", "TaskService.run_task()", "AnalysisWorkflow.stream()"], note: "202 仅表示任务已受理；报告会在 BackgroundTasks 的 Workflow 完成后生成。" });
      // 保存取消订阅函数，防止重复提交后旧 SSE 还继续写入页面状态。
      unsubscribeRef.current = subscribeToTask(created.task_id, {
        onEvent: (taskEvent) => {
          setEvents((current) => [...current, taskEvent]);
          setStatus(taskEvent.status);
          if (taskEvent.event === "done") {
            unsubscribeRef.current?.();
            onLearningEvent?.({ eventName: "subscribeToTask() done", apiMethod: "GET", apiPath: `/api/tasks/${created.task_id}/events`, apiStatus: "SSE done", stateChanges: ["status: running → completed", "events: 追加 done", "下一步 loadReport()"], backendFlow: ["tasks.py get_task_events()", "stream_task_events()", "EventRepository", "TaskService.run_task()"] });
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
      onLearningEvent?.({ eventName: "submit()", apiMethod: "POST", apiPath: "/api/tasks", apiStatus: "Backend error", stateChanges: ["status: queued → idle", "error: null → error"], backendFlow: ["tasks.py create_task()", "TaskService.create_task()"] });
    }
  }

  const busy = status === "queued" || status === "running";

  return (
    <>
      <PageHeader
        eyebrow="分析ワークフロー"
        title="分析依頼"
        description="分析依頼を作成し、SSE の進捗と現在のローカルワークフローが生成したレポートを確認します。"
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

      <BusinessLearningPanel
        pageName="分析依頼"
        purpose="关东地区饮料分类销售下降时，创建经营分析任务并确认报告生成过程。"
        scenario="内部资料已登记后，经营企划人员输入“関東地域の飲料カテゴリの売上減少を分析してください”，以 hybrid 模式取得 KPI 与静态调研结果。"
        prerequisites="Backend 已启动；任务问题不能为空。当前报告使用本地固定数据，不会自动引用 Documents 或 RAG 的结果。"
        relationship="本页产生 task_id 和 report。任务完成后，需要用户手动复制 task_id 到承認管理提交审批；与 RAG検索 当前未自动连接。"
        journey={{ previous: "RAG検索", current: "3 / 4 分析依頼", completion: "任务达到 completed 并取得 report。", next: "承認管理", recommendedCase: "APR-BIZ-001", transferredObjects: "task_id、report", connection: "当前手动复制 task_id。" }}
        cases={[
          { id: "TASK-BIZ-001", group: "标准业务 Case", purpose: "正常创建关东饮料销售下降分析。", input: "输入业务问题，选择 hybrid，点击「分析を開始」。", expected: "收到 queued 状态，SSE 显示 route／kpi／research／report，最终显示 Markdown 报告。" },
          { id: "TASK-BIZ-002", group: "异常与维护测试 Case", purpose: "确认必填校验。", input: "清空问题输入框。", expected: "「分析を開始」不可点击，不发送 POST 请求。" },
          { id: "TASK-BIZ-003", group: "异常与维护测试 Case", purpose: "确认不存在 task 的读取错误。", input: "使用不存在 task_id 请求报告。", expected: "Backend 返回实际 404；页面当前只在已创建任务完成后读取报告。" },
          { id: "TASK-BIZ-004", group: "异常与维护测试 Case", purpose: "确认未完成报告的业务错误。", input: "在 queued／running 阶段读取 report。", expected: "Backend 的 get_report 以实际 409 表示报告尚未生成。" },
          { id: "TASK-BIZ-005", group: "异常与维护测试 Case", purpose: "确认重新分析会清理旧页面状态。", input: "任务完成后再次点击「分析を開始」。", expected: "旧 task_id、SSE 列表和报告先清空，再订阅新任务；旧 SSE 会关闭。" },
        ]}
        flows={[
          {
            title: "创建任务与后台执行",
            api: "POST /api/tasks",
            frontend: ["frontend/src/pages/TasksPage.tsx submit()", "frontend/src/api.ts createTask()", "setTaskId / setStatus", "subscribeToTask()"],
            backend: ["backend/app/api/tasks.py create_task()", "TaskService.create_task()", "InMemoryTaskRepository.create()", "BackgroundTasks.add_task()", "TaskService.run_task()", "AnalysisWorkflow.stream()", "FixedKPIWorkflow / ResearchAgent / ReportGenerator"],
            note: "HTTP 202 只表示已受理；实际分析在 BackgroundTasks 中执行。",
          },
          {
            title: "SSE 与最终报告",
            api: "GET /api/tasks/{task_id}/events；GET /api/tasks/{task_id}/report",
            frontend: ["subscribeToTask()", "onEvent setEvents / setStatus", "done 后 loadReport()", "getReport()", "setReport"],
            backend: ["tasks.py get_task_events()", "stream_task_events()", "EventRepository", "tasks.py get_report()", "TaskService.get_report()", "InMemoryReportRepository.get()"],
            note: "SSE 是事件流，不使用普通 JSON envelope；报告接口返回已完成的 report。",
          },
        ]}
      />
    </>
  );
}
