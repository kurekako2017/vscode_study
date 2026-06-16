// 这个文件只做一件事：把后端接口封装成前端可复用的函数。
// 组件层不需要关心 fetch 细节，只要调用 startTask / cancelTask 这些函数即可。
import { API_BASE_URL } from "./config";
import type {
  CancelTaskResponse,
  FileListResponse,
  HealthResponse,
  TaskResponse,
  UploadResponse
} from "../types";

function apiUrl(path: string): string {
  return `${API_BASE_URL}${path}`;
}

async function requestJson<T>(input: RequestInfo | URL, init?: RequestInit): Promise<T> {
  // 统一的请求入口：
  // 1. 发请求
  // 2. 自动判断返回的是 JSON 还是纯文本
  // 3. 非 2xx 时抛出 Error，让上层统一处理
  const response = await fetch(input, init);
  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const message =
      typeof payload === "object" && payload && "detail" in payload
        ? String(payload.detail)
        : `HTTP ${response.status}`;
    throw new Error(message);
  }

  return payload as T;
}

export async function startTask(query: string, threadId: string): Promise<TaskResponse> {
  // 后端依赖 thread_id 把 HTTP 任务、WebSocket 和文件目录绑在一起，
  // 所以前端每次发任务时都要把当前 threadId 带上。
  return requestJson<TaskResponse>(apiUrl("/api/task"), {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      query,
      thread_id: threadId
    })
  });
}

export async function cancelTask(threadId: string): Promise<CancelTaskResponse> {
  return requestJson<CancelTaskResponse>(apiUrl(`/api/task/${encodeURIComponent(threadId)}/cancel`), {
    method: "POST"
  });
}

export async function uploadSessionFiles(
  files: File[],
  threadId: string
): Promise<UploadResponse> {
  // 文件上传必须用 FormData，不能像普通 JSON 请求那样 stringify。
  const formData = new FormData();
  formData.append("thread_id", threadId);
  files.forEach((file) => formData.append("files", file));

  return requestJson<UploadResponse>(apiUrl("/api/upload"), {
    method: "POST",
    body: formData
  });
}

export async function getHealthStatus(): Promise<HealthResponse> {
  return requestJson<HealthResponse>(apiUrl("/api/health"));
}

export async function listSessionFiles(path: string): Promise<FileListResponse> {
  const url = new URL(apiUrl("/api/files"));
  url.searchParams.set("path", path);
  return requestJson<FileListResponse>(url);
}

export function getDownloadUrl(path: string): string {
  const url = new URL(apiUrl("/api/download"));
  url.searchParams.set("path", path);
  return url.toString();
}
