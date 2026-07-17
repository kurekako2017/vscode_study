/**
 * 集中式前端 Learning Trace。
 *
 * - 不向 Backend 发送任何 Trace
 * - ring buffer 有限长度
 * - Token / password 等敏感字段必须脱敏
 * - 刷新时用 sessionStorage 保留最近安全记录
 */

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";

import {
  LIFECYCLE_LABELS,
  TRACE_BUFFER_LIMIT,
  TRACE_STORAGE_KEY,
  type ComponentLifecycleSnapshot,
  type LearningEvent,
  type LearningPage,
  type LearningTraceRecord,
  type LifecyclePhase,
  type PropEdgeSnapshot,
  type StateFlowStep,
  type TraceKind,
} from "./learningTypes";
import { safeSummary, sanitizeRecord } from "./sanitize";

interface RegisterComponentInput {
  componentId: string;
  displayName: string;
  parentId?: string | null;
  page?: LearningPage | string;
  route?: string;
  hooks?: string[];
}

interface LearningTraceContextValue {
  route: string;
  page: LearningPage | string;
  records: LearningTraceRecord[];
  components: ComponentLifecycleSnapshot[];
  propEdges: PropEdgeSnapshot[];
  latestEvent: LearningEvent | null;
  stateFlow: StateFlowStep[];
  strictModeEnabled: boolean;
  isPageReload: boolean;
  navigationType: string;
  activeComponentId: string | null;
  setRouteContext: (route: string, page: LearningPage | string) => void;
  recordLearningEvent: (event: LearningEvent) => void;
  pushTrace: (input: Omit<LearningTraceRecord, "id" | "timestamp"> & { id?: string; timestamp?: string }) => void;
  registerComponent: (input: RegisterComponentInput) => void;
  markLifecycle: (
    componentId: string,
    phase: LifecyclePhase,
    options?: { reason?: string; isActive?: boolean },
  ) => void;
  noteRender: (componentId: string, reason?: string, absoluteRenderCount?: number) => void;
  noteUnmount: (componentId: string) => void;
  recordProp: (from: string, to: string, propName: string, value: unknown) => void;
  recordStateChange: (component: string, name: string, from: unknown, to: unknown, trigger: string) => void;
  recordHook: (component: string, hookName: string, detail: string) => void;
  recordCall: (component: string, name: string, detail: string) => void;
  clearTrace: () => void;
}

const LearningTraceContext = createContext<LearningTraceContextValue | null>(null);

function nowIso(): string {
  return new Date().toISOString();
}

function makeId(prefix: string): string {
  return `${prefix}-${Math.random().toString(36).slice(2, 10)}-${Date.now().toString(36)}`;
}

function detectNavigationType(): { type: string; isReload: boolean } {
  try {
    const entries = performance.getEntriesByType("navigation") as PerformanceNavigationTiming[];
    const nav = entries[0];
    if (nav?.type) {
      return { type: nav.type, isReload: nav.type === "reload" };
    }
  } catch {
    /* ignore */
  }
  const legacy = (performance as Performance & { navigation?: { type?: number } }).navigation;
  if (legacy?.type === 1) return { type: "reload", isReload: true };
  return { type: "navigate", isReload: false };
}

