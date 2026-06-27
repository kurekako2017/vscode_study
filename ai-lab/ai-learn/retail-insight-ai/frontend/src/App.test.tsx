import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import App from "./App";

/** 用可控的内存实现替代浏览器 EventSource，让测试可以主动推送 SSE 事件。 */
class FakeEventSource {
  static instance: FakeEventSource;
  static readonly CLOSED = 2;
  readonly CLOSED = 2;
  readyState = 1;
  onerror: (() => void) | null = null;
  listeners = new Map<string, EventListener>();

  constructor(public readonly url: string) {
    FakeEventSource.instance = this;
  }

  addEventListener(name: string, listener: EventListener) {
    this.listeners.set(name, listener);
  }

  emit(name: string, payload: object) {
    // 测试使用与真实 SSE 相同的 JSON 字符串边界，而不是直接调用 React 状态。
    this.listeners.get(name)?.({ data: JSON.stringify(payload) } as MessageEvent);
  }

  close() {
    this.readyState = FakeEventSource.CLOSED;
  }
}

describe("App", () => {
  beforeEach(() => {
    vi.stubGlobal("EventSource", FakeEventSource);
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("creates a task, consumes SSE, and renders the report", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify({ task_id: "task-1", status: "queued" }), { status: 202 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({
        task_id: "task-1",
        markdown: "# 完了レポート",
        provider: "mock",
        created_at: "2026-06-27T00:00:00Z",
      }), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "分析を開始" }));

    await waitFor(() => expect(FakeEventSource.instance.url).toBe("/api/tasks/task-1/events"));
    FakeEventSource.instance.emit("status", {
      task_id: "task-1", sequence: 1, event: "status", message: "Task started",
      data: { status: "running", node: "route" }, created_at: "2026-06-27T00:00:00Z",
    });
    FakeEventSource.instance.emit("done", {
      task_id: "task-1", sequence: 2, event: "done", message: "Task completed",
      data: { status: "completed" }, created_at: "2026-06-27T00:00:01Z",
    });

    expect(await screen.findByText("# 完了レポート")).toBeInTheDocument();
    expect(screen.getByText("COMPLETED")).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("shows a task creation error", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ detail: "invalid request" }), { status: 422 }),
    ));
    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "分析を開始" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("invalid request");
  });
});
