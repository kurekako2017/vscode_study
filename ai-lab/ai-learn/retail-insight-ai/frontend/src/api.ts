import type {
  AnalysisMode,
  ApiResponse,
  ApprovalListResponse,
  ApprovalRejectRequest,
  ApprovalResponse,
  ApprovalRevisionRequest,
  ApprovalRevisionResponse,
  ApprovalSubmitRequest,
  DocumentArchiveResponse,
  DocumentChunkListResponse,
  DocumentImportResponse,
  DocumentListResponse,
  DocumentRetrievalSearchRequest,
  DocumentRetrievalSearchResponse,
  DocumentResponse,
  DocumentUploadSessionResponse,
  InternalRagAnswerRequest,
  InternalRagAnswerResponse,
  ReportResponse,
  TaskCreateResponse,
  TaskEvent,
} from "./types";

/** 保留 Backend error code，使 UI 不需要从 message 中猜错误类型。 */
export class ApiClientError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly detail: Record<string, unknown> = {},
  ) {
    super(message);
    this.name = "ApiClientError";
  }
}

interface DocumentListParams {
  status?: string;
  document_type?: string;
  language?: string;
  owner?: string;
  tag?: string;
  include_archived?: boolean;
  limit?: number;
  cursor?: string;
}

interface UploadDocumentInput {
  file: File;
  metadata: {
    title: string;
    description?: string;
    owner: string;
    tags: string[];
    language: string;
    document_type?: string;
  };
  idempotencyKey?: string;
}

interface ApprovalListParams {
  task_id?: string;
  status?: string;
  limit?: number;
  cursor?: string;
}

/** 统一处理 fetch 的网络层失败，避免组件中散落 try/catch 文案。 */
async function request(path: string, init?: RequestInit): Promise<Response> {
  try {
    return await fetch(path, init);
  } catch (reason) {
    throw new ApiClientError(
      "NETWORK_ERROR",
      reason instanceof Error ? reason.message : "Network request failed",
    );
  }
}

/** 解析统一 envelope，并保证调用方只会收到成功 data 或结构化异常。 */
async function unwrapResponse<T>(response: Response): Promise<T> {
  let envelope: ApiResponse<T>;
  try {
    envelope = (await response.json()) as ApiResponse<T>;
  } catch {
    throw new ApiClientError("INVALID_RESPONSE", `HTTP ${response.status}`);
  }

  if (!response.ok || !envelope.success || envelope.data === null) {
    throw new ApiClientError(
      envelope.error?.code ?? "HTTP_ERROR",
      envelope.error?.message ?? `HTTP ${response.status}`,
      envelope.error?.detail ?? {},
    );
  }
  return envelope.data;
}

/** 创建异步分析任务；这里只处理 HTTP 合同，不管理 React 页面状态。 */
export async function createTask(question: string, mode: AnalysisMode): Promise<TaskCreateResponse> {
  const response = await request("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, mode }),
  });
  return unwrapResponse<TaskCreateResponse>(response);
}

/** 在收到 done 事件后获取最终报告，避免把大段 Markdown 塞进 SSE。 */
export async function getReport(taskId: string): Promise<ReportResponse> {
  const response = await request(`/api/tasks/${taskId}/report`);
  return unwrapResponse<ReportResponse>(response);
}

/** 文档列表统一通过 API Client 组装 query，组件不直接拼接 URL。 */
export async function listDocuments(params: DocumentListParams = {}): Promise<DocumentListResponse> {
  const search = new URLSearchParams();
  if (params.status) search.set("status", params.status);
  if (params.document_type) search.set("document_type", params.document_type);
  if (params.language) search.set("language", params.language);
  if (params.owner) search.set("owner", params.owner);
  if (params.tag) search.set("tag", params.tag);
  if (params.include_archived) search.set("include_archived", "true");
  if (typeof params.limit === "number") search.set("limit", String(params.limit));
  if (params.cursor) search.set("cursor", params.cursor);

  const query = search.toString();
  const response = await request(query.length > 0 ? `/api/v1/documents?${query}` : "/api/v1/documents");
  const data = await unwrapResponse<DocumentListResponse>(response);
  return {
    ...data,
    items: data.items.map((item) => ({ ...item, tags: [...item.tags] })),
  };
}

/** 详情读取保持单独函数，方便列表和详情按需刷新。 */
export async function getDocument(documentId: string): Promise<DocumentResponse> {
  const response = await request(`/api/v1/documents/${documentId}`);
  const data = await unwrapResponse<DocumentResponse>(response);
  return { ...data, tags: [...data.tags] };
}

/** 上传沿用后端 multipart 合同，不在前端擅自改成 JSON。 */
export async function uploadDocument(input: UploadDocumentInput): Promise<DocumentUploadSessionResponse> {
  const formData = new FormData();
  formData.append("file", input.file);
  formData.append("metadata", JSON.stringify(input.metadata));
  const headers = new Headers();
  if (input.idempotencyKey) {
    headers.set("Idempotency-Key", input.idempotencyKey);
  }
  const response = await request("/api/v1/documents", {
    method: "POST",
    headers,
    body: formData,
  });
  return unwrapResponse<DocumentUploadSessionResponse>(response);
}

/** 归档动作只改状态，不改组件自己的业务判断。 */
export async function archiveDocument(documentId: string): Promise<DocumentArchiveResponse> {
  const response = await request(`/api/v1/documents/${documentId}`, { method: "DELETE" });
  return unwrapResponse<DocumentArchiveResponse>(response);
}

