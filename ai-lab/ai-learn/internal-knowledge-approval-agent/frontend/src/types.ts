export interface ApiErrorBody {
  code: string;
  message: string;
  detail: Record<string, unknown>;
}

export interface ApiResponse<T> {
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
