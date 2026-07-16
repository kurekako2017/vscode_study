/** Backend 支持的三条 Workflow 路径。 */
export type AnalysisMode = "hybrid" | "kpi" | "research";
/** 与 Backend TaskStatus 保持一致的公开状态。 */
export type TaskStatus = "queued" | "running" | "completed" | "failed";

/** 普通 JSON API 的标准错误对象。 */
export interface ApiError {
  code: string;
  message: string;
  detail: Record<string, unknown>;
}

/** 普通 JSON API 共用 envelope；SSE 事件不使用它。 */
export interface ApiResponse<T> {
  success: boolean;
  request_id: string;
  data: T | null;
  error: ApiError | null;
}

/** POST /api/tasks 的最小响应。 */
export interface TaskCreateResponse {
  task_id: string;
  status: TaskStatus;
}

/** SSE data 的类型合同；sequence 可用于排序和未来断线续传。 */
export interface TaskEvent {
  task_id: string;
  sequence: number;
  event: "status" | "done" | "error";
  status: TaskStatus;
  message: string;
  request_id: string;
  error_code: string | null;
  node: string | null;
  report_path: string | null;
  created_at: string;
}

/** 页面统一展示的最小错误信息。 */
export interface DisplayError {
  code: string;
  message: string;
}

/** GET /api/tasks/{task_id}/report 的响应。 */
export interface ReportResponse {
  task_id: string;
  markdown: string;
  provider: string;
  created_at: string;
}

/** 上传接口返回的同步会话结果。 */
export interface DocumentUploadSessionResponse {
  upload_id: string;
  document_id: string;
  status: "accepted" | "validating" | "storing" | "completed" | "failed";
  progress: number;
  created_at: string;
  updated_at: string;
  error_code: string | null;
  error_message: string | null;
}

/** 文档来源是后端公开给前端的最小来源快照。 */
export interface DocumentSourceResponse {
  source_type: string;
  uri: string;
  label: string | null;
  external_id: string | null;
}

/** 文档详情和列表条目共用同一个后端 schema。 */
export interface DocumentResponse {
  document_id: string;
  title: string;
  description: string | null;
  owner: string;
  created_at: string;
  updated_at: string;
  version: number;
  language: string;
  document_type: string;
  status: string;
  tags: string[];
  source: DocumentSourceResponse | null;
  checksum: string;
}

/** 文档列表接口当前返回 items + next_cursor。 */
export interface DocumentListResponse {
  items: DocumentResponse[];
  next_cursor: string | null;
}

/** 归档接口只返回最小状态变化结果。 */
export interface DocumentArchiveResponse {
  document_id: string;
  status: string;
}

/** 导入流水线当前返回同步 import 记录。 */
export interface DocumentImportResponse {
  import_id: string;
  document_id: string;
  status: string;
  created_at: string;
  updated_at: string;
  error_code: string | null;
  error_message: string | null;
}

/** chunk 详情包含内容与父文档快照。 */
export interface DocumentChunkResponse {
  document_id: string;
  version: number;
  chunk_id: string;
  chunk_index: number;
  content: string;
  character_count: number;
  metadata: DocumentResponse;
  created_at: string;
}

/** chunk 列表用于详情页展示数量与预览。 */
export interface DocumentChunkListResponse {
  document_id: string;
  version: number;
  items: DocumentChunkResponse[];
  next_cursor: string | null;
}

/** 检索请求当前只支持后端真实存在的 keyword filters。 */
export interface DocumentRetrievalSearchRequest {
  query: string;
  limit?: number;
  include_archived?: boolean;
  document_type?: string;
  language?: string;
  tags?: string[];
}

/** 检索结果当前固定返回 excerpt、score、source 和 metadata。 */
export interface DocumentRetrievalResultResponse {
  document_id: string;
  chunk_id: string;
  chunk_index: number;
  content_excerpt: string;
  score: number;
  source: DocumentSourceResponse;
  metadata: DocumentResponse;
}

/** Retrieval 成功响应没有 evaluation，只有 result list + total + mode。 */
export interface DocumentRetrievalSearchResponse {
  results: DocumentRetrievalResultResponse[];
  total: number;
  query: string;
  retrieval_mode: string;
}

/** Internal RAG 当前只有两种冻结回答模式。 */
export type InternalRagAnswerMode = "extractive" | "summary";

/** Internal RAG request 与后端 schema 保持一致。 */
export interface InternalRagAnswerRequest {
  question: string;
  limit?: number;
  include_archived?: boolean;
  document_type?: string;
  language?: string;
  tags?: string[];
  answer_mode: InternalRagAnswerMode;
  require_citations: boolean;
}

/** 引用字段来自真实 citation schema，而不是 retrieval metadata 全量复制。 */
export interface InternalRagCitationResponse {
  document_id: string;
  chunk_id: string;
  chunk_index: number;
  excerpt: string;
  source: DocumentSourceResponse;
  score: number;
}

/** Internal RAG 响应对前端公开 answer、citations、confidence、warnings。 */
export interface InternalRagAnswerResponse {
  answer: string;
  citations: InternalRagCitationResponse[];
  retrieval_mode: string;
  answer_mode: InternalRagAnswerMode;
  confidence: number;
  warnings: string[];
}

/** Approval workflow 当前复用 report status 作为审批状态。 */
export type ApprovalStatus =
  | "generated"
  | "pending_approval"
  | "approved"
  | "rejected"
  | "revised"
  | "published"
  | "archived";

/** Approval 列表和详情当前使用同一个后端响应结构。 */
export interface ApprovalResponse {
  approval_id: string;
  task_id: string;
  report_version_id: string;
  status: ApprovalStatus;
  requested_at: string;
  requested_by: string | null;
  requested_by_username?: string | null;
  requested_by_role?: string | null;
  decided_at: string | null;
  decided_by: string | null;
  decided_by_username?: string | null;
  decided_by_role?: string | null;
  decision_reason: string | null;
  revision_no: number;
  revised_from_version_id: string | null;
  history?: ApprovalHistoryResponse[];
}

/** Approval History 是业务状态历史，不等同于安全 Audit Log。 */
export interface ApprovalHistoryResponse {
  history_id: string;
  approval_id: string;
  action: string;
  from_status: ApprovalStatus | null;
  to_status: ApprovalStatus | null;
  actor_user_id: string | null;
  actor_username: string | null;
  actor_role: string | null;
  comment: string | null;
  reason: string | null;
  report_version_id: string | null;
  occurred_at: string;
}

/** Approval 列表接口当前返回 items + next_cursor。 */
export interface ApprovalListResponse {
  items: ApprovalResponse[];
  next_cursor: string | null;
}

/** 提交审批和批准接口都复用 comment 字段。 */
export interface ApprovalSubmitRequest {
  comment?: string;
}

/** Reject 接口要求 reason 字段。 */
export interface ApprovalRejectRequest {
  reason?: string;
}

/** Revise 接口要求 revision_reason 字段。 */
export interface ApprovalRevisionRequest {
  revision_reason?: string;
}

/** Report revise 成功后返回的是新版本快照，而不是 approval 明细。 */
export interface ApprovalRevisionResponse {
  task_id: string;
  report_version_id: string;
  status: ApprovalStatus;
  revision_no: number;
  revised_from_version_id: string | null;
}
