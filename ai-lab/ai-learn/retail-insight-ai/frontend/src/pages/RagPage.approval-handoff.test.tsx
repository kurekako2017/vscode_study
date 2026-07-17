import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { jsonResponse } from "../test/page-test-helpers";
import { RagPage } from "./RagPage";

describe("RagPage Report→Approval handoff", () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("shows task/report ids after report success and submits approval", async () => {
    const reportPayload = {
      report_id: "rep-1",
      report_version_id: "rv-1",
      task_id: "task-report-1",
      title: "Board Report",
      executive_summary: "Summary for board",
      kpi_findings: [],
      risks: [],
      recommendations: [],
      citations: [{ document_id: "d1", chunk_id: "c1", score: "1.0", excerpt: "e" }],
      provider: "stub-high-quality",
      model: "stub-high-quality-v1",
      route_tier: "high_quality",
      usage: { input_tokens: 10, output_tokens: 20, total_tokens: 30 },
      estimated_cost: "0.01",
      actual_cost: "0.01",
      currency: "USD",
      status: "succeeded",
      analysis_id: "an-1",
      usage_id: "u-1",
      created_at: "2026-07-17T00:00:00Z",
    };

    const fetchMock = vi.fn(async (input: RequestInfo, init?: RequestInit) => {
      const url = String(input);
      if (url.includes("/document-retrieval/search")) {
        return jsonResponse({
          success: true,
          request_id: "r1",
          data: {
            results: [
              {
                document_id: "d1",
                chunk_id: "c1",
                chunk_index: 0,
                content_excerpt: "evidence",
                score: 0.9,
                source: { source_type: "upload", uri: "u", label: null, external_id: null },
                metadata: {
                  document_id: "d1",
                  title: "Doc",
                  description: null,
                  owner: "o",
                  created_at: "2026-07-17T00:00:00Z",
                  updated_at: "2026-07-17T00:00:00Z",
                  version: 1,
                  language: "ja",
                  document_type: "markdown",
                  status: "validated",
                  tags: [],
                  source: null,
                  checksum: "x",
                },
              },
            ],
            total: 1,
            query: "q",
            retrieval_mode: "keyword",
          },
          error: null,
        }, 200);
      }
      if (url.includes("/ai-analysis")) {
        return jsonResponse({
          success: true,
          request_id: "a1",
          data: {
            analysis_id: "an-1",
            answer: "AI answer",
            citations: [{ document_id: "d1", chunk_id: "c1", score: "0.9", excerpt: "evidence" }],
            provider: "stub-low-cost",
            model: "stub-low-cost-v1",
            route_tier: "low_cost",
            usage: { input_tokens: 1, output_tokens: 2, total_tokens: 3 },
            cost: "0.001",
            currency: "USD",
            status: "succeeded",
            created_at: "2026-07-17T00:00:00Z",
          },
          error: null,
        }, 200);
      }
      if (url.includes("/executive-reports")) {
        return jsonResponse({
          success: true,
          request_id: "e1",
          data: reportPayload,
          error: null,
        }, 200);
      }
      if (url.includes("/submit-approval")) {
        return jsonResponse(
          {
            success: true,
            request_id: "s1",
            data: {
              approval_id: "apr-1",
              task_id: "task-report-1",
              report_version_id: "rv-1",
              status: "pending_approval",
              requested_by: "employee",
              decided_by: null,
              comment: null,
              rejection_reason: null,
              created_at: "2026-07-17T00:00:00Z",
              updated_at: "2026-07-17T00:00:00Z",
              history: [],
            },
            error: null,
          },
          201,
        );
      }
      return jsonResponse({ success: false, request_id: "x", data: null, error: { code: "unexpected", message: url, detail: {} } }, 500);
    });
    vi.stubGlobal("fetch", fetchMock);
    vi.spyOn(window, "confirm").mockReturnValue(true);
    const pushState = vi.spyOn(window.history, "pushState");

    render(<RagPage canRetrieve canAnalyze />);

    fireEvent.change(screen.getByLabelText("検索語"), { target: { value: "関東 売上" } });
    fireEvent.click(screen.getByRole("button", { name: "検索する" }));
    expect(await screen.findByText("evidence")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "AI分析" }));
    expect(await screen.findByText("AI answer")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "生成取締役会報告" }));
    expect(await screen.findByLabelText("报告审批传递")).toBeInTheDocument();
    const handoff = screen.getByLabelText("报告审批传递");
    expect(handoff).toHaveTextContent("task-report-1");
    expect(handoff).toHaveTextContent("rep-1");
    expect(handoff).toHaveTextContent("rv-1");
    expect(screen.getByRole("button", { name: "提交审批" })).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "提交审批" }));
    await waitFor(() => {
      expect(pushState).toHaveBeenCalled();
    });
    const url = String(pushState.mock.calls.at(-1)?.[2] ?? "");
    expect(url).toContain("/approval?approval_id=apr-1");
    const submitCall = fetchMock.mock.calls.find((call) => String(call[0]).includes("submit-approval"));
    expect(submitCall).toBeTruthy();
    expect(String(submitCall?.[0])).toContain("/api/v1/reports/task-report-1/submit-approval");
    const submitHeaders = new Headers((submitCall?.[1] as RequestInit | undefined)?.headers);
    expect(submitHeaders.get("Idempotency-Key")).toBe("approval-submit-task-report-1");
  });

  it("shows pending Approval message on 409 without navigating", async () => {
    const reportPayload = {
      report_id: "rep-2",
      report_version_id: "rv-2",
      task_id: "task-report-2",
      title: "Board Report",
      executive_summary: "Summary",
      kpi_findings: [],
      risks: [],
      recommendations: [],
      citations: [{ document_id: "d1", chunk_id: "c1", score: "1.0", excerpt: "e" }],
      provider: "stub-high-quality",
      model: "stub-high-quality-v1",
      route_tier: "high_quality",
      usage: { input_tokens: 10, output_tokens: 20, total_tokens: 30 },
      estimated_cost: "0.01",
      actual_cost: "0.01",
      currency: "USD",
      status: "succeeded",
      analysis_id: "an-2",
      usage_id: "u-2",
      created_at: "2026-07-17T00:00:00Z",
    };
    const fetchMock = vi.fn(async (input: RequestInfo) => {
      const url = String(input);
      if (url.includes("/document-retrieval/search")) {
        return jsonResponse({
          success: true,
          request_id: "r1",
          data: {
            results: [
              {
                document_id: "d1",
                chunk_id: "c1",
                chunk_index: 0,
                content_excerpt: "evidence",
                score: 0.9,
                source: { source_type: "upload", uri: "u", label: null, external_id: null },
                metadata: {
                  document_id: "d1",
                  title: "Doc",
                  description: null,
                  owner: "o",
                  created_at: "2026-07-17T00:00:00Z",
                  updated_at: "2026-07-17T00:00:00Z",
                  version: 1,
                  language: "ja",
                  document_type: "markdown",
                  status: "validated",
                  tags: [],
                  source: null,
                  checksum: "x",
                },
              },
            ],
            total: 1,
            query: "q",
            retrieval_mode: "keyword",
          },
          error: null,
        }, 200);
      }
      if (url.includes("/ai-analysis")) {
        return jsonResponse({
          success: true,
          request_id: "a1",
          data: {
            analysis_id: "an-2",
            answer: "AI answer",
            citations: [{ document_id: "d1", chunk_id: "c1", score: "0.9", excerpt: "evidence" }],
            provider: "stub-low-cost",
            model: "stub-low-cost-v1",
            route_tier: "low_cost",
            usage: { input_tokens: 1, output_tokens: 2, total_tokens: 3 },
            cost: "0.001",
            currency: "USD",
            status: "succeeded",
            created_at: "2026-07-17T00:00:00Z",
          },
          error: null,
        }, 200);
      }
      if (url.includes("/executive-reports")) {
        return jsonResponse({ success: true, request_id: "e1", data: reportPayload, error: null }, 200);
      }
      if (url.includes("/submit-approval")) {
        return jsonResponse(
          {
            success: false,
            request_id: "s1",
            data: null,
            error: {
              code: "approval_already_submitted",
              message: "Approval already submitted",
              detail: { task_id: "task-report-2" },
            },
          },
          409,
        );
      }
      return jsonResponse({ success: false, request_id: "x", data: null, error: { code: "unexpected", message: url, detail: {} } }, 500);
    });
    vi.stubGlobal("fetch", fetchMock);
    vi.spyOn(window, "confirm").mockReturnValue(true);
    const pushState = vi.spyOn(window.history, "pushState");

    render(<RagPage canRetrieve canAnalyze />);
    fireEvent.change(screen.getByLabelText("検索語"), { target: { value: "関東 売上" } });
    fireEvent.click(screen.getByRole("button", { name: "検索する" }));
    expect(await screen.findByText("evidence")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "AI分析" }));
    expect(await screen.findByText("AI answer")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "生成取締役会報告" }));
    expect(await screen.findByRole("button", { name: "提交审批" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "提交审批" }));
    expect(await screen.findByText(/已有 pending Approval/)).toBeInTheDocument();
    expect(pushState).not.toHaveBeenCalled();
  });
});
