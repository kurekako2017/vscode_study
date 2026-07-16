import { afterEach, describe, expect, it, vi } from "vitest";

import {
  ApiClientError,
  answerInternalRag,
  approveApproval,
  archiveDocument,
  createTask,
  getApproval,
  getDocument,
  getDocumentChunks,
  getHealth,
  importDocument,
  login,
  listApprovals,
  rejectApproval,
  requestApprovalRevision,
  listDocuments,
  searchDocumentRetrieval,
  setApiAccessToken,
  setApiAuthHandlers,
  subscribeToTask,
  submitApproval,
  uploadDocument,
} from "./api";

function jsonResponse(payload: object, status: number) {
  return new Response(JSON.stringify(payload), { status });
}

describe("API Client", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("unwraps data from a successful task API response", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse({
      success: true,
      request_id: "request-success",
      data: { task_id: "task-success", status: "queued" },
      error: null,
    }, 202)));

    await expect(createTask("在庫を確認", "kpi")).resolves.toEqual({
      task_id: "task-success",
      status: "queued",
    });
  });

  it("throws ApiClientError from a failed API response", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse({
      success: false,
      request_id: "request-failure",
      data: null,
      error: {
        code: "VALIDATION_ERROR",
        message: "Request validation failed",
        detail: { field: "question" },
      },
    }, 422)));

    const error = await createTask("", "kpi").catch((reason: unknown) => reason);
    expect(error).toBeInstanceOf(ApiClientError);
    expect(error).toMatchObject({
      code: "VALIDATION_ERROR",
      message: "Request validation failed",
      detail: { field: "question" },
    });
  });

  it("builds document list query parameters", async () => {
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse({
      success: true,
      request_id: "request-doc-list",
      data: { items: [], next_cursor: null },
      error: null,
    }, 200));
    vi.stubGlobal("fetch", fetchMock);

    await listDocuments({ include_archived: true, language: "ja", tag: "monthly" });

    expect(fetchMock).toHaveBeenCalledWith("/api/v1/documents?language=ja&tag=monthly&include_archived=true", undefined);
  });

  it("uploads document with multipart form data", async () => {
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse({
      success: true,
      request_id: "request-upload",
      data: {
        upload_id: "upload-1",
        document_id: "doc-1",
        status: "completed",
        progress: 100,
        created_at: "2026-07-09T00:00:00Z",
        updated_at: "2026-07-09T00:00:00Z",
        error_code: null,
        error_message: null,
      },
      error: null,
    }, 201));
    vi.stubGlobal("fetch", fetchMock);

    const file = new File(["# doc"], "doc.md", { type: "text/markdown" });
    await uploadDocument({
      file,
      metadata: {
        title: "Doc",
        owner: "analysis-team",
        tags: ["policy"],
        language: "ja",
      },
      idempotencyKey: "idem-1",
    });

    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(fetchMock.mock.calls[0][0]).toBe("/api/v1/documents");
    expect(init.method).toBe("POST");
    expect(init.body).toBeInstanceOf(FormData);
    expect((init.headers as Headers).get("Idempotency-Key")).toBe("idem-1");
  });

  it("reads document detail", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse({
      success: true,
      request_id: "request-detail",
      data: {
        document_id: "doc-1",
        title: "Policy",
        description: null,
        owner: "analysis-team",
        created_at: "2026-07-09T00:00:00Z",
        updated_at: "2026-07-09T00:00:00Z",
        version: 1,
        language: "ja",
        document_type: "markdown",
        status: "uploaded",
        tags: ["policy"],
        source: null,
        checksum: "sha256:doc-1",
      },
      error: null,
    }, 200)));

    await expect(getDocument("doc-1")).resolves.toMatchObject({ document_id: "doc-1", title: "Policy" });
  });

  it("calls archive, import, and chunk read endpoints", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-archive",
        data: { document_id: "doc-1", status: "archived" },
        error: null,
      }, 202))
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-import",
        data: {
          import_id: "import-1",
          document_id: "doc-1",
          status: "completed",
          created_at: "2026-07-09T00:00:00Z",
          updated_at: "2026-07-09T00:00:00Z",
          error_code: null,
          error_message: null,
        },
        error: null,
      }, 201))
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-chunks",
        data: { document_id: "doc-1", version: 1, items: [], next_cursor: null },
        error: null,
      }, 200));
    vi.stubGlobal("fetch", fetchMock);

    await archiveDocument("doc-1");
    await importDocument("doc-1");
    await getDocumentChunks("doc-1");

    expect(fetchMock.mock.calls[0][0]).toBe("/api/v1/documents/doc-1");
    expect((fetchMock.mock.calls[0][1] as RequestInit).method).toBe("DELETE");
    expect(fetchMock.mock.calls[1][0]).toBe("/api/v1/documents/doc-1/import");
    expect(fetchMock.mock.calls[2][0]).toBe("/api/v1/documents/doc-1/chunks");
  });

  it("calls document retrieval search with JSON body", async () => {
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse({
      success: true,
      request_id: "request-retrieval",
      data: {
        results: [],
        total: 0,
        query: "monthly policy",
        retrieval_mode: "keyword",
      },
      error: null,
    }, 200));
    vi.stubGlobal("fetch", fetchMock);

    await searchDocumentRetrieval({
      query: "monthly policy",
      limit: 5,
      include_archived: true,
      document_type: "markdown",
      language: "en",
      tags: ["policy"],
    });

    expect(fetchMock.mock.calls[0][0]).toBe("/api/v1/document-retrieval/search");
    expect((fetchMock.mock.calls[0][1] as RequestInit).method).toBe("POST");
    expect((fetchMock.mock.calls[0][1] as RequestInit).body).toBe(
      JSON.stringify({
        query: "monthly policy",
        limit: 5,
        include_archived: true,
        document_type: "markdown",
        language: "en",
        tags: ["policy"],
      }),
    );
  });

  it("calls internal rag answer with deterministic request body", async () => {
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse({
      success: true,
      request_id: "request-rag",
      data: {
        answer: "Extractive answer: policy",
        citations: [],
        retrieval_mode: "keyword",
        answer_mode: "extractive",
        confidence: 0.8,
        warnings: ["weak_match"],
      },
      error: null,
    }, 200));
    vi.stubGlobal("fetch", fetchMock);

    await answerInternalRag({
      question: "What is the policy?",
      limit: 3,
      include_archived: false,
      answer_mode: "extractive",
      require_citations: true,
      tags: ["policy"],
    });

    expect(fetchMock.mock.calls[0][0]).toBe("/api/v1/internal-rag/answer");
    expect((fetchMock.mock.calls[0][1] as RequestInit).method).toBe("POST");
  });

  it("calls approval list and detail endpoints", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-approval-list",
        data: {
          items: [],
          next_cursor: null,
        },
        error: null,
      }, 200))
      .mockResolvedValueOnce(jsonResponse({
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
        },
        error: null,
      }, 200));
    vi.stubGlobal("fetch", fetchMock);

    await listApprovals({ task_id: "task-1", status: "pending_approval" });
    await getApproval("approval-1");

    expect(fetchMock.mock.calls[0][0]).toBe("/api/v1/approvals?task_id=task-1&status=pending_approval");
    expect(fetchMock.mock.calls[1][0]).toBe("/api/v1/approvals/approval-1");
  });

  it("calls approval submit, approve, reject, and revise endpoints", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-submit-approval",
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
        },
        error: null,
      }, 201))
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-approve-approval",
        data: {
          approval_id: "approval-1",
          task_id: "task-1",
          report_version_id: "report-version-1",
          status: "approved",
          requested_at: "2026-07-12T00:00:00Z",
          requested_by: "user-test",
          decided_at: "2026-07-12T00:10:00Z",
          decided_by: "reviewer-1",
          decision_reason: "Approved",
          revision_no: 1,
          revised_from_version_id: null,
        },
        error: null,
      }, 200))
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-reject-approval",
        data: {
          approval_id: "approval-2",
          task_id: "task-2",
          report_version_id: "report-version-2",
          status: "rejected",
          requested_at: "2026-07-12T00:00:00Z",
          requested_by: "user-test",
          decided_at: "2026-07-12T00:12:00Z",
          decided_by: "reviewer-2",
          decision_reason: "Need clearer trace",
          revision_no: 1,
          revised_from_version_id: null,
        },
        error: null,
      }, 200))
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-revise-approval",
        data: {
          task_id: "task-2",
          report_version_id: "report-version-3",
          status: "revised",
          revision_no: 2,
          revised_from_version_id: "report-version-2",
        },
        error: null,
      }, 201));
    vi.stubGlobal("fetch", fetchMock);

    await submitApproval("task-1", { comment: "Ready" });
    await approveApproval("approval-1", { comment: "Approved" });
    await rejectApproval("approval-2", { reason: "Need clearer trace" });
    await requestApprovalRevision("task-2", { revision_reason: "Clarify trace" });

    expect(fetchMock.mock.calls[0][0]).toBe("/api/v1/reports/task-1/submit-approval");
    expect((fetchMock.mock.calls[0][1] as RequestInit).method).toBe("POST");
    expect(fetchMock.mock.calls[1][0]).toBe("/api/v1/approvals/approval-1/approve");
    expect(fetchMock.mock.calls[2][0]).toBe("/api/v1/approvals/approval-2/reject");
    expect(fetchMock.mock.calls[3][0]).toBe("/api/v1/reports/task-2/revise");
  });

  it("adds one centralized Bearer header to protected JSON requests", async () => {
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse({
      success: true,
      request_id: "request-authenticated",
      data: { task_id: "task-authenticated", status: "queued" },
      error: null,
    }, 202));
    vi.stubGlobal("fetch", fetchMock);
    setApiAccessToken("access-token");

    await createTask("在庫を確認", "kpi");

    const headers = new Headers((fetchMock.mock.calls[0][1] as RequestInit).headers);
    expect(headers.get("Authorization")).toBe("Bearer access-token");
  });

  it("keeps login and health anonymous even when an old token exists", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-login",
        data: { access_token: "new-token", token_type: "bearer", expires_in: 1800 },
        error: null,
      }, 200))
      .mockResolvedValueOnce(new Response(JSON.stringify({
        status: "ok",
        service: "retail-insight-ai",
      }), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    setApiAccessToken("old-token");

    await login("manager", "password");
    await getHealth();

    expect(new Headers((fetchMock.mock.calls[0][1] as RequestInit).headers).has("Authorization")).toBe(false);
    expect(fetchMock.mock.calls[1][1]).toBeUndefined();
  });

  it("runs one unauthorized handler for concurrent 401 responses", async () => {
    let releaseUnauthorized: (() => void) | undefined;
    const onUnauthorized = vi.fn(() => new Promise<void>((resolve) => {
      releaseUnauthorized = resolve;
    }));
    setApiAccessToken("expired-token");
    setApiAuthHandlers({ onUnauthorized });
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse({
      success: false,
      request_id: "request-unauthorized",
      data: null,
      error: { code: "unauthorized", message: "Unauthorized", detail: {} },
    }, 401)));

    const requests = [
      createTask("one", "kpi").catch(() => null),
      createTask("two", "kpi").catch(() => null),
    ];
    await vi.waitFor(() => expect(onUnauthorized).toHaveBeenCalledTimes(1));
    releaseUnauthorized?.();
    await Promise.all(requests);
    expect(onUnauthorized).toHaveBeenCalledTimes(1);
  });

  it("preserves the token and reports 403 through the global forbidden handler", async () => {
    const onForbidden = vi.fn();
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse({
      success: false,
      request_id: "request-forbidden",
      data: null,
      error: { code: "forbidden", message: "Forbidden", detail: {} },
    }, 403));
    setApiAccessToken("still-valid");
    setApiAuthHandlers({ onForbidden });
    vi.stubGlobal("fetch", fetchMock);

    await createTask("forbidden", "kpi").catch(() => null);
    await createTask("still-authenticated", "kpi").catch(() => null);

    expect(onForbidden).toHaveBeenCalledTimes(2);
    expect(new Headers((fetchMock.mock.calls[1][1] as RequestInit).headers).get("Authorization")).toBe("Bearer still-valid");
  });

  it("uses authenticated fetch streaming without putting the token in the SSE URL", async () => {
    const event = {
      task_id: "task-stream",
      sequence: 1,
      event: "done",
      status: "completed",
      message: "done",
      request_id: "request-stream",
      error_code: null,
      node: null,
      report_path: null,
      created_at: "2026-07-17T00:00:00Z",
    };
    const stream = new ReadableStream({
      start(controller) {
        controller.enqueue(new TextEncoder().encode(`event: done\ndata: ${JSON.stringify(event)}\n\n`));
        controller.close();
      },
    });
    const fetchMock = vi.fn().mockResolvedValue(new Response(stream, {
      status: 200,
      headers: { "Content-Type": "text/event-stream" },
    }));
    const onEvent = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    setApiAccessToken("stream-token");

    const unsubscribe = subscribeToTask("task-stream", {
      onEvent,
      onTransportError: vi.fn(),
    });
    await vi.waitFor(() => expect(onEvent).toHaveBeenCalledWith(event));
    unsubscribe();

    expect(fetchMock.mock.calls[0][0]).toBe("/api/tasks/task-stream/events");
    const headers = new Headers((fetchMock.mock.calls[0][1] as RequestInit).headers);
    expect(headers.get("Authorization")).toBe("Bearer stream-token");
    expect(String(fetchMock.mock.calls[0][0])).not.toContain("stream-token");
  });
});
