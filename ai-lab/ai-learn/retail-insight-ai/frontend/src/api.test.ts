import { afterEach, describe, expect, it, vi } from "vitest";

import { ApiClientError, createTask } from "./api";

describe("API Client", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("unwraps data from a successful API response", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      success: true,
      request_id: "request-success",
      data: { task_id: "task-success", status: "queued" },
      error: null,
    }), { status: 202 })));

    await expect(createTask("在庫を確認", "kpi")).resolves.toEqual({
      task_id: "task-success",
      status: "queued",
    });
  });

  it("throws ApiClientError from a failed API response", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      success: false,
      request_id: "request-failure",
      data: null,
      error: {
        code: "VALIDATION_ERROR",
        message: "Request validation failed",
        detail: { field: "question" },
      },
    }), { status: 422 })));

    const error = await createTask("", "kpi").catch((reason: unknown) => reason);
    expect(error).toBeInstanceOf(ApiClientError);
    expect(error).toMatchObject({
      code: "VALIDATION_ERROR",
      message: "Request validation failed",
      detail: { field: "question" },
    });
  });
});
