import { describe, expect, it } from "vitest";

import { isSensitiveKey, redactValue, safeSummary, sanitizeRecord } from "./sanitize";

describe("learning sanitize", () => {
  it("redacts access tokens and passwords", () => {
    expect(isSensitiveKey("accessToken")).toBe(true);
    expect(isSensitiveKey("password")).toBe(true);
    expect(isSensitiveKey("Authorization")).toBe(true);
    expect(redactValue("accessToken", "secret-value")).toBe("[REDACTED]");
    expect(redactValue("Authorization", "Bearer abc")).toBe("[REDACTED]");
  });

  it("summarizes objects and arrays without deep stringify", () => {
    expect(safeSummary([1, 2, 3])).toBe("Array(3)");
    expect(safeSummary({ a: 1, b: 2 })).toContain("Object{");
  });

  it("sanitizes records for trace payload", () => {
    const result = sanitizeRecord({
      accessToken: "abc",
      count: 2,
      label: "ok",
    });
    expect(result.accessToken).toBe("[REDACTED]");
    expect(result.count).toBe(2);
    expect(result.label).toBe("ok");
  });
});
