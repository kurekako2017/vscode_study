import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { chunkList, documentDetail, documentList, jsonResponse } from "../test/page-test-helpers";
import { DocumentsPage } from "./DocumentsPage";

describe("DocumentsPage", () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("shows document list, detail, and chunk count", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(documentList([{
        document_id: "doc-1",
        title: "Monthly Policy",
        description: "Internal monthly guidance",
        owner: "analysis-team",
        created_at: "2026-07-08T00:00:00Z",
        updated_at: "2026-07-09T00:00:00Z",
        version: 1,
        language: "ja",
        document_type: "markdown",
        status: "uploaded",
        tags: ["policy"],
        source: null,
        checksum: "sha256:doc-1",
      }]))
      .mockResolvedValueOnce(documentDetail())
      .mockResolvedValueOnce(chunkList([
        {
          document_id: "doc-1",
          version: 1,
          chunk_id: "chunk-1",
          chunk_index: 0,
          content: "Paragraph one",
          character_count: 13,
          metadata: {
            document_id: "doc-1",
            title: "Monthly Policy",
            description: "Internal monthly guidance",
            owner: "analysis-team",
            created_at: "2026-07-08T00:00:00Z",
            updated_at: "2026-07-09T00:00:00Z",
            version: 1,
            language: "ja",
            document_type: "markdown",
            status: "validated",
            tags: ["policy"],
            source: null,
            checksum: "sha256:doc-1",
          },
          created_at: "2026-07-09T00:00:00Z",
        },
      ]));
    vi.stubGlobal("fetch", fetchMock);

    render(<DocumentsPage />);

    expect(await screen.findByText("Monthly Policy")).toBeInTheDocument();
    expect(await screen.findByText("Chunk 数")).toBeInTheDocument();
    expect(await screen.findByText("Paragraph one")).toBeInTheDocument();
    expect(screen.getByText("业务测试与源码学习")).toBeInTheDocument();
    expect(screen.getByText("DOC-BIZ-001")).toBeInTheDocument();
    expect(screen.getAllByText(/POST \/api\/v1\/documents/).length).toBeGreaterThan(0);
    expect(screen.getByText("标准操作流程：将企业资料准备为可检索 Chunk")).toBeInTheDocument();
    expect(screen.getByText("步骤 2：上传文档")).toBeInTheDocument();
    expect(screen.getByText("步骤 3：执行 Import")).toBeInTheDocument();
    expect(screen.getByText("步骤 4：执行 Chunk")).toBeInTheDocument();
    expect(screen.getByText("步骤 5：进入 RAG検索")).toBeInTheDocument();
    expect(screen.getByText("Archive 维护场景，不是标准上传流程。")).toBeInTheDocument();
    expect(screen.getAllByText(/409 document_archived/).length).toBeGreaterThan(0);
    expect(screen.getByLabelText("文書管理 上一步下一步")).toHaveTextContent("下一步：RAG検索");
    expect(screen.getByLabelText("文書管理 上一步下一步")).toHaveTextContent("推荐 Case：RAG-BIZ-001");
  });

  it("shows empty state when there are no documents", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(documentList()));

    render(<DocumentsPage />);

    expect(await screen.findByText("文書はまだありません。ファイルをアップロードして文書ワークフローを開始してください。")).toBeInTheDocument();
  });

  it("shows document list API error and allows refresh retry", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(jsonResponse({
        success: false,
        request_id: "request-doc-error",
        data: null,
        error: { code: "DOCUMENT_LIST_ERROR", message: "List failed", detail: {} },
      }, 500))
      .mockResolvedValueOnce(documentList());
    vi.stubGlobal("fetch", fetchMock);

    render(<DocumentsPage />);

    expect(await screen.findByRole("alert")).toHaveTextContent("[DOCUMENT_LIST_ERROR] List failed");
    fireEvent.click(screen.getByRole("button", { name: "再試行 / 更新" }));
    expect(await screen.findByText("文書はまだありません。ファイルをアップロードして文書ワークフローを開始してください。")).toBeInTheDocument();
  });

  it("uploads a document successfully and refreshes the list", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(documentList())
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-upload",
        data: {
          upload_id: "upload-1",
          document_id: "doc-9",
          status: "completed",
          progress: 100,
          created_at: "2026-07-09T00:00:00Z",
          updated_at: "2026-07-09T00:00:00Z",
          error_code: null,
          error_message: null,
        },
        error: null,
      }, 201))
      .mockResolvedValueOnce(documentList([{
        document_id: "doc-9",
        title: "budget.csv",
        description: null,
        owner: "analysis-team",
        created_at: "2026-07-09T00:00:00Z",
        updated_at: "2026-07-09T00:00:00Z",
        version: 1,
        language: "ja",
        document_type: "csv",
        status: "uploaded",
        tags: ["finance"],
        source: null,
        checksum: "sha256:doc-9",
      }]))
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-doc-9",
        data: {
          document_id: "doc-9",
          title: "budget.csv",
          description: null,
          owner: "analysis-team",
          created_at: "2026-07-09T00:00:00Z",
          updated_at: "2026-07-09T00:00:00Z",
          version: 1,
          language: "ja",
          document_type: "csv",
          status: "uploaded",
          tags: ["finance"],
          source: null,
          checksum: "sha256:doc-9",
        },
        error: null,
      }, 200))
      .mockResolvedValueOnce(chunkList());
    vi.stubGlobal("fetch", fetchMock);

    render(<DocumentsPage />);

    const file = new File(["month,sales"], "budget.csv", { type: "text/csv" });
    fireEvent.change(screen.getByLabelText("ファイル"), { target: { files: [file] } });
    fireEvent.change(screen.getByLabelText("タグ（カンマ区切り）"), { target: { value: "finance" } });
    fireEvent.click(screen.getByRole("button", { name: "文書をアップロード" }));

    expect(await screen.findByRole("status")).toHaveTextContent("アップロードが完了しました: doc-9");
    expect((await screen.findAllByText("budget.csv")).length).toBeGreaterThan(0);
  });

  it("shows upload failure from backend", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(documentList())
      .mockResolvedValueOnce(jsonResponse({
        success: false,
        request_id: "request-upload-fail",
        data: null,
        error: { code: "missing_title", message: "Title required", detail: {} },
      }, 422));
    vi.stubGlobal("fetch", fetchMock);

    render(<DocumentsPage />);

    const file = new File(["# doc"], "missing.md", { type: "text/markdown" });
    fireEvent.change(screen.getByLabelText("ファイル"), { target: { files: [file] } });
    fireEvent.change(screen.getByLabelText("タイトル"), { target: { value: "Missing" } });
    fireEvent.click(screen.getByRole("button", { name: "文書をアップロード" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("[missing_title] Title required");
  });

  it("archives a document and refreshes current detail", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(documentList([{
        document_id: "doc-1",
        title: "Monthly Policy",
        description: "Internal monthly guidance",
        owner: "analysis-team",
        created_at: "2026-07-08T00:00:00Z",
        updated_at: "2026-07-09T00:00:00Z",
        version: 1,
        language: "ja",
        document_type: "markdown",
        status: "uploaded",
        tags: ["policy"],
        source: null,
        checksum: "sha256:doc-1",
      }]))
      .mockResolvedValueOnce(documentDetail())
      .mockResolvedValueOnce(chunkList())
      .mockResolvedValueOnce(jsonResponse({
        success: true,
        request_id: "request-archive",
        data: { document_id: "doc-1", status: "archived" },
        error: null,
      }, 202))
      .mockResolvedValueOnce(documentList())
      .mockResolvedValueOnce(documentDetail({ status: "archived" }))
      .mockResolvedValueOnce(chunkList());
    vi.stubGlobal("fetch", fetchMock);

    render(<DocumentsPage />);

    expect(await screen.findByText("Monthly Policy")).toBeInTheDocument();
    fireEvent.click(await screen.findByRole("button", { name: "アーカイブ" }));

    expect(await screen.findByRole("status")).toHaveTextContent("アーカイブを受け付けました: doc-1 (archived)");
  });
});
