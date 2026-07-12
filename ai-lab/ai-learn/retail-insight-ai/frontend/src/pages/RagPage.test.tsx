import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { jsonResponse, ragAnswerResponse, retrievalResponse } from "../test/page-test-helpers";
import { RagPage } from "./RagPage";

describe("RagPage", () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
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
    expect(screen.getByText("A. Document Retrieval")).toBeInTheDocument();
    expect(screen.getByText("C. insufficient_context")).toBeInTheDocument();
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