/** 导入动作返回真实 import 状态，供前端展示成功反馈。 */
export async function importDocument(documentId: string): Promise<DocumentImportResponse> {
  const response = await request(`/api/v1/documents/${documentId}/import`, { method: "POST" });
  return unwrapResponse<DocumentImportResponse>(response);
}

/** chunk 动作用真实接口返回结果驱动数量和预览。 */
export async function chunkDocument(documentId: string): Promise<DocumentChunkListResponse> {
  const response = await request(`/api/v1/documents/${documentId}/chunks`, { method: "POST" });
  return unwrapResponse<DocumentChunkListResponse>(response);
}

/** 详情页需要读取已存在 chunk，不能靠前端本地猜数量。 */
export async function getDocumentChunks(documentId: string): Promise<DocumentChunkListResponse> {
  const response = await request(`/api/v1/documents/${documentId}/chunks`);
  return unwrapResponse<DocumentChunkListResponse>(response);
}

/** 检索请求统一从 API Client 发出，组件只关心表单状态和结果渲染。 */
export async function searchDocumentRetrieval(
  payload: DocumentRetrievalSearchRequest,
): Promise<DocumentRetrievalSearchResponse> {
  const response = await request("/api/v1/document-retrieval/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return unwrapResponse<DocumentRetrievalSearchResponse>(response);
}

/** Internal RAG 当前只接 deterministic answer API，不在前端拼装假答案。 */
export async function answerInternalRag(
  payload: InternalRagAnswerRequest,
): Promise<InternalRagAnswerResponse> {
  const response = await request("/api/v1/internal-rag/answer", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return unwrapResponse<InternalRagAnswerResponse>(response);
}

/** Approval 列表查询参数统一在 API Client 里拼接，页面只管理筛选表单。 */
export async function listApprovals(params: ApprovalListParams = {}): Promise<ApprovalListResponse> {
  const search = new URLSearchParams();
  if (params.task_id) search.set("task_id", params.task_id);
  if (params.status) search.set("status", params.status);
  if (typeof params.limit === "number") search.set("limit", String(params.limit));
  if (params.cursor) search.set("cursor", params.cursor);

  const query = search.toString();
  const response = await request(query.length > 0 ? `/api/v1/approvals?${query}` : "/api/v1/approvals");
  return unwrapResponse<ApprovalListResponse>(response);
}

/** 详情读取单独拆开，方便列表刷新后继续保留当前选中项。 */
export async function getApproval(approvalId: string): Promise<ApprovalResponse> {
  const response = await request(`/api/v1/approvals/${approvalId}`);
  return unwrapResponse<ApprovalResponse>(response);
}

/** Submit Approval 会创建新的 pending 记录，因此返回 approval 明细。 */
export async function submitApproval(
  taskId: string,
  payload: ApprovalSubmitRequest,
): Promise<ApprovalResponse> {
  const response = await request(`/api/v1/reports/${taskId}/submit-approval`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return unwrapResponse<ApprovalResponse>(response);
}

/** 批准动作仍然走 comment 合同，前端不能擅自改字段名。 */
export async function approveApproval(
  approvalId: string,
  payload: ApprovalSubmitRequest,
): Promise<ApprovalResponse> {
  const response = await request(`/api/v1/approvals/${approvalId}/approve`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return unwrapResponse<ApprovalResponse>(response);
}

/** Reject 动作必须把 reason 交给后端校验，前端只做最小表单控制。 */
export async function rejectApproval(
  approvalId: string,
  payload: ApprovalRejectRequest,
): Promise<ApprovalResponse> {
  const response = await request(`/api/v1/approvals/${approvalId}/reject`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return unwrapResponse<ApprovalResponse>(response);
}

/** Revise 返回的是新的 report version 快照，便于页面提示版本变化。 */
export async function requestApprovalRevision(
  taskId: string,
  payload: ApprovalRevisionRequest,
): Promise<ApprovalRevisionResponse> {
  const response = await request(`/api/v1/reports/${taskId}/revise`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return unwrapResponse<ApprovalRevisionResponse>(response);
}

/**
 * 订阅任务状态，并返回显式关闭函数。
 * SSE 使用扁平 TaskEvent，不经过普通 JSON API 的 success/data/error envelope。
 */
export function subscribeToTask(
  taskId: string,
  handlers: {
    onEvent: (event: TaskEvent) => void;
    onTransportError: () => void;
  },
): () => void {
  const source = new EventSource(`/api/tasks/${taskId}/events`);

  /** 所有业务事件共享同一个 JSON Schema，因此可以复用解析函数。 */
  const receive = (message: MessageEvent<string>) => {
    handlers.onEvent(JSON.parse(message.data) as TaskEvent);
  };
  source.addEventListener("status", receive as EventListener);
  source.addEventListener("done", receive as EventListener);
  source.addEventListener("error", receive as EventListener);
  // 浏览器也用 onerror 表示传输层异常；只在连接确实关闭时提示用户。
  source.onerror = (event) => {
    // Backend 的业务 error 是 MessageEvent；不要把它误判成网络断线。
    if (event instanceof MessageEvent) return;
    if (source.readyState === EventSource.CLOSED) {
      handlers.onTransportError();
    }
  };

  // API Client 不猜测组件生命周期，而是把资源清理权交还调用方。
  return () => source.close();
}
