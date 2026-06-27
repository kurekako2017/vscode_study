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
