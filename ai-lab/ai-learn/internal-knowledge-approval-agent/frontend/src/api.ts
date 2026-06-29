/**
 * Frontend API 与 SSE 适配层。
 * 页面调用本文件，而本文件调用 FastAPI；输入是类型化参数，输出是 Promise 或取消订阅函数。
 * unwrap 统一处理 Backend 的 ApiResponse/error；subscribeQuestion 负责 EventSource 生命周期。
 * 初学者重点：HTTP 用于创建/查询/审批，SSE 只推送进度，最终报告仍通过 HTTP 获取。
 * 日本现场面试：可说明业务 error 事件与网络断线分开处理，error 后 Backend 不再发送 done。
 * 企业级替换：增加认证 Header、请求取消、Last-Event-ID/重连和统一遥测，但不在浏览器保存密钥。
 */

import type { ApiResponse, Approval, Question, QuestionEvent, Report } from "./types";

export class ApiClientError extends Error {
  constructor(public readonly code: string, message: string) {
    super(message);
    this.name = "ApiClientError";
  }
}

async function unwrap<T>(response: Response): Promise<T> {
  // Backend 无论成功或失败都使用统一外壳；页面只接收有效 data 或 ApiClientError。
  const body = (await response.json()) as ApiResponse<T>;
  if (!response.ok || !body.success || body.data === null) {
    throw new ApiClientError(body.error?.code ?? "HTTP_ERROR", body.error?.message ?? `HTTP ${response.status}`);
  }
  return body.data;
}

export async function createQuestion(question: string): Promise<Question> {
  // 对应 POST /api/questions，请求体为 { question }，成功时 Backend 返回 202。
  return unwrap<Question>(await fetch("/api/questions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  }));
}

export async function listApprovals(): Promise<Approval[]> {
  // 对应 GET /api/approvals，只返回当前 pending 的审批资源。
  return unwrap<Approval[]>(await fetch("/api/approvals"));
}

export async function decideApproval(questionId: string, decision: "approve" | "reject"): Promise<Approval> {
  // 对应审批动作 Endpoint；重复决定时 Backend 以 409 表达冲突。
  return unwrap<Approval>(await fetch(`/api/approvals/${questionId}/${decision}`, { method: "POST" }));
}

export async function getReport(questionId: string): Promise<Report> {
  // 报告未进入 completed 时 Backend 返回 REPORT_NOT_READY，而不是空报告。
  return unwrap<Report>(await fetch(`/api/questions/${questionId}/report`));
}

export function subscribeQuestion(
  questionId: string,
  onEvent: (event: QuestionEvent) => void,
  onTransportError: () => void,
): () => void {
  // EventSource 根据 Backend 的 event 字段分发命名事件；返回函数供 App 主动 close。
  const source = new EventSource(`/api/questions/${questionId}/events`);
  const receive = (message: MessageEvent<string>) => onEvent(JSON.parse(message.data) as QuestionEvent);
  ["received", "risk_checked", "answer_generated", "approval_required", "approved", "rejected", "completed", "error"].forEach((name) => {
    source.addEventListener(name, receive as EventListener);
  });
  source.onerror = (event) => {
    // Backend 的业务 error 也是 MessageEvent；这里只报告真正的传输中断。
    if (!(event instanceof MessageEvent) && source.readyState === EventSource.CLOSED) onTransportError();
  };
  return () => source.close();
}
