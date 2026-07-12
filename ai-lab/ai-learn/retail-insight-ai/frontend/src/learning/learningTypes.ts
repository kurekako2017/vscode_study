/** 右侧学习面板只保存最近一次页面操作，不承担业务状态或持久化责任。 */
export type LearningPage = "dashboard" | "documents" | "rag" | "tasks" | "approval";

export interface LearningEvent {
  eventName: string;
  stateChanges: string[];
  apiMethod?: string;
  apiPath?: string;
  apiStatus?: string;
  backendFlow?: string[];
  note?: string;
}

export type RecordLearningEvent = (event: LearningEvent) => void;
