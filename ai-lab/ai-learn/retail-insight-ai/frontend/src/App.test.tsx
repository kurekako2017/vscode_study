import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import App from "./App";
import { LearningSidebar } from "./components/LearningSidebar";
import { FakeEventSource, jsonResponse } from "./test/page-test-helpers";

describe("App navigation", () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("shows dashboard by default with current runtime facts", async () => {
    render(<App />);

    expect(screen.getByRole("heading", { level: 1, name: "Enterprise Retail Intelligence Platform" })).toBeInTheDocument();
    expect(screen.getByText("数据存储")).toBeInTheDocument();
    expect(screen.getByText("InMemory")).toBeInTheDocument();
    expect(screen.getAllByText("真实 LLM").length).toBeGreaterThan(0);
    expect(screen.getAllByText("未启用").length).toBeGreaterThan(0);
    expect(screen.getByLabelText("固定学习面板")).toHaveClass("learning-sidebar");
    expect(screen.getByText("实时学习面板")).toBeInTheDocument();
    expect(screen.getByText("尚未操作")).toBeInTheDocument();
  });

  it("highlights the current page in top navigation", async () => {
    render(<App />);

    expect(screen.getByRole("button", { name: "学习总览" })).toHaveAttribute("aria-current", "page");
    fireEvent.click(screen.getByRole("button", { name: "文書管理" }));
    expect(screen.getByRole("button", { name: "文書管理" })).toHaveAttribute("aria-current", "page");
  });

  it("uses the document-first enterprise navigation order", () => {
    render(<App />);

    expect(within(screen.getByRole("navigation", { name: "主要ページ" })).getAllByRole("button").map((button) => button.textContent)).toEqual([
      "学习总览",
      "文書管理",
      "RAG検索",
      "分析依頼",
      "承認管理",
    ]);
    expect(within(screen.getByLabelText("企业业务流程卡片")).getAllByRole("button").map((button) => button.textContent)).toEqual([
      "文書管理を開く",
      "RAG検索を開く",
      "分析依頼を開く",
      "承認管理を開く",
    ]);
  });

  it("shows each page's business object, lifecycle, and source locations", () => {
    const { rerender } = render(<LearningSidebar page="documents" latestEvent={null} />);
    expect(screen.getByText(/文書管理 · DocumentsPage · 1 \/ 4/)).toBeInTheDocument();
    expect(screen.getByText("02 当前业务对象")).toBeInTheDocument();
    expect(screen.getByText(/Scenario01 的销售、库存、促销、顾客和竞品内部资料/)).toBeInTheDocument();
    expect(screen.getByText("04 页面生命周期")).toBeInTheDocument();
    expect(screen.getByText("05 源码定位")).toBeInTheDocument();
    expect(screen.getByText("frontend/src/pages/DocumentsPage.tsx")).toBeInTheDocument();

    rerender(<LearningSidebar page="rag" latestEvent={null} />);
    expect(screen.getByText(/RAG検索 · RagPage · 2 \/ 4/)).toBeInTheDocument();
    expect(screen.getByText(/固定逻辑回答/)).toBeInTheDocument();

    rerender(<LearningSidebar page="tasks" latestEvent={null} />);
    expect(screen.getByText(/分析依頼 · TasksPage · 3 \/ 4/)).toBeInTheDocument();
    expect(screen.getByText(/初始为 idle；没有 task_id、SSE 事件或 report/)).toBeInTheDocument();
    expect(screen.getByText("Stream")).toBeInTheDocument();
    expect(screen.getByText(/【BackgroundTasks】.*【LangGraph】/)).toBeInTheDocument();
    expect(screen.getAllByText(/【SSE \/ EventSource】/)).toHaveLength(2);
    expect(screen.getByText("frontend/src/pages/TasksPage.tsx")).toBeInTheDocument();

    rerender(<LearningSidebar page="approval" latestEvent={null} />);
    expect(screen.getByText(/承認管理 · ApprovalPage · 4 \/ 4/)).toBeInTheDocument();
    expect(screen.getByText(/report_version_id 与审批审计事件/)).toBeInTheDocument();
    expect(screen.getByText(/【AuditMiddleware】/)).toBeInTheDocument();
  });

  it("shows the latest handler, state changes, and backend flow without owning business state", () => {
    render(<LearningSidebar
      page="tasks"
      latestEvent={{
        eventName: "submit()",
        apiMethod: "POST",
        apiPath: "/api/tasks",
        apiStatus: "202 Accepted",
        stateChanges: ["taskId: null → task-learning-1", "status: queued"],
        backendFlow: ["tasks.py create_task()", "TaskService.create_task()"],
      }}
    />);

    expect(screen.getByText("submit()")).toBeInTheDocument();
    expect(screen.getByText("POST /api/tasks · 202 Accepted")).toBeInTheDocument();
    expect(screen.getByText("taskId: null → task-learning-1")).toBeInTheDocument();
    expect(screen.getByText("本次操作链路")).toBeInTheDocument();
    expect(screen.getByText("tasks.py create_task() → TaskService.create_task()")).toBeInTheDocument();
  });

  it("records the Tasks submit, SSE, and report API flow in the learning sidebar", async () => {
    vi.stubGlobal("EventSource", FakeEventSource);
    vi.stubGlobal("fetch", vi.fn()
      .mockResolvedValueOnce(jsonResponse({
        success: true, request_id: "request-task-create", data: { task_id: "task-learning-1", status: "queued" }, error: null,
      }, 202))
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-task-report",
        data: { task_id: "task-learning-1", markdown: "# 学习报告", provider: "static", created_at: "2026-07-12T00:00:00Z" },
        error: null,
      }, 200)));

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "分析依頼" }));
    fireEvent.change(screen.getByLabelText("確認したい経営課題"), { target: { value: "関東飲料の売上を確認" } });
    fireEvent.click(screen.getByRole("button", { name: "分析を開始" }));

    await waitFor(() => expect(FakeEventSource.instance.url).toBe("/api/tasks/task-learning-1/events"));
    expect(screen.getAllByText("submit()").length).toBeGreaterThan(0);
    expect(screen.getByText("POST /api/tasks · 202 Accepted")).toBeInTheDocument();

    FakeEventSource.instance.emit("done", {
      task_id: "task-learning-1", sequence: 1, event: "done", message: "Task completed",
      status: "completed", request_id: "request-task-create", error_code: null,
      node: null, report_path: "/api/tasks/task-learning-1/report", created_at: "2026-07-12T00:00:01Z",
    });

    expect(await screen.findByText("# 学习报告")).toBeInTheDocument();
    expect(screen.getByText("loadReport()")).toBeInTheDocument();
    expect(screen.getByText(/GET \/api\/tasks\/task-learning-1\/report/)).toBeInTheDocument();
  });

  it("navigates to tasks from dashboard shortcut", async () => {
    render(<App />);

    fireEvent.click(screen.getByRole("button", { name: "分析依頼を開く" }));

    expect(screen.getAllByRole("heading", { name: "分析依頼" }).length).toBeGreaterThan(0);
    expect(screen.getByText("分析依頼を作成し、SSE の進捗と現在のローカルワークフローが生成したレポートを確認します。")).toBeInTheDocument();
  });

  it("navigates to documents from dashboard shortcut", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      success: true,
      request_id: "request-doc-list",
      data: { items: [], next_cursor: null },
      error: null,
    }), { status: 200 })));

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "文書管理を開く" }));

    expect(await screen.findByRole("heading", { name: "文書管理" })).toBeInTheDocument();
  });

  it("navigates to rag from dashboard shortcut", async () => {
    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "RAG検索を開く" }));

    expect(screen.getByRole("heading", { name: "RAG検索" })).toBeInTheDocument();
    expect(screen.getByText(/RAG検索 · RagPage · 2 \/ 4/)).toBeInTheDocument();
    expect(screen.getAllByText("POST /api/v1/internal-rag/answer").length).toBeGreaterThan(0);
  });

  it("records a local-only clear action in the learning sidebar", () => {
    render(<App />);

    fireEvent.click(screen.getByRole("button", { name: "RAG検索" }));
    fireEvent.click(screen.getByRole("button", { name: "結果をクリア" }));

    expect(screen.getByText("clearRetrievalResult()")).toBeInTheDocument();
    expect(screen.getByText("本次操作不发送 API 请求")).toBeInTheDocument();
  });

  it("explains insufficient_context as a backend evidence result in the learning sidebar", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      success: false,
      request_id: "request-rag-insufficient-context",
      data: null,
      error: { code: "insufficient_context", message: "No usable evidence", detail: {} },
    }), { status: 422 })));

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "RAG検索" }));
    fireEvent.change(screen.getByLabelText("質問"), { target: { value: "関東飲料の未登録要因" } });
    fireEvent.click(screen.getByRole("button", { name: "回答を生成" }));

    expect(await screen.findByText(/Backend 未找到足够的相关 Chunk/)).toBeInTheDocument();
    expect(screen.getAllByText("POST /api/v1/internal-rag/answer").length).toBeGreaterThan(0);
    expect(screen.getByText(/422 Unprocessable Entity/)).toBeInTheDocument();
  });

  it("navigates to approval from dashboard shortcut", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      success: true,
      request_id: "request-approval-list",
      data: { items: [], next_cursor: null },
      error: null,
    }), { status: 200 })));

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "承認管理を開く" }));

    expect(await screen.findByRole("heading", { name: "承認管理" })).toBeInTheDocument();
  });
});
