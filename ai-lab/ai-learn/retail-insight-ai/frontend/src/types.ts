/** Backend 支持的三条 Workflow 路径。 */
export type AnalysisMode = "hybrid" | "kpi" | "research";
/** 与 Backend TaskStatus 保持一致的公开状态。 */
export type TaskStatus = "queued" | "running" | "completed" | "failed";

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
  message: string;
  data: {
    status?: TaskStatus;
    node?: string;
    error?: string;
    report_path?: string;
  };
  created_at: string;
}

/** GET /api/tasks/{task_id}/report 的响应。 */
export interface ReportResponse {
  task_id: string;
  markdown: string;
  provider: string;
  created_at: string;
}
