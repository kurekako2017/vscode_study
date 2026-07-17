import { useLearningTraceOptional } from "../learning/LearningTraceContext";
import { pageCatalog } from "../learning/pageCatalog";
import {
  LIFECYCLE_LABELS,
  type LearningEvent,
  type LearningPage,
  type LifecyclePhase,
} from "../learning/learningTypes";

interface LearningSidebarProps {
  page: LearningPage;
  latestEvent: LearningEvent | null;
  route?: string;
}

function eventSummary(event: LearningEvent | null) {
  if (event === null) {
    return {
      title: "尚未操作",
      detail: "当前显示页面初始状态。执行一次页面操作后，这里会替换为本次真实 handler、API 与 state 变化。",
    };
  }
  const transport = event.apiPath
    ? `${event.apiMethod ?? "API"} ${event.apiPath} · ${event.apiStatus ?? "请求中"}`
    : "本次操作不发送 API 请求";
  return { title: event.eventName, detail: transport };
}

function formatTime(iso: string): string {
  try {
    return new Date(iso).toLocaleTimeString("zh-CN", { hour12: false });
  } catch {
    return iso;
  }
}

function phaseBadge(phase: LifecyclePhase | undefined): string {
  if (!phase) return "Mounted / 已挂载";
  return LIFECYCLE_LABELS[phase] ?? phase;
}

/**
 * LearningSidebar：实时学习面板。
 *
 * 栏目顺序固定：路由 → 页面 → Lifecycle Live → 组件树 → Hook → Props →
 * 事件 → 状态 → 流程 → Hook 监视器 → 源码 → 测试 → 调用 → StrictMode → 教学说明。
 *
 * 不发送 Backend 请求；不展示 Token/Password。
 */
