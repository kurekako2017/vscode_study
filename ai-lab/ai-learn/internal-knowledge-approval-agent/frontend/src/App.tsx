/**
 * 页面职责：承载问题提交、SSE 时间线、人工审批列表和最终报告四个视图。
 * 谁调用它：main.tsx 把 App 挂载到浏览器 DOM；用户操作再调用 api.ts。
 * 它调用谁：HTTP API、EventSource SSE，以及 React 的 state/effect hooks。
 * 输入：表单、导航和 Approve/Reject 点击；输出：可见状态、错误提示和报告。
 * 为什么需要这一层：把用户交互状态集中在一个教学页面，便于沿完整业务链阅读。
 * 初学者重点：view 控制画面，status/events 表示进度，watch 管理 SSE 生命周期。
 * 日本现场面试：可说明 UI 不是事实来源；刷新后仍应通过 Backend 状态与事件恢复。
 * 企业级替换：拆为 feature 组件并引入路由/查询缓存，但审批权限必须由 Backend 校验。
 */

import { FormEvent, useEffect, useRef, useState } from "react";

import { ApiClientError, createQuestion, decideApproval, getReport, listApprovals, subscribeQuestion } from "./api";
import type { Approval, QuestionEvent, Report } from "./types";

type View = "submit" | "status" | "approvals" | "result";

const defaultQuestion = "個人情報を含む障害ログの共有手順を確認したい";

