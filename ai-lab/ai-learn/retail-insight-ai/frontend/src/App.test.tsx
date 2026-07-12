import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import App from "./App";

/** 用可控的内存实现替代浏览器 EventSource，让测试可以主动推送 SSE 事件。 */
class FakeEventSource {
  static instance: FakeEventSource;
  static readonly CLOSED = 2;
  readonly CLOSED = 2;
  readyState = 1;
  onerror: ((event: Event) => void) | null = null;
  listeners = new Map<string, EventListener>();

  constructor(public readonly url: string) {
    FakeEventSource.instance = this;
  }

  addEventListener(name: string, listener: EventListener) {
    this.listeners.set(name, listener);
  }

  emit(name: string, payload: object) {
    this.listeners.get(name)?.({ data: JSON.stringify(payload) } as MessageEvent);
  }

  close() {
    this.readyState = FakeEventSource.CLOSED;
  }
}

function jsonResponse(payload: object, status: number) {
  return new Response(JSON.stringify(payload), { status });
}

function documentList(items: object[] = []) {
  return jsonResponse({
    success: true,
    request_id: "request-doc-list",
    data: { items, next_cursor: null },
    error: null,
  }, 200);
}

function documentDetail(overrides: Record<string, unknown> = {}) {
  return jsonResponse({
    success: true,
    request_id: "request-doc-detail",
    data: {
      document_id: "doc-1",
      title: "Monthly Policy",
      description: "Internal monthly guidance",
      owner: "analysis-team",
      created_at: "2026-07-08T00:00:00Z",
      updated_at: "2026-07-09T00:00:00Z",
      version: 1,
      language: "ja",
      document_type: "markdown",
      status: "uploaded",
      tags: ["policy"],
      source: {
        source_type: "local_file",
        uri: "backend/data/documents/monthly-policy.md",
        label: null,
        external_id: null,
      },
      checksum: "sha256:doc-1",
      ...overrides,
    },
    error: null,
  }, 200);
}

function chunkList(items: object[] = []) {
  return jsonResponse({
    success: true,
    request_id: "request-chunks",
    data: {
      document_id: "doc-1",
      version: 1,
      items,
      next_cursor: null,
    },
    error: null,
  }, 200);
}

function retrievalResponse(results: object[] = []) {
  return jsonResponse({
    success: true,
    request_id: "request-retrieval",
    data: {
      results,
      total: results.length,
      query: "monthly policy",
      retrieval_mode: "keyword",
    },
    error: null,
  }, 200);
}

function ragAnswerResponse(overrides: Record<string, unknown> = {}) {
  return jsonResponse({
    success: true,
    request_id: "request-rag",
    data: {
      answer: "Extractive answer: Monthly policy evidence.",
      citations: [
        {
          document_id: "doc-1",
          chunk_id: "chunk-1",
          chunk_index: 0,
          excerpt: "Monthly policy evidence.",
          source: {
            source_type: "upload_form",
            uri: "upload://doc-1/source",
            label: null,
            external_id: null,
          },
          score: 0.92,
        },
      ],
      retrieval_mode: "keyword",
      answer_mode: "extractive",
      confidence: 0.82,
      warnings: ["weak_match"],
      ...overrides,
    },
    error: null,
  }, 200);
}

function approvalList(items: object[] = []) {
  return jsonResponse({
    success: true,
    request_id: "request-approval-list",
    data: { items, next_cursor: null },
    error: null,
  }, 200);
}

function approvalDetail(overrides: Record<string, unknown> = {}) {
  return jsonResponse({
    success: true,
    request_id: "request-approval-detail",
    data: {
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
      ...overrides,
    },
    error: null,
  }, 200);
}

