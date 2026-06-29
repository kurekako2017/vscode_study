import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import App from "./App";


describe("App", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("renders the question form", () => {
    render(<App />);
    expect(screen.getByRole("heading", { name: "社内文書検索・承認ワークフローAIエージェント" })).toBeInTheDocument();
    expect(screen.getByLabelText("確認したい内容")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Workflow を開始" })).toBeInTheDocument();
  });

  it("displays an API error", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      success: false,
      request_id: "req-error",
      data: null,
      error: { code: "VALIDATION_ERROR", message: "Request validation failed", detail: {} },
    }), { status: 422, headers: { "Content-Type": "application/json" } })));

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Workflow を開始" }));

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent("[VALIDATION_ERROR] Request validation failed");
    });
  });
});
