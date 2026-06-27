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
      .mockResolvedValueOnce(new Response(JSON.stringify({
        success: true,
        request_id: "request-1",
        data: { task_id: "task-1", status: "queued" },
        error: null,
      }), { status: 202 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({
        success: true,
        request_id: "request-2",
        data: {
          task_id: "task-1",
          markdown: "# 完了レポート",
          provider: "static",
          created_at: "2026-06-27T00:00:00Z",
        },
        error: null,
      }), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "分析を開始" }));

    await waitFor(() => expect(FakeEventSource.instance.url).toBe("/api/tasks/task-1/events"));
    FakeEventSource.instance.emit("status", {
      task_id: "task-1", sequence: 1, event: "status", message: "Task started",
      status: "running", request_id: "request-1", error_code: null,
      node: "route", report_path: null, created_at: "2026-06-27T00:00:00Z",
    });
    FakeEventSource.instance.emit("done", {
      task_id: "task-1", sequence: 2, event: "done", message: "Task completed",
      status: "completed", request_id: "request-1", error_code: null,
      node: null, report_path: "/api/tasks/task-1/report", created_at: "2026-06-27T00:00:01Z",
    });

    expect(await screen.findByText("# 完了レポート")).toBeInTheDocument();
    expect(screen.getByText("COMPLETED")).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("shows a task creation error", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify({
        success: false,
        request_id: "request-error",
        data: null,
        error: { code: "VALIDATION_ERROR", message: "Request validation failed", detail: {} },
      }), { status: 422 }),
    ));
    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "分析を開始" }));
    expect(await screen.findByRole("alert")).toHaveTextContent(
      "[VALIDATION_ERROR] Request validation failed",
    );
  });

  it("shows the SSE error code and message without loading a report", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(new Response(JSON.stringify({
      success: true,
      request_id: "request-3",
      data: { task_id: "task-3", status: "queued" },
      error: null,
    }), { status: 202 }));
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "分析を開始" }));
    await waitFor(() => expect(FakeEventSource.instance.url).toBe("/api/tasks/task-3/events"));

    FakeEventSource.instance.emit("error", {
      task_id: "task-3", sequence: 2, event: "error", status: "failed",
      message: "Research provider failed", request_id: "request-3",
      error_code: "RESEARCH_PROVIDER_ERROR", node: null, report_path: null,
      created_at: "2026-06-27T00:00:01Z",
    });

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "[RESEARCH_PROVIDER_ERROR] Research provider failed",
    );
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });
});
