import { afterEach, describe, expect, it, vi } from "vitest";

import { createQuestion, decideApproval } from "./api";

describe("API client", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("creates a question from the success envelope", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      success: true,
      request_id: "req-1",
      data: { question_id: "q-1", status: "received", risk_level: null, approval_id: null, error_code: null, created_at: "now", updated_at: "now" },
      error: null,
    }), { status: 202 })));
    await expect(createQuestion("社内手順を確認")).resolves.toMatchObject({ question_id: "q-1" });
  });

  it("uses the explicit approval action endpoint", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({
      success: true,
      request_id: "req-2",
      data: { approval_id: "a-1", question_id: "q-1", question: "契約", risk_level: "HIGH", status: "approved", created_at: "now", decided_at: "now" },
      error: null,
    }), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    await decideApproval("a-1", "approve");
    expect(fetchMock).toHaveBeenCalledWith("/api/approvals/a-1/approve", { method: "POST" });
  });
});
