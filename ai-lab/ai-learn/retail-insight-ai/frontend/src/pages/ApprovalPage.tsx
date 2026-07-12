import { FormEvent, useEffect, useMemo, useState } from "react";

import {
  ApiClientError,
  approveApproval,
  getApproval,
  listApprovals,
  rejectApproval,
  requestApprovalRevision,
  submitApproval,
} from "../api";
import { BusinessLearningPanel } from "../components/BusinessLearningPanel";
import { PageHeader } from "../components/PageHeader";
import { StatusBadge } from "../components/StatusBadge";
import { StatusBanner } from "../components/StatusBanner";
import type {
  ApprovalListResponse,
  ApprovalResponse,
  ApprovalRevisionResponse,
  ApprovalStatus,
  DisplayError,
} from "../types";
import type { RecordLearningEvent } from "../learning/learningTypes";

type DecisionAction = "approve" | "reject" | "revise" | null;

const approvalStatuses: ApprovalStatus[] = [
  "pending_approval",
  "approved",
  "rejected",
  "revised",
  "published",
  "archived",
];

/**
 * ApprovalPage 负责展示审批列表、详情和审批动作。
 *
 * 为什么单独成页：
 * - Approval 有自己独立的状态机和错误分支，和 Documents / RAG 放在一起会让学习路径变乱。
 * - 当前仍然保持最小前端结构，不引入 Router 和全局状态框架。
 */
interface ApprovalPageProps {
  onLearningEvent?: RecordLearningEvent;
}

