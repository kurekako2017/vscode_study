import { describe, expect, it } from "vitest";

import {
  getPermissionsForRole,
  hasAllPermissions,
  hasAnyPermission,
  hasPermission,
  ROLE_PERMISSIONS,
} from "./permissions";

describe("frontend permission registry", () => {
  it("mirrors the frozen admin, manager, and employee mappings", () => {
    expect(ROLE_PERMISSIONS.admin).toHaveLength(10);
    expect(ROLE_PERMISSIONS.manager).toEqual([
      "documents.read",
      "documents.write",
      "documents.archive",
      "retrieval.query",
      "analysis.execute",
      "approval.submit",
      "approval.review",
      "approval.admin",
      "audit.read",
    ]);
    expect(ROLE_PERMISSIONS.employee).toEqual([
      "documents.read",
      "documents.write",
      "retrieval.query",
      "analysis.execute",
      "approval.submit",
    ]);
  });

  it("fails closed for unknown roles", () => {
    expect(getPermissionsForRole("super-admin")).toEqual([]);
    expect(hasPermission(getPermissionsForRole("unknown"), "documents.read")).toBe(false);
  });

  it("supports single, any, and all permission checks", () => {
    const employee = getPermissionsForRole("employee");
    expect(hasPermission(employee, "approval.submit")).toBe(true);
    expect(hasAnyPermission(employee, ["approval.review", "analysis.execute"])).toBe(true);
    expect(hasAllPermissions(employee, ["documents.read", "documents.write"])).toBe(true);
    expect(hasAllPermissions(employee, ["documents.read", "documents.archive"])).toBe(false);
  });
});