export default function App() {
  // 页面状态按职责分组理解：导航、问题标识、Workflow 状态、事件、审批、报告和错误。
  const [view, setView] = useState<View>("submit");
  const [question, setQuestion] = useState(defaultQuestion);
  const [questionId, setQuestionId] = useState<string | null>(null);
  const [status, setStatus] = useState("idle");
  const [events, setEvents] = useState<QuestionEvent[]>([]);
  const [approvals, setApprovals] = useState<Approval[]>([]);
  const [report, setReport] = useState<Report | null>(null);
  const [error, setError] = useState<string | null>(null);
  const unsubscribe = useRef<(() => void) | null>(null);

  // 组件卸载时关闭 EventSource，避免离开页面后仍保留网络连接和回调。
  useEffect(() => () => unsubscribe.current?.(), []);

  async function refreshApprovals() {
    // 审批列表是 Backend 的持久事实；进入审批页或点击更新时重新查询。
    try {
      setApprovals(await listApprovals());
    } catch (reason) {
      showError(reason);
    }
  }

  useEffect(() => {
    if (view === "approvals") void refreshApprovals();
  }, [view]);

  function showError(reason: unknown) {
    // 已知 API 错误显示稳定 error code；未知异常不暴露内部堆栈或敏感信息。
    setError(reason instanceof ApiClientError ? `[${reason.code}] ${reason.message}` : "[UNEXPECTED_ERROR] 処理に失敗しました");
  }

  function watch(id: string) {
    // 同一时间只保留一个 SSE 订阅。返回 completed/rejected/error 后主动关闭连接。
    unsubscribe.current?.();
    unsubscribe.current = subscribeQuestion(
      id,
      (item) => {
        // 函数式更新防止连续 SSE 覆盖前一条事件。
        setEvents((current) => [...current, item]);
        setStatus(item.status);
        if (item.event === "approval_required") {
          // 高风险问题暂停在审批页；Backend 状态而不是前端关键词决定是否审批。
          setView("approvals");
        } else if (item.event === "completed") {
          // completed 只表示报告已持久化，再通过独立 Report API 获取正式内容。
          unsubscribe.current?.();
          void getReport(id).then((value) => {
            setReport(value);
            setView("result");
          }).catch(showError);
        } else if (item.event === "rejected" || item.event === "error") {
          // rejected 是业务决定，error 是执行失败；二者都是当前 SSE 的终止事件。
          unsubscribe.current?.();
          if (item.event === "rejected") setView("status");
          else setError(`[${item.error_code ?? "WORKFLOW_ERROR"}] ${item.message}`);
        }
      },
      () => setError("[SSE_CONNECTION_ERROR] 進捗接続が切断されました"),
    );
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    // 提交流程：清理旧页面状态 → POST Question → 切换状态页 → 订阅该问题的 SSE。
    event.preventDefault();
    setError(null);
    setEvents([]);
    setReport(null);
    setStatus("received");
    try {
      const created = await createQuestion(question.trim());
      setQuestionId(created.question_id);
      setStatus(created.status);
      setView("status");
      watch(created.question_id);
    } catch (reason) {
      setStatus("idle");
      showError(reason);
    }
  }

  async function decide(item: Approval, decision: "approve" | "reject") {
    // 决定流程：先订阅恢复事件，再 POST 审批，避免漏掉执行很快的 approved/completed。
    setError(null);
    setQuestionId(item.question_id);
    setStatus(decision === "approve" ? "approved" : "rejected");
    // 页面刷新后可能没有旧 SSE，决定前重新订阅保证能看到恢复事件。
    watch(item.question_id);
    try {
      await decideApproval(item.question_id, decision);
      setView("status");
      await refreshApprovals();
    } catch (reason) {
      unsubscribe.current?.();
      showError(reason);
    }
  }

  return (
    <main className="shell">
      <header className="hero">
        <p className="eyebrow">INTERNAL KNOWLEDGE / CONTROLLED ANSWERS</p>
        <h1>社内文書検索・承認ワークフローAIエージェント</h1>
        <p>固定ローカル資料と明示的な承認フローで、回答の根拠と責任を管理します。</p>
      </header>

      <nav aria-label="主要画面">
        <button onClick={() => setView("submit")} className={view === "submit" ? "active" : ""}>質問提出</button>
        <button onClick={() => setView("approvals")} className={view === "approvals" ? "active" : ""}>承認一覧</button>
        <button onClick={() => setView("status")} className={view === "status" ? "active" : ""}>SSE 状態</button>
        <button onClick={() => setView("result")} className={view === "result" ? "active" : ""}>結果</button>
      </nav>

      {error && <div className="error" role="alert">{error}</div>}

      {view === "submit" && (
        <section className="panel">
          <span className="step">01 / QUESTION</span>
          <h2>社内文書への質問</h2>
          <form onSubmit={submit}>
            <label htmlFor="question">確認したい内容</label>
            <textarea id="question" rows={7} maxLength={1000} value={question} onChange={(e) => setQuestion(e.target.value)} />
            <button className="primary" disabled={question.trim().length < 2}>Workflow を開始</button>
          </form>
          <p className="hint">高リスク例：契約、個人情報、セキュリティ、経費、法務、障害対応</p>
        </section>
      )}

      {view === "status" && (
        <section className="panel" aria-live="polite">
          <span className="step">02 / EVENT STREAM</span>
          <div className="status-line"><strong>{status.toUpperCase()}</strong><small>{questionId ?? "質問未選択"}</small></div>
          {events.length === 0 ? <p className="empty">質問を送信すると状態が表示されます。</p> : (
            <ol className="timeline">
              {events.map((item, index) => (
                <li key={`${item.sequence}-${index}`}>
                  <span>{String(item.sequence).padStart(2, "0")}</span>
                  <div><strong>{item.message}</strong><small>{item.node ?? item.event} / {item.status}</small></div>
                </li>
              ))}
            </ol>
          )}
        </section>
      )}

      {view === "approvals" && (
        <section className="panel">
          <span className="step">03 / APPROVAL</span>
          <div className="section-title"><h2>承認待ち</h2><button onClick={() => void refreshApprovals()}>更新</button></div>
          {approvals.length === 0 ? <p className="empty">現在、承認待ちの質問はありません。</p> : approvals.map((item) => (
            <article className="approval" key={item.approval_id}>
              <div><span className="risk">HIGH RISK</span><small>{item.approval_id}</small></div>
              <h3>{item.question}</h3>
              <p>個人情報・契約・セキュリティ等の規則により、正式回答には担当者確認が必要です。</p>
              <div className="actions">
                <button className="approve" onClick={() => void decide(item, "approve")}>Approve</button>
                <button className="reject" onClick={() => void decide(item, "reject")}>Reject</button>
              </div>
            </article>
          ))}
        </section>
      )}

      {view === "result" && (
        <section className="panel report">
          <span className="step">04 / FINAL REPORT</span>
          {report ? <><div className="status-line"><strong>{report.risk_level}</strong><small>{report.question_id}</small></div><pre>{report.report}</pre></> : <p className="empty">完了した正式回答はまだありません。</p>}
        </section>
      )}
    </main>
  );
}
