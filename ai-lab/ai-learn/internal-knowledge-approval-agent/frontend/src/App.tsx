import { FormEvent, useEffect, useRef, useState } from "react";

import { ApiClientError, createQuestion, decideApproval, getReport, listApprovals, subscribeQuestion } from "./api";
import type { Approval, QuestionEvent, Report } from "./types";

type View = "submit" | "status" | "approvals" | "result";

const defaultQuestion = "個人情報を含む障害ログの共有手順を確認したい";

export default function App() {
  const [view, setView] = useState<View>("submit");
  const [question, setQuestion] = useState(defaultQuestion);
  const [questionId, setQuestionId] = useState<string | null>(null);
  const [status, setStatus] = useState("idle");
  const [events, setEvents] = useState<QuestionEvent[]>([]);
  const [approvals, setApprovals] = useState<Approval[]>([]);
  const [report, setReport] = useState<Report | null>(null);
  const [error, setError] = useState<string | null>(null);
  const unsubscribe = useRef<(() => void) | null>(null);

  useEffect(() => () => unsubscribe.current?.(), []);

  async function refreshApprovals() {
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
    setError(reason instanceof ApiClientError ? `[${reason.code}] ${reason.message}` : "[UNEXPECTED_ERROR] 処理に失敗しました");
  }

  function watch(id: string) {
    unsubscribe.current?.();
    unsubscribe.current = subscribeQuestion(
      id,
      (item) => {
        // 函数式更新防止连续 SSE 覆盖前一条事件。
        setEvents((current) => [...current, item]);
        setStatus(item.status);
        if (item.event === "approval_required") {
          setView("approvals");
        } else if (item.event === "done") {
          unsubscribe.current?.();
          void getReport(id).then((value) => {
            setReport(value);
            setView("result");
          }).catch(showError);
        } else if (item.event === "rejected" || item.event === "error") {
          unsubscribe.current?.();
          if (item.event === "rejected") setView("status");
          else setError(`[${item.error_code ?? "WORKFLOW_ERROR"}] ${item.message}`);
        }
      },
      () => setError("[SSE_CONNECTION_ERROR] 進捗接続が切断されました"),
    );
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
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
    setError(null);
    setQuestionId(item.question_id);
    setStatus(decision === "approve" ? "approved" : "rejected");
    // 页面刷新后可能没有旧 SSE，决定前重新订阅保证能看到恢复事件。
    watch(item.question_id);
    try {
      await decideApproval(item.approval_id, decision);
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
