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

    expect(screen.getByRole("heading", { name: "Dashboard" })).toBeInTheDocument();
    expect(screen.getByText("Repository")).toBeInTheDocument();
    expect(screen.getByText("InMemory")).toBeInTheDocument();
    expect(screen.getAllByText("Real LLM").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Disabled").length).toBeGreaterThan(0);
  });

  it("highlights the current page in top navigation", async () => {
    render(<App />);

    expect(screen.getByRole("button", { name: "Dashboard" })).toHaveAttribute("aria-current", "page");
    fireEvent.click(screen.getByRole("button", { name: "Documents" }));
    expect(screen.getByRole("button", { name: "Documents" })).toHaveAttribute("aria-current", "page");
  });

  it("navigates to tasks from dashboard shortcut", async () => {
    render(<App />);

    fireEvent.click(screen.getByRole("button", { name: "Open Tasks" }));

    expect(screen.getByRole("heading", { name: "Analysis / Tasks" })).toBeInTheDocument();
    expect(screen.getByText("Create a deterministic analysis task, observe SSE progress, and inspect the final generated report from the current local workflow.")).toBeInTheDocument();
  });

  it("navigates to documents from dashboard shortcut", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      success: true,
      request_id: "request-doc-list",
      data: { items: [], next_cursor: null },
      error: null,
    }), { status: 200 })));

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Open Documents" }));

    expect(await screen.findByRole("heading", { name: "Documents" })).toBeInTheDocument();
  });

  it("navigates to rag from dashboard shortcut", async () => {
    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Open RAG" }));

    expect(screen.getByRole("heading", { name: "RAG" })).toBeInTheDocument();
  });

  it("navigates to approval from dashboard shortcut", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      success: true,
      request_id: "request-approval-list",
      data: { items: [], next_cursor: null },
      error: null,
    }), { status: 200 })));

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Open Approval" }));

    expect(await screen.findByRole("heading", { name: "Approval" })).toBeInTheDocument();
  });
});
