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
import type {
  ApprovalListResponse,
  ApprovalResponse,
  ApprovalRevisionResponse,
  ApprovalStatus,
  DisplayError,
} from "../types";

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
export function ApprovalPage() {
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

  const currentIdentity = "System placeholder user";

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
    () => (selectedApproval ? selectedApproval.status.replaceAll("_", " ") : "not selected"),
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
      setListError(toDisplayError(reason, "APPROVAL_LIST_ERROR", "Approval list request failed"));
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
      setDetailError(toDisplayError(reason, "APPROVAL_DETAIL_ERROR", "Approval detail request failed"));
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
      setBannerMessage(`Approval submitted: ${created.approval_id}`);
    } catch (reason) {
      setSubmitError(toDisplayError(reason, "APPROVAL_SUBMIT_ERROR", "Submit approval failed"));
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
      setBannerMessage(`Approval approved: ${updated.approval_id}`);
    } catch (reason) {
      setDetailError(toDisplayError(reason, "APPROVAL_APPROVE_ERROR", "Approve request failed"));
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
      setBannerMessage(`Approval rejected: ${updated.approval_id}`);
    } catch (reason) {
      setDetailError(toDisplayError(reason, "APPROVAL_REJECT_ERROR", "Reject request failed"));
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
    } catch (reason) {
      setDetailError(toDisplayError(reason, "APPROVAL_REVISE_ERROR", "Revision request failed"));
    } finally {
      setDecisionLoading(null);
    }
  }

  return (
    <section className="approval-shell" aria-label="Approval workspace">
      <aside className="panel approval-sidebar">
        <div className="panel-heading">
          <span>01</span>
          <h2>Approval Queue</h2>
        </div>
        <p className="boundary">Current identity: {currentIdentity}</p>
        <form className="stack-form" onSubmit={handleFilterSubmit}>
          <label htmlFor="approval-filter-task-id">Task ID Filter</label>
          <input
            id="approval-filter-task-id"
            value={filterTaskId}
            onChange={(event) => setFilterTaskId(event.target.value)}
            disabled={listLoading || listRefreshing}
          />
          <label htmlFor="approval-filter-status">Status Filter</label>
          <select
            id="approval-filter-status"
            value={filterStatus}
            onChange={(event) => setFilterStatus(event.target.value)}
            disabled={listLoading || listRefreshing}
          >
            <option value="">all</option>
            {approvalStatuses.map((status) => (
              <option key={status} value={status}>{status}</option>
            ))}
          </select>
          <div className="action-row">
            <button type="submit" disabled={listLoading || listRefreshing}>
              {listLoading || listRefreshing ? "Loading…" : "Apply Filter"}
            </button>
            <button type="button" className="secondary-button" onClick={() => void loadApprovals(false)} disabled={listLoading || listRefreshing}>
              Retry / Refresh
            </button>
          </div>
        </form>

        {listError && <div className="error" role="alert">[{listError.code}] {listError.message}</div>}

        {listLoading ? (
          <p className="empty">Loading approvals…</p>
        ) : approvals.length === 0 ? (
          <p className="empty">No approvals found. Submit an approval request to begin the workflow.</p>
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
                  <small>Task {item.task_id}</small>
                </div>
                <div className="row-meta">
                  <span className={`pill status-pill status-pill-${item.status}`}>{item.status}</span>
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
            <h2>Submit Approval</h2>
          </div>
          <form className="stack-form" onSubmit={handleSubmitApproval}>
            <label htmlFor="approval-submit-task-id">Task ID</label>
            <input
              id="approval-submit-task-id"
              value={submitTaskId}
              onChange={(event) => setSubmitTaskId(event.target.value)}
              disabled={submitLoading}
            />
            <label htmlFor="approval-submit-comment">Comment</label>
            <textarea
              id="approval-submit-comment"
              rows={3}
              value={submitComment}
              onChange={(event) => setSubmitComment(event.target.value)}
              disabled={submitLoading}
            />
            <button type="submit" disabled={submitLoading || submitTaskId.trim().length === 0}>
              {submitLoading ? "Submitting…" : "Submit Approval"}
            </button>
            {submitError && <div className="error" role="alert">[{submitError.code}] {submitError.message}</div>}
          </form>
        </section>

        <section className="panel detail-panel approval-detail-panel" aria-live="polite">
          <div className="panel-heading">
            <span>03</span>
            <h2>Approval Detail</h2>
            <small>Status: {selectedStatusLabel}</small>
          </div>

          {bannerMessage && <div className="success-banner" role="status">{bannerMessage}</div>}
          {detailError && <div className="error" role="alert">[{detailError.code}] {detailError.message}</div>}

          {detailLoading ? (
            <p className="empty">Loading approval detail…</p>
          ) : selectedApproval === null ? (
            <p className="empty">Select an approval to inspect its status, version snapshot, and decision data.</p>
          ) : (
            <>
              <dl className="detail-grid">
                <div><dt>Approval ID</dt><dd>{selectedApproval.approval_id}</dd></div>
                <div><dt>Task ID</dt><dd>{selectedApproval.task_id}</dd></div>
                <div><dt>Report Version ID</dt><dd>{selectedApproval.report_version_id}</dd></div>
                <div><dt>Status</dt><dd><span className={`pill status-pill status-pill-${selectedApproval.status}`}>{selectedApproval.status}</span></dd></div>
                <div><dt>Requested At</dt><dd>{formatDateTime(selectedApproval.requested_at)}</dd></div>
                <div><dt>Requested By</dt><dd>{selectedApproval.requested_by ?? "system placeholder user"}</dd></div>
                <div><dt>Decided At</dt><dd>{selectedApproval.decided_at ? formatDateTime(selectedApproval.decided_at) : "Not decided yet"}</dd></div>
                <div><dt>Decided By</dt><dd>{selectedApproval.decided_by ?? "Not decided yet"}</dd></div>
                <div><dt>Decision Reason</dt><dd>{selectedApproval.decision_reason ?? "None"}</dd></div>
                <div><dt>Revision No</dt><dd>{selectedApproval.revision_no}</dd></div>
                <div><dt>Revised From</dt><dd>{selectedApproval.revised_from_version_id ?? "None"}</dd></div>
                <div><dt>Audit Summary</dt><dd>Audit fields are not returned directly by this API response.</dd></div>
              </dl>

              <div className="approval-actions">
                <section className="result-card">
                  <div className="subheading">
                    <strong>Approve</strong>
                    <small>Allowed only in pending_approval</small>
                  </div>
                  <label htmlFor="approval-approve-comment">Approval Comment</label>
                  <textarea
                    id="approval-approve-comment"
                    rows={3}
                    value={approveComment}
                    onChange={(event) => setApproveComment(event.target.value)}
                    disabled={!canApproveOrReject || decisionLoading !== null}
                  />
                  <button type="button" disabled={!canApproveOrReject || decisionLoading !== null} onClick={() => void handleApprove()}>
                    {decisionLoading === "approve" ? "Approving…" : "Approve"}
                  </button>
                </section>

                <section className="result-card">
                  <div className="subheading">
                    <strong>Reject</strong>
                    <small>Allowed only in pending_approval</small>
                  </div>
                  <label htmlFor="approval-reject-reason">Reject Reason</label>
                  <textarea
                    id="approval-reject-reason"
                    rows={3}
                    value={rejectReason}
                    onChange={(event) => setRejectReason(event.target.value)}
                    disabled={!canApproveOrReject || decisionLoading !== null}
                  />
                  <button type="button" disabled={!canApproveOrReject || decisionLoading !== null} onClick={() => void handleReject()}>
                    {decisionLoading === "reject" ? "Rejecting…" : "Reject"}
                  </button>
                </section>

                <section className="result-card">
                  <div className="subheading">
                    <strong>Request Revision / Revise</strong>
                    <small>Allowed only in rejected</small>
                  </div>
                  <label htmlFor="approval-revision-reason">Revision Reason</label>
                  <textarea
                    id="approval-revision-reason"
                    rows={3}
                    value={revisionReason}
                    onChange={(event) => setRevisionReason(event.target.value)}
                    disabled={!canRevise || decisionLoading !== null}
                  />
                  <button type="button" disabled={!canRevise || decisionLoading !== null} onClick={() => void handleRevise()}>
                    {decisionLoading === "revise" ? "Revising…" : "Request Revision"}
                  </button>
                </section>
              </div>
            </>
          )}
        </section>
      </section>
    </section>
  );
}

function formatDateTime(value: string) {
  return new Date(value).toLocaleString("ja-JP");
}

function buildRevisionMessage(result: ApprovalRevisionResponse) {
  return `Revision created: ${result.report_version_id} (${result.status} / v${result.revision_no})`;
}
