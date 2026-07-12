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
    fireEvent.change(screen.getByLabelText("Query"), { target: { value: "monthly policy" } });
    fireEvent.click(screen.getByRole("button", { name: "Search Retrieval" }));

    expect(await screen.findByRole("status")).toHaveTextContent("Retrieval mode: keyword / Total matches: 1");
    expect(await screen.findByText("Monthly policy evidence.")).toBeInTheDocument();
  });

  it("shows empty retrieval state from backend", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValueOnce(retrievalResponse()));

    render(<RagPage />);
    fireEvent.change(screen.getByLabelText("Query"), { target: { value: "no match" } });
    fireEvent.click(screen.getByRole("button", { name: "Search Retrieval" }));

    expect(await screen.findByText("No retrieval results found.")).toBeInTheDocument();
  });

  it("shows grounded internal rag answer and citations", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValueOnce(ragAnswerResponse()));

    render(<RagPage />);
    fireEvent.change(screen.getByLabelText("Question"), { target: { value: "What is the monthly policy?" } });
    fireEvent.click(screen.getByRole("button", { name: "Generate Answer" }));

    expect(await screen.findByRole("status")).toHaveTextContent("Answer mode: extractive");
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
    fireEvent.change(screen.getByLabelText("Question"), { target: { value: "rare token" } });
    fireEvent.click(screen.getByRole("button", { name: "Generate Answer" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("[insufficient_context] No usable evidence");
  });
});
