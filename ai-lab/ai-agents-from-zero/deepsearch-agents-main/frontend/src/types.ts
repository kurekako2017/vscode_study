// 这个文件集中定义前端会反复复用的类型。
// 初学者可以把它理解成“前端和后端约定好的数据结构说明书”。
export type ConnectionState = "connecting" | "connected" | "reconnecting" | "closed";

export type MonitorEventName =
  | "session_created"
  | "tool_start"
  | "assistant_call"
  | "task_result"
  | "task_cancelled"
  | "error"
  | string;

export interface MonitorMessage {
  // type 用来区分这是不是后端推来的监控事件
  type: "monitor_event";
  // event 是更细的事件种类，例如 tool_start / task_result
  event: MonitorEventName;
  // message 是给用户直接看的简短文本
  message: string;
  // data 放结构化上下文，例如工具参数、工作目录路径
  data: Record<string, unknown>;
  timestamp: string;
}

export interface PongMessage {
  type: "pong";
  message: string;
}

export type SocketMessage = MonitorMessage | PongMessage;

export interface TaskResponse {
  // status 一般是 started，表示“任务已经启动”，不是“任务已经执行完”
  status: "started" | string;
  thread_id: string;
}

export interface CancelTaskResponse {
  status: "cancelled" | "cancelling" | string;
  thread_id: string;
  message?: string;
}

export interface UploadResponse {
  status: "uploaded" | string;
  files: string[];
}

export interface HealthResponse {
  status: string;
  backend: string;
  llm: {
    configured: boolean;
    provider: string;
    source: string;
    model: string;
  };
  mysql: {
    host: string;
    port: string;
    configured: boolean;
  };
  services: {
    tavily: boolean;
    local_knowledge_base: boolean;
  };
}

export interface OutputFile {
  // path 是后端真实路径，前端靠它继续请求下载接口
  name: string;
  type: "file" | string;
  path: string;
  size: number;
  mtime: number;
}

export interface FileListResponse {
  files?: OutputFile[];
  error?: string;
}

export interface UploadedItem {
  // raw 是浏览器原始 File 对象，真正上传时要把它塞进 FormData
  uid: string;
  name: string;
  size: number;
  raw: File;
}