export function ApprovalPage({ onLearningEvent }: ApprovalPageProps = {}) {
  const [filterTaskId, setFilterTaskId] = useState("");
  const [filterStatus, setFilterStatus] = useState("");
  const [approvals, setApprovals] = useState<ApprovalListResponse["items"]>([]);
  const [listLoading, setListLoading] = useState(false);
  const [listRefreshing, setListRefreshing] = useState(false);
  const [listError, setListError] = useState<DisplayError | null>(null);
  const [selectedApprovalId, setSelectedApprovalId] = useState<string | null>(null);
  const [selectedApproval, setSelectedApproval] = useState<ApprovalResponse | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState<DisplayError | null>(null);
  const [bannerMessage, setBannerMessage] = useState<string | null>(null);

  const [submitTaskId, setSubmitTaskId] = useState("");
  const [submitComment, setSubmitComment] = useState("");
  const [submitLoading, setSubmitLoading] = useState(false);
  const [submitError, setSubmitError] = useState<DisplayError | null>(null);

  const [approveComment, setApproveComment] = useState("");
  const [rejectReason, setRejectReason] = useState("");
  const [revisionReason, setRevisionReason] = useState("");
  const [decisionLoading, setDecisionLoading] = useState<DecisionAction>(null);

  const currentIdentity = "システム既定ユーザー";

  useEffect(() => {
    void loadApprovals(true);
  }, []);

  useEffect(() => {
    if (selectedApprovalId === null) {
      setSelectedApproval(null);
      setDetailError(null);
      return;
    }
    void loadApprovalDetail(selectedApprovalId);
  }, [selectedApprovalId]);

  const canApproveOrReject = selectedApproval?.status === "pending_approval";
  const canRevise = selectedApproval?.status === "rejected";

  const selectedStatusLabel = useMemo(
    () => (selectedApproval ? selectedApproval.status.replaceAll("_", " ") : "未選択"),
    [selectedApproval],
  );

  function toDisplayError(reason: unknown, fallbackCode: string, fallbackMessage: string): DisplayError {
    if (reason instanceof ApiClientError) {
      return { code: reason.code, message: reason.message };
    }
    return { code: fallbackCode, message: fallbackMessage };
  }

  async function loadApprovals(force = false) {
    if (force) {
      setListLoading(true);
    } else {
      setListRefreshing(true);
    }
    setListError(null);
    try {
      const response = await listApprovals({
        task_id: filterTaskId.trim() || undefined,
        status: filterStatus || undefined,
      });
      setApprovals(response.items);
      setSelectedApprovalId((current) => {
        if (current !== null && response.items.some((item) => item.approval_id === current)) {
          return current;
        }
        return response.items[0]?.approval_id ?? null;
      });
    } catch (reason) {
      setListError(toDisplayError(reason, "APPROVAL_LIST_ERROR", "承認一覧の取得に失敗しました"));
    } finally {
      setListLoading(false);
      setListRefreshing(false);
    }
  }

  async function loadApprovalDetail(approvalId: string) {
    setDetailLoading(true);
    setDetailError(null);
    try {
      const detail = await getApproval(approvalId);
      // 详情始终以真实后端返回为准，避免列表快照过期后误导学习者。
      setSelectedApproval(detail);
    } catch (reason) {
      setSelectedApproval(null);
      setDetailError(toDisplayError(reason, "APPROVAL_DETAIL_ERROR", "承認詳細の取得に失敗しました"));
    } finally {
      setDetailLoading(false);
    }
  }

  async function refreshAfterChange(nextSelectedApprovalId: string | null) {
    await loadApprovals(false);
    if (nextSelectedApprovalId !== null) {
      if (nextSelectedApprovalId === selectedApprovalId) {
        await loadApprovalDetail(nextSelectedApprovalId);
      } else {
        setSelectedApprovalId(nextSelectedApprovalId);
      }
    }
  }

  async function handleFilterSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await loadApprovals(true);
  }

  async function handleSubmitApproval(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitLoading(true);
    setSubmitError(null);
    setBannerMessage(null);
    try {
      const created = await submitApproval(submitTaskId.trim(), {
        comment: submitComment.trim() || undefined,
      });
      await refreshAfterChange(created.approval_id);
      setSubmitComment("");
      setBannerMessage(`承認依頼を送信しました: ${created.approval_id}`);
      onLearningEvent?.({ eventName: "handleSubmitApproval()", apiMethod: "POST", apiPath: `/api/v1/reports/${created.task_id}/submit-approval`, apiStatus: "201 Created", stateChanges: [`approval_id: ${created.approval_id}`, `report_version_id: ${created.report_version_id}`, "列表与详情刷新"], backendFlow: ["approvals.py submit_approval()", "_run_audited_operation()", "AuditMiddleware.run()", "ApprovalService.submit_approval()", "InMemoryApprovalRepository.save_approval_request()"] });
    } catch (reason) {
      setSubmitError(toDisplayError(reason, "APPROVAL_SUBMIT_ERROR", "承認依頼の送信に失敗しました"));
      onLearningEvent?.({ eventName: "handleSubmitApproval()", apiMethod: "POST", apiPath: `/api/v1/reports/${submitTaskId.trim()}/submit-approval`, apiStatus: "Backend error", stateChanges: ["submitError: null → error"], backendFlow: ["approvals.py submit_approval()", "AuditMiddleware.run()", "ApprovalService.submit_approval()"] });
    } finally {
      setSubmitLoading(false);
    }
  }

  async function handleApprove() {
    if (selectedApproval === null) return;
    setDecisionLoading("approve");
    setBannerMessage(null);
    setDetailError(null);
    try {
      const updated = await approveApproval(selectedApproval.approval_id, {
        comment: approveComment.trim() || undefined,
      });
      // 批准后要刷新列表和详情，这样状态 badge 与决策信息会一起更新。
      await refreshAfterChange(updated.approval_id);
      setApproveComment("");
      setBannerMessage(`承認しました: ${updated.approval_id}`);
      onLearningEvent?.({ eventName: "handleApprove()", apiMethod: "POST", apiPath: `/api/v1/approvals/${updated.approval_id}/approve`, apiStatus: "200 OK", stateChanges: ["decisionLoading: approve → null", "approval status: approved", "列表与详情刷新"], backendFlow: ["approvals.py approve()", "_run_audited_operation()", "AuditMiddleware.run()", "ApprovalService.approve()", "InMemoryApprovalRepository.save_approval_request()"] });
    } catch (reason) {
      setDetailError(toDisplayError(reason, "APPROVAL_APPROVE_ERROR", "承認処理に失敗しました"));
      onLearningEvent?.({ eventName: "handleApprove()", apiMethod: "POST", apiPath: `/api/v1/approvals/${selectedApproval.approval_id}/approve`, apiStatus: "403 / 409 / Backend error", stateChanges: ["detailError: null → error"], backendFlow: ["approvals.py approve()", "AuditMiddleware.run()", "ApprovalService.approve()"] });
    } finally {
      setDecisionLoading(null);
    }
  }

  async function handleReject() {
    if (selectedApproval === null) return;
    setDecisionLoading("reject");
    setBannerMessage(null);
    setDetailError(null);
    try {
      const updated = await rejectApproval(selectedApproval.approval_id, {
        reason: rejectReason.trim() || undefined,
      });
      await refreshAfterChange(updated.approval_id);
      setRejectReason("");
      setBannerMessage(`却下しました: ${updated.approval_id}`);
      onLearningEvent?.({ eventName: "handleReject()", apiMethod: "POST", apiPath: `/api/v1/approvals/${updated.approval_id}/reject`, apiStatus: "200 OK", stateChanges: ["decisionLoading: reject → null", "approval status: rejected", "列表与详情刷新"], backendFlow: ["approvals.py reject()", "_run_audited_operation()", "AuditMiddleware.run()", "ApprovalService.reject()", "InMemoryApprovalRepository.save_approval_event()"] });
    } catch (reason) {
      setDetailError(toDisplayError(reason, "APPROVAL_REJECT_ERROR", "却下処理に失敗しました"));
      onLearningEvent?.({ eventName: "handleReject()", apiMethod: "POST", apiPath: `/api/v1/approvals/${selectedApproval.approval_id}/reject`, apiStatus: "403 / 409 / Backend error", stateChanges: ["detailError: null → error"], backendFlow: ["approvals.py reject()", "AuditMiddleware.run()", "ApprovalService.reject()"] });
    } finally {
      setDecisionLoading(null);
    }
  }

  async function handleRevise() {
    if (selectedApproval === null) return;
    setDecisionLoading("revise");
    setBannerMessage(null);
    setDetailError(null);
    try {
      const result = await requestApprovalRevision(selectedApproval.task_id, {
        revision_reason: revisionReason.trim() || undefined,
      });
      // revise 返回的是 report version，因此列表刷新后仍保留当前 approval 方便对照旧记录。
      await refreshAfterChange(selectedApproval.approval_id);
      setRevisionReason("");
      setBannerMessage(buildRevisionMessage(result));
      onLearningEvent?.({ eventName: "handleRevise()", apiMethod: "POST", apiPath: `/api/v1/reports/${selectedApproval.task_id}/revise`, apiStatus: "201 Created", stateChanges: [`report_version_id: ${result.report_version_id}`, "approval 列表与详情刷新"], backendFlow: ["approvals.py revise()", "_run_audited_operation()", "AuditMiddleware.run()", "ApprovalService.revise()", "InMemoryApprovalRepository.save_report_version()"] });
    } catch (reason) {
      setDetailError(toDisplayError(reason, "APPROVAL_REVISE_ERROR", "修正依頼に失敗しました"));
      onLearningEvent?.({ eventName: "handleRevise()", apiMethod: "POST", apiPath: `/api/v1/reports/${selectedApproval.task_id}/revise`, apiStatus: "403 / 409 / Backend error", stateChanges: ["detailError: null → error"], backendFlow: ["approvals.py revise()", "AuditMiddleware.run()", "ApprovalService.revise()"] });
    } finally {
      setDecisionLoading(null);
    }
  }

  return (
    <>
      <PageHeader
        eyebrow="承認ワークフロー"
        title="承認管理"
        description="承認待ち一覧と不変の承認詳細を確認し、Backend の状態遷移に従って承認、却下、修正依頼を実行します。"
      />

      <section className="approval-shell" aria-label="承認管理ワークスペース">
        <aside className="panel approval-sidebar">
        <div className="panel-heading">
          <span>01</span>
          <h2>承認待ち一覧</h2>
        </div>
        <p className="boundary">現在のユーザー: {currentIdentity}</p>
        <form className="stack-form" onSubmit={handleFilterSubmit}>
          <label htmlFor="approval-filter-task-id">Task ID 絞り込み</label>
          <input
            id="approval-filter-task-id"
            value={filterTaskId}
            onChange={(event) => setFilterTaskId(event.target.value)}
            disabled={listLoading || listRefreshing}
          />
          <label htmlFor="approval-filter-status">ステータス絞り込み</label>
          <select
            id="approval-filter-status"
            value={filterStatus}
            onChange={(event) => setFilterStatus(event.target.value)}
            disabled={listLoading || listRefreshing}
          >
            <option value="">すべて</option>
            {approvalStatuses.map((status) => (
              <option key={status} value={status}>{status}</option>
            ))}
          </select>
          <div className="action-row">
            <button type="submit" disabled={listLoading || listRefreshing}>
              {listLoading || listRefreshing ? "読み込み中…" : "絞り込む"}
            </button>
            <button type="button" className="secondary-button" onClick={() => void loadApprovals(false)} disabled={listLoading || listRefreshing}>
              再試行 / 更新
            </button>
          </div>
        </form>

        {listError && <StatusBanner tone="error">[{listError.code}] {listError.message}</StatusBanner>}

        {listLoading ? (
          <p className="empty">承認一覧を読み込み中…</p>
        ) : approvals.length === 0 ? (
          <p className="empty">承認依頼はありません。承認依頼を送信してワークフローを開始してください。</p>
        ) : (
          <div className="document-table approval-table">
            {approvals.map((item) => (
              <button
                key={item.approval_id}
                type="button"
                className={selectedApprovalId === item.approval_id ? "document-row selected" : "document-row"}
                onClick={() => setSelectedApprovalId(item.approval_id)}
              >
                <div>
                  <strong>{item.approval_id}</strong>
                  <small>Task ID: {item.task_id}</small>
                </div>
                <div className="row-meta">
                  <StatusBadge value={item.status} />
                  <span>v{item.revision_no}</span>
                </div>
              </button>
            ))}
          </div>
        )}
        </aside>

        <section className="approval-main">
        <section className="panel approval-submit-panel">
          <div className="panel-heading">
            <span>02</span>
            <h2>承認依頼を送信</h2>
          </div>
          <form className="stack-form" onSubmit={handleSubmitApproval}>
            <label htmlFor="approval-submit-task-id">Task ID</label>
            <input
              id="approval-submit-task-id"
              value={submitTaskId}
              onChange={(event) => setSubmitTaskId(event.target.value)}
              disabled={submitLoading}
            />
            <label htmlFor="approval-submit-comment">コメント</label>
            <textarea
              id="approval-submit-comment"
              rows={3}
              value={submitComment}
              onChange={(event) => setSubmitComment(event.target.value)}
              disabled={submitLoading}
            />
            <button type="submit" disabled={submitLoading || submitTaskId.trim().length === 0}>
              {submitLoading ? "送信中…" : "承認依頼を送信"}
            </button>
            {submitError && <StatusBanner tone="error">[{submitError.code}] {submitError.message}</StatusBanner>}
          </form>
        </section>

        <section className="panel detail-panel approval-detail-panel" aria-live="polite">
          <div className="panel-heading">
            <span>03</span>
            <h2>承認詳細</h2>
            <small>ステータス: {selectedStatusLabel}</small>
          </div>

          {bannerMessage && <StatusBanner tone="success">{bannerMessage}</StatusBanner>}
          {detailError && <StatusBanner tone="error">[{detailError.code}] {detailError.message}</StatusBanner>}

          {detailLoading ? (
            <p className="empty">承認詳細を読み込み中…</p>
          ) : selectedApproval === null ? (
            <p className="empty">承認依頼を選択すると、ステータス、バージョンスナップショット、判断情報を確認できます。</p>
          ) : (
            <>
              <dl className="detail-grid">
                <div><dt>承認 ID</dt><dd>{selectedApproval.approval_id}</dd></div>
                <div><dt>Task ID</dt><dd>{selectedApproval.task_id}</dd></div>
                <div><dt>レポートバージョン ID</dt><dd>{selectedApproval.report_version_id}</dd></div>
                <div><dt>ステータス</dt><dd><StatusBadge value={selectedApproval.status} /></dd></div>
                <div><dt>依頼日時</dt><dd>{formatDateTime(selectedApproval.requested_at)}</dd></div>
                <div><dt>依頼者</dt><dd>{selectedApproval.requested_by ?? "システム既定ユーザー"}</dd></div>
                <div><dt>判断日時</dt><dd>{selectedApproval.decided_at ? formatDateTime(selectedApproval.decided_at) : "未判断"}</dd></div>
                <div><dt>判断者</dt><dd>{selectedApproval.decided_by ?? "未判断"}</dd></div>
                <div><dt>判断理由</dt><dd>{selectedApproval.decision_reason ?? "なし"}</dd></div>
                <div><dt>改訂番号</dt><dd>{selectedApproval.revision_no}</dd></div>
                <div><dt>改訂元</dt><dd>{selectedApproval.revised_from_version_id ?? "なし"}</dd></div>
                <div><dt>監査情報</dt><dd>監査フィールドはこの API レスポンスに直接含まれません。</dd></div>
              </dl>

              <div className="approval-actions">
                <section className="result-card">
                  <div className="subheading">
                    <strong>承認</strong>
                    <small>pending_approval の場合のみ実行できます</small>
                  </div>
                  <label htmlFor="approval-approve-comment">承認コメント</label>
                  <textarea
                    id="approval-approve-comment"
                    rows={3}
                    value={approveComment}
                    onChange={(event) => setApproveComment(event.target.value)}
                    disabled={!canApproveOrReject || decisionLoading !== null}
                  />
                  <button type="button" disabled={!canApproveOrReject || decisionLoading !== null} onClick={() => void handleApprove()}>
                    {decisionLoading === "approve" ? "承認中…" : "承認"}
                  </button>
                </section>

                <section className="result-card">
                  <div className="subheading">
                    <strong>却下</strong>
                    <small>pending_approval の場合のみ実行できます</small>
                  </div>
                  <label htmlFor="approval-reject-reason">却下理由</label>
                  <textarea
                    id="approval-reject-reason"
                    rows={3}
                    value={rejectReason}
                    onChange={(event) => setRejectReason(event.target.value)}
                    disabled={!canApproveOrReject || decisionLoading !== null}
                  />
                  <button type="button" disabled={!canApproveOrReject || decisionLoading !== null} onClick={() => void handleReject()}>
                    {decisionLoading === "reject" ? "却下中…" : "却下"}
                  </button>
                </section>

                <section className="result-card">
                  <div className="subheading">
                    <strong>修正依頼</strong>
                    <small>rejected の場合のみ実行できます</small>
                  </div>
                  <label htmlFor="approval-revision-reason">修正理由</label>
                  <textarea
                    id="approval-revision-reason"
                    rows={3}
                    value={revisionReason}
                    onChange={(event) => setRevisionReason(event.target.value)}
                    disabled={!canRevise || decisionLoading !== null}
                  />
                  <button type="button" disabled={!canRevise || decisionLoading !== null} onClick={() => void handleRevise()}>
                    {decisionLoading === "revise" ? "修正依頼中…" : "修正依頼"}
                  </button>
                </section>
              </div>
            </>
          )}
        </section>
      </section>
      </section>

      <BusinessLearningPanel
        pageName="承認管理"
        purpose="将已完成的经营分析报告提交给负责人审批，并保留 approval_id、报告版本和审批审计事实。"
        scenario="关东饮料销售下降分析完成后，负责人手动输入 task_id 提交承认依赖，再根据审核结果执行承認、却下或修正依頼。"
        prerequisites="分析依頼已经完成并生成 report。当前用户是系统既定用户；Approval API 的 RBAC 已生效，权限不足会返回 403。"
        relationship="本页使用分析依頼产生的 task_id，创建 approval_id 和 report_version_id。task_id 当前不从 TasksPage 自动传入，必须手动复制；批准结果不自动回写到 Documents 或 RAG 页面。"
        journey={{ previous: "分析依頼", current: "4 / 4 承認管理", completion: "执行承認、却下或修正依頼，并记录审批结果。", next: "最终可审计报告", recommendedCase: "APR-BIZ-001", transferredObjects: "approval_id、report_version_id、approval event", connection: "当前没有独立的最终汇总页面。" }}
        cases={[
          { id: "APR-BIZ-001", group: "标准业务 Case", purpose: "正常提交关东饮料报告审批。", input: "输入已完成报告的 Task ID，填写可选コメント，点击「承認依頼を送信」。", expected: "POST 返回 approval_id、report_version_id、pending_approval；列表和详情刷新。" },
          { id: "APR-BIZ-002", group: "异常与维护测试 Case", purpose: "确认提交必填项。", input: "清空 Task ID。", expected: "提交按钮不可点击，不发送请求。" },
          { id: "APR-BIZ-003", group: "异常与维护测试 Case", purpose: "确认不存在或未完成报告。", input: "输入不存在 task_id 或尚未完成任务。", expected: "Backend 返回实际 404／409 等业务错误，页面显示结构化错误。" },
          { id: "APR-BIZ-004", group: "异常与维护测试 Case", purpose: "确认审批状态机和权限错误。", input: "对 pending_approval 点击「承認」或「却下」；或用无权限用户调用。", expected: "成功时状态刷新；重复决策返回实际 409，权限不足返回 403 permission_denied。" },
          { id: "APR-BIZ-005", group: "异常与维护测试 Case", purpose: "确认修正依頼与刷新。", input: "对 rejected 记录输入修正理由并点击「修正依頼」，或点击「再試行 / 更新」。", expected: "修正成功返回新的 report_version_id；刷新只重新读取列表／详情，不改变审批状态。" },
        ]}
        flows={[
          {
            title: "审批列表、详情与提交",
            api: "GET /api/v1/approvals；GET /api/v1/approvals/{approval_id}；POST /api/v1/reports/{task_id}/submit-approval",
            frontend: ["ApprovalPage loadApprovals() / loadApprovalDetail() / handleSubmitApproval()", "listApprovals() / getApproval() / submitApproval()", "setApprovals / setSelectedApproval / banner"],
            backend: ["approvals.py list_approvals() / get_approval() / submit_approval()", "_run_audited_operation()", "AuditMiddleware.run()", "ApprovalService.list_approvals() / get_approval() / submit_approval()", "InMemoryApprovalRepository"],
          },
          {
            title: "承認、却下与修正依頼",
            api: "POST /api/v1/approvals/{approval_id}/approve；POST /api/v1/approvals/{approval_id}/reject；POST /api/v1/reports/{task_id}/revise",
            frontend: ["handleApprove() / handleReject() / handleRevise()", "approveApproval() / rejectApproval() / requestApprovalRevision()", "refreshAfterChange()"],
            backend: ["approvals.py approve() / reject() / revise()", "_run_audited_operation()", "AuditMiddleware.run()", "ApprovalService.approve() / reject() / revise()", "InMemoryApprovalRepository.save_approval_request() / save_report_version() / save_approval_event()"],
            note: "审批 API 的授权与审计包装在 Router 层；当前页面不显示独立审计日志列表。",
          },
        ]}
      />
    </>
  );
}

function formatDateTime(value: string) {
  return new Date(value).toLocaleString("ja-JP");
}

function buildRevisionMessage(result: ApprovalRevisionResponse) {
  return `改訂を作成しました: ${result.report_version_id} (${result.status} / v${result.revision_no})`;
}
