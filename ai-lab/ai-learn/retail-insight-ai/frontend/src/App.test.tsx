import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import App from "./App";

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
    expect(screen.getByText("1. 文書管理")).toBeInTheDocument();
    expect(screen.getByText("4. 承認管理")).toBeInTheDocument();
  });

  it("highlights the current page in top navigation", async () => {
    render(<App />);

    expect(screen.getByRole("button", { name: "学习总览" })).toHaveAttribute("aria-current", "page");
    fireEvent.click(screen.getByRole("button", { name: "文書管理" }));
    expect(screen.getByRole("button", { name: "文書管理" })).toHaveAttribute("aria-current", "page");
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
    expect(screen.getByText("RagPage")).toBeInTheDocument();
    expect(screen.getAllByText("POST /api/v1/internal-rag/answer").length).toBeGreaterThan(0);
  });

  it("records a local-only clear action in the learning sidebar", () => {
    render(<App />);

    fireEvent.click(screen.getByRole("button", { name: "RAG検索" }));
    fireEvent.click(screen.getByRole("button", { name: "結果をクリア" }));

    expect(screen.getByText("clearRetrievalResult()")).toBeInTheDocument();
    expect(screen.getByText(/没有 API 请求/)).toBeInTheDocument();
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