export function LearningSidebar({ page, latestEvent, route }: LearningSidebarProps) {
  const trace = useLearningTraceOptional();
  const info = pageCatalog[page] ?? pageCatalog.dashboard;
  const effectiveRoute = route ?? trace?.route ?? info.route;
  const currentEvent = eventSummary(latestEvent ?? trace?.latestEvent ?? null);

  const components = trace?.components ?? [];
  const active = components.find((item) => item.isActive && item.isMounted)
    ?? components.find((item) => item.displayName === info.component && item.isMounted)
    ?? components.find((item) => item.isMounted)
    ?? null;

  const lifecycleRecords = (trace?.records ?? [])
    .filter((item) => item.kind === "lifecycle" || item.phase === "page_reload" || item.kind === "route")
    .slice(-8)
    .reverse();

  const recentEvents = (trace?.records ?? [])
    .filter((item) => item.kind === "event")
    .slice(-6)
    .reverse();

  const recentStates = (trace?.records ?? [])
    .filter((item) => item.kind === "state")
    .slice(-6)
    .reverse();

  const recentHooks = (trace?.records ?? [])
    .filter((item) => item.kind === "hook")
    .slice(-6)
    .reverse();

  const recentCalls = (trace?.records ?? [])
    .filter((item) => item.kind === "call")
    .slice(-6)
    .reverse();

  const propEdges = (trace?.propEdges ?? []).slice(-8).reverse();
  const stateFlow = trace?.stateFlow ?? [];

  return (
    <aside className="learning-sidebar" aria-label="固定学习面板">
      <div className="learning-sidebar-scroll">
        <div className="learning-sidebar-heading">
          <p className="page-eyebrow">ERIP / REACT MODERN LEARNING</p>
          <h2>实时学习面板</h2>
          <p>{info.navigation} · {info.component} · {info.step}</p>
        </div>

        {/* 01 当前路由 */}
        <section aria-label="当前路由">
          <h3>01 当前路由</h3>
          <code>{effectiveRoute}</code>
          <small>
            导航类型：{trace?.navigationType ?? "navigate"}
            {trace?.isPageReload ? " · 本次为 page_reload" : ""}
          </small>
        </section>

        {/* 02 当前页面 */}
        <section aria-label="当前页面">
          <h3>02 当前页面</h3>
          <strong>{info.navigation} · {info.component}</strong>
          <p>{info.businessObject}</p>
          <p className="learning-note">{info.whyNeeded}</p>
          <p className="learning-initial-state"><strong>初始：</strong>{info.initialState}</p>
        </section>

        {/* 03 React Lifecycle Live Status */}
        <section className="learning-live lifecycle-live" aria-live="polite" aria-label="React Lifecycle Live Status">
          <h3>03 React Lifecycle Live Status</h3>
          <div className="lifecycle-status-grid">
            <div>
              <dt>当前状态</dt>
              <dd><strong>{phaseBadge(active?.phase ?? "mounted")}</strong></dd>
            </div>
            <div>
              <dt>当前组件</dt>
              <dd>{active?.displayName ?? info.component}</dd>
            </div>
            <div>
              <dt>仍 Mounted</dt>
              <dd>{active?.isMounted === false ? "否" : "是"}</dd>
            </div>
            <div>
              <dt>Render 次数</dt>
              <dd>{active?.renderCount ?? 0}</dd>
            </div>
            <div>
              <dt>Mount 次数</dt>
              <dd>{active?.mountCount ?? 0}</dd>
            </div>
            <div>
              <dt>Update 次数</dt>
              <dd>{active?.updateCount ?? 0}</dd>
            </div>
            <div>
              <dt>Unmount 次数</dt>
              <dd>{active?.unmountCount ?? 0}</dd>
            </div>
            <div>
              <dt>最近变化时间</dt>
              <dd>{active ? formatTime(active.lastPhaseAt) : "—"}</dd>
            </div>
          </div>
          <p>
            <strong>最近原因：</strong>
            {active?.lastUpdateReason ?? (trace?.isPageReload ? "page_reload → mounting → mounted" : "初始展示")}
          </p>
          <div className="lifecycle-recent">
            <strong>最近生命周期记录</strong>
            {lifecycleRecords.length === 0 ? (
              <small>等待组件 mount 探针上报…</small>
            ) : (
              <ul className="learning-source-list">
                {lifecycleRecords.map((item) => (
                  <li key={item.id}>
                    <strong>{item.phase ? LIFECYCLE_LABELS[item.phase] : item.kind}</strong>
                    <code>{formatTime(item.timestamp)} · {item.summary}</code>
                    {item.detail && <small>{item.detail}</small>}
                  </li>
                ))}
              </ul>
            )}
          </div>
          {trace && (
            <button type="button" className="secondary-button lifecycle-clear" onClick={trace.clearTrace}>
              清空学习 Trace
            </button>
          )}
        </section>

        {/* 04 组件树 */}
        <section aria-label="组件树">
          <h3>04 组件树</h3>
          {components.length === 0 ? (
            <small>组件探针尚未注册。</small>
          ) : (
            <ul className="learning-source-list component-tree">
              {components.map((item) => (
                <li key={item.componentId} data-active={item.isActive && item.isMounted ? "true" : "false"}>
                  <strong>
                    {item.displayName}
                    {item.isActive && item.isMounted ? " · 当前页" : ""}
                    {!item.isMounted ? " · unmounted" : ""}
                  </strong>
                  <code>
                    {item.phase} · render {item.renderCount} · parent {item.parentId ?? "root"}
                  </code>
                  <small>{item.route} · {item.page}</small>
                </li>
              ))}
            </ul>
          )}
        </section>

        {/* 05 使用的 Hook */}
        <section aria-label="使用的 Hook">
          <h3>05 使用的 Hook</h3>
          <ul className="learning-source-list">
            {info.hooks.map((hook) => (
              <li key={hook.name}>
                <strong>{hook.name}</strong>
                <small>{hook.purpose}</small>
              </li>
            ))}
          </ul>
        </section>

        {/* 06 Props 传递 */}
        <section aria-label="Props 传递">
          <h3>06 Props 传递</h3>
          {propEdges.length === 0 ? (
            <small>尚无 Props 学习边；切换页面后会记录主要父→子 Props 安全摘要。</small>
          ) : (
            <ul className="learning-source-list">
              {propEdges.map((edge) => (
                <li key={edge.id}>
                  <strong>{edge.from} → {edge.to}</strong>
                  <code>{edge.propName} = {edge.safeSummary}</code>
                  <small>{formatTime(edge.updatedAt)}</small>
                </li>
              ))}
            </ul>
          )}
        </section>

        {/* 07 最近事件 */}
        <section className="learning-live" aria-live="polite" aria-label="最近事件">
          <h3>07 最近事件</h3>
          <strong>{currentEvent.title}</strong>
          <p>{currentEvent.detail}</p>
          {(latestEvent ?? trace?.latestEvent)?.stateChanges?.map((change) => (
            <code key={change}>{change}</code>
          ))}
          {(latestEvent ?? trace?.latestEvent)?.note && (
            <p className="learning-note">{(latestEvent ?? trace?.latestEvent)?.note}</p>
          )}
          {recentEvents.length > 0 && (
            <ul className="learning-source-list">
              {recentEvents.map((item) => (
                <li key={item.id}>
                  <code>{formatTime(item.timestamp)} · {item.summary}</code>
                </li>
              ))}
            </ul>
          )}
        </section>

        {/* 08 最近状态变化 */}
        <section aria-label="最近状态变化">
          <h3>08 最近状态变化</h3>
          {recentStates.length === 0 ? (
            <small>尚无 state 变化记录。页面 handler 上报后会出现在这里。</small>
          ) : (
            <ul className="learning-source-list">
              {recentStates.map((item) => (
                <li key={item.id}>
                  <code>{formatTime(item.timestamp)} · {item.summary}</code>
                  {item.detail && <small>{item.detail}</small>}
                </li>
              ))}
            </ul>
          )}
        </section>

        {/* 09 State 变化流程 */}
        <section aria-label="State 变化流程">
          <h3>09 State 变化流程</h3>
          <ol className="learning-lifecycle">
            {stateFlow.map((step, index) => (
              <li key={step.label}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                <div>
                  <strong>{step.label}</strong>
                  <small>{step.detail}</small>
                </div>
              </li>
            ))}
          </ol>
        </section>

        {/* 10 Hook 监视器 */}
        <section aria-label="Hook 监视器">
          <h3>10 Hook 监视器</h3>
          {recentHooks.length === 0 ? (
            <small>LifecycleProbe 注册 Hook 学习用途后显示于此。</small>
          ) : (
            <ul className="learning-source-list">
              {recentHooks.map((item) => (
                <li key={item.id}>
                  <strong>{item.summary}</strong>
                  <code>{item.component} · {formatTime(item.timestamp)}</code>
                  {item.detail && <small>{item.detail}</small>}
                </li>
              ))}
            </ul>
          )}
        </section>

        {/* 11 对应源码文件 */}
        <section aria-label="对应源码文件">
          <h3>11 对应源码文件</h3>
          <p className="source-hint">先读页面 handler，再顺着 API 适配层进入 Router 与业务边界。</p>
          <ul className="learning-source-list">
            {info.sources.map((source) => (
              <li key={source.path}>
                <strong>{source.label}</strong>
                <code>{source.path}</code>
                <small>{source.reason}</small>
              </li>
            ))}
          </ul>
          {(latestEvent ?? trace?.latestEvent)?.backendFlow && (
            <div className="learning-current-flow">
              <strong>本次操作链路</strong>
              <code>{(latestEvent ?? trace?.latestEvent)?.backendFlow?.join(" → ")}</code>
            </div>
          )}
        </section>

        {/* 12 对应测试文件 */}
        <section aria-label="对应测试文件">
          <h3>12 对应测试文件</h3>
          <ul className="learning-source-list">
            {info.tests.map((test) => (
              <li key={test.path}>
                <strong>{test.label}</strong>
                <code>{test.path}</code>
                <small>{test.reason}</small>
              </li>
            ))}
          </ul>
        </section>

        {/* 13 最近调用记录 */}
        <section aria-label="最近调用记录">
          <h3>13 最近调用记录</h3>
          {recentCalls.length === 0 ? (
            <small>API / handler 调用会显示在此（不含 Authorization 原文）。</small>
          ) : (
            <ul className="learning-source-list">
              {recentCalls.map((item) => (
                <li key={item.id}>
                  <code>{formatTime(item.timestamp)} · {item.summary}</code>
                  {item.detail && <small>{item.detail}</small>}
                </li>
              ))}
            </ul>
          )}
        </section>

        {/* 14 StrictMode */}
        <section aria-label="StrictMode">
          <h3>14 StrictMode</h3>
          <p>
            当前入口：<strong>{trace?.strictModeEnabled === false ? "未包裹 / 测试环境" : "已启用"}</strong>
          </p>
          <small>
            `main.tsx` 使用 React StrictMode。开发环境可能对 effect 执行两次，这是 React 帮助发现不安全副作用的行为，不是业务重复提交。
          </small>
        </section>

        {/* 15 React Lifecycle 教学说明（保留原教学） */}
        <section aria-label="React Lifecycle 教学说明">
          <h3>15 React Lifecycle 教学说明</h3>
          <p className="learning-initial-state"><strong>初始：</strong>{info.initialState}</p>
          <ol className="learning-lifecycle">
            {info.lifecycleTeaching.map((item, index) => (
              <li key={item.name}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                <div>
                  <strong>{item.name}</strong>
                  <small>{item.detail}</small>
                  <small className="learning-technology">
                    {item.technologies.map((technology) => `【${technology}】`).join(" ")}
                  </small>
                </div>
              </li>
            ))}
          </ol>
        </section>
      </div>
    </aside>
  );
}
