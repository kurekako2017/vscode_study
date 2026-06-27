import type {
  AnalysisMode,
  ApiResponse,
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
  const response = await fetch("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, mode }),
  });
  return unwrapResponse<TaskCreateResponse>(response);
}

/** 在收到 done 事件后获取最终报告，避免把大段 Markdown 塞进 SSE。 */
export async function getReport(taskId: string): Promise<ReportResponse> {
  const response = await fetch(`/api/tasks/${taskId}/report`);
  return unwrapResponse<ReportResponse>(response);
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
  source.onerror = () => {
    if (source.readyState === EventSource.CLOSED) {
      handlers.onTransportError();
    }
  };

  // API Client 不猜测组件生命周期，而是把资源清理权交还调用方。
  return () => source.close();
}
