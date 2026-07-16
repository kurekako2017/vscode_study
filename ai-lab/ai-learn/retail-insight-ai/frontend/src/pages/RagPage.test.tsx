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

  const evidenceItem = {
    document_id: "doc-ai", chunk_id: "chunk-ai", chunk_index: 0,
    content_excerpt: "Controlled AI evidence.", score: 0.95,
    source: { source_type: "upload", uri: "upload://ai", label: null, external_id: null },
    metadata: { document_id: "doc-ai", title: "AI Evidence", description: null, owner: "team",
      created_at: "2026-07-17T00:00:00Z", updated_at: "2026-07-17T00:00:00Z", version: 1,
      language: "en", document_type: "text", status: "uploaded", tags: [], source: null, checksum: "sha256:ai" },
  };

  async function showEvidence(fetchMock: ReturnType<typeof vi.fn>, canAnalyze = true) {
    vi.stubGlobal("fetch", fetchMock);
    render(<RagPage canAnalyze={canAnalyze} />);
    fireEvent.change(screen.getByLabelText("検索語"), { target: { value: "controlled evidence" } });
    fireEvent.click(screen.getByRole("button", { name: "検索する" }));
    await screen.findByText("Controlled AI evidence.");
  }

  it("does not expose the explicit AI button before retrieval evidence exists", () => {
    render(<RagPage />);
    expect(screen.queryByRole("button", { name: "AI分析" })).not.toBeInTheDocument();
  });

  it("does not expose AI analysis without analysis.execute", async () => {
    await showEvidence(vi.fn().mockResolvedValueOnce(retrievalResponse([evidenceItem])), false);
    expect(screen.queryByRole("button", { name: "AI分析" })).not.toBeInTheDocument();
  });

  it("cancels confirmation without sending an AI request", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(retrievalResponse([evidenceItem]));
    vi.stubGlobal("confirm", vi.fn().mockReturnValue(false));
    await showEvidence(fetchMock);
    fireEvent.click(screen.getByRole("button", { name: "AI分析" }));
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("shows Stub, estimated input and output cap in confirmation", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(retrievalResponse([evidenceItem]));
    const confirm = vi.fn().mockReturnValue(false);
    vi.stubGlobal("confirm", confirm);
    await showEvidence(fetchMock);
    fireEvent.click(screen.getByRole("button", { name: "AI分析" }));
    expect(confirm.mock.calls[0][0]).toMatch(/Stub/);
    expect(confirm.mock.calls[0][0]).toMatch(/推定入力/);
    expect(confirm.mock.calls[0][0]).toMatch(/256 tokens/);
  });

  it("sends only stable evidence refs, confirmation and an idempotency header", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(retrievalResponse([evidenceItem]))
      .mockResolvedValueOnce(aiSuccessResponse());
    vi.stubGlobal("confirm", vi.fn().mockReturnValue(true));
    await showEvidence(fetchMock);
    fireEvent.click(screen.getByRole("button", { name: "AI分析" }));
    await screen.findByText(/Usage: 12 \+ 8 = 20/);
    const [, init] = fetchMock.mock.calls[1] as [string, RequestInit];
    const body = JSON.parse(String(init.body));
    expect(body).toEqual({ question: "controlled evidence", evidence: [{ document_id: "doc-ai", chunk_id: "chunk-ai", score: 0.95 }], confirmed: true });
    expect(JSON.stringify(body)).not.toContain("Controlled AI evidence");
    expect((init.headers as Record<string, string>)["Idempotency-Key"]).toMatch(/^ai-/);
  });

  it("renders trusted usage, synthetic cost and model after success", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(retrievalResponse([evidenceItem])).mockResolvedValueOnce(aiSuccessResponse());
    vi.stubGlobal("confirm", vi.fn().mockReturnValue(true));
    await showEvidence(fetchMock);
    fireEvent.click(screen.getByRole("button", { name: "AI分析" }));
    expect(await screen.findByText("Cost: 0.00001800 USD")).toBeInTheDocument();
    expect(screen.getByText(/stub \/ stub-enterprise-v1 \/ succeeded/)).toBeInTheDocument();
  });

  it("renders quota 429 as a structured error", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(retrievalResponse([evidenceItem])).mockResolvedValueOnce(jsonResponse({ success: false, request_id: "q", data: null, error: { code: "llm_quota_exceeded", message: "Daily quota exceeded", detail: {} } }, 429));
    vi.stubGlobal("confirm", vi.fn().mockReturnValue(true));
    await showEvidence(fetchMock);
    fireEvent.click(screen.getByRole("button", { name: "AI分析" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("[llm_quota_exceeded] Daily quota exceeded");
  });

  it("renders permission 403 as a structured error", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(retrievalResponse([evidenceItem])).mockResolvedValueOnce(jsonResponse({ success: false, request_id: "f", data: null, error: { code: "forbidden", message: "Forbidden", detail: {} } }, 403));
    vi.stubGlobal("confirm", vi.fn().mockReturnValue(true));
    await showEvidence(fetchMock);
    fireEvent.click(screen.getByRole("button", { name: "AI分析" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("[forbidden] Forbidden");
  });

  it("renders evidence 422 as a structured error", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(retrievalResponse([evidenceItem])).mockResolvedValueOnce(jsonResponse({ success: false, request_id: "e", data: null, error: { code: "evidence_invalid", message: "Evidence unavailable", detail: {} } }, 422));
    vi.stubGlobal("confirm", vi.fn().mockReturnValue(true));
    await showEvidence(fetchMock);
    fireEvent.click(screen.getByRole("button", { name: "AI分析" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("[evidence_invalid] Evidence unavailable");
  });

  it("reuses the same idempotency key after a provider failure", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(retrievalResponse([evidenceItem]))
      .mockResolvedValueOnce(jsonResponse({ success: false, request_id: "p", data: null, error: { code: "provider_failed", message: "Provider failed", detail: {} } }, 502))
      .mockResolvedValueOnce(aiSuccessResponse());
    vi.stubGlobal("confirm", vi.fn().mockReturnValue(true));
    await showEvidence(fetchMock);
    fireEvent.click(screen.getByRole("button", { name: "AI分析" }));
    await screen.findByText(/provider_failed/);
    fireEvent.click(screen.getByRole("button", { name: "AI分析" }));
    await screen.findByText(/Usage: 12 \+ 8 = 20/);
    const first = (fetchMock.mock.calls[1][1].headers as Record<string, string>)["Idempotency-Key"];
    const second = (fetchMock.mock.calls[2][1].headers as Record<string, string>)["Idempotency-Key"];
    expect(second).toBe(first);
  });
});

function aiSuccessResponse() {
  return jsonResponse({ success: true, request_id: "ai", error: null, data: {
    analysis_id: "ana-1", answer: "Stub AI analysis", citations: [], provider: "stub",
    model: "stub-enterprise-v1", usage: { input_tokens: 12, output_tokens: 8, total_tokens: 20 },
    cost: "0.00001800", currency: "USD", status: "succeeded", created_at: "2026-07-17T00:00:00Z",
  } }, 200);
}
