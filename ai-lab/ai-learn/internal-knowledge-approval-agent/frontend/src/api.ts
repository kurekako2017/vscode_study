import type { ApiResponse, Approval, Question, QuestionEvent, Report } from "./types";

export class ApiClientError extends Error {
  constructor(public readonly code: string, message: string) {
    super(message);
    this.name = "ApiClientError";
  }
}

async function unwrap<T>(response: Response): Promise<T> {
  const body = (await response.json()) as ApiResponse<T>;
  if (!response.ok || !body.success || body.data === null) {
    throw new ApiClientError(body.error?.code ?? "HTTP_ERROR", body.error?.message ?? `HTTP ${response.status}`);
  }
  return body.data;
}

export async function createQuestion(question: string): Promise<Question> {
  return unwrap<Question>(await fetch("/api/questions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  }));
}

export async function listApprovals(): Promise<Approval[]> {
  return unwrap<Approval[]>(await fetch("/api/approvals"));
}

export async function decideApproval(questionId: string, decision: "approve" | "reject"): Promise<Approval> {
  return unwrap<Approval>(await fetch(`/api/approvals/${questionId}/${decision}`, { method: "POST" }));
}

export async function getReport(questionId: string): Promise<Report> {
  return unwrap<Report>(await fetch(`/api/questions/${questionId}/report`));
}

export function subscribeQuestion(
  questionId: string,
  onEvent: (event: QuestionEvent) => void,
  onTransportError: () => void,
): () => void {
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
