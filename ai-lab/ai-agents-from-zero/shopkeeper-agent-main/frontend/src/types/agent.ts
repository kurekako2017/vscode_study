/**
 * 智能体类型定义
 * 定义问数智能体前端使用的 SSE 事件、流程步骤和聊天消息类型
 */
export type ProgressStatus = "running" | "success" | "error";

// 后端在流式执行过程中会不断推送 step 级别的进度状态。
export type ProgressEvent = {
  type: "progress";
  step: string;
  status: ProgressStatus;
};

// 最终查询成功后，后端会把结构化结果放在 data 里返回。
export type ResultEvent = {
  type: "result";
  data: unknown;
};

// 任何阶段出现异常时，后端会推送 error 事件。
export type ErrorEvent = {
  type: "error";
  message: string;
};

// SSE 事件就是这三种之一，前端通过联合类型做区分处理。
export type AgentEvent = ProgressEvent | ResultEvent | ErrorEvent;

// StepState 用来驱动流程图里的节点高亮和状态更新。
export type StepState = {
  step: string;
  status: ProgressStatus;
  updatedAt: number;
};

// 一条聊天消息既可以是用户输入，也可以是助手输出。
export type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  createdAt: number;
  // assistant 消息在流式过程中会先显示 streaming，完成后变成 done。
  status?: "streaming" | "done" | "error";
  steps?: StepState[];
  result?: unknown;
  error?: string;
};
