import type { AnalysisMode, ReportResponse, TaskCreateResponse, TaskEvent } from "./types";

/** 尽量读取 Backend 的 detail；非 JSON 错误仍回退到可诊断的 HTTP 状态。 */
async function parseError(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as { detail?: string };
    return body.detail ?? `HTTP ${response.status}`;
  } catch {
    return `HTTP ${response.status}`;
  }
}

/** 创建异步分析任务；这里只处理 HTTP 合同，不管理 React 页面状态。 */
export async function createTask(question: string, mode: AnalysisMode): Promise<TaskCreateResponse> {
  const response = await fetch("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, mode }),
  });
  if (!response.ok) {
    throw new Error(await parseError(response));
  }
  return response.json() as Promise<TaskCreateResponse>;
}

/** 在收到 done 事件后获取最终报告，避免把大段 Markdown 塞进 SSE。 */
export async function getReport(taskId: string): Promise<ReportResponse> {
  const response = await fetch(`/api/tasks/${taskId}/report`);
  if (!response.ok) {
    throw new Error(await parseError(response));
  }
  return response.json() as Promise<ReportResponse>;
}

/**
 * 订阅任务状态，并返回显式关闭函数。
 * EventSource 会理解 Backend 的 status/done/error 自定义事件；调用方决定如何更新 UI。
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
