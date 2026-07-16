import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { jsonResponse, ragAnswerResponse, retrievalResponse } from "../test/page-test-helpers";
import { RagPage } from "./RagPage";

describe("RagPage", () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("renders only the RAG capability allowed by permission-derived props", () => {
    const { rerender } = render(<RagPage canRetrieve canAnalyze={false} />);
    let workspace = within(screen.getByLabelText("RAG 検索ワークスペース"));
    expect(workspace.getByRole("heading", { name: "文書検索" })).toBeInTheDocument();
    expect(workspace.queryByRole("heading", { name: "Internal RAG 回答" })).not.toBeInTheDocument();

    rerender(<RagPage canRetrieve={false} canAnalyze />);
    workspace = within(screen.getByLabelText("RAG 検索ワークスペース"));
    expect(workspace.queryByRole("heading", { name: "文書検索" })).not.toBeInTheDocument();
    expect(workspace.getByRole("heading", { name: "Internal RAG 回答" })).toBeInTheDocument();
  });

  it("shows retrieval results", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(retrievalResponse([
      {
        document_id: "doc-1",
        chunk_id: "chunk-1",
        chunk_index: 0,
        content_excerpt: "Monthly policy evidence.",
        score: 0.92,
        source: {
          source_type: "upload_form",
          uri: "upload://doc-1/source",
          label: null,
          external_id: null,
        },
        metadata: {
          document_id: "doc-1",
          title: "Monthly Policy",
          description: null,
          owner: "analysis-team",
          created_at: "2026-07-09T00:00:00Z",
          updated_at: "2026-07-09T00:00:00Z",
          version: 1,
          language: "en",
          document_type: "markdown",
          status: "validated",
          tags: ["policy"],
          source: null,
          checksum: "sha256:doc-1",
        },
      },
    ]));
    vi.stubGlobal("fetch", fetchMock);

    render(<RagPage />);
    fireEvent.change(screen.getByLabelText("検索語"), { target: { value: "monthly policy" } });
    fireEvent.click(screen.getByRole("button", { name: "検索する" }));

    expect(await screen.findByRole("status")).toHaveTextContent("検索方式: keyword / 一致件数: 1");
    expect(await screen.findByText("Monthly policy evidence.")).toBeInTheDocument();
    expect(screen.getByText("RAG-BIZ-001")).toBeInTheDocument();
    expect(screen.getByText("POST /api/v1/document-retrieval/search")).toBeInTheDocument();
    expect(screen.getByText("业务测试与源码学习")).toBeInTheDocument();
    expect(screen.getByLabelText("RAG検索 上一步下一步")).toHaveTextContent("上一步：文書管理");
    expect(screen.getByLabelText("RAG検索 上一步下一步")).toHaveTextContent("下一步：分析依頼");
    expect(screen.getByText("如何选择 RAG 输入")).toBeInTheDocument();
    expect(screen.getAllByText(/02_関東地域在庫レポート\.md/).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/検索語：神奈川 配送遅延 夕方欠品/).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/神奈川で夕方欠品が増加した理由は何ですか。/).length).toBeGreaterThan(0);
    expect(screen.getByText(/不推荐：競合店舗はなぜ値下げしましたか。/)).toBeInTheDocument();
    expect(screen.getByText(/Retrieval 成功后才执行 Answer/)).toBeInTheDocument();
    expect(screen.getByText(/results=0 时不建议直接生成 Internal RAG Answer/)).toBeInTheDocument();
    expect(screen.getAllByText(/insufficient_context/).length).toBeGreaterThan(0);
    expect(screen.getByText("综合经营问题的前置资料")).toBeInTheDocument();
    expect(screen.getByText("RAG-BIZ-005")).toBeInTheDocument();
  });

  it("shows empty retrieval state from backend", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValueOnce(retrievalResponse()));

    render(<RagPage />);
    fireEvent.change(screen.getByLabelText("検索語"), { target: { value: "no match" } });
    fireEvent.click(screen.getByRole("button", { name: "検索する" }));

    expect(await screen.findByText("検索結果はありません。")).toBeInTheDocument();
  });

  it("shows grounded internal rag answer and citations", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValueOnce(ragAnswerResponse()));

    render(<RagPage />);
    fireEvent.change(screen.getByLabelText("質問"), { target: { value: "What is the monthly policy?" } });
    fireEvent.click(screen.getByRole("button", { name: "回答を生成" }));

    expect(await screen.findByRole("status")).toHaveTextContent("回答方式: extractive");
    expect(await screen.findByText("Monthly policy evidence.")).toBeInTheDocument();
    expect(await screen.findByText("weak_match")).toBeInTheDocument();
  });

  it("shows internal rag API error", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValueOnce(jsonResponse({
      success: false,
      request_id: "request-rag-error",
      data: null,
      error: { code: "insufficient_context", message: "No usable evidence", detail: {} },
    }, 422)));

    render(<RagPage />);
    fireEvent.change(screen.getByLabelText("質問"), { target: { value: "rare token" } });
    fireEvent.click(screen.getByRole("button", { name: "回答を生成" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("[insufficient_context] No usable evidence");
  });
});