function loadPersistedRecords(): LearningTraceRecord[] {
  try {
    const raw = sessionStorage.getItem(TRACE_STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as LearningTraceRecord[];
    if (!Array.isArray(parsed)) return [];
    return parsed.slice(-TRACE_BUFFER_LIMIT);
  } catch {
    return [];
  }
}

function persistRecords(records: LearningTraceRecord[]) {
  try {
    // 只持久化安全摘要字段；不写 Token/Password。
    sessionStorage.setItem(TRACE_STORAGE_KEY, JSON.stringify(records.slice(-TRACE_BUFFER_LIMIT)));
  } catch {
    /* ignore quota */
  }
}

const DEFAULT_STATE_FLOW: StateFlowStep[] = [
  { label: "用户事件", detail: "点击、输入或路由切换进入 React 事件系统。" },
  { label: "Event Handler", detail: "页面 handler 处理业务意图并可能调用 API。" },
  { label: "setState / dispatch", detail: "更新 React state 或 Learning Trace（不含敏感原文）。" },
  { label: "React render", detail: "组件函数再次执行，计算下一棵 UI 树。" },
  { label: "DOM 更新", detail: "React 提交变更到浏览器 DOM。" },
];

export function LearningTraceProvider({
  children,
  strictModeEnabled = true,
}: {
  children: ReactNode;
  strictModeEnabled?: boolean;
}) {
  const navInfo = useMemo(() => detectNavigationType(), []);
  const [route, setRoute] = useState(() => window.location.pathname);
  const [page, setPage] = useState<LearningPage | string>("dashboard");
  const [records, setRecords] = useState<LearningTraceRecord[]>(() => loadPersistedRecords());
  const [components, setComponents] = useState<ComponentLifecycleSnapshot[]>([]);
  const [propEdges, setPropEdges] = useState<PropEdgeSnapshot[]>([]);
  const [latestEvent, setLatestEvent] = useState<LearningEvent | null>(null);
  const [activeComponentId, setActiveComponentId] = useState<string | null>(null);
  const bootstrapped = useRef(false);

  const pushTrace = useCallback((
    input: Omit<LearningTraceRecord, "id" | "timestamp"> & { id?: string; timestamp?: string },
  ) => {
    const record: LearningTraceRecord = {
      id: input.id ?? makeId(input.kind),
      timestamp: input.timestamp ?? nowIso(),
      kind: input.kind,
      component: input.component,
      page: input.page,
      route: input.route,
      summary: input.summary,
      phase: input.phase,
      detail: input.detail,
      safePayload: input.safePayload ? sanitizeRecord(input.safePayload as Record<string, unknown>) : undefined,
    };
    setRecords((prev) => {
      const next = [...prev, record].slice(-TRACE_BUFFER_LIMIT);
      persistRecords(next);
      return next;
    });
  }, []);

  useEffect(() => {
    if (bootstrapped.current) return;
    bootstrapped.current = true;
    if (navInfo.isReload) {
      pushTrace({
        kind: "navigation",
        phase: "page_reload",
        summary: `页面刷新 (${LIFECYCLE_LABELS.page_reload})`,
        detail: `navigation.type=${navInfo.type}`,
        route: window.location.pathname,
        safePayload: { navigationType: navInfo.type },
      });
    }
  }, [navInfo.isReload, navInfo.type, pushTrace]);

  const setRouteContext = useCallback((nextRoute: string, nextPage: LearningPage | string) => {
    setRoute((prevRoute) => {
      if (prevRoute && prevRoute !== nextRoute) {
        pushTrace({
          kind: "route",
          phase: "route_leave",
          summary: `离开路由 ${prevRoute}`,
          route: prevRoute,
          page,
        });
        pushTrace({
          kind: "route",
          phase: "route_enter",
          summary: `进入路由 ${nextRoute}`,
          route: nextRoute,
          page: nextPage,
        });
      }
      return nextRoute;
    });
    setPage(nextPage);
  }, [page, pushTrace]);

  const recordLearningEvent = useCallback((event: LearningEvent) => {
    setLatestEvent(event);
    pushTrace({
      kind: "event",
      summary: event.eventName,
      detail: event.apiPath
        ? `${event.apiMethod ?? "API"} ${event.apiPath} · ${event.apiStatus ?? ""}`
        : "本地事件（无 API）",
      page,
      route,
      safePayload: {
        stateChanges: event.stateChanges.join(" | "),
        note: event.note ?? null,
      },
    });
    for (const change of event.stateChanges) {
      pushTrace({
        kind: "state",
        summary: change,
        page,
        route,
        component: String(page),
      });
    }
    if (event.apiPath) {
      pushTrace({
        kind: "call",
        summary: `${event.apiMethod ?? "API"} ${event.apiPath}`,
        detail: event.apiStatus,
        page,
        route,
      });
    }
  }, [page, pushTrace, route]);

  const registerComponent = useCallback((input: RegisterComponentInput) => {
    setComponents((prev) => {
      const existing = prev.find((item) => item.componentId === input.componentId);
      if (existing) {
        return prev.map((item) =>
          item.componentId === input.componentId
            ? {
                ...item,
                displayName: input.displayName,
                parentId: input.parentId ?? item.parentId,
                page: input.page ?? item.page,
                route: input.route ?? item.route,
                hooks: input.hooks ?? item.hooks,
              }
            : item,
        );
      }
      const snapshot: ComponentLifecycleSnapshot = {
        componentId: input.componentId,
        displayName: input.displayName,
        parentId: input.parentId ?? null,
        page: input.page ?? page,
        route: input.route ?? route,
        phase: "mounting",
        isMounted: false,
        isActive: false,
        renderCount: 0,
        mountCount: 0,
        updateCount: 0,
        unmountCount: 0,
        lastPhaseAt: nowIso(),
        lastUpdateReason: "原因未明确",
        hooks: input.hooks ?? [],
      };
      return [...prev, snapshot];
    });
  }, [page, route]);

  const markLifecycle = useCallback((
    componentId: string,
    phase: LifecyclePhase,
    options?: { reason?: string; isActive?: boolean },
  ) => {
    setComponents((prev) =>
      prev.map((item) => {
        if (item.componentId !== componentId) {
          if (options?.isActive) {
            return { ...item, isActive: false };
          }
          return item;
        }
        const becameMounted = phase === "mounted" && item.phase !== "mounted";
        return {
          ...item,
          phase,
          isMounted: phase === "mounted" || phase === "updating" || phase === "updated" || phase === "mounting",
          isActive: options?.isActive ?? (phase === "unmounted" || phase === "unmounting" ? false : item.isActive),
          lastPhaseAt: nowIso(),
          lastUpdateReason: options?.reason ?? item.lastUpdateReason,
          mountCount: becameMounted ? item.mountCount + 1 : item.mountCount,
        };
      }),
    );
    if (options?.isActive) setActiveComponentId(componentId);
    pushTrace({
      kind: "lifecycle",
      phase,
      component: componentId,
      summary: `${componentId}: ${LIFECYCLE_LABELS[phase]}`,
      detail: options?.reason,
      page,
      route,
    });
  }, [page, pushTrace, route]);

  const noteRender = useCallback((componentId: string, reason?: string, absoluteRenderCount?: number) => {
    setComponents((prev) =>
      prev.map((item) => {
        if (item.componentId !== componentId) return item;
        const nextRender = absoluteRenderCount ?? item.renderCount + 1;
        const isFirstBatch = item.renderCount === 0;
        return {
          ...item,
          renderCount: nextRender,
          updateCount: isFirstBatch ? item.updateCount : item.updateCount + 1,
          phase: isFirstBatch ? "mounted" : "updated",
          isMounted: true,
          isActive: true,
          lastPhaseAt: nowIso(),
          lastUpdateReason: reason ?? (isFirstBatch ? "initial mount render" : "原因未明确"),
        };
      }),
    );
    setActiveComponentId(componentId);
  }, []);

  const noteUnmount = useCallback((componentId: string) => {
    setComponents((prev) =>
      prev.map((item) =>
        item.componentId === componentId
          ? {
              ...item,
              phase: "unmounted",
              isMounted: false,
              isActive: false,
              unmountCount: item.unmountCount + 1,
              lastPhaseAt: nowIso(),
            }
          : item,
      ),
    );
    pushTrace({
      kind: "lifecycle",
      phase: "unmounted",
      component: componentId,
      summary: `${componentId}: ${LIFECYCLE_LABELS.unmounted}`,
      page,
      route,
    });
  }, [page, pushTrace, route]);

  const recordProp = useCallback((from: string, to: string, propName: string, value: unknown) => {
    const edge: PropEdgeSnapshot = {
      id: makeId("prop"),
      from,
      to,
      propName,
      safeSummary: safeSummary(value, propName),
      updatedAt: nowIso(),
    };
    setPropEdges((prev) => {
      const filtered = prev.filter((item) => !(item.from === from && item.to === to && item.propName === propName));
      return [...filtered, edge].slice(-40);
    });
    pushTrace({
      kind: "prop",
      summary: `${from} → ${to}.${propName}`,
      detail: edge.safeSummary,
      component: to,
      page,
      route,
    });
  }, [page, pushTrace, route]);

  const recordStateChange = useCallback((
    component: string,
    name: string,
    from: unknown,
    to: unknown,
    trigger: string,
  ) => {
    pushTrace({
      kind: "state",
      component,
      summary: `${name}: ${safeSummary(from, name)} → ${safeSummary(to, name)}`,
      detail: `trigger=${trigger}`,
      page,
      route,
    });
  }, [page, pushTrace, route]);

  const recordHook = useCallback((component: string, hookName: string, detail: string) => {
    pushTrace({
      kind: "hook",
      component,
      summary: hookName,
      detail,
      page,
      route,
    });
  }, [page, pushTrace, route]);

  const recordCall = useCallback((component: string, name: string, detail: string) => {
    pushTrace({
      kind: "call",
      component,
      summary: name,
      detail,
      page,
      route,
    });
  }, [page, pushTrace, route]);

  const clearTrace = useCallback(() => {
    setRecords([]);
    setLatestEvent(null);
    setPropEdges([]);
    try {
      sessionStorage.removeItem(TRACE_STORAGE_KEY);
    } catch {
      /* ignore */
    }
    pushTrace({
      kind: "event",
      summary: "clearTrace()",
      detail: "学习 Trace 已清空（仅本地）",
    });
  }, [pushTrace]);

  const value = useMemo<LearningTraceContextValue>(() => ({
    route,
    page,
    records,
    components,
    propEdges,
    latestEvent,
    stateFlow: DEFAULT_STATE_FLOW,
    strictModeEnabled,
    isPageReload: navInfo.isReload,
    navigationType: navInfo.type,
    activeComponentId,
    setRouteContext,
    recordLearningEvent,
    pushTrace,
    registerComponent,
    markLifecycle,
    noteRender,
    noteUnmount,
    recordProp,
    recordStateChange,
    recordHook,
    recordCall,
    clearTrace,
  }), [
    route, page, records, components, propEdges, latestEvent, strictModeEnabled,
    navInfo.isReload, navInfo.type, activeComponentId, setRouteContext, recordLearningEvent,
    pushTrace, registerComponent, markLifecycle, noteRender, noteUnmount, recordProp,
    recordStateChange, recordHook, recordCall, clearTrace,
  ]);

  return (
    <LearningTraceContext.Provider value={value}>
      {children}
    </LearningTraceContext.Provider>
  );
}

export function useLearningTrace(): LearningTraceContextValue {
  const ctx = useContext(LearningTraceContext);
  if (!ctx) {
    throw new Error("useLearningTrace must be used within LearningTraceProvider");
  }
  return ctx;
}

/** 可选读取：LearningSidebar 在 Provider 外测试时返回 null。 */
export function useLearningTraceOptional(): LearningTraceContextValue | null {
  return useContext(LearningTraceContext);
}

export function useLifecycleTrace() {
  const trace = useLearningTrace();
  return {
    registerComponent: trace.registerComponent,
    markLifecycle: trace.markLifecycle,
    noteRender: trace.noteRender,
    noteUnmount: trace.noteUnmount,
    components: trace.components,
    activeComponentId: trace.activeComponentId,
  };
}

export function useEventTrace() {
  const trace = useLearningTrace();
  return {
    recordLearningEvent: trace.recordLearningEvent,
    latestEvent: trace.latestEvent,
    events: trace.records.filter((item) => item.kind === "event"),
  };
}

export function useStateTrace() {
  const trace = useLearningTrace();
  return {
    recordStateChange: trace.recordStateChange,
    stateRecords: trace.records.filter((item) => item.kind === "state"),
    stateFlow: trace.stateFlow,
  };
}

export function useCallTrace() {
  const trace = useLearningTrace();
  return {
    recordCall: trace.recordCall,
    calls: trace.records.filter((item) => item.kind === "call"),
  };
}

export type { TraceKind };
