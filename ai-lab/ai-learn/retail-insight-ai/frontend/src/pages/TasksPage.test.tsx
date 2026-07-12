import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { FakeEventSource, jsonResponse } from "../test/page-test-helpers";
import { TasksPage } from "./TasksPage";

describe("TasksPage", () => {
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
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-1",
        data: { task_id: "task-1", status: "queued" },
        error: null,
      }, 202))
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-2",
        data: {
          task_id: "task-1",
          markdown: "# 完了レポート",
          provider: "static",
          created_at: "2026-06-27T00:00:00Z",
        },
        error: null,
      }, 200));
    vi.stubGlobal("fetch", fetchMock);

    render(<TasksPage />);
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
  });
});
