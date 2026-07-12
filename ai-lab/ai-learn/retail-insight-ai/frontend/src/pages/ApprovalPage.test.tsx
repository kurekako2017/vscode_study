import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { approvalDetail, approvalList, jsonResponse } from "../test/page-test-helpers";
import { ApprovalPage } from "./ApprovalPage";

describe("ApprovalPage", () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("shows approval list and detail", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(approvalList([
        {
          approval_id: "approval-1",
          task_id: "task-1",
          report_version_id: "report-version-1",
          status: "pending_approval",
          requested_at: "2026-07-12T00:00:00Z",
          requested_by: "user-test",
          decided_at: null,
          decided_by: null,
          decision_reason: null,
          revision_no: 1,
          revised_from_version_id: null,
        },
      ]))
      .mockResolvedValueOnce(approvalDetail());
    vi.stubGlobal("fetch", fetchMock);

    render(<ApprovalPage />);

    expect(await screen.findByText("approval-1")).toBeInTheDocument();
    expect(await screen.findByText("report-version-1")).toBeInTheDocument();
    expect(await screen.findByText("Audit fields are not returned directly by this API response.")).toBeInTheDocument();
  });

  it("shows approval empty state and list retry error", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(jsonResponse({
        success: false,
        request_id: "request-approval-list-error",
        data: null,
        error: { code: "permission_denied", message: "Approval review denied", detail: {} },
      }, 403))
      .mockResolvedValueOnce(approvalList());
    vi.stubGlobal("fetch", fetchMock);

    render(<ApprovalPage />);

    expect(await screen.findByRole("alert")).toHaveTextContent("[permission_denied] Approval review denied");
    fireEvent.click(screen.getByRole("button", { name: "Retry / Refresh" }));
    expect(await screen.findByText("No approvals found. Submit an approval request to begin the workflow.")).toBeInTheDocument();
  });

  it("submits approval successfully and refreshes list plus detail", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(approvalList())
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-submit-approval",
        data: {
          approval_id: "approval-9",
          task_id: "task-9",
          report_version_id: "report-version-9",
          status: "pending_approval",
          requested_at: "2026-07-12T00:00:00Z",
          requested_by: "user-test",
          decided_at: null,
          decided_by: null,
          decision_reason: null,
          revision_no: 1,
          revised_from_version_id: null,
        },
        error: null,
      }, 201))
      .mockResolvedValueOnce(approvalList([
        {
          approval_id: "approval-9",
          task_id: "task-9",
          report_version_id: "report-version-9",
          status: "pending_approval",
          requested_at: "2026-07-12T00:00:00Z",
          requested_by: "user-test",
          decided_at: null,
          decided_by: null,
          decision_reason: null,
          revision_no: 1,
          revised_from_version_id: null,
        },
      ]))
      .mockResolvedValueOnce(approvalDetail({
        approval_id: "approval-9",
        task_id: "task-9",
        report_version_id: "report-version-9",
      }));
    vi.stubGlobal("fetch", fetchMock);

    render(<ApprovalPage />);
    fireEvent.change(screen.getByLabelText("Task ID"), { target: { value: "task-9" } });
    fireEvent.click(screen.getByRole("button", { name: "Submit Approval" }));

    expect(await screen.findByRole("status")).toHaveTextContent("Approval submitted: approval-9");
  });

  it("shows submit approval failure from backend", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(approvalList())
      .mockResolvedValueOnce(jsonResponse({
        success: false,
        request_id: "request-submit-approval-error",
        data: null,
        error: { code: "approval_already_submitted", message: "Already submitted", detail: {} },
      }, 409));
    vi.stubGlobal("fetch", fetchMock);

    render(<ApprovalPage />);
    fireEvent.change(screen.getByLabelText("Task ID"), { target: { value: "task-1" } });
    fireEvent.click(screen.getByRole("button", { name: "Submit Approval" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("[approval_already_submitted] Already submitted");
  });

  it("disables submit approval button while request is in flight", async () => {
    const submitGate: { resolve: (value: Response) => void } = {
      resolve: () => undefined,
    };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(approvalList())
      .mockImplementationOnce(() => new Promise<Response>((resolve) => {
        submitGate.resolve = resolve;
      }))
      .mockResolvedValueOnce(approvalList([
        {
          approval_id: "approval-10",
          task_id: "task-10",
          report_version_id: "report-version-10",
          status: "pending_approval",
          requested_at: "2026-07-12T00:00:00Z",
          requested_by: "user-test",
          decided_at: null,
          decided_by: null,
          decision_reason: null,
          revision_no: 1,
          revised_from_version_id: null,
        },
      ]))
      .mockResolvedValueOnce(approvalDetail({
        approval_id: "approval-10",
        task_id: "task-10",
        report_version_id: "report-version-10",
      }));
    vi.stubGlobal("fetch", fetchMock);

    render(<ApprovalPage />);
    fireEvent.change(screen.getByLabelText("Task ID"), { target: { value: "task-10" } });
    fireEvent.click(screen.getByRole("button", { name: "Submit Approval" }));

    expect(screen.getByRole("button", { name: "Submitting…" })).toBeDisabled();
    submitGate.resolve(jsonResponse({
      success: true,
      request_id: "request-submit-approval",
      data: {
        approval_id: "approval-10",
        task_id: "task-10",
        report_version_id: "report-version-10",
        status: "pending_approval",
        requested_at: "2026-07-12T00:00:00Z",
        requested_by: "user-test",
        decided_at: null,
        decided_by: null,
        decision_reason: null,
        revision_no: 1,
        revised_from_version_id: null,
      },
      error: null,
    }, 201));

    expect(await screen.findByRole("status")).toHaveTextContent("Approval submitted: approval-10");
  });

  it("approves a pending approval and refreshes detail", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(approvalList([
        {
          approval_id: "approval-1",
          task_id: "task-1",
          report_version_id: "report-version-1",
          status: "pending_approval",
          requested_at: "2026-07-12T00:00:00Z",
          requested_by: "user-test",
          decided_at: null,
          decided_by: null,
          decision_reason: null,
          revision_no: 1,
          revised_from_version_id: null,
        },
      ]))
      .mockResolvedValueOnce(approvalDetail())
      .mockResolvedValueOnce(approvalDetail({
        status: "approved",
        decided_at: "2026-07-12T00:10:00Z",
        decided_by: "reviewer-1",
        decision_reason: "Approved after review",
      }))
      .mockResolvedValueOnce(approvalList([
        {
          approval_id: "approval-1",
          task_id: "task-1",
          report_version_id: "report-version-1",
          status: "approved",
          requested_at: "2026-07-12T00:00:00Z",
          requested_by: "user-test",
          decided_at: "2026-07-12T00:10:00Z",
          decided_by: "reviewer-1",
          decision_reason: "Approved after review",
          revision_no: 1,
          revised_from_version_id: null,
        },
      ]))
      .mockResolvedValueOnce(approvalDetail({
        status: "approved",
        decided_at: "2026-07-12T00:10:00Z",
        decided_by: "reviewer-1",
        decision_reason: "Approved after review",
      }));
    vi.stubGlobal("fetch", fetchMock);

    render(<ApprovalPage />);

    const approveButton = await screen.findByRole("button", { name: "Approve" });
    fireEvent.change(screen.getByLabelText("Approval Comment"), { target: { value: "Approved after review" } });
    fireEvent.click(approveButton);

    expect(await screen.findByRole("status")).toHaveTextContent("Approval approved: approval-1");
    expect(await screen.findByText("Approved after review")).toBeInTheDocument();
  });

  it("rejects a pending approval and supports revision", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(approvalList([
        {
          approval_id: "approval-1",
          task_id: "task-1",
          report_version_id: "report-version-1",
          status: "pending_approval",
          requested_at: "2026-07-12T00:00:00Z",
          requested_by: "user-test",
          decided_at: null,
          decided_by: null,
          decision_reason: null,
          revision_no: 1,
          revised_from_version_id: null,
        },
      ]))
      .mockResolvedValueOnce(approvalDetail())
      .mockResolvedValueOnce(approvalDetail({
        status: "rejected",
        decided_at: "2026-07-12T00:10:00Z",
        decided_by: "reviewer-1",
        decision_reason: "Need clearer source trace",
      }))
      .mockResolvedValueOnce(approvalList([
        {
          approval_id: "approval-1",
          task_id: "task-1",
          report_version_id: "report-version-1",
          status: "rejected",
          requested_at: "2026-07-12T00:00:00Z",
          requested_by: "user-test",
          decided_at: "2026-07-12T00:10:00Z",
          decided_by: "reviewer-1",
          decision_reason: "Need clearer source trace",
          revision_no: 1,
          revised_from_version_id: null,
        },
      ]))
      .mockResolvedValueOnce(approvalDetail({
        status: "rejected",
        decided_at: "2026-07-12T00:10:00Z",
        decided_by: "reviewer-1",
        decision_reason: "Need clearer source trace",
      }))
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-revise",
        data: {
          task_id: "task-1",
          report_version_id: "report-version-2",
          status: "revised",
          revision_no: 2,
          revised_from_version_id: "report-version-1",
        },
        error: null,
      }, 201))
      .mockResolvedValueOnce(approvalList([
        {
          approval_id: "approval-1",
          task_id: "task-1",
          report_version_id: "report-version-1",
          status: "rejected",
          requested_at: "2026-07-12T00:00:00Z",
          requested_by: "user-test",
          decided_at: "2026-07-12T00:10:00Z",
          decided_by: "reviewer-1",
          decision_reason: "Need clearer source trace",
          revision_no: 1,
          revised_from_version_id: null,
        },
      ]))
      .mockResolvedValueOnce(approvalDetail({
        status: "rejected",
        decided_at: "2026-07-12T00:10:00Z",
        decided_by: "reviewer-1",
        decision_reason: "Need clearer source trace",
      }));
    vi.stubGlobal("fetch", fetchMock);

    render(<ApprovalPage />);

    fireEvent.change(await screen.findByLabelText("Reject Reason"), { target: { value: "Need clearer source trace" } });
    fireEvent.click(screen.getByRole("button", { name: "Reject" }));
    expect(await screen.findByRole("status")).toHaveTextContent("Approval rejected: approval-1");

    fireEvent.change(screen.getByLabelText("Revision Reason"), { target: { value: "Clarify trace" } });
    fireEvent.click(screen.getByRole("button", { name: "Request Revision" }));
    expect(await screen.findByRole("status")).toHaveTextContent("Revision created: report-version-2 (revised / v2)");
  });

  it("shows approval conflict error from approve API", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(approvalList([
        {
          approval_id: "approval-1",
          task_id: "task-1",
          report_version_id: "report-version-1",
          status: "pending_approval",
          requested_at: "2026-07-12T00:00:00Z",
          requested_by: "user-test",
          decided_at: null,
          decided_by: null,
          decision_reason: null,
          revision_no: 1,
          revised_from_version_id: null,
        },
      ]))
      .mockResolvedValueOnce(approvalDetail())
      .mockResolvedValueOnce(jsonResponse({
        success: false,
        request_id: "request-approve-conflict",
        data: null,
        error: { code: "approval_already_decided", message: "Already decided", detail: {} },
      }, 409));
    vi.stubGlobal("fetch", fetchMock);

    render(<ApprovalPage />);
    fireEvent.click(await screen.findByRole("button", { name: "Approve" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("[approval_already_decided] Already decided");
  });

  it("shows approval permission error from reject API", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(approvalList([
        {
          approval_id: "approval-1",
          task_id: "task-1",
          report_version_id: "report-version-1",
          status: "pending_approval",
          requested_at: "2026-07-12T00:00:00Z",
          requested_by: "user-test",
          decided_at: null,
          decided_by: null,
          decision_reason: null,
          revision_no: 1,
          revised_from_version_id: null,
        },
      ]))
      .mockResolvedValueOnce(approvalDetail())
      .mockResolvedValueOnce(jsonResponse({
        success: false,
        request_id: "request-reject-forbidden",
        data: null,
        error: { code: "permission_denied", message: "Reject denied", detail: {} },
      }, 403));
    vi.stubGlobal("fetch", fetchMock);

    render(<ApprovalPage />);
    fireEvent.change(await screen.findByLabelText("Reject Reason"), { target: { value: "Need clearer source trace" } });
    fireEvent.click(screen.getByRole("button", { name: "Reject" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("[permission_denied] Reject denied");
  });
});
