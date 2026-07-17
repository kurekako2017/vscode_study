/**
 * React Lifecycle Live Status 关键补测（不扩展业务功能）。
 */
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { useEffect, useRef } from "react";

import App from "../App";
import { LearningTraceProvider, useLearningTrace } from "./LearningTraceContext";
import { TRACE_BUFFER_LIMIT, TRACE_STORAGE_KEY } from "./learningTypes";
import { ADMIN_SESSION } from "../test/auth-test-helpers";
import { LifecycleProbe } from "./LifecycleProbe";

function TraceDump() {
  const trace = useLearningTrace();
  return (
    <div>
      <div data-testid="phase">{trace.components.find((c) => c.isActive)?.phase ?? "none"}</div>
      <div data-testid="record-count">{trace.records.length}</div>
      <div data-testid="reload">{String(trace.isPageReload)}</div>
      <button type="button" onClick={trace.clearTrace}>clear-trace</button>
      <pre data-testid="records">{JSON.stringify(trace.records)}</pre>
    </div>
  );
}

describe("Learning Trace lifecycle critical paths", () => {
  beforeEach(() => {
    sessionStorage.clear();
    vi.restoreAllMocks();
  });

  afterEach(() => {
    cleanup();
    sessionStorage.clear();
  });

  it("records mounting → mounted and increments render/mount counters", async () => {
    render(
      <LearningTraceProvider strictModeEnabled={false}>
        <LifecycleProbe componentId="ProbeA" displayName="ProbeA" isPageRoot hooks={["useState"]}>
          <div>child</div>
        </LifecycleProbe>
        <TraceDump />
      </LearningTraceProvider>,
    );

    await waitFor(() => {
      expect(screen.getByTestId("phase").textContent).toMatch(/mounted|updated/);
    });
    const records = screen.getByTestId("records").textContent ?? "";
    expect(records).toMatch(/mounting|mounted/i);
    expect(records.toLowerCase()).not.toContain("access_token");
    expect(records.toLowerCase()).not.toContain("password");
    expect(records.toLowerCase()).not.toContain("api_key");
  });

  it("marks previous page unmounted after route change in App", async () => {
    render(<App initialSession={ADMIN_SESSION} strictModeEnabled={false} />);
    expect(await screen.findByLabelText("React Lifecycle Live Status")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "RAG検索" }));
    expect(await screen.findByRole("heading", { name: "RAG検索" })).toBeInTheDocument();

    const live = screen.getByLabelText("React Lifecycle Live Status");
    expect(live.textContent).toMatch(/RagPage|Mounted|已挂载|Updated|更新/);
    // 组件树中 Dashboard 应为 unmounted（若仍在列表中）
    const tree = screen.getByLabelText("组件树");
    if (tree.textContent?.includes("DashboardPage")) {
      expect(tree.textContent).toMatch(/DashboardPage[\s\S]*unmounted|unmounted[\s\S]*DashboardPage/i);
    }
  });

  it("records page_reload when navigation type is reload", async () => {
    const spy = vi.spyOn(performance, "getEntriesByType").mockReturnValue([
      { type: "reload" } as PerformanceNavigationTiming,
    ]);
    render(
      <LearningTraceProvider strictModeEnabled={false}>
        <TraceDump />
      </LearningTraceProvider>,
    );
    await waitFor(() => {
      expect(screen.getByTestId("reload").textContent).toBe("true");
    });
    expect(screen.getByTestId("records").textContent).toMatch(/page_reload|页面刷新/);
    spy.mockRestore();
  });

  it("keeps non-empty lifecycle status after app mount (reload-safe UI)", async () => {
    render(<App initialSession={ADMIN_SESSION} strictModeEnabled={false} />);
    const live = await screen.findByLabelText("React Lifecycle Live Status");
    expect(within(live).getByText("当前状态")).toBeInTheDocument();
    expect(within(live).getAllByText(/Mounted|已挂载|Mounting|挂载|Updated|更新/).length).toBeGreaterThan(0);
    expect(within(live).getByText("Render 次数")).toBeInTheDocument();
  });

  it("does not call backend when opening dashboard", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<App initialSession={ADMIN_SESSION} strictModeEnabled={false} />);
    expect(screen.getByRole("heading", { level: 1, name: "Enterprise Retail Intelligence Platform" })).toBeInTheDocument();
    // 仪表盘本身不拉业务 API（Auth 已注入 session，不需要 /users/me）
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("enforces ring buffer limit", async () => {
    render(
      <LearningTraceProvider strictModeEnabled={false}>
        <FloodTrace />
        <TraceDump />
      </LearningTraceProvider>,
    );
    await waitFor(() => {
      const n = Number(screen.getByTestId("record-count").textContent);
      expect(n).toBeLessThanOrEqual(TRACE_BUFFER_LIMIT);
      expect(n).toBeGreaterThan(0);
    });
  });

  it("clearTrace removes sensitive-capable buffer and keeps UI usable", async () => {
    render(
      <LearningTraceProvider strictModeEnabled={false}>
        <LifecycleProbe componentId="ProbeClear" displayName="ProbeClear" isPageRoot>
          <div>x</div>
        </LifecycleProbe>
        <TraceDump />
      </LearningTraceProvider>,
    );
    await waitFor(() => expect(Number(screen.getByTestId("record-count").textContent)).toBeGreaterThan(0));
    fireEvent.click(screen.getByRole("button", { name: "clear-trace" }));
    await waitFor(() => {
      // clear 会再写一条 clear 事件
      expect(Number(screen.getByTestId("record-count").textContent)).toBeLessThanOrEqual(2);
    });
    expect(sessionStorage.getItem(TRACE_STORAGE_KEY)).toBeTruthy();
  });

  it("redacts token-like prop names in prop edges", async () => {
    function PropRecorder() {
      const trace = useLearningTrace();
      return (
        <button
          type="button"
          onClick={() => trace.recordProp("A", "B", "accessToken", "super-secret-token-value")}
        >
          record-prop
        </button>
      );
    }
    render(
      <LearningTraceProvider strictModeEnabled={false}>
        <PropRecorder />
        <TraceDump />
      </LearningTraceProvider>,
    );
    fireEvent.click(screen.getByRole("button", { name: "record-prop" }));
    await waitFor(() => {
      const text = screen.getByTestId("records").textContent ?? "";
      expect(text).toContain("accessToken");
      expect(text).not.toContain("super-secret-token-value");
      expect(text).toMatch(/REDACTED/);
    });
  });
});

function FloodTrace() {
  const trace = useLearningTrace();
  const done = useRef(false);
  useEffect(() => {
    if (done.current) return;
    done.current = true;
    for (let i = 0; i < TRACE_BUFFER_LIMIT + 20; i += 1) {
      trace.pushTrace({ kind: "event", summary: `flood-${i}` });
    }
  }, [trace]);
  return null;
}
