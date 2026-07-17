/**
 * 显式 Lifecycle 探针：mount / update / unmount 写入 Learning Trace。
 *
 * 重要：禁止在 render 阶段同步 setState 到 Trace Provider，否则会无限重渲染。
 * render 次数用 ref 累计，在 effect 中刷入 Trace。
 */

import { useEffect, useRef, type ReactNode } from "react";

import { useLearningTraceOptional } from "./LearningTraceContext";
import type { LearningPage } from "./learningTypes";

interface LifecycleProbeProps {
  componentId: string;
  displayName: string;
  parentId?: string | null;
  page?: LearningPage | string;
  route?: string;
  hooks?: string[];
  /** 是否为当前页面主组件。 */
  isPageRoot?: boolean;
  /**
   * 外部 revision：路由、页面或业务事件变化时递增/变化，触发 update 记录。
   * 不要传入每次 render 都变的随机值。
   */
  revision?: string | number;
  children: ReactNode;
}

export function LifecycleProbe({
  componentId,
  displayName,
  parentId = null,
  page,
  route,
  hooks = [],
  isPageRoot = false,
  revision = "",
  children,
}: LifecycleProbeProps) {
  const trace = useLearningTraceOptional();
  const renderCountRef = useRef(0);
  const mountedRef = useRef(false);
  renderCountRef.current += 1;

  // Mount / Unmount
  useEffect(() => {
    if (!trace) return;
    mountedRef.current = true;
    trace.registerComponent({
      componentId,
      displayName,
      parentId,
      page,
      route,
      hooks,
    });
    trace.markLifecycle(componentId, "mounting", {
      reason: "effect mount start",
      isActive: isPageRoot,
    });
    // 将截至 mount effect 的 render 次数刷入（StrictMode 下可能 > 1）。
    trace.noteRender(componentId, "initial mount render", renderCountRef.current);
    trace.markLifecycle(componentId, "mounted", {
      reason: "useEffect mount completed",
      isActive: isPageRoot,
    });
    for (const hookName of hooks) {
      trace.recordHook(componentId, hookName, "registered for learning");
    }
    return () => {
      mountedRef.current = false;
      trace.markLifecycle(componentId, "unmounting", { reason: "useEffect cleanup" });
      trace.noteUnmount(componentId);
    };
    // 仅绑定组件身份；hooks 列表为静态教学注册。
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [componentId]);

  const skipFirstRevision = useRef(true);
  // Update：仅当外部 revision 变化（路由/页面/业务事件）；跳过 mount 后第一次 effect。
  useEffect(() => {
    if (!trace || !mountedRef.current) return;
    if (skipFirstRevision.current) {
      skipFirstRevision.current = false;
      return;
    }
    if (revision === "" || revision === undefined) return;
    trace.markLifecycle(componentId, "updating", {
      reason: `revision → ${String(revision)}`,
      isActive: isPageRoot,
    });
    trace.noteRender(
      componentId,
      `update after revision (${String(revision)})`,
      renderCountRef.current,
    );
    trace.markLifecycle(componentId, "updated", {
      reason: `revision → ${String(revision)}`,
      isActive: isPageRoot,
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [revision, componentId]);

  return <>{children}</>;
}