describe("App", () => {
  beforeEach(() => {
    vi.stubGlobal("EventSource", FakeEventSource);
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("creates a task, consumes SSE, and renders the report", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-1",
        data: { task_id: "task-1", status: "queued" },
        error: null,
      }, 202))
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-2",
        data: {
          task_id: "task-1",
          markdown: "# 完了レポート",
          provider: "static",
          created_at: "2026-06-27T00:00:00Z",
        },
        error: null,
      }, 200));
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "分析を開始" }));

    await waitFor(() => expect(FakeEventSource.instance.url).toBe("/api/tasks/task-1/events"));
    FakeEventSource.instance.emit("status", {
      task_id: "task-1", sequence: 1, event: "status", message: "Task started",
      status: "running", request_id: "request-1", error_code: null,
      node: "route", report_path: null, created_at: "2026-06-27T00:00:00Z",
    });
    FakeEventSource.instance.emit("done", {
      task_id: "task-1", sequence: 2, event: "done", message: "Task completed",
      status: "completed", request_id: "request-1", error_code: null,
      node: null, report_path: "/api/tasks/task-1/report", created_at: "2026-06-27T00:00:01Z",
    });

    expect(await screen.findByText("# 完了レポート")).toBeInTheDocument();
    expect(screen.getByText("COMPLETED")).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("shows document list, detail, and chunk count", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(documentList([{
        document_id: "doc-1",
        title: "Monthly Policy",
        description: "Internal monthly guidance",
        owner: "analysis-team",
        created_at: "2026-07-08T00:00:00Z",
        updated_at: "2026-07-09T00:00:00Z",
        version: 1,
        language: "ja",
        document_type: "markdown",
        status: "uploaded",
        tags: ["policy"],
        source: null,
        checksum: "sha256:doc-1",
      }]))
      .mockResolvedValueOnce(documentDetail())
      .mockResolvedValueOnce(chunkList([
        {
          document_id: "doc-1",
          version: 1,
          chunk_id: "chunk-1",
          chunk_index: 0,
          content: "Paragraph one",
          character_count: 13,
          metadata: {
            document_id: "doc-1",
            title: "Monthly Policy",
            description: "Internal monthly guidance",
            owner: "analysis-team",
            created_at: "2026-07-08T00:00:00Z",
            updated_at: "2026-07-09T00:00:00Z",
            version: 1,
            language: "ja",
            document_type: "markdown",
            status: "validated",
            tags: ["policy"],
            source: null,
            checksum: "sha256:doc-1",
          },
          created_at: "2026-07-09T00:00:00Z",
        },
      ]));
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Documents" }));

    expect(await screen.findByText("Monthly Policy")).toBeInTheDocument();
    expect(await screen.findByText("Chunk Count")).toBeInTheDocument();
    expect(await screen.findByText("Paragraph one")).toBeInTheDocument();
  });

  it("shows empty state when there are no documents", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(documentList()));

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Documents" }));

    expect(await screen.findByText("No documents yet. Upload a file to start the document workflow.")).toBeInTheDocument();
  });

  it("shows document list API error and allows refresh retry", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(jsonResponse({
        success: false,
        request_id: "request-doc-error",
        data: null,
        error: { code: "DOCUMENT_LIST_ERROR", message: "List failed", detail: {} },
      }, 500))
      .mockResolvedValueOnce(documentList());
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Documents" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("[DOCUMENT_LIST_ERROR] List failed");
    fireEvent.click(screen.getByRole("button", { name: "Retry / Refresh" }));
    expect(await screen.findByText("No documents yet. Upload a file to start the document workflow.")).toBeInTheDocument();
  });

  it("uploads a document successfully and refreshes the list", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(documentList())
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-upload",
        data: {
          upload_id: "upload-1",
          document_id: "doc-9",
          status: "completed",
          progress: 100,
          created_at: "2026-07-09T00:00:00Z",
          updated_at: "2026-07-09T00:00:00Z",
          error_code: null,
          error_message: null,
        },
        error: null,
      }, 201))
      .mockResolvedValueOnce(documentList([{
        document_id: "doc-9",
        title: "budget.csv",
        description: null,
        owner: "analysis-team",
        created_at: "2026-07-09T00:00:00Z",
        updated_at: "2026-07-09T00:00:00Z",
        version: 1,
        language: "ja",
        document_type: "csv",
        status: "uploaded",
        tags: ["finance"],
        source: null,
        checksum: "sha256:doc-9",
      }]))
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-doc-9",
        data: {
          document_id: "doc-9",
          title: "budget.csv",
          description: null,
          owner: "analysis-team",
          created_at: "2026-07-09T00:00:00Z",
          updated_at: "2026-07-09T00:00:00Z",
          version: 1,
          language: "ja",
          document_type: "csv",
          status: "uploaded",
          tags: ["finance"],
          source: null,
          checksum: "sha256:doc-9",
        },
        error: null,
      }, 200))
      .mockResolvedValueOnce(chunkList());
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Documents" }));

    const file = new File(["month,sales"], "budget.csv", { type: "text/csv" });
    fireEvent.change(screen.getByLabelText("ファイル"), { target: { files: [file] } });
    fireEvent.change(screen.getByLabelText("Tags (comma separated)"), { target: { value: "finance" } });
    fireEvent.click(screen.getByRole("button", { name: "Upload Document" }));

    expect(await screen.findByRole("status")).toHaveTextContent("Upload completed: doc-9");
    expect((await screen.findAllByText("budget.csv")).length).toBeGreaterThan(0);
  });

  it("shows upload failure from backend", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(documentList())
      .mockResolvedValueOnce(jsonResponse({
        success: false,
        request_id: "request-upload-fail",
        data: null,
        error: { code: "missing_title", message: "Title required", detail: {} },
      }, 422));
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Documents" }));

    const file = new File(["# doc"], "missing.md", { type: "text/markdown" });
    fireEvent.change(screen.getByLabelText("ファイル"), { target: { files: [file] } });
    fireEvent.change(screen.getByLabelText("タイトル"), { target: { value: "Missing" } });
    fireEvent.click(screen.getByRole("button", { name: "Upload Document" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("[missing_title] Title required");
  });

  it("archives a document and refreshes current detail", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(documentList([{
        document_id: "doc-1",
        title: "Monthly Policy",
        description: "Internal monthly guidance",
        owner: "analysis-team",
        created_at: "2026-07-08T00:00:00Z",
        updated_at: "2026-07-09T00:00:00Z",
        version: 1,
        language: "ja",
        document_type: "markdown",
        status: "uploaded",
        tags: ["policy"],
        source: null,
        checksum: "sha256:doc-1",
      }]))
      .mockResolvedValueOnce(documentDetail())
      .mockResolvedValueOnce(chunkList())
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-archive",
        data: { document_id: "doc-1", status: "archived" },
        error: null,
      }, 202))
      .mockResolvedValueOnce(documentList())
      .mockResolvedValueOnce(documentDetail({ status: "archived" }))
      .mockResolvedValueOnce(chunkList());
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Documents" }));

    expect(await screen.findByText("Monthly Policy")).toBeInTheDocument();
    fireEvent.click(await screen.findByRole("button", { name: "Archive" }));

    expect(await screen.findByRole("status")).toHaveTextContent("Archive accepted: doc-1 (archived)");
  });

  it("shows retrieval results on the rag page", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(retrievalResponse([
      {
        document_id: "doc-1",
        chunk_id: "chunk-1",
        chunk_index: 0,
        content_excerpt: "Monthly policy evidence.",
        score: 0.92,
        source: {
          source_type: "upload_form",
          uri: "upload://doc-1/source",
          label: null,
          external_id: null,
        },
        metadata: {
          document_id: "doc-1",
          title: "Monthly Policy",
          description: null,
          owner: "analysis-team",
          created_at: "2026-07-09T00:00:00Z",
          updated_at: "2026-07-09T00:00:00Z",
          version: 1,
          language: "en",
          document_type: "markdown",
          status: "validated",
          tags: ["policy"],
          source: null,
          checksum: "sha256:doc-1",
        },
      },
    ]));
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "RAG" }));
    fireEvent.change(screen.getByLabelText("Query"), { target: { value: "monthly policy" } });
    fireEvent.click(screen.getByRole("button", { name: "Search Retrieval" }));

    expect(await screen.findByRole("status")).toHaveTextContent("Retrieval mode: keyword / Total matches: 1");
    expect(await screen.findByText("Monthly policy evidence.")).toBeInTheDocument();
  });

  it("shows empty retrieval state from backend", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValueOnce(retrievalResponse()));

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "RAG" }));
    fireEvent.change(screen.getByLabelText("Query"), { target: { value: "no match" } });
    fireEvent.click(screen.getByRole("button", { name: "Search Retrieval" }));

    expect(await screen.findByText("No retrieval results found.")).toBeInTheDocument();
  });

  it("shows grounded internal rag answer and citations", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValueOnce(ragAnswerResponse()));

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "RAG" }));
    fireEvent.change(screen.getByLabelText("Question"), { target: { value: "What is the monthly policy?" } });
    fireEvent.click(screen.getByRole("button", { name: "Generate Answer" }));

    expect(await screen.findByRole("status")).toHaveTextContent("Answer mode: extractive");
    expect(await screen.findByText("Monthly policy evidence.")).toBeInTheDocument();
    expect(await screen.findByText("weak_match")).toBeInTheDocument();
  });

  it("shows internal rag API error", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValueOnce(jsonResponse({
      success: false,
      request_id: "request-rag-error",
      data: null,
      error: { code: "insufficient_context", message: "No usable evidence", detail: {} },
    }, 422)));

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "RAG" }));
    fireEvent.change(screen.getByLabelText("Question"), { target: { value: "rare token" } });
    fireEvent.click(screen.getByRole("button", { name: "Generate Answer" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("[insufficient_context] No usable evidence");
  });

  it("shows approval list and detail on the approval page", async () => {
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

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Approval" }));

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

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Approval" }));

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

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Approval" }));
    fireEvent.change(screen.getByLabelText("Task ID"), { target: { value: "task-9" } });

    const submitButton = screen.getByRole("button", { name: "Submit Approval" });
    expect(submitButton).not.toBeDisabled();
    fireEvent.click(submitButton);

    expect(await screen.findByRole("status")).toHaveTextContent("Approval submitted: approval-9");
    expect(fetchMock.mock.calls[1][0]).toBe("/api/v1/reports/task-9/submit-approval");
    expect(fetchMock.mock.calls[2][0]).toBe("/api/v1/approvals");
    expect(fetchMock.mock.calls[3][0]).toBe("/api/v1/approvals/approval-9");
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

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Approval" }));
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

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Approval" }));
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

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Approval" }));

    const approveButton = await screen.findByRole("button", { name: "Approve" });
    expect(approveButton).not.toBeDisabled();
    fireEvent.change(screen.getByLabelText("Approval Comment"), { target: { value: "Approved after review" } });
    fireEvent.click(approveButton);

    expect(await screen.findByRole("status")).toHaveTextContent("Approval approved: approval-1");
    expect(await screen.findByText("Approved after review")).toBeInTheDocument();
    expect(fetchMock.mock.calls[2][0]).toBe("/api/v1/approvals/approval-1/approve");
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

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Approval" }));

    fireEvent.change(await screen.findByLabelText("Reject Reason"), { target: { value: "Need clearer source trace" } });
    fireEvent.click(screen.getByRole("button", { name: "Reject" }));

    expect(await screen.findByRole("status")).toHaveTextContent("Approval rejected: approval-1");

    const approveButton = await screen.findByRole("button", { name: "Approve" });
    expect(approveButton).toBeDisabled();
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

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Approval" }));
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

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Approval" }));
    fireEvent.change(await screen.findByLabelText("Reject Reason"), { target: { value: "Need clearer source trace" } });
    fireEvent.click(screen.getByRole("button", { name: "Reject" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("[permission_denied] Reject denied");
  });
});
