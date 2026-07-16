import { describe, expect, it } from "vitest";

import { buildTestJwt } from "../test/auth-test-helpers";
import { parseJwtIdentity } from "./jwtIdentity";

describe("JWT identity parsing", () => {
  it("reads only the frozen identity claims", () => {
    const token = buildTestJwt("manager", "manager", "user-manager", 2_000);
    expect(parseJwtIdentity(token, 1_500)).toEqual({
      sub: "user-manager",
      user_id: "user-manager",
      username: "manager",
      role: "manager",
      iat: 200,
      exp: 2_000,
      jti: "jti-manager",
    });
  });

  it("rejects expired, damaged, and incomplete tokens", () => {
    expect(parseJwtIdentity(buildTestJwt("employee", "employee", "user-employee", 1_000), 1_000)).toBeNull();
    expect(parseJwtIdentity("not-a-jwt")).toBeNull();
    expect(parseJwtIdentity("a.b.c")).toBeNull();
  });
});
