import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { documentList, jsonResponse } from "../test/page-test-helpers";
import { DocumentsPage } from "./DocumentsPage";

describe("DocumentsPage Document→RAG handoff", () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("enables 使用此文档检索 when searchable and navigates with document_id", async () => {
    const list = documentList([
      {
        document_id: "doc-searchable-1",
        title: "Searchable Doc",
        description: null,
        owner: "analysis-team",
        created_at: "2026-07-08T00:00:00Z",
        updated_at: "2026-07-09T00:00:00Z",
        version: 1,
        language: "ja",
        document_type: "markdown",
        status: "validated",
        tags: ["scenario01"],
        source: null,
        checksum: "sha256:doc-1",
        chunk_count: 3,
        searchable: true,
        archived: false,
      },
      {
        document_id: "doc-not-ready",
        title: "Not Ready",
        description: null,
        owner: "analysis-team",
        created_at: "2026-07-08T00:00:00Z",
        updated_at: "2026-07-09T00:00:00Z",
        version: 1,
        language: "ja",
        document_type: "markdown",
        status: "uploaded",
        tags: [],
        source: null,
        checksum: "sha256:doc-2",
        chunk_count: 0,
        searchable: false,
        archived: false,
      },
    ]);
    const detail = jsonResponse({
      success: true,
      request_id: "detail",
      data: {
        document_id: "doc-searchable-1",
        title: "Searchable Doc",
        description: null,
        owner: "analysis-team",
        created_at: "2026-07-08T00:00:00Z",
        updated_at: "2026-07-09T00:00:00Z",
        version: 1,
        language: "ja",
        document_type: "markdown",
        status: "validated",
        tags: ["scenario01"],
        source: null,
        checksum: "sha256:doc-1",
        chunk_count: 3,
        searchable: true,
        archived: false,
      },
      error: null,
    }, 200);
    const chunks = jsonResponse({
      success: true,
      request_id: "chunks",
      data: { document_id: "doc-searchable-1", version: 1, items: [], next_cursor: null },
      error: null,
    }, 200);
    const fetchMock = vi.fn(async (input: RequestInfo) => {
      const url = String(input);
      if (url.includes("/chunks")) return chunks;
      if (url.match(/\/documents\/[^?/]+$/)) return detail;
      return list;
    });
    vi.stubGlobal("fetch", fetchMock);

    const pushState = vi.spyOn(window.history, "pushState");
    render(<DocumentsPage />);

    expect(await screen.findByText("Searchable Doc")).toBeInTheDocument();
    expect(screen.getByText("doc-searchable-1")).toBeInTheDocument();
    expect(screen.getAllByText(/searchable:/i).length).toBeGreaterThan(0);

    const buttons = screen.getAllByRole("button", { name: "使用此文档检索" });
    expect(buttons[0]).not.toBeDisabled();
    expect(buttons[1]).toBeDisabled();

    fireEvent.click(buttons[0]);
    expect(pushState).toHaveBeenCalled();
    const url = String(pushState.mock.calls.at(-1)?.[2] ?? "");
    expect(url).toContain("/rag?document_id=doc-searchable-1");
  });
});
