/**
 * Frontend 与 Backend 的数据合同镜像。
 * api.ts 用这些接口约束 JSON，App.tsx 用它们约束页面状态；本文件不执行运行时校验。
 * 初学者应对照 backend/app/api/schemas.py 与 SSE Event 字段阅读。
 * 企业级可由 OpenAPI 自动生成 HTTP 类型，但事件联合类型仍需随 Backend 合同同步维护。
 */

export interface ApiErrorBody {
  code: string;
  message: string;
  detail: Record<string, unknown>;
}

export interface ApiResponse<T> {
  // success=true 时 data 非空；失败时 error 含稳定 code，request_id 用于跨端排查。
  success: boolean;
  request_id: string;
  data: T | null;
  error: ApiErrorBody | null;
}

export interface Question {
  question_id: string;
  status: string;
  risk_level: "LOW" | "HIGH" | null;
  approval_id: string | null;
  error_code: string | null;
  created_at: string;
  updated_at: string;
}

export interface Approval {
  approval_id: string;
  question_id: string;
  question: string;
  risk_level: "HIGH" | null;
  status: "pending" | "approved" | "rejected";
  created_at: string;
  decided_at: string | null;
}

export interface Report {
  question_id: string;
  report: string;
  risk_level: "LOW" | "HIGH";
  created_at: string;
  updated_at: string;
}

export interface QuestionEvent {
  // sequence 保证单个问题内的显示顺序；event 决定页面分支，status 表示业务状态。
  question_id: string;
  sequence: number;
  event: "received" | "risk_checked" | "answer_generated" | "approval_required" | "approved" | "rejected" | "completed" | "error";
  message: string;
  request_id: string;
  status: string;
  node: string | null;
  error_code: string | null;
  approval_id?: string;
  report_path?: string;
  risk_level?: "LOW" | "HIGH";
  created_at: string;
}
