/** 右侧学习面板与 Learning Trace 的稳定合同。 */

export type LearningPage = "dashboard" | "documents" | "rag" | "tasks" | "approval" | "login";

/** 业务页 handler 上报的最近一次操作（兼容既有 onLearningEvent）。 */
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

/** 统一生命周期状态（中英双语 UI）。 */
export type LifecyclePhase =
  | "mounting"
  | "mounted"
  | "updating"
  | "updated"
  | "unmounting"
  | "unmounted"
  | "page_reload"
  | "route_leave"
  | "route_enter";

export const LIFECYCLE_LABELS: Record<LifecyclePhase, string> = {
  mounting: "Mounting / 挂载中",
  mounted: "Mounted / 已挂载",
  updating: "Updating / 更新中",
  updated: "Updated / 已更新",
  unmounting: "Unmounting / 卸载中",
  unmounted: "Unmounted / 已卸载",
  page_reload: "Page Reload / 页面刷新",
  route_leave: "Route Leave / 路由离开",
  route_enter: "Route Enter / 路由进入",
};

export type TraceKind =
  | "lifecycle"
  | "event"
  | "state"
  | "hook"
  | "call"
  | "prop"
  | "route"
  | "navigation";

export interface LearningTraceRecord {
  id: string;
  kind: TraceKind;
  timestamp: string;
  component?: string;
  page?: LearningPage | string;
  route?: string;
  /** 人类可读摘要；不得包含 Token/Password 等敏感原文。 */
  summary: string;
  phase?: LifecyclePhase;
  detail?: string;
  safePayload?: Record<string, string | number | boolean | null>;
}

export interface ComponentLifecycleSnapshot {
  componentId: string;
  displayName: string;
  parentId: string | null;
  page: LearningPage | string;
  route: string;
  phase: LifecyclePhase;
  isMounted: boolean;
  isActive: boolean;
  renderCount: number;
  mountCount: number;
  updateCount: number;
  unmountCount: number;
  lastPhaseAt: string;
  lastUpdateReason: string;
  hooks: string[];
}

export interface PropEdgeSnapshot {
  id: string;
  from: string;
  to: string;
  propName: string;
  safeSummary: string;
  updatedAt: string;
}

export interface StateFlowStep {
  label: string;
  detail: string;
}

export interface PageCatalogEntry {
  page: LearningPage;
  route: string;
  navigation: string;
  component: string;
  step: string;
  businessObject: string;
  whyNeeded: string;
  initialState: string;
  hooks: Array<{ name: string; purpose: string }>;
  sources: Array<{ label: string; path: string; reason: string }>;
  tests: Array<{ label: string; path: string; reason: string }>;
  lifecycleTeaching: Array<{ name: string; detail: string; technologies: string[] }>;
}

export const TRACE_BUFFER_LIMIT = 80;
export const TRACE_STORAGE_KEY = "erip.learning.trace.v1";
