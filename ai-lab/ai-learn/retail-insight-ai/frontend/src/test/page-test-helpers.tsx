/** 用可控的内存实现替代浏览器 EventSource，让测试可以主动推送 SSE 事件。 */
export class FakeEventSource {
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

export function jsonResponse(payload: object, status: number) {
  return new Response(JSON.stringify(payload), { status });
}

export function documentList(items: object[] = []) {
  return jsonResponse({
    success: true,
    request_id: "request-doc-list",
    data: { items, next_cursor: null },
    error: null,
  }, 200);
}

export function documentDetail(overrides: Record<string, unknown> = {}) {
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

export function chunkList(items: object[] = []) {
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

export function retrievalResponse(results: object[] = []) {
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

export function ragAnswerResponse(overrides: Record<string, unknown> = {}) {
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

export function approvalList(items: object[] = []) {
  return jsonResponse({
    success: true,
    request_id: "request-approval-list",
    data: { items, next_cursor: null },
    error: null,
  }, 200);
}

export function approvalDetail(overrides: Record<string, unknown> = {}) {
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
