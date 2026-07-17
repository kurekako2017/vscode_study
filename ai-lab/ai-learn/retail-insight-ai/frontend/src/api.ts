import type {
  AnalysisMode,
  AIAnalysisRequest,
  AIAnalysisResponse,
  ExecutiveReportRequest,
  ExecutiveReportResponse,
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
  CurrentUserResponse,
  HealthResponse,
  LoginResponse,
  LlmProviderMode,
  LlmRuntimeResponse,
  ReportCatalogResponse,
  ReportResponse,
  TaskCreateResponse,
  TaskEvent,
} from "./types";

interface ApiAuthHandlers {
  onUnauthorized?: () => void | Promise<void>;
  onForbidden?: () => void;
}

interface RequestOptions {
  anonymous?: boolean;
}

let apiAccessToken: string | null = null;
let apiAuthHandlers: ApiAuthHandlers = {};
let unauthorizedHandling: Promise<void> | null = null;

/**
 * AuthContext 是浏览器内唯一 Token owner；页面不直接读取 Token，也不手写 Authorization。
 * 测试可以传 null 恢复匿名状态，生产登出也走同一入口。
 */
export function setApiAccessToken(accessToken: string | null) {
  apiAccessToken = accessToken;
}

/** 注册全局 401/403 行为，避免每个页面各自实现会话失效逻辑。 */
export function setApiAuthHandlers(handlers: ApiAuthHandlers) {
  apiAuthHandlers = handlers;
}

/** 仅供测试隔离使用，不接触任何浏览器持久存储。 */
export function resetApiAuthForTests() {
  apiAccessToken = null;
  apiAuthHandlers = {};
  unauthorizedHandling = null;
}

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
async function handleUnauthorizedOnce() {
  if (!apiAuthHandlers.onUnauthorized) return;
  if (unauthorizedHandling === null) {
    unauthorizedHandling = Promise.resolve(apiAuthHandlers.onUnauthorized())
      .finally(() => {
        unauthorizedHandling = null;
      });
  }
  await unauthorizedHandling;
}

async function request(
  path: string,
  init?: RequestInit,
  options: RequestOptions = {},
): Promise<Response> {
  try {
    let requestInit = init;
    if (!options.anonymous && apiAccessToken !== null) {
      const headers = new Headers(init?.headers);
      headers.set("Authorization", `Bearer ${apiAccessToken}`);
      requestInit = { ...init, headers };
    }
    const response = await fetch(path, requestInit);
    if (response.status === 401 && !options.anonymous) {
      await handleUnauthorizedOnce();
    } else if (response.status === 403 && !options.anonymous) {
      apiAuthHandlers.onForbidden?.();
    }
    return response;
  } catch (reason) {
    throw new ApiClientError(
      "NETWORK_ERROR",
      reason instanceof Error ? reason.message : "Network request failed",
    );
  }
}

/** Login 与 Health 是冻结匿名入口，不能误带旧会话的 Authorization Header。 */
export async function login(username: string, password: string): Promise<LoginResponse> {
  const response = await request("/api/v1/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  }, { anonymous: true });
  return unwrapResponse<LoginResponse>(response);
}

export async function getCurrentUser(): Promise<CurrentUserResponse> {
  const response = await request("/api/v1/users/me");
  return unwrapResponse<CurrentUserResponse>(response);
}

export async function getHealth(): Promise<HealthResponse> {
  const response = await request("/health", undefined, { anonymous: true });
  if (!response.ok) {
    throw new ApiClientError("HTTP_ERROR", `HTTP ${response.status}`);
  }
  return response.json() as Promise<HealthResponse>;
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

/** low_cost AI 分析；幂等键必须在同一次重试中复用。 */
export async function executeAIAnalysis(
  payload: AIAnalysisRequest,
  idempotencyKey: string,
): Promise<AIAnalysisResponse> {
  const response = await request("/api/v1/ai-analysis", {
    method: "POST",
    headers: { "Content-Type": "application/json", "Idempotency-Key": idempotencyKey },
    body: JSON.stringify(payload),
  });
  return unwrapResponse<AIAnalysisResponse>(response);
}

/** high_quality 董事会报告；仅在 succeeded AI Analysis 后由用户显式确认触发。 */
export async function generateExecutiveReport(
  payload: ExecutiveReportRequest,
  idempotencyKey: string,
): Promise<ExecutiveReportResponse> {
  const response = await request("/api/v1/executive-reports", {
    method: "POST",
    headers: { "Content-Type": "application/json", "Idempotency-Key": idempotencyKey },
    body: JSON.stringify(payload),
  });
  return unwrapResponse<ExecutiveReportResponse>(response);
}

/** 可供 submit-approval 选择的报告目录（避免手工记忆 task_id）。 */
export async function listReportCatalog(limit = 30): Promise<ReportCatalogResponse> {
  const response = await request(`/api/v1/reports?limit=${limit}`);
  return unwrapResponse<ReportCatalogResponse>(response);
}

/** 管理员查看 LLM 运行时（无 Key）。 */
export async function getLlmRuntime(): Promise<LlmRuntimeResponse> {
  const response = await request("/api/v1/admin/llm/runtime");
  return unwrapResponse<LlmRuntimeResponse>(response);
}

/** 管理员切换 stub/openrouter/fallback_chain；无密钥时后端 fail-closed。 */
export async function updateLlmRuntime(mode: LlmProviderMode): Promise<LlmRuntimeResponse> {
  const response = await request("/api/v1/admin/llm/runtime", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ llm_provider_mode: mode }),
  });
  return unwrapResponse<LlmRuntimeResponse>(response);
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
  if (apiAccessToken !== null) {
    const controller = new AbortController();
    void subscribeToAuthenticatedTaskStream(taskId, controller, handlers);
    return () => controller.abort();
  }

  // 匿名 fallback 只保留给既有本地组件测试；真实受保护页面始终使用上面的 Bearer fetch stream。
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

/**
 * 原生 EventSource 不能设置 Authorization Header，因此认证后的 SSE 使用 fetch stream。
 * Parser 只保存当前事件块，不记录完整流或报告正文。
 */
async function subscribeToAuthenticatedTaskStream(
  taskId: string,
  controller: AbortController,
  handlers: {
    onEvent: (event: TaskEvent) => void;
    onTransportError: () => void;
  },
) {
  try {
    const response = await request(`/api/tasks/${taskId}/events`, {
      headers: { Accept: "text/event-stream" },
      signal: controller.signal,
    });
    if (!response.ok || response.body === null) {
      handlers.onTransportError();
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (!controller.signal.aborted) {
      const { value, done } = await reader.read();
      buffer += decoder.decode(value, { stream: !done }).replaceAll("\r\n", "\n");
      let boundary = buffer.indexOf("\n\n");
      while (boundary >= 0) {
        const block = buffer.slice(0, boundary);
        buffer = buffer.slice(boundary + 2);
        const data = block
          .split("\n")
          .filter((line) => line.startsWith("data:"))
          .map((line) => line.slice(5).trimStart())
          .join("\n");
        if (data.length > 0) {
          handlers.onEvent(JSON.parse(data) as TaskEvent);
        }
        boundary = buffer.indexOf("\n\n");
      }
      if (done) break;
    }
  } catch (reason) {
    if (!controller.signal.aborted && (!(reason instanceof DOMException) || reason.name !== "AbortError")) {
      handlers.onTransportError();
    }
  }
}
